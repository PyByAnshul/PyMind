import chainlit as cl
import traceback
import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
from tinydb import TinyDB, Query
from datetime import datetime
import mimetypes
import base64

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API'))

logging.basicConfig(filename='chat.log', level=logging.INFO)

db = TinyDB('chat_history.json')
User = Query()

# System message to set AI personality
SYSTEM_MESSAGE = """You are a helpful, friendly, and knowledgeable AI assistant. 
You provide detailed, accurate, and engaging responses. 
You can handle various topics and maintain a professional yet approachable tone."""

def build_prompt_from_history(history, max_turns=5):
    convo = SYSTEM_MESSAGE + "\n\n"
    for turn in history[-max_turns:]:
        if "user" in turn:
            convo += "User: " + turn["user"] + "\n"
        elif "bot" in turn:
            convo += "Bot: " + turn["bot"] + "\n"
    convo += "User: "
    return convo

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@cl.on_chat_start
async def main():
    # Initialize empty history for user session
    session_id = str(datetime.now().timestamp())
    cl.user_session.set("session_id", session_id)
    
    if not db.search(User.id == session_id):
        db.insert({'id': session_id, 'history': []})
    
    # Create welcome messages
    await cl.Message(
        content="Welcome to PyMind!"
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    try:
        session_id = cl.user_session.get("session_id")
        user_data = db.get(User.id == session_id)
        history = user_data.get('history', []) if user_data else []
        
        msg_text = message.content.strip()

        # Commands
        if msg_text.lower() == "/reset":
            db.update({'history': []}, User.id == session_id)
            await cl.Message(content="Chat history cleared!").send()
            return

        if msg_text.lower() == "/help":
            help_msg = """Available Commands:
• /reset - Clear chat history
• /help - Show this message
• /history - Show chat history

Features:
• File upload support
• Markdown formatting
• Real-time streaming responses
• Persistent chat history"""
            await cl.Message(content=help_msg).send()
            return

        if msg_text.lower() == "/history":
            if history:
                history_text = "\n\n".join(
                    f"[{turn.get('timestamp', 'N/A')}] User: {turn['user']}\nBot: {turn.get('bot', '')}" 
                    for turn in history
                )
                await cl.Message(content=f"Your chat history:\n\n{history_text}").send()
            else:
                await cl.Message(content="No chat history yet.").send()
            return

        # Handle file uploads if present
        if message.elements:
            for element in message.elements:
                if hasattr(element, 'type') and element.type == 'file':
                    try:
                        file_content = await element.get_content()
                        file_name = element.name
                        file_type = mimetypes.guess_type(file_name)[0]
                        
                        # Add file information to the message
                        msg_text += f"\n[Attached file: {file_name} ({file_type})]"
                        
                        # Create a preview element for the file
                        preview_element = cl.Text(
                            name=f"file_preview_{file_name}",
                            content=f"File uploaded: {file_name}",
                            display="inline"
                        )
                        await cl.Message(content=f"File '{file_name}' received!", elements=[preview_element]).send()
                    except Exception as e:
                        await cl.Message(content=f"Error processing file {element.name}: {str(e)}").send()

        # Add user message to history with timestamp
        history.append({
            "user": msg_text,
            "timestamp": get_timestamp()
        })
        db.update({'history': history}, User.id == session_id)

        # Build prompt from history
        prompt = build_prompt_from_history(history)

        # Show thinking indicator
        thinking_msg = cl.Message(content="Thinking...", author="PyMind")
        await thinking_msg.send()

        # Generate response using Gemini
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(prompt)

        if response and response.text:
            full_response = response.text
        else:
            full_response = "Error: Gemini returned no response."

        # Remove thinking message and send the actual response
        await thinking_msg.remove()
        await cl.Message(content=full_response, author="PyMind").send()

        # Update history with bot reply
        history[-1]["bot"] = full_response
        history[-1]["bot_timestamp"] = get_timestamp()
        db.update({'history': history}, User.id == session_id)

        logging.info(f"User: {msg_text}")
        logging.info(f"Bot: {full_response}")

    except Exception as e:
        traceback.print_exc()
        await cl.Message(content=f"An error occurred: {str(e)}").send()

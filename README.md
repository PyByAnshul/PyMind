# PyMind - Your Intelligent Python Programming Assistant

PyMind is an AI-powered chat application built with Chainlit and Google's Gemini AI model, designed to help developers with Python programming tasks, code analysis, and learning.

## Features

- 🤖 AI-powered Python programming assistance
- 💬 Interactive chat interface
- 📁 File upload and analysis support
- 📝 Persistent chat history
- ⚡ Real-time responses
- 🎯 Command system for easy navigation
- 🔒 Session management
- 📊 Logging system

## Prerequisites

- Python 3.8 or higher
- Google API key for Gemini AI
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/PyMind.git
cd PyMind
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API=your_api_key_here
```

## Usage

1. Start the application:
```bash
chainlit run chainlit_app.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Available commands:
   - `/help` - Show available commands and features
   - `/reset` - Clear chat history
   - `/history` - View chat history

## Features in Detail

### AI Assistance
- Get help with Python programming concepts
- Code analysis and suggestions
- Debugging assistance
- Best practices recommendations

### File Handling
- Upload Python files for analysis
- Get code reviews
- Syntax checking
- Performance suggestions

### Chat History
- Persistent storage of conversations
- Session-based history management
- Timestamp tracking
- Easy history navigation

## Project Structure

```
PyMind/
├── chainlit_app.py      # Main application file
├── .chainlit/          # Chainlit configuration
├── .env                # Environment variables
├── chat_history.json   # Chat history database
├── chat.log           # Application logs
├── requirements.txt    # Project dependencies
└── README.md          # This file
```

## Dependencies

- chainlit
- google-generativeai
- python-dotenv
- tinydb

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Chainlit](https://github.com/Chainlit/chainlit) for the chat interface framework
- [Google Gemini AI](https://ai.google.dev/) for the AI model
- [TinyDB](https://tinydb.readthedocs.io/) for the database

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)
Project Link: [https://github.com/yourusername/PyMind](https://github.com/yourusername/PyMind)
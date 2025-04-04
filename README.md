# Multimodal LLM Discord Bot

A powerful Discord bot that supports conversations with multiple AI models (GPT-4o, Gemini 2.0 Flash, Gemini 2.5 Pro Experimental, DeepSeek V3), accepts image and document inputs, and maintains per-user chat history. The bot supports both thread-based conversations in servers and direct message interactions.

## Features

- **Multiple AI Models**: Switch between GPT-4o, Gemini 2.0 Flash, Gemini 2.5 Pro Experimental, and DeepSeek V3
- **Multimodal Input**: Upload and process images, PDFs, and Word documents
- **Per-User Memory**: Maintains conversation history for each user
- **Thread-Based Conversations**: Creates dedicated threads for each conversation in servers
- **Direct Message Support**: Chat privately with the bot via DMs
- **Slash Commands**: Easy-to-use Discord slash commands
- **Persistent Storage Options**: Choose between in-memory or SQLite database storage
- **Modular Architecture**: Clean separation between bot interface, backend API, and model handling

## Tech Stack

- **Bot Interface**: `discord.py`
- **API Backend**: `FastAPI`
- **Model Routing**: `LangChain`
- **Memory**: In-memory dictionary or SQLite database
- **File Parsing**: `PyMuPDF`, `python-docx`, `Pillow`
- **Environment Management**: `python-dotenv`

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))
- API keys for OpenAI, Google, and DeepSeek

### Installation

1. Clone the repository or download the source code

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on the `.env.example` template and add your API keys:
   ```
   DISCORD_BOT_TOKEN=your_discord_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   DEFAULT_MODEL=gpt-4o
   
   # Storage configuration (memory or sqlite)
   STORAGE_TYPE=memory
   
   # Database path (for SQLite storage)
   DB_PATH=sessions.db
   ```

### Running the Bot

1. Start the FastAPI backend:
   ```bash
   uvicorn backend.main:app --reload
   ```

2. In a separate terminal, start the Discord bot:
   ```bash
   python -m bot.client
   ```

## Usage

Once the bot is running and added to your Discord server, you can use the following slash commands:

- `/chat [message]` - Send a message to the AI assistant
  - In servers: Creates a new thread for the conversation
  - In DMs: Continues the conversation in the direct message channel
- `/upload [file] [question]` - Upload an image or document for context with an optional question
  - In servers: Creates a new thread for the conversation
  - In DMs: Continues the conversation in the direct message channel
- `/set_model [model]` - Change the AI model (options: gpt-4o, gemini-2.0-flash, gemini-2.5-pro-experimental, deepseek-v3)

You can also interact with the bot directly:

- **Direct Messages**: Simply send a message or upload a file to the bot in DMs
- **Thread Conversations**: Continue the conversation in threads created by the bot

## Project Structure

```
discord-llm-bot/
│
├── bot/
│   ├── client.py           # Starts the Discord bot
│   ├── commands.py         # Slash commands: /chat, /upload, /set_model
│   └── handlers.py         # Handles events, DMs, and thread conversations
│
├── backend/
│   ├── main.py             # FastAPI entrypoint
│   ├── routes.py           # /chat, /upload, /set_model endpoints
│   ├── session.py          # Session data structure
│   ├── session_manager.py  # Manages user sessions and contexts
│   ├── storage.py          # Storage backend interface
│   ├── db_storage.py       # SQLite storage implementation
│   └── config.py           # Configuration and environment variables
│
├── models/
│   ├── router.py           # Picks the right LLM using LangChain
│   ├── gpt.py              # GPT-4o wrapper
│   ├── gemini.py           # Gemini models wrapper
│   └── deepseek.py         # DeepSeek wrapper
│
├── utils/
│   ├── file_parser.py      # Convert images/docs to context
│   └── logger.py           # Logging
│
├── .env                    # API keys and tokens
├── .env.example           # Example environment variables
├── requirements.txt        # Python dependencies
└── README.md              # Setup guide and instructions
```

## Configuration Options

The bot can be configured using environment variables in the `.env` file:

- `DISCORD_BOT_TOKEN`: Your Discord bot token from the Developer Portal
- `OPENAI_API_KEY`: API key for OpenAI (GPT-4o)
- `GOOGLE_API_KEY`: API key for Google AI (Gemini models)
- `DEEPSEEK_API_KEY`: API key for DeepSeek (DeepSeek V3)
- `DEFAULT_MODEL`: Default model to use if not specified by the user (e.g., `gpt-4o`, `gemini-2.0-flash`)
- `STORAGE_TYPE`: Storage backend to use (`memory` or `sqlite`)
- `DB_PATH`: Path to the SQLite database file (when using `sqlite` storage)

## Extending the Bot

### Adding New Models

To add a new AI model:

1. Create a new wrapper in the `models/` directory
2. Update `models/router.py` to include the new model
3. Add the new model option to the `/set_model` command in `bot/commands.py`

### Implementing Different Storage Backends

The bot supports pluggable storage backends:

1. Create a new class that implements the `StorageBackend` interface in `backend/storage.py`
2. Update `backend/config.py` to include your new storage type
3. Add the necessary configuration options to `.env.example`

### Improving File Parsing

The current implementation provides basic file parsing. You can enhance it by:

- Adding support for more file types
- Implementing OCR for scanned documents
- Adding image analysis capabilities

### Enhancing Conversation Management

The bot currently supports thread-based conversations and direct messages. You can extend this by:

- Adding support for conversation summarization
- Implementing conversation export functionality
- Adding user preference management

## License

This project is licensed under the MIT License - see the LICENSE file for details.
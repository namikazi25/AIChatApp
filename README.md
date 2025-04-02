# Multimodal LLM Discord Bot

A powerful Discord bot that supports conversations with multiple AI models (GPT-4o, Gemini 1.5 Flash, DeepSeek V3), accepts image and document inputs, and maintains per-user chat history.

## Features

- **Multiple AI Models**: Switch between GPT-4o-mini, Gemini 2.0 Flash, and DeepSeek V3
- **Multimodal Input**: Upload and process images, PDFs, and Word documents
- **Per-User Memory**: Maintains conversation history for each user
- **Slash Commands**: Easy-to-use Discord slash commands
- **Modular Architecture**: Clean separation between bot interface, backend API, and model handling

## Tech Stack

- **Bot Interface**: `discord.py`
- **API Backend**: `FastAPI`
- **Model Routing**: `LangChain`
- **Memory**: In-memory dictionary (can be extended to Redis)
- **File Parsing**: `PyMuPDF`, `python-docx`, `Pillow`

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
- `/upload [file]` - Upload an image or document for context
- `/set_model [model]` - Change the AI model (options: gpt-4o, gemini-1.5-flash, deepseek-v3)

## Project Structure

```
discord-llm-bot/
│
├── bot/
│   ├── client.py           # Starts the Discord bot
│   ├── commands.py         # Slash commands: /chat, /upload, /set_model
│   └── handlers.py         # Handles events, sends to backend
│
├── backend/
│   ├── main.py             # FastAPI entrypoint
│   ├── routes.py           # /chat, /upload, /set_model
│   └── session.py          # Per-user session and memory
│
├── models/
│   ├── router.py           # Picks the right LLM using LangChain
│   ├── gpt.py              # GPT-4o wrapper
│   ├── gemini.py           # Gemini 1.5 wrapper
│   └── deepseek.py         # DeepSeek wrapper
│
├── utils/
│   ├── file_parser.py      # Convert images/docs to context
│   └── logger.py           # Logging
│
├── .env                    # API keys and tokens
├── requirements.txt        # Python dependencies
└── README.md              # Setup guide and instructions
```

## Extending the Bot

### Adding New Models

To add a new AI model:

1. Create a new wrapper in the `models/` directory
2. Update `models/router.py` to include the new model
3. Add the new model option to the `/set_model` command in `bot/commands.py`

### Improving File Parsing

The current implementation provides basic file parsing. You can enhance it by:

- Adding support for more file types
- Implementing OCR for scanned documents
- Adding image analysis capabilities

## License

This project is licensed under the MIT License - see the LICENSE file for details.
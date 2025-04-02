import os
from typing import Dict, List, Any
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.llms import GooglePalm
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()

# Set Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

async def call_gemini(message: str, memory: List[Dict[str, str]]) -> str:
    """Call the Google Gemini model"""
    try:
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Convert memory format to Gemini chat format
        chat_history = []
        for msg in memory:
            if msg["role"] == "user":
                chat_history.append({"role": "user", "parts": [msg["content"]]})
            elif msg["role"] == "assistant":
                chat_history.append({"role": "model", "parts": [msg["content"]]})
            elif msg["role"] == "system":
                # Gemini doesn't have a system role, so we'll add it as a user message
                chat_history.append({"role": "user", "parts": [f"System instruction: {msg['content']}"]})        
        
        # Start a chat session
        chat = model.start_chat(history=chat_history)
        
        # Generate response
        response = chat.send_message(message)
        
        # Return the response content
        return response.text
    except Exception as e:
        print(f"Error calling Gemini: {str(e)}")
        return f"I'm sorry, I encountered an error while processing your request with Gemini 1.5 Flash. Please try again later."
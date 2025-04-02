import os
from typing import Dict, List, Any
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set DeepSeek API key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

async def call_deepseek(message: str, memory: List[Dict[str, str]]) -> str:
    """Call the DeepSeek model"""
    try:
        # Prepare headers with API key
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }
        
        # Convert memory format to DeepSeek chat format
        messages = []
        for msg in memory:
            if msg["role"] in ["user", "assistant", "system"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Add the current message if it's not already in memory
        if not memory or memory[-1]["role"] != "user" or memory[-1]["content"] != message:
            messages.append({"role": "user", "content": message})
        
        # Prepare request payload
        payload = {
            "model": "deepseek-chat",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        # Make API request
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Return the response content
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error calling DeepSeek: {str(e)}")
        return f"I'm sorry, I encountered an error while processing your request with DeepSeek V3. Please try again later."
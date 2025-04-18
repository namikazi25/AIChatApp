import os
from typing import Dict, List, Any
import openai
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def call_gpt(message: str, memory: List[Dict[str, Any]]) -> str:
    """Call the OpenAI GPT model using LangChain"""
    try:
        # Initialize the ChatOpenAI model
        chat = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7,
            streaming=False,
            # Explicitly set proxies to None to avoid the error
            openai_proxy=None
        )
        
        # Convert memory format to LangChain message format
        messages = []
        for msg in memory:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                # Check if this is an image message
                if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                    # Create a multimodal message with image
                    image_data = msg["content"]
                    content = [
                        {"type": "text", "text": image_data["metadata"]},
                        {"type": "image_url", "image_url": {"url": f"data:{image_data['mime_type']};base64,{image_data['base64']}"}}                        
                    ]
                    messages.append(HumanMessage(content=content))
                else:
                    messages.append(SystemMessage(content=msg["content"]))
        
        # Add the current message if it's not already in memory
        if not memory or memory[-1]["role"] != "user" or memory[-1]["content"] != message:
            messages.append(HumanMessage(content=message))
        
        # Call the model
        response = chat(messages)
        
        # Return the response content
        return response.content
    except Exception as e:
        print(f"Error calling GPT: {str(e)}")
        return f"I'm sorry, I encountered an error while processing your request with GPT-4o. Please try again later."
    except Exception as e:
        print(f"Error calling GPT: {str(e)}")
        return f"I'm sorry, I encountered an error while processing your request with GPT-4o. Please try again later."
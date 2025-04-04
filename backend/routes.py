from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any, Optional
from pydantic import BaseModel
from backend.session import get_memory, add_to_memory
from models.router import get_llm_response, set_user_model
from utils.file_parser import parse_file

# Pydantic models for request validation
class ChatRequest(BaseModel):
    user_id: str
    message: str
    context_id: Optional[str] = None

class ModelRequest(BaseModel):
    user_id: str
    model: str
    context_id: Optional[str] = None

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """Process a chat message and get a response from the LLM"""
    try:
        # Get user's chat history with context if provided
        memory = get_memory(request.user_id, request.context_id)
        
        # Add user message to memory
        add_to_memory(request.user_id, {"role": "user", "content": request.message}, request.context_id)
        
        # Get response from the appropriate LLM
        response = await get_llm_response(request.user_id, request.message, memory, request.context_id)
        
        # Add assistant response to memory
        add_to_memory(request.user_id, {"role": "assistant", "content": response}, request.context_id)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.post("/upload")
async def upload(user_id: str = Form(...), file: UploadFile = File(...), question: str = Form(None), context_id: Optional[str] = Form(None)) -> Dict[str, Any]:
    """Process an uploaded file and optionally answer a question about it"""
    try:
        # Parse the uploaded file
        parsed_content = await parse_file(file)
        
        # Add file content to user's memory as system message
        if parsed_content["type"] == "image":
            # For images, store the full image data including base64
            system_message = parsed_content
            response_message = f"Image '{file.filename}' uploaded and processed successfully. The AI can now see and analyze this image."
        else:
            # For text-based files (PDF, DOCX)
            system_message = f"Content from uploaded file '{file.filename}':\n{parsed_content['content']}"
            response_message = f"File '{file.filename}' uploaded and processed successfully."
        
        add_to_memory(user_id, {"role": "system", "content": system_message}, context_id)
        
        # If a question was provided, process it immediately
        if question:
            # Add user question to memory
            add_to_memory(user_id, {"role": "user", "content": question}, context_id)
            
            # Get memory for context
            memory = get_memory(user_id, context_id)
            
            # Get response from the LLM
            response = await get_llm_response(user_id, question, memory, context_id)
            
            # Add assistant response to memory
            add_to_memory(user_id, {"role": "assistant", "content": response}, context_id)
            
            return {"response": response}
        
        return {"response": response_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/set_model")
async def set_model_route(request: ModelRequest) -> Dict[str, Any]:
    """Set the LLM model for a specific user"""
    try:
        # Validate model choice
        valid_models = ["gpt-4o", "gemini-2.0-flash", "gemini-2.5-pro-experimental", "deepseek-v3"]
        if request.model not in valid_models:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model. Choose from: {', '.join(valid_models)}"
            )
        
        # Set the user's model preference
        set_user_model(request.user_id, request.model, request.context_id)
        
        return {"response": f"Model set to {request.model}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting model: {str(e)}")
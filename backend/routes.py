from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any
from pydantic import BaseModel
from backend.session import get_memory, add_to_memory
from models.router import get_llm_response, set_user_model
from utils.file_parser import parse_file

# Pydantic models for request validation
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ModelRequest(BaseModel):
    user_id: str
    model: str

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    """Process a chat message and get a response from the LLM"""
    try:
        # Get user's chat history
        memory = get_memory(request.user_id)
        
        # Add user message to memory
        add_to_memory(request.user_id, {"role": "user", "content": request.message})
        
        # Get response from the appropriate LLM
        response = await get_llm_response(request.user_id, request.message, memory)
        
        # Add assistant response to memory
        add_to_memory(request.user_id, {"role": "assistant", "content": response})
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@router.post("/upload")
async def upload(user_id: str = Form(...), file: UploadFile = File(...)) -> Dict[str, Any]:
    """Process an uploaded file and add its content to the user's context"""
    try:
        # Parse the uploaded file
        parsed_content = await parse_file(file)
        
        # Add file content to user's memory as system message
        system_message = f"Content from uploaded file '{file.filename}':\n{parsed_content}"
        add_to_memory(user_id, {"role": "system", "content": system_message})
        
        return {"response": f"File '{file.filename}' uploaded and processed successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/set_model")
async def set_model_route(request: ModelRequest) -> Dict[str, Any]:
    """Set the LLM model for a specific user"""
    try:
        # Validate model choice
        valid_models = ["gpt-4o", "gemini-1.5-flash", "deepseek-v3"]
        if request.model not in valid_models:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid model. Choose from: {', '.join(valid_models)}"
            )
        
        # Set the user's model preference
        set_user_model(request.user_id, request.model)
        
        return {"response": f"Model set to {request.model}"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting model: {str(e)}")
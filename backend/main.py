import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from backend.routes import router
from backend.config import get_storage_backend
from backend.session import set_storage_backend

# Load environment variables
load_dotenv()

# Initialize session manager with configured storage backend
set_storage_backend(get_storage_backend())

# Create FastAPI app
app = FastAPI(title="Discord LLM Bot Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Discord LLM Bot API is running"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
import os
from pydantic import BaseModel

# Load environment variables
load_dotenv(override=True)

# Get Ollama server URL from environment variables
OLLAMA_SERVER_URL = os.getenv("OLLAMA_SERVER_URL")

# Initialize the language model
llm = OllamaLLM(model="llama3.2:1b", base_url=OLLAMA_SERVER_URL)

# Create FastAPI instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to specific origins in production (e.g., ["https://your-frontend.com"])
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

# Define a Pydantic model for the request body
class QuestionRequest(BaseModel):
    question: str

# Define the endpoint to accept a JSON body
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        response = llm.invoke(request.question)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

# Add a health check endpoint for debugging
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
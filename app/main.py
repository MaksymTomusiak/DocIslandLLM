from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
import os

# Load environment variables
load_dotenv(override=True)

# Get Ollama server URL from environment variables
OLLAMA_SERVER_URL = os.getenv("OLLAMA_SERVER_URL")

# Initialize the language model
llm = OllamaLLM(model="llama3.2", base_url=OLLAMA_SERVER_URL)

# Create FastAPI instance
app = FastAPI()

# Define a simple endpoint
@app.get("/ask")
async def ask_question(question: str):
    try:
        response = llm.invoke(question)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=80)
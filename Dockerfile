# Use the official Ollama image as the base
FROM ollama/ollama:latest

# Install Python, pip, and bash
RUN apt-get update && apt-get install -y python3 python3-pip bash

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy your FastAPI code
COPY app/main.py .

# Expose port 80 (Azure Web App requirement)
EXPOSE 80

# Set environment variable for Ollama server
ENV OLLAMA_SERVER_URL=http://localhost:11434

# Override the default ENTRYPOINT to use bash
ENTRYPOINT ["/bin/bash", "-c"]

# Start Ollama server and run Uvicorn
CMD ["ollama serve & sleep 5 && (ollama list | grep -q llama3.2 || ollama run llama3.2) && uvicorn main:app --host 0.0.0.0 --port 80"]
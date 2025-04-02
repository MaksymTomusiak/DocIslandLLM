# Use the official Ollama Docker image as the base
FROM ollama/ollama:latest

# Install Python and dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt

# Copy your Python API code
COPY app/main.py .

# Pull Llama3.2 model into the container (optional, or you can do this at runtime)
RUN ollama pull llama3.2

# Expose the port your API will run on (e.g., 5000)
EXPOSE 5000

# Start Ollama and your Python API
CMD ["sh", "-c", "ollama serve & python3 main.py"]
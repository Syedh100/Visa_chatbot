#!/bin/bash

echo "Starting UK Visa Chatbot..."

# Stop any existing containers
echo "Cleaning up..."
docker stop $(docker ps -q) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Start Ollama in Docker
echo "Starting AI (Ollama)..."
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# Wait a moment for Ollama to start
sleep 5

# Pull the AI model
echo "Downloading AI model..."
docker exec -it ollama ollama pull llama3

# Build the chatbot
echo "Building chatbot..."
docker build -t visa-chatbot .

# Start the chatbot
echo "Starting chatbot..."
docker run -p 8501:8501 --link ollama visa-chatbot

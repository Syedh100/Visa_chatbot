#!/bin/bash

echo "Starting chatbot..."

# stop old stuff
docker stop $(docker ps -q) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# start ollama
echo "Starting AI..."
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# wait a bit
sleep 5

# get the model
echo "Getting AI model..."
docker exec -it ollama ollama pull llama3

# build chatbot
echo "Building chatbot..."
docker build -t visa-chatbot .

# run it
echo "Starting chatbot..."
docker run -p 8501:8501 --link ollama visa-chatbot

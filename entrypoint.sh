#!/usr/bin/env bash
set -e

OLLAMA_MODEL="${OLLAMA_MODEL:-smollm2}"

echo "Starting Ollama server in background..."
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama server to be ready..."
until curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 1
done
echo "Ollama server is ready."

if [[ "$OLLAMA_MODEL" == *"qwen"* ]]; then
    MODEL_NAME="qwen2.5"
    MODELFILE="Modelfile.qwen2.5"
else
    MODEL_NAME="smollm2"
    MODELFILE="Modelfile.smollm2"
fi

echo "Creating custom Twilite model '$MODEL_NAME' from $MODELFILE..."
ollama create "$MODEL_NAME" -f "$MODELFILE"
echo "Model created successfully."

echo "Starting Twilite Discord Bot..."
exec python3 main.py

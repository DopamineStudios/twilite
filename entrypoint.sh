#!/usr/bin/env bash
set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-smollm2}"

echo "Starting Ollama server in background..."
ollama serve > /app/ollama.log 2>&1 &
OLLAMA_PID=$!

echo "Checking Ollama server at $OLLAMA_HOST..."
counter=0
max_retries=60
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $max_retries ]; then
        echo "Error: Ollama server failed to start within $max_retries seconds."
        if [ -f /app/ollama.log ]; then
            echo "--- Ollama Logs ---"
            cat /app/ollama.log
        fi
        exit 1
    fi
done

echo "Ollama server is ready."

if [[ "$OLLAMA_MODEL" == *"qwen"* ]]; then
    MODEL_NAME="qwen2.5"
    MODELFILE="Modelfile.qwen2.5"
else
    MODEL_NAME="smollm2"
    MODELFILE="Modelfile.smollm2"
fi

echo "Creating model '$MODEL_NAME' using $MODELFILE..."
ollama create "$MODEL_NAME" -f "$MODELFILE"
echo "Model '$MODEL_NAME' successfully registered!"

echo "Starting Twilite Discord Bot..."
exec python3 main.py

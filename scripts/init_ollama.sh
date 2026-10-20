#!/usr/bin/env bash
set -e

# Ollama initialization script for local setup
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
OLLAMA_MODEL="${OLLAMA_MODEL:-smollm2}"

echo "Checking Ollama server at $OLLAMA_HOST..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do
    echo "Waiting for Ollama server..."
    sleep 2
done

if [[ "$OLLAMA_MODEL" == *"qwen"* ]]; then
    MODEL_NAME="qwen2.5"
    MODELFILE="Modelfile.qwen2.5"
else
    MODEL_NAME="smollm2"
    MODELFILE="Modelfile.smollm2"
fi

echo "Ollama server is up. Creating model '$MODEL_NAME' using $MODELFILE..."
ollama create "$MODEL_NAME" -f "$MODELFILE"

echo "Model '$MODEL_NAME' successfully registered!"

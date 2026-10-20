#!/usr/bin/env bash
set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"

echo "Waiting for Ollama server at $OLLAMA_HOST..."
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do
    sleep 1
done
echo "Ollama server is ready."

echo "Starting Twilite Discord Bot..."
exec python3 main.py

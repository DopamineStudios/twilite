#!/usr/bin/env bash
set -e

OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"

echo "Checking Ollama server at $OLLAMA_HOST..."
counter=0
max_retries=30
until curl -s "$OLLAMA_HOST/api/tags" > /dev/null; do
    sleep 1
    counter=$((counter + 1))
    if [ $counter -ge $max_retries ]; then
        echo "Warning: Ollama server not reachable at $OLLAMA_HOST after $max_retries seconds. Starting bot anyway..."
        break
    fi
done
if [ $counter -lt $max_retries ]; then
    echo "Ollama server is ready."
fi

echo "Starting Twilite Discord Bot..."
exec python3 main.py

#!/bin/bash

# Ollama Initialization Script
# This script pulls common models for local development

echo "🚀 Starting Ollama model initialization..."

# Wait for Ollama service to be ready
echo "⏳ Waiting for Ollama service to start..."
while ! curl -f http://localhost:11434/api/tags >/dev/null 2>&1; do
    sleep 2
done

echo "✅ Ollama service is ready!"

# Get models from environment variable or use defaults
MODELS_STRING="${OLLAMA_AUTO_PULL_MODELS:-llama2:7b,codellama:7b,mistral:7b,phi:2.7b}"
IFS=',' read -ra MODELS <<< "$MODELS_STRING"

# Function to pull a model
pull_model() {
    local model=$1
    echo "📥 Pulling model: $model"
    if ollama pull "$model"; then
        echo "✅ Successfully pulled: $model"
    else
        echo "❌ Failed to pull: $model"
    fi
}

# Pull models if they don't exist
for model in "${MODELS[@]}"; do
    if ! ollama list | grep -q "$model"; then
        pull_model "$model"
    else
        echo "✅ Model already exists: $model"
    fi
done

echo "🎉 Ollama initialization complete!"
echo "📋 Available models:"
ollama list

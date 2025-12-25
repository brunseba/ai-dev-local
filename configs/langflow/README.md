# Langflow Configuration

This directory contains configuration files and examples for Langflow.

## Directory Structure

```
configs/langflow/
├── README.md           # This file
└── examples/          # Example workflow files
    ├── basic-chatbot.json
    ├── rag-workflow.json
    └── multi-agent.json
```

## Configuration

Langflow is configured primarily through environment variables in `.env`:

- `LANGFLOW_PORT`: Web interface port (default: 7860)
- `LANGFLOW_SUPERUSER`: Admin username (default: admin)
- `LANGFLOW_SUPERUSER_PASSWORD`: Admin password (default: admin123)
- `LANGFLOW_WORKERS`: Number of worker processes (default: 1)

## LiteLLM Integration

Langflow automatically integrates with LiteLLM through environment variables:

- `OPENAI_API_KEY`: Set to `${LITELLM_MASTER_KEY}`
- `OPENAI_API_BASE`: Set to `http://litellm:4000/v1`

This allows Langflow to access all models configured in LiteLLM.

## Langfuse Integration

When Langfuse keys are configured, Langflow automatically sends traces:

- `LANGFUSE_SECRET_KEY`: Your Langfuse secret key
- `LANGFUSE_PUBLIC_KEY`: Your Langfuse public key  
- `LANGFUSE_HOST`: Langfuse endpoint (http://langfuse:3000)

## Using Example Workflows

1. Access Langflow at http://localhost:7860
2. Click "Import" in the UI
3. Select an example JSON file from `examples/`
4. Configure any required API keys
5. Test the workflow in the Playground

## Creating Custom Workflows

1. Design your workflow in the Langflow UI
2. Click "Export" to save as JSON
3. Save to this directory for sharing
4. Share with team or commit to version control

## Database

Langflow uses the shared PostgreSQL instance:
- Database: `langflow`
- Connection: `postgresql://postgres:postgres@postgres:5432/langflow`

All flows and configurations are stored in the database and persist across restarts.

## Storage

Langflow data is stored in a Docker volume: `langflow_data`

This includes:
- Flow definitions
- Component configurations
- User settings
- Uploaded files

## For More Information

- Official Documentation: https://docs.langflow.org/
- Integration Guide: `../../docs/langflow-setup.md`
- LiteLLM Setup: `../../docs/langflow-litellm-integration.md`

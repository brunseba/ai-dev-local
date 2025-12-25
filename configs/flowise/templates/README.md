# Flowise Chatflow Templates

This directory contains pre-configured chatflow templates for AI Dev Local.

## Available Templates

### litellm-quickstart.json
A simple chatflow demonstrating how to use LiteLLM proxy with Flowise.

**Features:**
- Pre-configured to use LiteLLM proxy
- Shows proper credential configuration
- Includes example with GPT-3.5 Turbo
- Ready to import and test

## How to Import

1. Access Flowise UI: http://localhost:3001
2. Login with: `admin` / `admin123`
3. Click **"Chatflows"** in the left sidebar
4. Click **"Import Chatflow"** button
5. Select the template JSON file
6. Configure credentials if prompted
7. Test the chatflow

## Before Importing

Make sure you have:
1. Created the "LiteLLM Proxy" credential in Flowise
   - API Key: Your LITELLM_MASTER_KEY
   - No BasePath needed in credential (set in nodes)
2. LiteLLM service is running and accessible
3. At least one model configured in `configs/litellm_config.yaml`

## Customizing Templates

You can export your own chatflows as templates:
1. Create a chatflow in Flowise
2. Click the "..." menu on the chatflow card
3. Select "Export"
4. Save the JSON file to this directory
5. Share with your team or commit to version control

## Notes

- Template files use `${CREDENTIAL_NAME}` placeholders
- You'll need to select your actual credentials after import
- BasePath is set to `http://litellm:4000` in the templates
- Model names match those in `configs/litellm_config.yaml`

-- Initialize databases for AI Dev Local services

-- Create database for Langfuse
CREATE DATABASE langfuse;

-- Create database for FlowiseAI
CREATE DATABASE flowise;

-- Create database for LiteLLM
CREATE DATABASE litellm;

-- Create database for Vector Store
CREATE DATABASE vectordb;

-- Grant privileges to postgres user
GRANT ALL PRIVILEGES ON DATABASE langfuse TO postgres;
GRANT ALL PRIVILEGES ON DATABASE flowise TO postgres;
GRANT ALL PRIVILEGES ON DATABASE litellm TO postgres;
GRANT ALL PRIVILEGES ON DATABASE vectordb TO postgres;

-- Connect to vectordb and enable pgvector extension
\c vectordb;
CREATE EXTENSION IF NOT EXISTS vector;

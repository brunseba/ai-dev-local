# Flowise Vector Store Configuration

This guide explains how to configure vector stores in Flowise for your AI workflows.

## Overview

Flowise supports multiple vector store options:
- **FAISS** - Facebook AI Similarity Search (local, file-based)
- **Pinecone** - Cloud vector database
- **Qdrant** - Open-source vector search engine
- **PostgreSQL (pgvector)** - Use your existing PostgreSQL database
- **Chroma** - Open-source embedding database
- **Milvus** - Cloud-native vector database

## Storage Configuration

**Base Storage Path**: `/root/.flowise/storage`
- **Uploads**: `/root/.flowise/storage/uploads`
- **FAISS Indexes**: `/root/.flowise/storage/faiss`
- **Other Data**: `/root/.flowise/storage`

All data is persisted in the Docker volume `flowise_data`.

## FAISS Configuration

### Error: "could not open faiss.index for reading"

This error occurs when:
1. You're trying to **Load Existing Index** but the index file doesn't exist
2. The Base Path is incorrect or not specified

### Solution: Configure FAISS in Your Chatflow

When adding a FAISS node in Flowise:

1. **First Time Setup** (Create New Index):
   ```
   Base Path: /root/.flowise/storage/faiss/my-index
   Mode: Create New Index (or leave empty)
   ```

2. **Loading Existing Index**:
   ```
   Base Path: /root/.flowise/storage/faiss/my-index
   Mode: Load Existing Index
   ```
   ⚠️ Only use this AFTER you've created the index first

### FAISS Node Configuration

| Parameter | Description | Example |
|-----------|-------------|---------|
| **Base Path** | Directory where FAISS index will be stored | `/root/.flowise/storage/faiss/my-docs` |
| **Embeddings** | Embedding model to use | OpenAI Embeddings (text-embedding-3-small) |
| **Document Loader** | Source of documents | File Upload, URL, etc. |

### Example Workflow

1. **Create a FAISS Vector Store**:
   - Add a FAISS node
   - Set Base Path: `/root/.flowise/storage/faiss/documentation`
   - Connect an Embeddings node (e.g., OpenAI Embeddings)
   - Connect a Document Loader node
   - Run the workflow to create the index

2. **Use the Vector Store**:
   - In subsequent workflows, use the same Base Path
   - The index will be loaded automatically

## PostgreSQL (pgvector) Configuration

Instead of FAISS, you can use PostgreSQL with pgvector extension:

### Configuration

```
Connection String: postgresql://postgres:postgres@postgres:5432/vectordb
Table Name: embeddings
Embedding Model: OpenAI (text-embedding-3-small)
```

### Advantages over FAISS

- ✅ Persistent across container restarts
- ✅ Shared database with other services
- ✅ Better for production use
- ✅ Supports metadata filtering
- ✅ Concurrent access

### Setup in Flowise

1. Add a **Postgres** vector store node
2. Configure connection:
   ```
   Host: postgres
   Port: 5432
   Database: vectordb
   User: postgres
   Password: postgres
   Table Name: embeddings
   ```
3. Connect embeddings and document loaders
4. Run the workflow

## Using LiteLLM PGVector Service

You can also use the standalone pgvector API (port 8000) with Flowise:

### HTTP Vector Store Configuration

```
Endpoint: http://litellm-pgvector:8000/v1/vector_stores
API Key: [Your OPENAI_API_KEY from .env]
Vector Store ID: default
```

This allows you to:
- Use the same vector store across multiple tools
- Manage embeddings through a REST API
- Access from outside Flowise

## Best Practices

### 1. Choose the Right Vector Store

| Use Case | Recommended Store | Reason |
|----------|-------------------|--------|
| Quick prototyping | FAISS | Fast, local, no setup |
| Production workflows | PostgreSQL | Persistent, scalable |
| High-scale search | Pinecone/Milvus | Optimized for large datasets |
| Development | FAISS or pgvector | Easy to reset/rebuild |

### 2. Storage Paths

Always use absolute paths inside the container:

✅ **Good**:
- `/root/.flowise/storage/faiss/my-index`
- `/root/.flowise/storage/docs`

❌ **Bad**:
- `./faiss/my-index` (relative paths)
- `/tmp/faiss` (not persisted)
- `faiss.index` (no directory specified)

### 3. Index Naming

Use descriptive names for your indexes:

```
/root/.flowise/storage/faiss/product-docs
/root/.flowise/storage/faiss/customer-support
/root/.flowise/storage/faiss/technical-manuals
```

### 4. Embeddings Consistency

Always use the same embedding model for a vector store:
- If you create with `text-embedding-3-small`, always load with `text-embedding-3-small`
- Different models have different dimensions and cannot be mixed

## Troubleshooting

### Error: "could not open faiss.index for reading"

**Cause**: Index file doesn't exist

**Solutions**:
1. Create the directory:
   ```bash
   docker exec ai-dev-local-flowise-1 mkdir -p /root/.flowise/storage/faiss/my-index
   ```

2. In Flowise, use "Create New Index" mode first
3. Verify Base Path is correct
4. Check that documents are being loaded

### Error: "FAISS index already exists"

**Cause**: Trying to create an index that already exists

**Solutions**:
1. Use "Load Existing Index" mode
2. Or delete the existing index:
   ```bash
   docker exec ai-dev-local-flowise-1 rm -rf /root/.flowise/storage/faiss/my-index
   ```

### Error: Connection timeout to PostgreSQL

**Cause**: Cannot reach postgres service

**Solutions**:
1. Verify postgres container is running:
   ```bash
   docker compose ps postgres
   ```

2. Check connection string uses correct hostname:
   - ✅ `postgres` (inside Docker network)
   - ❌ `localhost` (wrong for container-to-container)

3. Test connection:
   ```bash
   docker exec ai-dev-local-flowise-1 nc -zv postgres 5432
   ```

### Error: Dimension mismatch

**Cause**: Using different embedding models

**Solution**: 
- Always use the same embedding model for a vector store
- If you need to change models, recreate the index

## Accessing Vector Stores

### From Flowise UI

1. Navigate to: `http://localhost:3001`
2. Create or open a chatflow
3. Add a Vector Store node
4. Configure as described above

### From Outside Flowise

Use the pgvector API directly:

```bash
# Create embeddings
curl -X POST http://localhost:8000/v1/vector_stores/default/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "Your text here",
    "model": "text-embedding-3-small"
  }'

# Search
curl -X POST http://localhost:8000/v1/vector_stores/default/search \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "search query",
    "limit": 5
  }'
```

## Storage Management

### View Storage Usage

```bash
# Check total storage
docker exec ai-dev-local-flowise-1 du -sh /root/.flowise/storage/*

# List FAISS indexes
docker exec ai-dev-local-flowise-1 ls -lh /root/.flowise/storage/faiss/

# Check disk space
docker exec ai-dev-local-flowise-1 df -h /root/.flowise/storage
```

### Backup Vector Stores

```bash
# Backup FAISS indexes
docker cp ai-dev-local-flowise-1:/root/.flowise/storage/faiss ./backups/faiss-$(date +%Y%m%d)

# Backup PostgreSQL
docker exec ai-dev-local-postgres-1 pg_dump -U postgres vectordb > vectordb-backup-$(date +%Y%m%d).sql
```

### Restore Vector Stores

```bash
# Restore FAISS indexes
docker cp ./backups/faiss-20251225 ai-dev-local-flowise-1:/root/.flowise/storage/faiss

# Restore PostgreSQL
cat vectordb-backup-20251225.sql | docker exec -i ai-dev-local-postgres-1 psql -U postgres vectordb
```

## Migrating Between Vector Stores

### FAISS to PostgreSQL

1. Export embeddings from FAISS (requires custom script)
2. Import to PostgreSQL using pgvector API
3. Update Flowise chatflows to use PostgreSQL node

### Local to Cloud (Pinecone/Milvus)

1. Export your data
2. Configure cloud provider credentials in Flowise
3. Create new chatflow with cloud vector store
4. Re-index your documents

## Environment Variables

Key environment variables for Flowise vector stores:

```bash
# Storage paths
BLOB_STORAGE_PATH=/root/.flowise/storage
SECRETKEY_PATH=/root/.flowise
LOG_PATH=/root/.flowise/logs

# Database (if using PostgreSQL)
DATABASE_TYPE=postgres
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=flowise
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

## Resources

- **Flowise Documentation**: https://docs.flowiseai.com/
- **FAISS Documentation**: https://github.com/facebookresearch/faiss
- **pgvector Documentation**: https://github.com/pgvector/pgvector
- **LangChain Vector Stores**: https://python.langchain.com/docs/modules/data_connection/vectorstores/

## Quick Reference

### Create New FAISS Index

```
Node: FAISS
Base Path: /root/.flowise/storage/faiss/[your-index-name]
Embeddings: OpenAI (text-embedding-3-small)
Document: [Your document source]
```

### Use PostgreSQL Instead

```
Node: Postgres
Host: postgres
Port: 5432
Database: vectordb
User: postgres
Password: postgres
Table: embeddings
Embeddings: OpenAI (text-embedding-3-small)
```

### Connect to External PGVector API

```
Node: Custom HTTP Vector Store
Endpoint: http://litellm-pgvector:8000/v1
API Key: [OPENAI_API_KEY from .env]
```

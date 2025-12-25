# Vector Store Management in LiteLLM

This guide explains how to use and manage vector stores with LiteLLM for Retrieval-Augmented Generation (RAG) use cases.

## Overview

Your AI Dev Local environment includes:
- **litellm-pgvector**: OpenAI-compatible vector store API using PostgreSQL with pgvector extension
- **LiteLLM Proxy**: Unified API with vector store registry support
- **Embedding Models**: Multiple embedding models configured (OpenAI, Cohere)

## Architecture

```
┌─────────────────┐
│   Your App      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│  LiteLLM Proxy  │─────▶│ Embedding Models │
│   Port 4000     │      │  (via LiteLLM)   │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ PGVector Store  │◀────▶│   PostgreSQL     │
│   Port 8000     │      │   + pgvector     │
└─────────────────┘      └──────────────────┘
```

## Configuration

### Current Setup

**Vector Store Service** (litellm-pgvector):
- URL: `http://localhost:8000`
- API Key: Set in `.env` as `VECTOR_STORE_API_KEY`
- Database: PostgreSQL with pgvector extension
- Embedding Model: `text-embedding-3-small` (via LiteLLM)

**LiteLLM Configuration**:
- LiteLLM provides embedding models used by the vector store
- Vector store is accessed directly via its API (port 8000), not through LiteLLM's vector store registry
- For cloud vector stores (OpenAI, Azure, Bedrock), you would use LiteLLM's vector_store_registry

### Environment Variables

```bash
# Vector Store Configuration
VECTOR_STORE_PORT=8000
VECTOR_STORE_API_KEY=sk-3zQNqmUvQBzpVeZbJRiZQA  # Generated LiteLLM key

# Embedding Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# LiteLLM Configuration
LITELLM_MASTER_KEY=D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB
```

## Usage Examples

### 1. Create a Vector Store

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000",
    api_key="sk-3zQNqmUvQBzpVeZbJRiZQA"
)

# Create a new vector store
vector_store = client.beta.vector_stores.create(
    name="my-knowledge-base",
    metadata={
        "project": "ai-dev-local",
        "environment": "development"
    }
)

print(f"Created vector store: {vector_store.id}")
```

### 2. Add Documents to Vector Store

```python
# Upload a file first
with open("document.pdf", "rb") as file:
    uploaded_file = client.files.create(
        file=file,
        purpose="assistants"
    )

# Add file to vector store
vector_store_file = client.beta.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=uploaded_file.id,
    chunking_strategy={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 800,
            "chunk_overlap_tokens": 400
        }
    }
)
```

### 3. Create Embeddings

```python
# Create embeddings for text
response = client.beta.vector_stores.create_embedding(
    vector_store_id=vector_store.id,
    input="Your text to embed",
    model="text-embedding-3-small"
)

print(f"Generated embedding with {len(response.data[0].embedding)} dimensions")
```

### 4. Search Vector Store

```python
# Search for relevant content
results = client.beta.vector_stores.search(
    vector_store_id=vector_store.id,
    query="What is the return policy?",
    limit=5
)

for result in results.data:
    print(f"Score: {result.score}")
    print(f"Content: {result.content}")
    print(f"Metadata: {result.metadata}")
    print("---")
```

### 5. Use with LLM Completion (RAG)

```python
# Using LiteLLM proxy with vector store
from openai import OpenAI

litellm_client = OpenAI(
    base_url="http://localhost:4000",
    api_key="D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB"
)

response = litellm_client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "What is our return policy?"}
    ],
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": ["vs_abc123"]
        }
    ]
)

print(response.choices[0].message.content)
```

## API Endpoints

### Vector Store Endpoints (Port 8000)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/vector_stores` | POST | Create a new vector store |
| `/v1/vector_stores` | GET | List all vector stores |
| `/v1/vector_stores/{id}` | GET | Get vector store details |
| `/v1/vector_stores/{id}` | DELETE | Delete a vector store |
| `/v1/vector_stores/{id}/search` | POST | Search within a vector store |
| `/v1/vector_stores/{id}/embeddings` | POST | Create embeddings |
| `/v1/vector_stores/{id}/embeddings/batch` | POST | Create batch embeddings |
| `/health` | GET | Health check |

### Using cURL

```bash
# Create vector store
curl -X POST http://localhost:8000/v1/vector_stores \
  -H "Authorization: Bearer sk-3zQNqmUvQBzpVeZbJRiZQA" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-store",
    "metadata": {"project": "demo"}
  }'

# Search vector store
curl -X POST http://localhost:8000/v1/vector_stores/vs_abc123/search \
  -H "Authorization: Bearer sk-3zQNqmUvQBzpVeZbJRiZQA" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the return policy?",
    "limit": 5
  }'
```

## LiteLLM UI Access

Access the LiteLLM dashboard to manage vector stores visually:

1. Open: `http://localhost:4000`
2. Login with credentials:
   - Username: `admin`
   - Password: `admin123`
3. Navigate to: **Experimental > Vector Stores**

### Features Available in UI:
- ✅ Create vector stores
- ✅ List all vector stores
- ✅ View vector store details
- ✅ Delete vector stores
- ✅ Configure credentials

## Best Practices

### 1. Chunking Strategy

For optimal retrieval, configure chunking parameters:

```python
chunking_strategy = {
    "type": "static",
    "static": {
        "max_chunk_size_tokens": 800,  # Adjust based on content
        "chunk_overlap_tokens": 400     # 50% overlap recommended
    }
}
```

**Guidelines:**
- **Technical docs**: 400-800 tokens per chunk
- **Long-form content**: 800-1200 tokens per chunk
- **FAQ/Short answers**: 200-400 tokens per chunk

### 2. Embedding Model Selection

| Model | Dimensions | Best For | Cost |
|-------|------------|----------|------|
| `text-embedding-3-small` | 1536 | General purpose, cost-effective | $ |
| `text-embedding-3-large` | 3072 | High accuracy, semantic search | $$$ |
| `text-embedding-ada-002` | 1536 | Legacy, good compatibility | $$ |

### 3. Search Optimization

```python
# Use filters for better results
results = client.beta.vector_stores.search(
    vector_store_id=vector_store.id,
    query="pricing information",
    limit=10,
    filters={
        "category": "support",
        "language": "en"
    },
    ranking_options={
        "score_threshold": 0.7  # Only return high-quality matches
    }
)
```

### 4. Metadata Management

Always include useful metadata:

```python
vector_store = client.beta.vector_stores.create(
    name="support-docs",
    metadata={
        "project": "customer-support",
        "version": "1.0",
        "last_updated": "2025-12-24",
        "category": "documentation",
        "language": "en"
    }
)
```

## Monitoring and Maintenance

### Check Vector Store Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": 1766615287}
```

### View Container Logs

```bash
# Vector store logs
docker logs ai-dev-local-litellm-pgvector-1

# LiteLLM logs
docker logs ai-dev-local-litellm-1

# PostgreSQL logs
docker logs ai-dev-local-postgres-1
```

### Database Management

```bash
# Connect to PostgreSQL
docker exec -it ai-dev-local-postgres-1 psql -U postgres

# Check vector store tables
\c vectordb
\dt

# View embeddings count
SELECT vector_store_id, COUNT(*) 
FROM embeddings 
GROUP BY vector_store_id;
```

## Troubleshooting

### Issue: Authentication Error

**Symptom:** `Invalid proxy server token passed`

**Solution:**
1. Verify `VECTOR_STORE_API_KEY` is set correctly in `.env`
2. Regenerate key via LiteLLM:
   ```bash
   curl -X POST http://localhost:4000/key/generate \
     -H "Authorization: Bearer D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB" \
     -H "Content-Type: application/json" \
     -d '{"key_alias": "vector-store", "models": ["text-embedding-3-small"]}'
   ```
3. Update `.env` with new key
4. Restart: `docker compose restart litellm-pgvector`

### Issue: Slow Search Performance

**Solutions:**
- Reduce `max_num_results` in search queries
- Add appropriate filters to narrow search scope
- Consider using `text-embedding-3-small` for faster processing
- Check PostgreSQL performance: `docker stats ai-dev-local-postgres-1`

### Issue: Connection Timeout

**Solutions:**
- Verify services are running: `docker compose ps`
- Check network connectivity between containers
- Increase timeout in client configuration
- Review logs for error messages

## Migration from Existing Data

If you have existing embeddings in another system:

```python
# Example migration script
import pandas as pd
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000",
    api_key="sk-3zQNqmUvQBzpVeZbJRiZQA"
)

# Create new vector store
vs = client.beta.vector_stores.create(name="migrated-data")

# Load existing embeddings
df = pd.read_csv("existing_embeddings.csv")

# Batch insert
for idx, row in df.iterrows():
    client.beta.vector_stores.embeddings.create(
        vector_store_id=vs.id,
        input=row['text'],
        embedding=row['embedding'].tolist(),
        metadata=row['metadata']
    )
    
    if idx % 100 == 0:
        print(f"Migrated {idx} documents")
```

## Advanced Configuration

### Custom Database Schema

You can customize database field names in docker-compose.yml:

```yaml
environment:
  DB_FIELDS__ID_FIELD: "custom_id"
  DB_FIELDS__CONTENT_FIELD: "document_text"
  DB_FIELDS__METADATA_FIELD: "doc_metadata"
  DB_FIELDS__EMBEDDING_FIELD: "vector"
  DB_FIELDS__VECTOR_STORE_ID_FIELD: "store_id"
  DB_FIELDS__CREATED_AT_FIELD: "timestamp"
```

### Multiple Vector Stores

Add more vector stores to `litellm_config.yaml`:

```yaml
vector_store_registry:
- vector_store_name: "pgvector-local"
  litellm_params:
    vector_store_id: "default"
    custom_llm_provider: "pgvector"
    # ... configuration

- vector_store_name: "openai-vectors"
  litellm_params:
    vector_store_id: "vs_openai_123"
    custom_llm_provider: "openai"
    api_key: os.environ/OPENAI_API_KEY
```

## Security Considerations

1. **API Key Rotation**: Regularly regenerate API keys
2. **Access Control**: Use per-project API keys with restricted permissions
3. **Data Encryption**: PostgreSQL connections use TLS in production
4. **Audit Logging**: Enable logging in LiteLLM for compliance
5. **Secrets Management**: Never commit `.env` files to version control

## Resources

- **API Documentation**: http://localhost:8000/docs
- **LiteLLM Dashboard**: http://localhost:4000
- **PGVector GitHub**: https://github.com/pgvector/pgvector
- **LiteLLM Docs**: https://docs.litellm.ai/docs/vector_stores/create
- **OpenAI Vector Stores**: https://platform.openai.com/docs/api-reference/vector-stores

## Support

For issues or questions:
1. Check logs: `docker compose logs litellm-pgvector`
2. Review this documentation
3. Consult LiteLLM documentation
4. Check GitHub issues for known problems

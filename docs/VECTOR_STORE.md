# Vector Store with LiteLLM PGVector

The AI Dev Local stack includes an OpenAI-compatible vector store API using PGVector for efficient vector storage and similarity search. This enables Retrieval-Augmented Generation (RAG) workflows with any embedding model supported by LiteLLM.

## Overview

**LiteLLM PGVector** provides:
- 🗄️ Efficient vector storage using PostgreSQL with pgvector extension
- 🔄 Seamless integration with LiteLLM proxy for any embedding model
- 🎛️ OpenAI-compatible API endpoints
- ⚡ FastAPI with async support
- 🐳 Docker-ready deployment

## Features

### Supported Operations

- **Vector Store Management**: Create, list, and delete vector stores
- **Document Storage**: Store documents with metadata and automatic embedding generation
- **Similarity Search**: Find relevant documents using vector similarity
- **Batch Operations**: Efficient batch document uploads
- **Custom Field Mapping**: Configurable database field names

### Supported Embedding Models

Any embedding model supported by LiteLLM can be used:

#### OpenAI
- `text-embedding-ada-002`
- `text-embedding-3-small`
- `text-embedding-3-large`

#### Cohere
- `embed-english-v3.0`
- `embed-multilingual-v3.0`

#### And many more through LiteLLM proxy...

## Configuration

### Environment Variables

Configure the vector store in your `.env` file:

```bash
# Vector Store Port
VECTOR_STORE_PORT=8000

# Embedding Model Configuration
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Database URL (auto-configured in docker-compose)
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/vectordb?schema=public

# LiteLLM Integration (auto-configured)
EMBEDDING__BASE_URL=http://litellm:4000
EMBEDDING__API_KEY=${LITELLM_MASTER_KEY}
```

### Database Field Customization

You can customize database field names (optional):

```bash
DB_FIELDS__ID_FIELD=id
DB_FIELDS__CONTENT_FIELD=content
DB_FIELDS__METADATA_FIELD=metadata
DB_FIELDS__EMBEDDING_FIELD=embedding
DB_FIELDS__VECTOR_STORE_ID_FIELD=vector_store_id
DB_FIELDS__CREATED_AT_FIELD=created_at
```

## Usage

### Starting the Service

The vector store starts automatically with other services:

```bash
ai-dev-local start
```

Access the API:
- **API Base URL**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

### API Examples

#### 1. Create a Vector Store

```bash
curl -X POST http://localhost:8000/v1/vector_stores \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d '{
    "name": "my-knowledge-base",
    "metadata": {
      "description": "Product documentation",
      "version": "1.0"
    }
  }'
```

#### 2. Add Documents

```bash
curl -X POST http://localhost:8000/v1/vector_stores/{vector_store_id}/files \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d '{
    "content": "AI Dev Local is a comprehensive development environment...",
    "metadata": {
      "source": "documentation",
      "page": "overview"
    }
  }'
```

#### 3. Search Documents

```bash
curl -X POST http://localhost:8000/v1/vector_stores/{vector_store_id}/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${OPENAI_API_KEY}" \
  -d '{
    "query": "How do I configure LiteLLM?",
    "limit": 5
  }'
```

#### 4. List Vector Stores

```bash
curl http://localhost:8000/v1/vector_stores \
  -H "Authorization: Bearer ${OPENAI_API_KEY}"
```

## Integration with AI Applications

### Python Example

```python
import openai

# Configure client to use local vector store
client = openai.OpenAI(
    api_key="your-openai-key",
    base_url="http://localhost:8000/v1"
)

# Create a vector store
vector_store = client.vector_stores.create(
    name="product-docs",
    metadata={"version": "1.0"}
)

# Add documents
client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    content="Documentation content here...",
    metadata={"source": "manual"}
)

# Search for relevant documents
results = client.vector_stores.search(
    vector_store_id=vector_store.id,
    query="How to install?",
    limit=3
)
```

### RAG Pattern

```python
def answer_with_context(question: str, vector_store_id: str) -> str:
    # 1. Find relevant documents
    search_results = client.vector_stores.search(
        vector_store_id=vector_store_id,
        query=question,
        limit=5
    )
    
    # 2. Build context from results
    context = "\n\n".join([
        doc["content"] for doc in search_results["data"]
    ])
    
    # 3. Generate answer using LiteLLM
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    
    return response.choices[0].message.content
```

## Use Cases

### 1. Knowledge Base Search
Store company documentation, wikis, and internal knowledge for semantic search.

### 2. Code Search
Index codebases with embeddings for intelligent code search and discovery.

### 3. Customer Support
Create a RAG-powered chatbot with product documentation and support articles.

### 4. Research Assistant
Build a research tool that retrieves relevant papers and documentation.

### 5. Content Recommendation
Implement similarity-based content recommendation systems.

## Database Schema

The vector store uses PostgreSQL with pgvector extension:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Example table structure
CREATE TABLE documents (
    id UUID PRIMARY KEY,
    vector_store_id UUID NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(1536),  -- Vector dimension depends on model
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for fast similarity search
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops);
```

## Performance Tips

### 1. Choose the Right Embedding Model

- **text-embedding-3-small**: Fast, cost-effective, good for most use cases (1536 dimensions)
- **text-embedding-3-large**: Higher quality, more expensive (3072 dimensions)
- **cohere/embed-english-v3.0**: Optimized for English, excellent quality (1024 dimensions)

### 2. Optimize Search

- Use appropriate `limit` values (3-10 for most RAG applications)
- Create proper indexes on frequently searched stores
- Consider batch operations for large document sets

### 3. Metadata Filtering

Use metadata to pre-filter documents before vector search:

```python
results = client.vector_stores.search(
    vector_store_id=vector_store_id,
    query="installation guide",
    filter={"source": "official-docs", "language": "en"},
    limit=5
)
```

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Logs

View service logs:

```bash
docker logs -f $(docker ps -q -f name=litellm-pgvector)
```

### Database Inspection

Connect to the vector database:

```bash
docker exec -it $(docker ps -q -f name=postgres) \
  psql -U postgres -d vectordb
```

Check vector stores:

```sql
SELECT * FROM vector_stores;
SELECT COUNT(*) FROM documents WHERE vector_store_id = 'your-store-id';
```

## Troubleshooting

### Service Not Starting

Check dependencies:
```bash
docker ps | grep -E "(postgres|litellm)"
```

Ensure both PostgreSQL and LiteLLM are healthy.

### Embedding Generation Fails

Verify LiteLLM configuration:
```bash
curl http://localhost:4000/health
```

Check API keys in `.env` file.

### Slow Search Performance

Create or rebuild vector indexes:
```sql
CREATE INDEX IF NOT EXISTS documents_embedding_idx 
ON documents USING ivfflat (embedding vector_cosine_ops);
```

## Advanced Configuration

### Custom Embedding Dimensions

Different models use different dimensions:

```bash
# text-embedding-3-small
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# text-embedding-3-large
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_DIMENSIONS=3072

# cohere/embed-english-v3.0
EMBEDDING_MODEL=embed-english-v3
EMBEDDING_DIMENSIONS=1024
```

### Multiple Vector Stores

You can run multiple instances with different configurations:

```yaml
# In docker-compose.override.yml
services:
  vector-store-openai:
    extends: litellm-pgvector
    environment:
      EMBEDDING__MODEL: text-embedding-3-small
      PORT: 8001
    ports:
      - "8001:8001"
  
  vector-store-cohere:
    extends: litellm-pgvector
    environment:
      EMBEDDING__MODEL: embed-english-v3
      PORT: 8002
    ports:
      - "8002:8002"
```

## Security Considerations

1. **API Key Management**: Store API keys in `.env`, never commit them
2. **Access Control**: Use OPENAI_API_KEY authentication for all requests
3. **Data Privacy**: Vector stores contain your data - ensure proper backup and access controls
4. **Network Security**: In production, use HTTPS and proper firewall rules

## Next Steps

- Explore the [API Documentation](http://localhost:8000/docs) for all available endpoints
- Check [LiteLLM Documentation](https://docs.litellm.ai/) for more embedding models
- Review [PGVector Documentation](https://github.com/pgvector/pgvector) for advanced indexing

## Resources

- [LiteLLM PGVector GitHub](https://github.com/BerriAI/litellm-pgvector)
- [PGVector Extension](https://github.com/pgvector/pgvector)
- [OpenAI Vector Stores API](https://platform.openai.com/docs/api-reference/vector-stores)
- [RAG Best Practices](https://docs.litellm.ai/docs/rag)

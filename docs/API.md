# Documentation de l'API

## Base URL

- Local: `http://localhost:8000`
- Production: `https://rag-api.example.com`

## Endpoints

### Health Check

```http
GET /health
```

**Réponse:**
```json
{
  "status": "healthy",
  "service": "rag-system"
}
```

### Query RAG

```http
POST /api/query
Content-Type: application/json
```

**Body:**
```json
{
  "question": "Qu'est-ce que Python?",
  "chat_history": [
    {
      "role": "user",
      "content": "Bonjour"
    },
    {
      "role": "assistant",
      "content": "Bonjour! Comment puis-je vous aider?"
    }
  ]
}
```

**Réponse:**
```json
{
  "question": "Qu'est-ce que Python?",
  "answer": "Python est un langage de programmation...",
  "sources": [
    {
      "content": "Python est un langage...",
      "metadata": {
        "source": "document.pdf",
        "page": 1
      }
    }
  ],
  "model": "gpt-4-turbo-preview"
}
```

### Query RAG (Streaming)

```http
POST /api/query/stream
Content-Type: application/json
```

**Body:** Identique à `/api/query`

**Réponse:** Server-Sent Events (SSE)

### Ingest Documents

```http
POST /api/ingest
Content-Type: application/json
```

**Body:**
```json
{
  "path": "/path/to/documents",
  "is_directory": true
}
```

**Réponse:**
```json
{
  "message": "Documents ingested successfully",
  "chunks_count": 150
}
```

### Upload Document

```http
POST /api/ingest/upload
Content-Type: multipart/form-data
```

**Body:** Form data avec fichier

**Réponse:**
```json
{
  "message": "File document.pdf ingested successfully",
  "chunks_count": 25
}
```

### Search Vector Store

```http
GET /api/search?query=Python&k=5
```

**Réponse:**
```json
{
  "query": "Python",
  "results": [
    {
      "content": "Python est un langage...",
      "metadata": {
        "source": "document.pdf",
        "page": 1
      }
    }
  ]
}
```

### Prometheus Metrics

```http
GET /metrics
```

**Réponse:** Métriques au format Prometheus

## Codes d'Erreur

- `200`: Succès
- `400`: Requête invalide
- `500`: Erreur serveur
- `503`: Service non disponible (RAG system non initialisé)

## Exemples avec cURL

### Query simple

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Qu'est-ce que Python?"
  }'
```

### Upload document

```bash
curl -X POST http://localhost:8000/api/ingest/upload \
  -F "file=@document.pdf"
```

### Search

```bash
curl "http://localhost:8000/api/search?query=Python&k=5"
```

## Exemples avec Python

```python
import requests

# Query
response = requests.post(
    "http://localhost:8000/api/query",
    json={"question": "Qu'est-ce que Python?"}
)
print(response.json())

# Upload
with open("document.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/api/ingest/upload",
        files={"file": f}
    )
print(response.json())
```




# Architecture du Système RAG

## Vue d'ensemble

Le système RAG (Retrieval-Augmented Generation) est conçu pour fournir des réponses précises en combinant la recherche de documents avec la génération de texte via des LLM.

## Composants Principaux

### 1. Ingestion (`src/rag/ingestion.py`)

- **DocumentIngester**: Charge et traite différents types de documents (PDF, DOCX, TXT)
- **Chunking**: Découpe les documents en chunks avec overlap pour préserver le contexte
- **Intégration MLflow**: Logging automatique des métriques d'ingestion

### 2. Retrieval (`src/rag/retrieval.py`)

- **RetrievalSystem**: Système de recherche vectorielle basé sur ChromaDB
- **Embeddings**: Utilise OpenAI Embeddings pour créer des représentations vectorielles
- **Compression optionnelle**: Utilise LLMChainExtractor pour compresser les résultats

### 3. Generation (`src/rag/generation.py`)

- **RAGGenerator**: Génère des réponses à partir du contexte récupéré
- **Prompt Engineering**: Template optimisé pour le RAG
- **Langfuse Integration**: Traçage des appels LLM pour l'observabilité

### 4. Pipeline (`src/rag/pipeline.py`)

- **RAGPipeline**: Pipeline complet utilisant LangGraph
- **Workflow**: Graph d'état avec nodes pour retrieval et generation
- **Streaming**: Support du streaming pour les réponses en temps réel

## API FastAPI

### Endpoints Principaux

- `POST /api/query`: Requête RAG standard
- `POST /api/query/stream`: Requête RAG avec streaming
- `POST /api/ingest`: Ingestion de documents
- `POST /api/ingest/upload`: Upload et ingestion de fichiers
- `GET /api/search`: Recherche dans le vector store
- `GET /health`: Health check
- `GET /metrics`: Métriques Prometheus

## Monitoring & Observabilité

### Langfuse
- Traçage des appels LLM
- Métriques de latence et coût
- Analyse des prompts et réponses

### Prometheus
- Métriques de performance (latence, throughput)
- Métriques de qualité (nombre de docs récupérés, longueur des réponses)
- Métriques système (requêtes actives, taille du vector store)

### Evidently
- Détection de drift de données
- Monitoring de la qualité des données
- Alertes automatiques

### MLflow
- Tracking des expériences
- Logging des paramètres et métriques
- Registry de modèles

## Infrastructure

### Docker
- Multi-stage build pour optimiser la taille de l'image
- Health checks intégrés
- Volumes pour la persistance des données

### Kubernetes
- Deployment avec réplicas pour haute disponibilité
- Service pour exposition interne
- Ingress pour exposition externe
- PVC pour persistance des données (ChromaDB, MLflow)
- ConfigMaps et Secrets pour la configuration

### CI/CD GitLab
- Tests automatiques (pytest, linting)
- Build et push d'images Docker
- Déploiement automatique (staging) et manuel (production)
- GitOps avec mise à jour des manifests

## Flux de Données

```
Document → Ingestion → Chunking → Embedding → Vector Store
                                                      ↓
User Query → Embedding → Similarity Search → Retrieval
                                                      ↓
Context Documents + Query → LLM → Generated Answer
```

## Sécurité

- Secrets gérés via Kubernetes Secrets
- Variables d'environnement pour les clés API
- Health checks et readiness probes
- Resource limits pour éviter les surcharges

## Scalabilité

- Horizontal scaling via Kubernetes replicas
- Vector store partagé via PVC ReadWriteMany
- Load balancing automatique via Service
- Caching possible au niveau de l'API




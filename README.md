# RAG System avec Kubernetes

Système RAG (Retrieval-Augmented Generation) complet avec déploiement Kubernetes, CI/CD GitOps, et monitoring.

## 🏗️ Architecture

- **RAG Engine**: LangChain + LangGraph pour le pipeline de retrieval et génération
- **API**: FastAPI pour l'exposition des endpoints
- **Vector Store**: ChromaDB pour le stockage des embeddings
- **Monitoring**: Langfuse, Prometheus, Grafana, Evidently
- **ML Engineering**: MLflow pour le tracking des expériences
- **Infrastructure**: Docker + Kubernetes avec GitOps

## 📁 Structure du Projet

```
rag_kube/
├── src/
│   ├── rag/              # Core RAG logic
│   ├── api/              # FastAPI application
│   ├── monitoring/       # Monitoring & observability
│   └── utils/            # Utilities
├── k8s/                  # Kubernetes manifests
├── docker/               # Dockerfiles
├── .gitlab-ci.yml        # CI/CD pipeline
├── mlflow/               # MLflow configuration
└── docs/                 # Documentation
```

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.10+
- Docker & Docker Compose
- Kubernetes cluster (minikube/kind pour le dev)
- kubectl configuré

### Installation Locale

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Lancer l'API
uvicorn src.api.main:app --reload
```

### Avec Docker

```bash
docker-compose up -d
```

### Avec Kubernetes

```bash
# Appliquer les manifests
kubectl apply -f k8s/

# Vérifier le déploiement
kubectl get pods -n rag-system
```

## 🔧 Configuration

Copier `.env.example` vers `.env` et configurer :

- `OPENAI_API_KEY`: Clé API OpenAI (ou autre provider)
- `LANGFUSE_SECRET_KEY`: Clé secrète Langfuse
- `LANGFUSE_PUBLIC_KEY`: Clé publique Langfuse
- `MLFLOW_TRACKING_URI`: URI du serveur MLflow

## 📊 Monitoring

- **Langfuse**: http://localhost:3000 (traces LLM)
- **Prometheus**: http://localhost:9090 (métriques)
- **Grafana**: http://localhost:3001 (dashboards)
- **MLflow**: http://localhost:5000 (experiments)

## 🧪 Tests

```bash
pytest tests/
```

## 📝 CI/CD

Le pipeline GitLab CI/CD est configuré pour :
- Tests automatiques
- Build Docker images
- Déploiement GitOps avec ArgoCD/Flux

## 📚 Documentation

Voir `docs/` pour la documentation détaillée.

## 🤝 Contribution

1. Créer une branche feature
2. Faire les modifications
3. Pousser et créer une MR

## 📄 Licence

MIT




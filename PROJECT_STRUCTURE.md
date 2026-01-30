# Structure du Projet RAG

## Vue d'ensemble

Ce projet implémente un système RAG (Retrieval-Augmented Generation) complet avec toutes les technologies demandées.

## Structure des Fichiers

```
rag_kube/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── config.py                 # Configuration avec Pydantic Settings
│   ├── api/                      # API FastAPI
│   │   ├── __init__.py
│   │   └── main.py              # Application FastAPI principale
│   ├── rag/                      # Core RAG logic
│   │   ├── __init__.py
│   │   ├── ingestion.py         # Ingestion et chunking de documents
│   │   ├── retrieval.py         # Système de recherche vectorielle
│   │   ├── generation.py        # Génération de réponses avec LLM
│   │   └── pipeline.py           # Pipeline complet avec LangGraph
│   ├── monitoring/               # Monitoring & Observabilité
│   │   ├── __init__.py
│   │   ├── prometheus.py        # Métriques Prometheus
│   │   └── evidently.py         # Monitoring Evidently AI
│   └── utils/                    # Utilitaires
│       ├── __init__.py
│       └── mlflow_utils.py      # Utilitaires MLflow
│
├── tests/                         # Tests unitaires
│   ├── __init__.py
│   ├── test_api.py              # Tests API
│   └── test_rag.py              # Tests RAG
│
├── k8s/                          # Manifests Kubernetes
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secret.yaml.example
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   ├── mlflow-deployment.yaml
│   └── kustomization.yaml
│
├── docker/                       # Configurations Docker
│   ├── prometheus/
│   │   └── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── dashboard.yml
│       └── datasources/
│           └── prometheus.yml
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── API.md
│
├── scripts/                      # Scripts utilitaires
│   ├── example_usage.py         # Exemple d'utilisation
│   ├── start.sh                 # Script de démarrage (Linux/Mac)
│   └── start.ps1                # Script de démarrage (Windows)
│
├── .gitlab-ci.yml                # Pipeline CI/CD GitLab
├── .gitlab/                      # Configuration GitLab
│   └── ci-variables.md
├── Dockerfile                    # Image Docker principale
├── docker-compose.yml           # Docker Compose pour développement
├── Makefile                      # Commandes Make
├── requirements.txt              # Dépendances Python
├── .gitignore                    # Fichiers ignorés par Git
├── README.md                     # Documentation principale
└── PROJECT_STRUCTURE.md          # Ce fichier
```

## Technologies Utilisées

### Core RAG
- ✅ **LangChain**: Framework pour applications LLM
- ✅ **LangGraph**: Pipeline de workflow avec graphes d'état
- ✅ **ChromaDB**: Vector store pour embeddings
- ✅ **OpenAI**: Embeddings et LLM

### API & Framework
- ✅ **FastAPI**: Framework web moderne et performant
- ✅ **Uvicorn**: Serveur ASGI
- ✅ **Pydantic**: Validation de données

### Monitoring & Observabilité
- ✅ **Langfuse**: Traçage des appels LLM
- ✅ **Prometheus**: Collecte de métriques
- ✅ **Grafana**: Visualisation des métriques
- ✅ **Evidently**: Monitoring de la qualité des données

### ML Engineering
- ✅ **MLflow**: Tracking d'expériences et registry de modèles
- ✅ **DVC**: Versioning de données (prêt pour intégration)

### Infrastructure
- ✅ **Docker**: Containerisation
- ✅ **Kubernetes**: Orchestration de conteneurs
- ✅ **GitLab CI/CD**: Pipeline d'intégration continue
- ✅ **GitOps**: Déploiement déclaratif

## Fonctionnalités Implémentées

### RAG Core
- [x] Ingestion de documents (PDF, DOCX, TXT)
- [x] Chunking avec overlap
- [x] Embeddings avec OpenAI
- [x] Recherche vectorielle avec ChromaDB
- [x] Génération de réponses avec LLM
- [x] Pipeline complet avec LangGraph
- [x] Support du streaming

### API
- [x] Endpoint de query RAG
- [x] Endpoint de query streaming
- [x] Endpoint d'ingestion de documents
- [x] Endpoint d'upload de fichiers
- [x] Endpoint de recherche
- [x] Health check
- [x] Métriques Prometheus

### Monitoring
- [x] Métriques Prometheus (latence, throughput, qualité)
- [x] Intégration Langfuse pour traçage LLM
- [x] Support Evidently pour drift detection
- [x] Logging MLflow pour expériences

### Infrastructure
- [x] Dockerfile multi-stage
- [x] Docker Compose avec tous les services
- [x] Manifests Kubernetes complets
- [x] ConfigMaps et Secrets
- [x] PersistentVolumeClaims
- [x] Ingress pour exposition externe
- [x] Health checks et readiness probes

### CI/CD
- [x] Pipeline GitLab CI/CD
- [x] Tests automatiques
- [x] Linting et formatage
- [x] Build et push d'images Docker
- [x] Déploiement automatique staging
- [x] Déploiement manuel production
- [x] Support GitOps

## Prochaines Étapes Possibles

### Améliorations RAG
- [ ] Support de plus de formats de documents
- [ ] Reranking des résultats de recherche
- [ ] Support multi-modal (images, audio)
- [ ] Cache des embeddings
- [ ] Fine-tuning de modèles d'embedding

### Infrastructure
- [ ] Support vLLM pour inference locale
- [ ] Intégration Ray pour traitement distribué
- [ ] Auto-scaling basé sur les métriques
- [ ] Backup automatique du vector store
- [ ] Multi-région deployment

### Monitoring
- [ ] Dashboards Grafana personnalisés
- [ ] Alertes automatiques
- [ ] A/B testing de modèles
- [ ] Analyse de coûts LLM

### Sécurité
- [ ] Authentification JWT
- [ ] Rate limiting
- [ ] Audit logging
- [ ] Chiffrement des données sensibles

## Utilisation

Voir `README.md` et `docs/` pour la documentation complète.




# Système RAG

Système **RAG** (Retrieval-Augmented Generation) pour interroger vos documents via une interface web, avec déploiement Kubernetes, observabilité (Langfuse, MLflow) et CI/CD.

---

## Présentation de l'application

L'interface web permet d'**ajouter des documents** (PDF, DOCX, TXT) au système et de **poser des questions** pour obtenir des réponses basées sur leur contenu.

![Interface Système RAG — Ajout de documents](images/Screenshot%20application.png)

- **Onglet « Ajouter des Documents »** : upload de fichiers (glisser-déposer ou sélection), formats supportés PDF, DOCX, TXT.
- **Onglet « Poser une Question »** : saisie de la question, affichage de la réponse, des sources et des scores d’évaluation (automatique + notation manuelle).

---

## Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| **Ingestion** | Chargement et chunking de PDF, DOCX, TXT ; embeddings et stockage dans ChromaDB. |
| **Recherche** | Recherche par similarité dans le vector store, contexte envoyé au LLM. |
| **Génération** | Réponses générées via LangChain/LangGraph avec modèle configurable (OpenAI, etc.). |
| **Interface web** | Une seule page : upload de documents et questions/réponses avec scores. |
| **Évaluation** | Scores automatiques (pertinence, complétude) et notation utilisateur (0–5 ou 👍/👎) envoyée à Langfuse. |
| **Observabilité** | Traces LLM et scores dans Langfuse ; métriques d’ingestion dans MLflow. |
| **Déploiement** | Docker, Kubernetes (manifests dans `k8s/`), pipeline GitLab CI/CD. |

---

## Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│  Interface Web  │────▶│  API FastAPI │────▶│  RAG Engine │
│  (static/.)     │     │  (src/api)   │     │  LangGraph  │
└─────────────────┘     └──────────────┘     └──────┬──────┘
         │                        │                 │
         │                        ▼                 ▼
         │               ┌──────────────┐   ┌─────────────┐
         │               │  Langfuse /  │   │  ChromaDB   │
         │               │  MLflow      │   │  (vecteurs) │
         │               └──────────────┘   └─────────────┘
         ▼
   Upload + Questions
```

- **RAG Engine** : LangChain + LangGraph (retrieval, génération).
- **API** : FastAPI (endpoints query, ingestion, santé, scoring Langfuse).
- **Vector Store** : ChromaDB (embeddings et recherche par similarité).
- **Monitoring** : Langfuse (traces, scores), MLflow (expériences / ingestion), optionnel Prometheus/Grafana/Evidently.

---

## Structure du projet

```
rag_kube/
├── src/
│   ├── api/           # FastAPI (main.py, routes)
│   ├── rag/           # Pipeline RAG (ingestion, retrieval, generation, pipeline)
│   ├── monitoring/    # Evidently, Prometheus
│   ├── utils/         # Langfuse scoring, MLflow REST
│   └── config.py      # Configuration (env)
├── static/            # Interface web (index.html)
├── scripts/           # Scripts CLI (upload, ask_question, start, etc.)
├── k8s/               # Manifests Kubernetes
├── docker/            # Prometheus, Grafana
├── docs/              # Documentation détaillée
├── images/            # Captures d’écran (ex. interface)
├── env.example        # Modèle de variables d’environnement
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Démarrage rapide

### Prérequis

- **Python 3.10+**
- Fichier **`.env`** configuré (voir [Configuration](#-configuration))

### 1. Environnement et dépendances

```bash
# Environnement virtuel
python -m venv venv

# Activation
# Windows (PowerShell) :
.\venv\Scripts\Activate.ps1
# Linux / macOS :
source venv/bin/activate

# Dépendances
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copier le modèle et éditer avec vos clés
cp env.example .env
```

Variables principales : `OPENAI_API_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` (ex. `http://localhost:3000`), optionnel `MLFLOW_TRACKING_URI`. Voir `env.example` pour la liste complète.

### 3. Lancer l’API

**Via le script (recommandé)**  
- Windows : `.\scripts\start.ps1`  
- Linux/macOS : `./scripts/start.sh`  

**Ou manuellement :**

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8001 --reload
```

- **Interface web** : [http://localhost:8001](http://localhost:8001)  
- **Documentation API** : [http://localhost:8001/docs](http://localhost:8001/docs)  

> Si le port 8000 est bloqué sous Windows (erreur socket), le script utilise le port **8001**.

---

## Utilisation

1. **Ajouter des documents**  
   Onglet « Ajouter des Documents » → choisir ou glisser-déposer des fichiers (PDF, DOCX, TXT) → « Uploader le document ».

2. **Poser une question**  
   Onglet « Poser une Question » → saisir la question → envoyer. La réponse, les sources et les scores s’affichent.

3. **Noter une réponse**  
   Utiliser les boutons 👍 / 👎 ou la note 0–5 et optionnellement un commentaire ; les notes sont envoyées à Langfuse.

---

## Configuration

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | Clé API OpenAI (ou autre provider selon le code). |
| `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` | Clés Langfuse pour les traces et scores. |
| `LANGFUSE_HOST` | URL Langfuse (ex. `http://localhost:3000`). |
| `MLFLOW_TRACKING_URI` | URI du serveur MLflow (optionnel). |
| `CHROMA_PERSIST_DIR` | Répertoire de persistance ChromaDB (défaut : `./chroma_db`). |

Détails et exemples dans `env.example`.

---

## Monitoring et observabilité

| Service | URL type | Rôle |
|---------|-----------|------|
| **Langfuse** | http://localhost:3000 | Traces LLM, scores (dont notation utilisateur). |
| **MLflow** | http://localhost:5000 | Suivi des expériences et métriques d’ingestion. |
| **Prometheus** | http://localhost:9090 | Métriques (si déployé). |
| **Grafana** | http://localhost:3001 | Dashboards (si déployé). |

Voir `docs/LANGFUSE_SETUP.md`, `docs/MLFLOW_GUIDE.md` et `docs/` pour le détail.

---

## Déploiement

- **Docker** : `docker-compose up -d` (voir `docker-compose.yml`).
- **Kubernetes** : `kubectl apply -f k8s/` puis vérifier les pods dans le namespace cible (ex. `rag-system`).

Le pipeline GitLab CI/CD (`.gitlab-ci.yml`) peut gérer build d’images et déploiement (ArgoCD/Flux selon configuration).

---

## Tests

```bash
pytest tests/
```

---

## Documentation

- **Interface web** : `README_WEB_INTERFACE.md`, `docs/HOW_TO_ADD_DOCUMENTS.md`
- **Langfuse** : `docs/LANGFUSE_SETUP.md`, `docs/LANGFUSE_SCORING.md`
- **MLflow** : `docs/MLFLOW_GUIDE.md`, `docs/MLFLOW_INTEGRATION.md`
- **Déploiement** : `docs/DEPLOYMENT.md`, `docs/ARCHITECTURE.md`
- **Dépannage** : `docs/TROUBLESHOOTING_USER_RATING.md`, etc.

---

## Licence

MIT

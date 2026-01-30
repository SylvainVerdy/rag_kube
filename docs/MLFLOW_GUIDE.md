# Guide MLflow pour le Système RAG

## 🚀 Démarrage de MLflow

### Option 1 : Avec Docker Compose (Recommandé)

```powershell
docker-compose up mlflow -d
```

MLflow sera accessible sur : **http://localhost:5000**

### Option 2 : Localement avec Python

```powershell
# Activer le venv
.\venv\Scripts\Activate.ps1

# Démarrer MLflow
mlflow server --backend-store-uri file:///$(pwd)/mlflow --default-artifact-root ./mlflow/artifacts --host 0.0.0.0 --port 5000
```

Ou utilisez le script :
```powershell
.\scripts\start_mlflow.ps1
```

## 📊 Accéder à l'Interface

Une fois MLflow démarré, ouvrez votre navigateur sur :

**http://localhost:5000**

## 📈 Ce que vous verrez dans MLflow

### 1. **Experiments (Expériences)**
- Liste de toutes les expériences RAG
- Par défaut : `rag_experiments`

### 2. **Runs (Exécutions)**
Chaque requête RAG crée un run avec :
- **Paramètres** :
  - `question` : La question posée
  - `model` : Le modèle LLM utilisé
  - `embedding_model` : Le modèle d'embedding
  - `document_path` : Chemin du document ingéré
  - `document_type` : Type de document (PDF, DOCX, etc.)

- **Métriques** :
  - `retrieved_docs_count` : Nombre de documents récupérés
  - `answer_length` : Longueur de la réponse
  - `total_chunks` : Nombre de chunks créés
  - `document_chunks` : Chunks par document
  - `avg_chunk_size` : Taille moyenne des chunks
  - `latency_seconds` : Temps de réponse

- **Artifacts** :
  - `answer.txt` : La réponse générée

### 3. **Comparaison de Runs**
- Comparez les performances entre différentes questions
- Analysez l'impact des paramètres (top_k, chunk_size, etc.)

## 🔍 Utilisation

### Voir les métriques d'une requête

1. Allez sur http://localhost:5000
2. Cliquez sur l'expérience `rag_experiments`
3. Sélectionnez un run pour voir les détails

### Comparer plusieurs runs

1. Dans la liste des runs, cochez plusieurs runs
2. Cliquez sur "Compare"
3. Comparez les métriques et paramètres

### Filtrer les runs

Utilisez les filtres pour :
- Filtrer par modèle
- Filtrer par date
- Filtrer par métriques (ex: réponse > 500 caractères)

## 📝 Configuration

Le tracking MLflow est automatiquement activé dans le système RAG. Les métriques sont loggées lors de :
- L'ingestion de documents
- Les requêtes RAG
- Les recherches dans le vector store

## 🔧 Dépannage

### MLflow ne démarre pas

```powershell
# Vérifier que MLflow est installé
pip show mlflow

# Vérifier le port 5000
netstat -ano | findstr :5000
```

### Pas de données dans MLflow

- Vérifiez que `MLFLOW_TRACKING_URI=http://localhost:5000` dans `.env`
- Vérifiez que MLflow est démarré avant de faire des requêtes
- Vérifiez les logs de l'API pour des erreurs MLflow

### Erreur de connexion

- Assurez-vous que MLflow tourne sur le port 5000
- Vérifiez que l'URI dans `.env` correspond au serveur MLflow


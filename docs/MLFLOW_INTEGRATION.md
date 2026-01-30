# Intégration MLflow avec le Système RAG

## ✅ Statut

L'intégration MLflow est **opérationnelle** via l'API REST, ce qui permet de tracker les métriques même si le module Python MLflow ne peut pas être importé.

## 🚀 Fonctionnement

### Upload de Documents

Lorsque vous uploadez un document via l'interface web ou l'API, le système :

1. **Crée automatiquement un run MLflow** avec le nom `ingest_<nom_fichier>`
2. **Log les paramètres** :
   - `filename` : Nom du fichier uploadé
   - `file_size_bytes` : Taille du fichier en octets
   - `document_path` : Chemin du document
   - `document_type` : Type de document (.pdf, .docx, .txt)

3. **Log les métriques** :
   - `chunks_created` : Nombre de chunks créés lors de l'ingestion
   - `avg_chunk_size` : Taille moyenne des chunks
   - `total_chunks` : Nombre total de chunks
   - `document_chunks` : Nombre de chunks par document

4. **Termine le run** avec le statut `FINISHED` (ou `FAILED` en cas d'erreur)

### Requêtes RAG

Les requêtes RAG peuvent également être trackées dans MLflow (à implémenter si nécessaire).

## 📊 Accéder aux Données

1. **Ouvrez MLflow** : http://localhost:5000
2. **Sélectionnez l'expérience** : `rag_experiments`
3. **Consultez les runs** : Chaque upload crée un nouveau run

## 🔧 Architecture Technique

### Client REST MLflow

Le système utilise un client REST (`src/utils/mlflow_rest.py`) qui :
- Communique directement avec l'API HTTP de MLflow
- N'a pas besoin du module Python MLflow
- Fonctionne même si les dépendances MLflow sont incomplètes

### Fallback Automatique

Le code essaie d'abord d'utiliser le SDK Python MLflow, puis bascule automatiquement sur le client REST si l'import échoue :

```python
# Try Python SDK first
try:
    import mlflow
    # Use Python SDK
except ImportError:
    # Fallback to REST API
    from src.utils.mlflow_rest import get_mlflow_client
```

## 🧪 Test

Pour tester l'intégration :

```powershell
# Test du client REST
.\venv\Scripts\python.exe scripts/test_mlflow_rest.py
```

## 📝 Exemple de Run MLflow

Après un upload, vous verrez dans MLflow :

**Run Name**: `ingest_mon_document.pdf`

**Paramètres**:
- `filename`: `mon_document.pdf`
- `file_size_bytes`: `1234567`
- `document_type`: `.pdf`

**Métriques**:
- `chunks_created`: `110`
- `avg_chunk_size`: `850.5`
- `total_chunks`: `110`

## 🐛 Dépannage

### Aucun run n'apparaît dans MLflow

1. Vérifiez que MLflow est démarré : `netstat -ano | findstr :5000`
2. Vérifiez les logs de l'API pour des erreurs MLflow
3. Testez le client REST : `.\venv\Scripts\python.exe scripts/test_mlflow_rest.py`

### Erreurs de connexion

- Vérifiez que `MLFLOW_TRACKING_URI=http://localhost:5000` dans `.env`
- Assurez-vous que MLflow est accessible sur le port 5000

### Expérience non trouvée

L'expérience `rag_experiments` est créée automatiquement au premier run. Si elle n'existe pas, le système utilisera l'expérience par défaut (ID: 0).


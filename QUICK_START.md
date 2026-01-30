# Guide de Démarrage Rapide

## ✅ Étape 1: Vérifier que .env existe

Le fichier `.env` doit être présent à la racine du projet avec vos clés API.

## ✅ Étape 2: Installer les dépendances

```powershell
# Créer l'environnement virtuel (si pas déjà fait)
python -m venv venv

# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

## ✅ Étape 3: Lancer l'API

```powershell
# Lancer l'API en mode développement
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera accessible sur: http://localhost:8000

## ✅ Étape 4: Tester l'API

### Health Check
```powershell
curl http://localhost:8000/health
```

Ou ouvrir dans le navigateur: http://localhost:8000/health

### Documentation API
Ouvrir: http://localhost:8000/docs (interface Swagger interactive)

### Tester une requête RAG
```powershell
# Avec PowerShell
$body = @{
    question = "Qu'est-ce que Python?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/query" -Method Post -Body $body -ContentType "application/json"
```

## 📝 Notes Importantes

1. **Premier lancement**: Le système va initialiser ChromaDB et créer les répertoires nécessaires
2. **Ingestion de documents**: Avant de poser des questions, vous devez ingérer des documents
3. **MLflow**: Si MLflow n'est pas lancé, les logs MLflow seront ignorés (pas bloquant)

## 🔧 Dépannage

### Erreur "OPENAI_API_KEY not found"
- Vérifier que le fichier `.env` existe à la racine
- Vérifier que la variable `OPENAI_API_KEY` est bien définie dans `.env`

### Erreur d'import
- Vérifier que toutes les dépendances sont installées: `pip install -r requirements.txt`

### Port déjà utilisé
- Changer le port: `uvicorn src.api.main:app --reload --port 8001`


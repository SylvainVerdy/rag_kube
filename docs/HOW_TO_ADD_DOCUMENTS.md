# Comment Ajouter des Documents au Système RAG

Il existe plusieurs méthodes pour ajouter des documents au système RAG.

## Méthode 1 : Upload via l'Interface Web (Recommandé)

### Étape 1 : Démarrer l'API

```powershell
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Étape 2 : Accéder à la Documentation Interactive

Ouvrez votre navigateur sur : **http://localhost:8000/docs**

### Étape 3 : Utiliser l'endpoint `/api/ingest/upload`

1. Trouvez l'endpoint `POST /api/ingest/upload` dans la documentation
2. Cliquez sur "Try it out"
3. Cliquez sur "Choose File" et sélectionnez votre document (PDF, DOCX, ou TXT)
4. Cliquez sur "Execute"
5. Vous verrez la réponse avec le nombre de chunks créés

## Méthode 2 : Upload via cURL (Ligne de commande)

### Windows PowerShell

```powershell
# Pour un fichier PDF
$filePath = "C:\chemin\vers\votre\document.pdf"
$uri = "http://localhost:8000/api/ingest/upload"

$form = @{
    file = Get-Item -Path $filePath
}

Invoke-RestMethod -Uri $uri -Method Post -Form $form
```

### Linux/Mac

```bash
curl -X POST "http://localhost:8000/api/ingest/upload" \
  -F "file=@/chemin/vers/votre/document.pdf"
```

## Méthode 3 : Upload via Python

Créez un fichier `upload_document.py` :

```python
import requests

# URL de l'API
url = "http://localhost:8000/api/ingest/upload"

# Chemin vers votre document
file_path = "votre_document.pdf"

# Upload du fichier
with open(file_path, "rb") as f:
    files = {"file": (file_path, f, "application/pdf")}
    response = requests.post(url, files=files)

print(response.json())
```

Exécutez :
```powershell
python upload_document.py
```

## Méthode 4 : Ingestion depuis un Répertoire

Si vous avez plusieurs documents dans un dossier :

### Via l'API

```powershell
$body = @{
    path = "C:\chemin\vers\repertoire\documents"
    is_directory = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/ingest" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

### Via Python

```python
import requests

url = "http://localhost:8000/api/ingest"
data = {
    "path": "/chemin/vers/repertoire/documents",
    "is_directory": True
}

response = requests.post(url, json=data)
print(response.json())
```

## Formats de Fichiers Supportés

- **PDF** (`.pdf`)
- **Word** (`.docx`)
- **Texte** (`.txt`)

## Vérifier que les Documents sont Ajoutés

### Via l'API de Recherche

```powershell
# Rechercher dans les documents ajoutés
$query = "votre recherche"
Invoke-RestMethod -Uri "http://localhost:8000/api/search?query=$query&k=5"
```

### Via Python

```python
import requests

url = "http://localhost:8000/api/search"
params = {"query": "votre recherche", "k": 5}
response = requests.get(url, params=params)
print(response.json())
```

## Exemple Complet : Script d'Upload

Créez `scripts/upload_document.py` :

```python
"""Script pour uploader un document au système RAG"""

import requests
import sys
from pathlib import Path

def upload_document(file_path: str, api_url: str = "http://localhost:8000"):
    """Upload un document au système RAG"""
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Erreur: Le fichier {file_path} n'existe pas")
        return False
    
    # Vérifier le format
    supported_formats = {".pdf", ".docx", ".txt"}
    if file_path.suffix.lower() not in supported_formats:
        print(f"❌ Erreur: Format non supporté. Formats acceptés: {supported_formats}")
        return False
    
    url = f"{api_url}/api/ingest/upload"
    
    print(f"📤 Upload de {file_path.name}...")
    
    try:
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}
            response = requests.post(url, files=files)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Succès! {result['message']}")
            print(f"📊 Nombre de chunks créés: {result['chunks_count']}")
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de l'upload: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   Détails: {e.response.text}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_document.py <chemin_vers_fichier>")
        print("Exemple: python upload_document.py document.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = upload_document(file_path)
    sys.exit(0 if success else 1)
```

Utilisation :
```powershell
python scripts/upload_document.py "C:\chemin\vers\document.pdf"
```

## Notes Importantes

1. **Premier Upload** : Le système va créer automatiquement le répertoire `chroma_db` pour stocker les embeddings
2. **Documents Multiples** : Vous pouvez uploader plusieurs documents, ils seront tous ajoutés au même vector store
3. **Chunking Automatique** : Les documents sont automatiquement découpés en chunks (par défaut: 1000 caractères avec overlap de 200)
4. **Persistance** : Les documents sont stockés dans `./chroma_db` et persistent entre les redémarrages

## Dépannage

### Erreur "RAG system not initialized"
- Assurez-vous que l'API est bien démarrée
- Vérifiez que le fichier `.env` contient `OPENAI_API_KEY`

### Erreur "Unsupported file type"
- Vérifiez que le fichier est en format PDF, DOCX ou TXT
- Vérifiez l'extension du fichier

### Erreur de connexion
- Vérifiez que l'API tourne sur le bon port (8000 par défaut)
- Vérifiez l'URL dans votre requête


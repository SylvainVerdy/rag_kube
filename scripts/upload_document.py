"""Script pour uploader un document au système RAG"""

import requests
import sys
from pathlib import Path

def upload_document(file_path: str, api_url: str = "http://localhost:8001"):
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
        # Vérifier la taille du fichier
        file_size = file_path.stat().st_size / (1024 * 1024)  # Taille en MB
        print(f"📏 Taille du fichier: {file_size:.2f} MB")
        
        if file_size > 50:
            print("⚠️  Attention: Fichier volumineux, l'upload peut prendre du temps...")
        
        # Configuration avec timeout plus long pour les gros fichiers
        timeout = (30, 300)  # (connect timeout, read timeout) en secondes
        
        with open(file_path, "rb") as f:
            files = {"file": (file_path.name, f, "application/octet-stream")}
            print("⏳ Envoi en cours...")
            response = requests.post(url, files=files, timeout=timeout)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Succès! {result['message']}")
            print(f"📊 Nombre de chunks créés: {result['chunks_count']}")
            return True
            
    except requests.exceptions.Timeout:
        print(f"❌ Erreur: Timeout - Le fichier est trop volumineux ou l'API ne répond pas")
        print(f"   Essayez de réduire la taille du fichier ou augmentez le timeout")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Erreur de connexion: Impossible de se connecter à l'API")
        print(f"   Vérifiez que l'API est démarrée sur {api_url}")
        print(f"   Détails: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de l'upload: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"   Détails: {error_detail}")
            except:
                print(f"   Détails: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python upload_document.py <chemin_vers_fichier>")
        print("Exemple: python upload_document.py document.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = upload_document(file_path)
    sys.exit(0 if success else 1)


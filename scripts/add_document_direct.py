"""Script pour ajouter directement un document au système RAG (sans API)"""

import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import RetrievalSystem

def add_document_direct(file_path: str):
    """Ajouter directement un document au vector store"""
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ Erreur: Le fichier {file_path} n'existe pas")
        return False
    
    # Vérifier le format
    supported_formats = {".pdf", ".docx", ".txt"}
    if file_path.suffix.lower() not in supported_formats:
        print(f"❌ Erreur: Format non supporté. Formats acceptés: {supported_formats}")
        return False
    
    print(f"📤 Traitement de {file_path.name}...")
    print(f"📏 Taille: {file_path.stat().st_size / (1024 * 1024):.2f} MB")
    
    try:
        # Initialiser les composants
        print("🔧 Initialisation du système RAG...")
        ingester = DocumentIngester(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        retrieval_system = RetrievalSystem(
            embedding_model=settings.embedding_model,
            top_k=settings.top_k
        )
        
        # Ingérer le document
        print("📄 Ingestion du document...")
        chunks = ingester.ingest(str(file_path), is_directory=False)
        
        print(f"✂️  Document découpé en {len(chunks)} chunks")
        
        # Ajouter au vector store
        print("💾 Ajout au vector store...")
        retrieval_system.add_documents(chunks)
        
        print(f"✅ Succès! Document ajouté avec {len(chunks)} chunks")
        print(f"📁 Vector store sauvegardé dans: {settings.chroma_persist_directory}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_document_direct.py <chemin_vers_fichier>")
        print("Exemple: python add_document_direct.py document.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = add_document_direct(file_path)
    sys.exit(0 if success else 1)


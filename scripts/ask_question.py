"""Script pour poser une question au système RAG"""

import requests
import sys
import json

def ask_question(question: str, api_url: str = "http://localhost:8001", chat_history=None):
    """Poser une question au système RAG via l'API"""
    
    url = f"{api_url}/api/query"
    
    payload = {
        "question": question
    }
    
    if chat_history:
        payload["chat_history"] = chat_history
    
    print(f"❓ Question: {question}")
    print("⏳ Recherche en cours...")
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        
        print("\n" + "="*60)
        print("✅ RÉPONSE:")
        print("="*60)
        print(result["answer"])
        print("\n" + "="*60)
        print(f"📚 Sources utilisées: {len(result.get('sources', []))} document(s)")
        print(f"🤖 Modèle: {result.get('model', 'N/A')}")
        
        if result.get('sources'):
            print("\n📄 Sources:")
            for i, source in enumerate(result['sources'][:3], 1):  # Afficher max 3 sources
                print(f"\n  {i}. Extrait:")
                print(f"     {source.get('content', '')[:200]}...")
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Erreur: Impossible de se connecter à l'API sur {api_url}")
        print("   Vérifiez que l'API est démarrée avec: uvicorn src.api.main:app --port 8001")
        return None
    except requests.exceptions.Timeout:
        print("❌ Erreur: Timeout - La requête prend trop de temps")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la requête: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"   Détails: {error_detail}")
            except:
                print(f"   Détails: {e.response.text}")
        return None

def ask_question_direct(question: str):
    """Poser une question directement (sans API)"""
    import sys
    from pathlib import Path
    
    # Ajouter le répertoire racine au path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    from src.rag.pipeline import RAGPipeline
    from src.rag.retrieval import RetrievalSystem
    from src.rag.generation import RAGGenerator
    from src.config import settings
    
    print(f"❓ Question: {question}")
    print("⏳ Initialisation du système RAG...")
    
    try:
        retrieval = RetrievalSystem(
            embedding_model=settings.embedding_model,
            top_k=settings.top_k
        )
        
        generator = RAGGenerator(
            llm_model=settings.llm_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )
        
        pipeline = RAGPipeline(retrieval, generator)
        
        print("🔍 Recherche dans les documents...")
        result = pipeline.run(question=question)
        
        print("\n" + "="*60)
        print("✅ RÉPONSE:")
        print("="*60)
        print(result["answer"])
        print("\n" + "="*60)
        print(f"📚 Sources utilisées: {len(result.get('sources', []))} document(s)")
        print(f"🤖 Modèle: {result.get('model', 'N/A')}")
        
        if result.get('sources'):
            print("\n📄 Sources:")
            for i, source in enumerate(result['sources'][:3], 1):
                print(f"\n  {i}. Extrait:")
                content = source.get('content', '')
                if isinstance(content, str):
                    print(f"     {content[:200]}...")
                else:
                    print(f"     {str(content)[:200]}...")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ask_question.py <question> [--direct]")
        print("\nExemples:")
        print('  python ask_question.py "Quels sont les avantages mentionnés?"')
        print('  python ask_question.py "Quels sont les avantages?" --direct')
        print("\nOptions:")
        print("  --direct  : Utilise le système RAG directement (sans API)")
        sys.exit(1)
    
    question = sys.argv[1]
    use_direct = "--direct" in sys.argv
    
    if use_direct:
        result = ask_question_direct(question)
    else:
        result = ask_question(question)
    
    sys.exit(0 if result else 1)


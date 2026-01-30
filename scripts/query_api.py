"""Script simple pour interroger l'API RAG"""

import requests
import sys

def query_rag(question: str, api_url: str = "http://localhost:8001"):
    """Interroger le système RAG"""
    
    url = f"{api_url}/api/query"
    
    try:
        response = requests.post(
            url,
            json={"question": question},
            timeout=60
        )
        response.raise_for_status()
        
        result = response.json()
        
        print(f"\n❓ Question: {question}\n")
        print(f"✅ Réponse:\n{result['answer']}\n")
        print(f"📚 {len(result.get('sources', []))} source(s) utilisée(s)")
        
        return result
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Erreur: L'API n'est pas accessible sur {api_url}")
        print("   Démarrez l'API avec: uvicorn src.api.main:app --port 8001")
        return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        question = input("Posez votre question: ")
    else:
        question = " ".join(sys.argv[1:])
    
    query_rag(question)


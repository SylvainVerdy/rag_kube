"""Script pour créer un score Langfuse"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.langfuse_scoring import create_score, score_rag_response, get_langfuse_client
from config import settings

def main():
    print("🔍 Test de création de scores Langfuse")
    print("=" * 50)
    print(f"🌐 Langfuse Host: {settings.langfuse_host}")
    print()
    
    # Test 1: Simple score
    print("1️⃣  Test: Création d'un score simple")
    score_id = create_score(
        trace_id=None,  # None = score global
        name="test_score",
        value=0.85,
        comment="Test score from script",
        metadata={"test": True, "source": "script"}
    )
    
    if score_id:
        print(f"   ✅ Score créé: {score_id}")
    else:
        print("   ❌ Échec de création du score")
    print()
    
    # Test 2: RAG scoring
    print("2️⃣  Test: Scoring d'une réponse RAG")
    scores = score_rag_response(
        trace_id=None,
        answer="This is a test answer that demonstrates the RAG system's ability to generate responses based on retrieved context.",
        question="What is the purpose of this system?",
        sources_count=3,
        answer_length=120,
        relevance_score=0.9,
        completeness_score=0.8
    )
    
    print(f"   ✅ {len(scores)} scores créés:")
    for name, score_id in scores.items():
        if score_id:
            print(f"      - {name}: {score_id}")
        else:
            print(f"      - {name}: ❌ Échec")
    print()
    
    # Test 3: Direct client usage
    print("3️⃣  Test: Utilisation directe du client")
    client = get_langfuse_client()
    if client:
        try:
            score = client.create_score(
                name="direct_test",
                value=0.75,
                comment="Direct client test"
            )
            print(f"   ✅ Score créé via client direct")
            if hasattr(score, 'id'):
                print(f"      Score ID: {score.id}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    else:
        print("   ⚠️  Client Langfuse non disponible")
    print()
    
    print("🌐 Vérifiez les scores dans Langfuse: http://localhost:3000")
    print("   Allez dans 'Scores' ou 'Traces' pour voir les scores créés")

if __name__ == "__main__":
    main()


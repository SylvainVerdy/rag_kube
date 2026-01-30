"""Test de création du score user_rating dans Langfuse"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.langfuse_scoring import create_score, get_langfuse_client
from config import settings

def main():
    print("🔍 Test de création du score user_rating")
    print("=" * 50)
    print(f"🌐 Langfuse Host: {settings.langfuse_host}")
    print()
    
    # Test 1: Créer un score user_rating sans trace_id
    print("1️⃣  Test: Créer un score user_rating (sans trace_id)")
    score_id = create_score(
        trace_id=None,
        name="user_rating",
        value=0.85,
        comment="Test de notation manuelle",
        metadata={
            "question": "Test question",
            "rating_type": "thumbs_up",
            "evaluation_type": "manual"
        }
    )
    
    if score_id:
        print(f"   ✅ Score créé: {score_id}")
    else:
        print("   ❌ Échec de création du score")
    print()
    
    # Test 2: Créer un score user_rating avec le client direct
    print("2️⃣  Test: Créer un score user_rating via client direct")
    client = get_langfuse_client()
    if client:
        try:
            score = client.create_score(
                name="user_rating",
                value=0.9,
                data_type="NUMERIC",
                comment="Test direct avec client",
                metadata={
                    "test": True,
                    "rating_type": "thumbs_up"
                }
            )
            print(f"   ✅ Score créé via client direct")
            if hasattr(score, 'id'):
                print(f"      Score ID: {score.id}")
            print(f"      Score: {score}")
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("   ⚠️  Client Langfuse non disponible")
    print()
    
    # Test 3: Vérifier les paramètres requis
    print("3️⃣  Test: Vérification des paramètres")
    print(f"   Secret Key: {'✅' if settings.langfuse_secret_key else '❌'}")
    print(f"   Public Key: {'✅' if settings.langfuse_public_key else '❌'}")
    print(f"   Host: {settings.langfuse_host}")
    print(f"   Enabled: {settings.enable_langfuse}")
    print()
    
    print("🌐 Vérifiez dans Langfuse: http://localhost:3000")
    print("   Allez dans 'Scores' pour voir les scores créés")
    print("   Recherchez 'user_rating' dans la liste des scores")

if __name__ == "__main__":
    main()

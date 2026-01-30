"""Script pour vérifier les scores dans Langfuse"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.langfuse_scoring import get_langfuse_client
from config import settings

def main():
    print("🔍 Vérification des scores dans Langfuse")
    print("=" * 50)
    print(f"🌐 Langfuse Host: {settings.langfuse_host}")
    print()
    
    client = get_langfuse_client()
    if not client:
        print("❌ Client Langfuse non disponible")
        return
    
    try:
        # Try to fetch scores using the client
        # Note: Langfuse Python SDK may not have a direct method to list scores
        # But we can verify the client works
        
        print("✅ Client Langfuse disponible")
        print()
        print("📋 Pour voir les scores user_rating dans Langfuse:")
        print()
        print("1. Ouvrez http://localhost:3000 dans votre navigateur")
        print("2. Cliquez sur 'Scores' dans le menu de gauche")
        print("3. Recherchez 'user_rating' dans la liste")
        print()
        print("OU")
        print()
        print("1. Allez dans 'Traces'")
        print("2. Cliquez sur une trace récente")
        print("3. Regardez la section 'Scores' de la trace")
        print()
        print("💡 Astuce: Les scores peuvent prendre quelques secondes à apparaître")
        print("   Rafraîchissez la page si nécessaire")
        print()
        
        # Test: Create a test score to verify it works
        print("🧪 Test: Création d'un score de test...")
        try:
            test_score = client.create_score(
                name="test_user_rating",
                value=0.75,
                comment="Score de test pour vérification"
            )
            print("   ✅ Score de test créé")
            print("   Vérifiez dans Langfuse - vous devriez voir 'test_user_rating'")
        except Exception as e:
            print(f"   ❌ Erreur lors de la création du score de test: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


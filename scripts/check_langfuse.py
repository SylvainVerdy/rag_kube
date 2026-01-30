"""Script pour vérifier la configuration Langfuse"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings

print("🔍 Vérification de la configuration Langfuse\n")
print("=" * 50)

# Vérifier les clés
print(f"✅ Langfuse activé: {settings.enable_langfuse}")
print(f"🌐 Host: {settings.langfuse_host}")

if settings.langfuse_secret_key:
    print(f"🔑 Secret Key: {'*' * 20}...{settings.langfuse_secret_key[-4:]}")
else:
    print("❌ Secret Key: NON CONFIGURÉ")

if settings.langfuse_public_key:
    print(f"🔑 Public Key: {settings.langfuse_public_key[:20]}...")
else:
    print("❌ Public Key: NON CONFIGURÉ")

print("\n" + "=" * 50)

# Test de connexion
if settings.enable_langfuse and settings.langfuse_secret_key and settings.langfuse_public_key:
    try:
        from langfuse.langchain import CallbackHandler
        import os
        
        # Le CallbackHandler utilise les variables d'environnement
        os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
        os.environ["LANGFUSE_HOST"] = settings.langfuse_host
        
        handler = CallbackHandler(
            public_key=settings.langfuse_public_key
        )
        print("✅ Langfuse peut être initialisé correctement!")
        print(f"   Connecté à: {settings.langfuse_host}")
        print("\n💡 Le CallbackHandler sera utilisé automatiquement lors des appels LLM")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        print("\n💡 Vérifiez:")
        print("   1. Que Langfuse tourne sur", settings.langfuse_host)
        print("   2. Que les clés API sont correctes")
        print("   3. Que l'URL est accessible")
        import traceback
        traceback.print_exc()
else:
    print("⚠️  Langfuse n'est pas complètement configuré")
    print("\n💡 Pour configurer:")
    print("   1. Ajoutez LANGFUSE_SECRET_KEY dans .env")
    print("   2. Ajoutez LANGFUSE_PUBLIC_KEY dans .env")
    print("   3. Vérifiez LANGFUSE_HOST (http://localhost:3000 pour local)")


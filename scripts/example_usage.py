"""Exemple d'utilisation du système RAG"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import settings
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import RetrievalSystem
from src.rag.generation import RAGGenerator
from src.rag.pipeline import RAGPipeline
from src.utils.mlflow_utils import init_mlflow, start_run, log_rag_metrics
import time


def main():
    """Exemple d'utilisation complète"""
    
    # Initialiser MLflow
    init_mlflow()
    
    with start_run(run_name="example_rag_run"):
        print("🚀 Initialisation du système RAG...")
        
        # 1. Ingestion de documents
        print("\n📄 Étape 1: Ingestion de documents")
        ingester = DocumentIngester(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
        
        # Exemple: ingérer un document (remplacer par votre chemin)
        # documents_path = "./data/sample_document.pdf"
        # if os.path.exists(documents_path):
        #     chunks = ingester.ingest(documents_path)
        #     print(f"✅ {len(chunks)} chunks créés")
        # else:
        #     print("⚠️  Aucun document trouvé, création de chunks d'exemple")
        #     from langchain.schema import Document
        #     chunks = [
        #         Document(
        #             page_content="Python est un langage de programmation de haut niveau.",
        #             metadata={"source": "example.txt"}
        #         )
        #     ]
        
        # Pour l'exemple, créons des chunks factices
        from langchain.schema import Document
        chunks = [
            Document(
                page_content="Python est un langage de programmation de haut niveau, interprété et orienté objet.",
                metadata={"source": "example1.txt"}
            ),
            Document(
                page_content="LangChain est un framework pour développer des applications avec des LLM.",
                metadata={"source": "example2.txt"}
            ),
            Document(
                page_content="RAG (Retrieval-Augmented Generation) combine recherche et génération pour améliorer les réponses.",
                metadata={"source": "example3.txt"}
            ),
        ]
        
        # 2. Initialisation du système de retrieval
        print("\n🔍 Étape 2: Initialisation du système de retrieval")
        retrieval_system = RetrievalSystem(
            embedding_model=settings.embedding_model,
            top_k=settings.top_k
        )
        
        # Ajouter les documents au vector store
        retrieval_system.add_documents(chunks)
        print(f"✅ {len(chunks)} documents ajoutés au vector store")
        
        # 3. Initialisation du générateur
        print("\n🤖 Étape 3: Initialisation du générateur RAG")
        generator = RAGGenerator(
            llm_model=settings.llm_model,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens
        )
        
        # 4. Création du pipeline complet
        print("\n🔗 Étape 4: Création du pipeline RAG")
        pipeline = RAGPipeline(retrieval_system, generator)
        
        # 5. Exécution d'une requête
        print("\n💬 Étape 5: Exécution d'une requête")
        question = "Qu'est-ce que Python?"
        
        start_time = time.time()
        result = pipeline.run(question=question)
        latency = time.time() - start_time
        
        print(f"\n❓ Question: {result['question']}")
        print(f"✅ Réponse: {result['answer']}")
        print(f"📚 Sources: {len(result['sources'])} documents")
        print(f"⏱️  Latence: {latency:.2f}s")
        
        # Logging des métriques
        log_rag_metrics(
            question=question,
            answer=result['answer'],
            retrieved_docs_count=len(result['sources']),
            answer_length=len(result['answer']),
            model=result['model'],
            latency=latency
        )
        
        # 6. Exemple de recherche
        print("\n🔎 Étape 6: Recherche dans le vector store")
        search_results = retrieval_system.similarity_search("LangChain", k=2)
        print(f"✅ {len(search_results)} résultats trouvés")
        for i, doc in enumerate(search_results, 1):
            print(f"  {i}. {doc.page_content[:100]}...")
        
        print("\n✨ Exemple terminé avec succès!")


if __name__ == "__main__":
    # Vérifier que les clés API sont configurées
    if not settings.openai_api_key:
        print("⚠️  Attention: OPENAI_API_KEY n'est pas configurée")
        print("   Configurez-la dans le fichier .env ou comme variable d'environnement")
        sys.exit(1)
    
    main()




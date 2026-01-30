"""Interface web Streamlit pour le système RAG"""

import streamlit as st
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.pipeline import RAGPipeline
from src.rag.retrieval import RetrievalSystem
from src.rag.generation import RAGGenerator
from src.config import settings

# Configuration de la page
st.set_page_config(
    page_title="Système RAG",
    page_icon="🤖",
    layout="wide"
)

# Initialiser le système RAG
@st.cache_resource
def init_rag_system():
    """Initialiser le système RAG (mis en cache)"""
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
    return pipeline

# Titre
st.title("🤖 Système RAG - Interface de Questions")
st.markdown("---")

# Initialiser le système
try:
    pipeline = init_rag_system()
    st.success("✅ Système RAG initialisé avec succès!")
except Exception as e:
    st.error(f"❌ Erreur lors de l'initialisation: {e}")
    st.stop()

# Initialiser l'historique de chat dans la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher l'historique de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie de question
if question := st.chat_input("Posez votre question sur vos documents..."):
    # Ajouter la question de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    
    # Afficher un indicateur de chargement
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            try:
                # Préparer l'historique pour l'API
                chat_history = [
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages[:-1]  # Exclure la question actuelle
                ]
                
                # Obtenir la réponse
                result = pipeline.run(question=question, chat_history=chat_history)
                
                # Afficher la réponse
                st.markdown(result["answer"])
                
                # Afficher les sources
                if result.get("sources"):
                    with st.expander(f"📚 Sources ({len(result['sources'])} documents)"):
                        for i, source in enumerate(result["sources"][:5], 1):
                            st.markdown(f"**Source {i}:**")
                            content = source.get("content", "")
                            if isinstance(content, str):
                                st.text(content[:300] + "..." if len(content) > 300 else content)
                            else:
                                st.text(str(content)[:300] + "...")
                
                # Ajouter la réponse à l'historique
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"]
                })
                
            except Exception as e:
                error_msg = f"❌ Erreur: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })

# Sidebar avec informations
with st.sidebar:
    st.header("ℹ️ Informations")
    st.markdown(f"**Modèle:** {settings.llm_model}")
    st.markdown(f"**Embedding:** {settings.embedding_model}")
    st.markdown(f"**Top K:** {settings.top_k}")
    
    st.markdown("---")
    
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📖 Comment utiliser")
    st.markdown("""
    1. Posez une question dans la zone de texte
    2. Attendez la réponse du système
    3. Consultez les sources utilisées
    4. Continuez la conversation
    """)


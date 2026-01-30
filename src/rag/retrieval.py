"""Retrieval system for vector search"""

from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
try:
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain.retrievers.document_compressors import LLMChainExtractor
    COMPRESSION_AVAILABLE = True
except ImportError:
    COMPRESSION_AVAILABLE = False
    ContextualCompressionRetriever = None
    LLMChainExtractor = None
from langchain_openai import ChatOpenAI
from src.config import settings

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    class MockMLflow:
        @staticmethod
        def log_param(*args, **kwargs): pass
        @staticmethod
        def log_metric(*args, **kwargs): pass
    mlflow = MockMLflow()


class RetrievalSystem:
    """Vector-based retrieval system"""
    
    def __init__(
        self,
        embedding_model: Optional[str] = None,
        vector_store: Optional[Chroma] = None,
        top_k: int = 5,
        use_compression: bool = False
    ):
        self.embedding_model_name = embedding_model or settings.embedding_model
        self.top_k = top_k
        self.use_compression = use_compression
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=self.embedding_model_name,
            openai_api_key=settings.openai_api_key
        )
        
        # Initialize or use existing vector store
        if vector_store is None:
            self.vector_store = Chroma(
                persist_directory=settings.chroma_persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.vector_store = vector_store
        
        # Setup retriever
        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.top_k}
        )
        
        # Optional compression retriever
        if use_compression and COMPRESSION_AVAILABLE:
            llm = ChatOpenAI(
                model=settings.llm_model,
                temperature=0,
                openai_api_key=settings.openai_api_key
            )
            compressor = LLMChainExtractor.from_llm(llm)
            self.retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=self.retriever
            )
        elif use_compression and not COMPRESSION_AVAILABLE:
            print("Warning: Compression retriever not available, using standard retriever")
    
    def add_documents(self, documents: List[Document]) -> List[str]:
        """Add documents to the vector store"""
        ids = self.vector_store.add_documents(documents)
        
        mlflow.log_metric("documents_added", len(ids))
        return ids
    
    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """Perform similarity search"""
        k = k or self.top_k
        
        # Utiliser invoke pour les nouvelles versions de LangChain
        try:
            results = self.retriever.invoke(query)
        except AttributeError:
            # Fallback pour les anciennes versions
            results = self.retriever.get_relevant_documents(query)
        
        # Log to MLflow (si disponible)
        if MLFLOW_AVAILABLE:
            mlflow.log_param("search_query", query)
            mlflow.log_metric("results_count", len(results))
        
        return results
    
    def similarity_search_with_score(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[tuple[Document, float]]:
        """Perform similarity search with scores"""
        k = k or self.top_k
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        
        mlflow.log_param("search_query", query)
        mlflow.log_metric("results_count", len(results))
        
        return results
    
    def get_retriever(self):
        """Get the retriever instance"""
        return self.retriever


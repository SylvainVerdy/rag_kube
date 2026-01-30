"""Document ingestion and processing"""

import os
from typing import List, Optional
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    # Mock mlflow pour éviter les erreurs
    class MockMLflow:
        @staticmethod
        def log_param(*args, **kwargs): pass
        @staticmethod
        def log_metric(*args, **kwargs): pass
    mlflow = MockMLflow()


class DocumentIngester:
    """Handle document ingestion and chunking"""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        chunking_strategy: str = "recursive"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        if chunking_strategy == "recursive":
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
            )
        else:
            raise ValueError(f"Unknown chunking strategy: {chunking_strategy}")
    
    def load_document(self, file_path: str) -> List[Document]:
        """Load a document from file path"""
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        loader_map = {
            ".pdf": PyPDFLoader,
            ".docx": Docx2txtLoader,
            ".txt": TextLoader,
        }
        
        if suffix not in loader_map:
            raise ValueError(f"Unsupported file type: {suffix}")
        
        loader = loader_map[suffix](str(path))
        documents = loader.load()
        
        # Log to MLflow (si disponible)
        if MLFLOW_AVAILABLE:
            mlflow.log_param("document_path", str(path))
            mlflow.log_param("document_type", suffix)
            mlflow.log_metric("document_chunks", len(documents))
        
        return documents
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """Load all supported documents from a directory"""
        directory = Path(directory_path)
        all_documents = []
        
        supported_extensions = {".pdf", ".docx", ".txt"}
        
        for file_path in directory.rglob("*"):
            if file_path.suffix.lower() in supported_extensions:
                try:
                    docs = self.load_document(str(file_path))
                    all_documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
                    continue
        
        if MLFLOW_AVAILABLE:
            mlflow.log_metric("total_documents", len(all_documents))
        return all_documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        
        if MLFLOW_AVAILABLE:
            mlflow.log_metric("total_chunks", len(chunks))
            mlflow.log_metric("avg_chunk_size", sum(len(chunk.page_content) for chunk in chunks) / len(chunks) if chunks else 0)
        
        return chunks
    
    def ingest(self, source: str, is_directory: bool = False) -> List[Document]:
        """Main ingestion method"""
        if is_directory:
            documents = self.load_directory(source)
        else:
            documents = self.load_document(source)
        
        chunks = self.chunk_documents(documents)
        return chunks




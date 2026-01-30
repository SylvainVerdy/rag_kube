"""Tests for RAG components"""

import pytest
from unittest.mock import Mock, patch
from langchain.schema import Document

from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import RetrievalSystem
from src.rag.generation import RAGGenerator


@pytest.fixture
def sample_documents():
    """Sample documents for testing"""
    return [
        Document(
            page_content="This is a test document about Python programming.",
            metadata={"source": "test1.txt", "page": 1}
        ),
        Document(
            page_content="Another document about machine learning and AI.",
            metadata={"source": "test2.txt", "page": 1}
        ),
    ]


def test_document_ingester_chunking(sample_documents):
    """Test document chunking"""
    ingester = DocumentIngester(chunk_size=50, chunk_overlap=10)
    chunks = ingester.chunk_documents(sample_documents)
    
    assert len(chunks) > 0
    assert all(isinstance(chunk, Document) for chunk in chunks)


@patch('src.rag.retrieval.OpenAIEmbeddings')
@patch('src.rag.retrieval.Chroma')
def test_retrieval_system_initialization(mock_chroma, mock_embeddings):
    """Test retrieval system initialization"""
    retrieval = RetrievalSystem()
    assert retrieval is not None
    assert retrieval.top_k > 0


@patch('src.rag.generation.ChatOpenAI')
def test_rag_generator_initialization(mock_llm):
    """Test RAG generator initialization"""
    generator = RAGGenerator()
    assert generator is not None
    assert generator.llm_model is not None


def test_rag_generator_prompt_template():
    """Test that prompt template is properly configured"""
    generator = RAGGenerator()
    assert generator.prompt_template is not None


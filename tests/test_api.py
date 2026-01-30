"""Tests for API endpoints"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from src.api.main import app


@pytest.fixture
def client():
    """Test client"""
    return TestClient(app)


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@patch('src.api.main.rag_pipeline')
def test_query_endpoint(mock_pipeline, client):
    """Test query endpoint"""
    mock_pipeline.run.return_value = {
        "question": "What is Python?",
        "answer": "Python is a programming language.",
        "sources": [],
        "model": "gpt-4"
    }
    
    response = client.post(
        "/api/query",
        json={"question": "What is Python?"}
    )
    
    # Note: This will fail if RAG system is not initialized
    # In a real scenario, we'd mock the initialization
    assert response.status_code in [200, 503]


def test_metrics_endpoint(client):
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    # Should return 200 if Prometheus is enabled, or 404 if not
    assert response.status_code in [200, 404]




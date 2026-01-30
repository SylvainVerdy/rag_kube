"""Prometheus metrics setup"""

from prometheus_client import Counter, Histogram, Gauge
from typing import Optional
from src.config import settings

# Metrics
query_counter = Counter(
    'rag_queries_total',
    'Total number of RAG queries',
    ['status']
)

query_duration = Histogram(
    'rag_query_duration_seconds',
    'Duration of RAG queries in seconds',
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

retrieval_docs_count = Histogram(
    'rag_retrieval_docs_count',
    'Number of documents retrieved',
    buckets=[1, 3, 5, 10, 20, 50]
)

answer_length = Histogram(
    'rag_answer_length',
    'Length of generated answers',
    buckets=[100, 500, 1000, 2000, 5000]
)

active_queries = Gauge(
    'rag_active_queries',
    'Number of active queries'
)

vector_store_size = Gauge(
    'rag_vector_store_size',
    'Number of documents in vector store'
)


def setup_prometheus_metrics():
    """Setup Prometheus metrics"""
    if not settings.enable_prometheus:
        return
    
    print("Prometheus metrics enabled")


def record_query(status: str = "success"):
    """Record a query metric"""
    query_counter.labels(status=status).inc()


def record_query_duration(duration: float):
    """Record query duration"""
    query_duration.observe(duration)


def record_retrieval_docs(count: int):
    """Record number of retrieved documents"""
    retrieval_docs_count.observe(count)


def record_answer_length(length: int):
    """Record answer length"""
    answer_length.observe(length)


def set_active_queries(count: int):
    """Set active queries count"""
    active_queries.set(count)


def set_vector_store_size(size: int):
    """Set vector store size"""
    vector_store_size.set(size)




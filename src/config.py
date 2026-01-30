"""Configuration management using Pydantic Settings"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Model Configuration
    embedding_model: str = "text-embedding-3-small"
    llm_model: str = "gpt-4-turbo-preview"
    temperature: float = 0.7
    max_tokens: int = 1000
    
    # Vector Store Configuration
    vector_store_type: str = "chroma"
    chroma_persist_directory: str = "./chroma_db"
    
    # Retrieval Configuration
    top_k: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # Langfuse Configuration
    langfuse_secret_key: Optional[str] = None
    langfuse_public_key: Optional[str] = None
    langfuse_host: str = "http://localhost:3000"  # Par défaut: instance locale
    enable_langfuse: bool = True
    
    # MLflow Configuration
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "rag_experiments"
    
    # Monitoring
    enable_prometheus: bool = True
    enable_evidently: bool = True
    
    # Kubernetes
    namespace: str = "rag-system"
    replicas: int = 2
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignorer les variables supplémentaires dans .env


settings = Settings()




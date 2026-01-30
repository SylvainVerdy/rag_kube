"""MLflow utilities for experiment tracking"""

import mlflow
from mlflow.tracking import MlflowClient
from typing import Dict, Optional
from src.config import settings


def init_mlflow():
    """Initialize MLflow tracking"""
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)


def start_run(run_name: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
    """Start a new MLflow run"""
    init_mlflow()
    return mlflow.start_run(run_name=run_name, tags=tags)


def log_rag_metrics(
    question: str,
    answer: str,
    retrieved_docs_count: int,
    answer_length: int,
    model: str,
    latency: float
):
    """Log RAG-specific metrics to MLflow"""
    mlflow.log_param("question", question)
    mlflow.log_param("model", model)
    mlflow.log_metric("retrieved_docs_count", retrieved_docs_count)
    mlflow.log_metric("answer_length", answer_length)
    mlflow.log_metric("latency_seconds", latency)
    
    # Log answer as artifact
    mlflow.log_text(answer, "answer.txt")


def log_model_performance(metrics: Dict[str, float]):
    """Log model performance metrics"""
    for metric_name, value in metrics.items():
        mlflow.log_metric(metric_name, value)


def register_model(model_name: str, model_path: str, metadata: Optional[Dict] = None):
    """Register a model in MLflow Model Registry"""
    client = MlflowClient()
    
    result = mlflow.register_model(
        model_path,
        model_name,
        tags=metadata
    )
    
    return result


def get_latest_model_version(model_name: str, stage: str = "Production"):
    """Get the latest model version for a given stage"""
    client = MlflowClient()
    
    latest_versions = client.get_latest_versions(
        model_name,
        stages=[stage]
    )
    
    if latest_versions:
        return latest_versions[0]
    return None




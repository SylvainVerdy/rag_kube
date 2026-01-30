"""Utilities Module"""

# Try to import MLflow utils, but don't fail if MLflow is not available
try:
    from .mlflow_utils import (
        init_mlflow,
        start_run,
        log_rag_metrics,
        log_model_performance,
        register_model,
        get_latest_model_version
    )
    __all__ = [
        "init_mlflow",
        "start_run",
        "log_rag_metrics",
        "log_model_performance",
        "register_model",
        "get_latest_model_version",
    ]
except ImportError:
    # MLflow not available, only export REST client
    __all__ = []

# Always export REST client
from .mlflow_rest import MLflowRESTClient, get_mlflow_client
__all__.extend(["MLflowRESTClient", "get_mlflow_client"])




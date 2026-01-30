"""MLflow REST API client - Alternative to Python SDK when imports fail"""

import requests
import json
from typing import Dict, Optional, Any

try:
    from src.config import settings
except ImportError:
    from config import settings


class MLflowRESTClient:
    """Simple MLflow REST API client"""
    
    def __init__(self, tracking_uri: Optional[str] = None):
        self.tracking_uri = tracking_uri or settings.mlflow_tracking_uri
        # Remove trailing slash
        if self.tracking_uri.endswith('/'):
            self.tracking_uri = self.tracking_uri[:-1]
        self.experiment_name = settings.mlflow_experiment_name
        self.experiment_id = None
        self.current_run_id = None
        self._ensure_experiment()
    
    def _ensure_experiment(self):
        """Ensure experiment exists, create if not"""
        try:
            # Try to get experiment
            response = requests.get(
                f"{self.tracking_uri}/api/2.0/mlflow/experiments/get-by-name",
                params={"experiment_name": self.experiment_name},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if "experiment" in data:
                    self.experiment_id = data["experiment"]["experiment_id"]
                else:
                    raise Exception("Experiment data not found in response")
            else:
                # Create experiment
                response = requests.post(
                    f"{self.tracking_uri}/api/2.0/mlflow/experiments/create",
                    json={"name": self.experiment_name},
                    timeout=5
                )
                if response.status_code == 200:
                    data = response.json()
                    if "experiment_id" in data:
                        self.experiment_id = data["experiment_id"]
                    elif "experiment" in data and "experiment_id" in data["experiment"]:
                        self.experiment_id = data["experiment"]["experiment_id"]
                    else:
                        raise Exception("Experiment ID not found in response")
                else:
                    raise Exception(f"Failed to create experiment: {response.text}")
        except Exception as e:
            print(f"⚠️  Warning: Could not ensure MLflow experiment: {e}")
            # Try to use default experiment (ID 0)
            self.experiment_id = "0"
    
    def start_run(self, run_name: Optional[str] = None, tags: Optional[Dict[str, str]] = None) -> str:
        """Start a new MLflow run"""
        try:
            tags = tags or {}
            tags["mlflow.runName"] = run_name or "unnamed_run"
            
            response = requests.post(
                f"{self.tracking_uri}/api/2.0/mlflow/runs/create",
                json={
                    "experiment_id": self.experiment_id,
                    "start_time": int(__import__("time").time() * 1000),
                    "tags": [{"key": k, "value": v} for k, v in tags.items()]
                },
                timeout=5
            )
            
            if response.status_code == 200:
                self.current_run_id = response.json()["run"]["info"]["run_id"]
                return self.current_run_id
            else:
                raise Exception(f"Failed to create run: {response.text}")
        except Exception as e:
            print(f"⚠️  Warning: Could not start MLflow run: {e}")
            return None
    
    def log_param(self, key: str, value: Any):
        """Log a parameter"""
        if not self.current_run_id:
            return
        
        try:
            requests.post(
                f"{self.tracking_uri}/api/2.0/mlflow/runs/log-parameter",
                json={
                    "run_id": self.current_run_id,
                    "key": key,
                    "value": str(value)
                },
                timeout=5
            )
        except Exception as e:
            print(f"⚠️  Warning: Could not log parameter {key}: {e}")
    
    def log_metric(self, key: str, value: float, timestamp: Optional[int] = None):
        """Log a metric"""
        if not self.current_run_id:
            return
        
        try:
            if timestamp is None:
                timestamp = int(__import__("time").time() * 1000)
            
            requests.post(
                f"{self.tracking_uri}/api/2.0/mlflow/runs/log-metric",
                json={
                    "run_id": self.current_run_id,
                    "key": key,
                    "value": float(value),
                    "timestamp": timestamp
                },
                timeout=5
            )
        except Exception as e:
            print(f"⚠️  Warning: Could not log metric {key}: {e}")
    
    def end_run(self, status: str = "FINISHED"):
        """End the current run"""
        if not self.current_run_id:
            return
        
        try:
            requests.post(
                f"{self.tracking_uri}/api/2.0/mlflow/runs/update",
                json={
                    "run_id": self.current_run_id,
                    "status": status
                },
                timeout=5
            )
            self.current_run_id = None
        except Exception as e:
            print(f"⚠️  Warning: Could not end MLflow run: {e}")


# Global instance
_mlflow_client: Optional[MLflowRESTClient] = None


def get_mlflow_client() -> Optional[MLflowRESTClient]:
    """Get or create MLflow REST client"""
    global _mlflow_client
    if _mlflow_client is None:
        try:
            _mlflow_client = MLflowRESTClient()
        except Exception as e:
            print(f"⚠️  Warning: Could not initialize MLflow REST client: {e}")
            return None
    return _mlflow_client


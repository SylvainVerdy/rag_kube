"""Test MLflow REST API client"""

import sys
import os

# Add src to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)

from utils.mlflow_rest import MLflowRESTClient
from config import settings

print("🔍 Test du client MLflow REST")
print("=" * 50)
print(f"📊 Tracking URI: {settings.mlflow_tracking_uri}")
print(f"📁 Experiment: {settings.mlflow_experiment_name}")
print()

try:
    client = MLflowRESTClient()
    
    print(f"✅ Client MLflow REST initialisé")
    print(f"   Experiment ID: {client.experiment_id}")
    print()
    
    # Créer un run de test
    run_id = client.start_run(
        run_name="test_rest_client",
        tags={"test": "true", "method": "rest_api"}
    )
    
    if run_id:
        print(f"✅ Run créé: {run_id}")
        
        # Logger des paramètres et métriques
        client.log_param("test_param", "test_value")
        client.log_metric("test_metric", 42.0)
        client.log_metric("another_metric", 3.14)
        
        print("✅ Paramètres et métriques loggés")
        
        # Terminer le run
        client.end_run(status="FINISHED")
        print("✅ Run terminé")
        print()
        print("🌐 Ouvrez http://localhost:5000 pour voir le run dans l'interface MLflow")
    else:
        print("❌ Échec de création du run")
        
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()


"""Script pour tester la connexion MLflow"""

import sys
import os
sys.path.insert(0, 'src')

from config import settings

print("🔍 Test de connexion MLflow")
print("=" * 50)

print(f"📊 Tracking URI: {settings.mlflow_tracking_uri}")
print(f"📁 Experiment: {settings.mlflow_experiment_name}")
print()

try:
    import mlflow
    from mlflow.tracking import MlflowClient
    
    # Initialiser MLflow
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)
    
    # Tester la connexion
    client = MlflowClient(settings.mlflow_tracking_uri)
    
    # Créer un run de test
    with mlflow.start_run(run_name="test_connection") as run:
        mlflow.log_param("test_param", "test_value")
        mlflow.log_metric("test_metric", 1.0)
        run_id = run.info.run_id
    
    print(f"✅ MLflow connecté avec succès!")
    print(f"   Run ID: {run_id}")
    print(f"   Experiment ID: {mlflow.get_experiment_by_name(settings.mlflow_experiment_name).experiment_id}")
    print()
    print("🌐 Ouvrez http://localhost:5000 pour voir le run dans l'interface MLflow")
    
except Exception as e:
    print(f"❌ Erreur de connexion MLflow: {e}")
    print()
    print("💡 Vérifiez que MLflow est démarré:")
    print("   - Option 1: docker-compose up mlflow -d")
    print("   - Option 2: .\\scripts\\start_mlflow_simple.ps1")
    import traceback
    traceback.print_exc()


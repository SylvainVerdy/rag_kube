#!/bin/bash

# Script pour démarrer MLflow localement

echo "🚀 Démarrage de MLflow..."

# Créer le répertoire mlflow s'il n'existe pas
mkdir -p mlflow

# Démarrer MLflow
mlflow server \
    --backend-store-uri file:///$(pwd)/mlflow \
    --default-artifact-root ./mlflow/artifacts \
    --host 0.0.0.0 \
    --port 5000


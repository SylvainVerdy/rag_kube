# Script PowerShell pour démarrer MLflow localement

Write-Host "🚀 Démarrage de MLflow..." -ForegroundColor Green

# Créer le répertoire mlflow s'il n'existe pas
if (-not (Test-Path mlflow)) {
    New-Item -ItemType Directory -Path mlflow | Out-Null
}

# Démarrer MLflow
Write-Host "📊 MLflow sera accessible sur: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📁 Données stockées dans: ./mlflow" -ForegroundColor Cyan
Write-Host ""

mlflow server `
    --backend-store-uri "file:///$PWD/mlflow" `
    --default-artifact-root "./mlflow/artifacts" `
    --host 0.0.0.0 `
    --port 5000


# Script simple pour démarrer MLflow

Write-Host "🚀 Démarrage de MLflow..." -ForegroundColor Green
Write-Host ""

# Activer le venv
& .\venv\Scripts\Activate.ps1

# Créer le répertoire mlflow
if (-not (Test-Path mlflow)) {
    New-Item -ItemType Directory -Path mlflow | Out-Null
}

Write-Host "📊 MLflow sera accessible sur: http://localhost:5000" -ForegroundColor Cyan
Write-Host "📁 Données stockées dans: ./mlflow" -ForegroundColor Cyan
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter MLflow" -ForegroundColor Yellow
Write-Host ""

# Démarrer MLflow
$mlflowPath = ".\venv\Scripts\mlflow.exe"
if (Test-Path $mlflowPath) {
    & $mlflowPath server `
        --backend-store-uri "file:///$PWD/mlflow" `
        --default-artifact-root "./mlflow/artifacts" `
        --host 0.0.0.0 `
        --port 5000
} else {
    Write-Host "❌ MLflow n'est pas installé. Installation..." -ForegroundColor Red
    pip install mlflow
    mlflow server `
        --backend-store-uri "file:///$PWD/mlflow" `
        --default-artifact-root "./mlflow/artifacts" `
        --host 0.0.0.0 `
        --port 5000
}


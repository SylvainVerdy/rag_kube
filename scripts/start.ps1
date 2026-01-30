# Script PowerShell de démarrage pour le système RAG

Write-Host "🚀 Démarrage du système RAG..." -ForegroundColor Green

# Vérifier que Python est installé
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python n'est pas installé" -ForegroundColor Red
    exit 1
}

# Vérifier que les variables d'environnement sont configurées
if (-not (Test-Path .env)) {
    Write-Host "⚠️  Fichier .env non trouvé" -ForegroundColor Yellow
    Write-Host "📝 Création du fichier .env depuis .env.example..." -ForegroundColor Cyan
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
        Write-Host "✅ Fichier .env créé. Veuillez le configurer avec vos clés API." -ForegroundColor Green
    } else {
        Write-Host "❌ Fichier .env.example non trouvé" -ForegroundColor Red
        exit 1
    }
}

# Créer un environnement virtuel s'il n'existe pas
if (-not (Test-Path venv)) {
    Write-Host "📦 Création de l'environnement virtuel..." -ForegroundColor Cyan
    python -m venv venv
}

# Activer l'environnement virtuel
Write-Host "🔌 Activation de l'environnement virtuel..." -ForegroundColor Cyan
& .\venv\Scripts\Activate.ps1

# Installer les dépendances
Write-Host "📥 Installation des dépendances..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt

# Créer les répertoires nécessaires
Write-Host "📁 Création des répertoires..." -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path chroma_db, data, logs, mlflow | Out-Null

# Lancer l'API
Write-Host "🌟 Lancement de l'API..." -ForegroundColor Green
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload




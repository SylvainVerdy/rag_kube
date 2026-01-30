#!/bin/bash

# Script de démarrage pour le système RAG

set -e

echo "🚀 Démarrage du système RAG..."

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier que les variables d'environnement sont configurées
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé"
    echo "📝 Création du fichier .env depuis .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Fichier .env créé. Veuillez le configurer avec vos clés API."
    else
        echo "❌ Fichier .env.example non trouvé"
        exit 1
    fi
fi

# Créer un environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔌 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Créer les répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p chroma_db data logs mlflow

# Lancer l'API
echo "🌟 Lancement de l'API..."
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload




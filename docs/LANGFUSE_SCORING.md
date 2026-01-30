# Langfuse Scoring pour le Système RAG

## 📊 Vue d'ensemble

Le système RAG intègre Langfuse pour évaluer et scorer les réponses générées. Cela permet de :
- **Tracker la qualité** des réponses RAG
- **Comparer les performances** entre différentes requêtes
- **Identifier les améliorations** nécessaires

## 🚀 Utilisation

### Méthode 1 : Via l'API REST

#### Créer un score simple

```python
import requests

response = requests.post(
    "http://localhost:8001/api/langfuse/score",
    json={
        "trace_id": "trace_123",  # Optionnel
        "name": "relevance",
        "value": 0.85,
        "comment": "La réponse est pertinente",
        "metadata": {
            "question": "Qu'est-ce que le RAG?",
            "source": "manual_evaluation"
        }
    }
)

print(response.json())
```

#### Scorer une réponse RAG complète

```python
response = requests.post(
    "http://localhost:8001/api/langfuse/score/rag",
    json={
        "trace_id": "trace_123",  # Optionnel
        "answer": "Le RAG est une technique...",
        "question": "Qu'est-ce que le RAG?",
        "sources_count": 3,
        "answer_length": 150,
        "relevance_score": 0.9,      # Optionnel (calculé automatiquement si absent)
        "completeness_score": 0.8,   # Optionnel
        "accuracy_score": 0.95       # Optionnel
    }
)

print(response.json())
```

### Méthode 2 : Via le script Python

```powershell
.\venv\Scripts\python.exe scripts/create_langfuse_score.py
```

### Méthode 3 : Directement dans le code

```python
from src.utils.langfuse_scoring import create_score, score_rag_response

# Score simple
score_id = create_score(
    trace_id="trace_123",
    name="relevance",
    value=0.85,
    comment="Bonne pertinence",
    metadata={"source": "manual"}
)

# Scoring RAG complet
scores = score_rag_response(
    trace_id="trace_123",
    answer="Réponse générée...",
    question="Question posée?",
    sources_count=3,
    answer_length=150,
    relevance_score=0.9,
    completeness_score=0.8
)
```

## 📈 Types de Scores

### Scores automatiques (heuristiques)

Si vous ne fournissez pas de scores manuels, le système calcule automatiquement :

- **Relevance** : Basé sur la longueur de la réponse et le nombre de sources
- **Completeness** : Basé sur la longueur de la réponse

### Scores manuels

Vous pouvez fournir vos propres scores :

- **relevance_score** : Pertinence de la réponse (0.0-1.0)
- **completeness_score** : Complétude de la réponse (0.0-1.0)
- **accuracy_score** : Précision de la réponse (0.0-1.0)

## 🔍 Visualisation dans Langfuse

1. **Ouvrez Langfuse** : http://localhost:3000
2. **Allez dans "Scores"** ou **"Traces"**
3. **Filtrez par nom de score** : relevance, completeness, accuracy
4. **Analysez les tendances** : Graphiques et statistiques

## 📝 Exemple Complet

```python
import requests

# 1. Poser une question au RAG
query_response = requests.post(
    "http://localhost:8001/api/query",
    json={
        "question": "Qu'est-ce que le RAG?"
    }
)

result = query_response.json()
print(f"Réponse: {result['answer']}")

# 2. Évaluer la réponse (manuellement ou automatiquement)
score_response = requests.post(
    "http://localhost:8001/api/langfuse/score/rag",
    json={
        "answer": result["answer"],
        "question": "Qu'est-ce que le RAG?",
        "sources_count": len(result.get("sources", [])),
        "answer_length": len(result["answer"]),
        "relevance_score": 0.9,  # Votre évaluation
        "completeness_score": 0.85
    }
)

print(f"Scores créés: {score_response.json()}")
```

## 🎯 Bonnes Pratiques

1. **Tracez les trace_id** : Pour lier les scores aux traces, passez le `trace_id` de Langfuse
2. **Scores cohérents** : Utilisez la même échelle (0.0-1.0) pour tous les scores
3. **Métadonnées** : Ajoutez des métadonnées utiles (question, modèle utilisé, etc.)
4. **Commentaires** : Ajoutez des commentaires pour expliquer vos scores

## 🔧 Configuration

Assurez-vous que votre `.env` contient :

```env
LANGFUSE_SECRET_KEY=votre_secret_key
LANGFUSE_PUBLIC_KEY=votre_public_key
LANGFUSE_HOST=http://localhost:3000
ENABLE_LANGFUSE=true
```

## 🐛 Dépannage

### "Failed to create score"

- Vérifiez que Langfuse est démarré
- Vérifiez les clés API dans `.env`
- Vérifiez que `ENABLE_LANGFUSE=true`

### Scores n'apparaissent pas dans Langfuse

- Rafraîchissez la page
- Vérifiez l'onglet "Scores" dans Langfuse
- Vérifiez les logs de l'API pour des erreurs


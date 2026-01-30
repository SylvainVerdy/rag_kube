# Système d'Évaluation RAG

## 📊 Vue d'ensemble

Le système RAG intègre un système complet d'évaluation qui combine :
1. **Évaluation automatique** : Scores calculés automatiquement (pertinence, complétude)
2. **Évaluation manuelle** : Notation par l'utilisateur depuis l'interface web
3. **Intégration Langfuse** : Tous les scores sont enregistrés dans Langfuse avec le trace_id

## 🔄 Flux d'Évaluation

### 1. Génération de la Réponse

Lorsqu'une question est posée :
1. Le système RAG génère une réponse
2. Langfuse crée automatiquement une trace avec un `trace_id`
3. Le `trace_id` est retourné dans la réponse API
4. Des scores automatiques sont calculés et affichés

### 2. Affichage dans l'Interface

L'interface web affiche :
- **Scores automatiques** : Pertinence et Complétude avec barres de progression
- **Boutons de notation** : 👍 Bonne réponse, 👎 À améliorer, ⭐ Noter (0-5)
- **Zone de commentaire** : Pour ajouter des notes supplémentaires

### 3. Enregistrement dans Langfuse

Quand l'utilisateur note la réponse :
1. Le score est envoyé à l'API avec le `trace_id`
2. Un score `user_rating` est créé dans Langfuse
3. Les scores de pertinence et complétude sont également enregistrés
4. Le commentaire est inclus dans les métadonnées

## 📝 Types de Scores

### Scores Automatiques

- **relevance** : Calculé basé sur la longueur de la réponse et le nombre de sources
- **completeness** : Calculé basé sur la longueur de la réponse

### Scores Manuels (User Rating)

- **user_rating** : Score principal donné par l'utilisateur (0.0 - 1.0)
- **relevance** : Score de pertinence (si fourni)
- **completeness** : Score de complétude (si fourni)

## 🔗 Liaison avec les Traces Langfuse

Chaque score est lié à la trace Langfuse correspondante via le `trace_id` :

```python
# Exemple de création de score
langfuse.create_score(
    trace_id="trace_123",  # ID de la trace
    name="user_rating",
    value=0.85,
    comment="Bonne réponse, très pertinente",
    metadata={
        "rating_type": "thumbs_up",
        "question": "Qu'est-ce que le RAG?",
        "evaluation_type": "manual"
    }
)
```

## 📊 Visualisation dans Langfuse

1. **Ouvrez Langfuse** : http://localhost:3000
2. **Allez dans "Traces"** : Vous verrez toutes les traces avec leurs scores
3. **Filtrez par score** : Cliquez sur un score pour voir toutes les traces avec ce score
4. **Analysez les tendances** : Graphiques et statistiques disponibles

## 🎯 Utilisation

### Depuis l'Interface Web

1. Posez une question
2. Consultez les scores automatiques affichés
3. Cliquez sur 👍, 👎, ou ⭐ pour noter
4. Ajoutez un commentaire (optionnel)
5. Cliquez sur "Envoyer l'évaluation"

### Depuis l'API

```python
import requests

# Noter une réponse
response = requests.post(
    "http://localhost:8001/api/langfuse/score/rag",
    json={
        "trace_id": "trace_123",
        "answer": "Réponse générée...",
        "question": "Question posée?",
        "sources_count": 3,
        "answer_length": 150,
        "accuracy_score": 0.9,
        "comment": "Excellente réponse",
        "rating_type": "thumbs_up"
    }
)
```

## 🔧 Configuration

Assurez-vous que votre `.env` contient :

```env
LANGFUSE_SECRET_KEY=votre_secret_key
LANGFUSE_PUBLIC_KEY=votre_public_key
LANGFUSE_HOST=http://localhost:3000
ENABLE_LANGFUSE=true
```

## 📈 Métadonnées Enregistrées

Chaque score contient des métadonnées riches :

```json
{
  "question": "Question posée",
  "answer_preview": "Aperçu de la réponse...",
  "rating_type": "thumbs_up",
  "sources_count": 3,
  "answer_length": 150,
  "evaluation_type": "manual"
}
```

## 🐛 Dépannage

### Les scores n'apparaissent pas dans Langfuse

1. Vérifiez que Langfuse est démarré
2. Vérifiez les clés API dans `.env`
3. Vérifiez les logs de l'API pour des erreurs
4. Vérifiez que le `trace_id` est bien fourni

### Le trace_id est None

- Le CallbackHandler Langfuse devrait créer automatiquement des traces
- Vérifiez que Langfuse est bien configuré
- Vérifiez les logs au démarrage de l'API

### Erreur lors de l'enregistrement

- Vérifiez la console du navigateur pour les erreurs
- Vérifiez les logs de l'API
- Vérifiez que l'endpoint `/api/langfuse/score/rag` est accessible


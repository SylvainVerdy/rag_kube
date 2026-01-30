"""Test simple de création de score Langfuse"""

from langfuse import get_client

langfuse = get_client()

# Test simple
score = langfuse.create_score(
    name="test_score",
    value=0.85,
    data_type="NUMERIC"
)

print(f"✅ Score créé: {score.id if hasattr(score, 'id') else score}")


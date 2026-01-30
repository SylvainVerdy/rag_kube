"""Langfuse scoring utilities for RAG evaluation"""

from typing import Optional, Dict, Any

try:
    from src.config import settings
except ImportError:
    from config import settings

try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFuse = None
    LANGFUSE_AVAILABLE = False


def get_langfuse_client() -> Optional[Any]:
    """Get Langfuse client instance"""
    if not LANGFUSE_AVAILABLE:
        return None
    
    if not settings.enable_langfuse:
        return None
    
    if not settings.langfuse_secret_key or not settings.langfuse_public_key:
        return None
    
    try:
        return Langfuse(
            secret_key=settings.langfuse_secret_key,
            public_key=settings.langfuse_public_key,
            host=settings.langfuse_host
        )
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize Langfuse client: {e}")
        return None


def create_score(
    trace_id: Optional[str] = None,
    name: str = "rag_quality",
    value: float = 0.0,
    comment: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    use_current_trace: bool = False
) -> Optional[str]:
    """
    Create a score in Langfuse
    
    Args:
        trace_id: ID of the trace to score (optional but recommended)
        name: Name of the score (e.g., "accuracy", "relevance", "completeness")
        value: Score value (typically 0.0 to 1.0)
        comment: Optional comment about the score
        metadata: Optional metadata dictionary
    
    Returns:
        Score ID if successful, None otherwise
    """
    if not LANGFUSE_AVAILABLE:
        print(f"⚠️  Langfuse non disponible")
        return None
    
    # Use the configured client from get_langfuse_client
    client = get_langfuse_client()
    if not client:
        print(f"⚠️  Client Langfuse non disponible")
        return None
    
    # Build comment first (needed for both score_current_trace and create_score)
    final_comment = None
    if comment:
        final_comment = str(comment)[:500]  # Truncate to 500 chars
    
    # Add metadata to comment if provided
    if metadata:
        try:
            import json
            metadata_items = []
            for k, v in list(metadata.items())[:5]:  # Limit to 5 items
                if isinstance(v, (str, int, float, bool)):
                    metadata_items.append(f"{k}:{v}")
                else:
                    metadata_items.append(f"{k}:{str(v)[:50]}")
            
            metadata_str = " | ".join(metadata_items)
            if len(metadata_str) > 200:
                metadata_str = metadata_str[:200] + "..."
            
            if final_comment:
                final_comment = f"{final_comment} | {metadata_str}"
            else:
                final_comment = metadata_str
        except Exception as e:
            print(f"   ⚠️  Metadata non sérialisable: {e}")
    
    # If use_current_trace is True and no trace_id provided, try to use score_current_trace
    if use_current_trace and not trace_id:
        try:
            if hasattr(client, 'score_current_trace'):
                # Use score_current_trace which scores the current trace automatically
                print(f"   📊 Utilisation de score_current_trace (trace courante)")
                try:
                    score_params = {
                        "name": name,
                        "value": float(value)
                    }
                    if final_comment:
                        score_params["comment"] = final_comment
                    
                    result = client.score_current_trace(**score_params)
                    print(f"   ✅ Score créé via score_current_trace")
                    return "created"  # Return success indicator
                except Exception as score_error:
                    print(f"   ⚠️  score_current_trace échoué: {score_error}, fallback sur create_score")
                    import traceback
                    traceback.print_exc()
            # Fallback: try to get trace_id
            if hasattr(client, 'get_current_trace_id'):
                trace_id = client.get_current_trace_id()
                if trace_id:
                    print(f"   🔗 Trace ID récupéré depuis contexte: {trace_id}")
        except Exception as e:
            print(f"   ⚠️  Could not use current trace: {e}")
    
    try:
        
        # Build score parameters
        # According to Langfuse docs, create_score requires: name, value, and optionally trace_id
        score_params = {
            "name": name,
            "value": float(value)
        }
        
        # Add trace_id if provided (important for linking to trace)
        if trace_id:
            score_params["trace_id"] = trace_id
            print(f"   🔗 Score lié à trace_id: {trace_id}")
        else:
            print(f"   ⚠️  Aucun trace_id fourni - score créé sans lien à une trace")
        
        # final_comment is already built above, no need to rebuild
        
        print(f"   📝 Création du score '{name}' avec valeur {value}")
        if trace_id:
            print(f"   🔗 Trace ID: {trace_id}")
        else:
            print(f"   ⚠️  Pas de trace_id - score créé sans lien")
        
        # Create score with minimal parameters to avoid "Bad request" errors
        # Langfuse create_score signature: name, value, trace_id=None, comment=None
        try:
            if trace_id and final_comment:
                score = client.create_score(
                    name=name,
                    value=float(value),
                    trace_id=trace_id,
                    comment=final_comment
                )
            elif trace_id:
                score = client.create_score(
                    name=name,
                    value=float(value),
                    trace_id=trace_id
                )
            elif final_comment:
                score = client.create_score(
                    name=name,
                    value=float(value),
                    comment=final_comment
                )
            else:
                score = client.create_score(
                    name=name,
                    value=float(value)
                )
        except Exception as create_error:
            print(f"   ❌ Erreur lors de l'appel create_score: {create_error}")
            import traceback
            traceback.print_exc()
            # Try with absolute minimal parameters as fallback
            try:
                print(f"   🔄 Tentative avec paramètres minimaux (name + value uniquement)...")
                score = client.create_score(
                    name=str(name),
                    value=float(value)
                )
                print(f"   ✅ Score créé avec paramètres minimaux")
            except Exception as min_error:
                print(f"   ❌ Erreur même avec paramètres minimaux: {min_error}")
                print(f"   💡 Le score peut quand même être créé côté serveur - vérifiez dans Langfuse")
                # Don't raise - return None to indicate we couldn't confirm creation
                return None
        
        # Get score ID - Langfuse may return different types
        # Note: Langfuse create_score may return None but still create the score
        score_id = None
        
        if score is not None:
            if hasattr(score, 'id'):
                score_id = score.id
            elif isinstance(score, str):
                score_id = score
            elif isinstance(score, dict) and 'id' in score:
                score_id = score['id']
            else:
                # Try to get ID from object attributes
                score_id = getattr(score, 'id', None)
        
        if score_id:
            print(f"   ✅ Score '{name}' créé avec ID: {score_id}")
            return score_id
        else:
            # Langfuse create_score may return None but still create the score
            # This is normal behavior - the score is created server-side
            print(f"   ✅ Score '{name}' créé (ID non retourné par l'API mais score créé)")
            print(f"   💡 Vérifiez dans Langfuse - le score devrait être visible")
            # Return a success indicator
            return "created"
    except Exception as e:
        print(f"❌ Erreur lors de la création du score '{name}': {e}")
        print(f"   Paramètres: name={name}, value={value}, trace_id={trace_id}")
        import traceback
        traceback.print_exc()
        return None


def score_rag_response(
    trace_id: Optional[str],
    answer: str,
    question: str,
    sources_count: int = 0,
    answer_length: int = 0,
    relevance_score: Optional[float] = None,
    completeness_score: Optional[float] = None,
    accuracy_score: Optional[float] = None
) -> Dict[str, Optional[str]]:
    """
    Create multiple scores for a RAG response
    
    Args:
        trace_id: ID of the trace
        answer: Generated answer
        question: Original question
        sources_count: Number of sources used
        answer_length: Length of the answer
        relevance_score: Relevance score (0.0-1.0)
        completeness_score: Completeness score (0.0-1.0)
        accuracy_score: Accuracy score (0.0-1.0)
    
    Returns:
        Dictionary with score IDs
    """
    scores = {}
    
    # Automatic scores based on heuristics
    if relevance_score is None:
        # Simple heuristic: longer answers with sources are more relevant
        relevance_score = min(1.0, (answer_length / 500) * 0.5 + (sources_count / 5) * 0.5)
    
    if completeness_score is None:
        # Heuristic: answers with more content are more complete
        completeness_score = min(1.0, answer_length / 300)
    
    # Create scores
    if relevance_score is not None:
        scores["relevance"] = create_score(
            trace_id=trace_id,
            name="relevance",
            value=relevance_score,
            comment=f"Relevance of answer to question: {question[:50]}...",
            metadata={
                "question": question,
                "sources_count": sources_count,
                "answer_length": answer_length
            }
        )
    
    if completeness_score is not None:
        scores["completeness"] = create_score(
            trace_id=trace_id,
            name="completeness",
            value=completeness_score,
            comment=f"Completeness of the answer",
            metadata={
                "answer_length": answer_length,
                "sources_count": sources_count
            }
        )
    
    if accuracy_score is not None:
        scores["accuracy"] = create_score(
            trace_id=trace_id,
            name="accuracy",
            value=accuracy_score,
            comment=f"Accuracy of the answer (manual evaluation)",
            metadata={
                "question": question,
                "answer_preview": answer[:200]
            }
        )
    
    return scores


def get_trace_id_from_generation(generation_id: Optional[str]) -> Optional[str]:
    """
    Get trace ID from a generation ID
    
    Note: This is a helper function. In practice, you might need to
    track trace IDs separately or retrieve them from Langfuse.
    """
    # This would need to be implemented based on how you track traces
    # For now, return None - trace IDs should be passed explicitly
    return None


"""FastAPI main application"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import tempfile
from pathlib import Path
from contextlib import asynccontextmanager

from src.config import settings
from src.rag.ingestion import DocumentIngester
from src.rag.retrieval import RetrievalSystem
from src.rag.generation import RAGGenerator
from src.rag.pipeline import RAGPipeline
from src.monitoring.prometheus import setup_prometheus_metrics
from src.monitoring.evidently import setup_evidently_monitoring

# Initialize RAG components
rag_pipeline: Optional[RAGPipeline] = None
document_ingester: Optional[DocumentIngester] = None
retrieval_system: Optional[RetrievalSystem] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    global rag_pipeline, document_ingester, retrieval_system
    
    # Startup
    print("Initializing RAG system...")
    
    # Initialize MLflow if available
    try:
        from src.utils.mlflow_utils import init_mlflow
        init_mlflow()
        print(f"✅ MLflow initialized - Tracking URI: {settings.mlflow_tracking_uri}")
        print(f"   Experiment: {settings.mlflow_experiment_name}")
    except Exception as e:
        print(f"⚠️  Warning: Could not initialize MLflow: {e}")
    
    document_ingester = DocumentIngester(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap
    )
    
    retrieval_system = RetrievalSystem(
        embedding_model=settings.embedding_model,
        top_k=settings.top_k
    )
    
    generator = RAGGenerator(
        llm_model=settings.llm_model,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens
    )
    
    rag_pipeline = RAGPipeline(retrieval_system, generator)
    
    # Setup monitoring
    if settings.enable_prometheus:
        setup_prometheus_metrics()
    
    if settings.enable_evidently:
        setup_evidently_monitoring()
    
    print("RAG system initialized!")
    
    yield
    
    # Shutdown
    print("Shutting down RAG system...")


# Create FastAPI app
app = FastAPI(
    title="RAG System API",
    description="Retrieval-Augmented Generation API with monitoring",
    version="0.1.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir les fichiers statiques
static_dir = Path(__file__).parent.parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# Pydantic models
class QuestionRequest(BaseModel):
    question: str
    chat_history: Optional[List[Dict[str, str]]] = None


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: List[Dict[str, Any]]  # Permet metadata comme dict
    model: str
    trace_id: Optional[str] = None
    auto_scores: Optional[Dict[str, float]] = None


class IngestRequest(BaseModel):
    path: str
    is_directory: bool = False


class IngestResponse(BaseModel):
    message: str
    chunks_count: int


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "rag-system"
    }


# Serve web interface
@app.get("/")
async def web_interface():
    """Serve the web interface"""
    static_dir = Path(__file__).parent.parent.parent / "static"
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Web interface not found. Please ensure static/index.html exists."}


# Serve web interface
@app.get("/")
async def web_interface():
    """Serve the web interface"""
    static_dir = Path(__file__).parent.parent.parent / "static"
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"message": "Web interface not found. Please ensure static/index.html exists."}


# Prometheus metrics endpoint
if settings.enable_prometheus:
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint"""
        return Response(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )


# RAG endpoints
@app.post("/api/query", response_model=QuestionResponse)
async def query(request: QuestionRequest):
    """Query the RAG system"""
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        result = rag_pipeline.run(
            question=request.question,
            chat_history=request.chat_history
        )
        
        # Get trace_id from result (set by RAGGenerator via pipeline)
        trace_id = result.get("trace_id")
        if trace_id:
            print(f"✅ Trace ID récupéré: {trace_id}")
        else:
            print(f"⚠️  Pas de trace_id dans le résultat")
        
        # Automatic evaluation and scoring
        auto_scores = {}
        
        try:
            # Calculate scores for display
            answer_length = len(result["answer"])
            sources_count = len(result.get("sources", []))
            
            # Heuristic scores
            relevance = min(1.0, (answer_length / 500) * 0.5 + (sources_count / 5) * 0.5)
            completeness = min(1.0, answer_length / 300)
            
            auto_scores = {
                "relevance": round(relevance, 2),
                "completeness": round(completeness, 2)
            }
            
            # Create automatic scores in Langfuse if trace_id is available
            if trace_id:
                try:
                    from src.utils.langfuse_scoring import score_rag_response
                    scores = score_rag_response(
                        trace_id=trace_id,
                        answer=result["answer"],
                        question=request.question,
                        sources_count=sources_count,
                        answer_length=answer_length
                    )
                    print(f"✅ Scores automatiques créés pour trace_id: {trace_id}")
                except Exception as score_error:
                    print(f"⚠️  Warning: Could not create automatic scores: {score_error}")
            else:
                print(f"⚠️  Pas de trace_id - scores automatiques non créés dans Langfuse")
                
        except Exception as e:
            print(f"⚠️  Warning: Could not create automatic scores: {e}")
            import traceback
            traceback.print_exc()
        
        # Ensure trace_id is in result
        result["trace_id"] = trace_id
        result["auto_scores"] = auto_scores if auto_scores else None
        
        return QuestionResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query/stream")
async def query_stream(request: QuestionRequest):
    """Stream query results"""
    if rag_pipeline is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    def generate():
        for state in rag_pipeline.stream(
            question=request.question,
            chat_history=request.chat_history
        ):
            yield f"data: {state}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/ingest", response_model=IngestResponse)
async def ingest_documents(request: IngestRequest):
    """Ingest documents into the vector store"""
    if document_ingester is None or retrieval_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        chunks = document_ingester.ingest(
            source=request.path,
            is_directory=request.is_directory
        )
        
        retrieval_system.add_documents(chunks)
        
        return IngestResponse(
            message="Documents ingested successfully",
            chunks_count=len(chunks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ingest/upload")
async def ingest_upload(file: UploadFile = File(...)):
    """Upload and ingest a document"""
    if document_ingester is None or retrieval_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    # MLflow tracking - Try Python SDK first, fallback to REST API
    mlflow_run_id = None
    mlflow_using_rest = False
    
    # Try Python SDK
    try:
        import mlflow
        from src.utils.mlflow_utils import start_run
        mlflow_run = start_run(
            run_name=f"ingest_{file.filename}",
            tags={"type": "ingestion", "filename": file.filename}
        )
        mlflow_run_id = mlflow_run.info.run_id if hasattr(mlflow_run, 'info') else None
        print(f"✅ MLflow run started (Python SDK): {mlflow_run_id}")
    except (ImportError, ModuleNotFoundError):
        # Fallback to REST API
        try:
            from src.utils.mlflow_rest import get_mlflow_client
            client = get_mlflow_client()
            if client:
                mlflow_run_id = client.start_run(
                    run_name=f"ingest_{file.filename}",
                    tags={"type": "ingestion", "filename": file.filename}
                )
                mlflow_using_rest = True
                print(f"✅ MLflow run started (REST API): {mlflow_run_id}")
        except Exception as e:
            print(f"⚠️  Warning: Could not start MLflow run: {e}")
    except Exception as e:
        print(f"⚠️  Warning: Could not start MLflow run: {e}")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        try:
            # Ingest document
            chunks = document_ingester.ingest(tmp_path, is_directory=False)
            retrieval_system.add_documents(chunks)
            
            # Log additional metrics to MLflow
            if mlflow_run_id:
                try:
                    if mlflow_using_rest:
                        from src.utils.mlflow_rest import get_mlflow_client
                        client = get_mlflow_client()
                        if client:
                            client.log_param("filename", file.filename)
                            client.log_param("file_size_bytes", len(content))
                            client.log_metric("chunks_created", len(chunks))
                            avg_chunk_size = sum(len(chunk.page_content) for chunk in chunks) / len(chunks) if chunks else 0
                            client.log_metric("avg_chunk_size", avg_chunk_size)
                    else:
                        import mlflow
                        mlflow.log_param("filename", file.filename)
                        mlflow.log_param("file_size_bytes", len(content))
                        mlflow.log_metric("chunks_created", len(chunks))
                        avg_chunk_size = sum(len(chunk.page_content) for chunk in chunks) / len(chunks) if chunks else 0
                        mlflow.log_metric("avg_chunk_size", avg_chunk_size)
                except Exception as e:
                    print(f"⚠️  Warning: Could not log to MLflow: {e}")
            
            return IngestResponse(
                message=f"File {file.filename} ingested successfully",
                chunks_count=len(chunks)
            )
        finally:
            # Clean up temp file
            os.unlink(tmp_path)
            # End MLflow run
            if mlflow_run_id:
                try:
                    if mlflow_using_rest:
                        from src.utils.mlflow_rest import get_mlflow_client
                        client = get_mlflow_client()
                        if client:
                            client.end_run(status="FINISHED")
                    else:
                        import mlflow
                        mlflow.end_run()
                except Exception as e:
                    print(f"⚠️  Warning: Could not end MLflow run: {e}")
    
    except Exception as e:
        # End MLflow run on error
        if mlflow_run_id:
            try:
                if mlflow_using_rest:
                    from src.utils.mlflow_rest import get_mlflow_client
                    client = get_mlflow_client()
                    if client:
                        client.end_run(status="FAILED")
                else:
                    import mlflow
                    mlflow.end_run(status="FAILED")
            except:
                pass
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/search")
async def search(query: str, k: Optional[int] = None):
    """Search the vector store"""
    if retrieval_system is None:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        results = retrieval_system.similarity_search(query, k=k)
        return {
            "query": query,
            "results": [
                {
                    "content": doc.page_content[:500],
                    "metadata": doc.metadata
                }
                for doc in results
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Langfuse scoring endpoints
class ScoreRequest(BaseModel):
    trace_id: Optional[str] = None
    name: str = "rag_quality"
    value: float = 0.0
    comment: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ScoreResponse(BaseModel):
    success: bool
    score_id: Optional[str] = None
    message: str


@app.post("/api/langfuse/score", response_model=ScoreResponse)
async def create_score_endpoint(request: ScoreRequest):
    """Create a Langfuse score"""
    try:
        from src.utils.langfuse_scoring import create_score
        
        score_id = create_score(
            trace_id=request.trace_id,
            name=request.name,
            value=request.value,
            comment=request.comment,
            metadata=request.metadata
        )
        
        if score_id:
            return ScoreResponse(
                success=True,
                score_id=score_id,
                message="Score created successfully"
            )
        else:
            return ScoreResponse(
                success=False,
                score_id=None,
                message="Failed to create score. Check Langfuse configuration."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class RAGScoreRequest(BaseModel):
    trace_id: Optional[str] = None
    answer: str
    question: str
    sources_count: int = 0
    answer_length: int = 0
    relevance_score: Optional[float] = None
    completeness_score: Optional[float] = None
    accuracy_score: Optional[float] = None
    comment: Optional[str] = None
    rating_type: Optional[str] = None  # "thumbs_up", "thumbs_down", "custom"
    raw_score: Optional[float] = None  # Valeur brute (0-5) pour référence


@app.post("/api/langfuse/score/rag", response_model=Dict[str, Any])
async def score_rag_endpoint(request: RAGScoreRequest):
    """Create multiple scores for a RAG response (manual evaluation from user)"""
    try:
        from src.utils.langfuse_scoring import create_score, get_langfuse_client
        
        client = get_langfuse_client()
        if not client:
            raise HTTPException(status_code=503, detail="Langfuse client not available")
        
        scores_created = {}
        answer_length = request.answer_length or len(request.answer)
        
        # Create user evaluation score (most important - this is the manual rating)
        if request.accuracy_score is not None:
            user_score_comment = request.comment or f"Évaluation manuelle: {request.rating_type or 'custom'}"
            if request.comment:
                user_score_comment = f"{request.comment} (Type: {request.rating_type or 'custom'})"
            
            print(f"📊 Création du score user_rating:")
            print(f"   trace_id reçu: {request.trace_id}")
            print(f"   accuracy_score (normalisé 0-1): {request.accuracy_score}")
            print(f"   raw_score reçu: {request.raw_score}")
            print(f"   comment: {user_score_comment}")
            print(f"   rating_type: {request.rating_type}")
            
            # Include metadata in comment since metadata param may not be supported
            full_comment = f"{user_score_comment}\n"
            if request.raw_score is not None:
                full_comment += f"Note brute: {request.raw_score}/5\n"
            full_comment += f"Question: {request.question[:100]}\n"
            full_comment += f"Rating Type: {request.rating_type or 'custom'}\n"
            full_comment += f"Sources: {request.sources_count}, Length: {answer_length}"
            
            # Si pas de trace_id, essayer de le récupérer depuis le contexte Langfuse
            trace_id_to_use = request.trace_id
            if not trace_id_to_use:
                print(f"   ⚠️  Pas de trace_id fourni - tentative de récupération depuis contexte")
                try:
                    from langfuse import Langfuse
                    langfuse_client = Langfuse(
                        secret_key=settings.langfuse_secret_key,
                        public_key=settings.langfuse_public_key,
                        host=settings.langfuse_host
                    )
                    if hasattr(langfuse_client, 'get_current_trace_id'):
                        trace_id_to_use = langfuse_client.get_current_trace_id()
                        if trace_id_to_use:
                            print(f"   ✅ Trace ID récupéré depuis contexte: {trace_id_to_use}")
                except Exception as e:
                    print(f"   ⚠️  Impossible de récupérer trace_id depuis contexte: {e}")
            
            # Utiliser la valeur brute (0-5) si disponible, sinon convertir la valeur normalisée (0-1) en 0-5
            # IMPORTANT: raw_score peut être 0, donc on vérifie explicitement is not None
            score_value_to_send = None
            if request.raw_score is not None:
                # Utiliser la valeur brute (0-5) directement
                score_value_to_send = float(request.raw_score)
                print(f"   ✅ Utilisation de la valeur brute: {score_value_to_send}/5")
            else:
                # Si pas de valeur brute, multiplier par 5 pour convertir 0-1 en 0-5
                score_value_to_send = float(request.accuracy_score) * 5.0
                print(f"   ⚠️  Pas de raw_score - conversion de {request.accuracy_score} (0-1) en {score_value_to_send} (0-5)")
            
            print(f"   📤 Valeur finale envoyée à Langfuse: {score_value_to_send}")
            
            # Créer le score avec le trace_id (ou utiliser score_current_trace si None)
            user_score_id = create_score(
                trace_id=trace_id_to_use,
                name="user_rating",
                value=score_value_to_send,  # Envoyer la valeur 0-5
                comment=full_comment,
                metadata=None,  # Don't use metadata, include in comment instead
                use_current_trace=True  # Try to use score_current_trace if trace_id is still None
            )
            
            if user_score_id:
                print(f"   ✅ Score créé avec ID: {user_score_id}")
            else:
                print(f"   ⚠️  Score créé mais ID non récupéré - vérifiez dans Langfuse")
            scores_created["user_rating"] = user_score_id
        
        # Create relevance score if provided
        if request.relevance_score is not None:
            relevance_id = create_score(
                trace_id=request.trace_id,
                name="relevance",
                value=request.relevance_score,
                comment=f"Relevance score (manual evaluation): {request.comment or ''}",
                metadata={
                    "question": request.question,
                    "sources_count": request.sources_count,
                    "evaluation_type": "manual"
                }
            )
            scores_created["relevance"] = relevance_id
        
        # Create completeness score if provided
        if request.completeness_score is not None:
            completeness_id = create_score(
                trace_id=request.trace_id,
                name="completeness",
                value=request.completeness_score,
                comment=f"Completeness score (manual evaluation): {request.comment or ''}",
                metadata={
                    "answer_length": answer_length,
                    "sources_count": request.sources_count,
                    "evaluation_type": "manual"
                }
            )
            scores_created["completeness"] = completeness_id
        
        return {
            "success": True,
            "scores": scores_created,
            "trace_id": request.trace_id,
            "message": f"✅ {len(scores_created)} score(s) créé(s) dans Langfuse"
        }
    except Exception as e:
        print(f"❌ Erreur lors de la création des scores: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )




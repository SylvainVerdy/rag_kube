"""RAG Generation with LangChain"""

from typing import List, Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
# Chains are now handled via LCEL (LangChain Expression Language)
try:
    from langfuse.langchain import CallbackHandler as LangfuseCallbackHandler
    LANGFUSE_AVAILABLE = True
except ImportError:
    try:
        from langfuse.callback import CallbackHandler as LangfuseCallbackHandler
        LANGFUSE_AVAILABLE = True
    except ImportError:
        try:
            from langchain_core.callbacks import LangfuseCallbackHandler
            LANGFUSE_AVAILABLE = True
        except ImportError:
            LangfuseCallbackHandler = None
            LANGFUSE_AVAILABLE = False
from src.config import settings

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    class MockMLflow:
        @staticmethod
        def log_param(*args, **kwargs): pass
        @staticmethod
        def log_metric(*args, **kwargs): pass
    mlflow = MockMLflow()


class RAGGenerator:
    """RAG generation system"""
    
    def __init__(
        self,
        llm_model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        use_langfuse: bool = True
    ):
        self.llm_model = llm_model or settings.llm_model
        self.temperature = temperature or settings.temperature
        self.max_tokens = max_tokens or settings.max_tokens
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=self.llm_model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=settings.openai_api_key
        )
        
        # Langfuse callback handler
        self.langfuse_handler = None
        if use_langfuse and settings.enable_langfuse and LANGFUSE_AVAILABLE and LangfuseCallbackHandler:
            if settings.langfuse_secret_key and settings.langfuse_public_key:
                try:
                    # Initialiser le client Langfuse d'abord
                    from langfuse import Langfuse
                    import os
                    
                    # Le CallbackHandler utilise les variables d'environnement
                    os.environ["LANGFUSE_SECRET_KEY"] = settings.langfuse_secret_key
                    os.environ["LANGFUSE_PUBLIC_KEY"] = settings.langfuse_public_key
                    os.environ["LANGFUSE_HOST"] = settings.langfuse_host
                    
                    # Initialiser le client (nécessaire pour que le CallbackHandler fonctionne)
                    langfuse_client = Langfuse(
                        secret_key=settings.langfuse_secret_key,
                        public_key=settings.langfuse_public_key,
                        host=settings.langfuse_host
                    )
                    
                    # Maintenant initialiser le CallbackHandler
                    self.langfuse_handler = LangfuseCallbackHandler(
                        public_key=settings.langfuse_public_key
                    )
                    print(f"✅ Langfuse initialisé - Host: {settings.langfuse_host}")
                except Exception as e:
                    print(f"⚠️  Warning: Could not initialize Langfuse: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                print("⚠️  Warning: Langfuse keys not configured in .env")
        elif use_langfuse and not LANGFUSE_AVAILABLE:
            print("⚠️  Warning: Langfuse not available (module not installed)")
        
        # Setup prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that answers questions based on the provided context.
Use only the information from the context to answer. If the context doesn't contain enough information,
say that you don't have enough information to answer the question.

Context:
{context}

Question: {question}

Provide a detailed and accurate answer:"""),
            MessagesPlaceholder(variable_name="chat_history"),
        ])
    
    def generate(
        self,
        question: str,
        context_documents: List[Document],
        chat_history: Optional[List] = None
    ) -> Dict[str, Any]:
        """Generate answer from question and context"""
        
        # Format context
        context = "\n\n".join([doc.page_content for doc in context_documents])
        
        # Format chat history
        formatted_history = []
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    formatted_history.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    formatted_history.append(AIMessage(content=msg["content"]))
        
        # Create chain
        chain = self.prompt_template | self.llm
        
        # Prepare callbacks (Langfuse handler)
        callbacks = []
        if self.langfuse_handler:
            callbacks.append(self.langfuse_handler)
        
        # Invoke with callbacks
        # The CallbackHandler will create a trace automatically
        response = chain.invoke(
            {
                "context": context,
                "question": question,
                "chat_history": formatted_history
            },
            config={"callbacks": callbacks} if callbacks else {}
        )
        
        answer = response.content
        
        # Try to get trace_id from the CallbackHandler after invocation
        # The CallbackHandler stores the trace_id internally
        trace_id = None
        try:
            if self.langfuse_handler:
                # Inspect the handler to find the trace_id
                # The CallbackHandler might store it in various attributes
                handler_attrs = dir(self.langfuse_handler)
                
                # Common attribute names where trace_id might be stored
                possible_attrs = ['trace_id', 'run_id', 'traceId', '_trace_id', '_run_id', 
                                'current_trace_id', 'langfuse_trace_id', 'trace']
                
                for attr_name in possible_attrs:
                    if hasattr(self.langfuse_handler, attr_name):
                        try:
                            attr_value = getattr(self.langfuse_handler, attr_name)
                            if attr_value and isinstance(attr_value, str) and len(attr_value) > 10:
                                trace_id = attr_value
                                print(f"✅ Trace ID trouvé dans handler.{attr_name}: {trace_id}")
                                break
                        except:
                            continue
                
                # If not found, try to get from handler's internal state
                if not trace_id:
                    # Try to access private attributes
                    for attr in handler_attrs:
                        if 'trace' in attr.lower() or 'run' in attr.lower():
                            try:
                                value = getattr(self.langfuse_handler, attr)
                                if value and isinstance(value, str) and len(value) > 10:
                                    trace_id = value
                                    print(f"✅ Trace ID trouvé dans handler.{attr}: {trace_id}")
                                    break
                            except:
                                continue
                
                if not trace_id:
                    print(f"⚠️  Trace ID non trouvé dans le CallbackHandler")
                    print(f"   Attributs inspectés: {len(handler_attrs)}")
                    print(f"   💡 Les scores utiliseront score_current_trace() si disponible")
        except Exception as e:
            print(f"⚠️  Warning: Could not get trace_id from handler: {e}")
        
        # Store trace_id for later use
        self.last_trace_id = trace_id
        
        # Log to MLflow (si disponible)
        if MLFLOW_AVAILABLE:
            mlflow.log_param("question", question)
            mlflow.log_metric("context_docs_count", len(context_documents))
            mlflow.log_metric("answer_length", len(answer))
        
        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata if isinstance(doc.metadata, dict) else {"source": str(doc.metadata)}
                }
                for doc in context_documents
            ],
            "model": self.llm_model,
            "trace_id": trace_id  # Include trace_id in response
        }
    
    def generate_with_retriever(
        self,
        question: str,
        retriever,
        chat_history: Optional[List] = None
    ) -> Dict[str, Any]:
        """Generate answer using a retriever"""
        # Retrieve relevant documents
        try:
            context_documents = retriever.invoke(question)
        except AttributeError:
            # Fallback pour les anciennes versions
            context_documents = retriever.get_relevant_documents(question)
        
        # Generate answer
        return self.generate(question, context_documents, chat_history)


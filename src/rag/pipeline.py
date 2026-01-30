"""Complete RAG Pipeline using LangGraph"""

from typing import List, Dict, Any, Optional, TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from .retrieval import RetrievalSystem
from .generation import RAGGenerator

try:
    import mlflow
    MLFLOW_AVAILABLE = True
except ImportError:
    MLFLOW_AVAILABLE = False
    class MockMLflow:
        @staticmethod
        def log_metric(*args, **kwargs): pass
    mlflow = MockMLflow()


class RAGState(TypedDict):
    """State for RAG pipeline"""
    messages: List
    documents: List
    question: str
    answer: str
    chat_history: List[Dict[str, str]]
    sources: List[Dict[str, Any]]


class RAGPipeline:
    """Complete RAG pipeline using LangGraph"""
    
    def __init__(
        self,
        retrieval_system: RetrievalSystem,
        generator: RAGGenerator
    ):
        self.retrieval_system = retrieval_system
        self.generator = generator
        
        # Build LangGraph workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(RAGState)
        
        # Add nodes
        workflow.add_node("retrieve", self._retrieve_node)
        workflow.add_node("generate", self._generate_node)
        
        # Set entry point
        workflow.set_entry_point("retrieve")
        
        # Add edges
        workflow.add_edge("retrieve", "generate")
        workflow.add_edge("generate", END)
        
        return workflow.compile()
    
    def _retrieve_node(self, state: RAGState) -> RAGState:
        """Retrieve relevant documents"""
        question = state.get("question", "")
        
        # Retrieve documents
        documents = self.retrieval_system.similarity_search(question)
        
        state["documents"] = documents
        if MLFLOW_AVAILABLE:
            mlflow.log_metric("retrieved_docs", len(documents))
        
        return state
    
    def _generate_node(self, state: RAGState) -> RAGState:
        """Generate answer from retrieved documents"""
        question = state.get("question", "")
        documents = state.get("documents", [])
        chat_history = state.get("chat_history", [])
        
        # Generate answer
        result = self.generator.generate(question, documents, chat_history)
        
        state["answer"] = result["answer"]
        state["sources"] = result.get("sources", [])
        
        return state
    
    def run(
        self,
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Run the complete RAG pipeline"""
        initial_state = {
            "question": question,
            "chat_history": chat_history or [],
            "messages": []
        }
        
        # Run workflow
        final_state = self.workflow.invoke(initial_state)
        
        # Get trace_id from generator if available
        trace_id = final_state.get("trace_id") or self.generator.last_trace_id if hasattr(self.generator, 'last_trace_id') else None
        
        return {
            "question": question,
            "answer": final_state.get("answer", ""),
            "sources": final_state.get("sources", []),
            "model": self.generator.llm_model,
            "trace_id": trace_id
        }
    
    def stream(
        self,
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ):
        """Stream the RAG pipeline execution"""
        initial_state = {
            "question": question,
            "chat_history": chat_history or [],
            "messages": []
        }
        
        for state in self.workflow.stream(initial_state):
            yield state


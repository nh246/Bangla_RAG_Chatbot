"""
Vector store initialization and management.
"""
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import Optional, List
import logging

from app.config import settings, FAQ_DATA

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStoreManager:
    """Singleton manager for the FAISS vector store."""
    
    _instance: Optional['VectorStoreManager'] = None
    _vector_store: Optional[FAISS] = None
    _documents: Optional[List[Document]] = None
    _embedding_model: Optional[HuggingFaceEmbeddings] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorStoreManager, cls).__new__(cls)
        return cls._instance
    
    def initialize(self) -> None:
        """Initialize the vector store and embedding model."""
        if self._vector_store is not None:
            logger.info("Vector store already initialized")
            return
        
        try:
            logger.info("Initializing embedding model...")
            # Initialize multilingual embedding model (supports Bengali)
            self._embedding_model = HuggingFaceEmbeddings(
                model_name=settings.embedding_model_name
            )
            
            logger.info("Creating documents from FAQ data...")
            # Create documents from FAQ data
            self._documents = [
                Document(
                    page_content=f"প্রশ্ন: {q} উত্তর: {a}",
                    metadata=meta
                )
                for q, a, meta in FAQ_DATA
            ]
            
            logger.info(f"Creating FAISS vector store with {len(self._documents)} documents...")
            # Create FAISS vector store
            self._vector_store = FAISS.from_documents(
                self._documents,
                self._embedding_model
            )
            
            logger.info("Vector store initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing vector store: {e}")
            raise
    
    @property
    def vector_store(self) -> Optional[FAISS]:
        """Get the vector store instance."""
        return self._vector_store
    
    @property
    def documents(self) -> Optional[List[Document]]:
        """Get the list of documents."""
        return self._documents
    
    @property
    def embedding_model(self) -> Optional[HuggingFaceEmbeddings]:
        """Get the embedding model."""
        return self._embedding_model
    
    @property
    def is_initialized(self) -> bool:
        """Check if vector store is initialized."""
        return self._vector_store is not None


# Global instance
vector_store_manager = VectorStoreManager()

import logging
from pathlib import Path
from app.core.config import settings
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

try:
    import chromadb
    HAS_CHROMADB = True
except ImportError:
    HAS_CHROMADB = False
    logger.warning("chromadb not installed - vector store functionality disabled")

class VectorStore:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.collections = {}
        self.client = None
        
        if HAS_CHROMADB:
            try:
                Path(settings.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)
                self.client = chromadb.PersistentClient(
                    path=settings.CHROMA_PERSIST_DIR
                )
                logger.info("ChromaDB initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize ChromaDB: {e}")
                self.client = None
    
    def get_or_create_collection(self, name: str):
        """Get or create a collection"""
        
        if not HAS_CHROMADB or self.client is None:
            logger.debug(f"ChromaDB not available - returning mock collection for {name}")
            return None
        
        if name in self.collections:
            return self.collections[name]
        
        logger.info(f"Creating/retrieving collection: {name}")
        
        collection = self.client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"}
        )
        
        self.collections[name] = collection
        return collection
    
    def add_documents(self, collection_name: str, documents: dict[str, str]):
        """Add documents to collection"""
        
        if not HAS_CHROMADB or self.client is None:
            logger.debug("ChromaDB not available - skipping document addition")
            return
        
        collection = self.get_or_create_collection(collection_name)
        if collection is None:
            return
        
        logger.info(f"Adding {len(documents)} documents to {collection_name}")
        
        ids = list(documents.keys())
        texts = list(documents.values())
        embeddings = self.embedding_service.get_embeddings_batch(texts)
        
        metadatas = [{"source": id_} for id_ in ids]
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
    
    def search(self, collection_name: str, query_text: str, n_results: int = 5) -> list[dict]:
        """Search collection by query text"""
        
        if not HAS_CHROMADB or self.client is None:
            logger.debug("ChromaDB not available - returning empty results")
            return []
        
        collection = self.get_or_create_collection(collection_name)
        if collection is None:
            return []
        
        logger.info(f"Searching {collection_name} for: {query_text[:50]}...")
        
        query_embedding = self.embedding_service.get_embedding(query_text)
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        formatted_results = []
        if results['ids'] and len(results['ids']) > 0:
            for i, id_ in enumerate(results['ids'][0]):
                formatted_results.append({
                    "id": id_,
                    "document": results['documents'][0][i],
                    "distance": results['distances'][0][i]
                })
        
        return formatted_results
    
    def clear_collection(self, collection_name: str):
        """Clear a collection"""
        
        if not HAS_CHROMADB or self.client is None:
            logger.debug("ChromaDB not available - skipping collection clear")
            return
        
        logger.info(f"Clearing collection: {collection_name}")
        
        if collection_name in self.collections:
            del self.collections[collection_name]
        
        try:
            self.client.delete_collection(name=collection_name)
        except:
            pass

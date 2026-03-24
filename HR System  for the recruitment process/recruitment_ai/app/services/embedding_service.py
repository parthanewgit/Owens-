import logging
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL
        self.embedding_cache = {}
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def get_embedding(self, text: str) -> list[float]:
        """Get embedding for text with caching"""
        
        if text in self.embedding_cache:
            logger.debug("Embedding cache hit")
            return self.embedding_cache[text]
        
        logger.info(f"Generating embedding for text: {text[:50]}...")
        
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        
        embedding = response.data[0].embedding
        self.embedding_cache[text] = embedding
        
        return embedding
    
    def get_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts"""
        
        logger.info(f"Generating embeddings for {len(texts)} texts")
        
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        
        embeddings = [item.embedding for item in response.data]
        
        for text, embedding in zip(texts, embeddings):
            self.embedding_cache[text] = embedding
        
        return embeddings
    
    def clear_cache(self):
        """Clear embedding cache"""
        self.embedding_cache.clear()
        logger.info("Embedding cache cleared")

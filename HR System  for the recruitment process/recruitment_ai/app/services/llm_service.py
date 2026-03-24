import json
import logging
from typing import Any, Optional
from openai import OpenAI, APIError, BadRequestError, AuthenticationError
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_structured_response(
        self,
        prompt: str,
        response_schema: dict,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> dict:
        """Generate a structured JSON response from LLM"""
        
        logger.info(f"LLM Request - Temperature: {temperature}, Tokens: {max_tokens}")
        logger.debug(f"Prompt length: {len(prompt)}, Schema: {response_schema.get('type')}")
        
        try:
            logger.debug(f"Using model: {self.model}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert recruitment AI system. Always respond with valid JSON matching the exact schema provided."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("LLM Response succeeded")
            return result
            
        except BadRequestError as e:
            logger.error(f"BadRequestError from OpenAI: {str(e)}")
            logger.error(f"Error message: {e.message if hasattr(e, 'message') else str(e)}")
            raise ValueError(f"OpenAI API BadRequest Error - check schema format or API key validity: {str(e)}")
        except AuthenticationError as e:
            logger.error(f"AuthenticationError: Invalid or expired OpenAI API key")
            raise ValueError(f"OpenAI Authentication Failed - Please check your API key in .env file")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            raise ValueError(f"Failed to parse LLM response as JSON: {e}")
        except Exception as e:
            logger.error(f"LLM error: {type(e).__name__}: {str(e)}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate plain text response from LLM"""
        
        logger.info(f"Text generation - Temperature: {temperature}")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert recruitment AI system."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def extract_skills_from_text(self, text: str) -> list[str]:
        """Extract skills from text"""
        
        # Truncate text if too long to avoid token limit issues
        max_chars = 3000
        if len(text) > max_chars:
            text = text[:max_chars]
        
        prompt = f"""Extract all technical and soft skills from the following text. Return as a JSON list.

Text:
{text}

Respond with JSON: {{"skills": ["skill1", "skill2", ...]}}"""
        
        response_schema = {
            "type": "object",
            "properties": {
                "skills": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 0
                }
            },
            "required": ["skills"]
        }
        
        result = self.generate_structured_response(
            prompt,
            response_schema,
            temperature=0.2,
            max_tokens=500
        )
        
        return result.get("skills", [])

import logging
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class QuestionGenerationAgent:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def generate_questions(
        self,
        job_description: str,
        num_technical: int = 5,
        num_behavioral: int = 3,
        num_scenario: int = 2
    ) -> dict:
        """Generate mixed-type interview questions based on job description"""
        
        logger.info(f"Generating {num_technical + num_behavioral + num_scenario} mixed-type questions")
        
        prompt = f"""Based on the following job description, generate interview questions in mixed format:

Job Description:
{job_description}

For each question, decide if it should be MCQ or Free Text based on the question type.

For MCQ questions: provide 4 options (A, B, C, D) and correct answer
For Free Text questions: provide the question and expected key points

Generate:
- {num_technical} technical questions (mix of MCQ and free text)
- {num_behavioral} behavioral questions (mix of MCQ and free text)
- {num_scenario} scenario-based questions (mix of MCQ and free text)

For each technical question return: {{"type": "mcq" or "freetext", "question": "...", "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}}, "correct_answer": "A"}} OR {{"type": "freetext", "question": "...", "expected_answer": "..."}}

Format: {{"technical_questions": [...], "behavioral_questions": [...], "scenario_questions": [...]}}"""
        
        response_schema = {
            "type": "object",
            "properties": {
                "technical_questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["mcq", "freetext"]
                            },
                            "question": {"type": "string"},
                            "options": {
                                "type": "object",
                                "properties": {
                                    "A": {"type": "string"},
                                    "B": {"type": "string"},
                                    "C": {"type": "string"},
                                    "D": {"type": "string"}
                                }
                            },
                            "correct_answer": {"type": "string"},
                            "expected_answer": {"type": "string"}
                        },
                        "required": ["type", "question"]
                    }
                },
                "behavioral_questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["mcq", "freetext"]
                            },
                            "question": {"type": "string"},
                            "options": {
                                "type": "object",
                                "properties": {
                                    "A": {"type": "string"},
                                    "B": {"type": "string"},
                                    "C": {"type": "string"},
                                    "D": {"type": "string"}
                                }
                            },
                            "correct_answer": {"type": "string"},
                            "expected_answer": {"type": "string"}
                        },
                        "required": ["type", "question"]
                    }
                },
                "scenario_questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["mcq", "freetext"]
                            },
                            "question": {"type": "string"},
                            "options": {
                                "type": "object",
                                "properties": {
                                    "A": {"type": "string"},
                                    "B": {"type": "string"},
                                    "C": {"type": "string"},
                                    "D": {"type": "string"}
                                }
                            },
                            "correct_answer": {"type": "string"},
                            "expected_answer": {"type": "string"}
                        },
                        "required": ["type", "question"]
                    }
                }
            },
            "required": ["technical_questions", "behavioral_questions", "scenario_questions"]
        }
        
        result = self.llm_service.generate_structured_response(
            prompt,
            response_schema,
            temperature=0.7
        )
        
        logger.info("Mixed-type question generation complete")
        
        return result

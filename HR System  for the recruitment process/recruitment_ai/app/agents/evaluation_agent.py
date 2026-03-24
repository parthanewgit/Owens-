import logging
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class AnswerEvaluationAgent:
    def __init__(self):
        self.llm_service = LLMService()
    
    async def evaluate(self, question: str, candidate_answer: str, mcq_answer: str = None, question_type: str = None, correct_answer: str = None) -> dict:
        """Evaluate candidate's answer to interview question"""
        
        logger.info("Starting answer evaluation")
        
        # For MCQ questions: direct scoring based on correct answer
        if question_type == "mcq" and correct_answer:
            is_correct = mcq_answer and mcq_answer.upper() == correct_answer.upper()
            score = 10 if is_correct else 0
            
            logger.info(f"MCQ Evaluation: {'Correct' if is_correct else 'Incorrect'} - Score {score}/10")
            
            return {
                "score": score,
                "strengths": None,
                "weaknesses": None,
                "improvement_suggestions": None,
                "expected_answer": correct_answer
            }
        
        # For free text questions: use LLM evaluation
        mcq_part = ""
        if mcq_answer:
            mcq_part = f"\nCandidate's MCQ Answer: {mcq_answer}"
        
        prompt = f"""Evaluate the following interview answer.

Question: {question}{mcq_part}

Candidate Answer: {candidate_answer}

Provide an evaluation with:
- Score (0-10)
- List of strengths (3-5 items)
- List of weaknesses (2-4 items)
- Improvement suggestions (2-3 items)
- Expected answer (a brief summary of what a strong answer should include)

Respond with JSON: {{"score": 0, "strengths": [...], "weaknesses": [...], "improvement_suggestions": [...], "expected_answer": "..."}}"""
        
        response_schema = {
            "type": "object",
            "properties": {
                "score": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 10,
                    "description": "Score from 0-10"
                },
                "strengths": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of strengths in the answer"
                },
                "weaknesses": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of weaknesses in the answer"
                },
                "improvement_suggestions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Suggestions for improvement"
                },
                "expected_answer": {
                    "type": "string",
                    "description": "Expected answer or key points that should be covered"
                }
            },
            "required": ["score", "strengths", "weaknesses", "improvement_suggestions", "expected_answer"]
        }
        
        result = self.llm_service.generate_structured_response(
            prompt,
            response_schema,
            temperature=0.3
        )
        
        logger.info(f"Evaluation complete: Score {result.get('score')}/10")
        
        return result

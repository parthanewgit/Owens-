import logging
from app.agents.resume_agent import ResumeMatchingAgent
from app.agents.question_agent import QuestionGenerationAgent
from app.agents.evaluation_agent import AnswerEvaluationAgent
from app.agents.learning_agent import LearningRoadmapAgent

logger = logging.getLogger(__name__)

class OrchestrationService:
    def __init__(self):
        self.resume_agent = ResumeMatchingAgent()
        self.question_agent = QuestionGenerationAgent()
        self.evaluation_agent = AnswerEvaluationAgent()
        self.learning_agent = LearningRoadmapAgent()
    
    async def analyze_candidates(
        self,
        job_description: str,
        resume_texts: dict[str, str]
    ) -> dict:
        """Orchestrate resume matching"""
        
        logger.info("Starting candidate analysis orchestration")
        
        result = await self.resume_agent.match_resumes(
            job_description,
            resume_texts
        )
        
        logger.info(f"Analysis complete: {len(result.get('ranked_candidates', []))} candidates")
        
        return result
    
    async def generate_questions(
        self,
        job_description: str,
        num_technical: int = 5,
        num_behavioral: int = 3,
        num_scenario: int = 2
    ) -> dict:
        """Orchestrate question generation"""
        
        logger.info(f"Starting question generation: {num_technical} technical, {num_behavioral} behavioral, {num_scenario} scenario")
        
        result = await self.question_agent.generate_questions(
            job_description,
            num_technical,
            num_behavioral,
            num_scenario
        )
        
        logger.info("Question generation complete")
        
        return result
    
    async def evaluate_answer(
        self,
        question: str,
        candidate_answer: str,
        mcq_answer: str = None,
        question_type: str = None,
        correct_answer: str = None
    ) -> dict:
        """Orchestrate answer evaluation"""
        
        logger.info("Starting answer evaluation")
        
        result = await self.evaluation_agent.evaluate(
            question,
            candidate_answer,
            mcq_answer,
            question_type,
            correct_answer
        )
        
        logger.info(f"Evaluation complete: Score {result.get('score')}/10")
        
        return result
    
    async def generate_learning_roadmap(
        self,
        missing_skills: list[str]
    ) -> dict:
        """Orchestrate learning roadmap generation"""
        
        logger.info(f"Generating learning roadmap for {len(missing_skills)} skills")
        
        result = await self.learning_agent.generate_roadmap(missing_skills)
        
        logger.info("Learning roadmap generation complete")
        
        return result

import logging
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class ResumeMatchingAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.embedding_service = EmbeddingService()
    
    async def match_resumes(
        self,
        job_description: str,
        resume_texts: dict[str, str]
    ) -> dict:
        """Match resumes against job description"""
        
        logger.info(f"Matching {len(resume_texts)} resumes against job")
        
        jd_skills = self.llm_service.extract_skills_from_text(job_description)
        logger.info(f"Extracted {len(jd_skills)} skills from job description")
        
        jd_embedding = self.embedding_service.get_embedding(job_description)
        
        ranked_candidates = []
        
        for candidate_name, resume_text in resume_texts.items():
            logger.info(f"Processing resume: {candidate_name}")
            
            resume_skills = self.llm_service.extract_skills_from_text(resume_text)
            
            resume_embedding = self.embedding_service.get_embedding(resume_text)
            
            similarity = cosine_similarity(
                [jd_embedding],
                [resume_embedding]
            )[0][0]
            
            # Case-insensitive skill matching
            resume_skills_lower = [s.lower() for s in resume_skills]
            jd_skills_lower = [s.lower() for s in jd_skills]
            
            matched_skills = [s for s in resume_skills if s.lower() in jd_skills_lower]
            missing_skills = [s for s in jd_skills if s.lower() not in resume_skills_lower]
            
            # Calculate skill-based score
            total_jd_skills = len(jd_skills)
            skill_match_score = 0.0
            
            if total_jd_skills > 0:
                skill_match_score = len(matched_skills) / total_jd_skills
            else:
                # If no skills extracted from JD, fall back to semantic similarity
                skill_match_score = similarity
            
            # Combine skill match score with semantic similarity (weighted average)
            # Weight skill matching more heavily (70%) and semantic similarity (30%)
            combined_score = (skill_match_score * 0.7) + (similarity * 0.3)
            
            ranked_candidates.append({
                "name": candidate_name,
                "similarity_score": float(combined_score),
                "skill_match_score": float(skill_match_score),
                "semantic_similarity": float(similarity),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "total_jd_skills": total_jd_skills
            })
        
        ranked_candidates.sort(
            key=lambda x: x["similarity_score"],
            reverse=True
        )
        
        logger.info(f"Ranking complete: {len(ranked_candidates)} candidates ranked")
        
        return {"ranked_candidates": ranked_candidates}

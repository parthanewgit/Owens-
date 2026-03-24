from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class SkillMatch(BaseModel):
    name: str
    similarity_score: float = Field(ge=0.0, le=1.0)
    skill_match_score: float = Field(ge=0.0, le=1.0, default=0.0)
    semantic_similarity: float = Field(ge=0.0, le=1.0, default=0.0)
    matched_skills: List[str]
    missing_skills: List[str]
    total_jd_skills: int = Field(default=0)

class ResumeAnalysisResponse(BaseModel):
    ranked_candidates: List[SkillMatch]

class QuestionRequest(BaseModel):
    job_description: str
    num_technical: int = 5
    num_behavioral: int = 3
    num_scenario: int = 2

class MCQQuestion(BaseModel):
    type: str = "mcq"
    question: str
    options: dict  # {"A": "option_a", "B": "option_b", "C": "option_c", "D": "option_d"}
    correct_answer: str  # "A", "B", "C", or "D"

class FreeTextQuestion(BaseModel):
    type: str = "freetext"
    question: str
    expected_answer: Optional[str] = None  # Key points expected in answer

class QuestionGenerationResponse(BaseModel):
    candidate_name: Optional[str] = None
    job_description: Optional[str] = None
    all_questions: Optional[List[dict]] = None  # Mixed MCQ and FreeText questions
    technical_questions: List[dict]
    behavioral_questions: List[dict]
    scenario_questions: List[dict]

class QuestionAnswer(BaseModel):
    question_index: int
    question_text: str
    question_type: str  # "mcq" or "freetext"
    mcq_answer: Optional[str] = None  # For MCQ questions
    free_text_answer: Optional[str] = None  # For free text questions

class AnswerEvaluationRequest(BaseModel):
    job_description: str
    candidate_name: Optional[str] = None
    answers: List[QuestionAnswer]  # Batch evaluation

class SingleAnswerEvaluationRequest(BaseModel):
    question: str
    candidate_answer: str
    mcq_answer: Optional[str] = None
    candidate_name: Optional[str] = None
    question_type: Optional[str] = None  # "mcq" or "freetext"
    correct_answer: Optional[str] = None  # For MCQ questions

class EvaluationScore(BaseModel):
    score: int = Field(ge=0, le=10)
    strengths: Optional[List[str]] = None  # Not provided for MCQ questions
    weaknesses: Optional[List[str]] = None  # Not provided for MCQ questions
    improvement_suggestions: Optional[List[str]] = None  # Not provided for MCQ questions
    expected_answer: Optional[str] = None  # Optionally provided by backend

class LearningRoadmapRequest(BaseModel):
    missing_skills: List[str]

class LearningRoadmapResponse(BaseModel):
    roadmap: dict  # Dict of weeks {week_1: {...}, week_2: {...}, ...}
    resources: List[str]
    mini_projects: List[str]

class AnalysisRequest(BaseModel):
    job_description: str
    resumes: dict

class CandidateProfile(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    matched_skills: List[str]
    missing_skills: List[str]
    similarity_score: float
    generated_questions: Optional[QuestionGenerationResponse] = None
    learning_roadmap: Optional[LearningRoadmapResponse] = None

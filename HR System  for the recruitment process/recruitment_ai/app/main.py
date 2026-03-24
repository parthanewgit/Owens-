import logging
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import tempfile
import os
import asyncio

from app.core.logging_config import logger
from app.core.config import settings
from app.models.schemas import (
    LoginRequest, TokenResponse, ResumeAnalysisResponse,
    QuestionGenerationResponse, AnswerEvaluationRequest, SingleAnswerEvaluationRequest, EvaluationScore,
    LearningRoadmapRequest, LearningRoadmapResponse, AnalysisRequest, QuestionRequest
)
from app.services.auth_service import AuthService
from app.services.parser_service import ParserService
from app.services.orchestration_service import OrchestrationService

app = FastAPI(
    title="HR Requirement System",
    description="Multi-Agent AI HR Requirement System - Project by Parthasarathi Mishra and Prateek Anand",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestration_service = OrchestrationService()

def get_current_user(authorization: Optional[str] = Header(None)):
    """Validate JWT token and return current user"""
    
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid authentication scheme")
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header"
        )
    
    user = AuthService.verify_token(token)
    return user

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    logger.info(f"OpenAI Model: {settings.OPENAI_MODEL}")
    logger.info(f"Database: {settings.DATABASE_URL}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutdown")

@app.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """User login endpoint"""
    
    logger.info(f"Login attempt for user: {request.username}")
    
    if not AuthService.verify_credentials(request.username, request.password):
        logger.warning(f"Failed login attempt: {request.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    access_token = AuthService.create_access_token(
        data={"sub": request.username}
    )
    
    logger.info(f"Successful login: {request.username}")
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resumes(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Analyze resumes against job description"""
    
    logger.info(f"Resume analysis request from {current_user['username']}")
    
    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description cannot be empty"
        )
    
    if not resumes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one resume file is required"
        )
    
    resume_texts = {}
    
    for resume_file in resumes:
        tmp_path = None
        try:
            # Write file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.filename)[1]) as tmp:
                contents = await resume_file.read()
                tmp.write(contents)
                tmp.flush()
                tmp_path = tmp.name
            
            # Parse after file is fully written and closed
            parsed_text = ParserService.parse_resume(tmp_path)
            if not parsed_text or not parsed_text.strip():
                raise ValueError(f"Could not extract text from {resume_file.filename}")
            resume_texts[resume_file.filename] = parsed_text
            
        except Exception as e:
            logger.error(f"Error processing resume {resume_file.filename}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing resume {resume_file.filename}: {str(e)}"
            )
        finally:
            # Clean up temp file
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except:
                    pass
    
    try:
        result = await orchestration_service.analyze_candidates(
            job_description,
            resume_texts
        )
        return result
    except ValueError as e:
        logger.error(f"Validation error during analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error during analysis orchestration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing resumes: {str(e)}"
        )

@app.post("/generate-questions", response_model=QuestionGenerationResponse)
async def generate_questions(
    request: QuestionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate mixed-type interview questions"""
    
    logger.info(f"Question generation request from {current_user['username']}")
    
    result = await orchestration_service.generate_questions(
        request.job_description,
        request.num_technical,
        request.num_behavioral,
        request.num_scenario
    )
    
    # Add job description to response
    result["job_description"] = request.job_description
    
    return result

@app.post("/evaluate-answer", response_model=EvaluationScore)
async def evaluate_answer(
    request: SingleAnswerEvaluationRequest,
    current_user: dict = Depends(get_current_user)
):
    """Evaluate single candidate answer with optional MCQ selection"""
    
    logger.info(f"Answer evaluation request from {current_user['username']}")
    
    result = await orchestration_service.evaluate_answer(
        request.question,
        request.candidate_answer,
        request.mcq_answer,
        request.question_type,
        request.correct_answer
    )
    
    return result

@app.post("/generate-learning-plan", response_model=LearningRoadmapResponse)
async def generate_learning_plan(
    request: LearningRoadmapRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate personalized learning roadmap"""
    
    logger.info(f"Learning plan generation request from {current_user['username']}")
    
    result = await orchestration_service.generate_learning_roadmap(
        request.missing_skills
    )
    
    return result

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

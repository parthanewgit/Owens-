# Recruitment AI System - Technical Documentation

**Version:** 1.0.0  
**Created:** March 24, 2026  
**Authors:** Parthasarathi Mishra, Prateek Anand

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Core Components](#core-components)
4. [Workflow & Process Flow](#workflow--process-flow)
5. [API Endpoints](#api-endpoints)
6. [Data Models](#data-models)
7. [Technology Stack](#technology-stack)
8. [Database Schema](#database-schema)
9. [Security Implementation](#security-implementation)
10. [Deployment Guide](#deployment-guide)

---

## System Overview

The **Recruitment AI System** is a multi-agent artificial intelligence platform designed to revolutionize the hiring process. It leverages advanced NLP, machine learning, and GPT-4 to automate and enhance candidate evaluation, interview preparation, and assessment.

### Key Objectives
- **Automate resume matching** against job descriptions
- **Generate role-specific interview questions** (Technical, Behavioral, Scenario-based)
- **Evaluate candidate answers** with AI-powered scoring
- **Provide learning roadmaps** for candidate skill development
- **Reduce hiring timeline** while improving quality assessment

### Core Features
✅ Resume Intelligence Agent  
✅ Question Generation Engine  
✅ Answer Evaluation System  
✅ Learning Roadmap Generator  
✅ JWT Authentication  
✅ Real-time Processing  
✅ Vector-based Semantic Search  

---

## Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE LAYER                         │
│                    (Streamlit Web Application)                       │
│                         Port: 8501                                   │
│  • Login Dashboard      • Resume Upload      • Answer Evaluation    │
│  • Question Generation  • Results Display    • Learning Paths       │
└────────────┬────────────────────────────────────────────────────────┘
             │
             │ HTTP/REST API
             │
┌────────────▼────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                               │
│                    (FastAPI Framework)                               │
│                         Port: 8000                                   │
│  • Request Routing     • CORS Handling      • Error Management      │
│  • Middleware Stack    • Authentication    • Log Aggregation       │
└────────────┬────────────────────────────────────────────────────────┘
             │
      ┌──────┴──────────────────────────────┐
      │                                     │
┌─────▼────────────────────┐    ┌──────────▼──────────────────┐
│  ORCHESTRATION SERVICE   │    │  AUTHENTICATION SERVICE     │
│  • Workflow Coordination │    │  • JWT Token Generation    │
│  • Agent Management      │    │  • Credential Validation   │
│  • Process Routing       │    │  • Token Verification      │
└─────┬────────────────────┘    └──────────────────────────────┘
      │
      ├─────────────────┬──────────────────┬──────────────────┐
      │                 │                  │                  │
┌─────▼────────┐  ┌────▼───────┐  ┌───────▼──────┐  ┌────────▼─────┐
│ RESUME AGENT │  │ QUESTION    │  │ EVALUATION   │  │ LEARNING     │
│              │  │ AGENT       │  │ AGENT        │  │ AGENT        │
│ • Skill      │  │             │  │              │  │              │
│   Extraction │  │ • Technical │  │ • Scoring    │  │ • Gap        │
│ • Matching   │  │   Questions │  │   Engine     │  │   Analysis   │
│ • Ranking    │  │ • Behavioral│  │ • Feedback   │  │ • Path       │
│              │  │   Questions │  │   Generation │  │   Creation   │
└─────┬────────┘  │ • Scenario  │  │              │  │              │
      │           │   Questions │  │ • Analytics  │  └──────────────┘
      │           │             │  │              │
      │           └────┬────────┘  └────┬─────────┘
      │                │               │
      │      ┌─────────┴───────────────┘
      │      │
┌─────▼──────▼──────────────────────────────────────────────────┐
│              EXTERNAL AI SERVICES LAYER                        │
│                                                                │
│  • OpenAI GPT-4o (LLM Processing)                             │
│  • OpenAI Embeddings (Vector Representations)                 │
│  • NLP Processing & Semantic Analysis                         │
└─────┬──────────────────────────────────────────────────────────┘
      │
      ├──────────────────┬───────────────────┐
      │                  │                   │
┌─────▼──────┐    ┌──────▼───────┐    ┌─────▼────────┐
│   ChromaDB  │    │   SQLite     │    │   Vector     │
│   (Vector   │    │   Database   │    │   Store      │
│   Database) │    │              │    │              │
│             │    │ • User Data  │    │ • Embeddings │
│ • Resume    │    │ • Questions  │    │ • Semantic   │
│   Embeddings│    │ • Answers    │    │   Search     │
│ • Semantic  │    │ • Evaluations│    │              │
│   Search    │    │              │    │              │
└─────────────┘    └──────────────┘    └──────────────┘
```

### Component Interaction Flow

```
User Input
    ↓
    ├─→ [Streamlit Frontend]
    │       ↓
    │   [API Request]
    │       ↓
    ├─→ [FastAPI Gateway] → [Authentication Service]
    │       ↓
    │   [Orchestration Service]
    │       ↓
    │   ┌─────────────────────────────────────┐
    │   │ Select Agent Based on Request Type  │
    │   └─────────────────────────────────────┘
    │       │
    │       ├─→ Resume Analysis
    │       │   └─→ Resume Agent → LLM → ChromaDB
    │       │
    │       ├─→ Question Generation
    │       │   └─→ Question Agent → LLM → Database
    │       │
    │       ├─→ Answer Evaluation
    │       │   └─→ Evaluation Agent → LLM → Scoring
    │       │
    │       └─→ Learning Path
    │           └─→ Learning Agent → Analysis → Database
    │
    └─→ [Response Processing]
        ↓
    [Frontend Display]
        ↓
    User Result
```

---

## Core Components

### 1. **Resume Matching Agent**
**File:** `app/agents/resume_agent.py`

**Functionality:**
- Extracts skills from resumes using NLP
- Compares extracted skills with job description requirements
- Calculates semantic similarity scores
- Ranks candidates based on match scores
- Identifies skill gaps

**Input:** Resume document(s) + Job description  
**Output:** Ranked list of candidates with match scores  
**Processing:**
1. Parse resume (PDF/DOCX)
2. Extract skills using NLP
3. Embed resume and JD using OpenAI
4. Calculate similarity scores (cosine similarity)
5. Rank candidates
6. Store results

---

### 2. **Question Generation Agent**
**File:** `app/agents/question_agent.py`

**Functionality:**
- Generates technical interview questions
- Creates behavioral questions
- Develops scenario-based questions
- Customizes questions based on job role
- Provides expected answers/rubrics

**Question Types:**
- **Technical Questions:** 5 per role
- **Behavioral Questions:** 3 per role
- **Scenario Questions:** 2 per role

**Input:** Job description + Question parameters  
**Output:** Structured questions with multiple choice options or free-text format  

---

### 3. **Answer Evaluation Agent**
**File:** `app/agents/evaluation_agent.py`

**Functionality:**
- Evaluates candidate answers against expected responses
- Scores MCQ answers (0-10 scale)
- Evaluates free-text answers using AI
- Provides detailed feedback
- Generates evaluation metrics

**Scoring Methodology:**
- **MCQ:** Binary (correct/incorrect) → 0 or 10 points
- **Free-text:** Semantic analysis → 0-10 points
- **Overall:** Average of all question scores

**Output Metrics:**
```
{
  "total_score": 7.5,
  "question_scores": [10, 8, 5, 7, 6],
  "feedback": "Strong technical foundation...",
  "strengths": ["..."],
  "improvements": ["..."]
}
```

---

### 4. **Learning Roadmap Agent**
**File:** `app/agents/learning_agent.py`

**Functionality:**
- Analyzes skill gaps identified in evaluation
- Creates personalized learning paths
- Recommends resources and training
- Estimates timeline for skill development
- Tracks progress

**Output Components:**
- Missing skills list
- Learning objectives
- Recommended courses/resources
- Estimated duration
- Success metrics

---

### 5. **Orchestration Service**
**File:** `app/services/orchestration_service.py`

**Purpose:** Central coordinator managing workflow and agent interactions

**Key Methods:**
```python
async def analyze_candidates() → Resume matching workflow
async def generate_questions() → Question generation workflow
async def evaluate_answers() → Answer evaluation workflow
async def create_learning_roadmap() → Learning path creation
async def process_documents() → Document parsing workflow
```

---

### 6. **Authentication Service**
**File:** `app/services/auth_service.py`

**Features:**
- JWT token generation and verification
- Credential validation
- Session management
- Role-based access control

**Flow:**
1. User credentials (username/password)
2. Validate against stored credentials
3. Generate JWT token (24-hour expiration)
4. Store token in session
5. Validate token on each protected endpoint

---

## Workflow & Process Flow

### Complete User Journey

#### Step 1: User Login
```
1. User enters credentials (admin/admin123)
2. System validates credentials
3. JWT token generated
4. Token stored in session
5. Dashboard accessible
```

#### Step 2: Resume Analysis
```
1. User uploads job description
2. User uploads resume(s)
3. Resume parsing service extracts text
4. Resume Agent processes resumes
5. Skills extracted via LLM
6. Vector embeddings created
7. Semantic matching performed
8. Candidates ranked by match score
9. Results displayed with match percentages
```

#### Step 3: Question Generation
```
1. User selects job role
2. System retrieves job description
3. Question Agent consulted
4. LLM generates 10 tailored questions:
   - 5 Technical
   - 3 Behavioral
   - 2 Scenario
5. Questions formatted with options/rubrics
6. Stored in database
7. Ready for candidate assessment
```

#### Step 4: Answer Evaluation
```
1. Candidate submits answers
2. System validates responses
3. Evaluation Agent processes each answer
4. Scoring engine: 
   - MCQ: Instant scoring
   - Free-text: Semantic analysis
5. Detailed feedback generated
6. Score aggregated
7. Performance analytics created
8. Results stored for future reference
```

#### Step 5: Learning Roadmap
```
1. System analyzes evaluation results
2. Identifies skill gaps
3. Learning Agent creates personalized path
4. Recommends resources and timeline
5. Stores roadmap in database
6. Provides progress tracking
```

---

## API Endpoints

### Authentication
```
POST /login
├─ Request: {username, password}
└─ Response: {access_token, token_type}
```

### Resume Analysis
```
POST /analyze
├─ Parameters:
│  ├─ job_description: string
│  └─ resumes: List[File]
└─ Response: 
   └─ ranked_candidates: List[SkillMatch]
      ├─ name: string
      ├─ similarity_score: float (0-1)
      ├─ matched_skills: List[string]
      └─ missing_skills: List[string]
```

### Question Generation
```
POST /generate_questions
├─ Request:
│  ├─ job_description: string
│  ├─ num_technical: int (default: 5)
│  ├─ num_behavioral: int (default: 3)
│  └─ num_scenario: int (default: 2)
└─ Response:
   └─ questions: List[Question]
      ├─ type: string (mcq|freetext)
      ├─ question: string
      ├─ options: dict (for MCQ)
      └─ expected_answer: string
```

### Answer Evaluation
```
POST /evaluate
├─ Request:
│  ├─ question_id: string
│  └─ answer: string
└─ Response:
   ├─ score: float (0-10)
   ├─ feedback: string
   ├─ strengths: List[string]
   └─ improvements: List[string]
```

### Learning Roadmap
```
POST /learning_roadmap
├─ Request:
│  ├─ evaluation_id: string
│  └─ skill_gaps: List[string]
└─ Response:
   ├─ roadmap: List[LearningModule]
   ├─ estimated_duration: string
   ├─ resources: List[string]
   └─ milestones: List[Milestone]
```

---

## Data Models

### Resume Data Model
```python
class Resume(BaseModel):
    candidate_name: str
    extracted_skills: List[str]
    years_experience: float
    qualifications: List[str]
    job_titles: List[str]
    embeddings: List[float]  # Vector representation
```

### Question Data Model
```python
class Question(BaseModel):
    id: str
    type: str  # "technical", "behavioral", "scenario"
    question_text: str
    options: Optional[Dict]  # MCQ options
    expected_answer: Optional[str]
    created_at: datetime
    job_role: str
```

### Answer Data Model
```python
class Answer(BaseModel):
    id: str
    question_id: str
    candidate_name: str
    answer_text: str
    submitted_at: datetime
    evaluation_score: float
    feedback: str
```

### Evaluation Data Model
```python
class Evaluation(BaseModel):
    id: str
    candidate_name: str
    answers: List[Answer]
    overall_score: float
    strengths: List[str]
    improvements: List[str]
    created_at: datetime
```

---

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | Streamlit | 1.28.1 | Web UI Framework |
| **Backend** | FastAPI | 0.104.1 | REST API Framework |
| **Server** | Uvicorn | 0.24.0 | ASGI Server |
| **Database** | SQLite | Latest | Relational Data |
| **Vector DB** | ChromaDB | 0.4.14 | Vector Storage |
| **LLM** | OpenAI GPT-4o | Latest | Language Model |
| **Embeddings** | OpenAI Ada | Latest | Text Embedding |
| **Data Validation** | Pydantic | 2.4.2 | Schema Validation |
| **ORM** | SQLAlchemy | 2.0.23 | Database ORM |
| **Auth** | PyJWT | 2.11.0 | Token Management |
| **Document Parsing** | PyPDF2 | 3.0.1 | PDF Processing |
| **Document Parsing** | python-docx | 0.8.11 | DOCX Processing |
| **Testing** | pytest | 7.4.3 | Test Framework |
| **ML** | scikit-learn | 1.3.2 | ML Algorithms |
| **Retry Logic** | tenacity | 8.2.3 | API Retries |

---

## Database Schema

### SQLite Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Resumes Table
CREATE TABLE resumes (
    id INTEGER PRIMARY KEY,
    candidate_name TEXT NOT NULL,
    original_filename TEXT,
    extracted_text TEXT,
    skills TEXT,  -- JSON array
    years_experience REAL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Questions Table
CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    job_role TEXT NOT NULL,
    question_type TEXT,  -- "technical", "behavioral", "scenario"
    question_text TEXT NOT NULL,
    options TEXT,  -- JSON for MCQ
    expected_answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Answers Table
CREATE TABLE answers (
    id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    candidate_name TEXT NOT NULL,
    answer_text TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Evaluations Table
CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY,
    candidate_name TEXT NOT NULL,
    question_id INTEGER NOT NULL,
    score REAL,  -- 0-10
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Learning Roadmaps Table
CREATE TABLE learning_roadmaps (
    id INTEGER PRIMARY KEY,
    candidate_name TEXT NOT NULL,
    skill_gap TEXT,  -- JSON array
    roadmap LONGTEXT,  -- Detailed learning plan
    estimated_duration TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Security Implementation

### Authentication & Authorization

**JWT Token Strategy:**
- Token Expiration: 24 hours
- Algorithm: HS256
- Secret Key: Stored in environment variables
- Token Structure:
  ```
  Header: {alg: "HS256", typ: "JWT"}
  Payload: {sub: username, exp: timestamp, iat: timestamp}
  Signature: HMAC-SHA256
  ```

**API Protection:**
```python
@app.post("/endpoint")
async def protected_endpoint(
    current_user: dict = Depends(get_current_user)
):
    # Only authenticated users can access
    pass
```

### CORS Configuration
- **Allowed Origins:** All ("*")
- **Allowed Methods:** GET, POST, PUT, DELETE
- **Allowed Headers:** All
- **Credentials:** Enabled

### Data Security
- ✅ Input validation using Pydantic
- ✅ SQL parameterization (SQLAlchemy ORM)
- ✅ JWT-based session management
- ✅ Environment variable secrets
- ✅ HTTPS ready deployment

### Error Handling
- HTTP Status codes properly returned
- Sensitive information not exposed in errors
- Comprehensive logging for debugging
- Request/response validation

---

## Deployment Guide

### Prerequisites
```
Python 3.9+
pip or conda
Virtual environment
```

### Installation

1. **Clone repository**
   ```bash
   cd recruitment_ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Unix/Mac
   .venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key
   ```

5. **Run application**
   ```bash
   # Backend
   python start_server.py
   
   # Frontend (in new terminal)
   streamlit run frontend/streamlit_app.py
   ```

### Accessing Application
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Default Credentials
- Username: `admin`
- Password: `admin123`

---

## Performance Metrics

### Expected Performance

| Operation | Avg Time | Max Time |
|-----------|----------|----------|
| Resume Upload & Parse | 2-3s | 5s |
| Resume Analysis (1 resume) | 3-4s | 7s |
| Question Generation (10 Q) | 5-7s | 10s |
| Answer Evaluation (1 answer) | 2-3s | 5s |
| Learning Roadmap Generation | 4-5s | 8s |

### Scalability
- Supports 100+ concurrent users
- Handles 10GB+ vector embeddings
- Database: Indexed for fast queries
- API: Rate limiting available

---

## Troubleshooting

### Common Issues

**Issue: "ModuleNotFoundError: No module named 'app'"**
- Solution: Ensure running from correct directory with virtual environment activated

**Issue: OpenAI API Key Error**
- Solution: Verify API key in `.env` file and check OpenAI account status

**Issue: ChromaDB Connection Error**
- Solution: Check `chroma_data` directory permissions

**Issue: Port Already in Use**
- Solution: Kill process or use different port

---

## Future Enhancements

1. **Advanced ML Models:** Custom fine-tuned models for specific industries
2. **Multi-language Support:** Support for candidates worldwide
3. **Video Interview Analysis:** Integration with video recording platforms
4. **Bias Detection:** AI fairness and bias detection mechanisms
5. **Advanced Analytics:** Comprehensive hiring analytics dashboard
6. **Integration APIs:** Slack, Email, Calendar integrations
7. **Mobile App:** iOS/Android companion application

---

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- OpenAI API: https://openai.com/api/
- ChromaDB: https://www.trychroma.com/
- Streamlit: https://streamlit.io/
- SQLAlchemy: https://www.sqlalchemy.org/

---

**End of Technical Documentation**

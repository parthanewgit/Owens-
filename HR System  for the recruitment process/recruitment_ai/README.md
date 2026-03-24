# HR Requirement System

**Project by**: Parthasarathi Mishra and Prateek Anand

Complete **production-ready** multi-agent AI HR Requirement system with FastAPI backend, Streamlit UI, and CrewAI orchestration.

## Features

- **Resume Matching & Skill Gap Detection**: Analyzes resumes against job descriptions using embeddings
- **Interview Question Generation**: Generates technical, behavioral, and scenario-based questions
- **Answer Evaluation**: Scores and provides feedback on candidate answers
- **Personalized Learning Roadmap**: Creates 6-week skill development plans
- **REST APIs**: Fully async FastAPI endpoints with JWT authentication
- **Streamlit UI**: Professional dashboard for all recruitment functions
- **Vector Store**: ChromaDB for efficient resume searching
- **Structured Logging**: Comprehensive logging across all components

## Tech Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: OpenAI GPT-4o, CrewAI, ChromaDB, Embeddings
- **Frontend**: Streamlit
- **Database**: SQLAlchemy (SQLite default, PostgreSQL configurable)
- **Authentication**: JWT
- **Infrastructure**: Docker, Python-dotenv

## Project Structure

```
recruitment_ai/
├── app/
│   ├── agents/
│   │   ├── resume_agent.py
│   │   ├── question_agent.py
│   │   ├── evaluation_agent.py
│   │   └── learning_agent.py
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   ├── parser_service.py
│   │   ├── orchestration_service.py
│   │   └── auth_service.py
│   ├── models/
│   │   └── schemas.py
│   ├── core/
│   │   ├── config.py
│   │   └── logging_config.py
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Setup

### Prerequisites

- Python 3.11+
- OpenAI API Key
- pip or conda

### Local Installation

1. Clone and navigate to the project:
```bash
cd recruitment_ai
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API Key
```

5. Run FastAPI backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. In another terminal, run Streamlit frontend:
```bash
streamlit run frontend/streamlit_app.py
```

Access the UI at: `http://localhost:8501`

## Docker Setup

1. Build Docker image:
```bash
docker build -t recruitment-ai .
```

2. Create .env file with OpenAI API Key:
```bash
cp .env.example .env
# Edit .env
```

3. Run container:
```bash
docker run -p 8000:8000 --env-file .env recruitment-ai
```

## API Endpoints

### Authentication

**Login**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Resume Analysis

**Analyze Resumes**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "job_description=Senior Python Developer" \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.pdf"
```

Response:
```json
{
  "ranked_candidates": [
    {
      "name": "resume1.pdf",
      "similarity_score": 0.92,
      "matched_skills": ["Python", "FastAPI", "Docker"],
      "missing_skills": ["Kubernetes"]
    }
  ]
}
```

### Question Generation

**Generate Interview Questions**
```bash
curl -X POST http://localhost:8000/generate-questions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Python Developer with FastAPI experience"
  }'
```

Response:
```json
{
  "technical_questions": [
    "Explain async/await in Python?",
    "How do you handle middleware in FastAPI?"
  ],
  "behavioral_questions": [
    "Describe a challenging project you led"
  ],
  "scenario_questions": [
    "Handle a production outage"
  ]
}
```

### Answer Evaluation

**Evaluate Candidate Answer**
```bash
curl -X POST http://localhost:8000/evaluate-answer \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain async/await in Python?",
    "candidate_answer": "Async/await is used for asynchronous programming..."
  }'
```

Response:
```json
{
  "score": 8,
  "strengths": ["Good understanding", "Clear explanation"],
  "weaknesses": ["Missing concurrency details"],
  "improvement_suggestions": ["Study asyncio module deeper"]
}
```

### Learning Roadmap

**Generate Learning Plan**
```bash
curl -X POST http://localhost:8000/generate-learning-plan \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "missing_skills": ["Kubernetes", "AWS"]
  }'
```

Response:
```json
{
  "roadmap": {
    "week_1": {
      "topic": "Kubernetes Basics",
      "resources": ["official docs", "tutorials"],
      "mini_project": "Deploy app to k8s"
    },
    ...
  },
  "resources": ["Kubernetes documentation", "AWS console"],
  "mini_projects": ["Deploy microservices", "Setup load balancing"]
}
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Running Tests

```bash
pytest tests/test_api.py -v
```

## Configuration

Edit `.env` file to configure:

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: Database connection string (default: SQLite)
- `JWT_SECRET_KEY`: JWT signing key
- `ADMIN_USERNAME` / `ADMIN_PASSWORD`: Credentials
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## Agents

### 1. Resume Matching Agent
- Extracts skills from job description and resumes
- Generates embeddings for semantic matching
- Calculates cosine similarity scores
- Identifies matched and missing skills
- Ranks candidates by relevance

### 2. Question Generation Agent
- Analyzes job description
- Generates 5 technical questions
- Generates 3 behavioral questions
- Generates 2 scenario-based questions
- Uses GPT-4o with temperature 0.7

### 3. Answer Evaluation Agent
- Evaluates candidate answers to questions
- Scores 0-10
- Identifies strengths and weaknesses
- Provides improvement suggestions
- Uses GPT-4o with temperature 0.3

### 4. Learning Roadmap Agent
- Creates 6-week personalized learning plans
- Provides weekly topics and resources
- Suggests mini-projects for practice
- References industry resources
- Uses GPT-4o with temperature 0.6

## Performance

- Embedding caching for faster searches
- Async endpoints for concurrent requests
- Retry logic with exponential backoff
- Structured logging for monitoring
- Vector store optimization with ChromaDB

## Security

- JWT authentication on all endpoints
- Environment variable management
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- Error handling without exposing internals

## Notes

- Resume parsing supports: PDF, DOCX, TXT
- Requires valid OpenAI API key for LLM operations
- Vector store persists locally in `chroma_data/`
- Database persists locally as `recruitment.db`
- All logs written to `recruitment_ai.log`

## License

Proprietary - Recruitment AI System

# Recruitment AI System - Architecture Diagrams

## 1. COMPLETE SYSTEM ARCHITECTURE

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║                    RECRUITMENT AI SYSTEM - FULL ARCHITECTURE                 ║
║                                                                               ║
║  ┌─────────────────────────────────────────────────────────────────────────┐ ║
║  │                      🖥️ PRESENTATION LAYER (Frontend)                   │ ║
║  │                                                                           │ ║
║  │                    STREAMLIT WEB APPLICATION (Port 8501)                │ ║
║  │                                                                           │ ║
║  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐   │ ║
║  │  │   Login      │  │   Dashboard  │  │  Resume      │  │Questions │   │ ║
║  │  │   Page       │  │  (Main Hub)  │  │  Upload      │  │Generator │   │ ║
║  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘   │ ║
║  │                                                                           │ ║
║  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐   │ ║
║  │  │ Results      │  │  Evaluation  │  │  Learning    │  │ Analytics│   │ ║
║  │  │ Display      │  │  Interface   │  │  Paths       │  │Dashboard │   │ ║
║  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘   │ ║
║  │                                                                           │ ║
║  │                     HTTP/REST Protocol (JSON)                           │ ║
║  └──────────────────────────────┬──────────────────────────────────────────┘ ║
║                                 │                                            ║
║  ┌──────────────────────────────▼──────────────────────────────────────────┐ ║
║  │                      🔗 API GATEWAY LAYER (Backend)                      │ ║
║  │                                                                           │ ║
║  │                   FASTAPI Web Framework (Port 8000)                      │ ║
║  │                                                                           │ ║
║  │  ┌──────────────────────────────────────────────────────────────────┐  │ ║
║  │  │ MIDDLEWARE STACK                                                 │  │ ║
║  │  │ • CORS Handler        • Request Logger        • Error Handler   │  │ ║
║  │  │ • Authentication      • Response Formatter    • Rate Limiter    │  │ ║
║  │  └──────────────────────────────────────────────────────────────────┘  │ ║
║  │                                                                           │ ║
║  │  ┌──────────────────────────────────────────────────────────────────┐  │ ║
║  │  │ ROUTE HANDLERS / ENDPOINTS                                       │  │ ║
║  │  │ [POST] /login                    [POST] /analyze               │  │ ║
║  │  │ [POST] /generate_questions       [POST] /evaluate             │  │ ║
║  │  │ [POST] /learning_roadmap         [GET]  /docs                │  │ ║
║  │  └──────────────────────────────────────────────────────────────────┘  │ ║
║  │                                                                           │ ║
║  └──────────────────────────┬──────────────────────────────────────────────┘ ║
║                             │                                               ║
║  ┌──────────────────────────┴──────────────────────────────────────────────┐ ║
║  │                    ⚙️ SERVICE LAYER (Business Logic)                    │ ║
║  │                                                                           │ ║
║  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │ ║
║  │  │ ORCHESTRATION   │  │ AUTHENTICATION  │  │ DOCUMENT        │       │ ║
║  │  │ SERVICE         │  │ SERVICE         │  │ PARSING SERVICE │       │ ║
║  │  │                 │  │                 │  │                 │       │ ║
║  │  │ Workflow        │  │ • JWT Generation│  │ • PDF Parsing   │       │ ║
║  │  │ Coordination    │  │ • Token Valid   │  │ • DOCX Parsing  │       │ ║
║  │  │ Agent Routing   │  │ • Credentials   │  │ • Text Extrac   │       │ ║
║  │  │ Process Flow    │  │   Verification  │  │ • Content Clean │       │ ║
║  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │ ║
║  │                                                                           │ ║
║  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │ ║
║  │  │ EMBEDDING       │  │ LLM             │  │ VECTOR          │       │ ║
║  │  │ SERVICE         │  │ SERVICE         │  │ SEARCH SERVICE  │       │ ║
║  │  │                 │  │                 │  │                 │       │ ║
║  │  │ • Ada Model     │  │ • GPT-4o        │  │ • ChromaDB      │       │ ║
║  │  │ • Vector Gen    │  │ • Prompt Eng    │  │   Integration   │       │ ║
║  │  │ • Dimensions    │  │ • Max Tokens    │  │ • Semantic      │       │ ║
║  │  │   (1536D)       │  │ • Temperature   │  │   Matching      │       │ ║
║  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │ ║
║  │                                                                           │ ║
║  └──────────────────────────┬──────────────────────────────────────────────┘ ║
║                             │                                               ║
║  ┌──────────────────────────┴──────────────────────────────────────────────┐ ║
║  │                   🤖 AI AGENTS LAYER (Intelligence)                     │ ║
║  │                                                                           │ ║
║  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐    │ ║
║  │  │  RESUME AGENT    │  │  QUESTION AGENT  │  │  EVALUATION AGENT│    │ ║
║  │  │                  │  │                  │  │                  │    │ ║
║  │  │ • Skill Extract  │  │ • Tech Questions │  │ • MCQ Scoring    │    │ ║
║  │  │ • Matching       │  │ • Behavior Q's   │  │ • Text Analysis  │    │ ║
║  │  │ • Ranking        │  │ • Scenario Q's   │  │ • Feedback Gen   │    │ ║
║  │  │ • Gap Analysis   │  │ • Format Output  │  │ • Metrics Calc   │    │ ║
║  │  └──────────────────┘  └──────────────────┘  └──────────────────┘    │ ║
║  │                                                                           │ ║
║  │  ┌──────────────────┐                                                   │ ║
║  │  │ LEARNING AGENT   │                                                   │ ║
║  │  │                  │                                                   │ ║
║  │  │ • Gap Analysis   │                                                   │ ║
║  │  │ • Path Creation  │                                                   │ ║
║  │  │ • Resource Rec   │                                                   │ ║
║  │  │ • Timeline Est   │                                                   │ ║
║  │  └──────────────────┘                                                   │ ║
║  │                                                                           │ ║
║  └──────────────────────────┬──────────────────────────────────────────────┘ ║
║                             │                                               ║
║  ┌──────────────────────────┴──────────────────────────────────────────────┐ ║
║  │               🧠 EXTERNAL AI & INTELLIGENCE LAYER                       │ ║
║  │                                                                           │ ║
║  │  ┌────────────────────────────────────────────────────────────────────┐ │ ║
║  │  │               OPENAI SERVICES (Cloud-based)                          │ │ ║
║  │  │                                                                      │ │ ║
║  │  │  GPT-4o Model                    Ada Embeddings Model              │ │ ║
║  │  │  ├─ NLP Processing        ├─ Text to Vectors (1536D)             │ │ ║
║  │  │  ├─ Text Generation       ├─ Semantic Representation             │ │ ║
║  │  │  ├─ Comprehension         ├─ Similarity Computation              │ │ ║
║  │  │  └─ Scoring Logic         └─ Context Understanding               │ │ ║
║  │  │                                                                      │ │ ║
║  │  └────────────────────────────────────────────────────────────────────┘ │ ║
║  │                                                                           │ ║
║  └──────────────────────────┬──────────────────────────────────────────────┘ ║
║                             │                                               ║
║  ┌──────────────────────────┴──────────────────────────────────────────────┐ ║
║  │                  💾 DATA PERSISTENCE LAYER (Storage)                     │ ║
║  │                                                                           │ ║
║  │  ┌────────────────────────┐         ┌────────────────────────┐        │ ║
║  │  │      SQLITE DB         │         │     CHROMADB           │        │ ║
║  │  │  (Relational Storage)  │         │ (Vector DB Storage)    │        │ ║
║  │  │                        │         │                        │        │ ║
║  │  │ Tables:                │         │ Collections:           │        │ ║
║  │  │ • users                │         │ • resume_embeddings    │        │ ║
║  │  │ • resumes              │         │ • question_embeddings  │        │ ║
║  │  │ • questions            │         │ • semantic_indices     │        │ ║
║  │  │ • answers              │         │                        │        │ ║
║  │  │ • evaluations          │         │ Features:              │        │ ║
║  │  │ • learning_roadmaps    │         │ • Vector Search        │        │ ║
║  │  │ • audit_logs           │         │ • Similarity Matching  │        │ ║
║  │  │                        │         │ • Persistent Storage   │        │ ║
║  │  └────────────────────────┘         └────────────────────────┘        │ ║
║  │        (File: recruitment.db)       (Folder: chroma_data)             │ ║
║  │                                                                           │ ║
║  └──────────────────────────────────────────────────────────────────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

---

## 2. DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

STEP 1: AUTHENTICATION
───────────────────────
   User Input                     Backend Processing              Response
   │                              │                              │
   └─→ [Login Credentials]        │                              │
         (username/password)      │                              │
                                  ├─→ AuthService.verify()       │
                                  │   ├─ Query users DB         │
                                  │   ├─ Hash comparison        │
                                  │   └─ JWT generation         │
                                  │                              │
                                  │                         ←─────│─ JWT Token
                                  │                              │
                                  │            Store in Session  │
                                  │                              ↓
   Display Dashboard             Ready for Protected Requests


STEP 2: RESUME ANALYSIS WORKFLOW
─────────────────────────────────
   User Upload                    Backend Processing              Data Storage
   │                              │                              │
   ├─→ [Job Description]          │                              │
   │                              ├─→ ParserService             │
   └─→ [Resume Files (PDF/DOCX)]  │   ├─ Parse documents        │
                                  │   └─ Extract text            │
                                  │                              │
                                  ├─→ ResumeAgent               │
                                  │   ├─ NLP skill extraction    │
                                  │   ├─ Embedding creation      ├─→ Store in ChromaDB
                                  │   ├─ Semantic matching       │   ├─ Vectors
                                  │   └─ Ranking algorithm       │   └─ Metadata
                                  │                              │
                                  ├─→ SQLite Update             │
                                  │   ├─ Save resume data        │
                                  │   └─ Store rankings          ├─→ Store in SQLite
                                  │                              │   ├─ Skills
                                  │                              │   └─ Scores
                                  │
                                  ├─→ Response Generation       │
                                  │   ├─ Format results          │
                                  │   └─ Create JSON            │
                                  │                              ↓
   Display Ranked Results        Results Ready             Database Updated


STEP 3: QUESTION GENERATION WORKFLOW
─────────────────────────────────────
   User Request                   Backend Processing              Database
   │                              │                              │
   └─→ [Job Description]          │                              │
       [Question Params]          ├─→ QuestionAgent             │
                                  │   ├─ LLM prompt creation    │
                                  │   ├─ Call GPT-4o            ├─→ Store Questions
                                  │   └─ Format questions       │   ├─ Technical Q's
                                  │                              │   ├─ Behavioral Q's
                                  ├─→ SQLite Insert            │   └─ Scenario Q's
                                  │   └─ Save all questions     │
                                  │                              │
                                  ├─→ Response Generation       │
                                  │   └─ Format for frontend    │
                                  │                              ↓
   Display Questions             Questions Ready           Stored & Indexed


STEP 4: ANSWER EVALUATION WORKFLOW
──────────────────────────────────
   User Submission               Backend Processing              Results Storage
   │                              │                              │
   ├─→ [Answer 1 (MCQ)]          │                              │
   ├─→ [Answer 2 (Freetext)]     ├─→ EvaluationAgent          │
   └─→ [Answer N (Mixed)]        │   ├─ MCQ: Instant grade     │
                                  │   ├─ Text: LLM analysis     │
                                  │   ├─ Score calculation      │
                                  │   └─ Feedback generation    ├─→ Store Results
                                  │                              │   ├─ Scores
                                  ├─→ SQLite Update            │   ├─ Feedback
                                  │   ├─ Save answers          │   └─ Analytics
                                  │   ├─ Save evaluations      │
                                  │   └─ Update metrics        │
                                  │                              │
                                  ├─→ Response Generation       │
                                  │   ├─ Aggregate scores       │
                                  │   └─ Format results         │
                                  │                              ↓
   Display Score & Feedback      Evaluation Complete      Metrics Calculated


STEP 5: LEARNING ROADMAP GENERATION
────────────────────────────────────
   Trigger                       Backend Processing              Roadmap Storage
   │                              │                              │
   └─→ [Evaluation Results]       │                              │
       [Skill Gaps]              ├─→ LearningAgent             │
                                  │   ├─ Gap analysis          │
                                  │   ├─ LLM path creation     │
                                  │   ├─ Resource mapping      │
                                  │   └─ Timeline estimation   ├─→ Store Roadmap
                                  │                              │   ├─ Gaps
                                  ├─→ SQLite Insert            │   ├─ Plan
                                  │   └─ Save roadmap          │   └─ Timeline
                                  │                              │
                                  ├─→ Response Generation       │
                                  │   └─ Format learning path   │
                                  │                              ↓
   Display Learning Path         Roadmap Ready            Personalized Plan Saved
```

---

## 3. AGENT INTERACTION DIAGRAM

```
                        ┌─────────────────────────────┐
                        │  ORCHESTRATION SERVICE      │
                        │  (Central Coordinator)      │
                        └────────────┬────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
    ┌─────────────────┐   ┌──────────────────┐   ┌──────────────────┐
    │  RESUME AGENT   │   │ QUESTION AGENT   │   │ EVALUATION AGENT │
    └────────┬────────┘   └────────┬─────────┘   └────────┬─────────┘
             │                     │                      │
             │                     │                      │
    ┌────────▼──────────┐  ┌──────▼────────┐    ┌────────▼──────────┐
    │  Skill Extraction │  │  Question     │    │  Answer Scoring   │
    │  Module           │  │  Generation   │    │  Module           │
    │  ├─ NLP Pipeline  │  │  Module       │    │  ├─ MCQ Scoring   │
    │  ├─ Entity Ext    │  │  ├─ Prompts   │    │  ├─ Text Analysis │
    │  └─ Skill List    │  │  ├─ Multi-QA  │    │  ├─ Semantics     │
    │                   │  │  └─ Format    │    │  └─ Grading       │
    └────────┬──────────┘  └──────┬────────┘    └────────┬──────────┘
             │                     │                      │
             │                     │                      │
    ┌────────▼──────────┐  ┌──────▼────────┐    ┌────────▼──────────┐
    │  Matching Module  │  │  Output Format │    │  Feedback Gen     │
    │  ├─ Embeddings    │  │  Module        │    │  Module           │
    │  ├─ Similarity    │  │  ├─ JSON       │    │  ├─ Insights      │
    │  └─ Ranking       │  │  ├─ Validation │    │  ├─ Suggestions   │
    │                   │  │  └─ Serialize  │    │  └─ Format        │
    └────────┬──────────┘  └──────┬────────┘    └────────┬──────────┘
             │                     │                      │
             └─────────────────────┼──────────────────────┘
                                   │
                        ┌──────────▼──────────┐
                        │  LEARNING AGENT    │
                        │  (Optional Fourth)  │
                        └──────────┬──────────┘
                                   │
                        ┌──────────▼──────────┐
                        │  Gap Analysis      │
                        │  Path Creation     │
                        │  Resource Mapping  │
                        └────────────────────┘
```

---

## 4. API REQUEST/RESPONSE CYCLE

```
CLIENT REQUEST                    SERVER PROCESSING              DATABASE OPERATIONS
─────────────────────────────────────────────────────────────────────────────────────

1. LOGIN ENDPOINT
────────────────
POST /login
├─ Content-Type: application/json
├─ Body: {
│   "username": "admin",
│   "password": "admin123"
│ }
│
└──────────────────────────────────────────────────────────────────────────────────────┐
                                                                                       │
                        ┌──────────────────────────────────────────┐                 │
                        │ FastAPI Router: POST /login              │                 │
                        ├──────────────────────────────────────────┤                 │
                        │ 1. Receive request                       │                 │
                        │ 2. Validate JSON schema                 │                 │
                        │ 3. Call AuthService.verify_credentials()│ ──────────┐    │
                        │ 4. Generate JWT token                   │           │    │
                        │ 5. Return TokenResponse                 │           │    │
                        └──────────────────────────────────────────┘           │    │
                                                                               │    │
                                                               ┌───────────────▼──┐ │
                                                               │ SQLite: users    │ │
                                                               ├──────────────────┤ │
                                                               │ Query:           │ │
                                                               │ SELECT * FROM    │ │
                                                               │ users WHERE      │ │
                                                               │ username='admin' │ │
                                                               │                  │ │
                                                               │ Result:          │ │
                                                               │ {id:1, pwd_hash} │ │
                                                               └──────────────────┘ │
                                                                                  │
Response: 200 OK                                                                 │
├─ Content-Type: application/json                                               │
├─ Body: {                                                                      │
│   "access_token": "eyJhbGciOiJIUzI1NiIsInR5c...",                           │
│   "token_type": "bearer"                                                      │
│ } ◄─────────────────────────────────────────────────────────────────────────┘


2. ANALYZE ENDPOINT (with Authorization)
─────────────────────────────────────────
POST /analyze
├─ Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5c...
├─ Content-Type: multipart/form-data
├─ Body:
│   ├─ job_description: "Python developer needed..."
│   └─ resumes: [file1.pdf, file2.pdf]
│
└──────────────────────────────────────────────────────────────────────────────────────┐
                                                                                       │
                        ┌──────────────────────────────────────────┐                 │
                        │ FastAPI Router: POST /analyze            │                 │
                        ├──────────────────────────────────────────┤                 │
                        │ 1. Validate JWT token                    │                 │
                        │ 2. Verify file types                     │                 │
                        │ 3. Call ParserService                    │ ──────────┐    │
                        │ 4. Call ResumeAgent.match_resumes()     │           │    │
                        │ 5. Format response                       │           │    │
                        └──────────────────────────────────────────┘           │    │
                                                                               │    │
                                                          ┌────────────────────┴──┐ │
                              ┌───────────────────────────▼──────────┐             │ │
                              │ ParserService                         │             │ │
                              ├───────────────────────────────────────┤             │ │
                              │ Parse PDF/DOCX files                 │             │ │
                              │ Extract text content                  │             │ │
                              │ Clean & normalize text                │             │ │
                              └───────────────────────────────────────┘             │ │
                                             │                                     │ │
                              ┌──────────────┴──────────────┐                     │ │
                              ▼                             ▼                     │ │
                     ┌──────────────────┐      ┌─────────────────────┐           │ │
                     │ ResumeAgent      │      │ OpenAI Embeddings   │           │ │
                     ├──────────────────┤      ├─────────────────────┤           │ │
                     │ NLP skill ext    │──────▶ Create vectors      │           │ │
                     │ Matching logic   │      │ Semantic search     │           │ │
                     │ Ranking algorithm│      │ Similarity compute  │           │ │
                     └──────────────────┘      └─────────────────────┘           │ │
                              │                                                   │ │
                              └──────────────────┬──────────────────┐            │ │
                                               │                   │            │ │
                                    ┌──────────▼────┐   ┌─────────▼──────┐     │ │
                                    │ SQLite: Store │   │ ChromaDB:      │     │ │
                                    │               │   │ Store Vectors  │     │ │
                                    │ • resumes     │   │                │     │ │
                                    │ • skills      │   │ • embeddings   │     │ │
                                    │ • scores      │   │ • metadata     │     │ │
                                    └───────────────┘   └────────────────┘     │ │
                                                                               │ │
Response: 200 OK                                                              │ │
├─ Content-Type: application/json                                            │ │
├─ Body: {                                                                   │ │
│   "ranked_candidates": [                                                   │ │
│     {                                                                       │ │
│       "name": "John Doe",                                                  │ │
│       "similarity_score": 0.92,                                            │ │
│       "matched_skills": ["Python", "FastAPI", "PostgreSQL"],               │ │
│       "missing_skills": ["Kubernetes"],                                    │ │
│       "total_jd_skills": 8                                                 │ │
│     }                                                                       │ │
│   ]                                                                         │ │
│ } ◄──────────────────────────────────────────────────────────────────────┘ │
                                                                              │
                                                             ┘
```

---

## 5. AUTHENTICATION & SECURITY FLOW

```
AUTHENTICATION FLOW
═════════════════════════════════════════════════════════════════════════════

Step 1: User Login
   ┌──────────────────────────────────────┐
   │ User enters: admin / admin123        │
   │ Submits to: POST /login              │
   └──────────────────┬───────────────────┘
                      │
Step 2: Credential Validation
   ┌──────────────────▼───────────────────┐
   │ AuthService.verify_credentials()     │
   ├────────────────────────────────────────┤
   │ • Query SQLite users table           │
   │ • Retrieve password hash             │
   │ • Compare hash with provided password│
   │ • Return True/False                  │
   └──────────────────┬───────────────────┘
                      │
                 ┌────┴────┐
                 │          │
            ✓ Valid    ✗ Invalid
                 │          │
                 │          └─── Return 401 Unauthorized
                 │
Step 3: JWT Token Generation
   ┌──────────────────▼───────────────────┐
   │ AuthService.create_access_token()    │
   ├────────────────────────────────────────┤
   │ Create JWT Payload:                  │
   │ {                                    │
   │   "sub": "admin",                    │
   │   "exp": future_timestamp,           │
   │   "iat": current_timestamp           │
   │ }                                    │
   │                                      │
   │ Sign with HS256:                     │
   │ signature = HMAC-SHA256(             │
   │   payload,                           │
   │   JWT_SECRET_KEY                     │
   │ )                                    │
   │                                      │
   │ Final Token: Header.Payload.Signature│
   └──────────────────┬───────────────────┘
                      │
Step 4: Return Token to Client
   ┌──────────────────▼───────────────────┐
   │ Response: 200 OK                     │
   │ {                                    │
   │   "access_token": "JWT_STRING",      │
   │   "token_type": "bearer"             │
   │ }                                    │
   │                                      │
   │ Client stores token in session       │
   └──────────────────────────────────────┘


PROTECTED ENDPOINT ACCESS
═════════════════════════════════════════════════════════════════════════════

Step 1: Client Request with Token
   ┌────────────────────────────────────────┐
   │ Header: Authorization: Bearer JWT_STR  │
   │ POST /analyze                          │
   │ Body: { job_description, resumes }     │
   └────────────────┬───────────────────────┘
                    │
Step 2: Middleware Intercepts
   ┌────────────────▼────────────────────┐
   │ FastAPI Middleware                  │
   ├──────────────────────────────────────┤
   │ 1. Extract Authorization header      │
   │ 2. Parse "Bearer <token>"            │
   │ 3. Validate token format             │
   │ 4. Call get_current_user()           │
   └────────────────┬────────────────────┘
                    │
Step 3: Token Verification
   ┌────────────────▼────────────────────┐
   │ AuthService.verify_token()           │
   ├──────────────────────────────────────┤
   │ • Decode JWT with secret key         │
   │ • Verify signature                   │
   │ • Check expiration (exp < now)       │
   │ • Extract username from payload      │
   └────────────────┬────────────────────┘
                    │
               ┌────┴─────┐
               │           │
           ✓ Valid   ✗ Invalid/Expired
               │           │
               │           └── Return 403 Forbidden
               │
Step 4: Process Authenticated Request
   ┌────────────────▼────────────────────┐
   │ Route Handler (now has user info)    │
   │ • Execute business logic             │
   │ • Access protected resources         │
   │ • Return response                    │
   └────────────────┬────────────────────┘
                    │
Step 5: Send Response
   ┌────────────────▼────────────────────┐
   │ Response: 200 OK                     │
   │ Content: Analysis results            │
   └────────────────────────────────────┘
```

---

## 6. VECTOR EMBEDDING & SEMANTIC SEARCH

```
TEXT-TO-VECTOR TRANSFORMATION
═════════════════════════════════════════════════════════════════════════════

Input Text                OpenAI Ada                Output Vector
|                         Embedding Model           |
|                         |                         |
| "Python backend         ├─ Tokenization ──────────┤
|  developer with SQL     │  (Break into tokens)    |
|  expertise required"    │                         ├─ 1536-dimensional
|                         ├─ Encoding ──────────────┤  vector space
|                         │  (Convert to numbers)   |
|                         │                         ├─ [0.145, -0.203,
|                         ├─ Normalization ────────┤  0.512, ..., 0.089]
|                         │  (Scale to range)      |
└─────────────────────────┘                         └─────────────────────


SEMANTIC MATCHING PROCESS
═════════════════════════════════════════════════════════════════════════════

Resume Text                              Job Description
|                                        |
├─ Embedded to Vector 1                 ├─ Embedded to Vector 2
│  (Resume Embedding)                    │  (JD Embedding)
│  [0.145, -0.203, 0.512, ...]        │  [0.198, -0.156, 0.478, ...]
│                                        │
└─────────────────────────────────────────────────────────────┐
                                                              │
                                    ┌─────────────────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │ Cosine Similarity Function   │
                    ├──────────────────────────────┤
                    │ cos(θ) = (A · B) / (|A| × |B|)
                    │                              │
                    │ Result: -1.0 to +1.0         │
                    │ Scale: 0% to 100%            │
                    └──────────────────┬───────────┘
                                       │
                                       ▼
                    ┌──────────────────────────────┐
                    │ Similarity Score: 0.92 (92%) │
                    └──────────────────────────────┘

ChromaDB Vector Store:
├─ Resume 1 embedding + metadata → similarity 0.92
├─ Resume 2 embedding + metadata → similarity 0.87
├─ Resume 3 embedding + metadata → similarity 0.78
└─ [Sorted by score for ranking]


Vector SEARCH OPERATIONS
═════════════════════════════════════════════════════════════════════════════

Query: "Find resumes matching Python developer JD"
|
├─ Embed JD: [vector_1536]
│
├─ ChromaDB Query:
│  query_vector = [vector_1536]
│  top_k = 10  (return top 10 matches)
│
├─ Compute Similarities:
│  └─ All stored resume vectors × JD vector
│
├─ Sort by Score:
│  ├─ Resume A: 0.945
│  ├─ Resume B: 0.923
│  ├─ Resume C: 0.887
│  └─ ...
│
└── Return Top 10 Results
    └─ With scores, metadata, and embeddings
```

---

**END OF ARCHITECTURE DIAGRAMS**

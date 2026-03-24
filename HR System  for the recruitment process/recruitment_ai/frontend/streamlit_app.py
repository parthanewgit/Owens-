import streamlit as st
import requests
import json
from typing import Optional
import time
import os

# Get API URL from environment or use default
BASE_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="HR Requirement System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header with title and authors
col1, col2 = st.columns([1, 1])
with col1:
    st.title("🚀 HR Requirement System")
with col2:
    st.markdown(
        """
        <div style="text-align: right; margin-top: 15px;">
            <p style="margin: 0; font-size: 14px;"><b>Project by</b></p>
            <p style="margin: 0; font-size: 13px;color: green;"><b>Parthasarathi Mishra</p>
            <p style="margin: 0; font-size: 13px;color: green;"><b>Prateek Anand</b></p>
        </div>
        """,
        unsafe_allow_html=True
    )
st.markdown("---")

def get_auth_header():
    """Get authorization header"""
    if "token" in st.session_state:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}

def login_form():
    """Render login form"""
    st.subheader("Login")
    
    username = st.text_input("Username", value="admin")
    password = st.text_input("Password", type="password", value="admin123")
    
    if st.button("Login", key="login_btn"):
        try:
            response = requests.post(
                f"{BASE_URL}/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.token = data["access_token"]
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
        except Exception as e:
            st.error(f"Login error: {e}")

def analyze_candidates_section():
    """Render resume analysis section"""
    st.subheader("📄 Resume Matching & Analysis")
    
    with st.form("analysis_form"):
        job_description = st.text_area(
            "Job Description",
            height=150,
            placeholder="Paste job description here..."
        )
        
        resume_files = st.file_uploader(
            "Upload Resumes",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True
        )
        
        submit_analysis = st.form_submit_button("Analyze Resumes")
    
    if submit_analysis:
        if not job_description:
            st.error("Please enter job description")
            return
        
        if not resume_files:
            st.error("Please upload at least one resume")
            return
        
        with st.spinner("Analyzing resumes..."):
            try:
                files = [
                    ("resumes", (file.name, file.getvalue(), file.type))
                    for file in resume_files
                ]
                
                response = requests.post(
                    f"{BASE_URL}/analyze",
                    data={"job_description": job_description},
                    files=files,
                    headers=get_auth_header()
                )
                
                if response.status_code == 200:
                    results = response.json()
                    st.session_state.analysis_results = results
                    st.session_state.analysis_job_description = job_description
                    st.success("Analysis complete!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error analyzing resumes: {e}")
    
    if "analysis_results" in st.session_state:
        st.markdown("### Results")
        
        candidates = st.session_state.analysis_results.get("ranked_candidates", [])
        
        if candidates:
            for idx, candidate in enumerate(candidates, 1):
                skill_score = candidate.get('skill_match_score', 0)
                semantic_score = candidate.get('semantic_similarity', 0)
                combined_score = candidate.get('similarity_score', 0)
                
                with st.expander(f"{idx}. {candidate['name']} (Overall Score: {combined_score:.2%})"):
                    # Score breakdown
                    st.write("**Score Breakdown:**")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Skill Match", f"{skill_score:.1%}", 
                                help=f"Matched {len(candidate.get('matched_skills', []))} out of {candidate.get('total_jd_skills', 0)} required skills")
                    
                    with col2:
                        st.metric("Semantic Similarity", f"{semantic_score:.1%}",
                                help="Content relevance based on AI analysis")
                    
                    with col3:
                        st.metric("Combined Score", f"{combined_score:.1%}",
                                help="70% skill match + 30% semantic similarity")
                    
                    # Skills section
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Matched Skills:**")
                        matched = candidate.get("matched_skills", [])
                        if matched:
                            for skill in matched:
                                st.write(f"✓ {skill}")
                        else:
                            st.write("*No skills matched*")
                    
                    with col2:
                        st.write("**Missing Skills:**")
                        missing = candidate.get("missing_skills", [])
                        if missing:
                            for skill in missing:
                                st.write(f"✗ {skill}")
                        else:
                            st.write("*All required skills present*")

def generate_questions_section():
    """Render question generation section"""
    st.subheader("❓ Interview Question Generation")
    
    # Get available candidates from analysis
    candidates_list = []
    analysis_jd = st.session_state.get("analysis_job_description", "")
    
    if "analysis_results" in st.session_state:
        candidates_list = st.session_state.analysis_results.get("ranked_candidates", [])
    
    with st.form("questions_form"):
        # Candidate selection
        if candidates_list:
            candidate_names = [c['name'] for c in candidates_list]
            candidate_names = [name.replace('.pdf', '').replace('.docx', '').replace('.txt', '') for name in candidate_names]
            selected_candidate = st.selectbox(
                "Select Candidate",
                candidate_names,
                key="candidate_select"
            )
        else:
            st.info("⚠️ No candidates available. Please analyze resumes first.")
            selected_candidate = None
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            num_technical = st.number_input("Technical Questions", min_value=1, max_value=10, value=5)
        with col2:
            num_behavioral = st.number_input("Behavioral Questions", min_value=1, max_value=10, value=3)
        with col3:
            num_scenario = st.number_input("Scenario Questions", min_value=1, max_value=10, value=2)
        
        submit_questions = st.form_submit_button("Generate Questions")
    
    if submit_questions:
        if not analysis_jd:
            st.error("Please analyze resumes first to get job description")
            return
        
        if not selected_candidate and candidates_list:
            st.error("Please select a candidate")
            return
        
        with st.spinner("Generating questions..."):
            try:
                response = requests.post(
                    f"{BASE_URL}/generate-questions",
                    json={
                        "job_description": analysis_jd,
                        "num_technical": num_technical,
                        "num_behavioral": num_behavioral,
                        "num_scenario": num_scenario
                    },
                    headers=get_auth_header()
                )
                
                if response.status_code == 200:
                    questions = response.json()
                    st.session_state.generated_questions = questions
                    st.session_state.selected_candidate_name = selected_candidate
                    st.session_state.job_description = analysis_jd
                    st.success("Questions generated!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error generating questions: {e}")
    
    if "generated_questions" in st.session_state:
        questions = st.session_state.generated_questions
        candidate_name = st.session_state.get("selected_candidate_name", "Candidate")
        
        st.divider()
        st.markdown(f"### 👤 Questions for: **{candidate_name}**")
        
        st.markdown("#### 📌 Technical Questions")
        for i, q in enumerate(questions.get("technical_questions", []), 1):
            if q.get("type") == "mcq":
                with st.expander(f"{i}. [MCQ] {q['question']}", expanded=False):
                    st.markdown("**Options:**")
                    for option_key in ['A', 'B', 'C', 'D']:
                        option_text = q['options'].get(option_key, '')
                        correct_marker = " ✓ (Correct)" if q['correct_answer'] == option_key else ""
                        st.write(f"**{option_key}.** {option_text}{correct_marker}")
            else:
                with st.expander(f"{i}. [Free Text] {q['question']}", expanded=False):
                    st.markdown("**Expected Answer:**")
                    st.write(q.get('expected_answer', ''))
        
        st.markdown("#### 💡 Behavioral Questions")
        for i, q in enumerate(questions.get("behavioral_questions", []), 1):
            if q.get("type") == "mcq":
                with st.expander(f"{i}. [MCQ] {q['question']}", expanded=False):
                    st.markdown("**Options:**")
                    for option_key in ['A', 'B', 'C', 'D']:
                        option_text = q['options'].get(option_key, '')
                        correct_marker = " ✓ (Correct)" if q['correct_answer'] == option_key else ""
                        st.write(f"**{option_key}.** {option_text}{correct_marker}")
            else:
                with st.expander(f"{i}. [Free Text] {q['question']}", expanded=False):
                    st.markdown("**Expected Answer:**")
                    st.write(q.get('expected_answer', ''))
        
        st.markdown("#### 🎯 Scenario Questions")
        for i, q in enumerate(questions.get("scenario_questions", []), 1):
            if q.get("type") == "mcq":
                with st.expander(f"{i}. [MCQ] {q['question']}", expanded=False):
                    st.markdown("**Options:**")
                    for option_key in ['A', 'B', 'C', 'D']:
                        option_text = q['options'].get(option_key, '')
                        correct_marker = " ✓ (Correct)" if q['correct_answer'] == option_key else ""
                        st.write(f"**{option_key}.** {option_text}{correct_marker}")
            else:
                with st.expander(f"{i}. [Free Text] {q['question']}", expanded=False):
                    st.markdown("**Expected Answer:**")
                    st.write(q.get('expected_answer', ''))

def evaluate_answers_section():
    """Render answer evaluation section with all questions"""
    st.subheader("📊 Answer Evaluation")
    
    # Check if questions are generated
    if "generated_questions" not in st.session_state:
        st.warning("⚠️ Please generate questions first in the 'Generate Questions' section")
        return
    
    # Get candidate name and JD
    candidate_name = st.session_state.get("selected_candidate_name", "Candidate")
    job_description = st.session_state.get("job_description", "")
    questions_data = st.session_state.generated_questions
    
    # Display JD
    if job_description:
        with st.expander("📋 Job Description (Auto-loaded)", expanded=False):
            st.write(job_description)
    
    st.markdown(f"### 👤 Candidate: **{candidate_name}**")
    st.markdown("---")
    
    # Prepare all questions
    all_questions = []
    
    # Add technical questions
    for i, q in enumerate(questions_data.get("technical_questions", [])):
        q['global_index'] = len(all_questions)
        q['category'] = "Technical"
        all_questions.append(q)
    
    # Add behavioral questions
    for i, q in enumerate(questions_data.get("behavioral_questions", [])):
        q['global_index'] = len(all_questions)
        q['category'] = "Behavioral"
        all_questions.append(q)
    
    # Add scenario questions
    for i, q in enumerate(questions_data.get("scenario_questions", [])):
        q['global_index'] = len(all_questions)
        q['category'] = "Scenario"
        all_questions.append(q)
    
    # Initialize session state for answers if needed
    if "candidate_answers" not in st.session_state:
        st.session_state.candidate_answers = {}
    
    # Display all questions and collect answers
    st.markdown("### 📝 Answer All Questions")
    
    with st.form("all_answers_form"):
        for idx, question in enumerate(all_questions):
            st.divider()
            
            # Question display
            question_type_label = f"[{question['type'].upper()}]" if question['type'] == 'mcq' else ""
            st.markdown(f"**Q{idx+1}. {question_type_label} {question['question']}**".strip())
            
            if question['type'] == 'mcq':
                # Display MCQ options
                st.markdown("**Options:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**A.** {question['options'].get('A', '')}")
                    st.write(f"**C.** {question['options'].get('C', '')}")
                with col2:
                    st.write(f"**B.** {question['options'].get('B', '')}")
                    st.write(f"**D.** {question['options'].get('D', '')}")
                
                # MCQ answer selection
                mcq_answer = st.radio(
                    "Select your answer:",
                    options=['A', 'B', 'C', 'D'],
                    label_visibility="collapsed",
                    key=f"mcq_answer_{idx}"
                )
                st.session_state.candidate_answers[idx] = {
                    'type': 'mcq',
                    'answer': mcq_answer,
                    'question': question['question'],
                    'correct_answer': question.get('correct_answer', '')
                }
            else:
                # Free text question
                free_text_answer = st.text_area(
                    "Your Answer:",
                    placeholder="Write your detailed answer here...",
                    key=f"freetext_answer_{idx}",
                    height=120
                )
                if free_text_answer:
                    st.session_state.candidate_answers[idx] = {
                        'type': 'freetext',
                        'answer': free_text_answer,
                        'question': question['question']
                    }
        
        st.divider()
        submit_all = st.form_submit_button("📊 Evaluate All Answers")
    
    if submit_all:
        # Validate that all questions are answered
        if len(st.session_state.candidate_answers) < len(all_questions):
            st.error("❌ Please answer all questions before evaluating")
            return
        
        st.info("✅ All answers collected. Evaluating responses...")
        
        # For now, we'll evaluate each answer individually
        # In a production system, you could batch evaluate
        with st.spinner("Evaluating answers..."):
            all_evaluations = []
            
            for idx, question in enumerate(all_questions):
                if idx in st.session_state.candidate_answers:
                    answer_data = st.session_state.candidate_answers[idx]
                    
                    try:
                        response = requests.post(
                            f"{BASE_URL}/evaluate-answer",
                            json={
                                "question": question['question'],
                                "candidate_answer": answer_data['answer'],
                                "mcq_answer": answer_data['answer'] if answer_data['type'] == 'mcq' else None,
                                "candidate_name": candidate_name,
                                "question_type": answer_data['type'],
                                "correct_answer": answer_data.get('correct_answer', None)
                            },
                            headers=get_auth_header()
                        )
                        
                        if response.status_code == 200:
                            evaluation = response.json()
                            evaluation['question_index'] = idx + 1
                            evaluation['question_text'] = question['question']
                            evaluation['question_type'] = question['type']
                            evaluation['category'] = question.get('category', 'General')
                            evaluation['user_answer'] = answer_data['answer']
                            all_evaluations.append(evaluation)
                    except Exception as e:
                        st.error(f"Error evaluating question {idx + 1}: {str(e)}")
            
            if all_evaluations:
                st.session_state.all_evaluations = all_evaluations
                st.success("✅ Evaluation complete!")
    
    # Display evaluations if available
    if "all_evaluations" in st.session_state:
        st.divider()
        st.markdown("## 📊 Evaluation Results")
        
        evaluations = st.session_state.all_evaluations
        
        # Calculate overall score
        total_score = sum(e.get('score', 0) for e in evaluations)
        average_score = total_score / len(evaluations) if evaluations else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Overall Score", f"{average_score:.1f}/10")
        with col2:
            st.metric("Total Questions", len(evaluations))
        with col3:
            st.metric("Avg Performance", f"{(average_score/10)*100:.0f}%")
        
        st.divider()
        
        # Display individual evaluations
        for eval_item in evaluations:
            with st.expander(
                f"Q{eval_item['question_index']}. [{eval_item['question_type'].upper()}] "
                f"Score: {eval_item.get('score', 0)}/10",
                expanded=False
            ):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"**Question:** {eval_item['question_text']}")
                    st.markdown(f"**Your Answer:** {eval_item['user_answer']}")
                    
                    score_bar = eval_item.get('score', 0) / 10
                    st.progress(score_bar, text=f"Score: {eval_item.get('score', 0)}/10")
                
                # Only show strengths/weaknesses for free text questions
                if eval_item['question_type'] == 'freetext':
                    with col2:
                        st.markdown("**✅ Strengths:**")
                        for strength in eval_item.get('strengths', []):
                            st.write(f"• {strength}")
                        
                        st.markdown("**⚠️ Weaknesses:**")
                        for weakness in eval_item.get('weaknesses', []):
                            st.write(f"• {weakness}")
                    
                    st.markdown("**💡 Improvement Suggestions:**")
                    for suggestion in eval_item.get('improvement_suggestions', []):
                        st.write(f"→ {suggestion}")
                else:
                    # MCQ question - show if answer is correct
                    is_correct = eval_item.get('score', 0) == 10
                    if is_correct:
                        st.success("✅ **Correct Answer!**")
                    else:
                        st.error("❌ **Incorrect Answer**")
                        if eval_item.get('expected_answer'):
                            st.markdown(f"**Correct Answer:** {eval_item['expected_answer']}")
                
                if eval_item.get('expected_answer') and eval_item['question_type'] == 'freetext':
                    st.markdown("**📚 Expected Answer / Key Points:**")
                    st.info(eval_item['expected_answer'])

def learning_roadmap_section():
    """Render learning roadmap section"""
    st.subheader("📚 Learning Roadmap Generator")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        skills_input = st.text_input(
            "Missing Skills (comma-separated)",
            placeholder="Python, Machine Learning, FastAPI, Docker..."
        )
    
    with col2:
        generate_roadmap = st.button("Generate Roadmap", key="roadmap_btn")
    
    if generate_roadmap:
        if not skills_input:
            st.error("Please enter at least one skill")
            return
        
        skills = [s.strip() for s in skills_input.split(",")]
        
        with st.spinner("Generating learning roadmap..."):
            try:
                response = requests.post(
                    f"{BASE_URL}/generate-learning-plan",
                    json={"missing_skills": skills},
                    headers=get_auth_header()
                )
                
                if response.status_code == 200:
                    roadmap = response.json()
                    st.session_state.roadmap = roadmap
                    st.success("Roadmap generated!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Error generating roadmap: {e}")
    
    if "roadmap" in st.session_state:
        roadmap = st.session_state.roadmap
        
        st.markdown("### 6-Week Learning Roadmap")
        
        for week_key, week_data in roadmap.get("roadmap", {}).items():
            with st.expander(f"**{week_key.replace('_', ' ').title()}**: {week_data.get('topic', '')}"):
                st.markdown("**Resources:**")
                for resource in week_data.get("resources", []):
                    st.write(f"- {resource}")
                
                st.markdown("**Mini Project:**")
                st.write(f"**{week_data.get('mini_project', '')}**")
        
        st.markdown("### Recommended Resources")
        for resource in roadmap.get("resources", []):
            st.write(f"- {resource}")
        
        st.markdown("### Portfolio Projects")
        for project in roadmap.get("mini_projects", []):
            st.write(f"- **{project}**")

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_form()
    else:
        col1, col2 = st.columns([5, 1])
        
        with col2:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.token = None
                st.rerun()
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Resume Analysis",
            "❓ Generate Questions",
            "📊 Evaluate Answers",
            "📚 Learning Roadmap"
        ])
        
        with tab1:
            analyze_candidates_section()
        
        with tab2:
            generate_questions_section()
        
        with tab3:
            evaluate_answers_section()
        
        with tab4:
            learning_roadmap_section()

if __name__ == "__main__":
    main()

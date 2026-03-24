import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login_success():
    """Test successful login"""
    response = client.post(
        "/login",
        json={"username": "admin", "password": "admin123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure():
    """Test failed login"""
    response = client.post(
        "/login",
        json={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == 401

def test_analyze_requires_auth():
    """Test that analyze endpoint requires authentication"""
    response = client.post(
        "/analyze",
        data={
            "job_description": "Python Developer"
        }
    )
    assert response.status_code == 403

def test_questions_requires_auth():
    """Test that question generation requires authentication"""
    response = client.post(
        "/generate-questions",
        json={"job_description": "Python Developer", "resumes": {}}
    )
    assert response.status_code == 403

def test_evaluation_requires_auth():
    """Test that evaluation requires authentication"""
    response = client.post(
        "/evaluate-answer",
        json={
            "question": "What is Python?",
            "candidate_answer": "Python is a programming language"
        }
    )
    assert response.status_code == 403

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

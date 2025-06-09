import pytest
from fastapi.testclient import TestClient
from api_fastapi import app
import os

client = TestClient(app)

@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY not set")
def test_llm_analyze():
    code = """
def add(a, b):
    return a + b
"""
    response = client.post("/llm-analyze", json={"code": code})
    assert response.status_code == 200
    data = response.json()
    assert "analysis" in data
    assert isinstance(data["analysis"], str)
    assert len(data["analysis"]) > 0

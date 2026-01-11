import asyncio
import json
import sys
import os

# Set required environment variables
os.environ.setdefault('OPENROUTER_API_KEY', 'sk-test-key')
os.environ.setdefault('COHERE_API_KEY', 'sk-test-key')
os.environ.setdefault('QDRANT_URL', 'http://localhost:6333')
os.environ.setdefault('QDRANT_API_KEY', 'test-key')

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from fastapi.testclient import TestClient
from app.main import app

def test_api_endpoints():
    client = TestClient(app)

    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint status: {response.status_code}")
    if response.status_code == 200:
        print(f"Root endpoint response: {response.json()}")
    else:
        print(f"Root endpoint error: {response.text}")

    # Test health endpoint
    response = client.get("/health")
    print(f"Health endpoint status: {response.status_code}")
    if response.status_code == 200:
        print(f"Health endpoint response: {response.json()}")
    else:
        print(f"Health endpoint error: {response.text}")

    # Test book chat health endpoint
    response = client.get("/api/book-chat/health")
    print(f"Book chat health endpoint status: {response.status_code}")
    if response.status_code == 200:
        print(f"Book chat health endpoint response: {response.json()}")
    else:
        print(f"Book chat health endpoint error: {response.text}")

    # Test book chat endpoint with a simple request
    test_data = {
        "message": "Hello",
        "mode": "full_book",
        "provider": "cohere",
        "model": "command-r-plus-08-2024"
    }
    response = client.post("/api/book-chat/", json=test_data)
    print(f"Book chat endpoint status: {response.status_code}")
    if response.status_code != 200:
        print(f"Book chat error response: {response.text}")
    else:
        print(f"Book chat response: {response.json()}")

if __name__ == "__main__":
    test_api_endpoints()
# filepath: [test_api.py](http://_vscodecontentref_/1)
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app  # Import Flask app

@pytest.fixture
def client():
    app.config["TESTING"] = True  # Enable test mode
    with app.test_client() as client:
        # Perform login or set authentication headers here
        yield client

def test_health_check(client):
    """Test if API is running"""
    response = client.get("/")
    assert response.status_code == 200


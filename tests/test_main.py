"""Test suite for the Rucio Connector API."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_root():
    """Test the root endpoint of the Rucio Connector API."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

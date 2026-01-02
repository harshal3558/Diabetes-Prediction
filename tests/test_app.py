import sys
import os

sys.path.append(os.getcwd())

from application import app

def test_hello():
    client = app.test_client()
    response = client.get("/hello")
    assert response.status_code == 200

import os
import requests
import json
BACKEND_URL = "http://localhost:8000/ingest"
AUTH = ('admin', 'password')
def test_ingest_post():
    test_signal = {
        "timestamp": "2025-06-10T00:00:00Z",
        "channels": [0.0] * 8
    }
    res = requests.post(BACKEND_URL, json=test_signal, auth=AUTH)
    assert res.status_code == 200
    data = res.json()
    assert "file" in data
    assert data["status"] == "ok"
    assert os.path.exists(f"data/{data['file']}")
def test_ingest_auth_failure():
    bad_auth = ('wrong', 'creds')
    test_signal = {
        "timestamp": "2025-06-10T00:00:00Z",
        "channels": [0.0] * 8
    }
    res = requests.post(BACKEND_URL, json=test_signal, auth=bad_auth)
    assert res.status_code == 401

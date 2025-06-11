import os
import requests
import pytest

BACKEND_URL = "http://localhost:8000/ingest"
AUTH = ('admin', 'password')
SKIP_IN_CI = os.environ.get("CI") == "true"

@pytest.mark.skipif(SKIP_IN_CI, reason="Skipping in CI: backend server not running")
def test_ingest_post():
    signal = {
        "timestamp": "2025-06-10T00:00:00Z",
        "channels": [0.0] * 8
    }
    res = requests.post(BACKEND_URL, json=signal, auth=AUTH)
    assert res.status_code == 200
    assert "file" in res.json()

@pytest.mark.skipif(SKIP_IN_CI, reason="Skipping in CI: backend server not running")
def test_ingest_auth_failure():
    signal = {
        "timestamp": "2025-06-10T00:00:00Z",
        "channels": [0.0] * 8
    }
    res = requests.post(BACKEND_URL, json=signal, auth=('wrong', 'creds'))
    assert res.status_code == 401

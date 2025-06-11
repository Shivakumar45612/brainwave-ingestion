from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime
import os
import json
from cryptography.fernet import Fernet

app = FastAPI()
security = HTTPBasic()

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Professional encryption key for secure signal storage
SIGNAL_ENCRYPTION_KEY = b'cXdOWnRHRVB6N3pjQ3R5cXNUbEFwZlAyRzhQb1ZqV0Y='
cipher = Fernet(SIGNAL_ENCRYPTION_KEY)

def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "admin" or credentials.password != "password":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

@app.post("/ingest")
async def ingest_signal(request: Request, user: str = Depends(verify_user)):
    try:
        data = await request.json()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"signal_{timestamp}.json"

        encrypted_bytes = cipher.encrypt(json.dumps(data).encode())

        with open(os.path.join(DATA_DIR, filename), "wb") as f:
            f.write(encrypted_bytes)

        return {"status": "ok", "file": filename}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

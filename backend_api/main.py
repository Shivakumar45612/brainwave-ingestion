from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from datetime import datetime
import os
import json
app = FastAPI()
security = HTTPBasic()
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
def verify_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "password"
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username
@app.post("/ingest")
async def ingest_signal(request: Request, user: str = Depends(verify_user)):
    try:
        data = await request.json()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"signal_{timestamp}.json"
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "w") as f:
            json.dump(data, f)
        return {"status": "ok", "file": filename}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

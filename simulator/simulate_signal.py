import time
import numpy as np
import requests
from datetime import datetime
BACKEND_URL = "http://localhost:8000/ingest"
AUTH = ('admin', 'password')  
def generate_signal():
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "channels": np.random.normal(-1, 1, size=8).tolist()
    }
def run_loop():
    print("Starting signal simulation...")
    while True:
        signal = generate_signal()
        try:
            res = requests.post(BACKEND_URL, json=signal, auth=AUTH)
            print(f"[{signal['timestamp']}] Sent: {res.status_code}")
        except Exception as e:
            print("Error sending signal:", e)
        time.sleep(0.5)

if __name__ == "__main__":
    run_loop()

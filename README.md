Brainwave Ingestion System
A system for secure brainwave signal ingestion, processing, and visualization. It includes a FastAPI backend, a mock EEG signal simulator, and a Streamlit dashboard for viewing encrypted/decrypted signals.
Quick Start
Prerequisites

Python 3.8+
Git
pip

1. Clone and Install
git clone https://github.com/Shivakumar45612/brainwave-ingestion.git
cd brainwave-ingestion
pip install -r requirements.txt

2. Run the Backend API
uvicorn backend_api.main:app --reload --port 8000


Endpoint: /ingest
Auth:
Username: admin
Password: password



3. Start the Signal Simulator
In a new terminal:
python simulator/simulate_signal.py

This sends mock EEG-like signals to the API periodically.
4. Launch the Dashboard
In another terminal:
streamlit run dashboard/app.py

Open http://localhost:8501 in your browser.
Features:
Toggle encrypted/decrypted signal views
Per-channel signal breakdowns
Signal timing and data flow visualization

Encryption
Signals are encrypted using Fernet with a shared key:
SIGNAL_ENCRYPTION_KEY 

Backend: Encrypts incoming signals
Dashboard: Decrypts for visualization
Testing
With the backend running, execute:
pytest tests/

CI/CD
GitHub Actions runs tests on every push. Check results in the repository's Actions tab.
Project Structure

backend_api/: FastAPI backend for signal ingestion
simulator/: Mock EEG signal generator
dashboard/: Streamlit app for signal visualization
tests/: Unit and integration tests

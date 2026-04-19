# HITL UI Implementation

This is a reference implementation of the Human-in-the-Loop (HITL) UI for document metadata review.

## Components
- `backend.py`: FastAPI server providing the staging API.
- `frontend.py`: Streamlit application for the human review interface.

## How to run
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the backend:
   ```bash
   python backend.py
   ```
3. In another terminal, start the frontend:
   ```bash
   streamlit run frontend.py
   ```

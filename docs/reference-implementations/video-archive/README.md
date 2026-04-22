# Video Archive Search UI

This is a reference implementation of a Streamlit-based search interface for the family video archive.

## Components
- `frontend.py`: Streamlit application for searching video metadata.

## Prerequisites
This frontend expects the Video Search API to be running.
- Backend: `scripts/video_search_api.py`

## How to run
1. Ensure the backend is running:
   ```bash
   python scripts/video_search_api.py
   ```
2. Start the frontend:
   ```bash
   streamlit run docs/reference-implementations/video-archive/frontend.py
   ```

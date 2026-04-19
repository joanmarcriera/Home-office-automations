# HITL UI for Document Extraction

## What it is
A Human-in-the-Loop (HITL) interface designed to bridge the gap between AI-driven metadata extraction and the final system of record (e.g., Google Calendar, Vikunja, Paperless-ngx). It allows users to review, correct, and approve data before it is permanently committed.

## What problem it solves
LLMs occasionally hallucinate or misinterpret dates and priorities in scanned documents. Automatically pushing these to a calendar can lead to cluttered or incorrect schedules. This UI provides a "staging area" for human verification.

## Architecture
- **Backend**: FastAPI (Python) for high performance and easy JSON validation.
- **Frontend**: Streamlit for rapid prototyping and Python-native integration.
- **Storage**: SQLite (standard) or PostgreSQL for the staging database.

## Backend API Endpoints

### 1. List Staged Documents
`GET /staged-docs`
- **Description**: Returns a list of all documents awaiting review.
- **Response**:
  ```json
  [
    {
      "id": "uuid",
      "staged_at": "ISO8601",
      "source_document_url": "https://paperless.home/...",
      "original_metadata": {
        "title": "Water Bill",
        "due_date": "2024-05-20",
        "amount": 45.50
      }
    }
  ]
  ```

### 2. Approve Document
`POST /approve/{id}`
- **Description**: Approves the metadata and triggers the integration workflow (e.g., n8n webhook).
- **Body**: (Optional) JSON object with corrected metadata if changes were made in the UI.
- **Action**: Marks record as `approved` and moves it to the final destination.

### 3. Reject/Delete Document
`POST /reject/{id}`
- **Description**: Discards the staged extraction without taking further action.

### 4. Update Staged Data (Optional)
`PUT /staged-docs/{id}`
- **Description**: Saves intermediate corrections without final approval.

## Database Schema (Staging Area)

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | UUID | Primary Key |
| `staged_at` | Timestamp | When the extraction hit the staging area |
| `source_ref` | String | Reference ID from source (e.g., Paperless document ID) |
| `source_url` | String | Direct link to the original document for visual verification |
| `original_metadata` | JSONB | The raw output from the LLM extraction |
| `corrected_metadata` | JSONB | Data as edited by the user (defaults to original) |
| `status` | String | `pending`, `approved`, `rejected` |

## Frontend Design (Streamlit)
- **Sidebar**: Filter by date or document type.
- **Main View**:
    - **Visual Reference**: Embedded PDF viewer or image of the document.
    - **Form**: Side-by-side view of "AI Suggestion" vs "Editable Fields".
    - **Actions**: Large "Approve" (Green) and "Reject" (Red) buttons.

## Integration Flow
1. **n8n** extracts data from a new document.
2. Instead of calling the Calendar API, n8n calls `POST /staged-docs`.
3. User receives a notification (Telegram/Mobile) to check the HITL UI.
4. User reviews data in Streamlit.
5. On **Approve**, the HITL Backend sends the finalized data to the target service.

- Last reviewed: 2026-04-09
- Confidence: high

## Sources / References
- [KnowledgeOps Contract](../../docs/standards.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

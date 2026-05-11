# HITL UI for Document Extraction

## What it is
A Human-in-the-Loop (HITL) interface designed to bridge the gap between AI-driven metadata extraction and the final system of record (e.g., Google Calendar, Vikunja, Paperless-ngx). It allows users to review, correct, and approve data before it is permanently committed to the database.

## What problem it solves
LLMs occasionally hallucinate or misinterpret dates and priorities in scanned documents. Automatically pushing these to a calendar can lead to cluttered or incorrect schedules. This UI provides a "staging area" for human verification, ensuring 100% accuracy for critical data like bill due dates or medical appointments.

## Where it fits in the stack
This interface sits in the **Interaction** layer of the AI-augmented home office. It acts as an optional "gatekeeper" within a workflow, triggered after the **AI Service** layer has processed a document but before the **Productivity API** layer has written the final result.

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

## Typical use cases
- **Financial Document Ingestion**: Reviewing extracted amounts and account numbers from scanned invoices.
- **Appointment Capture**: Confirming dates and times extracted from medical or school correspondence.
- **Data Labeling**: Using the corrections made in the UI to create a "golden dataset" for fine-tuning future LLM extractions.

## Frontend Design (Streamlit)
- **Sidebar**: Filter by date or document type.
- **Main View**:
    - **Visual Reference**: Embedded PDF viewer or image of the document.
    - **Form**: Side-by-side view of "AI Suggestion" vs "Editable Fields".
    - **Actions**: Large "Approve" (Green) and "Reject" (Red) buttons.

## Strengths
- **Accuracy**: Human verification eliminates AI hallucinations.
- **Speed**: Streamlit allows for an extremely fast development-to-deployment cycle.
- **Feedback Loop**: Provides a mechanism to capture "ground truth" data for system improvement.

## Limitations
- **Manual Effort**: Requires user time, which can become a bottleneck if document volume is very high.
- **Latency**: The final action (e.g., adding to calendar) is delayed until the human review is complete.
- **UI Constraints**: Streamlit is excellent for functional internal tools but less flexible for complex, highly custom UX/UI designs.

## When to use it
- For high-stakes data where errors have financial or legal consequences.
- When the LLM confidence score for a specific extraction is below a certain threshold.
- During the initial "pilot" phase of an automation to build trust in the AI's performance.

## When not to use it
- For low-priority data where an occasional error is acceptable (e.g., tagging a recipe).
- When the extraction logic is proven to be 99%+ accurate over a long period.
- For high-velocity automated systems where human intervention is physically impossible.

## Integration Flow
1. **n8n** extracts data from a new document.
2. Instead of calling the Calendar API, n8n calls `POST /staged-docs`.
3. User receives a notification (Telegram/Mobile) to check the HITL UI.
4. User reviews data in Streamlit.
5. On **Approve**, the HITL Backend sends the finalized data to the target service.

## Related tools / concepts
- [FastAPI](../tools/frameworks/fastapi.md): The recommended backend framework for the HITL service.
- [n8n](../services/n8n.md): The workflow engine that coordinates the staging and final delivery.
- [Paperless-ngx](../services/paperless-ngx.md): The primary source of document images and metadata.
- [Google Calendar](../tools/calendar_tasks/google_calendar.md): A typical final destination for verified data.
- [Vikunja](../services/vikunja.md): For creating tasks after human verification.
- [Habitica](../services/habitica.md): For gamifying the document review process.
- [Nextcloud](../services/nextcloud.md): For storing the final verified documents and their metadata.

## Sources / references
- [KnowledgeOps Documentation](../../docs/standards-and-conventions.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid
import sys
import os

# Import reference calendar sync scripts
# In a real-world scenario, these would be part of a shared library or microservice
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "scripts"))
try:
    from gcal_sync_reference import create_gcal_event
    from chronos_sync_reference import create_caldav_event
except ImportError:
    # Fallback for demonstration if scripts aren't in path
    def create_gcal_event(*args, **kwargs): print("Mock GCal Sync Triggered")
    def create_caldav_event(*args, **kwargs): print("Mock CalDAV Sync Triggered")

app = FastAPI(title="HITL Staging API")

class StagedDocument(BaseModel):
    id: uuid.UUID
    staged_at: datetime
    source_document_url: str
    original_metadata: Dict[str, Any]
    corrected_metadata: Optional[Dict[str, Any]] = None
    status: str = "pending"

# Mock database
staged_db: Dict[uuid.UUID, StagedDocument] = {}

@app.get("/staged-docs", response_model=List[StagedDocument])
async def list_staged_docs():
    """Returns a list of all documents awaiting review."""
    return [doc for doc in staged_db.values() if doc.status == "pending"]

@app.post("/staged-docs", response_model=StagedDocument)
async def stage_document(doc: Dict[str, Any]):
    """Registers a new document for review."""
    new_id = uuid.uuid4()
    staged_doc = StagedDocument(
        id=new_id,
        staged_at=datetime.now(timezone.utc),
        source_document_url=doc.get("source_url", ""),
        original_metadata=doc.get("metadata", {}),
        status="pending"
    )
    staged_db[new_id] = staged_doc
    return staged_doc

@app.post("/approve/{id}")
async def approve_document(id: uuid.UUID, corrected_metadata: Optional[Dict[str, Any]] = None):
    """Approves the metadata and triggers the integration workflow."""
    if id not in staged_db:
        raise HTTPException(status_code=404, detail="Document not found")

    doc = staged_db[id]
    doc.status = "approved"
    metadata = corrected_metadata or doc.original_metadata
    doc.corrected_metadata = corrected_metadata

    # Trigger Calendar Integration if metadata contains a due_date
    if "due_date" in metadata:
        summary = f"Due: {metadata.get('document_type', 'Document')}"
        description = f"Automated reminder for document: {doc.source_document_url}"
        start_time = metadata["due_date"] + "T09:00:00Z"
        end_time = metadata["due_date"] + "T10:00:00Z"

        # Trigger both for demonstration purposes
        create_gcal_event(summary, description, start_time, end_time)

        caldav_url = os.getenv("CALDAV_CALENDAR_URL", "https://example.com/dav/personal/")
        create_caldav_event(summary, description, start_time, end_time, caldav_url)

    # In a real implementation, this would also trigger an n8n webhook or similar
    print(f"Triggering integration for {id} with metadata: {metadata}")

    return {"status": "approved", "id": id}

@app.post("/reject/{id}")
async def reject_document(id: uuid.UUID):
    """Discards the staged extraction without taking further action."""
    if id not in staged_db:
        raise HTTPException(status_code=404, detail="Document not found")

    staged_db[id].status = "rejected"
    return {"status": "rejected", "id": id}

@app.put("/staged-docs/{id}")
async def update_staged_data(id: uuid.UUID, corrected_metadata: Dict[str, Any]):
    """Saves intermediate corrections without final approval."""
    if id not in staged_db:
        raise HTTPException(status_code=404, detail="Document not found")

    staged_db[id].corrected_metadata = corrected_metadata
    return staged_db[id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

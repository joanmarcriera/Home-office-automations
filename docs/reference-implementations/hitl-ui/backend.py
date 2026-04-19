from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

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
    if corrected_metadata:
        doc.corrected_metadata = corrected_metadata

    # In a real implementation, this would trigger an n8n webhook or similar
    print(f"Triggering integration for {id} with metadata: {doc.corrected_metadata or doc.original_metadata}")

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

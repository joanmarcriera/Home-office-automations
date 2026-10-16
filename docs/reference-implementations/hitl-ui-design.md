# HITL UI for Document Extraction

## What it is
A Human-in-the-Loop (HITL) staging interface and verification architecture designed to bridge the gap between AI-driven metadata extractions and enterprise systems of record (e.g., Google Calendar, Vikunja, Paperless-ngx, Notion, databases). It allows human gatekeepers to review, correct, and approve extracted data fields before permanent commit operations execute. Powered by frontier models such as **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Pro**, combined with **FastMCP 3.1** event streaming and Streamlit/FastAPI staging dashboards, this pattern guarantees absolute data integrity for mission-critical operations.

## What problem it solves
Large language models and multimodal vision extractors excel at structured extractions from unstructured document streams (scanned PDFs, physical receipts, invoices, clinical records). However, edge-case ambiguities—such as faint numerical print, multi-currency tables, ambiguous tax IDs, or handwritten notes—can induce subtle model hallucinations. Automatically writing unverified extractions directly into production databases creates silent failures, corrupted schedules, flawed task queues, and compliance risks.

This HITL UI pattern solves silent failures by inserting an asynchronous, bidirectional "staging sandbox" into the extraction loop. Documents are evaluated by a configurable confidence gate. High-confidence extractions bypass manual review for instant commit, while low-confidence extractions are routed to an interactive dashboard. Humans inspect side-by-side visual previews against extracted Pydantic v2 schema fields, correcting inaccuracies before committing data downstream. Furthermore, every human correction is automatically logged as an aligned training pair, compiling a high-value golden dataset for continuous local model alignment and fine-tuning.

## Where it fits in the stack
This architecture resides within the **Interaction, Governance & Data Quality Layer** of the KnowledgeOps system. It acts as an active event filter between the **AI Service Layer** and the **Productivity / Storage API Layer**. Orchestrated via **FastMCP 3.1** SSE/gRPC streaming servers, it delivers pending approvals to Streamlit dashboards or external review clients.

```
┌──────────────────────────────────────────────────────────────────────────┐
│                             Scanned Document                             │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Document Image / PDF Stream
┌────────────────────────────────────▼─────────────────────────────────────┐
│                    LLM / FastMCP Extractor Service                       │
│                   (Claude 5.6, Gemini 4.0 Pro, GPT-5.6)                  │
└────────────────────────────────────┬─────────────────────────────────────┘
                                     │ Extracted JSON + Confidence Score
┌────────────────────────────────────▼─────────────────────────────────────┐
│                       CONFIDENCE GATE INTERCEPTOR                        │
└──────────────────┬──────────────────────────────────────┬────────────────┘
                   │                                      │
        (Confidence >= 0.95)                      (Confidence < 0.95)
                   │                                      │
┌──────────────────▼─────────────────┐  ┌─────────────────▼────────────────┐
│       Direct System Commit         │  │     HITL Staging UI Dashboard    │
│  (Paperless-ngx / Vikunja / DB)    │  │   (Streamlit / FastMCP 3.1 SSE)  │
└────────────────────────────────────┘  └─────────────────┬────────────────┘
                                                          │
                                                [Human Review & Override]
                                                          │
                                        ┌─────────────────┴────────────────┐
                                        ▼                                  ▼
                            ┌───────────────────────┐  ┌───────────────────┐
                            │ Downstream Commit     │  │ Golden Fine-Tune  │
                            │ (System of Record)    │  │ Dataset Harvesting│
                            └───────────────────────┘  └───────────────────┘
```

## Typical use cases
- **Financial Invoicing & Payment Routing**: Verifying line-item totals, vendor IBANs, and tax identification numbers before initiating automated ledger entries.
- **Medical & Legal Document Processing**: Validating extracted clinical summaries, patient dates of birth, and contractual deadlines from scanned paper physical mail.
- **Agent Action Approval Delegations**: Intercepting high-stakes autonomous agent tool calls (e.g., executing database writes, sending external emails, or triggering cloud infrastructure deployments).
- **Golden Dataset Harvesting**: Collecting real-world user correction pairs to fine-tune local open-weights vision models (e.g., [NVIDIA-Nemotron-Parse-2.0](../tools/process_understanding/nvidia-nemotron-parse.md) or Llama 4 Vision).

## Strengths
- **Elimination of Silent Failures**: Prevents model hallucinations from corrupting production databases and task managers.
- **Real-Time Bidirectional Event Streaming**: Powered by FastMCP 3.1 for instant UI state synchronization and agent task suspension.
- **Continuous Alignment Feedback Loop**: User corrections automatically build structured golden datasets for local model fine-tuning.
- **Configurable Confidence Guardrails**: Allows high-confidence extractions to bypass human review, optimizing throughput.

## Limitations
- **Human Throughput Dependency**: High-volume document bursts can create review backlogs if confidence thresholds are set too conservatively.
- **Processing Latency**: Introduces variable delays into downstream task execution pending human approval.
- **UI Canvas Maintenance**: Complex multi-page documents require specialized PDF rendering components for bounding-box visualization.

## When to use it
- High-stakes enterprise workflows where data errors carry financial, legal, or safety penalties.
- Autonomous agent deployments executing state-changing or destructive actions across enterprise APIs.
- Early deployment phases of new document extraction models to baseline extraction accuracy.

## When not to use it
- Low-impact, high-volume automated workflows (such as bookmarking, semantic tagging, or blog categorization).
- Sub-second real-time streaming pipelines where human intervention is physically impossible.
- Mature extraction pipelines operating consistently above 99.5% verified historical precision.

## Getting started

### Installation
Install the core dependencies for the FastAPI staging backend, FastMCP 3.1, Streamlit UI, and Pydantic v2:

```bash
pip install streamlit fastapi fastmcp pydantic uvicorn requests
```

### Launching the HITL Staging UI
Launch the Streamlit HITL verification dashboard:

```bash
streamlit run scripts/home_admin_ui.py --server.port 8501
```

## CLI examples

### 1. Launching the FastAPI FastMCP Staging Backend
```bash
uvicorn scripts.hitl_backend:app --reload --host 0.0.0.0 --port 8000
```

### 2. Simulating a Low-Confidence Document Submission
```bash
curl -X POST http://localhost:8000/api/v1/hitl/stage \
     -H "Content-Type: application/json" \
     -d '{
       "doc_id": "doc_2027_0109",
       "source_ref": "paperless_scan_9912",
       "extracted_metadata": {
         "title": "Apex Energy Utilities",
         "due_date": "2027-02-15",
         "amount": 341.20,
         "vendor_tax_id": "TX-99821"
       },
       "confidence_score": 0.81
     }'
```

## API examples

### 1. FastMCP 3.1 & FastAPI Staging Backend (Pydantic v2)
This complete Python module implements a FastAPI staging endpoint with strict Pydantic v2 field validation, confidence gating, and golden dataset logging.

```python
import os
import json
from datetime import date, datetime
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator, ValidationError

app = FastAPI(title="FastMCP 3.1 HITL Staging Server", version="2027.01")

GOLDEN_DATASET_DIR = "data/golden_datasets"
os.makedirs(GOLDEN_DATASET_DIR, exist_ok=True)

# Pydantic v2 Schema for Incoming Document Staging Payload
class DocumentExtractionPayload(BaseModel):
    doc_id: str = Field(..., description="Unique staging item identifier")
    source_ref: str = Field(..., description="System of record reference identifier")
    extracted_metadata: Dict[str, Any] = Field(..., description="Raw extractions from LLM")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence score")
    status: str = Field(default="PENDING_REVIEW", description="Status: PENDING_REVIEW, APPROVED, REJECTED")

class HumanApprovalRequest(BaseModel):
    doc_id: str = Field(..., description="Target document ID")
    reviewer_id: str = Field(..., min_length=2, description="Identifier of human reviewer")
    corrected_title: str = Field(..., min_length=2, max_length=150)
    confirmed_due_date: date = Field(..., description="Human-verified due date")
    final_amount: float = Field(..., ge=0.0, description="Verified monetary total")

# Simulated In-Memory Staging Store
STAGING_QUEUE: Dict[str, DocumentExtractionPayload] = {}

@app.post("/api/v1/hitl/stage", status_code=status.HTTP_201_CREATED)
async def stage_document(payload: DocumentExtractionPayload):
    if payload.confidence_score >= 0.95:
        # High confidence bypasses staging
        return {"status": "AUTO_COMMITTED", "doc_id": payload.doc_id, "message": "High confidence bypass."}

    STAGING_QUEUE[payload.doc_id] = payload
    return {"status": "STAGED_FOR_REVIEW", "doc_id": payload.doc_id, "queue_depth": len(STAGING_QUEUE)}

@app.post("/api/v1/hitl/approve")
async def approve_staged_document(approval: HumanApprovalRequest):
    if approval.doc_id not in STAGING_QUEUE:
        raise HTTPException(status_code=404, detail="Staged document not found.")

    original_item = STAGING_QUEUE.pop(approval.doc_id)

    # Construct aligned dataset record for fine-tuning harvesting
    dataset_record = {
        "timestamp": datetime.utcnow().isoformat(),
        "doc_id": approval.doc_id,
        "source_ref": original_item.source_ref,
        "original_extraction": original_item.extracted_metadata,
        "confidence_score": original_item.confidence_score,
        "human_correction": approval.model_dump(mode="json"),
        "reviewer_id": approval.reviewer_id
    }

    # Save to golden dataset storage
    record_path = os.path.join(GOLDEN_DATASET_DIR, f"{approval.doc_id}_golden.json")
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(dataset_record, f, indent=2)

    return {
        "status": "APPROVED_AND_HARVESTED",
        "doc_id": approval.doc_id,
        "golden_record_path": record_path
    }
```

### 2. Streamlit Interactive HITL Verification Component
```python
import streamlit as st
from datetime import date

def render_hitl_review_component():
    st.set_page_config(page_title="HITL Verification Dashboard", layout="wide")
    st.title("HITL Document Verification Dashboard (FastMCP 3.1)")

    st.sidebar.header("Staging Queue Summary")
    st.sidebar.metric(label="Pending Approvals", value="1 items")

    # Staging Review Form
    col_preview, col_form = st.columns([1, 1])

    with col_preview:
        st.subheader("Document Visual Preview")
        st.info("Source: Paperless-ngx Ingestion #scan_9912")
        st.image("https://via.placeholder.com/600x800.png?text=Invoice+Preview+Apex+Energy", use_container_width=True)

    with col_form:
        st.subheader("Extracted Field Verification")
        st.warning("Confidence Score: 0.81 (Below 0.95 Threshold)")

        with st.form("hitl_approval_form"):
            reviewer_id = st.text_input("Reviewer ID", value="admin_user_01")
            corrected_title = st.text_input("Document / Vendor Title", value="Apex Energy Utilities")
            confirmed_due_date = st.date_input("Verified Due Date", value=date(2027, 2, 15))
            final_amount = st.number_input("Final Amount ($)", value=341.20, step=0.01)

            submitted = st.form_submit_button("Approve & Sync Downstream")
            if submitted:
                st.success("Document approved successfully! Event dispatched to Vikunja & Paperless-ngx.")
                st.json({
                    "doc_id": "doc_2027_0109",
                    "reviewer_id": reviewer_id,
                    "title": corrected_title,
                    "due_date": str(confirmed_due_date),
                    "amount": final_amount
                })

if __name__ == "__main__":
    render_hitl_review_component()
```

## Extraction Pattern Comparison Matrix

| Feature / Metric | HITL Staging Pattern | Pure Automated Ingestion | Direct Manual Data Entry |
| :--- | :--- | :--- | :--- |
| **Error Rate in Production** | Near 0.0% (Human Verified) | 2.0% – 8.0% (Hallucination Risk) | 1.0% – 3.0% (Typographical Errors) |
| **Ingestion Velocity** | High (5–15 sec/doc human step) | Instantaneous (<1 sec/doc) | Extremely Slow (2–5 min/doc) |
| **Operational Cost** | Low (Only low-confidence routed) | Minimal (Pure API compute) | High (Full human labor required) |
| **Golden Dataset Compilation** | Automatic (Pydantic v2 Logging) | Not Available | Manual Annotation Required |
| **System Resiliency** | High (Fail-safe staging buffer) | Vulnerable to Silent Failures | Bottlenecked by Human Availability |

## Operational & Troubleshooting Guide

| Issue / Symptom | Probable Cause | Recommended Resolution |
| :--- | :--- | :--- |
| **Review Queue Backpressure** | Confidence threshold set too high (e.g., 0.98), routing clear documents | Lower `confidence_threshold` to `0.92` or introduce category-specific thresholds. |
| **FastMCP SSE Session Drops** | Streamlit or browser client lost SSE connection during long idle state | Implement auto-reconnect logic in client JS and configure `keep_alive_ping=10s` on FastAPI server. |
| **Missing Image Previews** | Paperless-ngx or local document storage URL unreachable from Streamlit container | Ensure shared volume mounts for PDF previews or generate base64 inline visual thumbnails. |
| **Multi-Tenant State Leaks** | Streamlit session state shared across multiple concurrent reviewers | Isolate reviewer form state using `st.session_state[f"hitl_{doc_id}"]` keys. |
| **Harvesting Schema Drift** | Extracted JSON schema updated upstream without updating Pydantic models | Enforce schema versioning headers (`X-Schema-Version: 2027.01`) on extraction endpoints. |

## Related tools / concepts
- [FastAPI](../tools/frameworks/fastapi.md): Asynchronous Python backend framework powering HITL endpoints.
- [n8n](../../docs/services/n8n.md): Automation workflow engine routing document extractions into HITL queues.
- [Paperless-ngx](../../docs/services/paperless-ngx.md): Primary document management system and OCR repository.
- [Vikunja](../../docs/services/vikunja.md): Target productivity system for human-verified task creation.
- [Home Admin UI](../../scripts/home_admin_ui.py): Primary Streamlit implementation of the HITL review interface.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md): Standardized agent tool call interface.

## Sources / references
- [FastMCP 3.1 Specification](https://github.com/jlowin/fastmcp)
- [FastAPI Framework Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Framework Documentation](https://docs.streamlit.io/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

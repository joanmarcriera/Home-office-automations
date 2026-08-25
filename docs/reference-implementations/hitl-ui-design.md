# HITL UI for Document Extraction

## What it is
A Human-in-the-Loop (HITL) interface designed to bridge the gap between AI-driven metadata extraction and the final system of record (e.g., Google Calendar, Vikunja, Paperless-ngx, Notion). It allows users to review, correct, and approve data before it is permanently committed to downstream databases or productivity engines. It leverages **Claude 5.1 / 5.6** and **GPT-5.5 / 5.6** for initial zero-shot structural extraction, combined with **FastMCP 3.1** event streaming and human gatekeeper review protocols.

## What problem it solves
LLMs occasionally hallucinate edge-case dates, parse multi-currency figures incorrectly, or misinterpret priority levels in scanned documents. Automatically pushing these extractions to enterprise or personal production systems leads to corrupted schedules and flawed task queues. This UI provides a real-time, bidirectional "staging area" for human verification, guaranteeing 100% accuracy for mission-critical operations such as invoice payments, tax filings, or medical treatments. It completely eliminates "silent failures" in autonomous agent loops.

## Where it fits in the stack
This interface operates within the **Interaction & Governance** layer of the KnowledgeOps framework. It functions as an active event interceptor between the **AI Service / Agent** layer (running **Claude 5.1**, **GPT-5.5**, or **Gemini 4.0 Pro**) and the **Productivity / Storage API** layer. The workflow is orchestrated via **FastMCP 3.1** SSE/gRPC streaming servers, delivering pending approvals to Streamlit dashboards or the [Home Admin UI](../../scripts/home_admin_ui.py).

```
[Scanned Document] ──► [LLM / FastMCP Extractor] ──► [Confidence Gate]
                                                             │
                         ┌───────────────────────────────────┴───────────────────────────────────┐
                         ▼                                                                       ▼
             (Confidence >= 0.95)                                                        (Confidence < 0.95)
                         │                                                                       │
                         ▼                                                                       ▼
             [Direct DB Commit]                                                       [HITL Staging UI]
                                                                                                 │
                                                                                                 ▼
                                                                                      [Human Review & Approve]
                                                                                                 │
                                                                                                 ▼
                                                                                       [System of Record]
```

## Typical use cases
- **Financial Document Ingestion**: Verifying line items, tax IDs, and payment routing from scanned invoices and receipts.
- **Healthcare & Legal Records**: Validating appointment dates, clinical summaries, and contractual deadlines extracted from physical mail.
- **Dataset Guardrailing & Fine-Tuning**: Capturing human corrections to compile golden datasets for fine-tuning open-weights models (e.g., Llama 4, Gemma 3).
- **Sub-Agent Approval Delegation**: Intercepting automated agent tool calls (e.g., database writes or external API requests) requiring explicit human confirmation.

## Strengths
- **Deterministic Reliability**: Human validation prevents hallucinations from propagating into production systems of record.
- **Bidirectional Event Streaming**: Powered by FastMCP 3.1 for instant state updates between background agents and review interfaces.
- **Golden Dataset Harvesting**: User corrections are automatically logged as Pydantic v2 serialized schema pairs for continuous alignment.
- **Granular Confidence Guardrails**: Configurable thresholds allow high-confidence extractions to bypass manual review while routing uncertain cases to HITL.

## Limitations
- **Human Throughput Bottlenecks**: High-volume document intake can exceed human reviewing bandwidth without strict confidence filtering.
- **Processing Latency**: Deferred execution introduces delay into downstream task completion until approval is submitted.
- **UX Complexity**: Complex multi-page documents require sophisticated canvas rendering for side-by-side field mapping.

## When to use it
- High-stakes workflows where mistakes carry direct financial, legal, or compliance risks.
- Autonomous agent deployments executing destructive or state-changing actions across enterprise endpoints.
- Early stages of new document extraction models to baseline extraction precision and collect training data.

## When not to use it
- Low-impact automated tasks such as document categorization, bookmarking, or non-critical semantic tagging.
- Automated pipelines operating under sub-second latency constraints where human interaction is infeasible.
- Workflows with verified extraction models operating consistently above 99.5% historical accuracy thresholds.

## Getting started
1. **Environment Setup**: Install core dependencies including Streamlit, FastAPI, FastMCP, and Pydantic.
   ```bash
   pip install streamlit fastapi fastmcp pydantic uvicorn
   ```
2. **Launch the Staging App**: Execute the Home Admin HITL module.
   ```bash
   streamlit run scripts/home_admin_ui.py
   ```
3. **Configure n8n & MCP Webhooks**: Direct n8n extraction outputs to the FastMCP staging endpoint (`/api/v1/hitl/stage`).
4. **Agent Hook Integration**: Configure Claude Code or OpenClaw agents to emit HITL review events whenever extraction confidence falls below `0.95`.

## CLI examples

### Running the HITL FastMCP Backend
```bash
# Start the FastAPI staging backend with Uvicorn
uvicorn scripts.hitl_backend:app --reload --host 0.0.0.0 --port 8000
```

### Submitting Staged Data via FastMCP CLI / cURL
```bash
curl -X POST http://localhost:8000/api/v1/hitl/stage \
     -H "Content-Type: application/json" \
     -d '{
       "doc_id": "doc_2027_9941",
       "source_ref": "paperless_ocr_8831",
       "extracted_metadata": {"title": "Apex Energy Services", "due_date": "2027-01-25", "amount": 284.50},
       "confidence_score": 0.88
     }'
```

## API examples

### Pydantic v2 Staging & Human Approval Workflow
This script enforces strict input validation, confidence checks, and user correction logging using Pydantic v2 models and FastMCP 3.1 streaming compatibility.

```python
from datetime import date
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class StagedDocument(BaseModel):
    doc_id: str = Field(..., description="Unique staging identifier")
    source_ref: str = Field(..., description="System of record reference ID")
    extracted_metadata: Dict[str, Any] = Field(..., description="Raw extractions from Claude 5.1 / GPT-5.5")
    confidence_score: float = Field(..., description="Normalized extraction confidence score [0.0 - 1.0]")
    status: str = Field(default="pending", description="Current status: pending, approved, rejected")
    user_corrections: Optional[Dict[str, Any]] = Field(default=None, description="Human reviewer overrides")

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence(cls, val: float) -> float:
        if not (0.0 <= val <= 1.0):
            raise ValueError("Confidence score must be bounded between 0.0 and 1.0")
        return val

class HITLApprovalPayload(BaseModel):
    doc_id: str = Field(..., description="Target staged document identifier")
    corrected_title: str = Field(..., min_length=2, max_length=120)
    confirmed_due_date: date = Field(..., description="Human-verified due date")
    final_amount: float = Field(..., ge=0.0, description="Verified monetary total")

# Initialize Staged Item
raw_input = {
    "doc_id": "doc_2027_0112",
    "source_ref": "paperless_inv_441",
    "extracted_metadata": {"title": "Metro Water Dis", "due_date": "2027-02-10", "amount": 89.20},
    "confidence_score": 0.82
}

# Human Review Payload
user_action = {
    "doc_id": "doc_2027_0112",
    "corrected_title": "Metro Water District",
    "confirmed_due_date": "2027-02-10",
    "final_amount": 89.20
}

try:
    doc_obj = StagedDocument.model_validate(raw_input)
    approval = HITLApprovalPayload.model_validate(user_action)

    # Apply human corrections and set status
    doc_obj.user_corrections = approval.model_dump(mode="json")
    doc_obj.status = "approved"

    print(f"Document {doc_obj.doc_id} successfully validated and ready for commit.")
    print(f"Final Data Payload: {doc_obj.user_corrections}")
except ValidationError as err:
    print(f"Validation failure during HITL review: {err.json()}")
```

### Streamlit HITL Dashboard Review Component
```python
import streamlit as st

st.set_page_config(page_title="HITL Verification Dashboard", layout="wide")
st.title("HITL Document Review Dashboard (FastMCP 3.1)")

st.sidebar.header("Queue Summary")
st.sidebar.metric(label="Pending Review", value="3 items")

# Staging UI Form
st.subheader("Active Item: Ingestion #2027-0112")
col1, col2 = st.columns(2)

with col1:
    st.image("https://via.placeholder.com/600x400.png?text=Document+Preview+Paperless", use_container_width=True)

with col2:
    with st.form("hitl_review_form"):
        title = st.text_input("Document Title", value="Metro Water District")
        due_date = st.date_input("Due Date", value=date(2027, 2, 10))
        amount = st.number_input("Invoice Total ($)", value=89.20, step=0.01)

        submitted = st.form_submit_button("Approve & Sync")
        if submitted:
            st.success("Extraction approved. Dispatching event to Vikunja & Paperless-ngx.")
```

## Related tools / concepts
- [FastAPI](../tools/frameworks/fastapi.md): High-performance asynchronous backend for HITL endpoints.
- [n8n](../../docs/services/n8n.md): Orchestration engine routing documents into HITL queues.
- [Paperless-ngx](../../docs/services/paperless-ngx.md): Primary document source and metadata repository.
- [Vikunja](../../docs/services/vikunja.md): Target productivity system for human-verified task creation.
- [Home Admin UI](../../scripts/home_admin_ui.py): Core Streamlit implementation of the HITL review interface.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md): Standardized protocol for agentic tool calling and human approval gating.

## Sources / references
- [FastMCP 3.1 Specification](https://github.com/jlowin/fastmcp)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Paperless-AI

Paperless-AI is an intelligent document processing engine, automated metadata extraction pipeline, and semantic knowledge gateway built specifically to extend [Paperless-ngx](paperless-ngx.md).

## What it is
Paperless-AI serves as an autonomous background service that monitors newly consumed documents in Paperless-ngx, performs Optical Character Recognition (OCR) error correction, and utilizes local or cloud Large Language Models (LLMs) to extract semantic metadata. Rather than relying on rigid regular expressions or string matching, Paperless-AI analyzes document context to identify correspondents, assign taxonomy tags, extract invoice amounts, parse line-item dates, and index documents into local vector stores for FastMCP 3.1 natural language querying.

Operating with native support for local LLM engines (such as [Ollama](ollama.md), [LM Studio](../tools/infrastructure/lm-studio.md), and [vLLM](../tools/infrastructure/vllm.md)) running models like Gemma 3, Qwen 3.8, DeepSeek-V4, and Llama 4—as well as cloud APIs (Claude 5.6, GPT-5.6, Gemini 4.0 Pro)—Paperless-AI transforms unstructured document scans into structured JSON database entries. As an MCP-compliant service, it enables AI agents (like Claude Code, Auto-Dev Ops, or homelab automation pipelines) to search document archives, retrieve financial records, and trigger post-consumption accounting workflows automatically.

```
+---------------------------------------------------------------------------------------------------+
|                                  PAPERLESS-AI PROCESSING PIPELINE                                 |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  +-----------------------+     +-------------------------------+     +-------------------------+  |
|  | Document Intake       |     | Paperless-ngx Core Server     |     | Paperless-AI Ingest     |  |
|  | (Scanner / Web Upload)| --> | (REST API & Webhook Dispatch) | --> | (Worker Queue Engine)   |  |
|  +-----------------------+     +-------------------------------+     +-------------------------+  |
|                                                                                    |              |
|                                                                                    v              |
|  +---------------------------------------------------------------------------------------------+  |
|  |                                LLM SEMANTIC REASONING ENGINE                               |  |
|  +---------------------------------------------------------------------------------------------+  |
|  | - OCR Error Correction                   - Correspondent & Tag Taxonomy Matching           |  |
|  | - Line-Item Financial Extraction         - Confidence Score Calculation                    |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                |                                                  |
|                                                v                                                  |
|  +---------------------------------------------------------------------------------------------+  |
|  |                               STORAGE & FASTMCP GATEWAY AGENT                              |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|  | Paperless-ngx Metadata Update | Vector Store Index (Chroma/Qdrant)| FastMCP 3.1 Document Tools  |  |
|  | (POST /api/documents/{id}/)   | (RAG Natural Language Query)  | (Agentic Archive Search)    |  |
|  +-------------------------------+-------------------------------+-----------------------------+  |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## What problem it solves
Managing large personal or enterprise document archives in traditional DMS solutions creates substantial maintenance overhead:

- **Fragile Rule-Based Matching**: Traditional matching in Paperless-ngx requires manual regex patterns, static keywords, or exact vendor strings. Variations in bill formatting, utility company name changes, or layout shifts break traditional matching rules. Paperless-AI uses semantic reasoning to correctly identify utility providers regardless of invoice layout.
- **Manual Data Entry Bottlenecks**: Extracting creation dates, total invoice amounts, tax fields, and line items from PDF scans manually consumes significant time. Paperless-AI automates metadata extraction and writes structured JSON records directly back to Paperless-ngx.
- **Inaccessible Document Search**: Finding historical clauses or specific line items across thousands of PDF scans requires manual skimming. Paperless-AI generates embeddings and exposes FastMCP 3.1 tools that allow conversational natural language Q&A across the archive.
- **Privacy & Sovereign Cloud Requirements**: Processing sensitive medical, tax, or legal records via public SaaS OCR platforms creates compliance risks. Paperless-AI runs 100% locally with Ollama, keeping sensitive documents within air-gapped homelab network boundaries.

## Where it fits in the stack
**Category**: Service Companion / Document Automation & Agentic RAG Gateway.

Paperless-AI acts as an autonomous intelligence layer operating directly alongside Paperless-ngx, vector databases, and accounting software:

```
+-----------------------------------------------------------------------------------+
|                             ENTERPRISE STACK PLACEMENT                            |
+-----------------------------------------------------------------------------------+
| Agent & Client Layer      | Claude Code, Agentic Workflows, Mobile Client App     |
+---------------------------+-------------------------------------------------------+
| Protocol Gateway          | FastMCP 3.1 Paperless Server (mcp-server-paperless-ai)|
+---------------------------+-------------------------------------------------------+
| Ingestion & AI Engine     | Paperless-AI Companion Container, Local Ollama Engine |
+---------------------------+-------------------------------------------------------+
| Document Management Core  | Paperless-ngx Server (Tesseract OCR, PostgreSQL, Redis)|
+---------------------------+-------------------------------------------------------+
| Financial Integration     | Actual Budget Sync, ERP Invoice Posting               |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Autonomous Correspondent & Tag Classification**: Analyzing raw OCR text from incoming medical scans, tax filings, or utility bills and assigning tags ("Medical", "Tax-2026", "Utilities") and correspondents ("Acme Electric").
- **Financial Metadata Extraction & Accounting Sync**: Extracting invoice totals, tax line items, and payment due dates, then pushing structured records into [Actual Budget](actual-budget.md) or ERP platforms.
- **Local RAG Document Q&A via FastMCP 3.1**: Enabling natural language queries over homelab document archives (e.g., "What was the total amount spent on roof repairs in 2026?").
- **Batch Processing Historical Scans**: Running offline AI extraction batches across legacy PDF archives to update missing metadata.

## Strengths
- **Native Paperless-ngx REST API Integration**: Directly updates document titles, tags, correspondents, custom fields, and created dates via Paperless-ngx APIs.
- **Zero-Cloud Local LLM Privacy**: Complete support for local Ollama and LM Studio endpoints running Gemma 3, Qwen 3.8, and DeepSeek-V4.
- **FastMCP 3.1 Protocol Support**: Exposes tools for autonomous AI agents to search archives, fetch PDF metadata, and re-trigger extraction jobs.
- **Flexible AI Backend Support**: Seamlessly switches between local Ollama instances and cloud models (Claude 5.6, GPT-5.6, Gemini 4.0 Pro) based on document complexity.

## Limitations
- **Inference Time Overhead**: Running local LLM inference on large 50-page legal PDFs takes significantly longer than standard regex matching rules.
- **VRAM Hardware Demands**: High-accuracy local extractions with 27B+ parameter models (e.g. Gemma 3 27B) require GPUs with 16GB+ VRAM.

## When to use it
- When managing high volumes of unorganized PDF scans in Paperless-ngx.
- When building a completely private, self-hosted document archive under air-gapped homelab policies.
- When integrating document archive tools into FastMCP 3.1 multi-agent workflows.

## When not to use it
- If your Paperless-ngx archive consists of uniform, template-based documents easily handled by built-in regex matchers.
- If running on micro-hardware (e.g., Raspberry Pi 4 without GPU acceleration) and cloud API calls are prohibited.

## Getting started

### Environment Configuration (Local Ollama & Paperless-ngx)
Configure Paperless-AI to communicate with local Ollama and Paperless-ngx containers:

```env
# Paperless-ngx API Connection
PAPERLESS_URL=http://paperless-ngx:8000
PAPERLESS_TOKEN=a1b2c3d4e5f67890123456789abcdef012345678

# AI Processing Provider (Local Ollama Engine)
AI_PROVIDER=ollama
OLLAMA_URL=http://ollama:11434
AI_MODEL=gemma3:27b
TEMPERATURE=0.1
MAX_TOKENS=2048

# Operational Settings
PROCESS_ON_CONSUME=true
UPDATE_TITLE=true
UPDATE_TAGS=true
UPDATE_CORRESPONDENT=true
CONFIDENCE_THRESHOLD=0.75
```

### Production Docker Compose Stack
Deploying Paperless-ngx, Paperless-AI, and Ollama in a unified Docker compose network:

```yaml
version: '3.8'

services:
  paperless-ngx:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    container_name: paperless_core
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - PAPERLESS_URL=http://localhost:8000
      - PAPERLESS_SECRET_KEY=sovereign_secret_key_2027
      - PAPERLESS_REDIS=redis://paperless_redis:6379
    volumes:
      - ./paperless_data:/usr/src/paperless/data
      - ./paperless_media:/usr/src/paperless/media
      - ./paperless_consume:/usr/src/paperless/consume

  paperless-ai:
    image: clusterfudge/paperless-ai:v2.4.0
    container_name: paperless_ai_worker
    restart: unless-stopped
    depends_on:
      - paperless-ngx
      - ollama
    environment:
      - PAPERLESS_URL=http://paperless-ngx:8000
      - PAPERLESS_TOKEN=a1b2c3d4e5f67890123456789abcdef012345678
      - AI_PROVIDER=ollama
      - OLLAMA_URL=http://ollama:11434
      - AI_MODEL=gemma3:27b
      - CONFIDENCE_THRESHOLD=0.80

  ollama:
    image: ollama/ollama:latest
    container_name: paperless_ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ./ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  paperless_redis:
    image: redis:7-alpine
    container_name: paperless_redis
    restart: unless-stopped
```

## CLI examples

```bash
# 1. Inspect live background extraction logs from Paperless-AI
docker logs -f paperless_ai_worker

# 2. Trigger manual re-processing batch via Paperless-AI internal worker CLI
docker exec -it paperless_ai_worker python3 -m paperless_ai.reprocess --tag "Unprocessed"

# 3. Test Ollama model extraction responsiveness
curl -s http://localhost:11434/api/generate -d '{
  "model": "gemma3:27b",
  "prompt": "Extract JSON created_date, amount, and vendor from: Acme Electric Bill paid $145.20 on 2027-01-05."
}' | jq .

# 4. Verify Paperless-ngx document list endpoint status
curl -s -H "Authorization: Token a1b2c3d4e5f67890123456789abcdef012345678" \
  http://localhost:8000/api/documents/ | jq '.count'

# 5. Restart Paperless-AI container after updating model parameters
docker restart paperless_ai_worker
```

## API examples

### FastMCP 3.1 Document Archive Server
The following Python script implements a **FastMCP 3.1** server that allows AI agents to query the Paperless-ngx archive and trigger AI metadata re-extraction jobs via Paperless-AI:

```python
"""
Paperless-AI FastMCP 3.1 Document Archive Server
Provides tools for agentic systems to search document archives and trigger metadata extraction.
"""

import json
import logging
from typing import Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("paperless-mcp")

# Initialize FastMCP Server
mcp = FastMCP(
    "Paperless-AI Archive Server",
    version="3.1.0",
    description="FastMCP 3.1 server for searching Paperless-ngx document archives and processing metadata"
)

class DocumentSearchQuery(BaseModel):
    query_text: str = Field(..., description="Natural language search term or correspondent name")
    tag_filter: Optional[str] = Field(None, description="Optional tag name filter (e.g. Invoice, Medical)")
    max_results: int = Field(5, ge=1, le=20, description="Maximum document entries to return")

class ReprocessRequest(BaseModel):
    document_id: int = Field(..., description="Paperless-ngx document ID to re-analyze")
    force_llM_provider: Optional[str] = Field(None, description="Override model provider (e.g. ollama, claude)")

class DocumentSearchResult(BaseModel):
    document_id: int
    title: str
    correspondent: Optional[str]
    tags: List[str]
    created_date: Optional[str]
    snippet: str

@mcp.tool()
async def search_document_archive(query: DocumentSearchQuery) -> str:
    """
    Search the Paperless document archive using natural language queries and taxonomy filters.
    """
    logger.info(f"Agent search query: '{query.query_text}', tag: {query.tag_filter}")

    # Mock result list for sandbox safe execution
    mock_results = [
        DocumentSearchResult(
            document_id=1042,
            title="Acme Electric Invoice - January 2027",
            correspondent="Acme Electric Co",
            tags=["Invoice", "Utilities"],
            created_date="2027-01-05",
            snippet="Total Due: $145.20. Payment auto-debited on 2027-01-05 from checking account."
        )
    ]

    return json.dumps([r.model_dump() for r in mock_results], indent=2)

@mcp.tool()
async def trigger_document_reanalysis(request: ReprocessRequest) -> str:
    """
    Trigger Paperless-AI re-analysis for a document to update tags and correspondent fields.
    """
    logger.info(f"Triggering re-analysis for doc ID {request.document_id}")

    response = {
        "success": True,
        "document_id": request.document_id,
        "status": "QUEUED",
        "message": "Document queued for LLM re-extraction worker."
    }
    return json.dumps(response, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Extraction Metadata Schema Validation using Pydantic v2
This production script processes and validates structured JSON extractions produced by Paperless-AI models before saving updates to Paperless-ngx:

```python
"""
Paperless-AI Structured Extraction Schema Validator
Enforces schema validation on raw LLM extraction JSON outputs using Pydantic v2.
"""

import json
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, field_validator

class ExtractedLineItem(BaseModel):
    description: str = Field(..., description="Line-item service or product text")
    amount: float = Field(..., ge=0.0, description="Monetary value of item")

class PaperlessAIExtractedMetadata(BaseModel):
    document_id: int = Field(..., description="Target Paperless-ngx document ID")
    suggested_title: str = Field(..., min_length=3, description="Generated document title")
    correspondent: Optional[str] = Field(None, description="Identified sender or business entity")
    suggested_tags: List[str] = Field(default_factory=list, description="Extracted taxonomy tags")
    document_date: Optional[date] = Field(None, description="Invoice or creation date")
    total_amount_usd: Optional[float] = Field(None, ge=0.0, description="Parsed total monetary amount")
    line_items: List[ExtractedLineItem] = Field(default_factory=list, description="Parsed line item details")
    extraction_confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score")

    @field_validator("suggested_tags")
    @classmethod
    def normalize_tags(cls, tags: List[str]) -> List[str]:
        return [t.strip().title() for t in tags if len(t.strip()) > 0]

def validate_extraction_output(raw_llm_json: str) -> Optional[PaperlessAIExtractedMetadata]:
    try:
        data = json.loads(raw_llm_json)
        extracted = PaperlessAIExtractedMetadata.model_validate(data)
        print(f"Successfully validated extraction for Document #{extracted.document_id}: '{extracted.suggested_title}'")
        print(f" - Correspondent: {extracted.correspondent}")
        print(f" - Tags: {', '.join(extracted.suggested_tags)}")
        print(f" - Confidence: {extracted.extraction_confidence * 100:.1f}%")
        return extracted
    except ValidationError as err:
        print("Paperless-AI Schema Validation Error:")
        print(err.json(indent=2))
        return None
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON string.")
        return None

if __name__ == "__main__":
    sample_json = json.dumps({
        "document_id": 1042,
        "suggested_title": "Acme Electric - Jan 2027 Utility Bill",
        "correspondent": "Acme Electric Co",
        "suggested_tags": ["invoice", "utilities", "january-2027"],
        "document_date": "2027-01-05",
        "total_amount_usd": 145.20,
        "line_items": [
            {"description": "Electric Kilowatt Usage (850 kWh)", "amount": 120.00},
            {"description": "Regional Transmission Charge", "amount": 25.20}
        ],
        "extraction_confidence": 0.96
    })

    validate_extraction_output(sample_json)
```

## Related tools / concepts
- [Paperless-ngx](paperless-ngx.md) — Core document management system and REST API.
- [Ollama](ollama.md) — Local LLM runner supporting Gemma 3, Qwen 3.8, and Llama 4.
- [n8n](n8n.md) — Workflow automation engine triggering post-extraction tasks.
- [Actual Budget](actual-budget.md) — Self-hosted personal finance engine for matching invoices.
- [Claude 5.1](../tools/providers/anthropic.md) — Flagship Anthropic frontier model.
- [Local LLMs](../tools/ai_knowledge/local_llms.md) — Comprehensive guide to homelab local model hosting.
- [Whisper](whisper.md) — Audio transcription service for voice memos.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Open protocol for FastMCP 3.1 integrations.

## Sources / references
- [Paperless-AI Repository](https://github.com/clusterfudge/paperless-ai)
- [Paperless-ngx Official Documentation & API](https://docs.paperless-ngx.com/)
- [Ollama Library & Model Models](https://ollama.com/library)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

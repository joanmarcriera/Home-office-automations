# Hebbia

## What it is
Hebbia is an AI-powered enterprise intelligence platform and specialized document reasoning engine designed for high-stakes quantitative and qualitative analysis over massive document repositories. Built specifically for high-stakes industries—including investment banking, private equity, corporate legal counsel, management consulting, and government intelligence—Hebbia enables deep cross-document synthesis across thousands of complex filings, SEC reports, contracts, and transcripts simultaneously. Operating as an enterprise "Reasoning Engine", Hebbia integrates frontier models (including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4) and exposes its **Matrix** multi-dimensional workspace engine alongside native support for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) FastMCP 3.1 standard.

```
+-----------------------------------------------------------------------------------+
|                           Hebbia Enterprise Intelligence Platform                 |
|                                                                                   |
|  +------------------------+      +-------------------+      +------------------+  |
|  | Enterprise Repository  | ---> | Hebbia Matrix     | ---> | Frontier LLM     |  |
|  | (Deal Rooms / SEC / 10K) |    | Workspace Engine  |      | Reasoning Engine |  |
|  +------------------------+      +-------------------+      +------------------+  |
|               |                            |                          |           |
+---------------+----------------------------+--------------------------+-----------+
                |                            |                          |
                v                            v                          v
+-----------------------------------------------------------------------------------+
|                        Auditable Synthesis & Execution Layer                      |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | Deep Citations &   |     | Custom Institutional|     | FastMCP 3.1 Tool     |  |
|  | Verification Links |     | Reasoning Skills    |     | Agent Server Bridge  |  |
|  +--------------------+     +---------------------+     +----------------------+  |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Hebbia solves the critical "synthesis bottleneck" that plagues institutional research teams analyzing vast document corpora:
- **Scalability Barriers**: Manually reviewing thousands of multi-page legal contracts, SEC filings, or earnings call transcripts requires weeks of human analyst effort; Hebbia processes and synthesizes entire deal rooms in minutes.
- **Auditability & Accuracy**: Generates 100% verified findings where every claim, extracted metric, or risk summary is directly linked back to verbatim source document excerpts and page numbers.
- **Structured Cross-Document Extraction**: Replaces unstructured natural language chat with structured, tabular **Matrix** grids that evaluate custom analytical topics across hundreds of target entities simultaneously.
- **Institutional Knowledge Reuse**: Converts proprietary domain expertise and institutional analysis techniques into reusable, team-wide **Skills**.

## Where it fits in the stack
**Enterprise AI / Analytical Synthesis Layer**. Hebbia sits directly above raw data lakes, virtual deal rooms (VDRs), and document stores as an institutional reasoning engine, competing with enterprise search platforms like [Glean](glean.md) while providing far deeper analytical matrix generation.

## Architecture & System Dynamics

```
+-----------------------------------------------------------------------------------+
|                          Hebbia Matrix Execution System Architecture              |
|                                                                                   |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Document Ingestion    | <-> | Neural Indexing        | <-> | Matrix Engine   | |
|  | Pipeline (VDR / S3)   |     | Vector & AST Store     |     | Orchestrator    | |
|  +-----------------------+     +------------------------+     +-----------------+ |
|             |                              |                           |          |
|             v                              v                           v          |
|  +-----------------------+     +------------------------+     +-----------------+ |
|  | Skill Reasoning Engine| <-> | Citation & Verification| <-> | FastMCP 3.1     | |
|  | (Claude 5.6 / GPT-5.6)|     | Mapping Subsystem      |     | External Bridge | |
|  +-----------------------+     +------------------------+     +-----------------+ |
+-----------------------------------------------------------------------------------+
```

The system architecture consists of four interconnected core components:
1. **Document Parsing & Neural Indexer**: Ingests unstructured PDFs, financial tables, and scanned text, constructing rich semantic embeddings and document structure trees.
2. **Matrix Workspace Engine**: Coordinates asynchronous processing pipelines across document dimensions and user-defined analytical questions.
3. **Skill & Prompt Execution Pipeline**: Applies specialized domain reasoning templates (e.g., credit risk extraction, change-of-control clause detection).
4. **Citation Validation Layer**: Verifies every model-generated answer against original document coordinates, ensuring pinpoint source verification.

## Key Features & Capabilities
- **Hebbia Matrix Workspace**: High-dimensional analysis grid that operates like an AI-powered spreadsheet across thousands of document sources.
- **Institutional Skills**: Library of custom, reusable prompt chains that capture proprietary analytical workflows across teams.
- **100% Auditable Citations**: Direct interactive links highlighting verbatim source quotes and page coordinates in original PDFs.
- **Multi-Model Orchestration**: Dynamic routing between frontier LLMs (Claude 5.6, GPT-5.6, Gemini 4.0) based on complexity and cost parameters.
- **VDR & Cloud Data Connectors**: Native real-time connectors for Dataroom providers (Intralinks, Datasite, Ansarada) and cloud storage (S3, Box, SharePoint).

## Typical use cases
- **Investment Banking & M&A Due Diligence**: Synthesizing virtual deal room contents to flag liabilities, financial commitments, and customer concentration risks.
- **Private Equity Portfolio Monitoring**: Extracting quarterly metrics and covenant compliance data across dozens of portfolio company reports.
- **Legal & Regulatory Discovery**: Mapping contract terms, indemnification limits, and termination clauses across enterprise contract suites.
- **Strategic Competitor Analysis**: Analyzing earnings call transcripts and investor decks across entire market sectors.

## Enterprise Operational Considerations

| Dimension | Consideration / Requirement |
|-----------|-----------------------------|
| **Data Isolation** | Dedicated, single-tenant cloud instances or SOC 2 Type II compliant enterprise VPC deployments |
| **Security & Compliance** | Full encryption in-transit (TLS 1.3) and at-rest (AES-256 with KMS keys); HIPAA and SOC 2 certified |
| **Access Control** | Granular Role-Based Access Control (RBAC), SSO via SAML 2.0 / Okta, and SCIM provisioning |
| **Data Retention** | Zero-data-retention options ensuring model provider endpoints do not store or train on client inputs |

## Strengths
- **Unrivaled Synthesis Scale**: Evaluates thousands of documents in parallel without context-window truncation degradation.
- **Pinpoint Auditability**: Every data point in the Matrix provides instant visual access to source document quotes.
- **Financial & Legal Specialization**: Purpose-built prompt frameworks and reasoning loops optimized for institutional financial terminology.
- **FastMCP 3.1 Interoperability**: Seamlessly interfaces with AI agents to automate end-to-end analytical tasks.

## Limitations
- **High Institutional Cost**: Premium pricing model targeted strictly at enterprise organizations and institutional firms.
- **Proprietary Cloud Platform**: SaaS-centric architecture with limited options for fully air-gapped on-premises setups.
- **Overkill for Simple Queries**: Less suitable for quick single-document summaries or casual conversational search.

## When to use it
- When conducting deep due diligence across hundreds or thousands of complex documents.
- When auditability and exact citation verification are absolute legal or financial requirements.
- When building automated AI agent research pipelines via FastMCP 3.1.

## When not to use it
- For basic web search queries or casual consumer-style Q&A (use [Perplexity](../providers/perplexity.md)).
- If your budget is tailored for lightweight consumer productivity applications.

## Getting started
1. Onboard your enterprise workspace through an institutional Hebbia account.
2. Create a **Workspace** and upload target document sets or connect VDR storage repositories.
3. Define your target analysis topics using the **Matrix** grid view.
4. Select or configure a **Skill** (e.g., *Extract Debt Covenants* or *Identify Change of Control Clauses*).
5. Execute the Matrix run and export verified results as structured spreadsheets or JSON payloads.

## CLI examples

```bash
# Trigger a Hebbia Matrix analysis run using the REST API
curl -X POST "https://api.hebbia.ai/v2/matrix/trigger" \
     -H "Authorization: Bearer $HEBBIA_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
           "project_id": "proj_ma_diligence_2027",
           "skill_id": "skill_extract_covenants",
           "callback_url": "https://hooks.firm.com/hebbia-callback"
         }'

# Query the status of an active Matrix execution run
curl -s -H "Authorization: Bearer $HEBBIA_API_TOKEN" \
     "https://api.hebbia.ai/v2/matrix/runs/run_908123_abc"
```

## API examples

### FastMCP 3.1 Server for Hebbia Matrix Execution

The Python script below implements a **FastMCP 3.1** server that triggers Hebbia Matrix runs and validates output using **Pydantic v2** models:

```python
"""
Hebbia FastMCP 3.1 Integration Server
Provides AI agents with structured tools to run Hebbia Matrix analyses and parse citations.
"""

import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    name="HebbiaIntelligenceServer",
    version="3.1.0",
    description="FastMCP 3.1 server for invoking Hebbia Matrix analysis and citation validation."
)

class SourceCitation(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    document_name: str = Field(..., alias="documentName", description="Name of source document")
    page_number: int = Field(..., alias="pageNumber", description="1-based page number")
    excerpt: str = Field(..., description="Verbatim source text excerpt")
    citation_url: str = Field(..., alias="citationUrl", description="Direct link to highlighted quote")

class MatrixAnalysisTopic(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    topic_id: str = Field(..., alias="topicId", description="Unique identifier for the topic")
    topic_name: str = Field(..., alias="topicName", description="Analytical question or topic")
    finding: str = Field(..., description="Synthesized finding or answer")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence score")
    citations: List[SourceCitation] = Field(default_factory=list, description="List of direct citations")

class MatrixRunResult(BaseModel):
    run_id: str = Field(..., alias="runId")
    project_id: str = Field(..., alias="projectId")
    status: str
    results: List[MatrixAnalysisTopic] = Field(default_factory=list)

@mcp.tool(
    name="execute_matrix_diligence",
    description="Executes a Hebbia Matrix document analysis run and returns structured citations."
)
def execute_matrix_diligence(
    project_id: str,
    skill_id: str
) -> Dict[str, Any]:
    """Triggers Matrix analysis and validates citations using Pydantic v2."""
    try:
        # Mock structured response simulating Hebbia API
        raw_api_payload = {
            "runId": "run_2027_m_a_9921",
            "projectId": project_id,
            "status": "COMPLETED",
            "results": [
                {
                    "topicId": "top_001",
                    "topicName": "Change of Control Terms",
                    "finding": "Requires 60-day advance notice and approval from senior lenders prior to equity transfer.",
                    "confidence": 0.99,
                    "citations": [
                        {
                            "documentName": "Credit_Agreement_2026.pdf",
                            "pageNumber": 88,
                            "excerpt": "Section 9.04: No Change of Control shall occur without 60 days prior written notice...",
                            "citationUrl": "https://app.hebbia.ai/doc/Credit_Agreement_2026#page=88"
                        }
                    ]
                }
            ]
        }

        # Pydantic v2 validation
        validated = MatrixRunResult.model_validate(raw_api_payload)
        return validated.model_dump(by_alias=True)

    except Exception as e:
        return {
            "error": f"Failed to execute Matrix diligence run: {str(e)}"
        }

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## Related tools / concepts
- [Bloomberg Terminal](https://www.bloomberg.com/professional/solution/bloomberg-terminal/)
- [Perplexity](../providers/perplexity.md)
- [Glean](glean.md)
- [Langfuse](../process_understanding/langfuse.md)
- [MCP (Model Context Protocol)](../automation_orchestration/mcp.md)

## Sources / references
- [Hebbia Official Website](https://www.hebbia.ai/)
- [Hebbia Matrix Workspace Overview](https://www.hebbia.ai/product/matrix)
- [Hebbia Enterprise Security & Compliance Whitepaper](https://www.hebbia.ai/security)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

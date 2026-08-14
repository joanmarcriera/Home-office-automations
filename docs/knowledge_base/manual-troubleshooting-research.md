# Manual Troubleshooting Assistant Research

## What it is
This research evaluates the user interface and orchestration layer for a chat-based assistant designed to troubleshoot household appliances using scanned manuals. It leverages Retrieval-Augmented Generation (RAG) over a local vector database.

Key components evaluated in early January 2027:
- **UI Frameworks**: Comparison between Open WebUI and Streamlit for family use.
- **RAG Orchestration**: Integration with Ollama and local embedding models.
- **Agentic Loops**: Implementation of self-healing loops for autonomous remediation.
- **Schema Validation**: Enforcement of client-server and tool payloads using strict Pydantic v2 schemas.

## What problem it solves
Scanned manuals are often long, poorly indexed, and difficult to search during a "household emergency" (e.g., a leaking dishwasher). This assistant provides immediate, natural language answers to specific troubleshooting questions, reducing time-to-fix.

## Where it fits in the stack
**User Interface / Orchestration Layer**. It connects the user to local LLMs (Claude 5.1, Gemini 4.0 Pro/Flash, or GPT-5.5) and the Vector DB containing chunked manual data.

## Typical use cases
- Interpreting cryptic error codes on the oven or washing machine.
- Finding maintenance schedules (e.g., "how often to clean the dryer vent?").
- Step-by-step guidance for minor repairs or setup.
- Comparing troubleshooting steps across different model generations.

## Strengths
- **Accessibility**: Family members can ask questions via phone or tablet without technical knowledge.
- **Privacy**: Entirely self-hosted when using local LLMs and embeddings.
- **Accuracy**: RAG reduces hallucinations by grounding the LLM in the actual text of the manual.
- **Frontier Support**: Optimized for Claude 5.1 and GPT-5.5 reasoning patterns.

## Limitations
- **OCR Quality**: Poorly scanned manuals may lead to incorrect information retrieval.
- **Complex Diagrams**: LLMs may struggle to interpret "Figure 1.2" if the diagram isn't correctly indexed or provided as VLM context.

## When to use it
- For any household appliance with a digital or physical manual.
- When troubleshooting non-dangerous issues that don't require immediate professional intervention.

## When not to use it
- **Dangerous Repairs**: High-voltage electrical work or gas line issues should always be handled by professionals.
- **Time-Critical Safety**: Do not use the assistant if there is a fire or immediate safety risk.

## Getting started
### Environment Setup
1. Ensure Open WebUI or Streamlit is installed and connected to your local LLM provider (e.g., Ollama).
2. Prepare your appliance manuals in PDF format.
3. Configure your vector database (e.g., ChromaDB) for document ingestion.

### Basic Assistant Query
```bash
# Example query to the troubleshooting assistant via CLI
python3 scripts/home_admin_agent.py "Why is my Bosch dishwasher flashing E24?"
```

## CLI examples
The research implementation can be tested and managed via CLI.

```bash
# Start the reference implementation (Streamlit-based)
streamlit run scripts/home_admin_ui.py

# Index a new manual into the vector database
python3 scripts/process_manuals.py --file manuals/bosch_dishwasher.pdf

# Test the RAG retrieval without the UI
python3 scripts/verify_manual_retrieval.py "E24 error code meaning"
```

## API examples
The assistant can be integrated into larger workflows via API using strict Pydantic v2 models for schema validation.

### 1. Robust Query Validation Script (Python)
This script demonstrates validation of troubleshooting inquiries and replies using Pydantic v2 schemas.

```python
import requests
from typing import List, Optional
from pydantic import BaseModel, Field

class ApplianceIssue(BaseModel):
    appliance_name: str = Field(..., description="E.g., Bosch Dishwasher Series 800")
    error_code: str = Field(..., description="Error code shown on appliance, e.g., E24")
    description: Optional[str] = Field(None, description="Optional symptoms description")

class TroubleshootingQuery(BaseModel):
    issue: ApplianceIssue
    context_tags: List[str] = Field(default_factory=lambda: ["manuals"])

class TroubleshootingResponse(BaseModel):
    error_code: str
    remediation_steps: List[str] = Field(..., description="Step-by-step resolution instructions")
    confidence_score: float = Field(..., ge=0.0, le=1.0)

def get_troubleshooting_help(query: TroubleshootingQuery) -> TroubleshootingResponse:
    """Queries the local troubleshooting engine and validates the response schema."""
    url = "http://localhost:8000/api/chat"

    # Payload is automatically serialized to validated JSON using model_dump_json()
    response = requests.post(url, data=query.model_dump_json(), headers={"Content-Type": "application/json"})
    response.raise_for_status()

    # Parse and enforce response schema
    return TroubleshootingResponse.model_validate(response.json())

if __name__ == "__main__":
    # Example construction of validated payload
    query_payload = TroubleshootingQuery(
        issue=ApplianceIssue(
            appliance_name="Bosch Dishwasher Series 800",
            error_code="E24",
            description="Fails to drain water completely"
        )
    )
    print("Payload validated successfully:", query_payload.model_dump())
```

### 2. Dynamic Troubleshooting using MCP 3.1 Task Protocol
Under the early January 2027 standard, we represent a troubleshooting task dynamically using the MCP 3.1 Task Protocol JSON payload.

```json
{
  "$schema": "https://modelcontextprotocol.org/schemas/mcp-3.1-task.json",
  "task": {
    "id": "troubleshoot-dishwasher-0831",
    "name": "Analyze Dishwasher Error",
    "parameters": {
      "appliance": "Bosch Dishwasher Series 800",
      "error_code": "E24",
      "rag_index": "household_manuals_v2"
    },
    "steps": [
      {
        "name": "query-vector-db",
        "tool": "chromadb-search",
        "arguments": {
          "query": "E24 error drain pump drain hose blockage",
          "limit": 3
        }
      },
      {
        "name": "generate-remediation",
        "tool": "claude-5-1-reason",
        "arguments": {
          "prompt": "Based on retrieved chunks: {{steps.query-vector-db.output}}, construct clear, illustrated step-by-step instructions to clear the E24 error."
        }
      }
    ]
  }
}
```

## Related tools / concepts
- [Open WebUI](../services/open-webui.md)
- [Ollama](../services/ollama.md)
- [Paperless-ngx](../services/paperless-ngx.md)
- [RAG Pattern](./patterns/rag-pattern.md)
- [n8n](../services/n8n.md)
- [ChromaDB](./vector-db-comparison.md)
- [Self-Healing Agent](./self-healing-agent-research.md)
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md)

## Sources / References
- [Open WebUI Documentation](https://docs.openwebui.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Self-Healing Agentic Loops for Homelab Automation](https://riera.co.uk/blog/self-healing-agents)

## Contribution Metadata
- Last reviewed: 2027-01-05
- Confidence: high

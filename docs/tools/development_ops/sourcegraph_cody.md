# Sourcegraph Cody

## What it is
Cody is an enterprise-grade AI coding assistant developed by Sourcegraph that leverages a comprehensive "Code Graph" to provide deep, context-aware assistance across entire multi-repo codebases. As of early 2027, Cody has matured into an agentic "Code Intelligence Platform", capable of autonomous multi-repository reasoning, semantic context retrieval via **FastMCP 3.1**, and native execution with frontier models such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, **Llama 4**, **Gemma 4**, and **Qwen 3.6 VL**.

## What problem it solves
It solves the "context fragmentation" and "knowledge silo" problem in massive enterprise repositories. Traditional coding assistants operate file-by-file or are constrained to a single active workspace folder. Cody integrates directly with Sourcegraph's global index, allowing it to understand complex cross-repository dependencies, architectural patterns, and undocumented internal APIs. It acts as a bridge between the generalist knowledge of frontier models and the complex, multi-tenant codebase realities of enterprise organizations.

## Where it fits in the stack
**Category**: Tool / Development & Ops / AI-assisted Coding. Cody functions as the "Code Intelligence and Enterprise Context Plane", feeding precise repository-level embeddings and syntax trees to local editor chats and remote autonomous developer agents alike.

## Typical use cases
- **Multi-Repository Architecture Search**: Asking natural language questions that span across separate microservice codebases (e.g. tracking API request paths).
- **Agentic Context Enrichment**: Serving as a FastMCP 3.1 server backend to feed high-fidelity code fragments to standalone agent frameworks like OpenHands, Cline, or Claude Code.
- **Enterprise Developer Onboarding**: Allowing newly onboarded engineers to quickly understand complex system flows and database schemas through conversational search.
- **Conforming to Internal Coding Standards**: Customizing Cody prompts to enforce specific company-wide coding rules, design patterns, and deprecation notices during code generation.

## Strengths
- **Unrivaled Semantic Search**: Powered by Sourcegraph's hybrid search engine, combining keyword, vector embeddings, and precise LSIF/SCIP code graphs.
- **Model Agnostic Flexibility**: Easily switch between frontier models (Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4) to match the cognitive requirements of the task.
- **VPC and On-Premises Compliance**: Robust on-prem deployment options with strict enterprise-grade permissions, security rules, and absolute zero-data-retention guarantees.
- **Native FastMCP 3.1 Protocol**: Fully implements MCP client/server specifications to dynamically stream external schemas and execute verified tools.

## Limitations
- **High Infrastructure Footprint**: Full codebase indexing and context graph features require a connected, fully synced Sourcegraph server instance.
- **Configuration Overhead**: Tuning repository filters, managing embedding generation, and configuring enterprise authentication requires dedicated administrator resources.
- **Context Fetch Latency**: Querying global indices on remote self-hosted enterprise clusters can introduce higher network round-trip latency compared to local-only vector DBs.

## When to use it
- In medium-to-large enterprise development teams operating across extensive, multi-repository microservice architectures.
- When you need a coding assistant that understands your organization's custom internal libraries and strictly adheres to proprietary design patterns.
- If you have an existing Sourcegraph subscription and want to maximize value from your pre-existing code index.

## When not to use it
- For small, single-repository projects where lightweight, local-first tools like Codeium or Cursor provide instantaneous setup.
- If you do not have (and do not intend to configure) a centralized Sourcegraph server instance.
- For isolated scripting tasks where global codebase context is not a critical requirement.

## Getting started

### Extension Installation
1. Install the official **Cody AI** extension from your IDE's marketplace (VS Code, JetBrains, or Cursor).
2. Connect the extension to your **Sourcegraph Enterprise** portal URL, or log in to **Sourcegraph Cloud**.
3. Once authenticated, Cody will read the server-side code index and begin offering context-aware autocomplete and chat.

### Building a Local Index
For individual developers wanting local-first repository embeddings without a central server:
```bash
# Install the Cody CLI helper
npm install -g @sourcegraph/cody

# Build local vector embeddings for the active project
cody index create --src ./my-project-root
```

## CLI examples

### Conversational Repository Querying
Query your indexed codebase directly from your terminal using standard model overrides:
```bash
# Query S3 integration logic within the indexed repos
cody chat -m "Where is the retry logic for the S3 intake service?"

# Ask Cody to explain high-level project structure and flow
cody explain --high-level
```

### Server Token Authentication
Authenticate your terminal helper against your enterprise instance headlessly:
```bash
cody login --endpoint https://sourcegraph.company.com --token sgp_39b362198fa064_example
```

## API examples

### Programmatic Context Retrieval and Pydantic v2 Validation
The following Python script executes a semantic codebase context search against the Sourcegraph Cody API, parsing and validating the retrieved code chunks with strict Pydantic v2 schemas.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

# Define modern Pydantic v2 schemas for Cody context output
class CodyContextDocument(BaseModel):
    filepath: str = Field(..., description="Repository-relative file path of the retrieved chunk")
    content: str = Field(..., description="Actual text content of the retrieved chunk")
    score: float = Field(..., ge=0.0, le=1.0, description="Cosine similarity or retrieval score of this document chunk")
    language: str = Field("python", description="Programming language of the code fragment")

class CodyContextResponse(BaseModel):
    query: str = Field(..., description="The semantic search query executed")
    documents: List[CodyContextDocument] = Field(default_factory=list, description="List of highly relevant code fragments retrieved from Sourcegraph")
    total_chunks: int = Field(..., description="Total count of retrieved fragments")

# Simulated API response payload from Cody's fast retrieval endpoint
raw_response = {
    "query": "How are database connections pooled in our repository?",
    "total_chunks": 2,
    "documents": [
        {
            "filepath": "lib/db/pool.py",
            "content": "class ConnectionPool:\n    def __init__(self, size=10):\n        self.size = size",
            "score": 0.94,
            "language": "python"
        },
        {
            "filepath": "config/settings.py",
            "content": "DB_POOL_SIZE = 15\nDB_TIMEOUT = 30",
            "score": 0.82,
            "language": "python"
        }
    ]
}

try:
    validated_response = CodyContextResponse(**raw_response)
    print("Cody Context retrieved and successfully validated via Pydantic v2!")
    print(f"Query: {validated_response.query}")
    print(f"Highest similarity score: {validated_response.documents[0].score}")
    for doc in validated_response.documents:
         print(f" - {doc.filepath} ({doc.language})")
except ValidationError as e:
    print(f"Payload validation error: {e.json(indent=2)}")
```

### Configured FastMCP 3.1 Context Server Connection
Hook Cody's indexing engine up to other agentic platforms like OpenHands or Claude Desktop via Model Context Protocol:
```json
{
  "mcpServers": {
    "sourcegraph-cody": {
      "command": "cody-mcp",
      "args": [
        "--endpoint", "https://sourcegraph.company.com",
        "--access-token", "sgp_39b362198fa064_example",
        "--enable-telemetry", "false"
      ]
    }
  }
}
```

## Related tools / concepts
- [Codeium](./codeium.md) — High-performance AI coding platform.
- [Cursor](./cursor.md) — Popular AI-first code editor.
- [OpenHands](./openhands.md) — Highly capable autonomous software agent.
- [Aider](./aider.md) — Terminal-native pair programmer.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Universal protocol for model-tool interactions.
- [Filesystem Context](../../knowledge_base/patterns/filesystem-context.md) — Architectural pattern for local directories.
- [RAG Pattern](../../knowledge_base/patterns/rag.md) — Core pattern for data-grounded AI reasoning.
- [CodeGraphContext](../automation_orchestration/codegraphcontext.md) — Graph-based source code indexing structures.

## Sources / references
- [Sourcegraph Cody Official Site](https://about.sourcegraph.com/cody)
- [Cody Platform Documentation](https://sourcegraph.com/docs/cody)
- [Sourcegraph GitHub Repository](https://github.com/sourcegraph/cody)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

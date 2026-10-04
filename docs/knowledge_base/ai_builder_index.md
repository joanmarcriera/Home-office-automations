# AI Builder Index

## What it is
The **AI Builder Index** is the primary architectural discovery portal and capability mapping framework for the automation, AI engineering, and KnowledgeOps stack documented across this repository. It functions as an outcome-driven directory, taxonomy, and decision matrix that routes systems architects, agentic engineers, and platform developers to the precise tools, services, FastMCP 3.1 protocol servers, and architectural patterns required to achieve specific system capabilities. As of early 2027, the index is deeply optimized for the **FastMCP 3.1** framework and the **MCP 3.1 Task Protocol** specification, enabling seamless composition across frontier reasoning models ([Claude 5.6](../tools/providers/anthropic.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md)), open weights ([Qwen 3.6 VL](../tools/ai_knowledge/qwen.md), [Gemma 4](../tools/ai_knowledge/local_llms.md), [DeepSeek-V4](../tools/providers/deepseek.md)), and local inference engines ([LocalAI](../tools/infrastructure/localai.md), [Ollama](../services/ollama.md), [ExLlamaV2](../tools/infrastructure/exllamav2.md)).

## What problem it solves
Modern AI engineering suffers from severe fragmentation and discovery friction across disparate agent frameworks, vector database backends, tool protocols, and execution environments. Without a unified taxonomy and structural index:
- **Architectural Fragmentation**: Teams re-invent workflow patterns, tool interfaces, and security perimeters rather than leveraging proven standards.
- **Protocol Incompatibility**: Integrating legacy REST/GraphQL services into agent loops requires ad-hoc wrapper code instead of standard Model Context Protocol schemas.
- **Inference Misalignment**: Selecting sub-optimal models or execution engines leads to cost overruns, latency bottlenecks, or data privacy non-compliance.
- **Decision Fatigue**: Engineers face dozens of overlapping options (e.g., [LangGraph](../tools/frameworks/langgraph.md) vs. [Ag2](../tools/frameworks/ag2.md) vs. [OpenClaw](../tools/development_ops/openclaw.md) vs. [Symphony](../tools/agents/symphony.md)).

The AI Builder Index eliminates this friction by organizing the entire KnowledgeOps technical stack into **Goal-Oriented Outcome Buckets**, providing normative architectural defaults, and detailing production-grade FastMCP 3.1 server patterns for every core domain.

## Where it fits in the stack
```
+-----------------------------------------------------------------------------------+
|                            KNOWLEDGE OPS DISCOVERY LAYER                          |
|                             docs/knowledge_base/ai_builder_index.md               |
+-----------------------------------------------------------------------------------+
          |                                  |                                  |
          v                                  v                                  v
+-----------------------+          +-----------------------+          +-----------------------+
|  FRAMEWORKS & AGENTS  |          |  DATA & INFERENCE     |          | INTEGRATION & DEPLOY  |
|  - FastMCP 3.1 Server |          |  - mem0 / Weaviate    |          |  - Docker / K3s       |
|  - LangGraph / AG2    |          |  - Ollama / ExLlamaV2 |          |  - Vault / Authentik  |
|  - OpenClaw / Cline   |          |  - Tavily / OpenPangu |          |  - n8n / Airflow      |
+-----------------------+          +-----------------------+          +-----------------------+
          |                                  |                                  |
          +----------------------------------+----------------------------------+
                                             |
                                             v
+-----------------------------------------------------------------------------------+
|                        MCP 3.1 PROTOCOL & INFERENCE INFRASTRUCTURE                 |
|            (JSON-RPC 2.0 / SSE / Stdio / Tool Call Execution Engine)               |
+-----------------------------------------------------------------------------------+
```

The AI Builder Index sits at the apex of the documentation hierarchy. It serves as the primary router between the high-level home catalog ([Home Index](../index.md)) and the granular technical implementations stored in `docs/tools/`, `docs/services/`, and `docs/playbooks/`.

## Architectural Topology & Classification Taxonomy

The repository taxonomy is structured across six primary operational dimensions. The index provides direct mapping across these layers to ensure coherent system design:

```
+----------------------------------------------------------------------------------------------------+
|                                      AI BUILDER TAXONOMY MATRIX                                     |
+--------------------------+----------------------------------+--------------------------------------+
| Layer                    | Primary Focus                    | Key Ecosystem Components             |
+--------------------------+----------------------------------+--------------------------------------+
| 1. Orchestration & Agents| Multi-step execution & planning  | FastMCP 3.1, LangGraph, OpenClaw,    |
|                          |                                  | Cline, AG2, Smolagents, Letta        |
+--------------------------+----------------------------------+--------------------------------------+
| 2. Context & Memory      | Epistemic storage & retrieval    | mem0, Weaviate, GraphRAG,            |
|                          |                                  | Arize-AI, Langfuse, Qdrant           |
+--------------------------+----------------------------------+--------------------------------------+
| 3. Tool Protocols (MCP)  | Standardized schema execution    | Vault-MCP, Playwright-MCP,           |
|                          |                                  | ServiceNow-MCP, Makefile-MCP          |
+--------------------------+----------------------------------+--------------------------------------+
| 4. Local & Edge Inference| Sovereign, low-latency models    | LocalAI, Ollama, ExLlamaV2,          |
|                          |                                  | Llamafile, ROCm, TGI                 |
+--------------------------+----------------------------------+--------------------------------------+
| 5. Security & Identity   | Access governance & secrets      | Authentik, HashiCorp Vault,          |
|                          |                                  | Okta, Gitleaks, Cal.com Security      |
+--------------------------+----------------------------------+--------------------------------------+
| 6. Service Automation    | Workflow execution engines       | n8n, Airflow, Rclone, Immich,        |
|                          |                                  | Paperless-AI, Prowlarr               |
+--------------------------+----------------------------------+--------------------------------------+
```

## Typical use cases
- **Multi-Agent Systems Design**: Selecting appropriate FastMCP 3.1 tool protocol bindings for agentic collaboration across heterogeneous models.
- **Enterprise Knowledge Integration**: Combining structured data sources with hybrid vector search (RAG) using [Weaviate](../tools/infrastructure/weaviate.md) and [mem0](../tools/agents/mem0.md).
- **Sovereign AI Infrastructure Deployment**: Configuring air-gapped, high-throughput local inference pipelines using [ExLlamaV2](../tools/infrastructure/exllamav2.md) and [Ollama](../services/ollama.md).
- **Identity & Protocol Governance**: Enforcing OAuth2/OIDC boundaries and granular capability permissions across MCP tool servers via [Authentik](../services/authentik.md) and [Vault-MCP](../tools/automation_orchestration/vault-mcp.md).
- **Automated Operations & CI/CD**: Interfacing agentic coding assistants ([Cline](../tools/agents/cline.md), [Roo-Code](../tools/agents/roo-code.md)) with automated test and deployment pipelines.

## Strengths
- **Protocol Standardization**: Built around FastMCP 3.1 and Model Context Protocol 3.1 schemas to ensure decoupled tool servers and client interoperability.
- **Production-Grade Schemas**: Provides validated Pydantic v2 schemas for tool indexing, agent routing, and metadata registries.
- **Deterministic Routing**: Clear decision matrices remove ambiguity when selecting between competing tools or frameworks.
- **Comprehensive Ecosystem Coverage**: Encompasses proprietary frontier APIs, open weights models, self-hosted services, and edge computing patterns.

## Limitations
- **Ecosystem Dynamics**: Fast-paced AI developments necessitate continuous index re-validation as model context limits and protocol capabilities evolve.
- **Meta-Document Abstraction**: Provides high-level operational maps and architectural defaults rather than line-by-line tool source code.
- **Opinionated Stack Defaults**: Prioritizes standard MCP 3.1 interfaces over non-standard proprietary REST APIs.

## When to use it
- When evaluating system requirements for new AI agent or automation projects.
- When selecting stack defaults for production deployments (e.g., choice of vector store, agent framework, or auth provider).
- When designing multi-tool MCP servers that require standard tool definition schemas and robust error handling.

## When not to use it
- When looking for specific command-line syntax for a single standalone tool (refer directly to the specific tool documentation file).
- When troubleshooting low-level kernel or GPU driver issues (refer to [ROCm](../tools/infrastructure/rocm.md) or infrastructure playbooks).

## Getting started

### Outcome Navigation & Stack Recommendations

| Operational Goal | Primary Entry Point | Secondary Stack Components | Target Architecture |
| :--- | :--- | :--- | :--- |
| **Autonomous Coding Agents** | [Roo-Code](../tools/agents/roo-code.md) / [Cline](../tools/agents/cline.md) | [Claude Code](../tools/development_ops/claude-code.md), [Playwright-MCP](../tools/automation_orchestration/playwright-mcp.md) | Local IDE + FastMCP 3.1 execution loop |
| **Enterprise RAG & Memory** | [mem0](../tools/agents/mem0.md) | [Weaviate](../tools/infrastructure/weaviate.md), [GraphRAG](../tools/frameworks/graphrag.md), [Tavily](../tools/providers/tavily.md) | Hybrid semantic retrieval + long-term memory |
| **Workflow Automation** | [n8n](../services/n8n.md) | [Vault-MCP](../tools/automation_orchestration/vault-mcp.md), [Authentik](../services/authentik.md) | Low-code engine + secure MCP credentials |
| **Local Private AI** | [Ollama](../services/ollama.md) | [LocalAI](../tools/infrastructure/localai.md), [ExLlamaV2](../tools/infrastructure/exllamav2.md), [ROCm](../tools/infrastructure/rocm.md) | Air-gapped GPU server + FastMCP gateway |
| **Agentic Web Scraping** | [Browser Use](../tools/automation_orchestration/browser-use.md) | [Playwright](../tools/development_ops/playwright.md), [OpenPangu](../tools/providers/openpangu.md) | Headless browser cluster + visual parse |

### Recommended Entry Cards

<div class="grid cards" markdown>

-   **Agentic Development & Coding**
    ---
    Explore [Roo-Code](../tools/agents/roo-code.md), [Cline](../tools/agents/cline.md), and [Claude Code](../tools/development_ops/claude-code.md) for self-healing code generation.

-   **Context & Enterprise RAG**
    ---
    Leverage [mem0](../tools/agents/mem0.md), [Weaviate](../tools/infrastructure/weaviate.md), and [GraphRAG](../tools/frameworks/graphrag.md) for scalable epistemic recall.

-   **Sovereign & Local AI**
    ---
    Deploy [Ollama](../services/ollama.md), [LocalAI](../tools/infrastructure/localai.md), and [ExLlamaV2](../tools/infrastructure/exllamav2.md) on private hardware.

-   **Security & Protocol Governance**
    ---
    Enforce identity via [Authentik](../services/authentik.md) and secrets isolation via [HashiCorp Vault](../tools/automation_orchestration/hashicorp-vault.md).

</div>

## CLI examples

You can query and validate the AI Builder Index and associated documentation using standard shell utilities and Python scripts:

```bash
# Search for FastMCP 3.1 protocol references across the builder index
grep -i "FastMCP 3.1" docs/knowledge_base/ai_builder_index.md

# Validate all document links across the AI builder index and knowledge base
python3 scripts/check_docs_contract.py docs/knowledge_base/ai_builder_index.md

# Perform catalog consistency audit across tools and data schemas
python3 scripts/check_catalog_consistency.py

# List all index entries classified under agent frameworks
grep -E "\[.*\]\(\.\./tools/(agents|frameworks)/.*\)" docs/knowledge_base/ai_builder_index.md
```

## API examples

Below is a complete FastMCP 3.1 server implementation demonstrating how the AI Builder Index can be exposed programmatically as a Model Context Protocol tool. This server allows agents to query repository tools, filter by capability, and retrieve structured architectural defaults:

```python
"""
FastMCP 3.1 Server for AI Builder Index Discovery & Tool Routing.
Exposes repository tooling catalog and architectural guidance to AI agents.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ai-builder-index", version="3.1.0")

class ToolCapabilityQuery(BaseModel):
    category: str = Field(
        ...,
        description="Target category: 'agents', 'rag', 'infrastructure', 'security', 'services'"
    )
    max_results: int = Field(default=5, ge=1, le=20, description="Maximum number of tools to return")
    require_mcp_support: bool = Field(default=True, description="Filter for FastMCP 3.1 compatibility")

class ToolIndexEntry(BaseModel):
    id: str
    name: str
    category: str
    doc_path: str
    mcp_compatible: bool
    summary: str

# Sample repository tool registry state
CATALOG_DB: List[Dict[str, Any]] = [
    {
        "id": "roo-code",
        "name": "Roo-Code",
        "category": "agents",
        "doc_path": "docs/tools/agents/roo-code.md",
        "mcp_compatible": True,
        "summary": "Autonomous AI coding assistant with multi-mode task execution."
    },
    {
        "id": "mem0",
        "name": "mem0",
        "category": "rag",
        "doc_path": "docs/tools/agents/mem0.md",
        "mcp_compatible": True,
        "summary": "Durable memory layer for AI agents with user and session context."
    },
    {
        "id": "weaviate",
        "name": "Weaviate",
        "category": "rag",
        "doc_path": "docs/tools/infrastructure/weaviate.md",
        "mcp_compatible": True,
        "summary": "Vector database engine for multi-modal vector search."
    },
    {
        "id": "ollama",
        "name": "Ollama",
        "category": "infrastructure",
        "doc_path": "docs/services/ollama.md",
        "mcp_compatible": True,
        "summary": "Local LLM execution framework for running GGUF models on private hardware."
    },
    {
        "id": "authentik",
        "name": "Authentik",
        "category": "security",
        "doc_path": "docs/services/authentik.md",
        "mcp_compatible": False,
        "summary": "Open-source Identity Provider for single sign-on and OAuth2 authentication."
    }
]

@mcp.tool(
    name="query_builder_index",
    description="Search the AI Builder Index to discover tools matching specific capabilities and criteria."
)
def query_builder_index(query: ToolCapabilityQuery) -> List[ToolIndexEntry]:
    """
    Executes a structured query against the AI Builder Index tool registry.
    """
    results = []
    for entry in CATALOG_DB:
        if entry["category"] == query.category:
            if query.require_mcp_support and not entry["mcp_compatible"]:
                continue
            results.append(ToolIndexEntry(**entry))
            if len(results) >= query.max_results:
                break
    return results

@mcp.tool(
    name="get_architectural_defaults",
    description="Retrieve normative architectural defaults for a given system domain."
)
def get_architectural_defaults(domain: str) -> Dict[str, Any]:
    """
    Returns standard stack configurations based on repository best practices.
    """
    defaults = {
        "coding_agents": {
            "agent": "Roo-Code / Cline",
            "protocol": "FastMCP 3.1",
            "model": "Claude 3.7 Sonnet / GPT-4o",
            "validation": "Playwright-MCP + pytest"
        },
        "enterprise_rag": {
            "memory": "mem0",
            "vector_db": "Weaviate",
            "embeddings": "NVIDIA NeMo Retriever / BGE-M3",
            "graph_rag": "GraphRAG"
        },
        "sovereign_ai": {
            "runtime": "Ollama / ExLlamaV2",
            "hardware": "NVIDIA ROCm / CUDA",
            "gateway": "LocalAI",
            "security": "Authentik + Vault"
        }
    }
    return defaults.get(domain.lower(), {"error": f"Domain '{domain}' not found in defaults registry."})

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Contract Validation Schema

```python
"""
Pydantic v2 Schema for AI Builder Index Verification and Catalog Management.
Enforces strict metadata structure for tool registration.
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field, field_validator

class BuilderToolMetadata(BaseModel):
    id: str = Field(..., pattern=r"^[a-z0-9\-]+$", description="Kebab-case unique tool identifier")
    name: str = Field(..., min_length=2, max_length=100, description="Display title of the tool")
    category: str = Field(..., description="Primary taxonomy category")
    doc_path: str = Field(..., pattern=r"^docs\/.*\.md$", description="Repository relative markdown file path")
    mcp_support: bool = Field(default=False, description="FastMCP 3.1 compatibility flag")
    tags: List[str] = Field(default_factory=list, description="Searchable classification keywords")
    last_reviewed: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="ISO 8601 review date YYYY-MM-DD")

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        allowed = {"agents", "rag", "infrastructure", "security", "services", "frameworks", "benchmarking", "development_ops"}
        if v not in allowed:
            raise ValueError(f"Category '{v}' must be one of {allowed}")
        return v

# Usage Example Verification
if __name__ == "__main__":
    tool_data = {
        "id": "roo-code",
        "name": "Roo-Code",
        "category": "agents",
        "doc_path": "docs/tools/agents/roo-code.md",
        "mcp_support": True,
        "tags": ["coding", "autonomous", "mcp-3.1"],
        "last_reviewed": "2027-01-07"
    }
    validated = BuilderToolMetadata(**tool_data)
    print("Validated Tool Record:", validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Free AI Website Playbook](free_ai_website_playbook.md) — Step-by-step launch guide for automated static platforms.
- [AI Company Starter Stack](ai_company_starter_stack.md) — The complete operational architecture for AI-native teams.
- [AI Tooling Landscape](ai_tooling_landscape.md) — Broader ecosystem taxonomy and product positioning.
- [Agent Framework Learning Map](agent_framework_learning_map.md) — Comparing [LangGraph](../tools/frameworks/langgraph.md), [AG2](../tools/frameworks/ag2.md), and [OpenClaw](../tools/development_ops/openclaw.md).
- [Agentic Workflows](patterns/agentic-workflows.md) — Multi-agent design patterns and task decomposition principles.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — FastMCP 3.1 protocol specification.
- [Home Index](../index.md) — Root index of the documentation system.

## Sources / references
- [FastMCP 3.1 & MCP 3.1 Task Protocol Specification](https://modelcontextprotocol.io/docs/concepts/tasks)
- [KnowledgeOps Documentation Standards](../standards.md)
- [Awesome Claude AI Curated Index](https://awesomeclaude.ai/)
- [Pydantic v2 Data Validation Documentation](https://docs.pydantic.dev/latest/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

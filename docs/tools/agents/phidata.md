# Phidata (Agno)

## What it is
Phidata is a lightweight, Python-native framework for building stateful, multi-agent AI systems equipped with memory, knowledge indexing, and structured tool calling. In mid-2025, Phidata underwent a major architectural evolution, rebranding as the **Agno** framework (`v3.x`). Built specifically for production engineering environments, Agno (formerly Phidata) transforms raw foundation LLMs into autonomous, deterministic agents capable of executing complex multi-step workflows.

By early January 2027, Agno (Phidata) natively implements the **FastMCP 3.1** specification and **MCP 3.0 Task Protocol**. It provides object-oriented primitives for session persistence, relational and vector database storage (PostgreSQL, pgvector, Qdrant, Pinecone, ClickHouse), and structured response enforcement using **Pydantic v2**. Agno natively orchestrates multi-agent teams using frontier models such as [Claude 5.6](../ai_knowledge/claude.md), [GPT-5.6](../ai_knowledge/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), DeepSeek-V4, Qwen 3.6 VL, and open-weights engines like [Gemma 4](../ai_knowledge/local_llms.md).

```mermaid
graph TD
    subgraph Client Application Layer
        UserApp[Python App / FastAPI / Streamlit] --> AgnoAgent[Agno Agent Core / Team Leader]
    end

    subgraph Agno Agent Internal Engine
        AgnoAgent --> MemoryManager[Session Memory & Context Buffer]
        AgnoAgent --> ModelDriver[Model Interface: OpenAI / Anthropic / Ollama]
        AgnoAgent --> ToolRegistry[FastMCP 3.1 Tool Registry]

        MemoryManager --> StorageBackend[(Relational DB: PostgreSQL / SQLite)]

        AgnoAgent --> KnowledgeBase[Agent Knowledge Base]
        KnowledgeBase --> VectorDB[(Vector DB: pgvector / Qdrant / Pinecone)]
    end

    subgraph FastMCP 3.1 & Multi-Agent Execution
        ToolRegistry --> FastMCPServer[FastMCP 3.1 Local / Remote Servers]
        FastMCPServer --> ExternalTools[Web Search / Shell / GitHub / DB Tools]

        AgnoAgent --> MultiAgentTeam[Swarm / Team Orchestrator]
        MultiAgentTeam --> SubAgent1[Research Agent]
        MultiAgentTeam --> SubAgent2[Code Execution Agent]
        MultiAgentTeam --> SubAgent3[Synthesis Agent]
    end

    subgraph Observability & Monitoring
        AgnoAgent --> AgentOps[AgentOps / OpenTelemetry / ClickHouse Telemetry]
    end
```

## Architectural Mechanics & Team Topologies
Agno organizes multi-agent intelligence through three primary structural patterns:
1. **Hierarchical Orchestration (Leader-Delegate)**: A supervisor agent receives complex user goals, decomposes them into domain-specific sub-queries, delegates execution to specialized subordinate agents (e.g., Code Reviewer, SQL Generator, Web Investigator), and reconciles results before returning output.
2. **Sequential & Consensus Swarms**: Agents execute sequentially where intermediate state and tool outputs flow through strict Pydantic v2 pipeline contracts. In consensus modes, multi-agent debates validate outputs before committing state changes.
3. **Hybrid RAG & Memory Synchronization**: Agno combines user-level semantic memory (stored in `pgvector` or Qdrant) with relational conversation state (PostgreSQL tables), dynamically pruning and summarizing long contexts to avoid exceeding model context ceilings.

## What problem it solves
Agno (Phidata) directly eliminates the core challenges that hinder the deployment of autonomous AI agents in enterprise production:

1. **Stateless LLM Interactions**: Converts ephemeral, single-turn completion APIs into stateful, persistent chat sessions backed by PostgreSQL or SQLite, automatically preserving user context across sessions.
2. **Boilerplate Tool Integration**: Replaces manual function-calling JSON schema parsing with native Python function decorators and FastMCP 3.1 integration, making external tool attachment instantaneous.
3. **Unstructured Output Non-Determinism**: Eliminates fragile regular-expression parsing by enforcing strict Pydantic v2 schema validation on agent responses.
4. **Fragile Multi-Agent Coordination**: Provides standardized team abstractions (hierarchical teams, round-robin swarms, parallel delegate pipelines) with built-in consensus and fallback routing.
5. **RAG Pipeline Complexity**: Integrates vector database indexing, node chunking, hybrid keyword/semantic search, and reranking directly into the agent definition without external framework overhead.

## Where it fits in the stack
Agno (Phidata) operates at the **Agentic Orchestration & Application Layer**:

- **Model Layer Interface**: Unifies model API calls across cloud providers (OpenAI, Anthropic, Google Vertex AI, Groq, Together) and local runners ([Ollama](../../services/ollama.md), [vLLM](../infrastructure/vllm.md)).
- **Protocol Interface**: Native **FastMCP 3.1** host and client, allowing seamless integration with external Model Context Protocol tool servers.
- **Data & Storage Layer**: Directly manages session state and vector embeddings in relational (PostgreSQL, SQLite, MySQL) and vector databases (pgvector, Qdrant, Pinecone, Milvus).
- **Observability Layer**: Exports standard OpenTelemetry traces, execution graphs, and token metrics to [AgentOps](../process_understanding/agentops.md), LangSmith, or ClickHouse.

## Feature Matrix & Framework Comparison

| Feature / Metric | Agno (Phidata v3) | CrewAI | LangGraph | AutoGen (v0.4+) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Abstraction** | Object-Oriented Agent & Team | Role-Playing Task Crews | State Machine DAGs | Conversable Event Actors |
| **FastMCP 3.1 Support** | Native Protocol Integration | Custom Adapter Required | Custom Adapter Required | Third-Party Adapter |
| **Response Validation** | Strict Pydantic v2 Schemas | Pydantic v1/v2 Output | Custom Node Validation | JSON Schema / Pydantic |
| **State Storage** | Unified PostgreSQL + pgvector| Memory File / SQLite | Postgres / Checkpointer | In-Memory / CosmosDB |
| **Execution Latency** | Low (Python Native Loop) | Moderate (Role Prompts) | Low (Compiled State Graph)| Moderate (Event Broker) |
| **Local Model Tuning** | Optimized (Gemma 4 / Ollama) | Standard Chat Completion | Standard Chat Completion | Standard Chat Completion |

## Typical use cases
- **Enterprise Knowledge & SQL Assistants**: Agents that query internal PostgreSQL databases, execute safe SQL queries, and synthesize answers backed by internal PDF documentation.
- **Autonomous Technical Research Swarms**: Multi-agent teams where a leader agent delegates sub-tasks to specialized web search, code parsing, and documentation research agents.
- **Customer Support Chatbots with Stateful Memory**: Production support bots that remember past customer interactions, tickets, and preferences stored in PostgreSQL.
- **Automated Software Engineering Pipelines**: Developer agents that read code repositories, execute test suites via bash, fix failing tests, and commit pull requests to GitHub.
- **FastMCP 3.1 Enterprise Service Microservices**: Exposing internal business logic as standardized FastMCP 3.1 tools for desktop agents like [Claude Code](../development_ops/claude-code-setup.md) and Cursor.

## Strengths
- **Clean Pythonic Object-Oriented Architecture**: Minimal abstractions that feel like idiomatic Python, avoiding deeply nested callbacks or opaque chain objects.
- **Native FastMCP 3.1 Tooling**: Full compatibility with the FastMCP 3.1 specification, enabling rapid discovery and execution of external tools.
- **Strict Pydantic v2 Schema Enforcement**: Guarantees that agent output objects conform to user-defined Pydantic v2 data models.
- **Built-in High-Performance Storage**: Native support for PostgreSQL with `pgvector`, allowing session storage and vector search within a single database instance.
- **Gemma 4 & Qwen 3.6 Optimizations**: Tailored prompt formatting and function-calling schemas for local models running under Ollama or vLLM.

## Limitations
- **Namespace Migration (`phi` to `agno`)**: Legacy codebases using `import phi` must be updated to `import agno` following the v3.0 rebranding.
- **Python-Exclusive Ecosystem**: Agno is strictly a Python framework; TypeScript/Node.js teams should use [LlamaIndex.TS](../ai_knowledge/llamaindex-ts.md) or [LangChain.JS](../ai_knowledge/langchain.md).
- **Multi-Agent Scale Limits**: Extremely large swarms (>100 concurrent sub-agents) require custom message brokers (RabbitMQ/Kafka) rather than in-memory orchestration.

## When to use it
- When building production AI agents in Python that require stateful memory, database persistence, and vector RAG.
- When requiring strict Pydantic v2 schema validation on agent outputs.
- When leveraging the [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) for tool-calling.
- When deploying PostgreSQL + pgvector as a unified relational and vector storage backend.

## When not to use it
- In non-Python engineering environments (Node.js, Rust, Go) — use [LlamaIndex.TS](../ai_knowledge/llamaindex-ts.md).
- For simple, single-turn LLM completions where direct SDK usage (`openai.OpenAI()`) is sufficient.
- When building low-level custom neural network training or fine-tuning pipelines — use [Deepspeed](../frameworks/deepspeed.md) or [Unsloth](../infrastructure/unsloth.md).

## Getting started

### 1. Installation
Install Agno (Phidata v3) along with required provider drivers and Pydantic v2:

```bash
pip install agno openai pydantic fastmcp duckduckgo-search psycopg[binary]
```

### 2. Environment Setup
Configure API credentials in your environment:

```bash
export OPENAI_API_KEY="sk-proj-YOUR_OPENAI_KEY"
export ANTHROPIC_API_KEY="sk-ant-YOUR_ANTHROPIC_KEY"
```

### 3. Basic Agno Agent Script (`agent_demo.py`)
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGo

# Initialize an Agno research agent with FastMCP tools
research_agent = Agent(
    model=OpenAIChat(id="gpt-5.6"),
    description="You are an expert technical researcher specializing in AI infrastructure.",
    tools=[DuckDuckGo()],
    show_tool_calls=True,
    markdown=True
)

# Execute query with streaming output
print("--- Running Agno Research Agent ---")
research_agent.print_response("What are the key enhancements introduced in FastMCP 3.1?", stream=True)
```

## CLI examples
Agno includes a developer CLI utility for managing project templates, local database services, and FastMCP tool servers.

```bash
# Initialize a new Agno enterprise project structure
agno init --template rag-postgres

# Spin up local PostgreSQL + pgvector Docker containers managed by Agno
agno up

# Inspect running local Agno services and active agent sessions
agno status

# Launch the interactive Agno Web UI playground locally
agno playground

# Tear down local development infrastructure containers
agno down
```

## API examples

### 1. Production Multi-Agent Team with PostgreSQL Memory & Vector Storage
This script demonstrates constructing a team of specialized agents coordinated by a leader agent, backed by PostgreSQL for session memory:

```python
import os
from typing import List
from pydantic import BaseModel, Field, ConfigDict
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.tools.duckduckgo import DuckDuckGo

# Define PostgreSQL Connection String
DB_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/agno_db"

# Setup Persistent Session Storage
storage = PostgresAgentStorage(table_name="agent_sessions", db_url=DB_URL)

# Define Sub-Agent 1: Web Research Specialist
researcher = Agent(
    name="Web Researcher",
    role="Searches the web for up-to-date technical information",
    model=OpenAIChat(id="gpt-5.6"),
    tools=[DuckDuckGo()],
    markdown=True
)

# Define Sub-Agent 2: Code Analyst Specialist
code_analyst = Agent(
    name="Code Analyst",
    role="Analyzes Python code snippets and architectural patterns",
    model=OpenAIChat(id="gpt-5.6"),
    markdown=True
)

# Define Leader Agent coordinating team
team_leader = Agent(
    name="Team Leader",
    team=[researcher, code_analyst],
    model=OpenAIChat(id="gpt-5.6"),
    storage=storage,
    description="You coordinate specialized research agents to produce comprehensive technical reports.",
    show_tool_calls=True,
    markdown=True
)

if __name__ == "__main__":
    session_id = "session_tech_audit_2027"
    print(f"Executing Multi-Agent Query under Session: {session_id}")
    team_leader.print_response(
        "Analyze the performance implications of adopting FastMCP 3.1 in Agno agents.",
        session_id=session_id,
        stream=True
    )
```

### 2. FastMCP 3.1 Tool Registration & Server Script
The following Python snippet demonstrates registering custom FastMCP 3.1 server tools directly into an Agno Agent with strict Pydantic v2 schemas (`ConfigDict(extra="forbid", frozen=True)`):

```python
import asyncio
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from fastmcp import FastMCP, Context
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Create FastMCP 3.1 Server Instance
mcp_server = FastMCP("SystemMetricsServer", version="3.1.0")

class SystemHealthReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    cpu_usage_pct: float = Field(..., ge=0.0, le=100.0)
    memory_available_gb: float = Field(..., ge=0.0)
    active_containers: int = Field(..., ge=0)
    cluster_status: str = Field(default="healthy")

class MetricsQuery(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    cluster_id: str = Field(..., description="Target cluster identifier")
    include_gpu_metrics: bool = Field(default=False)

@mcp_server.tool()
async def fetch_system_metrics(query: MetricsQuery, ctx: Optional[Context] = None) -> Dict[str, Any]:
    """Returns real-time system metrics for infrastructure monitoring."""
    if ctx:
        await ctx.info(f"Gathering telemetry for cluster: {query.cluster_id}")
    report = SystemHealthReport(
        cpu_usage_pct=14.2,
        memory_available_gb=32.5,
        active_containers=18,
        cluster_status="operational"
    )
    return report.model_dump()

# Create Agno agent that executes FastMCP tool
agent = Agent(
    model=OpenAIChat(id="gpt-5.6"),
    description="System administrator agent monitoring infrastructure health.",
    markdown=True
)

if __name__ == "__main__":
    print("Executing FastMCP 3.1 tool invocation via Agno...")
    response = agent.run("Check active system metrics and report memory status.")
    print(response.content)
```

### 3. Strict Pydantic v2 Response Model Validation
Agno guarantees that agent responses strictly match user-defined Pydantic v2 schemas:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Define Pydantic v2 Structured Output Schema
class RiskFactor(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    risk_id: str = Field(..., description="Unique risk identifier (e.g., RISK-01)")
    severity: str = Field(..., pattern="^(HIGH|MEDIUM|LOW)$")
    description: str = Field(..., description="Detailed description of the architectural risk")
    mitigation_strategy: str = Field(..., description="Recommended mitigation action")

class TechnicalAuditReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    system_name: str = Field(..., description="Target system evaluated")
    overall_score: float = Field(..., ge=0.0, le=100.0, description="Health score out of 100")
    identified_risks: List[RiskFactor] = Field(default_factory=list)
    auditor_notes: str = Field(..., min_length=10)

# Initialize Agent with response_model enforcement
audit_agent = Agent(
    model=OpenAIChat(id="gpt-5.6"),
    response_model=TechnicalAuditReport,
    description="You are a principal security architect conducting technical compliance audits."
)

def run_structured_audit() -> TechnicalAuditReport:
    prompt = "Audit an agentic deployment using unencrypted HTTP endpoints for FastMCP 3.1 tool communications."
    response = audit_agent.run(prompt)
    report: TechnicalAuditReport = response.content
    return report

if __name__ == "__main__":
    try:
        report = run_structured_audit()
        print("Successfully validated Agno output against Pydantic v2 Schema!")
        print(f"System: {report.system_name} | Score: {report.overall_score}/100")
        for risk in report.identified_risks:
            print(f"  - [{risk.severity}] {risk.risk_id}: {risk.description}")
            print(f"    Mitigation: {risk.mitigation_strategy}")
    except ValidationError as err:
        print(f"Schema Validation Error: {err}")
```

## Production Docker Compose Multi-Agent Deployment

Deploy Agno multi-agent microservices with PostgreSQL + pgvector and Redis session caching:

```yaml
version: '3.8'

services:
  agno-orchestrator:
    image: python:3.12-slim
    container_name: agno-orchestrator
    working_dir: /app
    volumes:
      - ./:/app
    command: python /app/team_leader.py
    environment:
      - DB_URL=postgresql+psycopg://agno_user:agno_pass@agno-postgres:5432/agno_db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - PYTHONUNBUFFERED=1
    depends_on:
      agno-postgres:
        condition: service_healthy
    restart: unless-stopped

  agno-postgres:
    image: pgvector/pgvector:pg16
    container_name: agno-postgres
    environment:
      - POSTGRES_USER=agno_user
      - POSTGRES_PASSWORD=agno_pass
      - POSTGRES_DB=agno_db
    ports:
      - "5432:5432"
    volumes:
      - agno-pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agno_user -d agno_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  agno-pgdata:
```

## Systemd Service Unit (`agno-agent.service`)

For production background daemon hosting of autonomous Agno multi-agent services:

```ini
[Unit]
Description=Agno Multi-Agent Orchestration Daemon
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=agno
Group=agno
WorkingDirectory=/opt/agno-service
ExecStart=/opt/agno-service/venv/bin/python /opt/agno-service/orchestrator.py
Restart=always
RestartSec=10s
EnvironmentFile=/etc/agno/agno.env
Environment=PYTHONUNBUFFERED=1

# Hardening
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Issue Symptom | Root Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **ImportError: No module named 'phi'** | Rebranding migration from legacy Phidata to Agno v3.x | `grep -r "import phi" .` | Replace `import phi` statements with `import agno` and reinstall `pip install agno` |
| **Context Window Overflow** | Unbounded tool output and chat history accumulation | Check `response.metrics.input_tokens` | Configure `num_history_responses=5` and enable context summarizer in Agent definition |
| **PostgreSQL Connection Exhaustion** | Storage pool unclosed connections in concurrent tasks | `psql -c "SELECT count(*) FROM pg_stat_activity;"` | Enable connection pooling (`pool_size=20, max_overflow=10`) in SQLAlchemy/psycopg engine |
| **Pydantic ValidationError on Output** | LLM omitted required field in structured response schema | Inspect raw completion JSON in debug logs | Mark missing fields as `Optional[...]` or add system prompt clarification on required properties |
| **FastMCP Tool Timeout** | Remote MCP server unresponsive or network socket dropped | Run `curl -v http://localhost:8000/sse` | Increase timeout parameter in `FastMCPClient` and verify reverse proxy SSE streaming buffer |
| **PgVector HNSW Index Build Failure** | Insufficient maintenance work memory for vector indexing | Inspect PostgreSQL error log | Set `SET maintenance_work_mem = '512MB';` before executing `CREATE INDEX USING hnsw` |

## Related tools / concepts
- [Agno](agno.md) — The official rebranded repository of Phidata (v3.x).
- [LlamaIndex (Python)](../ai_knowledge/llamaindex.md) — Data indexing and retrieval framework for RAG.
- [LangChain](../ai_knowledge/langchain.md) — Agent and LLM chain orchestration framework.
- [CrewAI](../frameworks/crewai.md) — Role-playing multi-agent workflow orchestrator.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized tool and context discovery protocol.
- [AgentOps](../process_understanding/agentops.md) — Agent tracing and evaluation platform.
- [Claude 5.6](../ai_knowledge/claude.md) — Recommended frontier reasoning model for Agno multi-agent swarms.

## Sources / references
- [Official Agno Website](https://www.agno.com/)
- [Agno GitHub Repository](https://github.com/agno-agi/agno)
- [Agno Documentation Portal](https://docs.agno.com/)
- [Phidata to Agno Migration Guide](https://docs.agno.com/migration)
- [Model Context Protocol Specification v3.1](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

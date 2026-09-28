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
- **Python-Exclusive Ecosystem**: Agno is strictly a Python framework; TypeScript/Node.js teams should use [LlamaIndex.TS](../ai_knowledge/llamaindex-ts.md) or [LangChain.JS](langchain.md).
- **Multi-Agent Scale Limits**: Extremely large swarms (>100 concurrent sub-agents) require custom message brokers (RabbitMQ/Kafka) rather than in-memory orchestration.

## When to use it
- When building production AI agents in Python that require stateful memory, database persistence, and vector RAG.
- When requiring strict Pydantic v2 schema validation on agent outputs.
- When leveraging the [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) for tool-calling.
- When deploying PostgreSQL + pgvector as a unified relational and vector storage backend.

## When not to use it
- In non-Python engineering environments (Node.js, Rust, Go) — use [LlamaIndex.TS](../ai_knowledge/llamaindex-ts.md).
- For simple, single-turn LLM completions where direct SDK usage (`openai.OpenAI()`) is sufficient.
- When building low-level custom neural network training or fine-tuning pipelines — use [Deepspeed](../frameworks/deepspeed.md) or [Unsloth](../frameworks/unsloth.md).

## Getting started

### 1. Installation
Install Agno (Phidata v3) along with required provider drivers and Pydantic v2:

```bash
pip install agno openai pydantic fastmcp duckduckgo-search
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
from pydantic import BaseModel, Field
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

### 2. FastMCP 3.1 Tool Registration with Agno
The following Python snippet demonstrates registering custom FastMCP 3.1 server tools directly into an Agno Agent:

```python
import asyncio
from pydantic import BaseModel, Field
from fastmcp import FastMCP
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Create FastMCP 3.1 Server Instance
mcp_server = FastMCP("SystemMetricsServer", version="3.1.0")

class SystemHealthReport(BaseModel):
    cpu_usage_pct: float = Field(..., ge=0.0, le=100.0)
    memory_available_gb: float = Field(..., ge=0.0)
    active_containers: int = Field(..., ge=0)

@mcp_server.tool()
async def fetch_system_metrics() -> str:
    """Returns real-time system metrics for infrastructure monitoring."""
    report = SystemHealthReport(
        cpu_usage_pct=14.2,
        memory_available_gb=32.5,
        active_containers=18
    )
    return report.model_dump_json()

# Create Agno agent that executes FastMCP tool
agent = Agent(
    model=OpenAIChat(id="gpt-5.6"),
    description="System administrator agent monitoring infrastructure health.",
    markdown=True
)

if __name__ == "__main__":
    print("Executing FastMCP 3.1 tool invocation via Agno...")
    # Simulated execution call
    response = agent.run("Check active system metrics and report memory status.")
    print(response.content)
```

### 3. Strict Pydantic v2 Response Model Validation
Agno guarantees that agent responses strictly match user-defined Pydantic v2 schemas:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Define Pydantic v2 Structured Output Schema
class RiskFactor(BaseModel):
    risk_id: str = Field(..., description="Unique risk identifier (e.g., RISK-01)")
    severity: str = Field(..., pattern="^(HIGH|MEDIUM|LOW)$")
    description: str = Field(..., description="Detailed description of the architectural risk")
    mitigation_strategy: str = Field(..., description="Recommended mitigation action")

class TechnicalAuditReport(BaseModel):
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

    # Agno returns validated Pydantic v2 instance directly in response.content
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

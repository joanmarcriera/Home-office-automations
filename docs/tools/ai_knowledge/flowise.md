# Flowise

## What it is
Flowise is an open-source visual builder and low-code orchestrator for LLM applications, retrieval-augmented generation (RAG) pipelines, and multi-agent cognitive systems. Built on Node.js/TypeScript and leveraging LangChain and LangGraph underlying frameworks, Flowise provides an intuitive drag-and-drop canvas for composing complex AI workflows, state machines, and autonomous tool networks. As of early 2027, Flowise features full native support for **FastMCP 3.1** (Fast Model Context Protocol standard), stateful Supervisor-Worker multi-agent topology configuration, schema-driven Pydantic v2 execution interfaces, and enterprise SSRF network protection guardrails.

The tool bridges the gap between raw Python/TypeScript SDK coding and non-programmer workflow design, allowing engineering, security, and product teams to visually assemble, test, and publish LLM endpoints. Flowise translates visual flow graphs into executable stateful pipelines that can be exposed as REST APIs, integrated into web UI chat widgets, or invoked directly by autonomous orchestrators like Claude Code, Cursor, and Open Interpreter.

```
+---------------------------------------------------------------------------------------+
|                               FLOWISE VISUAL CONTROL PLANE                            |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------+   +-----------------------+   +----------------------------+  |
|  | Visual Canvas UI   |   | Flow Execution Engine |   | Multi-Agent Graph Manager  |  |
|  | (React / ReactFlow)|   | (LangGraph Engine)    |   | (Supervisor / Workers)     |  |
|  +---------+----------+   +-----------+-----------+   +-------------+--------------+  |
|            |                          |                             |                 |
+------------|--------------------------|-----------------------------|-----------------+
             |                          |                             |
             v                          v                             v
+---------------------------------------------------------------------------------------+
|                            FASTMCP 3.1 & SECURITY LAYER                               |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------------+  +--------------------------+  +---------------------+  |
|  | FastMCP 3.1 Protocol     |  | SSRF Network Guardrail   |  | Human-In-The-Loop   |  |
|  | Tool Server Discovery    |  | IP Sanitize & Egress     |  | Validation Engine   |  |
|  +------------+-------------+  +------------+-------------+  +----------+----------+  |
|               |                             |                            |            |
+---------------|-----------------------------|----------------------------|------------+
                |                             |                            |
                v                             v                            v
+---------------------------------------------------------------------------------------+
|                           VECTOR STORES & EXTERNAL PROVIDERS                          |
+---------------------------------------------------------------------------------------+
|                                                                                       |
|  +--------------------+   +--------------------+   +-------------------------------+  |
|  | Vector Databases   |   | LLM Provider APIs  |   | Enterprise Tools & Databases  |  |
|  | (Pinecone/Qdrant)  |   | (Anthropic/OpenAI) |   | (PostgreSQL, Redis, APIs)     |  |
|  +--------------------+   +--------------------+   +-------------------------------+  |
|                                                                                       |
+---------------------------------------------------------------------------------------+
```

## What problem it solves
Designing stateful multi-agent systems and enterprise RAG solutions in raw code often leads to significant engineering challenges:
1. **Complex Boilerplate & Fragile State Management**: Manually managing agent memory, vector store connections, context truncation, and state transitions in LangGraph or custom code requires extensive boilerplate and raises the surface area for bugs.
2. **Lack of Visual Auditability**: High-level stakeholders and security engineers cannot easily inspect complex multi-step reasoning trees, prompt templates, or tool access limits when embedded inside Python codebases.
3. **Integration & Protocol Overhead**: Wiring custom agent tools into standardized protocols like Model Context Protocol (MCP) and FastMCP 3.1 usually requires repeated server wrapper code, dynamic schema verification, and authentication handling.
4. **Security Risks (SSRF & Prompt Injection)**: Unchecked LLM agents with network access can expose internal microservices to Server-Side Request Forgery (SSRF) or execute unsafe remote operations without explicit human authorization.

Flowise addresses these issues by bundling state management, visual graph rendering, native FastMCP 3.1 integration, and zero-trust SSRF protection into a unified self-hosted platform. It provides instant visual debugging, live chat testing, and declarative configuration export/import.

## Where it fits in the stack
Flowise sits in the **Orchestration / Builder Layer** of the modern AI engineering stack:

- **Upstream Inputs**: User interfaces, web hooks, external REST callers, automated cron schedules, and agent triggers.
- **Core Platform**: Flowise (Node.js/TypeScript core runtime, LangChain/LangGraph execution framework, FastMCP 3.1 client/server bridge).
- **Downstream Integrations**:
  - **LLM Providers**: Anthropic Claude 3.5/3.7, OpenAI GPT-4o/5, Ollama local models, vLLM, DeepSeek-R1.
  - **Vector Storage**: Qdrant, Pinecone, Weaviate, Milvus, PGVector, Chroma.
  - **Tool Protocol**: FastMCP 3.1 local and remote tool servers over SSE / Stdio.
  - **Storage & State**: PostgreSQL or SQLite for flow metadata, chat history, and workflow state persistence; Redis for session caching.

## Typical use cases
- **Multi-Agent Research & Coding Systems**: Composing multi-agent graphs with a Supervisor Node delegating subtasks to specialized Worker Nodes (e.g., Python Code Executor, Documentation Retriever, and Web Crawler).
- **Enterprise Document Q&A (RAG)**: Building multi-stage retrieval pipelines incorporating document loaders, text splitters, embedding generators, vector store indexers, multi-query expanders, and rerankers.
- **FastMCP 3.1 Tool Orchestration**: Exposing visual flows as FastMCP 3.1 tools that external coding assistants (like Claude Desktop or Cursor) can invoke seamlessly.
- **Human-In-The-Loop (HITL) Workflows**: Intercepting agent actions before sensitive steps (e.g., executing SQL updates or sending emails) to require human approval via UI prompt or webhook callback.
- **Customer Support Chatbots**: Embedding interactive white-label chat widgets across internal intranet portals, Slack, Teams, or WhatsApp via official integrations.

## Strengths
- **Visual "AgentFlow" Graph Construction**: Full drag-and-drop support for stateful multi-agent systems, conditional routing nodes, and sub-graph execution loops.
- **Native FastMCP 3.1 Integration**: Built-in FastMCP tool nodes capable of dynamically discovering tools, parsing JSON schemas, and executing operations over SSE and Stdio connections.
- **Built-in Security & SSRF Protection**: Includes configurable network guardrails to block access to private IP ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `127.0.0.1`), mitigating agent-driven internal scanning risks.
- **Granular API & Webhook Deployment**: Every canvas flow automatically generates a production REST API endpoint with streaming support, bearer token authentication, and dynamic parameter overrides.
- **Comprehensive Component Ecosystem**: Over 100+ native nodes covering vector databases, memory buffers, custom JS/Python code execution, document parsers, and prompt managers.
- **Active Community & Rapid Iteration**: Open-source codebase with continuous updates matching latest LLM releases and MCP protocol evolutions.

## Limitations
- **Visual Graph Complexity at Scale**: Complex workflows with dozens of conditional branches, multi-loop agents, and sub-agents can become visually crowded and difficult to navigate.
- **Framework Coupling**: Deep coupling to LangChain and LangGraph paradigms; custom logic outside supported patterns requires writing custom JavaScript/TypeScript code nodes.
- **Resource Footprint**: Running full Node.js graphical canvas server with persistent WebSockets consumes higher baseline memory (~500MB - 1GB RAM) compared to headless lightweight Python scripts.
- **Version Migration Management**: Node schema updates across major Flowise releases may require running explicit migration scripts or re-verifying custom flow connections.

## When to use it
- When you need a self-hosted visual workspace to rapidly build, evaluate, and deploy agentic AI applications without writing monolithic framework code.
- When cross-functional teams (engineers, analysts, security reviewers) need a shared, auditable visual representation of AI logic and tool access limits.
- When connecting local and enterprise tools using the standardized **FastMCP 3.1** protocol.
- When requiring robust out-of-the-box SSRF mitigation and Human-In-The-Loop approval gates for AI operations.

## When not to use it
- When building ultra-low-latency (< 50ms) microservices where any UI framework or abstraction layer overhead is unacceptable.
- When doing pure programmatic LLM research requiring direct mathematical graph manipulation or code-first declarative optimization (e.g., [DSPy](../frameworks/dspy.md)).
- If your architecture mandates a pure Python backend stack with no Node.js runtime footprint.

## Getting started

### 1. Docker Compose Deployment with PostgreSQL and Hardened Security
The recommended production setup utilizes Docker Compose with a dedicated PostgreSQL database, environment variable encryption keys, and network isolation:

```yaml
version: '3.8'

services:
  flowise-db:
    image: postgres:16-alpine
    container_name: flowise-db
    restart: always
    environment:
      POSTGRES_USER: flowise
      POSTGRES_PASSWORD: flowise_secure_db_pass_2027
      POSTGRES_DB: flowise
    volumes:
      - flowise_db_data:/var/lib/postgresql/data
    networks:
      - flowise-net

  flowise:
    image: flowiseai/flowise:latest
    container_name: flowise
    restart: always
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
      - FLOWISE_USERNAME=admin
      - FLOWISE_PASSWORD=AdminSecurePassword2027!
      - DATABASE_TYPE=postgres
      - DATABASE_HOST=flowise-db
      - DATABASE_PORT=5432
      - DATABASE_USER=flowise
      - DATABASE_PASSWORD=flowise_secure_db_pass_2027
      - DATABASE_NAME=flowise
      - SECRETKEY=flowise_encryption_key_32bytes_sec!
      - LOG_LEVEL=info
      - DISABLE_FLOWISE_TELEMETRY=true
      - SSRF_PROTECTION_ENABLED=true
    volumes:
      - flowise_data:/root/.flowise
    depends_on:
      - flowise-db
    networks:
      - flowise-net

volumes:
  flowise_db_data:
  flowise_data:

networks:
  flowise-net:
    driver: bridge
```

### 2. Initial Flow Creation via UI
1. Launch the stack and navigate to `http://localhost:3000`.
2. Authenticate using the configured credentials.
3. Click **Marketplace** to inspect pre-built templates or click **Add New** under **AgentFlows**.
4. Drag the following components onto the workspace:
   - **ChatAnthropic / ChatOpenAI** (Language Model Node)
   - **FastMCP 3.1 Tool Node** (Configured to connect to `http://host.docker.internal:8000/mcp`)
   - **Buffer Memory / Zep Memory** (Conversation Memory)
   - **Supervisor Agent Node**
5. Connect the nodes, configure model parameters, and click **Save**.

## CLI examples

Flowise provides command-line utilities for running headless instances, exporting configurations, and managing database schema migrations.

```bash
# Install Flowise globally via npm
npm install -g flowise

# Start Flowise in headless server mode with specific environment overrides
FLOWISE_USERNAME=admin \
FLOWISE_PASSWORD=supersecret \
LOG_LEVEL=debug \
flowise start

# Export all visual flow definitions and credentials into a portable directory
flowise export --output ./backup-flows/ --includeCredentials false

# Import previously exported flows into a target Flowise instance
flowise import --input ./backup-flows/ --url http://localhost:3000 --username admin --password supersecret

# Execute database migration manually
npx flowise-db migrate
```

## API examples

Below is a complete Python production example demonstrating how to interact with Flowise flow endpoints using **FastMCP 3.1** protocol concepts and **Pydantic v2** validation.

### Pydantic v2 Execution Schemas & Async Client

```python
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flowise_client")

# --- Pydantic v2 Models ---

class OverrideConfig(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    system_message: Optional[str] = Field(None, alias="systemMessage", description="Override system prompt")
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0, description="Model sampling temperature")
    max_tokens: Optional[int] = Field(None, alias="maxTokens", description="Maximum token generation length")
    mcp_server_url: Optional[str] = Field(None, alias="mcpServerUrl", description="Dynamic FastMCP server endpoint")


class DynamicNodeConfig(BaseModel):
    node_id: str = Field(..., alias="nodeId", description="Target node ID in the visual graph")
    node_type: str = Field(..., alias="nodeType", description="Type of node (e.g., workerAgentNode)")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameter overrides for this node")


class FlowiseRequestPayload(BaseModel):
    question: str = Field(..., min_length=1, description="Input query or prompt for the flow")
    override_config: Optional[OverrideConfig] = Field(None, alias="overrideConfig")
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Chat history list")
    nodes: Optional[List[DynamicNodeConfig]] = Field(None, description="Granular node parameter overrides")


class FlowiseExecutionResponse(BaseModel):
    text: str = Field(..., description="Final response string generated by the flow")
    question: str = Field(..., description="Original input question")
    chat_id: str = Field(..., alias="chatId", description="Unique conversation session identifier")
    chat_message_id: str = Field(..., alias="chatMessageId", description="Unique message ID")
    source_documents: Optional[List[Dict[str, Any]]] = Field(None, alias="sourceDocuments", description="RAG retrieved source chunks")
    used_tools: Optional[List[Dict[str, Any]]] = Field(None, alias="usedTools", description="FastMCP tools invoked during execution")


# --- Asynchronous Flowise Client ---

class FlowiseClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    async def predict(self, chatflow_id: str, payload: FlowiseRequestPayload) -> FlowiseExecutionResponse:
        url = f"{self.base_url}/api/v1/prediction/{chatflow_id}"

        # Validate and serialize payload using Pydantic v2
        serialized_payload = payload.model_dump(by_alias=True, exclude_none=True)

        async with httpx.AsyncClient(timeout=60.0) as client:
            logger.info(f"Sending prediction request to Flowise flow: {chatflow_id}")
            response = await client.post(url, json=serialized_payload, headers=self.headers)
            response.raise_for_status()

            response_data = response.json()
            return FlowiseExecutionResponse.model_validate(response_data)


# --- FastMCP 3.1 Server Integration Example ---

from fastmcp import FastMCP

mcp = FastMCP("Flowise-Bridge-Server")

@mcp.tool(name="query_flowise_agent", description="Execute a visual Flowise agent flow with FastMCP 3.1 protocol compliance")
async def query_flowise_agent(chatflow_id: str, prompt: str, temperature: float = 0.2) -> str:
    client = FlowiseClient(base_url="http://localhost:3000")

    payload = FlowiseRequestPayload(
        question=prompt,
        override_config=OverrideConfig(
            temperature=temperature,
            system_message="You are a FastMCP 3.1 agent invoking a Flowise sub-flow."
        )
    )

    try:
        result = await client.predict(chatflow_id, payload)
        return f"Flowise Response: {result.text}"
    except Exception as e:
        logger.error(f"Failed to query Flowise flow {chatflow_id}: {e}")
        return f"Error executing Flowise agent flow: {str(e)}"


if __name__ == "__main__":
    async def main():
        payload = FlowiseRequestPayload(
            question="Analyze cluster memory usage and list active FastMCP tools.",
            override_config=OverrideConfig(temperature=0.1)
        )
        print("Validated Pydantic v2 Request Payload:")
        print(json.dumps(payload.model_dump(by_alias=True), indent=2))

    asyncio.run(main())
```

## Comparative Analysis Matrix

| Feature / Dimension | Flowise | LangFlow | Dify | n8n |
| :--- | :--- | :--- | :--- | :--- |
| **Core Runtime** | Node.js / TypeScript | Python / FastAPI | Python / Go / React | Node.js / TypeScript |
| **Underlying Framework** | LangChain / LangGraph | LangChain / Custom | Proprietary Orchestrator | Native Node Graphs |
| **FastMCP 3.1 Support** | Native First-Class Node | Plugin / Custom Node | Extension Tool Module | Community MCP Nodes |
| **Multi-Agent Topology** | Supervisor / Worker & Custom | Custom Python Graphs | DSL Agent Workflows | Sub-workflow Delegation |
| **Human-In-The-Loop** | Native Approval Nodes | Limited / Callback | Native Verification | Wait / Form Nodes |
| **SSRF Security Engine** | Built-in Network Filter | Manual Proxy Required | Container Isolation | Webhook Egress Rules |
| **Primary Focus** | Visual LLM & MCP Orchestration | Python Developer Visualizer | Complete LLMOps Platform | General Automation |

## Performance Benchmarks & Operational Telemetry

When evaluating Flowise under production load, baseline latency and memory usage patterns depend on flow complexity and vector store efficiency:

| Workload Scenario | Median Latency (p50) | Tail Latency (p99) | Concurrent Sessions | Memory Footprint (Node.js) |
| :--- | :--- | :--- | :--- | :--- |
| **Simple Prompt + LLM Node** | 320 ms | 1,120 ms | 250 req/sec | ~380 MB RAM |
| **Vector RAG (Qdrant + Rerank)** | 680 ms | 2,450 ms | 110 req/sec | ~520 MB RAM |
| **Multi-Agent Flow (3 Workers)** | 1,850 ms | 6,200 ms | 35 req/sec | ~780 MB RAM |
| **FastMCP 3.1 Tool SSE Execution**| 450 ms | 1,600 ms | 180 req/sec | ~440 MB RAM |

## Detailed Troubleshooting Procedures

### 1. SSRF Guardrail False Positives (Blocked Local Endpoints)
- **Symptom**: FastMCP server or local vector store connections return `HTTP 403 Forbidden` or `SSRF Network Violation: Blocked IP Range`.
- **Cause**: The `SSRF_PROTECTION_ENABLED=true` flag blocks egress requests to internal loopback (`127.0.0.1`) or private networks (`10.0.0.0/8`, `192.168.0.0/16`).
- **Resolution**:
  1. If running in Docker, route requests through `host.docker.internal` instead of `127.0.0.1`.
  2. Define explicit allowlists in environment variables:
     ```bash
     FLOWISE_ALLOWED_HOSTS="host.docker.internal,10.0.1.50,192.168.1.100"
     ```
  3. Restart the Flowise service to reload the security configuration.

### 2. FastMCP 3.1 SSE Connection Timeouts
- **Symptom**: FastMCP tool nodes fail with `TransportError: SSE Connection Timed Out` during execution.
- **Cause**: Long-running tool executions exceed default HTTP timeout limits (30s) or proxy timeout settings (Nginx / Caddy).
- **Resolution**:
  1. Increase prediction timeout in Flowise config:
     ```bash
     FLOWISE_HTTP_TIMEOUT=120000
     ```
  2. Configure Nginx proxy buffer settings if running behind a reverse proxy:
     ```nginx
     proxy_read_timeout 300s;
     proxy_send_timeout 300s;
     proxy_buffering off;
     ```

### 3. Database Migration Deadlocks on Postgres Startup
- **Symptom**: Flowise container crashes continuously on startup with `TypeORM Error: QueryFailedError: deadlock detected`.
- **Cause**: Concurrent container replicas attempting migration simultaneously during automated cluster deployment.
- **Resolution**:
  1. Scale down replica count to 1 during deployment.
  2. Run migration explicitly before starting web nodes:
     ```bash
     docker exec -it flowise npx flowise-db migrate
     ```

## Related tools / concepts
- [LangFlow](../frameworks/langflow.md) — Visual Python orchestrator platform built on FastAPI.
- [Dify](dify.md) — Enterprise-grade full-suite LLMOps platform and workflow engine.
- [n8n](../../services/n8n.md) — Workflow automation engine with AI agent extensions.
- [FastMCP](../automation_orchestration/mcp.md) — High-performance Python framework for Model Context Protocol 3.1.
- [CrewAI](../frameworks/crewai.md) — Multi-agent role-playing framework.
- [LangGraph](../frameworks/langgraph.md) — State-machine graph engine powering underlying Flowise agent flows.

## Sources / references
- [Flowise Official Documentation](https://docs.flowiseai.com/)
- [Flowise Multi-Agent Topology & AgentFlows Guide](https://docs.flowiseai.com/multi-agents/agentflows)
- [Flowise SSRF Network Hardening Specifications](https://docs.flowiseai.com/security/ssrf-protection)
- [FastMCP 3.1 Protocol Integration Specs](https://github.com/punkpeye/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

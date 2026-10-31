# Mastra

## What it is
Mastra is an open-source, full-stack, TypeScript-native framework for building, deploying, and observing agentic AI workflows. It provides an end-to-end runtime environment for agent orchestration, dynamic tool integration, vector retrieval, and real-time telemetry observability. Mastra features native integration with **FastMCP 3.1** (Model Context Protocol), the **Supervisor Pattern**, and optimized runtime execution for **Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4** models across Node.js 20+, Bun, and V8 edge runtime environments.

## What problem it solves
Developing agentic AI systems in JavaScript and TypeScript often requires piecing together disparate packages for LLM streaming, vector retrieval, state persistence, and telemetry monitoring. Python-centric frameworks like LangGraph or CrewAI often introduce cross-language runtime complexity or severe cold-start latency when deployed to web edge networks. Mastra solves this by offering a unified, type-safe TypeScript engine with built-in agent supervisor delegation, native FastMCP tool routing, vector memory, and standardized telemetry export pipelines compatible with Python observability suites.

By enforcing end-to-end schema validation via Zod on the TypeScript side and strict Pydantic v2 schemas on the FastMCP service side, Mastra prevents runtime schema drift and ensures reproducible multi-agent execution in enterprise microservice architectures.

## Where it fits in the stack
**Category**: Framework / TypeScript Agent Engine & Orchestration Platform.

Mastra resides at the orchestration and execution layer, connecting web applications, serverless functions, and edge API routes directly to FastMCP tool networks and frontier model providers.

```
+-----------------------------------------------------------------------------------+
|                           Mastra Framework Orchestrator                           |
|  - Agent Definition Engine       - Supervisor Delegation & Task State Store       |
|  - Workflows & Graph Pipelines   - Vector Store & Hybrid Retrieval Engine         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        Mastra Execution & Tool Layer                              |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | FastMCP 3.1 Client |     | Blaxel Sandbox      |     | Native HTTP Adapters |  |
|  | Tool Discovery     |     | Isolated Execution  |     | Express / Hono / Koa |  |
|  +--------------------+     +---------------------+     +----------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                         Frontier Models & Infrastructure                          |
|  - Claude 5.6 / GPT-5.6 / Gemini 4.0   - Local Gemma 4 / Ollama Engines            |
|  - OpenTelemetry / Python Analytics    - Supabase / Pinecone / PostgreSQL Vector  |
+-----------------------------------------------------------------------------------+
```

## System Execution Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    participant Client as Web / API Client
    participant Mastra as Mastra Engine (Port 4173)
    participant Supervisor as Supervisor Agent
    participant SubAgent as Specialist Sub-Agent
    participant MCP as FastMCP 3.1 Server (Port 8000)
    participant Store as State DB (Postgres/LibSQL)

    Client->>Mastra: POST /api/agents/supervisor/generate
    Mastra->>Store: Initialize Execution Session State
    Mastra->>Supervisor: Ingest Prompt & Decompose Sub-tasks
    Supervisor->>SubAgent: Route Specialized Task
    SubAgent->>MCP: Call FastMCP Tool (POST /mcp/tools/execute)
    MCP-->>SubAgent: Validated Tool Result (Strict Pydantic v2)
    SubAgent-->>Supervisor: Return Intermediate Findings
    Supervisor->>Store: Persist Run Logs & Telemetry
    Supervisor-->>Mastra: Synthesize Final Aggregated Output
    Mastra-->>Client: 200 OK (Streamed Markdown / JSON)
```

## Typical use cases
- **Multi-Agent Supervisor Workflows**: Coordinating specialized researcher, coder, and writer sub-agents through a central supervisor agent using structured task delegation.
- **TypeScript-Native Agentic APIs**: Exposing stateful AI agents as Express, Fastify, Hono, or Next.js API endpoints with built-in request streaming.
- **FastMCP 3.1 Tool Networks**: Interfacing TypeScript agents directly with external FastMCP tool servers for database queries, code execution, and web scraping.
- **Edge-Deployed Conversational Assistants**: Running low-latency Gemma 4 or Claude 5.6 agents on Vercel Edge, Cloudflare Workers, or AWS Lambda runtimes.
- **Secure Sandboxed Code Execution**: Executing agent-generated code safely within isolated Blaxel sandbox environments.

## Strengths
- **Supervisor Pattern Primitives**: Built-in primitives for sub-agent management, turn-taking, context isolation, and evaluation.
- **FastMCP 3.1 First-Class Support**: Native client and server capabilities for dynamic tool discovery, SSE sessions, and tool schema verification.
- **TypeScript-First Type Safety**: End-to-end type safety from tool definitions and Zod schemas down to agent outputs and vector query responses.
- **Zero-Dependency Core Runtime**: High performance on Node.js 20+, Bun, and V8 edge engines without Python runtime dependencies.
- **Standardized Telemetry Pipelines**: Export OpenTelemetry metrics and structured JSON execution logs for ingestion by Python monitoring platforms.

## Limitations
- **Ecosystem Focus**: Exclusively tailored for JavaScript/TypeScript developers; Python data science teams may prefer LangGraph or PydanticAI.
- **Framework Age**: Younger community ecosystem compared to LangChain, though rapidly expanding.
- **State Store Complexity**: Operating high-concurrency multi-agent workflows requires external PostgreSQL or LibSQL database backends.

## When to use it
- When building full-stack, type-safe AI applications or agent microservices in Node.js, Bun, or edge JavaScript runtimes.
- When implementing multi-agent delegation architectures using the Supervisor Pattern.
- When integrating agents with FastMCP 3.1 servers and edge vector databases.

## When not to use it
- For pure Python data pipelines or machine learning research projects where Python frameworks (PydanticAI, LangGraph) are mandatory.
- For simple static prompt templates that do not require tool calling or state orchestration.

## Getting started

### 1. Initialize Mastra Application
```bash
npx create-mastra@latest my-mastra-app
cd my-mastra-app
npm install @mastra/core @mastra/rag @ai-sdk/anthropic zod
```

### 2. Configure Environment Variables
Create `.env` file in the project root:
```env
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-proj-...
FASTMCP_SERVER_URL=http://localhost:8000/mcp
DATABASE_URL=postgresql://mastra:mastrapassword@localhost:5432/mastra_db
```

### 3. Create Agent and Supervisor Configuration
Create `src/mastra/index.ts`:
```typescript
import { Agent, Mastra } from '@mastra/core';
import { anthropic } from '@ai-sdk/anthropic';

export const researcherAgent = new Agent({
  name: 'Researcher',
  instructions: 'Gather research data and summarize key technical details.',
  model: anthropic('claude-5-6-sonnet'),
});

export const writerAgent = new Agent({
  name: 'Writer',
  instructions: 'Synthesize research summaries into technical documentation.',
  model: anthropic('claude-5-6-sonnet'),
});

export const supervisorAgent = new Agent({
  name: 'Supervisor',
  instructions: 'Delegate tasks between Researcher and Writer agents to fulfill user requests.',
  model: anthropic('claude-5-6-sonnet'),
});

export const mastra = new Mastra({
  agents: { researcher: researcherAgent, writer: writerAgent },
  supervisor: supervisorAgent,
});
```

## Systemd Service Unit Configuration

### Production Mastra Engine Service (`/etc/systemd/system/mastra-engine.service`)
```ini
[Unit]
Description=Mastra TypeScript Agent Workflow Engine
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=mastra
Group=mastra
WorkingDirectory=/opt/mastra-app
Environment=NODE_ENV=production
Environment=PORT=4173
EnvironmentFile=/etc/mastra/environment
ExecStart=/usr/bin/node dist/server.js
Restart=always
RestartSec=5s
LimitNOFILE=65536
MemoryMax=8G

# Sandboxing & Security
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/mastra-app/data /var/log/mastra /tmp
NoNewPrivileges=true
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true

[Install]
WantedBy=multi-user.target
```

To enable and inspect the systemd service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now mastra-engine.service
sudo systemctl status mastra-engine.service
journalctl -u mastra-engine.service -f --output=short-iso
```

## Multi-Container Docker Compose Stack

The following production-grade `docker-compose.yml` deploys the Mastra Engine alongside a PostgreSQL state database with pgvector, a FastMCP Python tool bridge container, and Redis for caching:

```yaml
version: "3.8"

services:
  mastra-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mastra-engine
    restart: always
    ports:
      - "4173:4173"
    environment:
      - NODE_ENV=production
      - PORT=4173
      - DATABASE_URL=postgresql://mastra:mastrapassword@postgres:5432/mastra_db
      - REDIS_URL=redis://redis:6379/0
      - FASTMCP_SERVER_URL=http://mcp-bridge:8000
    depends_on:
      postgres:
        condition: service_healthy
      mcp-bridge:
        condition: service_started
    networks:
      - mastra-net

  mcp-bridge:
    build:
      context: ./mcp-bridge
      dockerfile: Dockerfile
    container_name: mastra-mcp-bridge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=info
    networks:
      - mastra-net

  postgres:
    image: pgvector/pgvector:pg16
    container_name: mastra-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_USER=mastra
      - POSTGRES_PASSWORD=mastrapassword
      - POSTGRES_DB=mastra_db
    volumes:
      - pg-data:/var/lib/postgresql/data
    networks:
      - mastra-net
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mastra -d mastra_db"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7.2-alpine
    container_name: mastra-redis
    restart: unless-stopped
    volumes:
      - redis-data:/data
    networks:
      - mastra-net

networks:
  mastra-net:
    driver: bridge

volumes:
  pg-data:
  redis-data:
```

## CLI examples

### Development & Inspection Commands
```bash
# Start local Mastra development server and UI inspector
mastra dev --port 4173

# Inspect registered agents, tools, and workflows
mastra inspect

# Discover and test FastMCP 3.1 tool endpoints
mastra tools discover --mcp-endpoint http://localhost:8000/mcp

# Build production bundle for Node.js / Serverless runtimes
mastra build
```

## API examples

### 1. Mastra Agent Execution with FastMCP 3.1 Tool Calls (TypeScript)
This TypeScript script demonstrates configuring a Mastra agent that interacts with FastMCP 3.1 tools over SSE.

```typescript
import { Agent, Mastra, createTool } from '@mastra/core';
import { anthropic } from '@ai-sdk/anthropic';
import { z } from 'zod';

// Define Mastra native tool wrapping FastMCP endpoint
const systemMetricsTool = createTool({
  id: 'get-system-metrics',
  description: 'Fetch real-time cluster memory and CPU utilization from FastMCP',
  inputSchema: z.object({
    clusterId: z.string().describe('Target infrastructure cluster identifier'),
  }),
  outputSchema: z.object({
    clusterId: z.string(),
    cpuPercent: z.number(),
    memoryPercent: z.number(),
    status: z.string(),
  }),
  execute: async ({ context }) => {
    const res = await fetch('http://localhost:8000/mcp/tools/metrics', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cluster_id: context.clusterId }),
    });
    return await res.json();
  },
});

export const opsAgent = new Agent({
  name: 'DevOpsAgent',
  instructions: 'Monitor infrastructure health and execute remediation tools.',
  model: anthropic('claude-5-6-sonnet'),
  tools: { getSystemMetrics: systemMetricsTool },
});

export const mastraApp = new Mastra({
  agents: { opsAgent },
});

// Execution function
async function runAgent() {
  const agent = mastraApp.getAgent('opsAgent');
  const response = await agent.generate([
    { role: 'user', content: 'Check system health metrics for cluster us-east-1a.' },
  ]);

  console.log('Agent Output:', response.text);
}

runAgent();
```

### 2. FastMCP 3.1 Tool Gateway in Python (Strict Pydantic v2)
A Python FastMCP server providing tools called by Mastra TypeScript agents, using strict Pydantic v2 models with `extra="forbid"`.

```python
#!/usr/bin/env python3
"""
FastMCP 3.1 Tool Bridge Server for Mastra Agent Engine.
Enforces strict Pydantic v2 validation with extra="forbid".
"""

import logging
from typing import Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mastra-mcp-bridge")

mcp = FastMCP("Mastra-Bridge-Server", version="3.1.0")

class ClusterHealthRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    cluster_id: str = Field(..., alias="clusterId", description="Target infrastructure cluster ID")
    detailed_metrics: bool = Field(default=False, alias="detailedMetrics")

class ClusterHealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    clusterId: str
    cpuPercent: float
    memoryPercent: float
    status: str
    activeNodes: int

@mcp.tool(name="metrics", description="Provide real-time cluster health and performance metrics to Mastra agent callers.")
def get_metrics(request: ClusterHealthRequest) -> Dict[str, Any]:
    """Provide real-time cluster metrics to Mastra agent callers."""
    logger.info("Serving cluster health for: %s", request.cluster_id)
    resp = ClusterHealthResponse(
        clusterId=request.cluster_id,
        cpuPercent=34.2,
        memoryPercent=61.8,
        status="healthy",
        activeNodes=12
    )
    return resp.model_dump()

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

### 3. Pydantic v2 Schema Validation for Mastra Supervisor Execution Logs
This Python script validates structured execution telemetry emitted by Mastra supervisor agent workflows.

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator, ValidationError

class ToolExecutionLog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tool_id: str = Field(..., alias="toolId")
    duration_ms: float = Field(..., alias="durationMs", ge=0.0)
    input_payload: Dict[str, Any] = Field(..., alias="inputPayload")
    output_payload: Dict[str, Any] = Field(..., alias="outputPayload")

class SubAgentRunLog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    agent_name: str = Field(..., alias="agentName")
    step_id: str = Field(..., alias="stepId")
    status: str = Field(..., alias="status")
    execution_time_ms: float = Field(..., alias="executionTimeMs", ge=0.0)
    tool_calls: List[ToolExecutionLog] = Field(default_factory=list, alias="toolCalls")

class MastraSupervisorTelemetryLog(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., alias="sessionId")
    supervisor_id: str = Field(..., alias="supervisorId")
    model_name: str = Field(..., alias="modelName")
    total_prompt_tokens: int = Field(..., alias="totalPromptTokens", ge=0)
    total_completion_tokens: int = Field(..., alias="totalCompletionTokens", ge=0)
    sub_agent_runs: List[SubAgentRunLog] = Field(..., alias="subAgentRuns")

def validate_mastra_telemetry(log_json: str) -> Optional[MastraSupervisorTelemetryLog]:
    """Validate Mastra supervisor telemetry JSON payload."""
    try:
        telemetry = MastraSupervisorTelemetryLog.model_validate_json(log_json)
        print(f"[SUCCESS] Validated Telemetry for Mastra Session: {telemetry.session_id}")
        print(f"  Supervisor: {telemetry.supervisor_id} | Model: {telemetry.model_name}")
        print(f"  Tokens: Prompt={telemetry.total_prompt_tokens}, Completion={telemetry.total_completion_tokens}")
        print(f"  Sub-agent Executions: {len(telemetry.sub_agent_runs)}")
        return telemetry
    except ValidationError as err:
        print(f"[ERROR] Telemetry validation failed: {err.error_count()} errors found.")
        print(err.json(indent=2))
        return None

# Sample Telemetry Test Log
sample_telemetry_payload = """
{
    "sessionId": "sess_mastra_99812",
    "supervisorId": "ProjectSupervisor",
    "modelName": "claude-5-6-sonnet",
    "totalPromptTokens": 1420,
    "totalCompletionTokens": 480,
    "subAgentRuns": [
        {
            "agentName": "Researcher",
            "stepId": "step_research_01",
            "status": "completed",
            "executionTimeMs": 320.5,
            "toolCalls": [
                {
                    "toolId": "get-system-metrics",
                    "durationMs": 45.2,
                    "inputPayload": {"clusterId": "us-east-1a"},
                    "outputPayload": {"cpuPercent": 34.2, "status": "healthy"}
                }
            ]
        }
    ]
}
"""

validated_log = validate_mastra_telemetry(sample_telemetry_payload)
```

## Diagnostic Troubleshooting Matrix

| Error Symptom / Log Output | Likely Root Cause | Diagnostic Inspection Command | Remediation & Resolution Steps |
| :--- | :--- | :--- | :--- |
| **Tool Execution Rejection**: `Tool schema mismatch: extra field detected` | Mastra agent passed undeclared arguments to a FastMCP server enforcing `extra="forbid"`. | Inspect Zod tool schema and FastMCP Pydantic model definitions. | Ensure tool schema definitions are synchronized and declare exact parameter names without extra fields. |
| **SSE Connection Drop**: `EventSource failed loading: http://localhost:8000/mcp` | FastMCP Python sidecar crashed or proxy terminated long-running streaming HTTP connection. | `docker logs mastra-mcp-bridge` or `curl -N http://localhost:8000/mcp` | Increase proxy keep-alive timeout and set `transport="sse"` with heartbeat pings enabled on FastMCP server. |
| **Supervisor Infinite Delegation**: `Agent exceeded maximum turn count (10)` | Circular task handoff between sub-agents without convergence condition. | `journalctl -u mastra-engine.service \| grep -i "delegate"` | Refine supervisor system prompt with explicit termination criteria and reduce `maxTurns` limit. |
| **Database Pool Exhaustion**: `remaining connection slots are reserved for non-replication superuser` | High concurrent agent workflows exhausted PostgreSQL connections. | `docker exec -it mastra-postgres psql -U mastra -c "SELECT count(*) FROM pg_stat_activity;"` | Configure connection pooling (PgBouncer) or set `connectionTimeoutMillis: 5000` and `max: 20` in Mastra config. |
| **Out of Memory during Vector Indexing**: `JavaScript heap out of memory` | Ingesting large document collections into local memory vector store without chunk streaming. | `node --max-old-space-size=4096 dist/server.js` | Increase Node heap memory or delegate vector embedding storage directly to external Pgvector or Pinecone. |

## Advanced Architectural Patterns

### The Supervisor Pattern Topology
Mastra's Supervisor Pattern manages multi-agent coordination by separating task routing from domain execution:
1. **Goal Ingestion**: The Supervisor agent evaluates user input and decomposes complex requests into sub-tasks.
2. **Sub-Agent Selection**: Tasks are routed to dedicated sub-agents (e.g., Researcher, Coder, Reviewer).
3. **Execution & Evaluation**: Sub-agents execute tools (FastMCP 3.1) and return results to the Supervisor.
4. **Final Synthesis**: The Supervisor evaluates task completion, iterating if needed, before responding to the caller.

```
[ User Application Request ]
            |
            v
+-------------------------------------------------------------------------+
|                        Mastra Supervisor Agent                          |
|  - Goal Decomposition Engine    - Turn-Taking Evaluation                |
|  - Sub-Agent Task Routing       - Final Output Synthesis                |
+-------------------------------------------------------------------------+
       |                                   |
       v                                   v
+------------------------+       +------------------------+
|    Research Agent      |       |      Coding Agent      |
|  (Claude 5.6 Sonnet)   |       |  (Claude 5.6 Sonnet)   |
+------------------------+       +------------------------+
       |                                   |
       v                                   v
+-------------------------------------------------------------------------+
|                  FastMCP 3.1 Distributed Tool Network                   |
|  - Vector DB Queries     - Web Search     - Code Sandbox Exec         |
+-------------------------------------------------------------------------+
```

## Related tools / concepts
- [LangGraph](langgraph.md) — Python/TS graph agent framework.
- [CrewAI](crewai.md) — Multi-agent role-playing orchestration library.
- [Agno](../agents/agno.md) — Python assistant framework with vector search.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent tools.
- [Vercel AI SDK](../development_ops/vercel-ai-sdk.md) — Primitive streaming library for web apps.
- [LocalAI](../infrastructure/localai.md) — OpenAI-compatible local multi-modal inference server.

## Sources / references
- [Mastra Official Site](https://mastra.ai/)
- [Mastra GitHub Repository](https://github.com/mastra-ai/mastra)
- [Mastra Documentation](https://mastra.ai/docs)
- [Mastra Supervisor Pattern Guide](https://mastra.ai/docs/guide/agents/supervisor-pattern)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

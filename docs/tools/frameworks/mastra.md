# Mastra

## What it is
Mastra is an open-source, full-stack, TypeScript-native framework for building, deploying, and observing agentic AI workflows. It provides an end-to-end environment for agent orchestration, tool integration, vector retrieval, and real-time observability. Mastra features native integration with **FastMCP 3.1** (Model Context Protocol), the **Supervisor Pattern**, and optimized runtime support for **Gemma 4**, **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4** models in Node.js, Bun, and edge runtime environments.

## What problem it solves
Developing agentic AI systems in JavaScript and TypeScript often requires piecing together disparate packages for LLM streaming, vector retrieval, state persistence, and telemetry monitoring. Python-centric frameworks like LangGraph or CrewAI often introduce cross-language runtime complexity or severe cold-start latency when deployed to web edge networks. Mastra solves this by offering a unified, type-safe TypeScript engine with built-in agent supervisor delegation, native FastMCP tool routing, vector memory, and standardized telemetry export pipelines compatible with Python observability suites.

## Where it fits in the stack
**Framework / TypeScript Agent Engine & Orchestration Platform**. Mastra resides at the orchestration and execution layer, connecting web applications, serverless functions, and edge API routes directly to FastMCP tool networks and frontier model providers.

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

### 2. FastMCP 3.1 Tool Gateway in Python
A Python FastMCP server providing tools called by Mastra TypeScript agents.

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("Mastra-Bridge-Server")

class ClusterHealthRequest(BaseModel):
    cluster_id: str = Field(..., alias="cluster_id")

class ClusterHealthResponse(BaseModel):
    clusterId: str
    cpuPercent: float
    memoryPercent: float
    status: str

@mcp.tool(name="metrics")
def get_metrics(request: ClusterHealthRequest) -> ClusterHealthResponse:
    """Provide real-time cluster metrics to Mastra agent callers."""
    return ClusterHealthResponse(
        clusterId=request.cluster_id,
        cpuPercent=34.2,
        memoryPercent=61.8,
        status="healthy"
    )

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=8000)
```

### 3. Pydantic v2 Schema Validation for Mastra Supervisor Execution Logs
This Python script validates structured execution telemetry emitted by Mastra supervisor agent workflows.

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class ToolExecutionLog(BaseModel):
    tool_id: str = Field(..., alias="toolId")
    duration_ms: float = Field(..., alias="durationMs", ge=0.0)
    input_payload: Dict[str, Any] = Field(..., alias="inputPayload")
    output_payload: Dict[str, Any] = Field(..., alias="outputPayload")

class SubAgentRunLog(BaseModel):
    agent_name: str = Field(..., alias="agentName")
    step_id: str = Field(..., alias="stepId")
    status: str = Field(..., alias="status")
    execution_time_ms: float = Field(..., alias="executionTimeMs", ge=0.0)
    tool_calls: List[ToolExecutionLog] = Field(default_factory=list, alias="toolCalls")

class MastraSupervisorTelemetryLog(BaseModel):
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

## Sources / references
- [Mastra Official Site](https://mastra.ai/)
- [Mastra GitHub Repository](https://github.com/mastra-ai/mastra)
- [Mastra Documentation](https://mastra.ai/docs)
- [Mastra Supervisor Pattern Guide](https://mastra.ai/docs/guide/agents/supervisor-pattern)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

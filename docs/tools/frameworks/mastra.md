# Mastra

## What it is
Mastra is an open-source, TypeScript-native framework and enterprise developer platform designed for building, deploying, evaluating, and managing multi-agent systems, complex RAG pipelines, and agentic workflows. Reaching version **v2.5+** in early 2027, Mastra features first-class integration with the **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1**, providing a unified TypeScript engine for agent orchestration, dynamic tool binding, memory management, vector retrieval, and real-time observability. Mastra optimizes model execution across frontier LLMs (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Gemma 4**) in Node.js, Bun, edge, and serverless environments.

## What problem it solves
Developing agentic AI systems in TypeScript has historically suffered from fragmented abstractions, poor type safety across tool boundaries, lack of standardized multi-agent coordination patterns, and cumbersome cross-language observability when communicating with Python data engineering pipelines. Developers frequently had to string together disparate vector databases, custom memory stores, and manual retry loops. Mastra resolves these challenges by providing a unified, type-safe platform featuring a native **Supervisor Pattern**, built-in Language Server Protocol (LSP) diagnostics, sandboxed execution via the **Blaxel sandbox provider**, and structured telemetry exports that can be validated by Python monitoring systems via **Pydantic v2**.

## Where it fits in the stack
**Framework / Agent Platform / Multi-Agent Orchestration Layer**. Mastra sits at the framework and orchestration layer, bridging client application routes (Next.js, Express, Hono) with underlying LLM model providers, FastMCP 3.1 tool servers, and vector database engines.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     Web Client / API Endpoint (Hono / Next.js)              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ Agent Execution & Telemetry
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                             Mastra Core Engine                              │
│         (Supervisor Pattern / Agent Workflows / Vector Store RAG)           │
└──────────────┬──────────────────────────────┬───────────────────────────────┘
               │                              │
               │ FastMCP 3.1 Tool Calls       │ LLM Provider Requests
┌──────────────▼──────────────┐                ┌──────────────▼───────────────┐
│   FastMCP 3.1 Tool Servers  │                │     Frontier AI Models       │
│ (Blaxel Sandbox / Local DB) │                │ (Claude 5.6, GPT-5.6, etc.)  │
└─────────────────────────────┘                └──────────────────────────────┘
```

## Typical use cases
- **Multi-Agent Supervisor Orchestration**: Coordinating specialized agents (e.g., researcher, coder, QA validator) under a central supervisor agent using Mastra's built-in supervisor primitives.
- **Local-First TypeScript AI Agents**: Deploying **Gemma 4** or **Llama 4** agents directly within Node.js or Bun runtimes with native WebAssembly/V8 acceleration.
- **Sandboxed Tool Execution**: Running untrusted agent-generated Python or Bash scripts inside secure, isolated execution sandboxes via the **Blaxel provider**.
- **Enterprise RAG & Hybrid Vector Search**: Executing hybrid vector and metadata-only filtering across knowledge bases without requiring raw embedding generation steps for structured queries.
- **Cross-Language Telemetry Ingestion**: Emitting structured agent execution logs and token usage metrics that Python observability stacks validate using **Pydantic v2**.

## Strengths
- **Native Supervisor Pattern**: Built-in primitives for delegating tasks between agents, tracking multi-step iterations, and isolating context memory.
- **Type-Safe MCP 3.1 Integration**: First-class support for FastMCP 3.1 dynamic tool discovery, task protocol routing, and session state preservation.
- **TypeScript First DX**: Complete end-to-end type safety from tool parameters to agent outputs with real-time LSP diagnostic feedback in IDEs.
- **Multi-Framework Adapters**: Pre-built HTTP deployment adapters for Express, Hono, Fastify, and Koa to expose agents as high-throughput microservices.
- **Comprehensive Observability**: Native tracking of model latency, token costs, tool call payloads, and step-by-step agent trajectory traces.

## Limitations
- **Ecosystem Age Relative to Python**: While rapidly adopted in the JS/TS community, Python frameworks (LangChain, CrewAI) still hold a larger ecosystem of legacy community tools.
- **TypeScript Dependency**: Primarily designed for Node.js/Bun runtimes; teams operating strictly in Python must use REST/gRPC wrappers to integrate with Mastra.

## When to use it
- When building full-stack, type-safe AI agent applications in TypeScript or Next.js.
- When orchestrating multi-agent workflows requiring formal supervisor delegation and execution tracking.
- When executing untrusted agent tools in secure cloud sandboxes (Blaxel).
- When real-time LSP diagnostic feedback and TypeScript model schemas are prioritized for developer productivity.

## When not to use it
- When the data science and agent pipeline is 100% written in Python (consider [Agno](../agents/agno.md) or [PydanticAI](pydantic-ai.md)).
- For simple static prompt templates where a raw model SDK (`@ai-sdk/anthropic`) is sufficient without agent state management.

## Getting started

To initialize a new Mastra project:

1. **Create Project**:
   ```bash
   npx create-mastra@latest my-mastra-app
   cd my-mastra-app
   ```

2. **Configure Environment Variables**:
   Create a `.env` file in the project root:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-...
   OPENAI_API_KEY=sk-proj-...
   ```

3. **Define an Agent (`src/mastra/agents/index.ts`)**:
   ```typescript
   import { Agent } from '@mastra/core';

   export const researcher = new Agent({
     name: 'ResearchAgent',
     instructions: 'You analyze technical documentation and extract key findings.',
     model: { provider: 'ANTHROPIC', name: 'claude-5-6-sonnet' },
   });
   ```

4. **Start Development Server**:
   ```bash
   npm run dev
   ```

## CLI examples

Mastra provides CLI tools for project setup, development server hosting, and MCP tool inspection:

```bash
# Initialize a new Mastra project structure
mastra init my-agent-suite

# Launch local Mastra development server with live observability UI
mastra dev --port 4100

# Inspect available FastMCP 3.1 tools connected to local Mastra server
mastra tools inspect --mcp-url http://localhost:4100

# Run evaluation benchmark suite against agent prompts
mastra eval run --suite accuracy-tests
```

## API examples

### TypeScript: Setting up a Multi-Agent Supervisor System
Building a Supervisor agent pattern with Mastra in TypeScript:

```typescript
import { Agent, Mastra } from '@mastra/core';

// 1. Define Sub-Agents
const researchAgent = new Agent({
  name: 'Researcher',
  instructions: 'Gather facts and inspect documentation.',
  model: { provider: 'ANTHROPIC', name: 'claude-5-6-sonnet' },
});

const codeAgent = new Agent({
  name: 'Coder',
  instructions: 'Generate clean, modular TypeScript code.',
  model: { provider: 'OPENAI', name: 'gpt-5.6' },
});

// 2. Define Manager/Supervisor Agent
const supervisor = new Agent({
  name: 'ProjectManager',
  instructions: 'Delegate tasks between Researcher and Coder, then summarize results.',
  model: { provider: 'GOOGLE', name: 'gemma-4-27b' },
});

// 3. Instantiate Mastra Instance with Supervisor Pattern
export const mastra = new Mastra({
  agents: { researcher: researchAgent, coder: codeAgent },
  supervisor,
});

// 4. Execute Supervisor Workflow
async function executeTask() {
  const result = await mastra.getSupervisor().generate({
    prompt: 'Research FastMCP 3.1 and write a TypeScript connection handler.',
  });
  console.log('Supervisor Completion:', result.text);
}
```

### TypeScript: Exposing Mastra Agent via Hono HTTP Endpoint
```typescript
import { Hono } from 'hono';
import { mastra } from './mastra/index';

const app = new Hono();

app.post('/api/agent/chat', async (c) => {
  const { prompt } = await c.req.json();
  const agent = mastra.getAgent('researcher');

  const response = await agent.generate({ prompt });
  return c.json({
    status: 'success',
    text: response.text,
    usage: response.usage,
  });
});

export default app;
```

### Python: Cross-Language Telemetry Ingestion & Pydantic v2 Validation
When Mastra agents emit execution telemetry to Python data engineering pipelines, strict **Pydantic v2** models validate schema structure and token metrics:

```python
import json
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ValidationError

# 1. Pydantic v2 validation models for Mastra Telemetry JSON
class SubAgentRunLog(BaseModel):
    agent_name: str = Field(..., alias="agentName")
    step_id: str = Field(..., alias="stepId")
    duration_ms: float = Field(..., ge=0.0, alias="durationMs")
    status: Literal["success", "failure", "running"] = Field(default="success")
    logs: List[str] = Field(default_factory=list)

class MastraSupervisorTelemetry(BaseModel):
    session_id: str = Field(..., alias="sessionId")
    supervisor_name: str = Field(..., alias="supervisorName")
    selected_frontier_model: str = Field(..., alias="selectedFrontierModel")
    prompt_tokens: int = Field(..., ge=0, alias="promptTokens")
    completion_tokens: int = Field(..., ge=0, alias="completionTokens")
    sub_agent_runs: List[SubAgentRunLog] = Field(default_factory=list, alias="subAgentRuns")

    @field_validator("selected_frontier_model")
    @classmethod
    def validate_frontier_model(cls, val: str) -> str:
        sota_models = ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra", "DeepSeek-V4", "Gemma 4", "Llama 4"]
        if not any(m in val for m in sota_models):
            raise ValueError(f"Model '{val}' must belong to early 2027 frontier suite: {sota_models}")
        return val

def parse_mastra_telemetry(raw_json: str) -> Optional[MastraSupervisorTelemetry]:
    try:
        telemetry = MastraSupervisorTelemetry.model_validate_json(raw_json)
        print(f"Validated Mastra Telemetry Session [{telemetry.session_id}]")
        print(f"Supervisor: {telemetry.supervisor_name} | Model: {telemetry.selected_frontier_model}")
        print(f"Sub-Agent Steps Recorded: {len(telemetry.sub_agent_runs)}")
        return telemetry
    except ValidationError as err:
        print(f"Mastra Telemetry Validation Failure: {err.errors()}")
        return None

# Test validation
json_payload = """
{
    "sessionId": "sess_mastra_88412",
    "supervisorName": "ProjectManager",
    "selectedFrontierModel": "Claude 5.6",
    "promptTokens": 1240,
    "completionTokens": 450,
    "subAgentRuns": [
        {
            "agentName": "Researcher",
            "stepId": "step_inspect_docs",
            "durationMs": 240.8,
            "status": "success",
            "logs": ["Fetched FastMCP 3.1 specification document."]
        }
    ]
}
"""

validated_data = parse_mastra_telemetry(json_payload)
```

## Comparative Matrix: Mastra vs Alternative Agent Frameworks

| Capability / Feature | Mastra (v2.5+) | LangGraph (TS / Py) | CrewAI (Python) | Agno (Python) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Language** | Native TypeScript | TypeScript & Python | Python | Python |
| **Supervisor Pattern** | First-Class Primitive | Graph State Node | Process/Crew Manager | Team Primitive |
| **FastMCP 3.1 Integration** | Native Built-In | Tool Adapter Required | Custom Tool Wrapper | Native Tool Classes |
| **IDE Diagnostics** | Built-In LSP Support | Standard TS Types | Pydantic Schema Hints | Pydantic Schema Hints |
| **Sandbox Execution** | Native Blaxel Provider | LangChain Sandbox | Local/Docker Sandbox | Docker Containers |
| **HTTP Framework Adapters**| Hono, Express, Fastify, Koa | LangGraph Cloud API | FastAPI / CLI | FastAPI Integration |
| **Vector Search Filtering** | Hybrid + Metadata-Only | Vector Store Retrievers| Knowledge Source RAG | Vector Db Integrations |

## Production Deployment & Optimization Checklist

1. **Sandboxed Tool Security**:
   - Route all dynamic code generation or shell tool execution through the **Blaxel sandbox provider** to prevent local container escapes.

2. **Telemetry Sampling Rate**:
   - In high-throughput production environments, configure Mastra telemetry export sampling to 10-20% to reduce logging bandwidth overhead.

3. **FastMCP 3.1 Session Caching**:
   - Cache FastMCP tool discovery objects across agent runs to minimize handshake latency during multi-turn conversations.

4. **Edge Deployment Target Compatibility**:
   - Ensure external native Node.js C++ modules are excluded when deploying Mastra agents to Cloudflare Workers or Vercel Edge Runtime.

## Step-by-Step Troubleshooting Guide

### Issue 1: "Supervisor agent fails to delegate tasks to sub-agents"
- **Root Cause**: Sub-agent names or capabilities are missing from the supervisor system prompt context, or model context window was exceeded.
- **Resolution**:
  1. Verify sub-agent key registration in `new Mastra({ agents: { researcher, coder } })`.
  2. Increase max steps limit: `generate({ prompt, maxSteps: 10 })`.
  3. Inspect supervisor trajectory logs in Mastra Dev UI (`http://localhost:4100`).

### Issue 2: "LSP diagnostic errors during FastMCP tool schema creation"
- **Root Cause**: Zod or TypeScript schema definitions mismatch expected FastMCP 3.1 parameters.
- **Resolution**:
  1. Ensure `@mastra/core` and `fastmcp` packages are updated to matching major versions.
  2. Run `mastra tools inspect` to validate tool schema compliance.

### Issue 3: "Blaxel sandbox tool execution times out"
- **Root Cause**: Cold start delay on Blaxel sandbox container startup or network proxy block.
- **Resolution**:
  1. Set explicit timeout in tool configuration: `timeout: 15000`.
  2. Verify `BLAXEL_API_KEY` and `BLAXEL_WORKSPACE` environment variables are correctly configured.

## Related tools / concepts
- [Phidata](../agents/phidata.md) — Python assistant framework with memory.
- [LangGraph](langgraph.md) — Graph-based agent orchestration framework.
- [CrewAI](crewai.md) — Role-playing multi-agent framework.
- [Agno](../agents/agno.md) — High-performance Python agent engine.
- [AG2](ag2.md) — Universal multi-agent platform.
- [PydanticAI](pydantic-ai.md) — Python-based type-safe agent framework.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Protocol for agent tools.

## Sources / references
- [Mastra Official Portal](https://mastra.ai/)
- [Mastra Documentation & Guides](https://mastra.ai/docs)
- [Mastra GitHub Repository](https://github.com/mastra-ai/mastra)
- [Mastra Changelog](https://mastra.ai/blog/category/changelogs)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

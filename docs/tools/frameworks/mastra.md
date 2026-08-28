# Mastra

## What it is
Mastra is an open-source, TypeScript-native framework designed for building, deploying, and managing AI agents. It provides a unified platform for agent orchestration, tool integration, and observability. As of early 2027, it has reached **v2.5.0+**, featuring deep integration with the **Model Context Protocol (MCP 3.1)**, **FastMCP 3.1**, and optimized support for **Gemma 4**, Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4 models in local TypeScript and serverless environments.

## What problem it solves
It addresses the fragmentation of AI development in the TypeScript ecosystem. Mastra provides a cohesive set of tools for building reliable agents, connecting them to various data sources via **FastMCP 3.1**, and monitoring their performance. It simplifies multi-agent coordination through first-class primitives like the **Supervisor Pattern** and provides high-performance infrastructure via the **Blaxel sandbox provider**. It also resolves cross-language telemetry challenges by emitting standardized, validated payloads for Python monitoring stacks.

## Where it fits in the stack
**Framework / Agent Platform / Orchestration Layer**. Mastra sits at the orchestration layer, enabling developers to define, run, and monitor agents in TypeScript and integrate them into existing Node.js or edge runtime applications.

## Typical use cases
- **Multi-Agent Coordination**: Orchestrating specialized agents (e.g., researcher + writer) using a central supervisor to delegate and evaluate completion.
- **Local-First AI Agents**: Running [Gemma 4](../ai_knowledge/local_llms.md) agents entirely in the TypeScript runtime with native V8/Wasm acceleration.
- **Enterprise Observability**: Monitoring agent iterations, tool calls, and completion scores in real-time with native LSP diagnostics.
- **High-Performance Sandboxing**: Executing agent tools in secure, isolated environments via the **Blaxel provider**.

## Strengths
- **Supervisor Pattern**: Dedicated primitive for managing delegation, iteration tracking, and context isolation between agents.
- **MCP 3.1 Native**: Built-in support for the latest Task Protocol, enabling dynamic tool discovery and session-aware routing.
- **Developer Experience**: Modern TypeScript-first design with built-in LSP diagnostics for real-time workspace feedback.
- **Flexible Deployment**: Native adapters for Express, Hono, Fastify, and Koa to expose agents as high-performance HTTP endpoints.

## Limitations
- **Ecosystem Maturity**: While rapidly growing, it is still newer than frameworks like LangChain or AutoGen, meaning fewer legacy third-party plugins.
- **TypeScript Only**: Primarily targeted at the Node.js/TypeScript ecosystem, which may exclude Python-heavy data science teams.

## When to use it
- When you want a complete, type-safe platform for building and managing multi-agent systems in TypeScript.
- When you value built-in observability and standardized patterns like the Supervisor Pattern.
- When you need to run agentic tools in secure, managed sandboxes (Blaxel).

## When not to use it
- For simple, one-off AI experiments where a lighter SDK is sufficient.
- If your primary development environment is Python.

## Getting started

### Installation
```bash
npx create-mastra@latest
```

### Basic Supervisor Setup (TypeScript)
```typescript
import { Agent, Mastra } from '@mastra/core';

const supervisor = new Agent({
  name: 'Manager',
  instructions: 'Coordinate the researcher and writer.',
  model: { provider: 'GOOGLE', name: 'gemma-4-27b' },
});

const mastra = new Mastra({
  agents: [researcher, writer],
  supervisor // Enables the Supervisor Pattern
});
```

## CLI examples

### Initializing a Project
```bash
mastra init my-agent-project
```

### Running the Dev Server
```bash
mastra dev
```

### MCP 3.1 Tool Discovery
```bash
mastra tools inspect --mcp-url http://localhost:3000
```

## API examples

### Metadata-Only Vector Query (TypeScript)
```typescript
const results = await mastra.vector.query({
  collection: 'knowledge-base',
  query: 'Early 2027 AI trends',
  metadataOnly: true // Hybrid retrieval without embeddings
});
```

### Python (Mastra Cross-Language Telemetry & Output Validation)
Because Mastra emits structured telemetry for cross-environment monitoring, Python data engineering stacks can parse and validate Mastra supervisor runs using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator

# 1. Define strict validation schemas for Mastra Agent & Supervisor telemetry output
class MastraAgentTelemetry(BaseModel):
    agent_name: str = Field(..., serialization_alias="agentName", validation_alias="agentName")
    step_id: str = Field(..., serialization_alias="stepId", validation_alias="stepId")
    duration_ms: float = Field(..., ge=0, serialization_alias="durationMs", validation_alias="durationMs")
    status: Literal["success", "failure", "running"] = Field(default="success")
    logs: List[str] = Field(default_factory=list)

class MastraSupervisorTelemetry(BaseModel):
    session_id: str = Field(..., serialization_alias="sessionId", validation_alias="sessionId")
    supervisor_name: str = Field(..., serialization_alias="supervisorName", validation_alias="supervisorName")
    sub_agent_runs: List[MastraAgentTelemetry] = Field(..., serialization_alias="subAgentRuns", validation_alias="subAgentRuns")
    completion_tokens: int = Field(..., ge=0, serialization_alias="completionTokens", validation_alias="completionTokens")
    prompt_tokens: int = Field(..., ge=0, serialization_alias="promptTokens", validation_alias="promptTokens")
    selected_frontier_model: str = Field(..., serialization_alias="selectedFrontierModel", validation_alias="selectedFrontierModel")

    @field_validator("selected_frontier_model")
    @classmethod
    def validate_frontier_model(cls, v: str) -> str:
        allowed = ["Claude 5.6", "GPT-5.6", "Gemini 4.0 Ultra", "Llama 4", "Gemma 4", "DeepSeek-V4"]
        if not any(m in v for m in allowed):
            raise ValueError(f"Model {v} must be an early 2027 SOTA model: {allowed}")
        return v

# 2. Simulated Telemetry JSON payload emitted by a Mastra Supervisor
mastra_telemetry_payload = {
    "sessionId": "session-mastra-4091",
    "supervisorName": "ProjectManager",
    "completionTokens": 1024,
    "promptTokens": 512,
    "selectedFrontierModel": "Claude 5.6",
    "subAgentRuns": [
        {
            "agentName": "DocFinder",
            "stepId": "step-retrieve-files",
            "durationMs": 340.5,
            "status": "success",
            "logs": ["Query executed: 'Pydantic v2 validation'", "Retrieved 3 files."]
        }
    ]
}

# 3. Perform strict validation
try:
    telemetry = MastraSupervisorTelemetry(**mastra_telemetry_payload)
    print("Mastra telemetry output validated successfully!")
    print(f"Session ID: {telemetry.session_id}")
    print(f"Supervisor Model: {telemetry.selected_frontier_model}")
    print(f"Prompt / Completion Tokens: {telemetry.prompt_tokens} / {telemetry.completion_tokens}")
    for run in telemetry.sub_agent_runs:
        print(f" - Sub-Agent Run: {run.agent_name} [{run.status}] in {run.duration_ms}ms")
except Exception as e:
    print(f"Telemetry validation failed: {e}")
```

## Related tools / concepts
- [Phidata](../agents/phidata.md) — Assistant framework with memory.
- [LangGraph](langgraph.md) — Graph-based agent coordination.
- [CrewAI](crewai.md) — Multi-agent role-playing framework.
- [Agno](../agents/agno.md) — Rebranded Phidata.
- [AG2](ag2.md) — Universal agent runtime.
- [PydanticAI](pydantic-ai.md) — Python-based type-safe agents.
- [MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Native support in Mastra.
- [Rivet](rivet.md) — Visual agent design.

## Sources / References
- [Official Website](https://mastra.ai/)
- [Mastra Changelog](https://mastra.ai/blog/category/changelogs)
- [GitHub Repository](https://github.com/mastra-ai/mastra)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

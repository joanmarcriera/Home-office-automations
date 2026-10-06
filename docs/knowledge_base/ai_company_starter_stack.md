# AI Company Starter Stack

## What it is
The AI Company Starter Stack is an opinionated blueprint and operational architecture designed to transform traditional enterprise operations into an AI-native organization. Rather than treating AI as disconnected chat widgets or isolated experiments, this framework establishes a unified operating system where workflow orchestrators ([n8n](../services/n8n.md)), procedure packages ([Claude Skills](../tools/agents/claude-skills-ecosystem.md)), persistent context stores ([mem0](../tools/agents/mem0.md)), and frontier models (Claude 5.6, GPT-5.6, DeepSeek-V4, Gemini 4.0 Ultra, Gemma 4, Qwen 3.6 VL) function as cohesive infrastructure.

## What problem it solves
Organizations adopting AI frequently suffer from "tool sprawl"—fragmented SaaS subscriptions, disconnected scripts, duplicated token spending, and shadow AI usage. The AI Company Starter Stack eliminates this fragmentation by specifying an integrated, tiered architecture. It enforces standardized data boundaries, centralized credential vaults, and protocol-native tool execution (FastMCP 3.1) so every autonomous workflow accumulates enterprise intelligence and operational leverage.

## Where it fits in the stack
**Category**: Knowledge Base / Architectural Blueprint. It serves as the top-level **operating system blueprint** across the repository, linking tools from `docs/services/`, `docs/tools/`, and `docs/architecture/` into a turnkey enterprise reference architecture.

## Architecture Diagram
```
+-----------------------------------------------------------------------------------+
|                        AI Company Starter Stack Architecture                      |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Web & Interaction Surface (OpenWebUI, Next.js, FastMCP 3.1 Webhooks)        |  |
|  +-----------------------------------------------------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Control Plane & Workflow Orchestration (n8n, Temporal, Vikunja Task Sync)   |  |
|  +-----------------------------------------------------------------------------+  |
|                     ||                                    ||                      |
|                     \/                                    \/                      |
|  +--------------------------------------+  +-----------------------------------+  |
|  | Context & Memory Layer               |  | FastMCP 3.1 Agent Execution Engine|  |
|  | (mem0, Qdrant, Paperless-ngx, Dolt)  |  | (Claude Skills, Composio, Agno)   |  |
|  +--------------------------------------+  +-----------------------------------+  |
|                                        ||                                         |
|                                        \/                                         |
|  +-----------------------------------------------------------------------------+  |
|  | Inference & Router Layer (Claude 5.6, GPT-5.6, DeepSeek-V4, LocalAI, Ollama) |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Bootstrapping an AI Agency**: Using research pack components to automate market research, client profiling, and outreach.
- **Internal Knowledge Base Modernization**: Combining Paperless-ngx, Unstructured, and Qdrant to convert raw internal files into queryable agent memory.
- **Developer Workflow Automation**: Packaging software delivery SOPs into Claude Skills to run automated CI bug triage and PR generation.
- **Cost-Optimized Local Inference**: Offloading routine classification tasks to Ollama/LocalAI while reserving frontier models for reasoning.

## Strengths
- **Cohesive Interoperability**: Every selected tool natively speaks OpenTelemetry tracing, REST APIs, or FastMCP 3.1 protocols.
- **Cost Controls**: Combines frontier model routing for complex tasks with local inference for routine transformations, drastically lowering API costs.
- **Data Sovereignty**: Keeps sensitive customer records inside self-hosted databases and local vector stores.
- **Fast Deployment**: Provides pre-tested, turn-key configurations that accelerate setup time from months to days.

## Limitations
- **Maintenance Overhead**: Running self-hosted infrastructure (n8n, Qdrant, LocalAI) requires ongoing devops maintenance.
- **Configuration Complexity**: Requires establishing clear FastMCP 3.1 schemas and credential security policies.

## When to use it
- When building a new company and desiring an AI-first operating model from day one.
- When current AI efforts are fragmented across uncoordinated SaaS tools and scripts.
- When needing to enforce strict data privacy boundaries while leveraging frontier models.

## When not to use it
- If looking for a single turnkey SaaS app rather than a multi-component architecture.
- In legacy environments where self-hosted orchestration tools cannot be deployed.

## Getting started
1. **Deploy Core Control Plane**: Set up self-hosted [n8n](../../services/n8n.md) with persistent PostgreSQL storage.
2. **Establish Context Store**: Spin up [Qdrant](../tools/infrastructure/qdrant.md) and [mem0](../tools/agents/mem0.md) for long-term memory.
3. **Configure FastMCP 3.1 Gateway**: Install the FastMCP 3.1 runtime to expose internal database tools to agent clients.
4. **Deploy Frontier & Local Models**: Set up API access keys for frontier providers alongside a local [Ollama](../tools/infrastructure/ollama.md) instance.

## CLI examples
```bash
# Spin up the starter stack core components using Docker Compose
docker compose -f docker-compose.starter-stack.yml up -d

# Initialize a new FastMCP 3.1 workflow project
mcp init enterprise-workflow --version 3.1

# Deploy FastMCP server on port 8080
mcp dev run enterprise-workflow --port 8080
```

## API examples
The following Python script illustrates orchestrating an enterprise agentic task using FastMCP 3.1 and Pydantic v2 validation models:

```python
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, field_validator
from fastmcp import FastMCP

# 1. Initialize FastMCP 3.1 Server for the Starter Stack
mcp = FastMCP(
    name="ai-company-starter-stack-orchestrator",
    version="3.1"
)

# 2. Define Pydantic v2 Task Configuration Models
class WorkflowTaskConfig(BaseModel):
    task_id: str = Field(..., description="Unique task identifier")
    instruction: str = Field(..., min_length=10, description="Task execution objective")
    target_model: str = Field(default="claude-5.6", description="Target model tier")
    context_depth: int = Field(default=3, ge=1, le=10)

    @field_validator("target_model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        valid_models = {"claude-5.6", "gpt-5.6", "deepseek-v4", "local-llama-4"}
        if v.lower() not in valid_models:
            raise ValueError(f"Model must be one of {valid_models}")
        return v.lower()

class TaskExecutionResult(BaseModel):
    task_id: str
    status: str
    summary: str
    tokens_used: int
    cost_estimate_usd: float

# 3. Register Tool Endpoints
@mcp.tool(name="execute_company_task", description="Execute an enterprise agentic task within the starter stack")
def execute_company_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """FastMCP 3.1 tool endpoint for agentic task execution."""
    try:
        task_cfg = WorkflowTaskConfig.model_validate(payload)

        # Simulated execution logic
        result = TaskExecutionResult(
            task_id=task_cfg.task_id,
            status="completed",
            summary=f"Processed objective '{task_cfg.instruction}' using {task_cfg.target_model}",
            tokens_used=1250,
            cost_estimate_usd=0.00375
        )
        return result.model_dump()
    except Exception as e:
        return {
            "task_id": payload.get("task_id", "unknown"),
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [AI Tooling Landscape](ai_tooling_landscape.md)
- [AI Builder Index](ai_builder_index.md)
- [Agent Protocols](agent_protocols.md)
- [Model Routing Guide](model_routing_guide.md)
- [Multi-Agent KnowledgeOps](../architecture/multi_agent_knowledgeops.md)
- [Infrastructure](../architecture/infrastructure.md)

## Sources / references
- [Free AI Website Playbook](free_ai_website_playbook.md)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [FastMCP 3.1 Specification Reference](https://github.com/jlowin/fastmcp)
- [n8n Automation Platform](https://n8n.io/)
- [mem0 Memory Architecture](https://github.com/mem0ai/mem0)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

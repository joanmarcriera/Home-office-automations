# Bee Agent Framework

## What it is
The Bee Agent Framework (v1.6+, early 2027) is an open-source, enterprise-grade orchestration framework developed by IBM Research and hosted under the Linux Foundation. Built explicitly to eliminate the "Reliability Gap" in autonomous agentic workflows, the Bee Agent Framework delivers complete architectural feature parity between **TypeScript** (Node.js/Bun/Browser) and **Python** (3.10–3.12+). It combines deterministic workflow controls, declarative constraint templates, OpenTelemetry-native execution tracing, and native support for **FastMCP 3.1 (Model Context Protocol)** and the **MCP 3.1 Task Protocol**.

Optimized for both cloud frontier reasoning models (GPT-5.6, Claude 5.6, Gemini 4.0 Ultra, DeepSeek-V4) and local open-weights MoE models (Gemma 4 26B, Qwen 3.6, Llama 4), the Bee Agent Framework introduces "Requirement Agents"—specialized runtime guardrail agents that evaluate model output against policy constraints before executing tool calls or returning finalized responses.

## What problem it solves
Autonomous agents operating in production environments frequently suffer from non-deterministic failures:
- **Agent Drift & Infinite Loops**: Autonomous models can get trapped in repetitive tool-invocation loops or lose sight of original system prompt goals.
- **Unverified Tool Execution**: Executing database write operations or external API calls without runtime policy checks creates severe security and data integrity risks.
- **Black-Box Traceability**: Complex multi-step reasoning chains are difficult to debug or audit without standardized OpenTelemetry traces.
- **Language Stack Fragmentation**: Engineering organizations using TypeScript for frontend/edge applications and Python for backend/data pipelines struggle to share agent logic across teams.

The Bee Agent Framework addresses these issues through:
- **Observability-by-Design**: Generates granular, OpenTelemetry-compliant execution traces capturing every prompt state, tool parameter, and token metric.
- **Requirement Agents & Runtime Policy Enforcement**: Intercepts tool calls to validate permissions, parameter boundaries, and compliance rules in real-time.
- **Cross-Language Code Parity**: Shared object schemas and event-driven memory models across TypeScript and Python runtimes.
- **Native FastMCP 3.1 & Task Protocol Support**: Connects seamlessly to remote FastMCP 3.1 servers for dynamic tool discovery and agentic task delegation.

```
+---------------------------------------------------------------------------------------------------+
|                              BEE AGENT FRAMEWORK ARCHITECTURE                                     |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Multi-Language App   |     |  Bee Core Orchestrator|     |  Inference Layer (10+ Drivers)|   |
|   |                       |     |                       |     |                               |   |
|   | - TypeScript / Node   | --> | - BeeAgent Runtime    | --> | - IBM Watsonx.ai              |   |
|   | - Python Data Service |     | - Event System & State|     | - OpenAI (GPT-5.6)            |   |
|   | - Next.js Edge Client |     | - Sliding Memory Window|    | - Local Ollama (Gemma 4)      |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                             |                                 |                   |
|                                             v                                 v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Policy & Audit Layer |     |  Requirement Guardrails|    |  FastMCP 3.1 Tool Gateway     |   |
|   |                       |     |                       |     |                               |   |
|   | - OpenTelemetry Trace | <-- | - Policy Enforcement  | <-- | - Database Tools              |   |
|   | - JSON Audit Logger   |     | - Input Sanitization  |     | - Search & Web Scraping       |   |
|   | - SLA Alert Hooks     |     | - Pydantic v2 Guard   |     | - Enterprise ERP Adapters     |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Agent Orchestration Framework.

The Bee Agent Framework operates at the **Orchestration & Governance Layer**, positioning itself between **Inference Models** (Watsonx, OpenAI, Anthropic, Ollama) and **Tooling/Infrastructure Services** (FastMCP 3.1 servers, databases, search APIs, enterprise ERPs).

## Typical use cases
- **Enterprise Automation Pipelines**: Multi-step administrative workflows requiring strict RBAC policy enforcement, input validation, and audit trails.
- **Multi-Agent Collaboration Networks**: Coordinating specialized sub-agents (e.g. Planning Agent, Execution Agent, Verification Agent) to resolve complex user requests.
- **Polyglot Monorepo Deployments**: Sharing identical agent execution trees between Next.js React frontend applications and Python FastAPI microservices.
- **Hybrid Cloud / Local LLM Networks**: Routing routine background sub-tasks to local Gemma 4 instances while delegating complex reasoning steps to Claude 5.6 or GPT-5.6.

## Strengths
- **Enterprise-Grade Reliability**: Built-in Requirement Agents and policy guardrails minimize hallucinated tool calls.
- **Strict Open Governance**: Hosted by the Linux Foundation (LF AI & Data), protecting against single-vendor lock-in.
- **Full TypeScript & Python Parity**: Identical framework classes and patterns across both primary language stacks.
- **Built-In OpenTelemetry Tracing**: First-class support for OTel exporters (Jaeger, Prometheus, ClickHouse, Grafana Tempo).
- **FastMCP 3.1 & Task Protocol Compliant**: Standardized tool calling and task delegation protocols out-of-the-box.

## Limitations
- **Slightly Higher Boilerplate**: Focusing on enterprise reliability introduces more abstractions (Workflows, Providers, Guardrails) than minimal scripting frameworks.
- **Ecosystem Growth Phase**: While backed by IBM and Linux Foundation, community tool repositories are actively growing compared to older frameworks like LangChain.

## When to use it
- When building production AI systems that demand strict governance, policy enforcement, and audit-ready execution traces.
- When working in a polyglot environment requiring shared agent logic across TypeScript and Python codebases.
- When integrating with FastMCP 3.1 tool servers and enterprise Watsonx or cloud LLM infrastructures.

## When not to use it
- For quick, single-script AI prototypes where lightweight wrappers (LiteLLM, Agno) are faster to write.
- When running on resource-constrained micro-controllers or embedded edge hardware with strict memory constraints.

## Getting started

### Installation
=== "TypeScript"
    ```bash
    npm install @beeai/framework pydantic-mcp
    ```
=== "Python"
    ```bash
    pip install beeai-framework pydantic mcp
    ```

## CLI examples

```bash
# Initialize a new Bee Agent project template
beeai init my-enterprise-agent --template multi-agent

# Launch the development server with hot-reloading enabled
beeai dev --port 18788 --verbose

# Verify FastMCP 3.1 server connectivity using Task Protocol
beeai mcp verify http://localhost:18790 --protocol task-v3.1
```

## API examples

=== "TypeScript"
    ```typescript
    import { BeeAgent } from "@beeai/framework/agents/bee/agent";
    import { UnstructuredRawModel } from "@beeai/framework/backend/unstructured";
    import { DuckDuckGoSearchTool } from "@beeai/framework/tools/search/duckduckgo";

    async function main() {
        const agent = new BeeAgent({
            llm: new UnstructuredRawModel({ modelId: "gpt-5.6" }),
            tools: [new DuckDuckGoSearchTool()],
            memory: []
        });

        const response = await agent.run({ prompt: "Synthesize key architectural benefits of BeeAI Framework." });
        console.log("Agent Result:\n", response.result.text);
    }
    main();
    ```

=== "Python"
    ```python
    import asyncio
    from beeai_framework.agents.bee.agent import BeeAgent
    from beeai_framework.backend.chat import ChatModel
    from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool

    async def main():
        agent = BeeAgent(
            llm=ChatModel.from_name("openai:gpt-5.6"),
            tools=[DuckDuckGoSearchTool()],
            memory=[]
        )

        response = await agent.run(prompt="Analyze the benefits of cross-language agent frameworks.")
        print("Agent Output:\n", response.result.text)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

## FastMCP 3.1 Integration Pattern

Below is a complete FastMCP 3.1 tool server demonstrating how Bee Agent Framework instances can query remote tools and validate execution payloads:

```python
import asyncio
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("BeeFrameworkToolGateway", version="3.1.0")

class AgentTaskExecutionRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    agent_id: str = Field(..., description="Unique Bee Agent identifier")
    task_prompt: str = Field(..., min_length=5, description="Prompt assigned to agent")
    model_provider: str = Field("openai:gpt-5.6", description="Active LLM provider identifier")
    allowed_tools: List[str] = Field(default_factory=list, description="Permitted tool set")

class AgentTaskExecutionResponse(BaseModel):
    task_id: str
    status: str
    steps_completed: int
    output_summary: str
    telemetry_trace_id: str

@mcp.tool()
def execute_bee_agent_task(
    agent_id: str,
    task_prompt: str,
    model_provider: str = "openai:gpt-5.6"
) -> str:
    """
    FastMCP tool wrapper executing a managed Bee Agent task step.
    Returns JSON string fulfilling AgentTaskExecutionResponse schema.
    """
    # Validate payload
    req = AgentTaskExecutionRequest(
        agent_id=agent_id,
        task_prompt=task_prompt,
        model_provider=model_provider,
        allowed_tools=["DuckDuckGoSearchTool", "CalculatorTool"]
    )

    # Simulated Bee Agent execution
    response = AgentTaskExecutionResponse(
        task_id=f"tsk_bee_{int(asyncio.get_event_loop().time())}",
        status="completed",
        steps_completed=3,
        output_summary=f"Bee Agent '{req.agent_id}' successfully executed task: '{req.task_prompt[:40]}...'",
        telemetry_trace_id="tr_bee_99120_otel"
    )
    return response.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Type-Safe Observability & Trace Verification (Pydantic v2)

To enforce enterprise auditability, telemetry traces generated by Bee Agents are validated using **Pydantic v2**:

```python
from datetime import datetime
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ToolInvocationRecord(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    tool_name: str = Field(..., description="Name of executed tool")
    arguments: dict = Field(default_factory=dict)
    execution_time_ms: float = Field(..., ge=0.0)
    success: bool = Field(True)

class TokenTelemetry(BaseModel):
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    total_tokens: int = Field(..., ge=0)

class BeeAgentTrace(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    trace_id: str = Field(..., description="Unique OpenTelemetry trace ID")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    model_name: str = Field(...)
    steps_count: int = Field(..., ge=1)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    tool_calls: List[ToolInvocationRecord] = Field(default_factory=list)
    telemetry: TokenTelemetry
    status: Literal["success", "failed", "policy_violated", "halted"] = Field("success")

    @field_validator("model_name")
    @classmethod
    def validate_model_name(cls, val: str) -> str:
        if not val or len(val) < 3:
            raise ValueError("Invalid model_name identifier in trace.")
        return val

# Demonstration of trace validation
sample_trace_payload = {
    "trace_id": "bee-trace-99120-2027",
    "model_name": "gpt-5.6",
    "steps_count": 3,
    "confidence_score": 0.98,
    "tool_calls": [
        {
            "tool_name": "DuckDuckGoSearchTool",
            "arguments": {"query": "FastMCP 3.1 specifications"},
            "execution_time_ms": 112.5,
            "success": True
        }
    ],
    "telemetry": {
        "prompt_tokens": 1250,
        "completion_tokens": 480,
        "total_tokens": 1730
    },
    "status": "success"
}

validated_trace = BeeAgentTrace(**sample_trace_payload)
print("Validated Bee Agent Trace:\n", validated_trace.model_dump_json(indent=2))
```

## Related tools / concepts
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md): Standardized tool and task protocol definitions.
- [LangGraph](../frameworks/langgraph.md): Graph-based agent orchestration framework.
- [Claude Skills Ecosystem](claude-skills-ecosystem.md): Modular skill packages for Claude Code.
- [Phidata](phidata.md): Framework for building autonomous assistant systems.
- [Agno](agno.md): Lightweight agent framework.
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md): Open reasoning model family.
- [Local LLMs (Gemma 4, Qwen 3.6)](../ai_knowledge/local_llms.md): Open-weights model execution.

## Sources / references
- [BeeAI Framework GitHub Repository](https://github.com/i-am-bee/beeai-framework)
- [Official BeeAI Documentation](https://i-am-bee.github.io/beeai-framework/)
- [IBM Research: AI Agent Reliability with BeeAI](https://research.ibm.com/blog/ai-agent-reliability-beeai)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

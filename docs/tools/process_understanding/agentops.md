# AgentOps

## What it is
AgentOps is a specialized, enterprise-grade observability, telemetry, and evaluation platform engineered specifically for autonomous AI agents and multi-agent teams. It provides a comprehensive suite of tools for tracking agent performance, debugging complex multi-step reasoning workflows, visualizing prompt chains, and monitoring production agent deployments across frontier model ecosystems in early 2027.

## What problem it solves
Developing autonomous agents is uniquely challenging due to their non-deterministic execution paths, recursive loops, and the high complexity of multi-turn tool interactions. AgentOps solves the "black box" problem by providing:
- **Execution Transparency**: Step-by-step agent execution graphs, trace nesting, and complete session replays.
- **Reliability Tracking**: Direct identification of infinite loops, recursive thought anti-patterns, and tool selection failures.
- **Cost Management**: Real-time tracking of token spend across 400+ LLM providers via gateways like [LiteLLM](../../services/litellm.md).
- **Benchmarking & Guardrails**: Rigorous evaluation metrics to measure agent task success, tool utilization rates, and compliance against guardrail policies.

## Where it fits in the stack
AgentOps sits in the **AI Observability and Developer Tooling** layer. It is specifically optimized for agentic frameworks and provides native, first-class support for multi-agent orchestration and **FastMCP 3.1 / Model Context Protocol** tool calls.

## Typical use cases
- **Multi-Agent Orchestration**: Monitoring interactions and task handoffs between agents in frameworks like [CrewAI](../frameworks/crewai.md), AG2 ([AutoGen](../frameworks/autogen.md)), or [LangGraph](../frameworks/langgraph.md).
- **FastMCP Tool Observability**: Tracking calls to [MCP](../automation_orchestration/mcp.md) servers to identify tool latency, payload sizes, and failure rates under FastMCP 3.1.
- **Debugging Tool Failures**: Investigating exact model inputs and tool responses when agents fail or select incorrect parameters.
- **Production Session Analysis**: Replaying user-agent interactions powered by models like **Claude 5.1 Opus** or **GPT-5.5** to identify edge cases and improve agent reliability.
- **Token and Bill Tracking**: Monitoring real-time token spend across long-running autonomous tasks across multiple model providers.

## Strengths
- **Framework Native**: Deep, multi-framework integrations with [CrewAI](../frameworks/crewai.md), [AutoGen](../frameworks/autogen.md), LangChain, LlamaIndex, and Smolagents.
- **Agent-Centric UI**: A dedicated dashboard designed for agentic flows, featuring session replays, directed event graphs, and structured agent metadata.
- **Fine-tuning Support**: Ability to export successful multi-turn agent execution traces to fine-tune specialized open-weights models (e.g., Llama 4, Qwen 3.8), reducing operational costs by up to 30%.
- **PII & Guardrail Security**: Built-in security features including honeypot detection, PII redacting, and prompt injection defenses via PromptArmor integration.

## Limitations
- **Specialization**: Designed specifically for multi-step agentic workflows; may introduce unnecessary overhead for static RAG or simple single-prompt applications.
- **Cloud-Centric**: While self-hosting options exist, the full feature set and analytics suite are optimized for the AgentOps cloud environment.
- **Instrumentation Overhead**: Detailed tracing requires properly instrumenting custom agent classes, decorators, and tool execution functions.

## When to use it
- When building multi-agent systems that require detailed tracking of agent handoffs and collaborative task execution.
- When you need a persistent "Flight Recorder" for autonomous agents to debug non-deterministic failures in production.
- When using popular agent frameworks like [CrewAI](../frameworks/crewai.md), [AutoGen](../frameworks/autogen.md), or [LangGraph](../frameworks/langgraph.md) and requiring instant observability.
- When monitoring and controlling LLM costs across a variety of providers within a unified management dashboard.

## When not to use it
- For basic chat applications where standard request/response logging (like [Helicone](helicone.md)) is sufficient.
- If you require an entirely local, offline observability tool without any external dependencies or cloud components.
- If your application does not follow agentic patterns (no autonomous tool use or multi-step reasoning).

## Getting started

### Installation
```bash
pip install agentops pydantic
```

### Basic Integration
AgentOps can be integrated with minimal setup by initializing the client session.

```python
import os
import agentops

# Initialize the AgentOps client
# agentops.init() reads AGENTOPS_API_KEY from environment variables
agentops.init(api_key=os.getenv("AGENTOPS_API_KEY", "your-api-key"), tags=["production-v2"])

# Your agentic execution logic here...
# e.g., executing agent workflows with CrewAI or AutoGen

# End session with explicit status reporting
agentops.end_session('Success')
```

### Using Decorators for Custom Agents
For custom agent implementations, use decorators to maintain a rich trace hierarchy.

```python
from agentops.sdk.decorators import agent, operation
from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    query: str = Field(description="Search topic query")
    max_results: int = Field(default=5, ge=1, le=20)

@agent
class ResearchAgent:
    def __init__(self, name: str):
        self.name = name

    @operation
    def search_topic(self, request: ResearchRequest) -> str:
        # Custom research execution logic...
        return f"Retrieved {request.max_results} results for query: '{request.query}'"

def run_research() -> str:
    my_agent = ResearchAgent("SeniorResearcher")
    req = ResearchRequest(query="FastMCP 3.1 protocol advancements", max_results=10)
    return my_agent.search_topic(req)
```

## CLI examples

### Initializing AgentOps Project
```bash
# Set your API key in the environment
export AGENTOPS_API_KEY="your_api_key_here"
```

### Checking Agent Health
```bash
# Verify API key configuration and connectivity
python -c "import agentops; print(f'AgentOps API Key set: {bool(agentops.get_api_key())}')"
```

### Exporting Session Data
```bash
# Export session trace data for offline evaluation
agentops export --session_id "sess_abc123" --format json
```

## API examples

### Recording Tool Usage with FastMCP 3.1
Track specific FastMCP 3.1 tool invocations using Pydantic v2 structured payload validation.

```python
from typing import Dict, Any
import agentops
from pydantic import BaseModel, Field

class FastMCPToolCall(BaseModel):
    tool_name: str = Field(description="Name of the MCP tool")
    server_id: str = Field(description="ID of the target FastMCP 3.1 server")
    parameters: Dict[str, Any] = Field(default_factory=dict)

@agentops.sdk.decorators.operation
def execute_mcp_tool(payload: FastMCPToolCall) -> Dict[str, Any]:
    # Record structured FastMCP action in AgentOps session trace
    agentops.record_action(
        f"Calling FastMCP Tool: {payload.tool_name}",
        params={"server": payload.server_id, "args": payload.parameters}
    )
    # Tool execution logic...
    return {"status": "success", "tool": payload.tool_name, "output": "Execution complete"}
```

### Handling Multi-Model Sessions
Track performance and cost across **Claude 5.1 Opus** and **GPT-5.5** within a single session.

```python
import agentops

def run_multi_model_session() -> None:
    # Initialize session with model comparison tags
    agentops.init(tags=["multi-model-eval", "claude-5-1", "gpt-5-5"])

    # Step 1: Execute Claude 5.1 reasoning task
    agentops.record_action("Reasoning Step", params={"model": "claude-5-1-opus-20261031"})

    # Step 2: Execute GPT-5.5 code generation task
    agentops.record_action("Code Generation Step", params={"model": "gpt-5.5-preview"})

    # Complete session with explicit status
    agentops.end_session('Success')
```

## Related tools / concepts
- [Langfuse](langfuse.md) - Open-source observability and evaluation platform.
- [Helicone](helicone.md) - Proxy-based LLM observability and gateway.
- [Arize AI](arize-ai.md) - Enterprise-grade ML observability and evaluation.
- [W&B Weave](wandb-weave.md) - Lightweight tracing for ML workflows.
- [MCP](../automation_orchestration/mcp.md) - Model Context Protocol for connecting agents to tools.
- [Claude](../ai_knowledge/claude.md) - Frontier model suite powering complex agent systems.
- [CrewAI](../frameworks/crewai.md) - Multi-agent framework with native AgentOps integration.
- [AutoGen](../frameworks/autogen.md) - Microsoft's multi-agent conversational framework.
- [LiteLLM](../../services/litellm.md) - Gateway integrating with AgentOps for unified cost tracking.

## Sources / references
- [AgentOps Official Website](https://www.agentops.ai/)
- [AgentOps Documentation](https://docs.agentops.ai/introduction)
- [AgentOps GitHub Repository](https://github.com/AgentOps-AI/agentops)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

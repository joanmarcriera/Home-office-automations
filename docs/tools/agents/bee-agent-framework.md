# Bee Agent Framework

## What it is
The Bee Agent Framework (v1.6+, early January 2027) is an open-source framework by IBM Research for building, deploying, and orchestrating production-grade AI agents. It provides complete feature parity between TypeScript and Python, allowing for robust multi-agent systems with native Model Context Protocol (MCP 3.1) and [MCP 3.1 / FastMCP 3.1 Task Protocol](../../knowledge_base/agent_protocols.md) support.

## What problem it solves
It focuses on the "Reliability Gap" in autonomous agents. By providing "Requirement Agents" that enforce runtime policies and "Observability-by-Design" via detailed execution traces, Bee ensures that complex multi-step agentic workflows remain predictable, auditable, and production-ready. It is specifically optimized for [Gemma 4](../ai_knowledge/local_llms.md), [Qwen 3.6](../ai_knowledge/local_llms.md), and frontier models like [GPT-5.6](../ai_knowledge/openai.md), [Claude 5.6](../providers/anthropic.md), and [Gemini 4.0 Ultra](../ai_knowledge/gemini.md).

## Where it fits in the stack
**Category**: Agent Orchestration Framework. It sits between the Model/Inference layer (supporting 10+ providers like Watsonx, Ollama, and OpenAI) and the Tool/Infrastructure layer, managing state, memory, and tool execution.

## Typical use cases
- **Enterprise Automation**: Workflows requiring strict governance, policy enforcement, and audit trails.
- **Multi-Agent Orchestration**: Systems where specialized agents (Planner, Executor, Reviewer) must collaborate on complex tasks.
- **Cross-Platform Development**: Projects that require shared agent logic between TypeScript (web/frontend) and Python (data/backend) environments.
- **Hybrid Cloud Agents**: Deploying agents that bridge local [Gemma 4](../ai_knowledge/local_llms.md) instances with enterprise Watsonx.ai models.

## Strengths
- **Reliability**: Built-in safeguards and policy enforcement agents to minimize agent drift and failure.
- **Observability**: Industry-leading execution tracing and OpenTelemetry integration.
- **Language Parity**: Simultaneous support for TypeScript and Python with identical architectural patterns.
- **Protocol Native**: Full, first-class support for MCP 3.1 and the Agentic Session Orchestration pattern.
- **Governance**: Hosted by the Linux Foundation under open governance for long-term stability.

## Limitations
- **Learning Curve**: The focus on enterprise reliability introduces more abstractions (Workflows, Templates, Providers) than minimal frameworks like Agno.
- **Overhead**: The comprehensive feature set may introduce more latency and resource usage than lightweight alternatives for simple tasks.
- **Maturity**: While robust, the ecosystem of community-contributed tools is still growing compared to LangChain.

## When to use it
- **Production AI Systems**: When you need a framework designed for scale, security, and enterprise-grade reliability.
- **Deep Observability Requirements**: If your use case requires detailed tracing to debug or audit complex agent decisions.
- **Multi-Language Teams**: When your organization utilizes both TS and Python and wants a unified agent architecture.
- **Linux Foundation Alignment**: If your project requires an open-governance framework with no vendor lock-in.

## When not to use it
- **Rapid Prototyping**: For simple, one-off scripts, lightweight SDKs like LiteLLM or raw provider APIs are faster.
- **Minimal Resource Environments**: If running on extremely constrained hardware where framework overhead must be minimized.
- **Single-Agent Chatbots**: For basic conversational UI without complex tool use or state management, Bee might be overkill.

## Getting started

### Installation
=== "TypeScript"
    ```bash
    npm install @beeai/framework
    ```
=== "Python"
    ```bash
    pip install beeai-framework pydantic
    ```

### Basic Agent Setup
Initialize a Bee agent with a provider (e.g., Watsonx or OpenAI) and a set of tools. Bee also supports local execution with [Gemma 4](../ai_knowledge/local_llms.md) via [Ollama](../../services/ollama.md).

## CLI examples
```bash
# Initialize a new Bee project template
beeai init my-enterprise-agent --template multi-agent

# Start the Bee development server with live-reloading
beeai dev --port 18788 --verbose

# Validate MCP server connectivity using Task Protocol and FastMCP 3.1
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

        const response = await agent.run({ prompt: "Synthesize a report on BeeAI framework updates." });
        console.log(response.result.text);
    }
    main();
    ```
=== "Python"
    ```python
    from beeai_framework.agents.bee.agent import BeeAgent
    from beeai_framework.backend.chat import ChatModel
    from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool

    agent = BeeAgent(
        llm=ChatModel.from_name("openai:gpt-5.6"),
        tools=[DuckDuckGoSearchTool()],
        memory=[]
    )

    response = agent.run(prompt="Analyze the benefits of multi-language agent frameworks.")
    print(response.result.text)
    ```

### Strict Schema Trace Verification (Python & Pydantic v2)
To enforce strict reliability, enterprise deployments use Pydantic v2 to validate execution trace schemas and token usage parameters generated by the Bee Agent:

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class ToolInvocationSchema(BaseModel):
    tool_name: str = Field(..., description="The name of the invoked MCP or native tool.")
    arguments: dict = Field(default_factory=dict, description="Input arguments passed to the tool.")
    execution_time_ms: float = Field(..., ge=0.0)
    success: bool = Field(True)

class TokenTelemetry(BaseModel):
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    total_tokens: int = Field(..., ge=0)

class BeeAgentTrace(BaseModel):
    trace_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    model_name: str
    steps_count: int = Field(..., ge=1)
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    tool_calls: List[ToolInvocationSchema] = Field(default_factory=list)
    telemetry: TokenTelemetry
    status: str = Field("success")

    @field_validator("status")
    @classmethod
    def validate_status(cls, val: str) -> str:
        allowed = {"success", "failed", "policy_violated", "halted"}
        if val not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return val

# Example parsing and verifying a trace generated by the agentic run
sample_trace_data = {
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

validated_trace = BeeAgentTrace(**sample_trace_data)
print(f"Verified Trace ID: {validated_trace.trace_id} with Status: {validated_trace.status}")
```

## Related tools / concepts
- [Agent Protocols (MCP)](../../knowledge_base/agent_protocols.md)
- [MCP 3.1 / FastMCP 3.1](../../knowledge_base/patterns/data-copilot-mcp-tooling.md)
- [LangGraph](../frameworks/langgraph.md)
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Phidata](phidata.md)
- [Superpowers](superpowers.md)
- [Agno](agno.md)
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Local LLMs (Gemma 4, Qwen 3.6)](../ai_knowledge/local_llms.md)

## Sources / References
- [BeeAI Framework GitHub Repository](https://github.com/i-am-bee/beeai-framework)
- [Official BeeAI Documentation](https://i-am-bee.github.io/beeai-framework/)
- [IBM Research: AI Agent Reliability with BeeAI](https://research.ibm.com/blog/ai-agent-reliability-beeai)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

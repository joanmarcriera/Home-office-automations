# Smolagents

## What it is
Smolagents is a lightweight, high-performance agent framework developed by Hugging Face. Focused on simplicity, speed, and clean code paths, it is optimized for creating small, highly specialized agents that leverage tool-calling or direct code execution. As of late 2026, smolagents has progressed to **v1.8.0+**, featuring native integration with the **Model Context Protocol (MCP 3.1)**, **FastMCP 3.1**, and native secure execution of agent-written code.

## What problem it solves
Many traditional agent frameworks are bloated, introducing heavy abstractions, complex dependency chains, and significant latency overhead. Smolagents provides a "minimalist" approach to tool-calling and code-writing agents. It solves the developer experience (DX) and speed challenges of edge and serverless environments, making it incredibly straightforward to build, run, and audit specialized agents using local models or frontier model endpoints.

## Where it fits in the stack
**Category**: Frameworks / Agent Library / Lightweight Agent Platform

## Typical use cases
- **Personal Assistants**: Lightweight agents running locally on your workstation for files, mail, and system automation.
- **Edge Computing**: Running quantized [Gemma 3](../ai_knowledge/local_llms.md) or Llama 4 models on devices with limited memory.
- **Micro-Agents**: Specialized sub-agents acting within a larger multi-agent architecture (e.g., orchestrators calling a dedicated smolagent for code execution).
- **Code-Based Task Solving**: Using the framework's unique `CodeAgent` to write and evaluate Python code block trajectories to answer reasoning-heavy questions.

## Strengths
- **Minimal Footprint**: Light dependencies, clear codebase, and very low execution overhead.
- **Code-as-Actions (CodeAgent)**: Unique ability to solve problems by writing and executing Python blocks in a local or containerized sandbox.
- **Native Python Tools**: Elegant, decorator-driven custom tool creation using pure Python function definitions (`@tool`).
- **Hugging Face Ecosystem Native**: Seamlessly leverages Hugging Face Hub, `transformers`, and local `vllm`/Ollama endpoints.
- **FastMCP 3.1 Support**: Dynamic, standard-compliant connection to remote tools and resources.

## Limitations
- **Feature Scope**: Does not provide out-of-the-box support for complex database routing or high-level visual workflow builders.
- **Persistent State**: Persistent state machines and multi-turn session databases require custom setup.

## When to use it
- When you want a simple, highly transparent agent implementation without heavy-weight wrapper abstractions.
- For building specialized, fast, single-purpose micro-agents.
- When working heavily with local LLMs (via Ollama or vLLM) or Hugging Face repository resources.
- For code-execution agent workflows where the model solves problems via Python scripts.

## When not to use it
- For enterprise-scale legacy workflows that require deep, complex database integrations out of the box.
- When visual design canvases or flow-chart interfaces are required for non-technical users.

## Getting started

### Installation
```bash
pip install smolagents
```

### Minimal Python Example
```python
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

# Define the agent with a search tool
agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel())

# Run a task
agent.run("What is the current population of Tokyo?")
```

## CLI examples

```bash
# Running a smolagents script
python my_agent.py

# Launching a smolagents developer terminal UI
smolagents chat --model "meta-llama/Llama-3.3-70B-Instruct"

# Inspecting local and remote tool definitions
smolagents tools list
```

## API examples

### CodeAgent with Local Ollama
```python
from smolagents import CodeAgent, LiteLLMModel

# Initialize with a local Ollama model via LiteLLM
model = LiteLLMModel(
    model_id="ollama/llama3",
    api_base="http://localhost:11434"
)

agent = CodeAgent(tools=[], model=model)
agent.run("Calculate the first 10 Fibonacci numbers using a recursive function.")
```

### Custom Tool and Run Verification (Python with Pydantic v2)
In late 2026/2027 enterprise pipelines, agent outputs and tool arguments must be strictly validated before execution to prevent malicious or malformed tool invocation. Smolagents custom tool structures and agent execution logs can be validated using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field, field_validator
from smolagents import tool, CodeAgent, HfApiModel

# 1. Define strict validation schemas for Smolagents tool execution logs and agent runs
class SmolagentToolCall(BaseModel):
    tool_name: str = Field(..., serialization_alias="toolName", validation_alias="toolName")
    arguments: Dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = Field(..., ge=0, serialization_alias="executionTimeMs", validation_alias="executionTimeMs")

class SmolagentRunTrace(BaseModel):
    agent_id: str = Field(..., serialization_alias="agentId", validation_alias="agentId")
    frontier_model: str = Field(..., serialization_alias="frontierModel", validation_alias="frontierModel")
    steps: List[SmolagentToolCall] = Field(default_factory=list)
    final_answer: str = Field(..., serialization_alias="finalAnswer", validation_alias="finalAnswer")

    @field_validator("frontier_model")
    @classmethod
    def validate_frontier_model(cls, v: str) -> str:
        allowed = ["Claude 5.1", "GPT-5.5", "Gemini 4.0", "Llama 4", "Gemma 3"]
        if not any(model in v for model in allowed):
            raise ValueError(f"Model {v} must be a modern SOTA model: {allowed}")
        return v

# 2. Define a decorator-based tool conforming to smolagents specifications
@tool
def get_weather_forecast(location: str) -> str:
    """
    Retrieves the weather forecast for a specified city and state.

    Args:
        location: The city and state, e.g. "Seattle, WA"
    """
    return f"The forecast for {location} is rainy with a high of 52°F."

# 3. Simulate and Validate a Smolagent Execution Run Trace in Python
run_payload = {
    "agentId": "agent-smol-409",
    "frontierModel": "Claude 5.1",
    "finalAnswer": "The weather in Seattle, WA is rainy with a high of 52 degrees Fahrenheit.",
    "steps": [
        {
            "toolName": "get_weather_forecast",
            "arguments": {"location": "Seattle, WA"},
            "executionTimeMs": 112.5
        }
    ]
}

try:
    trace = SmolagentRunTrace(**run_payload)
    print("Smolagent execution trace validated successfully via Pydantic v2!")
    print(f"Agent ID: {trace.agent_id}")
    print(f"Frontier Model: {trace.frontier_model}")
    print(f"Final Answer: {trace.final_answer}")
    for step in trace.steps:
        print(f"  - Called Tool: {step.tool_name} with args {step.arguments} (Took {step.execution_time_ms}ms)")
except Exception as e:
    print(f"Trace validation failed: {e}")
```

## Related tools / concepts
- [LangChain](../../tools/ai_knowledge/langchain.md)
- [Hugging Face Hub](../../tools/providers/huggingface.md)
- [AutoGen](autogen.md)
- [DSPy](dspy.md)
- [Haystack](haystack.md)
- [LangGraph](langgraph.md)
- [Semantic Kernel](semantic-kernel.md)
- [vLLM](../../tools/infrastructure/vllm.md)
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md)

## Sources / references
- [GitHub](https://github.com/huggingface/smolagents)
- [Blog Post](https://huggingface.co/blog/smolagents)
- [Hugging Face Agents Documentation](https://huggingface.co/docs/smolagents/index)

## Contribution Metadata
- Last reviewed: 2026-12-10
- Confidence: high

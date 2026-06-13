# Smolagents

## What it is
Smolagents is a lightweight and efficient agent framework developed by Hugging Face. It focuses on simplicity, speed, and ease of use, making it ideal for building small, specialized agents that use tools.

## What problem it solves
Many agent frameworks are heavy and introduce significant abstraction overhead. Smolagents provides a "minimalist" approach to tool-calling agents, making them easier to understand, debug, and deploy in resource-constrained environments or as part of larger microservices.

## Where it fits in the stack
**Framework / Agent Library**. It serves as a lightweight alternative to larger orchestrators, optimized for fast inference and local model integration.

## Typical use cases
- **Personal Assistants**: Small agents for local task automation.
- **Edge Computing**: Running agents on devices with limited resources using quantized models.
- **Micro-Agents**: Specialized agents within a larger multi-agent architecture.
- **Rapid Prototyping**: Testing tool-calling capabilities of frontier models like `claude-4-8-opus-20260528`.

## Strengths
- **Lightweight**: Minimal dependencies and small code footprint.
- **Native Python Tools**: Simple decorator-based tool definition (`@tool`).
- **Hugging Face Integration**: Seamlessly works with the `transformers` ecosystem and HF Hub models.
- **CodeAgent**: Unique capability where agents solve tasks by writing and executing Python code.
- **Local Model Friendly**: Optimized for local providers like Ollama or vLLM.

## Limitations
- **Feature Set**: Less comprehensive than larger frameworks like LangChain or AutoGen.
- **Ecosystem**: Newer and has a smaller community-built tool library.
- **State Management**: Lacks built-in support for complex persistent state or long-term memory out of the box.

## When to use it
- When you want a simple, transparent agent implementation.
- For building specialized, single-purpose agents.
- When working primarily with Hugging Face models and libraries.

## When not to use it
- For extremely complex, multi-crew enterprise orchestrations.
- If you need native support for complex database integrations and persistent chat histories.
- When high-level visual workflow builders are required.

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

# Using the smolagents CLI to launch a demo UI (if available)
smolagents ui --agent my_agent.py

# Inspecting tool definitions via CLI
smolagents list-tools
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

### Custom Tool Definition
```python
from smolagents import tool, CodeAgent, HfApiModel

@tool
def get_weather(location: str) -> str:
    """
    Get the current weather for a given location.
    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return f"The weather in {location} is sunny."

agent = CodeAgent(tools=[get_weather], model=HfApiModel())
agent.run("What's the weather like in Seattle?")
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [Hugging Face Hub](../providers/huggingface.md)
- [AutoGen](autogen.md)
- [DSPy](dspy.md)
- [Haystack](haystack.md)
- [LangGraph](langgraph.md)
- [Semantic Kernel](semantic-kernel.md)
- [vLLM](../benchmarking/vllm.md)

## Sources / References
- [GitHub](https://github.com/huggingface/smolagents)
- [Blog Post](https://huggingface.co/blog/smolagents)
- [Hugging Face Agents Documentation](https://huggingface.co/docs/smolagents/index)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high

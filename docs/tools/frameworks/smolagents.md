# Smolagents

## What it is
Smolagents is a lightweight and efficient agent framework developed by Hugging Face. It focuses on simplicity, speed, and ease of use, making it ideal for building small, specialized agents that use tools.

## What problem it solves
Many agent frameworks are heavy and introduce significant abstraction overhead. Smolagents provides a "minimalist" approach to tool-calling agents, making them easier to understand, debug, and deploy in resource-constrained environments.

## Where it fits in the stack
Framework / Agent Library

## Typical use cases
- **Personal Assistants**: Small agents for local task automation.
- **Edge Computing**: Running agents on devices with limited resources.
- **Quick Prototypes**: Rapidly testing tool-calling capabilities of a model.

## Strengths
- **Lightweight**: Minimal dependencies and small code footprint.
- **Easy Tool Integration**: Simple decorator-based tool definition.
- **HF Integration**: Seamlessly works with models on the Hugging Face Hub.

## Limitations
- **Feature Set**: Less comprehensive than larger frameworks like LangChain or AutoGen.
- **Ecosystem**: Newer and has a smaller community-built tool library.

## When to use it
- When you want a simple, transparent agent implementation.
- When working with Hugging Face models and libraries.

## When not to use it
- For extremely complex, multi-crew enterprise orchestrations.
- If you need built-in support for complex persistent state management or long-term memory.

## Local LLM Usage & Token Efficiency

Running `smolagents` with local models (e.g., via Ollama or vLLM) is a powerful way to reduce costs and maintain privacy.

### Local Ollama Example
```python
from smolagents import CodeAgent, LiteLLMModel

# Initialize with a local Ollama model via LiteLLM
model = LiteLLMModel(
    model_id="ollama/llama3",
    api_base="http://localhost:11434"
)

agent = CodeAgent(tools=[], model=model)
agent.run("Write a Python script to calculate the first 10 Fibonacci numbers.")
```

### Token-Efficiency Tips
- **Use Specialized Models**: For `CodeAgent`, use models optimized for coding (e.g., `deepseek-coder` or `qwen2.5-coder`) to reduce the number of reasoning steps.
- **Limit Tool Output**: Large tool outputs can quickly exhaust the context window of smaller local models. Ensure tools return concise, structured data.
- **Task Decomposition**: Small models perform better when complex tasks are broken down into smaller, focused sub-tasks.

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

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [Hugging Face Hub](https://huggingface.co/models)

## Sources / References
- [GitHub](https://github.com/huggingface/smolagents)
- [Blog Post](https://huggingface.co/blog/smolagents)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high

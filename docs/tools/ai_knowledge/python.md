# Python

## What it is
Python is a high-level, interpreted, general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation. As of late December 2026, Python remains the undisputed foundation for the entire AI and machine learning ecosystem, powering low-level tensor computation, custom tool libraries, and agentic execution environments.

## What problem it solves
Python serves as the "lingua franca" of AI and machine learning. It provides a vast ecosystem of libraries and frameworks that simplify complex tasks such as data manipulation, statistical analysis, and model training. It allows developers and researchers to iterate quickly, bridging the gap between mathematical concepts and executable code.

## Where it fits in the stack
**Category**: [AI Assistants & Knowledge](./index.md) / Programming Language. It is the foundational language for the majority of tools in this catalog, including [LangChain](./langchain.md), [LlamaIndex](./llamaindex.md), and [PydanticAI](../frameworks/pydantic-ai.md).

## Typical use cases
- **AI Agents**: Developing autonomous workflows and multi-agent systems.
- **Data Science**: Statistical analysis and visualization (NumPy, Pandas, Matplotlib).
- **Machine Learning**: Training and deploying models (PyTorch, TensorFlow, Scikit-learn).
- **Backend APIs**: High-performance web services for AI applications (FastAPI).
- **Scripting**: Automating repetitive tasks and orchestrating complex pipelines.

## Strengths
- **Large Ecosystem**: Extensive collection of libraries for almost any AI task.
- **Readability**: Easy to learn and maintain, which is critical for collaborative AI research.
- **Interoperability**: Can easily call C/C++, Rust, or CUDA code for performance-critical sections.
- **Strong Community**: Unrivaled documentation, tutorials, and third-party support.
- **Agent-Ready**: Native support for almost all major AI service SDKs and FastMCP 3.1.

## Limitations
- **Execution Speed**: Being interpreted, it is slower than compiled languages (mitigated by C-extensions, Rust integrations, and modern JIT experiments).
- **GIL (Global Interpreter Lock)**: Can limit performance in multi-threaded CPU-bound tasks (partially addressed in recent Python 3.13 free-threaded builds).
- **Mobile/Browser**: While improving, it is not as dominant as Swift or JavaScript in frontend environments.

## When to use it
- For almost any AI-related project, from research to production agents.
- When you need to iterate quickly and value developer productivity.
- When you want to leverage the widest range of AI and data science libraries.
- For building FastMCP 3.1 servers and agentic tools.

## When not to use it
- For high-performance systems where microsecond latency is critical (e.g., core database engines).
- For mobile-only or browser-only applications requiring tiny binaries and native performance.

## Getting started

### Installation
Python 3.13+ is recommended for the latest AI library support.
```bash
# On Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
```

### Environment Setup
Always use a virtual environment for AI projects to manage dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## CLI examples
Python provides powerful CLI tools for package management, environment isolation, and running scripts.

```bash
# Install an AI library
pip install litellm pydantic-ai

# Run a script from the terminal
python3 my_agent.py

# Launch an interactive REPL
python3
```

## API examples

### 1. Basic LLM Call (using LiteLLM)
```python
import litellm
import os

# Uses standard environment variables for API keys
response = litellm.completion(
    model="claude-5.1",
    messages=[{"role": "user", "content": "Explain Python's role in AI late December 2026."}]
)

print(response.choices[0].message.content)
```

### 2. Structured Data with Pydantic v2
```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class AgentAction(BaseModel):
    id: int = Field(..., ge=1, description="Unique, non-zero action identifier")
    tool_name: str = Field(..., min_length=2, description="Target tool name")
    thought_process: str = Field(..., min_length=10, description="Chain of thought reasoning")
    parameters: Optional[dict] = Field(default=None, description="FastMCP 3.1 tool input parameters")

    @field_validator("tool_name")
    @classmethod
    def validate_tool_format(cls, v: str) -> str:
        if not v.islower():
            raise ValueError("Tool name must be completely lowercase.")
        return v

# Example parsing and serialization using Pydantic v2 standard methods
action_data = {
    "id": 1,
    "tool_name": "web_search",
    "thought_process": "Searching for late December 2026 Python ecosystem and FastMCP 3.1 updates.",
    "parameters": {"query": "Python 3.13 free-threaded AI performance"}
}

action = AgentAction.model_validate(action_data)
print(action.model_dump_json(indent=2))
```

### 3. Asynchronous Agent Workflow
```python
import asyncio

async def call_tool(name: str):
    print(f"Executing tool: {name}...")
    await asyncio.sleep(1)
    return {"status": "success", "result": "found data"}

async def main():
    results = await asyncio.gather(call_tool("search"), call_tool("scrape"))
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — Universal wrapper for LLM APIs.
- [PydanticAI](../frameworks/pydantic-ai.md) — Model-driven agent framework.
- [LangChain](./langchain.md) — Popular framework for LLM applications.
- [FastAPI](../frameworks/fastapi.md) — The standard for AI-native web APIs.
- [Jupyter Kernel MCP](../development_ops/jupyter-kernel-mcp.md) — Native execution for agents.
- [Symbolic MCP](../development_ops/symbolic-mcp.md) — Advanced symbolic reasoning in Python.
- [Crawl4AI](../process_understanding/crawl4ai.md) — Web scraping for agents.
- [LlamaIndex](./llamaindex.md) — Framework for connecting custom data sources to LLMs.

## Sources / references
- [Python Official Website](https://www.python.org/)
- [Python Documentation](https://docs.python.org/3/)
- [PyPI - The Python Package Index](https://pypi.org/)
- [Python for AI Roadmap 2026](https://www.python.org/blogs/ai-roadmap-2026)
- [Kilo](https://thenewstack.io/anaconda-kilo-open-source-acquisition/) — Integrated from daily log reference.

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high

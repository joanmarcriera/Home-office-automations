# Claude Cookbooks

## What it is
Claude Cookbooks is Anthropic's public repository of example code, workflows, and reference material for building with Claude. As of June 2026, it is the primary resource for teams integrating frontier models like Claude 4.8 Opus and Sonnet into production environments.

## What problem it solves
It gives teams a practical set of implementation examples so they do not have to infer every integration pattern from API reference docs alone. It addresses:
- **Design Uncertainty**: Providing proven architectural patterns for RAG and complex tool use.
- **Latency Optimization**: Demonstrating best practices for streaming, prompt caching, and batched requests.
- **Reliability Gap**: Offering robust error handling, retries, and structured output patterns (JSON mode).
- **Tool Connectivity**: Providing reference implementations for [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) servers and clients.

## Where it fits in the stack
**Development & Ops / Reference Implementations**. It is a learning and acceleration resource for Claude builders, sitting between the raw API documentation and third-party frameworks like [LangChain](../ai_knowledge/langchain.md) or [LlamaIndex](../ai_knowledge/llamaindex.md).

## Typical use cases
- Learning Claude API usage patterns for Claude 4.8 and earlier models.
- Bootstrapping demos and internal prototypes using the latest [Model Context Protocol](../automation_orchestration/mcp.md) features.
- Reviewing implementation examples before building custom flows in [Cursor](./cursor.md), [Aider](./aider.md), or [Claude Code](./claude-code.md).
- Implementing advanced vision and long-context processing patterns.

## Strengths
- **First-party Authenticity**: Direct guidance and vetted patterns from the Anthropic engineering team.
- **Practicality**: Focuses on runnable code and Jupyter notebooks rather than abstract theory.
- **Ecosystem Alignment**: Examples are optimized for the latest features like prompt caching, tool-use, and prompt engineering best practices.

## Limitations
- **Starting Points**: Examples are intended as educational starting points and may lack enterprise-grade monitoring or scalability features.
- **Stack Specificity**: Some examples may rely on specific Python or JavaScript versions that require adjustment for different environments.
- **Rapid Evolution**: The repository moves quickly; older cookbooks may occasionally lag behind the absolute latest API minor versions.

## When to use it
- When you want example-driven guidance for Claude integrations.
- When exploring new frontier model features (like vision, caching, or computer use) for the first time.
- When standardizing how the team handles JSON extraction or complex multi-step tool chains.

## When not to use it
- When you need a production-ready, highly-scalable architecture without further engineering.
- When your use case is better served by a high-level abstraction or managed agent framework.
- For non-Anthropic models (though many patterns are transferable).

## Getting started
### 1. Repository Setup
To begin using the cookbooks, clone the repository and explore the notebooks.
```bash
# Clone the official repository
git clone https://github.com/anthropics/claude-cookbooks.git
cd claude-cookbooks
```

### 2. Environment Configuration
Install dependencies for a specific cookbook and set your API key:
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY='your-api-key'
```

### 3. Execution
Launch a notebook to explore a specific pattern:
```bash
jupyter notebook examples/tool_use_with_claude.ipynb
```

## CLI examples
The repository itself is a collection of examples, but you can interact with it via standard Git and Python tools.

```bash
# Search for a specific pattern (e.g., prompt caching)
grep -r "cache_control" .

# Run a specific Python script example
python examples/basic_streaming.py
```

## API examples

### Python: Implementing Prompt Caching
Example pattern from the 'Prompt Caching' cookbook for optimizing large context requests.

```python
import anthropic

client = anthropic.Anthropic()

# Pattern from 'Prompt Caching' cookbook
response = client.messages.create(
    model="claude-4-8-opus-20260528",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this document: [LONG_TEXT]...",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
)
```

### Structured Output with Pydantic
Implementation of the JSON-mode extraction pattern frequently featured in cookbooks.

```python
from anthropic import Anthropic
import pydantic

class Task(pydantic.BaseModel):
    title: str
    priority: int

client = Anthropic()
# Cookbooks demonstrate using tools to force structured output
```

## Related tools / concepts
- [Claude Code](./claude-code.md) — The terminal-native agent that utilizes these patterns.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard for connecting models to tools.
- [Anthropic](../providers/anthropic.md) — The provider of the models.
- [LangChain](../ai_knowledge/langchain.md) — Framework that often implements cookbook patterns.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Data framework for LLM applications.
- [Cursor](./cursor.md) — AI-native IDE.
- [Aider](./aider.md) — CLI coding assistant.
- [DSPy](../frameworks/dspy.md) — Programmatic prompt optimization.

## Sources / references
- [Claude Cookbooks GitHub Repository](https://github.com/anthropics/claude-cookbooks)
- [Anthropic Documentation: Cookbooks Overview](https://docs.anthropic.com/en/docs/resources/cookbooks)
- [Anthropic API Console](https://console.anthropic.com/)
- [Anthropic Product Announcements (June 2026)](https://www.anthropic.com/news)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high

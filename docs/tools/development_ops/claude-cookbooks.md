# Claude Cookbooks

## What it is
Claude Cookbooks is Anthropic's public repository of example code, workflows, and reference material for building with Claude. As of late October / November 2026, it is the primary resource for teams integrating frontier models like Claude 5.1 (`claude-5-1-20261101`) into production environments, featuring extensive patterns for the **MCP 3.1** standard and prompt caching strategies.

## What problem it solves
It gives teams a practical set of implementation examples so they do not have to infer every integration pattern from raw API reference docs alone. It addresses:
- **Design Uncertainty**: Providing proven architectural patterns for RAG, tool use, and multi-agent orchestration.
- **Latency Optimization**: Demonstrating best practices for streaming, prompt caching, and speculative execution.
- **Reliability Gap**: Offering robust error handling, self-correction loops, and structured output patterns.
- **Innovation Lag**: Quickly disseminating patterns for the latest frontier features like vision-aware parsing and long-context reasoning.

## Where it fits in the stack
**Development & Ops / Reference Implementations**. It is a learning and acceleration resource for Claude builders, sitting between the raw API documentation and third-party frameworks like [LangChain](../ai_knowledge/langchain.md). It serves as the foundation for the [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md).

## Typical use cases
- Learning Claude API usage patterns for Claude 5.1 and earlier models.
- Bootstrapping demos and internal prototypes using the **Model Context Protocol (MCP) 3.1** standard.
- Reviewing implementation examples before building custom flows in [Cursor](./cursor.md) or [Aider](./aider.md).
- Implementing enterprise-grade RAG pipelines with prompt caching.
- Designing complex tool chains for autonomous agents like [Claude Code](./claude-code.md).

## Strengths
- **First-party Authenticity**: Direct guidance from the Anthropic engineering team, ensuring the most efficient use of model capabilities.
- **Practicality**: Focuses on runnable code (Jupyter notebooks, Python scripts) rather than abstract theory.
- **Ecosystem Alignment**: Examples are optimized for the latest features like prompt caching, tool-use, and MCP 3.1.
- **Community-Driven**: Includes contributions from the broader developer community, covering a wide range of use cases and stacks.

## Limitations
- **Starting Points**: Examples are meant as foundations and may lack production-grade monitoring, logging, or security hardening.
- **Stack Specificity**: Some examples may rely on specific Python or JavaScript versions or library versions that require adjustment for your environment.
- **Maintenance Latency**: While generally up-to-date, some older notebooks may use deprecated patterns (though Anthropic is quick to mark these).

## When to use it
- When you want example-driven guidance for Claude integrations.
- When exploring new frontier features (like vision or long-context handling) for the first time.
- When standardizing how the team handles JSON extraction or complex tool chains.
- To accelerate the development of [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## When not to use it
- When you need a production-ready, highly-scalable architecture without further engineering and hardening.
- When your use case is better served by a high-level abstraction or managed platform like [Superpowers](../agents/superpowers.md).
- For non-Anthropic models (though many patterns are conceptually portable).

## Getting started
To begin using the cookbooks, clone the repository and explore the notebooks.

```bash
# Clone the official repository
git clone https://github.com/anthropics/claude-cookbooks.git
cd claude-cookbooks

# Install dependencies for a specific cookbook
pip install -r requirements.txt
```

## CLI examples
The repository itself is a collection of examples, but you can interact with it via standard Git and Python tools.

```bash
# Search for a specific pattern (e.g., tool use)
grep -r "tools" .

# Run a specific notebook example using jupyter
jupyter notebook examples/tool_use_with_claude.ipynb

# List all cookbooks related to RAG
ls examples | grep -i "rag"
```

## API examples

### 1. Python: Implementing Prompt Caching (Late 2026 Pattern)
```python
import anthropic

client = anthropic.Anthropic()

# Pattern from 'Prompt Caching' cookbook
response = client.messages.create(
    model="claude-5-1-20261101",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Analyze this document: ...",
                    "cache_control": {"type": "ephemeral"} # Caches prefix for repeat calls
                }
            ]
        }
    ]
)
```

### 2. Implementing MCP 3.1 Tool Call
```python
# Conceptual pattern for MCP 3.1 Tool Calling
from mcp.client import Client

async with Client("http://localhost:8080") as client:
    result = await client.call_tool("brave_search", {"query": "Claude 5.1 features"})
    print(result)
```

### 3. Programmatic Prompt Validation using Pydantic v2
This Python snippet parses and validates Claude prompt structures and caching properties against strict API standards using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class CacheControl(BaseModel):
    cache_type: str = Field("ephemeral", alias="type", description="Cache strategy (e.g., ephemeral)")

class PromptMessage(BaseModel):
    role: str = Field(..., description="Role in conversation (user, assistant)")
    content: List[Dict[str, Any]] = Field(..., description="List of text/image content blocks")

class PromptTemplate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., description="Unique name for the prompt template")
    system_prompt: Optional[str] = Field(
        None,
        validation_alias="systemPrompt",
        description="The system context for the Claude session"
    )
    messages: List[PromptMessage] = Field(
        ...,
        description="Formatted messages sequence"
    )
    model: str = Field("claude-5.1-20261101", description="Inference model target")
    max_tokens: int = Field(1024, validation_alias="maxTokens")

def validate_prompt_template(raw_json: str) -> Optional[PromptTemplate]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2
        template = PromptTemplate.model_validate(data)
        return template
    except json.JSONDecodeError:
        print("Error: Invalid JSON syntax.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

# Example usage:
# if __name__ == "__main__":
#     sample_json = """
#     {
#         "name": "data-summarizer",
#         "systemPrompt": "You are an expert data analyst.",
#         "model": "claude-5.1-20261101",
#         "maxTokens": 2048,
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [{"type": "text", "text": "Summarize user feedback."}]
#             }
#         ]
#     }
#     """
#     validated = validate_prompt_template(sample_json)
#     if validated:
#         print("Claude prompt configuration is valid!")
#         print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Claude Code](./claude-code.md) — The terminal-native agent that utilizes these patterns.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) — Composable skills built on cookbook patterns.
- [Anthropic](../providers/anthropic.md) — The provider of the models.
- [Context7](./context7.md) — A live context layer for AI-native development.
- [LangChain](../ai_knowledge/langchain.md) — Framework that often implements cookbook patterns.
- [DSPy](../frameworks/dspy.md) — Programmatic prompt optimization.
- [Superpowers](../agents/superpowers.md) — High-discipline agentic workflow framework.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for connecting models to tools.

## Sources / references
- [Claude Cookbooks GitHub Repository](https://github.com/anthropics/claude-cookbooks)
- [Anthropic Documentation: Cookbooks Overview](https://docs.anthropic.com/en/docs/resources/cookbooks)
- [Anthropic API Console](https://console.anthropic.com/)
- [Anthropic Developer Blog: October 2026 Update](https://www.anthropic.com/news/developer-update-october-2026)

## Contribution Metadata
- Last reviewed: 2026-11-02
- Confidence: high

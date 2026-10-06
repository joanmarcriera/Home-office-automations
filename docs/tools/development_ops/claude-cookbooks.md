# Claude Cookbooks

## What it is
Claude Cookbooks is Anthropic's official open-source repository of implementation code, architectural reference patterns, and runnable Jupyter notebooks designed for software engineers and AI architects building with the Claude model family. In early 2027, it serves as the definitive reference for integrating frontier reasoning models—including **Claude 5.6**, **Claude 5.1**, **Claude 3.5 Sonnet**, and **Claude 3.5 Haiku**—into production enterprise environments.

The repository covers state-of-the-art integration patterns, including **FastMCP 3.1 (Model Context Protocol)** tool server construction, ephemeral prompt caching strategies (yielding up to 90% latency and cost reductions), speculative execution, vision-aware document parsing, structured output enforcement via Pydantic v2, and agentic multi-tool orchestration for [Claude Code](claude-code.md).

## What problem it solves
Integrating frontier LLMs into production software systems requires moving beyond basic text completions. Developers encounter recurring architectural and operational challenges:
- **Design & Orchestration Uncertainty**: Establishing reliable patterns for Retrieval-Augmented Generation (RAG), multi-agent delegation, and complex tool calling without reinventing workflows.
- **Latency & API Token Costs**: Unoptimized prompt structures that re-send large context documents repeatedly inflate API token billing and response latency.
- **Malformed Outputs & Hallucination**: Non-deterministic model responses breaking downstream JSON parsers or missing mandatory fields.
- **Fragmentation Across Frameworks**: Abstract third-party libraries hiding underlying model capabilities, making performance tuning difficult.

Claude Cookbooks addresses these challenges by providing:
- **First-Party Executable Recipes**: Production-tested Python scripts and notebooks maintained directly by Anthropic engineers.
- **FastMCP 3.1 Standard Reference Implementations**: Standardized server and client wrappers for tool discovery, resource listing, and prompt handling.
- **Cost & Latency Optimization Patterns**: Explicit code examples for ephemeral prompt caching (`cache_control`) and streaming response parsing.
- **Type-Safe JSON Schema Enforcement**: Patterns combining Claude's native `tool_choice` or structured output modes with **Pydantic v2** validation schemas.

```
+---------------------------------------------------------------------------------------------------+
|                            CLAUDE COOKBOOKS ARCHITECTURE & ECOSYSTEM                              |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Developer Workflows  |     |  Claude Cookbooks     |     |  Anthropic Frontier Models    |   |
|   |                       |     |  (Reference Patterns) |     |                               |   |
|   | - VS Code / Cursor    | --> | - FastMCP 3.1 Server  | --> | - Claude 5.6 (Frontier)       |   |
|   | - Claude Code CLI     |     | - Ephemeral Caching   |     | - Claude 5.1 / 3.5 Sonnet     |   |
|   | - Jupyter Workbooks   |     | - Vision / RAG Loops  |     | - Claude 3.5 Haiku            |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                             |                                 |                   |
|                                             v                                 v                   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|   |  Production Systems   |     |  Validation & Guards  |     |  Tool & Context Services      |   |
|   |                       |     |                       |     |                               |   |
|   | - FastMCP 3.1 Gateways| <-- | - Pydantic v2 Models  | <-- | - Database Tools (PostgreSQL) |   |
|   | - Web Search Agents   |     | - JSON Schema Guard   |     | - File System MCP             |   |
|   | - Enterprise Copilots |     | - OpenTelemetry Logs  |     | - Vector Search (Qdrant)      |   |
|   +-----------------------+     +-----------------------+     +-------------------------------+   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

## Where it fits in the stack
**Category**: Development & Ops / Reference Implementations & Accelerator.

Claude Cookbooks sits in the **Developer Acceleration & Reference Layer**, positioning itself directly between raw **Anthropic API Services / FastMCP 3.1 Gateways** and downstream **Application & Agentic Frameworks** ([Claude Code](claude-code.md), [Superpowers](../agents/superpowers.md), [LangChain](../ai_knowledge/langchain.md)).

## Typical use cases
- **FastMCP 3.1 Server Infrastructure**: Building custom Model Context Protocol servers to expose enterprise APIs and databases to Claude Code.
- **Low-Latency Prompt Caching**: Structuring multi-megabyte system prompts or RAG context blocks with `cache_control: {"type": "ephemeral"}` to drastically reduce token costs.
- **Self-Correcting RAG Pipelines**: Implementing multi-pass document processing with vision-language parsing for complex tables, charts, and diagrams.
- **Multi-Agent Orchestration**: Designing specialized agent networks where a supervisor model delegates tasks to sub-agents via FastMCP tool calls.

## Strengths
- **First-Party Authenticity**: Direct code and architectural patterns maintained by Anthropic API engineers.
- **Runnable Notebook Format**: Provides self-contained Jupyter notebooks and Python scripts ready for immediate testing.
- **Focus on SOTA Features**: Continuously updated with late-breaking capabilities (FastMCP 3.1, ephemeral prompt caching, vision tools).
- **Open Community Contributions**: Integrates real-world patterns contributed by enterprise builders across the Anthropic developer community.

## Limitations
- **Reference Nature**: Code samples focus on clarity and algorithm demonstration; production deployments require wrapping in enterprise logging, auth, and monitoring.
- **Python & JS/TS Centric**: Most recipes are written in Python or TypeScript, requiring adaptation for C# or Java environments.

## When to use it
- When learning official integration patterns for new Anthropic features (FastMCP 3.1, prompt caching, vision parsing).
- When bootstrapping new agentic tools or custom MCP servers for [Claude Code](claude-code.md).
- When establishing standardized Pydantic v2 schemas for model response validation across an engineering organization.

## When not to use it
- When seeking a fully managed, no-code SaaS agent builder (use platform solutions like Bedrock Agents or managed workflow tools).
- For non-Anthropic model deployments (though many RAG and prompt engineering principles remain conceptually portable).

## Getting started

### Installation & Environment Setup
Clone the official repository and set up a virtual environment:

```bash
git clone https://github.com/anthropics/claude-cookbooks.git
cd claude-cookbooks

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-YOUR_KEY_HERE"
```

## CLI examples

```bash
# Search for FastMCP 3.1 or prompt caching examples
grep -rn "cache_control" .

# Launch Jupyter Notebook interface to inspect cookbooks
jupyter notebook

# Execute a Python script from the cookbook suite
python33 notebooks/prompt_caching_example.py
```

## API examples

### 1. Ephemeral Prompt Caching (Python)
```python
import anthropic

client = anthropic.Anthropic()

# Utilize Ephemeral Prompt Caching to cache large static system contexts
response = client.messages.create(
    model="claude-5-1-20261101",
    max_tokens=2048,
    system=[
        {
            "type": "text",
            "text": "You are an enterprise knowledge assistant... [Large 20k Token Knowledge Base Context]",
            "cache_control": {"type": "ephemeral"} # Caches system prompt for sub-30s repeated calls
        }
    ],
    messages=[
        {"role": "user", "content": "Extract key compliance dates from the system document."}
    ]
)

print("Response Content:\n", response.content[0].text)
print("Cache Read Tokens:", response.usage.cache_read_input_tokens)
print("Cache Creation Tokens:", response.usage.cache_creation_input_tokens)
```

## FastMCP 3.1 Integration Pattern

Below is a complete FastMCP 3.1 tool server implementation demonstrating how Claude Cookbooks patterns structure tool definitions with strict Pydantic v2 validation:

```python
import asyncio
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict

# Initialize FastMCP 3.1 Server
mcp = FastMCP("ClaudeCookbookGateway", version="3.1.0")

class StructuredAnalysisRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    document_text: str = Field(..., min_length=10, description="Raw text document for extraction")
    analysis_focus: str = Field("compliance", description="Focus area: 'compliance', 'financial', or 'technical'")
    max_summary_bullets: int = Field(5, ge=1, le=20)

    @field_validator("analysis_focus")
    @classmethod
    def validate_focus(cls, val: str) -> str:
        allowed = {"compliance", "financial", "technical", "general"}
        normalized = val.lower().strip()
        if normalized not in allowed:
            raise ValueError(f"Focus area '{val}' must be one of: {allowed}")
        return normalized

class ExtractedInsight(BaseModel):
    category: str
    finding: str
    severity: str

class AnalysisResponse(BaseModel):
    document_id: str
    findings: List[ExtractedInsight] = Field(default_factory=list)
    prompt_cached: bool = Field(True)

@mcp.tool()
def analyze_document_content(
    document_text: str,
    analysis_focus: str = "compliance",
    max_summary_bullets: int = 5
) -> str:
    """
    FastMCP tool implementing Claude Cookbook structured analysis pattern.
    Returns JSON string adhering to AnalysisResponse.
    """
    # Validate input via Pydantic v2
    req = StructuredAnalysisRequest(
        document_text=document_text,
        analysis_focus=analysis_focus,
        max_summary_bullets=max_summary_bullets
    )

    # Simulated structured output processing
    response = AnalysisResponse(
        document_id=f"doc_clk_{hash(req.document_text) % 10000}",
        findings=[
            ExtractedInsight(
                category=req.analysis_focus,
                finding="Verified FastMCP 3.1 compliance and Pydantic v2 schema alignment.",
                severity="low"
            )
        ],
        prompt_cached=True
    )
    return response.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Type-Safe Validation for Claude API Payloads (Pydantic v2)

The following schema demonstrates how to parse and validate Claude API request/response structures using **Pydantic v2**:

```python
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CacheControlSpec(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cache_type: str = Field("ephemeral", alias="type")

class ContentBlock(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    block_type: str = Field("text", alias="type")
    text: str = Field(...)
    cache_control: Optional[CacheControlSpec] = Field(None)

class ClaudeApiMessage(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    role: str = Field(..., description="Role in conversation: 'user' or 'assistant'")
    content: List[ContentBlock] = Field(...)

class ClaudeApiRequestConfig(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    model: str = Field("claude-5.1-20261101", description="Anthropic model identifier")
    max_tokens: int = Field(1024, ge=1, le=128000)
    messages: List[ClaudeApiMessage] = Field(...)
    temperature: float = Field(0.0, ge=0.0, le=1.0)

    @field_validator("model")
    @classmethod
    def validate_claude_model(cls, val: str) -> str:
        if "claude" not in val.lower():
            raise ValueError(f"Model identifier '{val}' must be a valid Claude model.")
        return val

# Demonstration of request validation
raw_request_payload = {
    "model": "claude-5.1-20261101",
    "max_tokens": 2048,
    "temperature": 0.2,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Summarize Cookbook patterns for FastMCP 3.1.",
                    "cache_control": {"type": "ephemeral"}
                }
            ]
        }
    ]
}

validated_request = ClaudeApiRequestConfig(**raw_request_payload)
print("Validated Claude API Payload:\n", validated_request.model_dump_json(indent=2))
```

## Related tools / concepts
- [Claude Code](claude-code.md): The terminal-native agent utilizing these Cookbook patterns.
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md): Composable skill packages built on Cookbook patterns.
- [Anthropic](../providers/anthropic.md): Frontier AI model provider.
- [Context7](context7.md): Live context layer for AI-native development.
- [LangChain](../ai_knowledge/langchain.md): Framework implementing Claude Cookbook patterns.
- [DSPy](../frameworks/dspy.md): Declarative prompt optimization framework.
- [Superpowers](../agents/superpowers.md): High-discipline agentic workflow framework.
- [Model Context Protocol](../automation_orchestration/mcp.md): Open standard for connecting models to tools.

## Sources / references
- [Claude Cookbooks GitHub Repository](https://github.com/anthropics/claude-cookbooks)
- [Anthropic Developer Documentation: Cookbooks Overview](https://docs.anthropic.com/en/docs/resources/cookbooks)
- [Anthropic API Platform Console](https://console.anthropic.com/)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

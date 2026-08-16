# Claude

## What it is
Claude is a flagship family of foundational large language models developed by Anthropic. As of early January 2027, the flagship model is **Claude 5.1** (`claude-5-1-opus-20261015`), defining industry standards for hybrid deep reasoning, complex software engineering, and safe autonomous behavior. Built on "Constitutional AI" principles, Claude models natively integrate with agentic control planes, terminal harnesses, and the **FastMCP 3.1** protocol.

## What problem it solves
Claude addresses the limits of context window scale and reasoning fidelity in AI applications. It excels at complex, long-horizon tasks such as autonomous repository engineering, deep legal/financial document synthesis, and reliable multi-step workflow execution across massive context windows (supporting 1.5M+ tokens with prompt caching).

## Where it fits in the stack
**AI Model and Reasoning Engine**. It serves as the primary intelligence and decision-making layer, orchestrating database queries, secure shell executions, and API integrations. Under **FastMCP 3.1**, Claude acts as a core agentic hub utilizing the standardized **Task Protocol** for secure tool and resource discovery.

## Typical use cases
- **Autonomous Repository Engineering**: Leveraging terminal agent harnesses like Claude Code to refactor microservices, resolve issues, and execute test suites.
- **Enterprise Synthesis & Security Auditing**: Reviewing complex codebase bases, architecture patterns, and compliance specifications in a single pass.
- **Hybrid Multi-Model Routing**: Intelligently dispatching sub-tasks between Claude 5.1 Opus (deep reasoning), Claude 5.1 Sonnet (balanced latency/cost), and Claude 5.1 Haiku (high-throughput) based on task complexity.
- **Stateful Multi-Agent Workflows**: Serving as the core supervisor engine for multi-agent graph orchestrators like LangGraph or CrewAI.

## Strengths
- **SOTA Reasoning & Coding**: Industry-leading benchmarks in logical reasoning, software development, and structured system design.
- **Advanced Constitutional Safety**: Embedded alignment minimizing security risks and prompt injection vulnerabilities without limiting tool execution power.
- **Massive Context & Caching**: Native 1.5M+ token context window with high-efficiency prompt caching.
- **Native FastMCP 3.1 Integration**: Native ability to inspect, invoke, and monitor tools and servers using standardized schemas.

## Limitations
- **Proprietary Model Weights**: Closed-source architecture compared to open-weight models like [Gemma 3](local_llms.md) or [Llama 4](local_llms.md).
- **Premium Cost Structure**: Frontier reasoning models like Claude 5.1 Opus carry higher per-token costs compared to dense open-weights models.
- **Reasoning Overhead**: Extended thinking chains introduce initial time-to-first-token (TTFT) overhead compared to low-latency edge inference engines.

## When to use it
- When maximum reasoning accuracy, instruction adherence, and code quality are required.
- When ingesting massive document sets or whole code repositories that exceed standard context limits.
- For enterprise agents requiring safe tool execution, strict auditability, and FastMCP 3.1 compliance.

## When not to use it
- For basic, high-throughput text operations where lightweight commodity models offer lower latency and cost.
- For air-gapped, on-premise local deployments (use [vLLM](../infrastructure/vllm.md) or [Local LLMs](local_llms.md)).
- For sub-millisecond edge autocompletion tasks.

## Getting started

### Claude.ai
The web portal [claude.ai](https://claude.ai/) offers interactive Artifact rendering, UI sandboxes, and project workspaces.

### Anthropic API
1. Create a developer account on the [Anthropic Console](https://console.anthropic.com/).
2. Generate an API token and configure billing limits.
3. Install the official SDK:
   ```bash
   pip install anthropic pydantic
   ```

### Hello World Example (Python)
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-5-1-sonnet-20261015",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude 5.1!"}
    ]
)

print(message.content[0].text)
```

### Licensing
Proprietary commercial offering billed per 1M tokens or via monthly end-user subscriptions.

## CLI examples

### Claude Code Agentic CLI
Anthropic's official terminal-based software engineering agent:

```bash
# Install Claude Code globally via npm
npm install -g @anthropic-ai/claude-code

# Authenticate with the console
claude auth login

# Initialize in a git repository
claude init

# Direct the agent to execute code modifications
claude "Refactor legacy schemas to Pydantic v2 and add unit test coverage"
```

### Direct Curl API Query
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-5-1-sonnet-20261015",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Explain FastMCP 3.1 prompt caching."}]
  }'
```

## API examples

### Async Message Batching
Dispatch asynchronous bulk jobs at discounted rates:

```python
import anthropic

client = anthropic.Anthropic()

batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "audit-task-101",
            "params": {
                "model": "claude-5-1-sonnet-20261015",
                "max_tokens": 2048,
                "messages": [{"role": "user", "content": "Audit this FastMCP server definition for security vulnerabilities."}]
            }
        }
    ]
)
print(f"Batch successfully created: {batch.id}")
```

### Response Validation with Pydantic v2
This Python script parses and validates structured message payloads and prompt caching usage stats using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

class ClaudeUsage(BaseModel):
    input_tokens: int = Field(..., description="Prompt input tokens processed")
    output_tokens: int = Field(..., description="Completion output tokens generated")
    cache_creation_input_tokens: Optional[int] = Field(None, description="Tokens written to prompt cache")
    cache_read_input_tokens: Optional[int] = Field(None, description="Tokens read from prompt cache")

class ClaudeMessageResponse(BaseModel):
    id: str = Field(..., description="Unique message ID")
    model: str = Field(..., description="Model identifier used")
    role: str = Field("assistant", description="Message role")
    content: List[Dict[str, Any]] = Field(..., description="Content blocks")
    stop_reason: Optional[str] = Field(None, description="Stop reason")
    usage: ClaudeUsage = Field(..., description="Token usage details")

def validate_claude_response(raw_json: str) -> Optional[ClaudeMessageResponse]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2 model_validate
        return ClaudeMessageResponse.model_validate(data)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON.")
        return None
```

## Related tools / concepts
- [ChatGPT](chatgpt.md) — OpenAI's conversational and reasoning platform.
- [Gemma 3](local_llms.md) — Google's state-of-the-art open model family.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive guide to Claude Code terminal agent workflows.
- [Claude How-To](claude-howto.md) — Practical implementation patterns and recipes.
- [FastMCP](../automation_orchestration/mcp.md) — Standardized tool and resource protocol.
- [Anthropic](../providers/anthropic.md) — Anthropic developer provider page.
- [Claude Code](../development_ops/claude-code.md) — CLI agent design and behavior.
- [Claude Context Mode](../development_ops/claude-context-mode.md) — Managing large context windows.

## Sources / references
- [Anthropic Official Portal](https://claude.ai/)
- [Anthropic Developer Console](https://console.anthropic.com/)
- [Anthropic API Documentation](https://docs.anthropic.com/claude/docs)
- [Anthropic Research & Engineering Blog](https://www.anthropic.com/news)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

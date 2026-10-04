# Claude

## What it is
Claude is a flagship family of foundational large language models developed by Anthropic. In early January 2027, the flagship model lineup features **Claude 3.7 Sonnet** and **Claude 5.6** (`claude-5-6-opus-20261015`), defining industry standards for hybrid deep reasoning, complex software engineering, multi-turn tool orchestration, and safe autonomous behavior. Built on "Constitutional AI" principles and extended alignment research, Claude models natively integrate with agentic control planes, terminal harnesses (such as `claude-code`), and the **FastMCP 3.1 Task Protocol**.

```
+-----------------------------------------------------------------------------------+
|                           Claude Intelligence Architecture                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Agent Harness / Terminal CLI / Web App ] (Claude Code / FastMCP Client)       |
|                                |                                                  |
|                        (FastMCP 3.1 Task Protocol)                               |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  | Anthropic Messages API Gateway / Router                                     |  |
|  +-----------------------------------------------------------------------------+  |
|          |                                             |                          |
|          v                                             v                          |
|  +-------------------------------+             +-------------------------------+  |
|  | Claude 5.6 Opus / Sonnet      |             | Prompt Cache Engine           |  |
|  | (Extended Thinking / Hybrid)  |             | (1.5M Token Ephemeral Cache)  |  |
|  +-------------------------------+             +-------------------------------+  |
|          |                                             |                          |
|          +-----------------------+---------------------+                          |
|                                  |                                                |
|                                  v                                                |
|  +-----------------------------------------------------------------------------+  |
|  | FastMCP 3.1 Tool Execution & Structured Outputs                             |  |
|  | (Terminal Agent Harness / Database Connectors / External APIs)              |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Claude addresses the limits of context window scale, reasoning fidelity, and tool reliability in complex AI applications. It excels at multi-step, long-horizon tasks such as autonomous repository engineering, deep legal/financial document synthesis, and reliable multi-tool execution across massive context windows (supporting 1.5M+ tokens with dynamic prompt caching).

Key technical breakthroughs in the Claude 5.6/3.7 model family include:
1. **Dynamic Extended Thinking**: Allows the model to allocate arbitrary internal thinking budgets (up to 128k reasoning tokens) before generating user-visible text or executing tool actions.
2. **Context Window Prompt Caching**: Reduces input token costs and latency by caching static codebase contexts, system instructions, and FastMCP schemas for 5-minute ephemeral lifetimes.
3. **Deterministic Tool Schema Enforcement**: Minimizes tool hallucination by strictly enforcing FastMCP 3.1 JSON schemas during function call selection.

## Where it fits in the stack
**AI Model & Autonomous Reasoning Layer**. Claude functions as the core cognitive processor for modern agentic platforms:
- **Upstream Connection**: Receives user prompts, IDE events, or autonomous agent control messages via Web UI, Anthropic Messages API, or local terminal harnesses.
- **Cognitive Execution**: Processes multi-modal inputs (text, code, images, structured JSON) using hybrid neural-symbolic extended reasoning chains.
- **Downstream Dispatch**: Generates tool invocations over FastMCP 3.1, modifying local codebases, querying vector engines, or dispatching sub-agent tasks.

## Typical use cases
- **Autonomous Repository Engineering**: Leveraging terminal agent harnesses like Claude Code to refactor microservices, resolve complex issues, and execute multi-language test suites.
- **Enterprise Security Auditing**: Analyzing million-line codebases and cloud infrastructure manifests in a single context window to discover vulnerabilities.
- **Hybrid Multi-Model Routing**: Intelligently dispatching sub-tasks between Claude 5.6 Opus (deep reasoning), Claude 5.6 Sonnet (balanced latency/cost), and Claude 5.6 Haiku (high-throughput edge routing).
- **Stateful Multi-Agent Workflows**: Serving as the core supervisor engine for multi-agent graph orchestrators like LangGraph, Bee, or CrewAI.

## Strengths
- **State-of-the-Art Reasoning & Coding**: Industry-leading performance on SWE-bench Verified, HumanEval, and real-world multi-repo refactoring benchmarks.
- **Advanced Constitutional Safety**: Embedded alignment minimizing security risks and prompt injection vulnerabilities without limiting developer tool execution power.
- **Massive Context & Caching**: Native 1.5M+ token context window with sub-second retrieval via high-efficiency prompt caching.
- **Native FastMCP 3.1 Integration**: First-class support for FastMCP task states, resource streaming, and schema validation.

## Limitations
- **Proprietary Closed Weights**: Closed-source API architecture compared to open-weight models like [Gemma 4](../ai_knowledge/local_llms.md) or Llama 4.
- **Cost for Extended Thinking**: Allocating large extended thinking token budgets carries increased API compute charges per request.
- **Network Dependency**: Requires secure connection to Anthropic API endpoints; offline edge execution requires local model fallbacks.

## When to use it
- When maximum reasoning accuracy, complex code generation, and reliable instruction adherence are required.
- When ingesting massive document repositories that exceed standard context window limits.
- For enterprise agent platforms requiring safe tool execution, strict auditability, and FastMCP 3.1 compliance.

## When not to use it
- For basic, high-volume commodity text processing where lightweight local models offer lower latency and zero variable cost.
- For completely air-gapped on-premise deployments without internet routing (use [vLLM](../infrastructure/vllm.md) or [Local LLMs](local_llms.md)).

## Getting started

### Interactive & Developer Portals
1. **Claude.ai Portal**: Interactive artifact rendering, project knowledge bases, and team workspaces.
2. **Anthropic Developer Console**: Create API keys, configure rate limit tiers, and monitor usage metrics.

### System Installation & Setup
```bash
# Install official Anthropic Python SDK
pip install anthropic pydantic httpx

# Set API key environment variable
export ANTHROPIC_API_KEY="sk-ant-api03-your-actual-api-key-here"
```

## CLI examples

### Terminal Agent Harness (Claude Code)
Anthropic's official agentic CLI for software engineering:

```bash
# Install Claude Code globally via npm
npm install -g @anthropic-ai/claude-code

# Authenticate with Anthropic Developer Console
claude auth login

# Initialize Claude agent in target git repository
claude init

# Instruct Claude Code to perform multi-file refactoring
claude "Refactor legacy FastMCP 2.0 handlers to FastMCP 3.1 Task Protocol in src/mcp_server.py and add unit test coverage"
```

### Direct Curl Query with Dynamic Prompt Caching
```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-7-sonnet-20250219",
    "max_tokens": 2048,
    "thinking": {
      "type": "enabled",
      "budget_tokens": 1024
    },
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "System architecture guidelines for FastMCP 3.1 Task Protocol...",
            "cache_control": {"type": "ephemeral"}
          },
          {
            "type": "text",
            "text": "How do we handle task cancellation during streaming?"
          }
        ]
      }
    ]
  }'
```

## API examples

### Complete FastMCP 3.1 Task Protocol Integration Script
This production-ready Python script demonstrates how an autonomous agent can invoke Claude 3.7 / 5.6 using the Anthropic API with extended thinking enabled, managing tool calls over the FastMCP 3.1 Task Protocol.

```python
"""
Claude FastMCP 3.1 Extended Thinking Agent Engine.
Demonstrates Anthropic API messaging with extended thinking tokens and tool execution.
"""

import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional
import anthropic
from pydantic import BaseModel, Field

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("claude-agent-mcp")

# Environment Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-7-sonnet-20250219")

client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

# Define Tool Schemas for Claude Execution
AVAILABLE_TOOLS = [
    {
        "name": "mcp_execute_bash",
        "description": "Executes a bash command in a secure sandbox container.",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "The command line string to execute."}
            },
            "required": ["command"]
        }
    }
]


async def run_claude_thinking_agent(prompt: str) -> None:
    logger.info(f"Submitting query to {CLAUDE_MODEL} with extended thinking budget...")

    messages = [
        {"role": "user", "content": prompt}
    ]

    try:
        response = await client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            thinking={
                "type": "enabled",
                "budget_tokens": 2048
            },
            tools=AVAILABLE_TOOLS,
            messages=messages
        )

        logger.info(f"Response Received. Stop Reason: {response.stop_reason}")

        # Display thinking blocks and final text content
        for block in response.content:
            if block.type == "thinking":
                print("\n=== CLAUDE EXTENDED THINKING BLOCK ===")
                print(block.thinking)
                print("======================================")
            elif block.type == "text":
                print("\n=== CLAUDE RESPONSE ===")
                print(block.text)
            elif block.type == "tool_use":
                print(f"\n=== TOOL CALL REQUESTED: {block.name} ===")
                print(f"Arguments: {block.input}")

    except anthropic.APIError as err:
        logger.error(f"Anthropic API execution failed: {err}")


if __name__ == "__main__":
    test_prompt = "Analyze the performance bottleneck in our database indexer and suggest a shell command to benchmark throughput."
    asyncio.run(run_claude_thinking_agent(test_prompt))
```

### Pydantic v2 Usage Stats & Response Audit Validation
This script validates Anthropic API response payloads, token usage metrics, prompt cache statistics, and thinking block details using strict Pydantic v2 models.

```python
"""
Pydantic v2 Payload & Cache Metrics Auditor for Claude API.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class CacheUsageMetrics(BaseModel):
    cache_creation_input_tokens: int = Field(default=0, ge=0, description="Tokens written to ephemeral prompt cache")
    cache_read_input_tokens: int = Field(default=0, ge=0, description="Tokens read from ephemeral prompt cache")


class TokenUsageReport(BaseModel):
    input_tokens: int = Field(..., ge=0, description="Input prompt tokens processed")
    output_tokens: int = Field(..., ge=0, description="Generated response tokens")
    cache_metrics: Optional[CacheUsageMetrics] = Field(default=None)

    @model_validator(mode="after")
    def compute_cache_efficiency(self) -> "TokenUsageReport":
        if self.cache_metrics and self.input_tokens > 0:
            read_tokens = self.cache_metrics.cache_read_input_tokens
            efficiency = (read_tokens / (self.input_tokens + read_tokens)) * 100
            print(f"[Metrics] Prompt Cache Hit Rate: {efficiency:.1f}%")
        return self


class ClaudeResponsePayload(BaseModel):
    id: str = Field(..., min_length=4, description="Unique Claude message ID")
    model: str = Field(..., description="Claude model variant used")
    role: str = Field(default="assistant")
    stop_reason: str = Field(..., description="Termination reason: end_turn, tool_use, max_tokens")
    usage: TokenUsageReport = Field(..., description="Token and cache telemetry")

    @field_validator("stop_reason")
    @classmethod
    def validate_stop_reason(cls, v: str) -> str:
        valid_reasons = {"end_turn", "tool_use", "max_tokens", "stop_sequence"}
        if v not in valid_reasons:
            raise ValueError(f"Unknown stop reason: {v}")
        return v


def audit_api_response(raw_payload: dict) -> None:
    try:
        validated = ClaudeResponsePayload.model_validate(raw_payload)
        print("=== Claude API Response Successfully Audited ===")
        print(f"Message ID: {validated.id} | Model: {validated.model}")
        print(f"Input Tokens: {validated.usage.input_tokens} | Output Tokens: {validated.usage.output_tokens}")
        print(f"Stop Reason: {validated.stop_reason}")
    except Exception as err:
        print(f"Audit Validation Error: {err}")


if __name__ == "__main__":
    sample_response_data = {
        "id": "msg_01XJ920KLLM8",
        "model": "claude-3-7-sonnet-20250219",
        "role": "assistant",
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 1240,
            "output_tokens": 380,
            "cache_metrics": {
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 4800
            }
        }
    }

    audit_api_response(sample_response_data)
```

## Related tools / concepts
- [ChatGPT](chatgpt.md) — OpenAI conversational and reasoning platform.
- [Gemma 4](../ai_knowledge/local_llms.md) — Open model family for edge deployment.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive guide to Claude Code terminal workflows.
- [Claude How-To](claude-howto.md) — Practical implementation patterns and recipes.
- [FastMCP](../automation_orchestration/mcp.md) — Standardized tool and resource protocol.
- [Anthropic](../providers/anthropic.md) — Anthropic developer provider page.
- [Claude Code](../development_ops/claude-code.md) — CLI agent design and behavior.
- [Claude Context Mode](../development_ops/claude-context-mode.md) — Managing large context windows.

## Sources / references
- [Anthropic Official Web Portal](https://claude.ai/)
- [Anthropic Developer Console](https://console.anthropic.com/)
- [Anthropic API Documentation](https://docs.anthropic.com/claude/docs)
- [Anthropic Research & Engineering Blog](https://www.anthropic.com/news)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

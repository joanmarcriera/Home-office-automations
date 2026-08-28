# OpenClaw

## What it is
OpenClaw (formerly Clawdbot/Moltbot) is an open-source, self-hostable autonomous AI agent platform designed for deploying personal and team agents. It runs as a lightweight TypeScript "Gateway" process that interfaces with 50+ messaging channels (Telegram, WhatsApp, Signal, Discord, Slack) and manages persistent local memory, fully supporting the [MCP 3.1 Task Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) and FastMCP 3.1 streaming telemetry as of early January 2027.

## What problem it solves
Setting up a personal AI agent that works continuously and integrates with local system resources normally requires complex orchestration. OpenClaw simplifies this by providing a single-port Gateway (18789) that bridges LLMs (GPT-5.6, Claude 5.6, Gemini 4.0 Ultra, DeepSeek-V4, or [Gemma 4](../ai_knowledge/local_llms.md)) to the user's local operating system and messaging apps, utilizing **FastMCP 3.1** for rapid, low-latency tool execution and streaming event progress.

## Where it fits in the stack
**Agent Runtime / Orchestration Layer**. OpenClaw is the execution environment for autonomous behaviors. It sits between the user's communication channels and the model inference provider ([LiteLLM](../../services/litellm.md)), utilizing [MCP 3.1](../../tools/automation_orchestration/mcp.md) for seamless tool integration.

## Typical use cases
- **Personal Assistant**: Manage tasks in [Vikunja](../../services/vikunja.md) or [Home Assistant](../../services/home-assistant.md) via chat.
- **Local File Automation**: Organize downloads, process receipts (OCR), and update local databases autonomously.
- **CI/CD Remediation**: Automatically analyze build failures and draft PR fixes in GitHub using [Claude Code](claude-code.md).
- **Scheduled Research**: Aggregate web research into a daily briefing via [SearXNG](../../services/searXNG-automation.md).
- **Gemma 4 / Qwen 3.6 Integration**: Running local-first agentic workflows with [Gemma 4](../ai_knowledge/local_llms.md) and Qwen 3.6 VL via FastMCP 3.1.

## Strengths
- **Low Latency**: Local Gateway architecture ensures fast tool execution and messaging compared to cloud-only platforms.
- **Privacy-First**: Conversation history and vector memory stay on your local device or self-hosted infrastructure.
- **Extreme Extensibility**: 2,500+ community skills on **ClawdHub** cover almost any API or service.
- **Model Agnostic**: Seamlessly switch between [Ollama](../../services/ollama.md), [Gemma 4](../ai_knowledge/local_llms.md), DeepSeek-V4, GPT-5.6, Llama 4, and Claude 5.6.
- **FastMCP 3.1 Support**: Native integration with the latest Model Context Protocol for unified tool access and streaming task progress.

## Limitations
- **Security Governance**: Requires technical knowledge to properly sandbox and secure against unauthorized remote skill invocation.
- **Token Consumption**: Autonomous loops can quickly consume API budgets; requires [LiteLLM](../../services/litellm.md) budget management.
- **macOS/Linux Focus**: Windows support is primarily via WSL2/Docker, with some native limitations.

## When to use it
- For tasks requiring multi-step reasoning and action-taking on a local machine or home server.
- When you want a ready-to-run personal assistant that works through existing messaging apps like Signal or Discord.
- For home-lab automation tied to Ollama, n8n, Paperless-ngx, or Vikunja.

## When not to use it
- For mission-critical tasks where zero autonomous interpretation is required (use [n8n](../../services/n8n.md) instead).
- If you are uncomfortable maintaining a self-hosted Docker or Node.js environment.
- For purely cloud-native workflows where local system access is not needed.

## Getting started

### Local Installation (macOS/Linux)
OpenClaw is optimized for local execution on macOS (Apple Silicon) and Linux.

```bash
# One-command installer (Official 2027 script)
curl -fsSL https://openclaw.io/install.sh | sh

# Start the Gateway
openclaw start
```

### Docker Setup (Self-hosted)
For server environments, use Docker to ensure sandboxed tool execution.

```yaml
services:
  openclaw:
    image: openclaw/openclaw:latest
    ports:
      - "18789:18789"
    environment:
      GATEWAY_PORT: 18789
      LLM_BASE_URL: "http://litellm:4000"
      LLM_MODEL: "claude-5-6-sonnet"
      SIGNAL_SERVICE_URL: "http://signal-api:8080"
    volumes:
      - ./skills:/app/skills
      - ./memory:/app/memory
```

## CLI examples
OpenClaw provides a powerful CLI for managing the agent and its memory:

```bash
# Install a skill from ClawdHub
openclaw skill install clawdhub:receipt-processor

# Evaluate agent performance on a specific suite
openclaw eval --suite tests/assistant_bench.yaml

# Inspect the vector memory
openclaw memory query "What did we discuss about the house renovation?"
```

## API examples
OpenClaw exposes a REST API (typically on port 18789) for programmatic interaction:

```bash
# Trigger a specific skill via API
curl -X POST http://localhost:18789/api/execute \
  -H "Content-Type: application/json" \
  -d '{"skill": "weather-report", "params": {"location": "San Francisco"}}'

# Query the agent's status
curl http://localhost:18789/api/status
```

## Programmatic Integration Example
Here is a robust Python script utilizing Pydantic v2 to validate skill execution metadata and output schemas returned from the OpenClaw Gateway.

```python
import requests
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ValidationError

class SkillResult(BaseModel):
    skill_name: str = Field(..., alias="skill")
    success: bool
    execution_time_ms: float = Field(..., ge=0)
    data: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)

def execute_openclaw_skill(skill_name: str, params: Dict[str, Any]) -> Optional[SkillResult]:
    """Triggers an OpenClaw skill via Gateway REST API and validates output with Pydantic v2."""
    url = "http://localhost:18789/api/execute"
    payload = {
        "skill": skill_name,
        "params": params
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        raw_json = response.json()

        # Parse and validate with Pydantic v2 model
        validated_result = SkillResult.model_validate(raw_json)
        return validated_result
    except requests.RequestException as e:
        print(f"Network error interacting with OpenClaw Gateway: {e}")
        return None
    except ValidationError as e:
        print(f"OpenClaw execution schema mismatch: {e}")
        return None

if __name__ == "__main__":
    result = execute_openclaw_skill("receipt-processor", {"file_path": "/data/invoice_9912.pdf"})
    if result and result.success:
        print(f"Skill '{result.skill_name}' completed successfully in {result.execution_time_ms}ms")
        print(f"Extracted metadata: {result.data}")
    else:
        error_msg = result.errors if result else "Execution failed"
        print(f"Failed to execute skill: {error_msg}")
```

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — Recommended model router and inference plane.
- [Claude Code](claude-code.md) — For agentic coding and terminal-based automation.
- [OpenHands](openhands.md) — For code-heavy engineering tasks.
- [n8n](../../services/n8n.md) — For deterministic, non-conversational workflows.
- [Ollama](../../services/ollama.md) — Local model inference engine.
- [Gemma 4](../ai_knowledge/local_llms.md) — Recommended local model for agentic tasks.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Standard for agentic tool use.
- [Nanoclaw](nanoclaw.md) — Lightweight, containerized alternative.

## Sources / references
- [Official Website](https://openclaw.io/)
- [GitHub Repository](https://github.com/openclaw/openclaw)
- [ClawdHub Skill Registry](https://clawdhub.ai/)
- [FastMCP 3.1 Protocol Documentation](https://modelcontextprotocol.org)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

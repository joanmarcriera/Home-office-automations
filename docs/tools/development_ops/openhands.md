# OpenHands

## What it is
OpenHands (formerly OpenDevin) is an open-source platform for autonomous AI software engineering. It provides a full sandboxed execution environment — terminal, browser, file editor, and code runner — that lets AI agents plan, implement, test, and verify software changes end-to-end. As of early January 2027, it is the industry-standard execution environment for high-autonomy agents powered by frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**. It features native support for the **FastMCP 3.1 Task Protocol**, enabling seamless event streaming, structured tool execution, and verifiable telemetry.

SWE-Bench Verified score: **81.4%** (one of the highest published scores for autonomous software engineering agents).

## What problem it solves
Complex software engineering tasks — implementing a multi-file REST feature, hunting down a subtle async race condition, migrating a database schema, writing unit and integration tests — require more than single-file edits. They require running code, inspecting browser output, reading error logs, and iterating on failures. OpenHands provides that full loop: an AI agent that can plan, act, observe outcomes, and self-correct inside a safe sandbox without constant human intervention. It eliminates the reliability gap in AI coding by providing a containerized, verifiable execution environment.

## Where it fits in the stack
**Agent Platform / Execution Environment Layer**. OpenHands is heavier than a code-editor plugin ([Aider](aider.md), [Cursor](cursor.md)) and more code-focused than a general personal agent platform ([OpenClaw](openclaw.md)). It is the right layer when you need a multi-step, self-verifying software engineering loop. It often serves as the core execution backend for "Autonomous Software Factories".

```text
┌────────────────────────────────────────────────────────┐
│             User (CLI / Local GUI / Cloud UI)           │
└──────────────────────────┬─────────────────────────────┘
                           │  task description
┌──────────────────────────▼─────────────────────────────┐
│                   OpenHands Agent Loop                  │
│  Plan → Act (edit/run/browse) → Observe → Revise       │
└──────────────────────────┬─────────────────────────────┘
                           │  LLM API calls
┌──────────────────────────▼─────────────────────────────┐
│     LiteLLM / OpenRouter / Ollama / Direct API          │
└──────────────────────────┬─────────────────────────────┘
                           │  sandboxed execution
┌──────────────────────────▼─────────────────────────────┐
│          Docker Sandbox (terminal + browser + files)    │
└────────────────────────────────────────────────────────┘
```

## Typical use cases
- **End-to-end feature implementation**: "Implement a REST endpoint for user profile updates, including input validation, error handling, and tests."
- **Bug hunting and resolution**: "The background job occasionally throws a KeyError in worker.py. Find the root cause and fix it."
- **Codebase migration**: "Migrate all uses of the deprecated `requests` library to `httpx` with async support."
- **Documentation generation**: "Generate API reference docs for all public classes in the `sdk/` directory."
- **Test coverage improvement**: "Our coverage report shows src/parsers/ at 42%. Write tests to bring it to 85%+."
- **Security review and remediation**: "Scan this codebase for SQL injection vulnerabilities and apply fixes."
- **Microagent Orchestration**: Utilizing YAML-defined sub-agents (e.g., `.openhands/microagents/test-writer.yaml`) for scoped, domain-specific tasks.

## Strengths
- **High SWE-Bench Performance**: 81.4% on SWE-bench Verified — among the highest published scores for autonomous software engineering agents.
- **Full Sandboxed Execution Environment**: Terminal, browser, file editor, and code runner in a unified Docker environment.
- **Model-Agnostic and Frontier SOTA Optimized**: Optimized for Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Qwen 3.6 VL, and local Gemma 4 / Llama 4 via Ollama.
- **FastMCP 3.1 Task Protocol Native**: Leverages the standardized Task Protocol for structured tool-use and real-time streaming telemetry.
- **Microagent Architecture**: Reusable, scoped sub-agents for specialized domain tasks.
- **MIT-licensed Core**: Open-source core with full self-hosting capabilities.

## Limitations
- **Resource Intensive**: The Docker sandbox requires significant RAM; minimum 8 GB for practical use, 16 GB+ recommended for multi-container workloads.
- **Latency Over Single Edits**: The autonomous plan-act-observe loop adds step latency compared to single-file inline code generators.
- **Token Consumption**: Autonomous multi-step loops consume substantial token budgets; LiteLLM budget control is recommended.
- **Security Scope**: Requires isolated Docker daemon configuration and network policy sandboxing.

## When to use it
- For complex, multi-step software engineering tasks requiring iteration and execution verification.
- When the agent needs to execute code, run tests, and observe browser output to confirm correctness.
- When you require a sandboxed execution environment that isolates changes from your host machine.
- When building automated software factory pipelines via the OpenHands SDK.

## When not to use it
- For simple single-file code edits — use [Aider](aider.md) or [Claude Code](claude-code.md).
- On environments with severe RAM restrictions (< 8 GB).
- When sub-second response times are required.
- For non-coding personal assistant tasks (use [OpenClaw](openclaw.md)).

## Getting started

### Docker Installation (Local GUI)
```bash
# Pull and run the official container (2027 release)
docker run -it --rm \
  -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik \
  -e LOG_ALL_EVENTS=true \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/.openhands-state:/.openhands-state \
  -p 3000:3000 \
  --add-host host.docker.internal:host-gateway \
  --name openhands-app \
  docker.all-hands.dev/all-hands-ai/openhands:0.45

# Access the GUI at http://localhost:3000
```

### Model Configuration
OpenHands connects to any model via an OpenAI-compatible interface or direct provider API:

```bash
# Claude 5.6 (Recommended)
export LLM_MODEL="anthropic/claude-5-6-sonnet"
export LLM_API_KEY="<anthropic-key>"

# Gemini 4.0 Ultra
export LLM_MODEL="google/gemini-4.0-ultra"
export LLM_API_KEY="<gemini-key>"

# Local Gemma 4 via Ollama
export LLM_MODEL="ollama/gemma-4"
export LLM_BASE_URL="http://localhost:11434"
```

## CLI examples

### Installation
```bash
pip install openhands-ai
```

### Running a task
```bash
export LLM_MODEL="anthropic/claude-5-6-sonnet"
export LLM_API_KEY="<key>"

# Run an autonomous engineering task
openhands "Fix the failing unit tests in src/tests/test_parser.py"
```

## API examples

### Python SDK Usage
The Python SDK lets you build custom agent pipelines or run OpenHands non-interactively:

```python
from openhands import OpenHandsAgent

agent = OpenHandsAgent(
    model="anthropic/claude-5-6-sonnet",
    api_key="<key>",
    workspace_dir="./my-project",
)

result = agent.run(
    "Add comprehensive type annotations to all functions in src/utils.py "
    "and update the docstrings to match."
)
print(result.summary)

# Interactive session via SDK
with agent.session() as session:
    session.run("Fix imports in main.py")
    session.run("Run pytest and report failures")
```

### Robust OpenHands Config Validation with Pydantic v2
The following Python script illustrates how to model and programmatically validate an OpenHands agent configuration and Docker runtime sandbox profile under early January 2027 standards, ensuring strict schema safety and type correctness using Pydantic v2:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
import json

class SandboxConfig(BaseModel):
    container_image: str = Field(default="docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik")
    memory_limit_gb: int = Field(default=16, ge=4, le=128)
    allow_network_access: bool = True
    exposed_ports: List[int] = Field(default_factory=list)

    @field_validator("exposed_ports")
    @classmethod
    def validate_ports(cls, ports: List[int]) -> List[int]:
        for port in ports:
            if not (1 <= port <= 65535):
                raise ValueError(f"Port {port} must be a valid port number.")
        return ports

class OpenHandsConfig(BaseModel):
    model_name: str = Field(..., pattern=r"^[a-zA-Z0-9_/.-]+$")
    api_key: str = Field(..., min_length=1)
    workspace_dir: str = Field(default="./workspace")
    sandbox: SandboxConfig = Field(default_factory=SandboxConfig)
    mcp_version: str = Field("3.1", pattern=r"^3\.1$")
    timeout_seconds: int = Field(default=3600, ge=60, le=86400)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "model_name": "anthropic/claude-5-6-sonnet",
                "api_key": "sk-ant-...",
                "workspace_dir": "./my-project",
                "sandbox": {
                    "container_image": "docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik",
                    "memory_limit_gb": 16,
                    "allow_network_access": True,
                    "exposed_ports": [3000, 8080]
                },
                "mcp_version": "3.1",
                "timeout_seconds": 1800
            }
        }
    }

def validate_config(payload: dict) -> str:
    """Validates OpenHands configuration payload using Pydantic v2."""
    try:
        config = OpenHandsConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_config": config.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    test_payload = {
        "model_name": "anthropic/claude-5-6-sonnet",
        "api_key": "sk-ant-test-key-123",
        "workspace_dir": "./agent-sandbox",
        "sandbox": {
            "container_image": "docker.all-hands.dev/all-hands-ai/runtime:0.45-nikolaik",
            "memory_limit_gb": 16,
            "allow_network_access": True,
            "exposed_ports": [3000, 8000]
        },
        "mcp_version": "3.1",
        "timeout_seconds": 1800
    }
    print(validate_config(test_payload))
```

## Related tools / concepts
- [LiteLLM](../../services/litellm.md) — Recommended model proxy for local/cloud LLM routing.
- [Aider](aider.md) — Targeted terminal pair-programmer.
- [Claude Code](claude-code.md) — Interactive CLI with tight Anthropic model integration.
- [OpenClaw](openclaw.md) — General-purpose autonomous agent runtime.
- [Gemma 4](../ai_knowledge/local_llms.md) — Preferred local model for high-autonomy coding tasks.
- [Model Context Protocol](../automation_orchestration/mcp.md) — Standard for agent tool integration.
- [SWE-Bench](../benchmarking/swe-bench.md) — Benchmark for evaluating software engineering agents.
- [Cursor](cursor.md) — AI-powered code editor.
- [Claude Code Container MCP](claude-code-container-mcp.md) — Sandboxed execution for Claude Code.

## Sources / references
- [GitHub — All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands Documentation](https://docs.openhands.dev/)
- [OpenHands SDK Docs](https://docs.openhands.dev/sdk)
- [FastMCP 3.1 Task Protocol Specification](https://modelcontextprotocol.org)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Kimi Code CLI

## What it is
Kimi Code CLI (officially `kimi-cli`) is an open-source, terminal-native AI coding agent from Moonshot AI. It operates as an agentic loop directly in the terminal, capable of reading and editing code, executing shell commands, searching the web, and autonomously planning multi-step software development tasks. As of early 2027, it is a leading alternative for developers seeking high-performance agentic workflows outside of browser-based IDEs, powered by Moonshot's **Kimi K3.5** models and fully integrated with **FastMCP 3.1** protocols.

## What problem it solves
It reduces context switching by bringing AI-powered software engineering capabilities into the developer's primary workspace: the terminal. Unlike standard chat interfaces, Kimi Code CLI has direct access to the local filesystem and shell, allowing it to perform actions like refactoring code, running tests, and fixing build errors autonomously. It leverages frontier reasoning models to handle complex multi-file edits that traditional autocomplete tools cannot manage.

## Where it fits in the stack
**Development & Ops / AI Coding Agent**. It is a CLI-native alternative to [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code.md), optimized for high-speed terminal interaction and agentic workflows. It integrates with the broader ecosystem via the **FastMCP 3.1** protocol for tool discovery and resource management.

## Typical use cases
- **Autonomous Feature Implementation**: Describing a new feature and letting the agent write the code and verify it.
- **Automated Bug Fixing**: Providing a stack trace and letting the agent find the root cause and apply a patch.
- **Codebase Exploration**: Asking questions about unfamiliar architectures or "finding where X is implemented."
- **Terminal Operations**: Natural language commands for complex shell tasks (e.g., "Find all large log files and compress them").
- **Agentic CI/CD**: Running as a headless agent to perform automated remediation in deployment pipelines.

## Strengths
- **Agentic Loop**: Plans, executes, and adjusts actions based on terminal feedback.
- **Native Terminal Integration**: No need to leave the shell for AI assistance.
- **FastMCP 3.1 Support**: Full support for the Model Context Protocol, enabling connection to thousands of external tools and data sources.
- **Web Access**: Can search and fetch live documentation to ground its coding suggestions.
- **Multi-Model Support**: Native support for Claude 5.1, GPT-5.5, and Moonshot's Kimi K3.5 models.
- **NVIDIA NIM Integration**: Can be configured to use local NVIDIA Inference Microservices (NIM) for ultra-low latency on **NVIDIA Rubin** GPUs.

## Limitations
- **Latency**: Agentic reasoning steps can take time, especially for complex planning.
- **Shell Compatibility**: Some built-in shell commands like `cd` are currently handled via a workaround rather than natively in all modes.
- **Context Management**: Large codebases can still hit context limits if not managed carefully, though planning helps.
- **Hardware Requirements**: Local NIM execution requires modern GPU hardware for optimal performance.

## When to use it
- When you want an AI pair programmer that can actually *run* the code it writes.
- For rapid refactoring tasks across multiple files.
- When working in remote SSH environments where a browser-based AI is inaccessible.
- As a faster, terminal-native alternative to [Claude Code](../development_ops/claude-code.md).
- When you need to integrate with local MCP servers for private data access.

## When not to use it
- For simple snippets that don't require file or shell context (use a standard chat).
- If you prefer a GUI-first experience (use [Cursor](../development_ops/cursor.md)).
- In environments where terminal access is strictly restricted or audited in a way that interferes with agentic execution.

## Getting started

### Installation
Install using the official script (requires Python 3.12+):

```bash
# Linux / macOS
curl -LsSf https://code.kimi.com/install.sh | bash

# Verify installation
kimi --version
```

### Initial Setup
Run the setup wizard to configure your API provider or local NIM:

```bash
kimi /login
```

### Hello World Example
To verify Kimi is working correctly:

```bash
kimi "Write a 'hello world' script in Python and run it"
```

## CLI examples

```bash
# Refactor a specific module
kimi "Refactor the authentication logic in src/auth.py to use JWT instead of sessions"

# Find and fix errors
kimi "Run the test suite and fix any failing tests in the reports module"

# Explain code
kimi "Explain how the routing works in this project"

# Use a specific FastMCP 3.1 tool
kimi "Use the github-mcp server to list open issues in this repo"
```

## API examples

### IDE Integration (Zed setting setting)
Kimi Code CLI supports the Agent Client Protocol (ACP). To use it as an agent server in Zed, add this to your `settings.json`:

```json
{
  "agent_servers": {
    "Kimi Code CLI": {
      "type": "custom",
      "command": "kimi",
      "args": ["acp"]
    }
  }
}
```

### Manual Configuration (~/.kimi/config.toml)
For advanced users, providers can be configured manually:

```toml
[providers.kimi-for-coding]
type = "kimi"
base_url = "https://api.kimi.com/coding/v1"
api_key = "sk-xxxxxxxxxxxx"

[providers.nvidia-nim]
type = "openai_legacy"
base_url = "http://localhost:8000/v1"
api_key = "nim-local"
```

### Programmatic Integration (FastMCP 3.1 compliant with Pydantic v2)
Executing coding tasks programmatically using a JSON-RPC FastMCP 3.1 interface with strict Pydantic v2 validation:

```python
import json
import urllib.request
from pydantic import BaseModel, Field, field_validator

class KimiTaskPayload(BaseModel):
    prompt: str = Field(..., description="Coding instruction/task description.")
    workspace_path: str = Field(..., description="Absolute path to the repository.")
    mcp_version: str = Field(default="3.1", description="FastMCP specification version.")

    @field_validator('workspace_path')
    @classmethod
    def validate_path(cls, v: str) -> str:
        if not v.startswith("/"):
            raise ValueError("workspace_path must be an absolute path starting with /")
        return v

def invoke_kimi_mcp_task(task: KimiTaskPayload) -> dict:
    url = "http://localhost:8000/v1/mcp/tasks"
    payload = {
        "jsonrpc": "2.0",
        "method": "execute_kimi_agent",
        "params": task.model_dump(),
        "id": "kimi-cli-task-execution"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

# Example usage:
# task = KimiTaskPayload(prompt="Fix tests", workspace_path="/home/user/repo")
# print(invoke_kimi_mcp_task(task))
```

## Related tools / concepts
- [Aider](../development_ops/aider.md)
- [Claude Code](../development_ops/claude-code.md)
- [Mentat](../development_ops/mentat.md)
- [Plandex](../development_ops/plandex.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Agent Client Protocol (ACP)](../../knowledge_base/agent_protocols.md)
- [Moonshot AI](../providers/moonshot.md)
- [Terminal Benchmarking](../benchmarking/terminal-bench.md)
- [NVIDIA NIM](../providers/nvidia.md)

## Sources / references
- [Official Kimi Code CLI Repository](https://github.com/MoonshotAI/kimi-cli)
- [Kimi Code CLI Documentation](https://moonshotai.github.io/kimi-cli/en/guides/getting-started.html)
- [Sébastien Dubois: Kimi CLI Overview](https://www.dsebastien.net/kimi-cli/)
- [NVIDIA NIM for LLMs](https://www.nvidia.com/en-us/ai-data-science/generative-ai/nim/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

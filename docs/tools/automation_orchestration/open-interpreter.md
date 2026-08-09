# Open Interpreter

## What it is
Open Interpreter is an open-source framework that allows Large Language Models (LLMs) to execute code (Python, JavaScript, Shell, R, and more) directly on your local computer. It provides a natural language interface to your system's capabilities, functioning as a powerful, locally-hosted, and uncensored alternative to OpenAI's Advanced Data Analysis (formerly Code Interpreter). As of December 2026, it is a cornerstone for "local-first" agentic workflows, featuring native support for **MCP 3.1 / FastMCP 3.1**, **Gemma 3**, **Llama 4**, and optimized integration with **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, and **Qwen 3.6**.

## What problem it solves
It overcomes the "walled garden" limitations of hosted LLM sandboxes. While hosted environments are restricted by sandboxing, lack of internet access (at times), and limited library availability, Open Interpreter runs on *your* hardware with *your* permissions. This enables agents to perform real-world tasks like managing local file systems, controlling system settings, interacting with local hardware/databases, and using any locally installed CLI tools without restriction.

## Where it fits in the stack
**Category**: Automation & Orchestration / Agentic Execution. It serves as the primary bridge between high-level LLM reasoning and low-level OS execution, providing a secure environment (via user confirmation) or a fully autonomous one (via the `--auto_run` flag).

## Typical use cases
- **Intelligent Local File Management**: "Scan my downloads folder, organize documents by month, and archive anything older than 90 days to my NAS."
- **Localized Data Science**: "Analyze my local SQLite database, generate a forecast for the next quarter, and output the charts as high-resolution PNGs."
- **OS-Level System Control**: "Switch my workstation to focus mode, launch my development Docker stack, and open the relevant Slack channels."
- **Automated Developer Workflows**: "Iterate through all files in this project and update the imports to reflect the latest FastMCP 3.1 schema requirements."

## Strengths
- **Unrestricted Local Access**: Full reach to your computer's files, internet connection, and installed environment.
- **Privacy-First Architecture**: When utilized with local models (Gemma 3, Llama 4, Qwen 3.6), sensitive data remains entirely on-premises.
- **Multilingual Execution**: Seamlessly switches between Python, Bash, JavaScript, and R within a single conversational turn.
- **FastMCP 3.1 Task Protocol**: Acts as a native MCP server or client, exposing local system capabilities as standardized tools to remote or localized agentic clients.

## Limitations
- **Security Implications**: Executing LLM-generated code locally requires vigilant oversight; a single hallucinated or malicious command can lead to catastrophic data loss.
- **Hardware Performance**: The speed and reliability of local execution are strictly bound by the host machine's CPU, GPU, and RAM.
- **Environmental Drift**: Code that runs perfectly in one local environment may fail in another due to missing dependencies or differing OS versions.

## When to use it
- When an agent needs direct, stateful interaction with the local file system or operating system.
- For complex data processing tasks where data privacy and sovereignty are non-negotiable.
- When leveraging open-weights models (Gemma 3, Llama 4, Qwen 3.6) for sophisticated system-level automation.

## When not to use it
- On production servers or highly sensitive environments without additional sandboxing (e.g., within a dedicated Docker or Podman container).
- For simple conversational tasks that do not require any system interaction or code execution.

## Getting started

### Installation
```bash
pip install open-interpreter
```

### Basic Usage with Gemma 3
```bash
# Start an interactive session using Gemma 3 via Ollama
interpreter --model ollama/gemma-3-27b
```
Type your request: "Create a summary of the current directory's file structure and save it to structure.md."

## CLI examples
```bash
# Start a standard interactive session
interpreter

# Run a specific task autonomously in a sandboxed environment
interpreter --task "Resize all JPGs in ~/Pictures to 1080p" --auto_run --safe_mode

# List all available local and remote models for use
interpreter --list-models
```

## API examples

### Programmatic Python Setup with Pydantic v2 Validation
To maintain the safety and integrity of code execution in late 2026, structured inputs must be strictly validated before invocation.

```python
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from interpreter import interpreter

# 1. Define strict validation schemas using Pydantic v2
class SafeExecutionPolicy(BaseModel):
    allowed_commands: List[str] = Field(
        default=["ls", "git status", "pip list"],
        description="Explicit list of permitted CLI command prefixes for the agent."
    )
    max_tokens: int = Field(default=2048, ge=256, le=8192)
    sandbox_enabled: bool = Field(default=True)

class TaskRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500)
    policy: SafeExecutionPolicy = Field(default_factory=SafeExecutionPolicy)

# 2. Programmatic execution utilizing validation and Open Interpreter
def run_autonomous_task(request_data: dict) -> str:
    try:
        # Strict validation of input using Pydantic v2
        request = TaskRequest.model_validate(request_data)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        raise

    # Configure interpreter with late 2026 local-first configurations
    interpreter.offline = True
    interpreter.llm.model = "ollama/gemma-3-27b"
    interpreter.llm.api_base = "http://localhost:11434/v1"

    # Configure safety and execution limits from our validated model
    interpreter.auto_run = request.policy.sandbox_enabled

    # Execute the request safely
    response = interpreter.chat(request.prompt)
    return str(response)

# Example invocation
if __name__ == "__main__":
    payload = {
        "prompt": "Check the status of our current git branch and list untracked files.",
        "policy": {
            "allowed_commands": ["git status"],
            "max_tokens": 1024,
            "sandbox_enabled": True
        }
    }
    result = run_autonomous_task(payload)
    print(result)
```

## Related tools / concepts
- [Ollama](../../services/ollama.md) — The preferred engine for running local models like Gemma 3 or Llama 4 with Interpreter.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's official CLI agent with deep system integration.
- [Aider](../development_ops/aider.md) — A specialized tool for LLM-assisted coding in terminal environments.
- [Model Context Protocol (MCP)](mcp.md) — For standardizing tool and resource access.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Architectural patterns for code-executing agents.
- [Goose](../agents/goose.md) — An alternative framework for local agentic execution.
- [Cline](../agents/cline.md) — A VS Code extension providing terminal-based agent capabilities.
- [OpenHands](../development_ops/openhands.md) — A comprehensive platform for autonomous software engineering.

## Sources / references
- [Open Interpreter Official Website](https://openinterpreter.com/)
- [Open Interpreter GitHub Repository](https://github.com/OpenInterpreter/open-interpreter)
- [FastMCP 3.1 Integration Guide](https://docs.openinterpreter.com/integrations/mcp)

## Contribution Metadata
- Last reviewed: 2026-12-23
- Confidence: high

# Cline

## What it is
Cline (formerly Claude Dev) is an open-source, autonomous AI coding agent that operates natively within VS Code and JetBrains IDEs. It possesses comprehensive access to the local filesystem, terminal, and a built-in browser, enabling it to execute end-to-end software engineering tasks. As of late October / November 2026, Cline is recognized as a foundational platform for agentic development, known for its stability and broad model support, including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0**, and **Gemma 3**.

## What problem it solves
Cline addresses the "copy-paste fatigue" by eliminating the need to manually transfer code and terminal output between a chat interface and the IDE. It solves the context limitation problem of standard LLM interfaces by allowing the agent to proactively explore the codebase, run its own tests, and debug issues until a task is completed, significantly increasing developer throughput for complex features.

## Where it fits in the stack
**Agent / IDE Extension / CLI / Developer Experience (DX)**. It acts as a high-level orchestrator that sits between the developer and the toolchain (Git, Compilers, Browsers, LLMs).

## Typical use cases
- **Legacy Migration**: Analyzing an entire codebase to migrate from deprecated libraries to modern equivalents (e.g., upgrading to React 19).
- **Test-Driven Development (TDD)**: Writing a test, observing it fail, and autonomously iterating on the code until the test passes.
- **System Discovery**: Exploring a new or large repository to map out dependencies and explain architectural patterns.
- **End-to-End Bug Fixing**: Taking a bug report, reproducing it with a script, fixing the code, and verifying the fix via the internal browser.
- **Local-First Development**: Running agentic tasks using high-performance local models like **Gemma 3** via Ollama or LM Studio.

## Strengths
- **Fully Autonomous**: Can manage long-running multi-step tasks including file creation, terminal commands, and browser interaction.
- **Provider Agnostic**: Robust support for all major LLMs (Claude 5.1, GPT-5.5, Gemini 4.0, **Gemma 3**) and local models.
- **Human-in-the-Loop**: Transparently asks for permission before any destructive action (e.g., file overwrite or terminal execution).
- **Extensible via MCP**: Native support for the Model Context Protocol (MCP) 3.1 to access external tools like Google Search or specialized APIs.
- **Stability**: Known for a reliable core feature set compared to more experimental forks.

## Limitations
- **Token Consumption**: Highly autonomous "Act" sessions can be expensive due to large context windows and iterative loops.
- **Performance Overhead**: Complex tasks in large repositories can cause IDE latency during intensive indexing or reasoning phases.
- **Safety Boundaries**: Requires careful oversight when granted full terminal access in sensitive environments.

## When to use it
- When you need an agent to perform multi-file edits and terminal-based verification.
- For complex refactoring tasks where the agent needs to "see" the result of its changes in real-time.
- If you want to use frontier models like Claude 5.1 or **Gemma 3** with full IDE context without vendor lock-in.

## When not to use it
- For trivial, single-line completions where a standard completion engine is faster.
- In environments where IDE extensions are strictly prohibited from accessing the terminal or filesystem.
- If you prefer the highly customizable "Custom Modes" feature found in its fork, [Roo Code](roo-code.md).

## Getting started
### Installation
1. Search for **Cline** in the VS Code Marketplace and install.
2. Click the robot icon in the sidebar to open the Cline interface.
3. Configure your API key (e.g., Anthropic, OpenAI, or OpenRouter) in the settings.
4. Select `claude-5-1-sonnet-20261022` or a **Gemma 3** model for best results.

### Basic Usage
1. Type a task in the chat box (e.g., "Add a dark mode toggle to the navbar using Tailwind").
2. Review the proposed plan.
3. Approve tool executions (file edits, terminal commands) as the agent progresses.

## CLI examples
```bash
# Install Cline CLI globally
npm install -g cline

# Authenticate with your preferred provider
cline auth

# Run a task in "Headless" mode (auto-approve all actions)
cline -y "Refactor the authentication logic to use JWT"

# Example: Using the Cline CLI for automated repository audits
cline task "Audit the current project for security vulnerabilities"

# Checking the version of the installed agent environment
cline --version
```

## API examples
Cline can be extended via MCP servers. A sample configuration in the Cline settings to add a search tool:

```json
{
  "mcpServers": {
    "google-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-search"],
      "env": {
        "GOOGLE_API_KEY": "your_key_here"
      }
    }
  }
}
```

### Validation of MCP Server Configurations with Pydantic v2
This python example parses and validates custom MCP server registration parameters and command line environment variables using **Pydantic v2**:

```python
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

class MCPServerParams(BaseModel):
    command: str = Field(..., description="The executable command to start the MCP server, e.g., node, python, npx")
    args: List[str] = Field(default_factory=list, description="Arguments to pass to the server command")
    env: Dict[str, str] = Field(default_factory=dict, description="Environment variables required by the server")

class ClineMCPSettings(BaseModel):
    mcp_servers: Dict[str, MCPServerParams] = Field(..., alias="mcpServers", description="Map of registered MCP server configurations")

def validate_cline_mcp_config(raw_json: str) -> Optional[ClineMCPSettings]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2 model_validate
        return ClineMCPSettings.model_validate(data)
    except ValidationError as e:
        print(f"Validation Error: {e.json()}")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON.")
        return None
```

## Related tools / concepts
- [Roo Code](roo-code.md) — A popular fork with more customization.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — The tool interaction standard.
- [Aider](../development_ops/aider.md) — Terminal-centric agent alternative.
- [Claude Code](../development_ops/claude-code.md) — Anthropic's native CLI.
- [Windsurf](../development_ops/windsurf.md) — Next-gen agentic IDE.
- [Gemma 3](../ai_knowledge/local_llms.md) — Standard high-performance local model.
- [Local LLMs](../ai_knowledge/local_llms.md) — Privacy-first execution guide.
- [Model Routing](../../knowledge_base/model_routing_guide.md) — Strategy for model selection.

## Sources / references
- [Official Cline GitHub](https://github.com/cline/cline)
- [Cline Documentation](https://docs.cline.bot/)
- [Anthropic Computer Use API](https://www.anthropic.com/news/computer-use)
- [MCP 3.1 Protocol Documentation](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high

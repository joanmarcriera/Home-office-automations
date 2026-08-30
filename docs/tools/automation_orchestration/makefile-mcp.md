# Makefile MCP

## What it is
An MCP server that auto-discovers Makefile targets and exposes them as individual, documented tools for AI assistants like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
Traditional Makefile MCP implementations often expose a single generic `make` tool, which prevents LLMs from "seeing" available targets in their tool list. `makefile-mcp` parses the Makefile to register each documented target as its own tool with descriptions, improving discoverability and ease of use in agentic workflows.

## Where it fits in the stack
**Tool / Automation**. It provides a discovery and execution layer for project-specific automation, bridging the gap between local build systems and frontier models using the [Model Context Protocol](mcp.md).

## Typical use cases
- Exposing build, test, lint, and deploy workflows to coding agents.
- Managing multi-project workflows by dynamically switching working directories.
- Documenting available automation targets for AI assistants in complex monorepos.

## Strengths
- **Target Discovery**: Automatically parses `##` comments to provide tool descriptions.
- **Dynamic Configuration**: Allows changing the working directory at runtime via a dedicated tool.
- **Security**: No shell expansion used; supports strict inclusion/exclusion of targets.
- **Built with FastMCP**: Full support for MCP 3.1 / FastMCP 3.1 routing logic and task protocol.

## Limitations
- Requires targets to be documented with `##` to be exposed as tools.
- Commands run in a specified working directory only.
- Limited to GNU Make compatible Makefiles.

## When to use it
- When you want your AI assistant to have direct, visible access to your project's `make` targets.
- When working on complex projects with many automation steps defined in a Makefile.
- When you need to switch contexts between different Makefiles in a single session.

## When not to use it
- If you do not use Makefiles for project automation.
- If you prefer a single generic entry point for all shell commands.
- For high-stakes production deployment targets without a "dry-run" check.

## Getting started

Makefile MCP scans your project Makefile and converts each documented target into an individual MCP tool. Targets must be documented using double-hash (`##`) comments on the target declaration line.

### Makefile Documentation Convention
Ensure your project `Makefile` targets are structured as follows:
```makefile
.PHONY: test lint build

test: ## Run the full unit and integration test suite
	pytest tests/ -v

lint: ## Execute lint and code style checks using ruff
	ruff check src/

build: lint test ## Package distribution archives
	python3 -m build
```

### 1. Installation
Install the server package locally or run it dynamically using `uv` (recommended) or standard `pip`:

```bash
# Recommended installation via uv
uv pip install makefile-mcp

# Standard installation via pip
pip install makefile-mcp

# Or run instantly without installation using uvx
uvx makefile-mcp --list
```

### 2. Configuration (Claude Desktop)
To register the server with your MCP client, append it to your `claude_desktop_config.json` configuration file:

```json
{
  "mcpServers": {
    "makefile-mcp": {
      "command": "uvx",
      "args": [
        "makefile-mcp",
        "--cwd",
        "/absolute/path/to/your/project"
      ]
    }
  }
}
```

### Hello World Example
Run the command in your shell to preview which Makefile targets will be exposed to your AI assistant as specialized tools:

```bash
makefile-mcp --list
```

## CLI examples
You can configure and customize target exposure and naming scopes directly via the command-line options:

```bash
# 1. Start the server exposing only safe targets while blocking dangerous ones
makefile-mcp --include "test,lint,format" --exclude "deploy,publish"

# 2. Expose targets with a custom tool prefix to avoid collision in client menus
makefile-mcp --prefix "myproj_"

# 3. Target a specific custom Makefile located outside the working directory
makefile-mcp --makefile ./build/Makefile --cwd ./build
```

## API examples

### Programmatic Setup with Pydantic v2 Validation
Below is a robust Python example utilizing **Pydantic v2** validation to parse and execute discovered Makefile targets securely under early January 2027 SOTA agentic environments.

```python
import subprocess
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# 1. Define schemas using strict Pydantic v2 annotations
class MakefileTarget(BaseModel):
    name: str = Field(..., min_length=1, description="The name of the Makefile target to execute.")
    description: Optional[str] = Field(default=None, description="The description of what this target does.")
    args: Optional[str] = Field(default=None, description="Optional command line arguments/variables to pass to Make (e.g. 'VERBOSE=1').")
    dry_run: bool = Field(default=False, description="Preview the execution commands without actually running them.")

class MakefileExecutorConfig(BaseModel):
    working_directory: str = Field(..., description="The directory where the Makefile resides.")
    allowed_targets: List[str] = Field(default_factory=list, description="Strict allowlist of Makefile targets.")
    timeout_seconds: int = Field(default=300, ge=10, le=1800)

# 2. Programmatic execution utilizing validation and process execution
def execute_makefile_target(config_payload: dict, target_payload: dict) -> str:
    try:
        # Strict validation of input configurations and target arguments using Pydantic v2
        config = MakefileExecutorConfig.model_validate(config_payload)
        target = MakefileTarget.model_validate(target_payload)
    except ValidationError as e:
        print(f"Validation failed: {e}")
        raise

    # Security check against the allowlist
    if config.allowed_targets and target.name not in config.allowed_targets:
        raise ValueError(f"Target '{target.name}' is not in the list of allowed targets.")

    # Formulate command
    cmd = ["make", target.name]
    if target.dry_run:
        cmd.append("--dry-run")
    if target.args:
        # Avoid shell expansion, pass directly
        cmd.append(target.args)

    print(f"Executing command: {' '.join(cmd)} in directory: {config.working_directory}")

    # In a production early January 2027 FastMCP 3.1 setup, this runs inside the server
    # Here we mock the command execution output
    simulated_output = f"Executing: {' '.join(cmd)}\nTarget run completed successfully."
    return simulated_output

# Example invocation in early 2027
if __name__ == "__main__":
    executor_config = {
        "working_directory": "/home/user/workspace/project",
        "allowed_targets": ["test", "lint", "build"],
        "timeout_seconds": 60
    }
    target_request = {
        "name": "test",
        "description": "Run the full unit and integration test suite",
        "args": "VERBOSE=1",
        "dry_run": True
    }

    result = execute_makefile_target(executor_config, target_request)
    print(result)
```

## Related tools / concepts
- [GNU Make](gnu-make.md)
- [Model Context Protocol](mcp.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [Zapier](zapier.md)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [MCP Registry](mcp-registry.md)
- [Claude Code](../development_ops/claude-code.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Makefile MCP GitHub](https://github.com/democratize-technology/makefile-mcp)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

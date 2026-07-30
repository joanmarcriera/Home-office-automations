# Desktop Commander MCP

## What it is
A privacy-first Model Context Protocol (MCP 3.1) server that provides AI assistants with terminal control, filesystem access, and surgical text editing capabilities. It is built to be the "local hands" for frontier models like **Claude 5.1** and **GPT-5.5**.

## What problem it solves
It enables AI assistants to interact directly with the local machine's development environment while strictly removing all telemetry, analytics, and external tracking typically found in similar tools. It solves the "trust gap" in agentic workflows by ensuring no data leaves the local environment except through explicitly defined MCP 3.1 tool calls.

## Where it fits in the stack
**Development & Ops / Tool Layer**. It serves as a secure bridge between an LLM-based agent (running in an MCP-compliant host like Claude Desktop or Cursor) and the local OS.

## Typical use cases
- Reading and writing files in a local development environment.
- Executing terminal commands and managing local processes for **Llama 4** fine-tuning.
- Searching code using `ripgrep` integrations for complex refactoring.
- Applying targeted search/replace operations (edit blocks) across multiple files.

## Strengths
- **Privacy-First**: No telemetry, analytics, or external connections; operates entirely on-device.
- **MCP 3.1 Native**: Full support for the latest Task Protocol, secure resource connection, and resource discovery.
- **Surgical Editing**: Includes the `edit_block` tool for precise, idempotent text replacements.
- **Configurable Security**: Allows blocking specific commands and restricting access to white-listed directories.

## Limitations
- **Permission Bound**: Operates with the permissions of the user running the server; lacks its own sandboxing.
- **Manual Config**: Requires manual configuration of allowed directories for security.
- **Local Only**: Not designed for remote or cloud-based execution without additional tunneling.

## When to use it
- When you want to give an agent access to your local dev environment but are concerned about privacy or data leakage.
- When you need a lightweight, reliable bridge for filesystem and terminal operations for `claude-5-1-20261101`.
- In highly regulated environments where telemetry is strictly prohibited.

## When not to use it
- In untrusted environments where the agent could perform destructive actions (unless strictly configured).
- If you require cloud-native orchestration (consider [Superconductor](superconductor.md) instead).
- If you need native browser automation (use [Playwright](playwright.md) for those tasks).

## Getting started

Desktop Commander MCP is designed for local-first, privacy-conscious AI workflows.

### 1. Installation
```bash
npm install -g @democratize-technology/desktop-commander-mcp
```

### 2. Configuration
Add the server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "desktop-commander": {
      "command": "desktop-commander-mcp",
      "args": [],
      "env": {
        "ALLOWED_DIRECTORIES": "/home/user/projects"
      }
    }
  }
}
```

### 3. Verify Connection
Check the Claude Desktop logs or status bar to ensure the server is connected and the `edit_block` and `run_command` tools are available.

## CLI examples

### 1. Starting the server manually
Useful for debugging or using with custom MCP clients:
```bash
desktop-commander-mcp --port 3000
```

### 2. Listing allowed directories
Verify which paths the commander has access to:
```bash
desktop-commander-mcp --list-allowed
```

### 3. Running a specific tool via CLI (using mcp-cli)
```bash
mcp-cli call desktop-commander list_files --path "."
```

## API examples

### 1. Searching Code (search_code)
Search for specific patterns across the codebase with high performance using `ripgrep`.

```json
{
  "tool": "search_code",
  "arguments": {
    "query": "async function authenticate",
    "include": ["src/**/*.ts"],
    "exclude": ["node_modules/**"]
  }
}
```

### 2. Surgical Editing (edit_block)
Apply precise text replacements using SEARCH/REPLACE blocks.

```json
{
  "tool": "edit_block",
  "arguments": {
    "path": "src/auth.ts",
    "edit": "<<<<<<< SEARCH\n  return user.id;\n=======\n  return { id: user.id, role: user.role };\n>>>>>>> REPLACE"
  }
}
```

### 3. Programmatic Configuration Validation using Pydantic v2
This Python script validates Desktop Commander directory whitelists and surgical editing arguments using **Pydantic v2** models before they are invoked by the local agent:

```python
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict, field_validator

class EditBlockArgs(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    path: str = Field(..., description="Target file path relative to allowed directories")
    edit: str = Field(..., description="The git merge diff block containing SEARCH/REPLACE blocks")

    @field_validator("edit")
    @classmethod
    def check_edit_block_syntax(cls, v: str) -> str:
        if "<<<<<<< SEARCH" not in v or "=======" not in v or ">>>>>>> REPLACE" not in v:
            raise ValueError("The edit must contain valid SEARCH/REPLACE markers: <<<<<<< SEARCH, =======, >>>>>>> REPLACE")
        return v

class CommanderConfig(BaseModel):
    allowed_directories: List[str] = Field(
        ...,
        validation_alias="allowedDirectories",
        description="Whitelist of host file system directories the agent is allowed to access"
    )
    port: int = Field(3000, description="TCP port to run the MCP server on")

def validate_commander_args(raw_json: str) -> Optional[EditBlockArgs]:
    try:
        data = json.loads(raw_json)
        # Validate using Pydantic v2
        args = EditBlockArgs.model_validate(data)
        return args
    except json.JSONDecodeError:
        print("Error: Input is not valid JSON.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None

# Example usage:
# if __name__ == "__main__":
#     sample_args = """
#     {
#         "path": "src/auth.py",
#         "edit": "<<<<<<< SEARCH\\n    return user.id\\n=======\\n    return user.id, user.role\\n>>>>>>> REPLACE"
#     }
#     """
#     validated_args = validate_commander_args(sample_args)
#     if validated_args:
#         print("Edit block configuration successfully verified!")
#         print(validated_args.model_dump_json(indent=2))
```

## Related tools / concepts
- [Claude Code](claude-code-setup.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude Code Container MCP](claude-code-container-mcp.md)
- [Aider](aider.md)
- [VS Code](vscode.md)
- [Zed](zed.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Agent Protocols](../../knowledge_base/agent_protocols.md)
- [Local LLMs](../ai_knowledge/local_llms.md)

## Sources / References
- [Desktop Commander MCP GitHub](https://github.com/democratize-technology/DesktopCommanderMCP)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-11-02
- Confidence: high

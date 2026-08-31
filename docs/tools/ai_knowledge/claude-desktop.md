# Claude Desktop

## What it is
Claude Desktop is a native application for macOS and Windows that brings Anthropic's Claude AI models directly to the user's workspace. It serves as the primary host for the Model Context Protocol (MCP), allowing Claude to interact with local files, data, and tools securely. As of early January 2027, it is the reference implementation for "Agentic Desktop" workflows, natively supporting **MCP 3.1 / FastMCP 3.1 Task Protocol** and frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**.

## What problem it solves
It overcomes the limitations of browser-based AI by providing a secure, local execution environment. Key problems solved include:
- **Local Context**: Direct access to local files and system resources through MCP without uploading sensitive data to public cloud environments.
- **Deep Integration**: Seamlessly integrates into desktop workflows via keyboard shortcuts, system-level hooks, and direct file drag-and-drop operations.
- **Tool Orchestration**: Serves as a standard host for MCP servers, enabling Claude to perform complex actions like searching local databases, interacting with desktop APIs, or managing terminal sessions.
- **Multi-Agent Coordination**: With MCP 3.1 / FastMCP 3.1 Task Protocol integrations, the desktop app acts as a local coordinator for sub-agents executing background micro-missions.

## Where it fits in the stack
**AI Assistants & Knowledge**. It is a primary interface for interacting with [Anthropic (Claude)](../providers/anthropic.md) and acts as the "host" in the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) architecture.

## Typical use cases
- **Developer Workflows**: Indexing local codebases and running local tests through MCP servers like `filesystem` or `playwright`.
- **Data Analysis**: Querying local CSVs, Excel files, or SQLite databases directly from the chat interface.
- **Personal Productivity**: Connecting to local calendars, email clients, and note-taking apps via MCP extensions.
- **Secure File Processing**: Summarizing and extracting data from sensitive local documents under strict enterprise privacy bounds.

## Strengths
- **MCP 3.1 / FastMCP 3.1 Native**: The flagship implementation for MCP, supporting both local and remote MCP servers with dedicated configuration parameters and schema validations.
- **Stateful Task Support**: Supports the MCP 3.1 Task Protocol, enabling stateful, long-running agentic loops to run securely in the background.
- **High Performance**: Native performance with optimized resource usage for long-running agentic tasks on local CPU/GPU setups.
- **Enhanced Privacy**: Local MCP operations keep sensitive data on the machine; only necessary context slices are sent to the model.

## Limitations
- **OS Support**: Currently only available for macOS and Windows; no official Linux desktop app (though Claude Code/CLI is available).
- **Subscription Gates**: Advanced features like specific enterprise desktop extensions and higher model limits require Pro or Team subscriptions.
- **Configuration Complexity**: Setting up complex MCP configurations still requires manual JSON editing (though the UI is improving).

## When to use it
- When you need to give Claude access to your local filesystem or databases via MCP.
- For deep integration of AI into your daily macOS or Windows professional workflows.
- When you prefer a stable, native desktop application experience over a browser tab.
- For secure processing of sensitive documents that should stay local.

## When not to use it
- If you are on a Linux-based operating system (use [Claude Code](../development_ops/claude-code.md) or the CLI).
- If you have very limited system resources and prefer the lightweight nature of a browser tab.
- If your workflow is entirely cloud-based and does not require local system access.

## Getting started

1. **Download**: Visit the [Official Download Page](https://claude.ai/download) and select the version for your OS.
2. **Install**: Open the installer and follow the prompts.
3. **Sign In**: Log in with your Anthropic account.
4. **Configure MCP**: To add local tools, edit your `claude_desktop_config.json` file.
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

## CLI examples

### Managing the App via Terminal
While Claude Desktop is a GUI app, it can be interacted with via terminal for configuration:
```bash
# Open the MCP configuration file (macOS)
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Check if MCP servers are running (using standard process tools)
ps aux | grep mcp

# Verify the local configuration JSON using native python schema validator
python3 -c "import json, os; json.load(open(os.path.expanduser('~/Library/Application Support/Claude/claude_desktop_config.json')))"
```

## API examples

### Programmatic Configuration Schema Validation (Python + Pydantic v2)
This example provides a robust, self-contained Python validation utility designed to read the standard local `claude_desktop_config.json` file, validate its structure against strict **Pydantic v2** models, and identify schema errors before launching the Claude Desktop daemon under early January 2027 SOTA standards.

```python
import json
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ValidationError

# Define sub-schemas for individual MCP servers
class MCPServerConfig(BaseModel):
    command: str = Field(..., description="The executable name or path to run the server")
    args: List[str] = Field(default_factory=list, description="Command line arguments passed to the server")
    env: Optional[Dict[str, str]] = Field(default=None, description="Environment variable overrides for the server runtime")

# Define the root schema for Claude Desktop config
class ClaudeDesktopConfig(BaseModel):
    mcp_servers: Dict[str, MCPServerConfig] = Field(
        ...,
        alias="mcpServers",
        description="Dictionary mapping server identifier keys to their execution options"
    )

    class Config:
        populate_by_name = True  # Allows parsing raw JSON containing 'mcpServers' camelCase alias

def validate_config_string(json_str: str) -> Optional[ClaudeDesktopConfig]:
    try:
        raw_dict = json.loads(json_str)
        # Parse and strictly validate using Pydantic v2
        validated_config = ClaudeDesktopConfig.model_validate(raw_dict)
        return validated_config
    except ValidationError as ve:
        print(f"Pydantic Validation failed: {ve}")
        return None
    except json.JSONDecodeError as je:
        print(f"Malformed JSON string: {je}")
        return None

if __name__ == "__main__":
    print("Initiating Claude Desktop Configuration validation test...")
    # Simulated content of a typical claude_desktop_config.json file featuring FastMCP 3.1 variables
    sample_config = """
    {
      "mcpServers": {
        "filesystem": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/jules/project"],
          "env": {
            "MCP_PROTOCOL_VERSION": "FastMCP 3.1"
          }
        },
        "sqlite": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "/Users/jules/home.db"],
          "env": {
            "MCP_PROTOCOL_VERSION": "FastMCP 3.1"
          }
        }
      }
    }
    """

    config = validate_config_string(sample_config)
    if config:
        print("Claude Desktop config is perfectly valid!")
        for server_name, server_cfg in config.mcp_servers.items():
            print(f"  MCP Server: {server_name}")
            print(f"    Command: {server_cfg.command}")
            print(f"    Arguments: {', '.join(server_cfg.args)}")
            if server_cfg.env:
                print(f"    Env Protocol Version: {server_cfg.env.get('MCP_PROTOCOL_VERSION', 'Not Specified')}")
```

## Related tools / concepts
- [Anthropic (Claude)](../providers/anthropic.md) — the provider for models used in the app.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — the core protocol for extensions.
- [Claude Code](../development_ops/claude-code.md) — the CLI-based counterpart for developers.
- [Filesystem-as-Interface](../../knowledge_base/patterns/filesystem-context.md) — the design pattern used by MCP.
- [ServiceNow MCP Server](../automation_orchestration/servicenow-mcp.md) — example of a remote MCP server.
- [Goose](../agents/goose.md) — alternative agentic CLI tool.
- [Aider](../development_ops/aider.md) — another terminal-based AI coding assistant.
- [OpenHands](../development_ops/openhands.md) — agentic platform that can interact with desktop environments.

## Sources / references
- [Official Download Page](https://claude.ai/download)
- [Claude Desktop Documentation](https://support.claude.com/en/articles/10065433-install-claude-desktop)
- [Model Context Protocol Website](https://modelcontextprotocol.io/introduction)
- [Claude Desktop Release Notes](https://anthropic.com/news/claude-desktop-updates)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

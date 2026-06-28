# CliHub

## What it is
CliHub is a generator that connects to a Model Context Protocol (MCP) server and produces a compiled, standalone CLI binary. Each tool exposed by the MCP server is automatically converted into a command within the generated CLI. As of June 2026, it supports **MCP 3.0** and is a primary tool for "freezing" agent capabilities into stable binaries.

## What problem it solves
MCP clients (like **Claude 4.8 Desktop**) are excellent for interactive agent workflows, but they can add significant runtime overhead and deployment complexity for automated tasks. CliHub solves this by converting MCP tools into portable, fast, and scriptable binaries. It allows "one-command" deployment of entire tool suites for both humans and agents, bridging the gap between dynamic agent tools and static DevOps pipelines.

## Where it fits in the stack
**Automation / Orchestration Tool**. It bridges the gap between the emerging MCP ecosystem and traditional shell-native workflows. It effectively allows you to "compile" your agentic tools into standard DevOps-friendly binaries for use by models like **Llama 4 Maverick**.

## Typical use cases
- Packaging complex MCP tool suites (like Jira or GitHub) into static binaries for CI/CD pipelines.
- Running MCP-backed workflows in shell scripts without needing a full MCP client stack.
- Shipping deterministic, versioned tool interfaces to autonomous agent runtimes.
- Reducing latency for tool invocation in high-frequency automation loops.
- Debugging MCP servers directly from the terminal with standard CLI arguments.

## Strengths
- **Simplicity**: One-command codegen flow from MCP endpoint to ready-to-use CLI.
- **Portability**: Generates binaries for multiple target platforms (Linux, macOS, Windows).
- **Efficiency**: Eliminates the overhead of maintaining an active MCP transport session for simple, one-off tool calls.
- **Interoperability**: Supports both HTTP/SSE and stdio MCP transport protocols.
- **Agent-Friendly**: Standard CLI interfaces are easily understood by older agent models or simpler automation scripts.

## Limitations
- **Static Schema**: The generated CLI reflects the MCP server schema at the time of generation; it requires regeneration if the server tools change.
- **Auth Management**: Authentication setup (API tokens, environment variables) must still be handled securely outside of the binary.
- **No Stateful Sessions**: Unlike a live MCP client, each CLI call is independent, which may not be suitable for servers that rely on multi-call state.

## When to use it
- When you want to distribute MCP capabilities in a lightweight, zero-dependency model.
- When building automated DevOps pipelines that need to leverage agent-designed tools.
- When you want to use MCP tools as part of a larger bash or python automation script.
- When debugging a new MCP server and you want a standard CLI interface to test each tool.

## When not to use it
- When a long-running, stateful MCP session is required for advanced multi-step reasoning.
- When dynamic, runtime discovery of new tools is a core part of the workflow.
- When the overhead of an MCP client (like the `mcp-cli` or `claude-code`) is already acceptable.

## Getting started

### Installation
You can install the CliHub generator via Go or by downloading a pre-compiled binary.

```bash
# Install via Go
go install github.com/thellimist/clihub@latest
```

### Basic Usage
Generate a CLI from a local MCP server (stdio):

```bash
# Generate a CLI named 'my-tool' from a Node-based MCP server
clihub generate --name my-tool --command "npx -y @anthropic-ai/mcp-server-atlassian"
```

## CLI examples

### 1. Generating a Remote CLI (SSE)
Connect to a hosted MCP server and generate a local binary:

```bash
clihub generate --name remote-tool --url "https://mcp.example.com/sse"
```

### 2. Invoking a Generated Command
Once generated, you can use the binary like any other CLI tool. If you generated a Jira CLI:

```bash
# List issues using the generated CLI
./jira-cli get_issue --key PROJ-123

# Commands are derived from tool names
./jira-cli search_issues --jql "project = PROJ AND status = Open"
```

### 3. Multi-Platform Build
CliHub can leverage Go's cross-compilation to build for different environments:

```bash
GOOS=linux GOARCH=amd64 clihub generate --name jira-linux --command "..."
```

## API examples

### 1. Programmatic Generation (Go)
Integrate CliHub's generation logic into your own Go-based developer tools:

```go
import "github.com/thellimist/clihub/pkg/generator"

func main() {
    config := generator.Config{
        Name:    "my-tool",
        Command: "npx -y @some/mcp-server",
    }
    generator.Generate(config)
}
```

### 2. Wrapping CliHub in Python
Using Python to manage versioning and distribution of generated binaries:

```python
import subprocess

def update_tool(name, mcp_command):
    subprocess.run(["clihub", "generate", "--name", name, "--command", mcp_command])
    print(f"Updated {name} to latest MCP schema.")

update_tool("kb-tool", "python3 scripts/mcp_kb_server.py")
```

### 3. Calling via n8n
Instead of configuring complex MCP nodes, use the "Execute Command" node to call a CliHub binary:
```json
{
  "node": "Execute Command",
  "parameters": {
    "command": "./jira-cli get_issue --key={{$json.key}}"
  }
}
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) - The underlying protocol.
- [MCP Registry](mcp-registry.md) - For finding MCP servers to compile.
- [ServiceNow MCP Server](servicenow-mcp.md) - A target for compilation.
- [Atlassian Jira MCP Implementations](atlassian-jira-mcp.md) - A target for compilation.
- [Playwright MCP Server](playwright-mcp.md) - A target for compilation.
- [Agent Protocols](../../knowledge_base/agent_protocols.md) - Conceptual background.
- [Claude Code](../development_ops/claude-code.md) - A high-level consumer of MCP.
- [n8n](../../services/n8n.md) - Orchestrator that can use generated binaries.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Target model for static binaries.

## Sources / References
- [CliHub Repository](https://github.com/thellimist/clihub)
- [I Made MCP 94% Cheaper (And It Only Took One Command)](https://kanyilmaz.me/2026/02/23/cli-vs-mcp.html)
- [MCP Official Documentation](https://modelcontextprotocol.io/)

## Contribution Metadata

- Last reviewed: 2026-06-28
- Confidence: high

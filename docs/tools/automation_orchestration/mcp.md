# Model Context Protocol (MCP)

## What it is
The Model Context Protocol (MCP) is an open-source standard designed to facilitate secure, two-way, capability-negotiated connections between LLM reasoning engines and local or remote data sources, workflows, and tools. Developed originally by Anthropic and rapidly adopted as a cross-industry standard, the protocol defines how AI models interact with the physical and digital resources around them. As of late November/December 2026, **MCP 3.1** and **FastMCP 3.1** are the active production standards, offering native support for the most advanced reasoning models including **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, **Gemma 3**, and **Qwen 3.6**.

## What problem it solves
It eradicates the "integration bottleneck" of AI engineering. Historically, developers had to write customized wrapper code for every single tool-model combination, which led to fragile, non-reusable integrations. MCP provides a unified JSON-RPC-based transport schema, allowing any compatible server (e.g., local filesystems, postgres databases, web scrapers) to plug instantly into any compatible client (e.g., Claude Desktop, Roo Code, Vellum, or customized agent daemons). This solves tool fragmentation and accelerates agent development across both local and enterprise-scale workspaces.

## Where it fits in the stack
**Category**: Core Protocol / Automation & Orchestration / Pattern. It serves as the standard "Reasoning-to-Resource Glue" layer, bridging the gap between frontier inference models and local/remote host environments (API gateways, servers, execution sandboxes).

## Typical use cases
- **Secure File Orchestration**: Granting an IDE agent fine-grained access to local project filesystems under strict permission boundaries.
- **Enterprise Data Federation**: Bridging complex relational databases (PostgreSQL, BigQuery) with models via dynamically queried schemas.
- **Unified Agent Tools**: Building an MCP tool once and sharing it seamlessly across multiple client platforms (e.g., [Goose](../agents/goose.md), [Cline](../agents/cline.md), and custom workspace daemons).
- **Heterogeneous Agent Chains**: Running complex pipelines where **Claude 5.1** coordinates high-level planning, while **Gemma 3** or **Qwen 3.6** executes local scripts via a fast, secure MCP transport.

## Strengths
- **Standardized Transport**: Relies on robust, lightweight transport schemas like Stdio, SSE (Server-Sent Events), and advanced micropayment-enabled protocols.
- **Vendor Agnostic**: Supported by key players across the frontier model spectrum, minimizing platform lock-in.
- **Dynamic Capabilities**: Clients and servers negotiate capabilities (Tools, Prompts, Resources) during initial handshake steps, preventing unsupported action errors.
- **Rich Developer Tooling**: Includes standard debugging tools like the official MCP Inspector for rapid iteration.

## Limitations
- **Overhead for Small Tasks**: Implementing an asynchronous JSON-RPC protocol can feel like overkill for trivial scripts that can be executed directly via a standard CLI.
- **Complex Auth & Access Control**: While the protocol supports capability negotiation, authenticating and auditing granular multi-user permissions across multiple servers remains a significant systems architecture challenge.
- **Stateless Nature**: The core protocol does not manage long-term conversation history or complex session states natively; state management must be solved by the client application layer.

## When to use it
- To expose custom APIs, databases, or local filesystems to frontier models (Claude 5.1, GPT-5.5) inside a standardized, secure sandbox.
- When building tools and agent extensions that you intend to distribute across the broader open-source ecosystem.
- For high-reliability, agentic RAG setups where LLMs must dynamically discover, query, and structure relevant local and remote data assets.

## When not to use it
- For static, hardcoded tool functions inside a single, dedicated app where standard API library calls are faster and less complex.
- If the target reasoning engine lacks native JSON-RPC transport capabilities or an adapter wrapper.
- When security boundaries dictate absolute shell isolation and standard sandboxed command line tools are preferred.

## Getting started

### MCP Architecture
MCP enforces a strict client-server protocol. The client (such as Claude Desktop or Roo Code) establishes a connection with a dedicated MCP server over standard input/output (Stdio) or HTTP with Server-Sent Events (SSE).

### Example: Exposing Local Directories in Claude Desktop
To add standard filesystem tools to Claude Desktop, configure your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "local-filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/user/workspace/allowed-folder"
      ]
    }
  }
}
```

### Developing a FastMCP 3.1 Compliant Server
With FastMCP 3.1, server definitions are highly streamlined. Below is a TypeScript example demonstrating how to declare and serve tools:

```typescript
import { FastMCP } from "fastmcp";

// Initialize FastMCP server with late 2026 specs
const server = new FastMCP({
  name: "enterprise-weather-tracker",
  version: "3.1.0"
});

// Register a basic tool
server.addTool({
  name: "get_current_temp",
  description: "Retrieve real-time temperature data for a specific location",
  parameters: {
    type: "object",
    properties: {
      location: { type: "string", description: "City and state/country" }
    },
    required: ["location"]
  },
  execute: async ({ location }) => {
    // Business logic to contact external API
    return { temperature: "22C", status: "Sunny", location };
  }
});

// Launch transport listener (Stdio by default)
server.start();
```

## CLI examples
MCP features standard terminal utilities to audit, inspect, and verify server handshakes:

```bash
# Launch the late 2026 MCP Inspector tool on a local Javascript server
npx @modelcontextprotocol/inspector node my-mcp-server.js

# Query tools directly via terminal stdio by feeding a standard JSON-RPC request
echo '{"jsonrpc":"2.0","method":"tools/list","id":1,"params":{}}' | node my-mcp-server.js

# Connect a headless client utility to inspect a local server session
mcp-cli connect stdio --command node --args my-mcp-server.js
```

## API examples
MCP communication relies entirely on structured JSON-RPC 2.0 payloads. Developers can utilize Python to interact with, query, and strictly validate MCP tool execution data. Below is a Python script utilizing **Pydantic v2** to validate tool responses:

### 1. Python: Validate MCP Tool Calls and Handshakes
```python
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError

# Define strict JSON-RPC 2.0 and MCP schemas
class MCPToolCallRequest(BaseModel):
    jsonrpc: str = Field("2.0", pattern="^2\\.0$")
    method: str = Field("tools/call", pattern="^tools/call$")
    params: Dict[str, Any] = Field(..., description="Target tool name and arguments payload")
    id: int = Field(..., description="Unique Request ID")

class ToolCallResult(BaseModel):
    tool_name: str = Field(..., description="The name of the executed tool")
    success: bool = Field(True, description="Execution success state")
    output: Dict[str, Any] = Field(..., description="Structured return values")

# Test validation of an MCP tool call request
def validate_client_request(raw_payload: str) -> Optional[MCPToolCallRequest]:
    try:
        data = json.loads(raw_payload)
        return MCPToolCallRequest.model_validate(data)
    except ValidationError as e:
        print(f"Schema violation detected: {e}")
        return None
    except json.JSONDecodeError:
        print("Invalid raw JSON payload.")
        return None

if __name__ == "__main__":
    # Example client call payload
    test_payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_current_temp",
            "arguments": {
                "location": "Boston, MA"
            }
        },
        "id": 42
    })

    print("Parsing client request...")
    request = validate_client_request(test_payload)
    if request:
        print(f"Validated request {request.id}. Method: {request.method}")
        print(f"Target Tool: {request.params.get('name')} | Arguments: {request.params.get('arguments')}")
    else:
        print("Validation process failed.")
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Standard CLI companion using MCP natively.
- [Roo Code](../agents/roo-code.md) — Highly extensible IDE agent utilizing MCP 3.1.
- [MCP Registry](mcp-registry.md) — Central directory for community and enterprise servers.
- [Data Copilot MCP Tooling](../../knowledge_base/patterns/data-copilot-mcp-tooling.md) — Enterprise orchestration pattern.
- [Cline](../agents/cline.md) — Multi-model IDE agent with deep protocol support.
- [n8n](../../services/n8n.md) — Multi-system visual workflow and trigger integrator.
- [Vellum](vellum.md) — Comprehensive macOS assistant utilising desktop MCP integrations.
- [Chronos MCP](chronos-mcp.md) — Standardized calendar, scheduling, and email orchestration tool.

## Sources / references
- [Model Context Protocol Official Site](https://modelcontextprotocol.io/)
- [Anthropic Developer Documents: MCP Concepts](https://modelcontextprotocol.io/docs/concepts/architecture)
- [Official Model Context Protocol GitHub SDKs](https://github.com/modelcontextprotocol)
- [LocalLLaMA Community Critiques of MCP Architecture](https://www.reddit.com/r/LocalLLaMA/comments/1uvaqxp/mcp_is_bad/)

## Contribution Metadata
- Last reviewed: 2026-12-25
- Confidence: high

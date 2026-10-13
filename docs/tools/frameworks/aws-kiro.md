# AWS Kiro

## What it is
AWS Kiro is an open-source, lightweight agent-client protocol and runtime layer designed to cleanly decouple AI agents from the editors, IDEs, and local user environments they interact with. As of early January 2027, Kiro standardizes message formats, FastMCP 3.1 capabilities handshakes, and bidirectional file/terminal synchronization, allowing software engineering agents powered by models like **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra** to run inside any Kiro-compliant host application without custom adapter code.

## What problem it solves
Historically, AI software engineering agents were tightly-coupled to specific environments—resulting in custom VS Code extensions, separate Neovim configurations, and non-reusable command-line runners. When a new IDE or a new agent is released, authors have to build redundant glue code. AWS Kiro solves this fragmentation by defining a standardized protocol, letting any developer host any Kiro agent instantly with unified transport primitives.

## Where it fits in the stack
**Agent Client & Interoperability Layer**. It operates as a communication standard between frontend user interfaces (IDEs, web consoles, shell terminals) and backend agent runtimes, complementing standard protocols like LSP (Language Server Protocol) and FastMCP 3.1 (Model Context Protocol).

## Typical use cases
- **Multi-Editor Agent Deployments**: Running a single, advanced software engineering agent across multiple environments like VS Code, Cursor, and Vim.
- **Remote Developer Workspace Integration**: Deploying coding agents in cloud-hosted workspaces while controlling them from local editor interfaces.
- **Agent Capabilities Negotiation**: Determining at startup whether a newly connected agent supports terminal commands, multi-file editing, or search filters under FastMCP 3.1 Task Protocol definitions.
- **Bidirectional Terminal Streaming**: Creating a secure, buffered pipe to stream interactive terminal states and user approvals between editors and autonomous agents.

---

## Architecture & Decoupled Transport Flow

AWS Kiro introduces a bidirectional, JSON-RPC 2.0 communication bus between host IDE clients and remote/local agent runtime engines.

```
+-----------------------------------------------------------------------------------+
|                            EDITOR HOST APPLICATION                                |
|  +-----------------------+   +-----------------------+   +---------------------+  |
|  |  VS Code / Cursor UI  |   | Terminal Panel / PTY  |   | File Diff Viewer    |  |
|  +-----------+-----------+   +-----------+-----------+   +----------+----------+  |
+--------------|---------------------------|--------------------------|-------------+
               | (capabilities)            | (terminal stream)        | (file patch)
               v                           v                          v
+-----------------------------------------------------------------------------------+
|                           AWS KIRO PROTOCOL TRANSPORT LAYER                       |
|  +-----------------------------------------------------------------------------+  |
|  | Kiro JSON-RPC 2.0 Message Router & Capabilities Handshake Engine             |  |
|  |  +--------------------------------+   +----------------------------------+  |  |
|  |  | Workspace Capabilities Schema  |   | FastMCP 3.1 Task Protocol Bridge |  |  |
|  |  +---------------+----------------+   +----------------+-----------------+  |  |
|  +------------------|-------------------------------------|--------------------+  |
+---------------------|-------------------------------------|-----------------------+
                      |                                     |
                      v                                     v
+-----------------------------------------------------------------------------------+
|                             BACKEND AGENT RUNTIME                                 |
|  +-------------------+       +-------------------+       +---------------------+  |
|  | LLM Planning Engine       | Tool Execution Loop |    | Vector Memory Index |  |
|  +-------------------+       +-------------------+       +---------------------+  |
+-----------------------------------------------------------------------------------+
```

### Agent Client Protocol Comparison Matrix

| Feature / Dimension | AWS Kiro Protocol | Language Server Protocol (LSP) | MCP 3.1 / FastMCP | Custom IDE Plugin API |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | AI Agent <-> Editor Transport| Code Intelligence / AST | LLM <-> External Tools | Specific Editor UI |
| **Protocol Foundation** | JSON-RPC 2.0 | JSON-RPC 2.0 | JSON-RPC 2.0 / SSE | Native JS / Lua / Python |
| **Agent Capability Negotiation**| Native Built-in | Dynamic Capabilities | Server Info Tools | Static Package Manifest |
| **Terminal Sync** | Bidirectional Stream | N/A | Exposed as Tools | Direct Native PTY |
| **Multi-Editor Portability**| High (Universal) | High (Universal) | High (Universal) | Low (Single Editor) |

---

## FastMCP 3.1 Production Implementation & Pydantic v2 Schema

Below is a complete, runnable **FastMCP 3.1** server that implements the **AWS Kiro** handshake and message routing specification with strict **Pydantic v2** models.

```python
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict, ValidationError
from fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP(
    title="AWS Kiro Protocol Gateway",
    version="3.1.0",
    description="FastMCP 3.1 server handling AWS Kiro client initialization and tool execution."
)

# Pydantic v2 Schema Declarations
class WorkspaceCapabilities(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    file_edit: bool = Field(default=False, alias="fileEdit", description="Whether the host supports direct file editing")
    terminal_exec: bool = Field(default=False, alias="terminalExec", description="Whether the host supports terminal execution")
    user_approval_required: bool = Field(default=True, alias="userApprovalRequired", description="Whether user confirmation is required")
    fastmcp_task_support: bool = Field(default=True, alias="fastmcpTaskSupport", description="Support for FastMCP 3.1 Task Protocol")

class KiroInitializeParams(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    task_id: str = Field(..., alias="taskId", description="FastMCP 3.1 correlation identifier")
    client_name: str = Field(..., alias="clientName", description="Name of the editor host application")
    protocol_version: str = Field(default="1.1.0", alias="protocolVersion", description="Kiro protocol version")
    capabilities: WorkspaceCapabilities = Field(..., description="Workspace capabilities supported by host")

class KiroInitializeResult(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    task_id: str = Field(..., alias="taskId")
    agent_name: str = Field(..., alias="agentName")
    status: str = Field(..., description="Negotiation status ('ready', 'unsupported')")
    negotiated_capabilities: WorkspaceCapabilities = Field(..., alias="negotiatedCapabilities")
    timestamp: str = Field(..., description="ISO completion timestamp")

# FastMCP 3.1 Server Tools
@mcp.tool(
    name="kiro_initialize_handshake",
    description="Processes an AWS Kiro client handshake and negotiates capabilities."
)
async def kiro_initialize_handshake(params: KiroInitializeParams) -> KiroInitializeResult:
    # Negotiate capabilities: Ensure agent matches host settings
    negotiated = WorkspaceCapabilities(
        fileEdit=params.capabilities.file_edit,
        terminalExec=params.capabilities.terminal_exec,
        userApprovalRequired=True,
        fastmcpTaskSupport=params.capabilities.fastmcp_task_support
    )

    return KiroInitializeResult(
        taskId=params.task_id,
        agentName="AWS-Kiro-Agentic-Pro",
        status="ready",
        negotiatedCapabilities=negotiated,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

if __name__ == "__main__":
    mcp.run()
```

---

## Strengths
- **Clean Decoupling**: Fully separates the developer interface from complex, compute-heavy agent logical loops.
- **JSON-RPC Foundation**: Utilizes lightweight, battle-tested transport specifications for fast message passing and easy debugging.
- **Standardized Handshaking**: Includes structured capabilities negotiations for dynamic feature toggles at runtime.
- **Unified Security Model**: Explicitly defines transport-level access controls and user confirmation schemas.

## Limitations
- **Early Stage Adoption**: Editor ecosystems are still developing native Kiro clients, requiring separate plugin shells.
- **Fringe Terminal Features**: Highly interactive or stateful custom terminal applications can be complex to sync via JSON-RPC.
- **Slight Transport Overhead**: For extremely fast local operations, Kiro's serialization can add negligible microseconds compared to direct subprocess calls.

---

## When to use it
- When you are developing a coding or debugging agent and want to ensure it is immediately compatible with multiple IDEs and code editors.
- When building a distributed developer stack where the AI agent runs on powerful cloud clusters while the developer uses a local IDE.
- For standardizing human-in-the-loop interactive control over file system modifications.

## When not to use it
- When building a completely closed, proprietary developer assistant that is permanently coupled to a single, proprietary interface.
- For simple, non-interactive scripting agents that only require a one-way CLI execution flow and do not sync file state.
- In highly resource-constrained embedded microcontrollers where JSON-RPC serialization overhead cannot be tolerated.

---

## Getting started
1. **Add AWS Kiro to your codebase**: Install the official runtime package:
   ```bash
   pip install aws-kiro pydantic>=2.0.0
   ```
2. **Launch a Kiro Server**: Start the local Kiro loop inside your custom agent:
   ```python
   from aws_kiro import KiroServer

   server = KiroServer(port=9090)
   server.start()
   ```
3. **Establish Capabilities**: Define what tool execution commands your agent supports in JSON:
   ```json
   {
     "jsonrpc": "2.0",
     "method": "initialize",
     "params": {
       "clientName": "VSCode-Host",
       "capabilities": {
         "workspace": {"fileEdit": true, "terminalExec": true}
       }
     },
     "id": 1
   }
   ```

---

## Operational Hardening, Deployment & Troubleshooting

### Operational Safety & Security Guidelines
1. **Enforce Approval Boundaries**: Set `userApprovalRequired: true` by default in all Kiro handshake configurations for terminal commands and file destructive actions (`git reset`, `rm -rf`).
2. **Transport Encryption**: For remote Kiro connections (e.g., local IDE connecting to remote cloud agent), route JSON-RPC traffic over TLS or an SSH tunnel (`ssh -L 9090:localhost:9090 user@remote-agent-host`).
3. **Sanitize Messages**: Enforce JSON schema validation via Pydantic v2 before processing incoming RPC payloads to prevent remote execution exploits or buffer overruns.

### Troubleshooting Guide

| Issue / Error | Root Cause | Remediation Command / Solution |
| :--- | :--- | :--- |
| `JSON-RPC error -32600: Invalid Request` | Malformed RPC message structure | Validate request payload against `KiroInitializeParams` schema |
| `Handshake Timeout (9090 Unreachable)` | Kiro backend agent process crashed or port bound | Check port binding with `lsof -i :9090` and review server logs |
| `Capability Mismatch: terminalExec Disabled` | Host editor rejected terminal stream capability | Set `terminalExec: false` in agent runtime configuration |
| `FastMCP Bridge Desynchronization` | Mismatch in FastMCP 3.1 task protocol version | Upgrade `fastmcp` package to 3.1.0+ on both host and agent |

---

## CLI examples
AWS Kiro provides a diagnostic command-line runner to inspect local servers, audit capability handshakes, and debug JSON-RPC streams.

```bash
# Start a Kiro developer-agent mock server for diagnostics
kiro-cli start-server --port 9090 --mock-agent coding

# Ping and audit capabilities negotiation for an active Kiro server
kiro-cli ping --url "http://localhost:9090" --handshake

# Stream live JSON-RPC messages and event payloads for auditing
kiro-cli stream --url "http://localhost:9090" --verbose
```

---

## API examples

### Python JSON-RPC Capability Validation with AWS Kiro & Pydantic v2
This API example demonstrates how to validate Kiro capabilities negotiation and handshaking messages using strict **Pydantic v2** structures and FastMCP 3.1 task parameters.

```python
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict

# Define schema for Kiro client workspace capabilities
class WorkspaceCapabilities(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    file_edit: bool = Field(default=False, alias="fileEdit", description="Whether the host supports direct file editing")
    terminal_exec: bool = Field(default=False, alias="terminalExec", description="Whether the host supports terminal command execution")
    user_approval_required: bool = Field(default=True, alias="userApprovalRequired", description="Whether user confirmation is needed for write actions")
    fastmcp_task_support: bool = Field(default=True, alias="fastmcpTaskSupport", description="Support for FastMCP 3.1 Task Protocol")

# Define schema for Kiro initial handshake message
class KiroInitializeParams(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    client_name: str = Field(..., alias="clientName", description="Name of the editor host application")
    protocol_version: str = Field(default="1.1.0", alias="protocolVersion", description="The Kiro protocol version used")
    capabilities: WorkspaceCapabilities = Field(..., description="Workspace features supported by the editor host")

# Define schema for the Kiro initialization response
class KiroInitializeResult(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    agent_name: str = Field(..., alias="agentName", description="Name of the responsive AI agent")
    status: str = Field(..., description="Verification status, e.g., 'authenticated' or 'ready'")
    negotiated_capabilities: WorkspaceCapabilities = Field(..., alias="negotiatedCapabilities")

def process_kiro_handshake(raw_json_payload: str) -> KiroInitializeResult:
    # Parse and validate incoming client handshake
    data = json.loads(raw_json_payload)
    params = KiroInitializeParams.model_validate(data)

    # Simulated negotiation: If client lacks terminal execution, ensure agent matches it
    negotiated_terminal = params.capabilities.terminal_exec

    negotiated = WorkspaceCapabilities(
        fileEdit=params.capabilities.file_edit,
        terminalExec=negotiated_terminal,
        userApprovalRequired=True,
        fastmcpTaskSupport=params.capabilities.fastmcp_task_support
    )

    result = KiroInitializeResult(
        agentName="AWS-Kiro-Developer-Pro",
        status="ready",
        negotiatedCapabilities=negotiated
    )
    return result

if __name__ == "__main__":
    # Simulate a VS Code client handshake request
    handshake_payload = {
        "clientName": "VSCode-Host-Client",
        "protocolVersion": "1.1.0",
        "capabilities": {
            "fileEdit": True,
            "terminalExec": False,
            "userApprovalRequired": True,
            "fastmcpTaskSupport": True
        }
    }

    raw_request = json.dumps(handshake_payload)
    negotiated_state = process_kiro_handshake(raw_request)

    print("--- AWS Kiro Capabilities Negotiation Passed ---")
    print(f"Connected Agent: {negotiated_state.agent_name}")
    print(f"Negotiation Status: {negotiated_state.status}")
    print(f"File Edit Support: {negotiated_state.negotiated_capabilities.file_edit}")
    print(f"Terminal Exec Support: {negotiated_state.negotiated_capabilities.terminal_exec}")
```

---

## Related tools / concepts
- [Cline](../agents/cline.md) — Advanced developer agent that communicates with IDEs using structured client protocols.
- [Windsurf](../development_ops/windsurf.md) — Next-generation IDE designed with high-interoperability agent systems.
- [Claude Code](../development_ops/claude-code.md) — CLI coding agent that benefits from decoupled client protocols.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open protocol defining how clients expose tools and context to LLM agents.
- [OpenAI Agents SDK](../frameworks/openai-agents-sdk.md) — Framework for building orchestrations that require Kiro transport bridges.
- [Google ADK](../frameworks/google-adk.md) — Framework standardizing robot and device controls for agents.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Architectural pattern for multi-agent knowledge engineering.
- [AutoGen](../frameworks/autogen.md) — Conversational agent-framework benefiting from clean transport abstraction layers.

---

## Sources / references
- [Kiro Agent Client Protocol Specifications and Editor Decoupling standards](https://thenewstack.io/kiro-agent-client-protocol/)
- [JSON-RPC 2.0 Specifications](https://www.jsonrpc.org/specification)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Vault MCP

## What it is
The Vault MCP (Model Context Protocol) server is a production-grade interface that allows AI agents to securely interact with HashiCorp Vault. As of July 2026, it fully supports the **MCP 3.0 Task Protocol**, providing standardized tools for managing Key-Value (KV) secrets, policies, and namespaces. This enables frontier models like [Gemma 3](../ai_knowledge/local_llms.md) and [Claude 4.8 Opus](../providers/anthropic.md) to perform secure credential management tasks within a unified agentic framework.

## What problem it solves
It solves the "secret sprawl" and insecure credential handling common in agentic workflows by providing a standardized, auditable bridge to [HashiCorp Vault](hashicorp-vault.md). It allows AI assistants to retrieve, rotate, and manage sensitive tokens or API keys without requiring manual intervention or hardcoding secrets in application environments. By utilizing the **MCP 3.0** standard, it ensures consistent behavior across different agent platforms.

## Where it fits in the stack
**Automation / Orchestration**. It functions as the security and secret management interface within the **Agentic** layer, connecting AI-driven workflows to the underlying [HashiCorp Vault](hashicorp-vault.md) security infrastructure.

## Typical use cases
- **Automated Secret Rotation**: An agent identifies an expiring API key and uses Vault MCP to generate and store a new one.
- **Dynamic Access Control**: Having an agent draft and apply HCL policies for temporary development environments via natural language.
- **Credential Injection for Developers**: Allowing terminal-based agents like [Claude Code](../development_ops/claude-code-setup.md) or [Aider](../development_ops/aider.md) to securely fetch dev-stage secrets.
- **Security Posture Auditing**: Using an agent to perform health checks and verify policy compliance across multiple Vault namespaces.
- **Workflow-Specific Credentials**: Providing [n8n](../../services/n8n.md) or [AirOps](airops.md) workflows with just-in-time credentials for restricted API access.

## Strengths
- **KV v1 and v2 Native**: Automatically detects and handles both versions of the Vault Key-Value secrets engine.
- **Namespace Aware**: Full compatibility with Vault Enterprise namespaces, essential for complex organizational structures.
- **MCP 3.0 Compliant**: Implements the latest Task Protocol for improved reliability in multi-step agentic reasoning.
- **Built on hvac**: Leverages the robust and thread-safe `hvac` Python library for all Vault interactions.
- **Conversationally Driven**: Enables complex security operations to be performed using natural language prompts.

## Limitations
- **Engine Scope**: Focuses primarily on KV and Policy engines; support for more advanced engines (e.g., Transit, PKI) may require custom extensions.
- **Bootstrapping**: Requires an initial Vault token or AppRole with sufficient permissions to be provided to the MCP server environment.
- **Audit Responsibility**: While it logs actions, organizations must ensure Vault's native auditing is enabled to track agent-initiated changes.

## When to use it
- When your infrastructure relies on [HashiCorp Vault](hashicorp-vault.md) and you want to enable AI-assisted security operations.
- For building autonomous agents that require secure, time-limited access to enterprise credentials.
- When you need to manage complex Vault policies or secrets through a conversational interface like [Claude Desktop](../providers/anthropic.md) or [Cursor](../development_ops/cursor.md).

## When not to use it
- In environments where AI agents are strictly prohibited from interacting with sensitive infrastructure.
- For high-frequency application-level secret retrieval (applications should use the Vault REST API or `hvac` directly).
- If you are using a different secret management provider (e.g., 1Password or AWS Secrets Manager) without a compatible MCP bridge.

## Getting started

### 1. Installation
The Vault MCP server is typically installed via `pip`:

```bash
pip install vault-mcp
```

### 2. Basic Configuration
Run the server by providing your [HashiCorp Vault](hashicorp-vault.md) address and a valid token via environment variables:

```bash
export VAULT_ADDR="https://vault.example.com:8200"
export VAULT_TOKEN="hvs.your-secure-token"
python -m vault_mcp
```

### 3. Client Integration
Configure your MCP client (e.g., Claude Desktop) to connect to the running server.

## CLI examples

```bash
# Verify connection and server version
python -m vault_mcp --version

# Run the server in a specific enterprise namespace
VAULT_NAMESPACE="admin/production" python -m vault_mcp

# List all tools exposed to the agent
mcp-client list-tools --server-cmd "python -m vault_mcp"
```

## API examples

### Extending Vault MCP with FastMCP 3.0
You can create specialized security tools by extending the core server logic:

```python
from vault_mcp import VaultServer
from mcp.server.fastmcp import FastMCP

# Initializing a custom security extension using July 2026 standards
mcp = FastMCP("vault-extension-pro")

@mcp.tool()
async def check_vault_sealing_status() -> str:
    """Check if the Vault instance is currently sealed or unsealed."""
    # Logic utilizing the internal hvac client
    return "Vault is currently unsealed and operational."

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [HashiCorp Vault](hashicorp-vault.md) — The underlying security and secrets engine.
- [Model Context Protocol (MCP)](mcp.md) — The communication standard for AI agents.
- [Gemma 3](../ai_knowledge/local_llms.md) — Frontier open model with native MCP 3.0 support.
- [Claude Code](../development_ops/claude-code-setup.md) — Terminal-based agent that leverages security MCPs.
- [n8n](../../services/n8n.md) — Often integrated with Vault for secure workflow automation.
- [AirOps](airops.md) — Enterprise AI platform that can orchestrate secure tasks.
- [Authentik](../../services/authentik.md) — For managing identity-based access to the MCP server.
- [Axiom Guardian](../development_ops/axiom-guardian.md) — For providing additional security guardrails for agent actions.

## Sources / references
- [Vault MCP GitHub Repository](https://github.com/democratize-technology/vault-mcp)
- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [hvac Python Client Library](https://hvac.readthedocs.io/)
- [HashiCorp Vault KV Secrets Engine Guide](https://developer.hashicorp.com/vault/docs/secrets/kv)
- [MCP 3.0 Task Protocol Spec](https://modelcontextprotocol.io/docs/concepts/tasks)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high

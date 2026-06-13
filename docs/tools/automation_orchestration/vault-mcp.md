# Vault MCP

## What it is
The Vault MCP (Model Context Protocol) server is a production-ready interface that allows AI agents to securely interact with HashiCorp Vault. It provides tools for managing KV secrets, policies, and namespaces, enabling models like [Claude 4.8 Opus](../providers/anthropic.md) to perform secure secret management tasks.

## What problem it solves
It solves the "secret sprawl" problem in agentic workflows by providing a standardized, secure way for AI assistants to retrieve or manage credentials without manual CLI or API intervention. It allows agents to generate policies, rotate secrets, and check the health of security infrastructure through a conversational interface.

## Where it fits in the stack
**Automation / Orchestration**. It functions as the security and secret management interface within the **Agentic** layer.

## Typical use cases
- **Automated Secret Rotation**: Asking an agent to rotate database credentials and update the corresponding Vault entry.
- **Dynamic Policy Generation**: Having an agent draft and apply HCL policies for a new microservice.
- **Credential Retrieval**: Allowing a developer-facing agent (e.g., [Claude Code](../development_ops/claude-code-setup.md)) to fetch temporary development secrets.
- **Security Auditing**: Performing health checks and verifying policy compliance across multiple Vault namespaces.

## Strengths
- **KV v1 and v2 Support**: Automatically detects and supports both versions of the Key-Value secrets engine.
- **Namespace Awareness**: Fully compatible with Vault Enterprise namespaces.
- **Policy Management**: Enables complete lifecycle management of Vault policies using natural language.
- **Enterprise-Grade**: Built using the robust `hvac` Python client for thread-safe and secure operations.

## Limitations
- **Scope Restriction**: Primarily focused on the KV and Policy engines; does not yet support all Vault secret engines (e.g., PKI, Transit) natively.
- **Token Sensitivity**: Requires providing an initial Vault token or AppRole with sufficient permissions to the MCP server environment.
- **Statefulness**: Changes made by the agent are immediate and permanent within the Vault instance.

## When to use it
- When your infrastructure utilizes HashiCorp Vault for secret management and you want AI-assisted control.
- When building autonomous agents that need to securely access or manage environment-specific credentials.
- When you need to generate complex Vault policies via natural language prompts.

## When not to use it
- When using a different secret management provider (e.g., AWS Secrets Manager, 1Password) without a compatible bridge.
- In environments where AI agents are strictly prohibited from accessing any sensitive or privileged infrastructure.
- For managing high-traffic, real-time application secret retrieval (apps should use the Vault API directly).

## Getting started
Vault MCP requires a running HashiCorp Vault instance and a valid authentication token.

### 1. Installation
```bash
pip install vault-mcp
```

### 2. Basic Configuration
Run the server using environment variables for authentication:
```bash
export VAULT_ADDR="https://vault.example.com:8200"
export VAULT_TOKEN="hvs.your-token-here"
python -m vault_mcp
```

## CLI examples
The following commands demonstrate how to interact with the Vault MCP server.

```bash
# Verify the server version and connection
python -m vault_mcp --version

# Run the server in a specific Vault namespace
VAULT_NAMESPACE="admin/production" python -m vault_mcp

# List available tools exposed by the MCP server
mcp-client list-tools --server-cmd "python -m vault_mcp"
```

## API examples
The Vault MCP server utilizes the `hvac` client internally. You can extend its capabilities using the Python MCP SDK.

```python
from vault_mcp import VaultServer
from mcp.server.fastmcp import FastMCP

# Initializing a custom Vault MCP server using FastMCP 3.0
mcp = FastMCP("vault-extension")

@mcp.tool()
async def check_vault_health() -> str:
    """Check the sealing status and health of the Vault instance."""
    # Internal logic using hvac client
    return "Vault is unsealed and healthy."

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Model Context Protocol (MCP)](mcp.md) — The standard for agent-tool communication.
- [HashiCorp Vault](https://www.vaultproject.io/) — The underlying secrets engine.
- [ServiceNow MCP](servicenow-mcp.md) — For orchestrating IT service management.
- [Authentik](../../services/authentik.md) — For identity and access management.
- [Claude Code](../development_ops/claude-code-setup.md) — A primary consumer of security-focused MCPs.
- [n8n](../../services/n8n.md) — For building complex security automation workflows.
- [Vikunja MCP](vikunja-mcp.md) — Example of a task-oriented MCP.
- [FastMCP 3.0](mcp.md) — The preferred framework for building MCP servers in 2026.

## Sources / references
- [Vault MCP GitHub Repository](https://github.com/democratize-technology/vault-mcp)
- [HashiCorp Vault KV Secrets Engine Documentation](https://developer.hashicorp.com/vault/docs/secrets/kv)
- [hvac Python Client Documentation](https://hvac.readthedocs.io/)
- [Official MCP Documentation](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high

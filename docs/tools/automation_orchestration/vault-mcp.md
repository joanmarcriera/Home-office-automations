# Vault MCP Server

## What it is
A production-ready HashiCorp Vault Model Context Protocol (MCP) server that provides a comprehensive interface to Vault's KV secrets engine and policy management.

## What problem it solves
It enables AI assistants to securely interact with HashiCorp Vault for managing secrets and policies, reducing the need for manual API calls or CLI interactions for secret management tasks.

## Where it fits in the stack
**Infra / Tool**. It provides the security and secret management interface for AI agents.

## Typical use cases
- Creating, reading, updating, and deleting secrets in Vault's KV engine.
- Managing Vault policies (ACLs).
- Performing health checks and verifying Vault configurations.
- Generating policy strings for specific access requirements.

## Strengths
- **Full Secret Management**: Supports both KV v1 and v2 with automatic detection.
- **Policy Management**: Enables agents to manage access control policies.
- **Enterprise Ready**: Supports namespaces for Vault Enterprise deployments.
- **Security-First**: Thread-safe client management, detailed error handling, and permission checks.

## Limitations
- Coverage depends on the supported tool set (primarily KV and Policy engines).
- Requires a running HashiCorp Vault instance and a valid token.

## When to use it
- When your organization uses HashiCorp Vault and you want AI assistants to manage or retrieve secrets securely.
- When you need an MCP-native way to handle secrets in your agent workflows.

## When not to use it
- When you do not use HashiCorp Vault for secret management.
- When governance rules prohibit AI assistants from accessing secret management systems.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (software); Vault usage/licensing still applies.
- **Self-hostable**: Yes

## Getting started

Vault MCP requires a running HashiCorp Vault instance and can be configured to use either a token or AppRole for authentication.

### 1. Installation
```bash
pip install vault-mcp
```

### 2. Configuration (Claude Desktop)
Add the server to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "vault": {
      "command": "python",
      "args": ["-m", "vault_mcp"],
      "env": {
        "VAULT_ADDR": "https://vault.example.com:8200",
        "VAULT_TOKEN": "your-vault-token",
        "VAULT_NAMESPACE": "admin"
      }
    }
  }
}
```

### 3. Policy Example
The MCP server can generate policy strings. For example, to grant read access to a specific path:

```hcl
path "secret/data/my-app/*" {
  capabilities = ["read", "list"]
}
```

## Related tools / concepts
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Authentik](../../services/authentik.md)
- [Kubernetes](../../architecture/infrastructure.md)
- [Tailscale](../../services/tailscale.md)
- [Headscale](../../services/headscale.md)
- [hvac (Python Vault Client)](https://github.com/hvac/hvac)

## Sources / References
- [Vault MCP GitHub](https://github.com/democratize-technology/vault-mcp)
- [HashiCorp Vault KV Secrets Engine](https://developer.hashicorp.com/vault/docs/secrets/kv)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high

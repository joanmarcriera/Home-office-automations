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

## Related tools / concepts
- [HashiCorp Vault](https://www.vaultproject.io/)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [hvac (Python Vault Client)](https://github.com/hvac/hvac)

## Sources / References
- [Vault MCP GitHub](https://github.com/democratize-technology/vault-mcp)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high

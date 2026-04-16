# HashiCorp Vault

## What it is
HashiCorp Vault is an identity-based secrets and data protection service that allows you to centrally store, access, and deploy secrets like API keys, passwords, and certificates.

## What problem it solves
Managing secrets in plain text (environment variables, config files) is a major security risk. Vault provides a single, secure source of truth for all secrets, with strict access control and detailed audit logs.

## Where it fits in the stack
**Infrastructure / Security Layer**. It is the "vault" for the homelab, protecting credentials used by n8n, Home Assistant, and other services.

## Typical use cases
- **Centralized Secret Storage**: Storing database passwords and API keys securely.
- **Dynamic Credentials**: Generating on-demand credentials for AWS or Postgres that expire automatically.
- **Encryption as a Service**: Encrypting sensitive data in transit without exposing encryption keys to the application.
- **PKI (Public Key Infrastructure)**: Generating and managing SSL/TLS certificates for internal services.

## Strengths
- **Secure by Design**: All data is encrypted at rest and in transit.
- **Detailed Auditing**: Every interaction with a secret is logged.
- **Ephemeral Secrets**: Reduces the "blast radius" of a leak by using short-lived credentials.
- **Shamir's Secret Sharing**: Securely unseals the vault using multiple key holders.

## Limitations
- **Operational Complexity**: Initial setup and maintenance (unsealing, policies) can be steep.
- **Dependency**: If Vault is down, all services that depend on it for credentials may fail.

## When to use it
- When you have a complex homelab with multiple users and services that require secure credential management.
- If you want to move away from hardcoded secrets in your automation scripts.

## When not to use it
- For very simple setups where a basic `.env` file or native service secret management (e.g., Docker Secrets) is sufficient.

## Related tools / concepts
- [Vault MCP Server](../automation_orchestration/vault-mcp.md)
- [Docker Secrets](https://docs.docker.com/engine/swarm/secrets/)
- [Tailscale OIDC](../../services/tailscale.md) (for identity)

## Sources / references
- [Official Website](https://www.vaultproject.io/)
- [Vault Documentation](https://developer.hashicorp.com/vault/docs)

## Contribution Metadata
- Last reviewed: 2026-04-06
- Confidence: high

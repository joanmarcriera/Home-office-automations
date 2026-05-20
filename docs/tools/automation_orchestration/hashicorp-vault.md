# HashiCorp Vault

## What it is
HashiCorp Vault is an identity-based secrets and data protection service that allows you to centrally store, access, and deploy secrets like API keys, passwords, and certificates.

## What problem it solves
Managing secrets in plain text (environment variables, config files) is a major security risk. Vault provides a single, secure source of truth for all secrets, with strict access control and detailed audit logs. It enables "secret sprawl" prevention by centralizing where sensitive information lives.

## Where it fits in the stack
**Infrastructure / Security Layer**. It is the "vault" for the homelab, protecting credentials used by [n8n](../../services/n8n.md), [Home Assistant](../../services/home-assistant.md), and other services.

## Typical use cases
- **Centralized Secret Storage**: Storing database passwords and API keys securely.
- **Dynamic Credentials**: Generating on-demand credentials for AWS or Postgres that expire automatically.
- **Encryption as a Service**: Encrypting sensitive data in transit without exposing encryption keys to the application.
- **PKI (Public Key Infrastructure)**: Generating and managing SSL/TLS certificates for internal services.

## Getting started

### Installation
Vault can be run as a standalone binary or via Docker:

```bash
# Docker-based installation (Development mode)
docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -p 8200:8200 hashicorp/vault
```

### Initializing and Unsealing
In a production-like setup (not dev mode), Vault starts in a sealed state:

```bash
# Initialize Vault (returns unseal keys and root token)
vault operator init

# Unseal Vault (requires 3 out of 5 keys by default)
vault operator unseal <unseal-key-1>
vault operator unseal <unseal-key-2>
vault operator unseal <unseal-key-3>
```

## CLI Reference

### Authentication
```bash
# Login with the root token or an auth method
vault login <token>
```

### Key-Value (KV) Secret Engine
Vault uses a filesystem-like path for secrets:

```bash
# Enable the KV engine v2
vault secrets enable -path=secret kv-v2

# Write a secret
vault kv put secret/n8n api_key="sk_live_12345"

# Read a secret
vault kv get secret/n8n
```

### Policy Management
Policies define what a user or service can do:

```bash
# Create a policy from a file
vault policy write n8n-policy - <<EOF
path "secret/data/n8n" {
  capabilities = ["read"]
}
EOF
```

## API Examples

### Reading a Secret via CURL
Applications can interact with Vault via its REST API:

```bash
curl --header "X-Vault-Token: <token>" \
     --request GET \
     http://127.0.0.1:8200/v1/secret/data/n8n
```

### Integration with Python
Using the `hvac` library for programmatic access:

```python
import hvac

client = hvac.Client(url='http://127.0.0.1:8200', token='myroot')

# Read secret
read_response = client.secrets.kv.v2.read_secret_version(path='n8n')
api_key = read_response['data']['data']['api_key']
print(f"Retrieved API Key: {api_key}")
```

## Strengths
- **Secure by Design**: All data is encrypted at rest and in transit.
- **Detailed Auditing**: Every interaction with a secret is logged.
- **Ephemeral Secrets**: Reduces the "blast radius" of a leak by using short-lived credentials.
- **Multi-cloud Support**: Integrates with AWS, Azure, GCP, and Kubernetes.

## Limitations
- **Operational Complexity**: Initial setup and maintenance (unsealing, policies) can be steep.
- **Dependency**: If Vault is down, all services that depend on it for credentials may fail.
- **Hardware Lock**: Requires `IPC_LOCK` capability in Docker for production use to prevent memory swapping.

## When to use it
- When you have a complex homelab with multiple users and services that require secure credential management.
- If you want to move away from hardcoded secrets in your automation scripts.
- When you need dynamic, short-lived credentials for cloud providers.

## When not to use it
- For very simple setups where a basic `.env` file or native service secret management (e.g., Docker Secrets) is sufficient.
- If the overhead of managing a dedicated security service outweighs the security benefits of your project.

## Related tools / concepts
- [Vault MCP Server](../automation_orchestration/vault-mcp.md)
- [LiteLLM](../../services/litellm.md) (for managing model API keys)
- [Tailscale OIDC](../../services/tailscale.md) (for identity)
- [Docker](../infrastructure/docker.md)
- [GNU Make](gnu-make.md)
- [OpenClaw](../development_ops/openclaw.md)
- [Authentik](../../services/authentik.md)

## Sources / references
- [Official Website](https://www.vaultproject.io/)
- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [hvac Python Library](https://github.com/hvac/hvac)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high

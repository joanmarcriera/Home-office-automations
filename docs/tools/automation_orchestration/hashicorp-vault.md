# HashiCorp Vault

## What it is
HashiCorp Vault is an identity-based secrets and data protection service that allows you to centrally store, access, and deploy secrets like API keys, passwords, and certificates. As of June 2026, it is the industry standard for managing sensitive credentials in agentic workflows, often serving as the secure backend for models like `claude-4-8-opus-20260528` and GPT-5.5.

## What problem it solves
Managing secrets in plain text (environment variables, configuration files) is a major security risk. Vault provides a single, secure source of truth for all secrets, with strict access control and detailed audit logs. It enables "secret sprawl" prevention by centralizing where sensitive information lives and who (or what) can access it.

## Where it fits in the stack
**Infrastructure / Security Layer**. It is the "vault" for the homelab and enterprise alike, protecting credentials used by [n8n](../../services/n8n.md), [Home Assistant](../../services/home-assistant.md), and [OpenClaw](../development_ops/openclaw.md). It often integrates with [Vault MCP](../automation_orchestration/vault-mcp.md) to provide AI agents with time-limited access to tools.

## Typical use cases
- **Centralized Secret Storage**: Storing database passwords and API keys securely.
- **Dynamic Credentials**: Generating on-demand credentials for AWS, Postgres, or Google Cloud that expire automatically.
- **Encryption as a Service**: Encrypting sensitive data in transit/at rest without exposing encryption keys to the application.
- **PKI (Public Key Infrastructure)**: Generating and managing SSL/TLS certificates for internal services.
- **Agentic Secret Injection**: Securely providing API keys to autonomous agents at runtime.

## Strengths
- **Secure by Design**: All data is encrypted at rest and in transit; memory is locked to prevent swapping.
- **Detailed Auditing**: Every interaction with a secret is logged, providing a clear trail for compliance.
- **Ephemeral Secrets**: Reduces the "blast radius" of a leak by using short-lived, dynamically generated credentials.
- **Multi-cloud Support**: Robust integrations with AWS, Azure, GCP, Kubernetes, and OIDC providers.

## Limitations
- **Operational Complexity**: Initial setup, unsealing processes, and complex policy management can have a steep learning curve.
- **High Dependency**: If Vault is unavailable, all downstream services that depend on it for credentials may fail (the "locked door" problem).
- **Resource Overhead**: Requires careful resource planning for high availability in production environments.

## When to use it
- When you have a complex homelab or enterprise environment with multiple services requiring secure credential management.
- If you want to move away from hardcoded secrets in your automation scripts and Docker Compose files.
- When you need to provide AI agents with restricted, auditable access to sensitive APIs.

## When not to use it
- For very simple, single-server setups where basic `.env` files or native service secret management (e.g., Docker Secrets) is sufficient.
- If the operational overhead of managing a dedicated security service outweighs the security benefits of a small-scale project.

## Getting started

### Installation
Vault can be run as a standalone binary or via Docker:

```bash
# Docker-based installation (Development mode)
docker run --cap-add=IPC_LOCK -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' -p 8200:8200 hashicorp/vault
```

### Initializing and Unsealing
In a production-like setup, Vault starts in a sealed state and must be initialized:

```bash
# Initialize Vault (returns unseal keys and root token)
vault operator init

# Unseal Vault (requires a quorum of keys, e.g., 3 out of 5)
vault operator unseal <unseal-key-1>
vault operator unseal <unseal-key-2>
vault operator unseal <unseal-key-3>
```

## CLI examples

### Authentication
```bash
# Login with the root token or an auth method (e.g., GitHub, AppRole)
vault login <token>
```

### Key-Value (KV) Secret Management
Vault uses a filesystem-like path for secrets:

```bash
# Enable the KV engine v2
vault secrets enable -path=secret kv-v2

# Write a secret (e.g., for n8n)
vault kv put secret/n8n api_key="sk_live_12345"

# Read the secret
vault kv get secret/n8n

# List all secrets in a path
vault kv list secret/
```

### Policy Management
```bash
# Create a policy from a file to restrict access
vault policy write n8n-readonly-policy - <<EOF
path "secret/data/n8n" {
  capabilities = ["read"]
}
EOF
```

## API examples

### Reading a Secret via CURL
Applications (or agents) can interact with Vault via its REST API:

```bash
curl --header "X-Vault-Token: <token>" \
     --request GET \
     http://127.0.0.1:8200/v1/secret/data/n8n
```

### Python Integration (hvac)
Using the `hvac` library for programmatic secret retrieval in June 2026:

```python
import hvac

# Initialize client
client = hvac.Client(url='http://127.0.0.1:8200', token='myroot')

# Read secret from KV v2 engine
try:
    read_response = client.secrets.kv.v2.read_secret_version(path='n8n')
    api_key = read_response['data']['data']['api_key']
    print(f"Retrieved API Key: {api_key}")
except Exception as e:
    print(f"Error retrieving secret: {e}")
```

## Related tools / concepts
- [Vault MCP Server](../automation_orchestration/vault-mcp.md) — The bridge for AI agents.
- [Authentik](../../services/authentik.md) — For OIDC-based authentication to Vault.
- [Tailscale](../../services/tailscale.md) — For secure networking to the Vault instance.
- [Docker](../infrastructure/docker.md) — Primary deployment method.
- [Axiom Guardian](../development_ops/axiom-guardian.md) — For validating requests to sensitive systems.

## Sources / references
- [HashiCorp Vault Official Website](https://www.vaultproject.io/)
- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [hvac Python Library GitHub](https://github.com/hvac/hvac)
- [Vault MCP GitHub](https://github.com/modelcontextprotocol/servers/tree/main/src/vault)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high

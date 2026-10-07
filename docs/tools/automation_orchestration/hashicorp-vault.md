# HashiCorp Vault

## What it is
HashiCorp Vault is an identity-based secrets and data protection service designed to centrally store, access, and deploy sensitive credentials such as API keys, passwords, and certificates. As of early 2027, it serves as the foundational security layer for agentic workflows, providing secure backend storage for frontier models like **Gemma 4**, **DeepSeek-V4**, **Qwen 3.6 VL**, **Claude 5.6**, **GPT-5.6**, and **Gemini 4.0 Ultra** via standardized **Vault MCP** and **FastMCP 3.1** integrations.

Vault enforces strict perimeter control and dynamic credential issuance across distributed microservices, multi-cloud Kubernetes clusters, and local agentic runtimes. By replacing long-lived credentials with ephemeral leased tokens and dynamic secret engines, Vault establishes zero-trust security architecture for modern autonomous software execution.

```
+-----------------------------------------------------------------------------------+
|                            AGENTIC ORCHESTRATION LAYER                            |
|  [ FastMCP 3.1 Task Protocol ] <---> [ Vault MCP Bridge ] <---> [ Agent Runtime ] |
+-----------------------------------------------------------------------------------+
                                         |
                                (Authenticated Call)
                                         v
+-----------------------------------------------------------------------------------+
|                             HASHICORP VAULT CORE                                  |
|                                                                                   |
|  +---------------------+  +----------------------+  +--------------------------+  |
|  | Secret Engines      |  | Auth Methods         |  | Audit System             |  |
|  | - KV v2             |  | - AppRole / Token    |  | - File / Syslog          |  |
|  | - Dynamic DB        |  | - Kubernetes Service |  | - Structured JSON        |  |
|  | - PKI & Transit     |  | - OIDC / Authentik   |  | - Non-repudiation Log    |  |
|  +---------------------+  +----------------------+  +--------------------------+  |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | Cryptographic Storage Barrier (AES-256-GCM / Shamir Secret Sharing Unseal)    |  |
|  +-----------------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                             PHYSICAL / CONTAINER STORAGE                          |
|         [ PostgreSQL / Raft Storage Cluster / Local Encrypted Memory ]            |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing secrets in plain text, environment variables, or unprotected configuration files creates significant security vulnerabilities. Vault provides a single, secure source of truth with strict access control, automated secret rotation, and granular auditing. It eliminates "secret sprawl" by centralizing credential management and ensuring that only authorized agents and services can access specific sensitive information.

Key enterprise security challenges mitigated by HashiCorp Vault include:
- **Secret Leakage in Source Control**: Preventing API tokens from being accidentally committed into code repositories or prompt logs.
- **Over-privileged Agent Credentials**: Restricting autonomous LLM agents to dynamic, scope-bounded credentials that expire after single-task completion.
- **Lack of Cryptographic Audit Trails**: Providing tamper-proof logs for regulatory compliance and forensic audit when LLMs interact with corporate databases.
- **Manual Key Lifecycle Management**: Automating TLS certificate renewal, database user rotation, and transit encryption key rekeying without application downtime.

## Where it fits in the stack
**Infrastructure / Security Layer**. It is the primary security engine for both homelab and enterprise environments, protecting credentials used by [n8n](../../services/n8n.md), [Home Assistant](../../services/home-assistant.md), and [Aider](../development_ops/aider.md). It integrates deeply with the [Model Context Protocol (MCP)](mcp.md) ecosystem via [Vault MCP](vault-mcp.md) to provide AI agents with secure, time-limited access to tools.

```
+-----------------------------------------------------------------------------------+
|                              APPLICATIONS & AGENTS                                |
|   [ Claude Code ]      [ FastMCP 3.1 Server ]      [ n8n Automation Engine ]     |
+-----------------------------------------------------------------------------------+
           |                        |                            |
           v                        v                            v
+-----------------------------------------------------------------------------------+
|                              VAULT SECURITY GATEWAY                               |
|                     (AppRole Authentication & Policy Checks)                      |
+-----------------------------------------------------------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------------------+
|                             DYNAMIC SECRET ENGINES                                |
|   +-------------------+    +--------------------+    +--------------------+       |
|   | KV v2 (Key-Value) |    | Dynamic Database   |    | PKI Certificate    |       |
|   | Provider API Keys |    | Ephemeral Postgres |    | Internal MutualTLS |       |
|   +-------------------+    +--------------------+    +--------------------+       |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Centralized Secret Management**: Securely storing and managing API keys for providers like [Fireworks AI](../providers/fireworks.md) and [Cohere](../providers/cohere.md).
- **Dynamic Credentials**: On-demand generation of temporary credentials for AWS, Postgres, or Google Cloud that expire automatically after use.
- **Encryption as a Service**: Offloading data encryption tasks to Vault to ensure that encryption keys never leave the secure environment.
- **Agentic Secret Injection**: Securely injecting credentials into autonomous agent environments at runtime via [Vault MCP](vault-mcp.md).
- **Identity-Based Access**: Leveraging [Authentik](../../services/authentik.md) or OIDC for secure, role-based access to infrastructure secrets.
- **PKI Certificate Authority**: Managing internal TLS certificates for microservice mutual authentication (mTLS) with automated zero-downtime rotation.

## Detailed Architecture & Secret Engines

Vault operates on a storage-barrier model where all stored data is encrypted using an internal Encryption Key before being written to the underlying storage backend (Raft or database). Access to Vault functions is mediated through distinct engines:

1. **KV v2 (Key-Value Version 2)**: Provides versioned key-value storage. Older versions of secrets can be recovered or permanently soft/hard deleted. Perfect for LLM provider credentials.
2. **Database Engine**: Generates dynamic database credentials with custom TTLs. When an agent requests database access, Vault creates a temporary user in PostgreSQL or MySQL and drops the user when the lease expires.
3. **Transit Engine**: Performs encryption, decryption, HMAC generation, and signatures in-flight without storing the data inside Vault ("Encryption-as-a-Service").
4. **PKI Engine**: Acts as a Root or Intermediate Certificate Authority (CA) to dynamically generate X.509 certificates for short-lived service communication.

```
+-----------------------------------------------------------------------------------+
|                             VAULT LEASE LIFECYCLE                                 |
|                                                                                   |
|  1. Agent Requests Credential -> [ Vault Core Validation ]                        |
|                                              |                                    |
|  2. Dynamic Engine Generates Secret <--------+                                    |
|                                              |                                    |
|  3. Lease Assigned (TTL: 15m) ---------------> [ Lease Renewal Daemon ]           |
|                                              |                                    |
|  4. Expiration / Explicit Revocation --------> [ Automated User Drop / Key Wipe ] |
+-----------------------------------------------------------------------------------+
```

## Strengths
- **Hardened Security**: Data is encrypted at rest and in transit using industry-standard algorithms (AES-256-GCM); memory is locked to prevent swapping.
- **Detailed Audit Logs**: Every interaction—successful or denied—is logged, providing a complete audit trail for compliance and security forensics.
- **Ephemeral Secrets**: Minimizes the risk of credential theft by using short-lived, dynamically generated secrets that are automatically revoked.
- **Multi-Cloud Native**: Robust support for secret management across AWS, Azure, GCP, Kubernetes, and on-premise infrastructure.
- **Granular Policy Engine**: Declarative HCL policies allow path-based and capability-based (read, create, update, delete, list, sudo) access control down to individual JSON object fields.

## Limitations
- **Operational Overhead**: Requires careful management of initialization, unsealing processes, and complex HCL policy design.
- **Single Point of Failure**: If the Vault instance is unavailable or sealed, all downstream services depending on it for secrets will fail.
- **Resource Intensity**: High-availability production deployments require significant planning and infrastructure resources compared to simpler secret managers.
- **Learning Curve**: Mastering token renewed leases, unsealing quorums, and authentication backend mapping requires dedicated administrative expertise.

## When to use it
- In complex environments where multiple AI agents and automated services require secure, auditable access to sensitive credentials.
- When moving towards a "Zero Trust" architecture for agentic infrastructure.
- When you need to provide AI assistants (e.g., [Claude Code](../development_ops/claude-code-setup.md)) with restricted, temporary access to privileged system APIs.
- When regulatory frameworks (e.g., SOC2, HIPAA, ISO 27001) mandate continuous credential rotation and cryptographic audit logging.

## When not to use it
- For very simple, single-server projects where basic `.env` files or native platform secret management (e.g., GitHub Secrets) is sufficient.
- In resource-constrained environments where the operational cost of managing a dedicated security service outweighs the security benefits.

## Getting started

### 1. Installation & Docker Setup
Deploy Vault via Docker for rapid setup in a development environment or production server:

```bash
# Start Vault in development mode with a fixed root token
docker run --cap-add=IPC_LOCK \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' \
  -e 'VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200' \
  -p 8200:8200 \
  --name vault-dev \
  hashicorp/vault:latest
```

### 2. Initializing and Unsealing
For production environments utilizing the Integrated Raft storage engine:

```bash
# Set environment variable to target local instance
export VAULT_ADDR='http://127.0.0.1:8200'

# Initialize to generate unseal keys and the initial root token
vault operator init -key-shares=5 -key-threshold=3 > cluster-keys.txt

# Unseal Vault (requires a quorum of 3 out of 5 key shares)
vault operator unseal <unseal-key-1>
vault operator unseal <unseal-key-2>
vault operator unseal <unseal-key-3>
```

### 3. Configure Agent Access
Set up [Vault MCP](vault-mcp.md) to bridge your Vault instance with your AI agents using FastMCP 3.1 Task Protocol.

```bash
# Login with root or admin token
vault login token="myroot"

# Enable AppRole Auth Engine for agent authentication
vault auth enable approle

# Create policy for AI Agent secret consumption
vault policy write agent-read-policy - <<EOF
path "secret/data/agents/*" {
  capabilities = ["read", "list"]
}
path "database/creds/agent-role" {
  capabilities = ["read"]
}
EOF

# Create AppRole for FastMCP agent
vault write auth/approle/role/fastmcp-agent \
    secret_id_ttl=24h \
    token_num_uses=0 \
    token_ttl=1h \
    token_max_ttl=4h \
    secret_id_num_uses=0 \
    policies="agent-read-policy"
```

## CLI examples

### Authentication and Engine Setup
```bash
# Login with your token
vault login <token>

# Enable the Key-Value (KV) version 2 secrets engine
vault secrets enable -path=secret kv-v2

# Enable Dynamic Database engine
vault secrets enable database
```

### Managing KV Secrets
```bash
# Write a secret for an agentic workflow
vault kv put secret/agents/config api_key="sk_prod_54321" model_tier="enterprise"

# Retrieve the secret
vault kv get secret/agents/config

# Retrieve metadata about secret versions
vault kv metadata get secret/agents/config

# List available secrets in a specific path
vault kv list secret/agents/
```

### Dynamic Database Credentials Configuration
```bash
# Configure PostgreSQL database connection
vault write database/config/postgresql-db \
    plugin_name=postgresql-database-plugin \
    allowed_roles="agent-role" \
    connection_url="postgresql://{{username}}:{{password}}@postgres.internal:5432/agent_db?sslmode=disable" \
    username="vault_admin" \
    password="admin_password"

# Define dynamic role with 1-hour revocation TTL
vault write database/creds/agent-role \
    db_name=postgresql-db \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Generate temporary database credentials
vault read database/creds/agent-role
```

## API examples

### Reading Secrets via REST API
Agents can interact with Vault using standard HTTP REST requests:

```bash
curl --header "X-Vault-Token: <token>" \
     --request GET \
     http://127.0.0.1:8200/v1/secret/data/agents/config
```

### Transit Encryption-as-a-Service via REST
```bash
# Enable transit engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/llm-prompt-key

# Encrypt sensitive text
curl --header "X-Vault-Token: <token>" \
     --request POST \
     --data '{"plaintext": "VGhpcyBpcyBhIHNlbnNpdGl2ZSBsb2c="}' \
     http://127.0.0.1:8200/v1/transit/encrypt/llm-prompt-key
```

### Python Integration with FastMCP 3.1 & Pydantic v2
Below is a full Python implementation demonstrating a FastMCP 3.1 server integration with HashiCorp Vault. It retrieves secrets dynamically, validates payloads using Pydantic v2 schemas, and encrypts outgoing data using Vault's Transit engine.

```python
import hvac
import base64
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, SecretStr, ValidationError
from typing import Optional, Dict, Any

# 1. Initialize FastMCP 3.1 Server
mcp = FastMCP("VaultSecurityServer", version="3.1.0")

# 2. Pydantic v2 Models for Secret Schemas
class VaultConfig(BaseModel):
    vault_url: str = Field("http://127.0.0.1:8200", description="Vault cluster HTTP endpoint")
    role_id: str = Field(..., description="AppRole Role ID")
    secret_id: SecretStr = Field(..., description="AppRole Secret ID")

class AgentCredentialsResponse(BaseModel):
    provider_name: str = Field(..., pattern="^(anthropic|openai|google|cohere|deepseek)$")
    api_key: SecretStr = Field(..., min_length=16, description="Vault-stored provider API key")
    model_tier: str = Field("standard", description="Model access tier authorized for this token")
    task_id: Optional[str] = Field(None, description="FastMCP 3.1 Task Protocol execution ID")

class DynamicDBCredentials(BaseModel):
    username: str = Field(..., description="Ephemeral database username")
    password: SecretStr = Field(..., description="Ephemeral database password")
    lease_id: str = Field(..., description="Vault lease tracking ID")
    lease_duration: int = Field(..., description="Time to live in seconds")

# 3. Helper for Vault Authentication via AppRole
def get_authenticated_vault_client(config: VaultConfig) -> hvac.Client:
    client = hvac.Client(url=config.vault_url)
    auth_response = client.auth.approle.login(
        role_id=config.role_id,
        secret_id=config.secret_id.get_secret_value()
    )
    if not client.is_authenticated():
        raise RuntimeError("Vault AppRole authentication failed")
    return client

# 4. FastMCP 3.1 Tools
@mcp.tool()
def get_agent_secret(
    vault_url: str,
    role_id: str,
    secret_id: str,
    secret_path: str,
    task_id: Optional[str] = None
) -> Dict[str, Any]:
    """Retrieve and validate an LLM provider key from Vault KV v2 engine."""
    config = VaultConfig(vault_url=vault_url, role_id=role_id, secret_id=SecretStr(secret_id))
    client = get_authenticated_vault_client(config)

    try:
        response = client.secrets.kv.v2.read_secret_version(path=secret_path)
        raw_data = response['data']['data']
        raw_data['task_id'] = task_id

        # Validate against Pydantic v2 model
        creds = AgentCredentialsResponse.model_validate(raw_data)

        return {
            "status": "success",
            "provider_name": creds.provider_name,
            "api_key": creds.api_key.get_secret_value(),
            "model_tier": creds.model_tier,
            "task_id": creds.task_id
        }
    except ValidationError as ve:
        return {"status": "error", "type": "ValidationError", "details": str(ve)}
    except Exception as e:
        return {"status": "error", "type": "VaultError", "details": str(e)}

@mcp.tool()
def generate_db_credentials(
    vault_url: str,
    role_id: str,
    secret_id: str,
    db_role_name: str
) -> Dict[str, Any]:
    """Generate ephemeral dynamic database credentials via Vault Database Engine."""
    config = VaultConfig(vault_url=vault_url, role_id=role_id, secret_id=SecretStr(secret_id))
    client = get_authenticated_vault_client(config)

    try:
        lease = client.secrets.database.generate_credentials(name=db_role_name)
        data = {
            "username": lease['data']['username'],
            "password": lease['data']['password'],
            "lease_id": lease['lease_id'],
            "lease_duration": lease['lease_duration']
        }
        validated_db = DynamicDBCredentials.model_validate(data)
        return {
            "status": "success",
            "db_username": validated_db.username,
            "db_password": validated_db.password.get_secret_value(),
            "lease_id": validated_db.lease_id,
            "ttl_seconds": validated_db.lease_duration
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}

@mcp.tool()
def encrypt_transit_data(
    vault_url: str,
    role_id: str,
    secret_id: str,
    key_name: str,
    plaintext_data: str
) -> Dict[str, Any]:
    """Encrypt sensitive prompt data using Vault Transit Encryption Engine."""
    config = VaultConfig(vault_url=vault_url, role_id=role_id, secret_id=SecretStr(secret_id))
    client = get_authenticated_vault_client(config)

    encoded_bytes = base64.b64encode(plaintext_data.encode('utf-8')).decode('utf-8')
    response = client.secrets.transit.encrypt_data(
        name=key_name,
        plaintext=encoded_bytes
    )
    return {
        "status": "success",
        "ciphertext": response['data']['ciphertext']
    }

if __name__ == "__main__":
    mcp.run()
```

## Security Best Practices for Agentic Systems

1. **Never Hardcode Root Tokens**: Development root tokens should never enter production. Use AppRole or Kubernetes authentication methods.
2. **Short-Lived Leases**: Configure max TTLs for LLM tokens to 15–60 minutes to minimize blast radius during credential compromise.
3. **Audit Stream Export**: Pipe Vault's JSON audit log directly to SIEM solutions (e.g., Elastic, Splunk) or ClickHouse to track LLM tool invocations.
4. **Memory Locking (`mlock`)**: Ensure Vault runs with `--cap-add=IPC_LOCK` or Linux capabilities enabled so secret values are never written to swap memory.
5. **Auto-Unseal with HSM or Cloud KMS**: In enterprise environments, use AWS KMS, GCP KMS, or HashiCorp Cloud Platform (HCP) Auto-Unseal to eliminate manual unseal key assembly on server restart.

## Related tools / concepts
- [Vault MCP](vault-mcp.md) — The Model Context Protocol interface for HashiCorp Vault.
- [Model Context Protocol (MCP)](mcp.md) — The standardized protocol for agent-tool communication (FastMCP 3.1).
- [Authentik](../../services/authentik.md) — Identity provider for managing Vault access.
- [Aider](../development_ops/aider.md) — Agentic IDE that can leverage Vault-stored credentials.
- [n8n](../../services/n8n.md) — Automation platform that often requires secure secret management.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier model used for orchestrating secure workflows.
- [Axiom Guardian](../development_ops/axiom-guardian.md) — For validating requests and managing security boundaries.
- [Docker](../infrastructure/docker.md) — The preferred method for containerized Vault deployment.

## Sources / references
- [HashiCorp Vault Official Site](https://www.vaultproject.io/)
- [Vault Documentation Portal](https://developer.hashicorp.com/vault/docs)
- [hvac Python Client Library](https://hvac.readthedocs.io/)
- [Official MCP Specification](https://modelcontextprotocol.io/)
- [Vault MCP Repository](https://github.com/democratize-technology/vault-mcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

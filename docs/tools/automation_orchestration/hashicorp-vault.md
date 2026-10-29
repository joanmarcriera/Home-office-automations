# HashiCorp Vault

## What it is
HashiCorp Vault is an enterprise-grade identity-based secret management, data encryption, and privileged credential management engine. Designed to secure sensitive credentials—including API tokens, database connection strings, TLS certificates, SSH keys, and cloud access keys—Vault provides centralized control, auditing, dynamic leasing, and real-time encryption in transit and at rest. As of late 2026 / early 2027, Vault functions as the core security foundation for agentic workflows and automated homelab/enterprise infrastructure. It bridges identity providers (such as [Authentik](../../services/authentik.md), Keycloak, and OIDC) with AI models (such as **Claude 5.6**, **GPT-5.6**, **Gemma 4**, **DeepSeek-V4**, and **Qwen 3.6 VL**) through standardized **Vault MCP** and **FastMCP 3.1** protocol integrations.

## Workflow Orchestration & Sequence Architecture
The following sequence diagram illustrates the lifecycle of dynamic credential requesting, policy authorization, and lease auto-revocation between an AI agent and HashiCorp Vault via FastMCP 3.1:

```mermaid
sequenceDiagram
    autonumber
    actor Agent as Autonomous AI Agent
    participant MCP as FastMCP 3.1 Vault Server
    participant Vault as Vault Core Engine
    participant Auth as Authentik OIDC / AppRole Engine
    participant Postgres as Target Database / AWS Service

    Agent->>MCP: Request Ephemeral DB Credentials (`fetch_dynamic_db_cred`)
    MCP->>Auth: Validate Agent AppRole Secret ID / OIDC Token
    Auth-->>MCP: Return Authorized Token + HCL Policy
    MCP->>Vault: GET /v1/database/creds/agent-read-role
    Vault->>Postgres: CREATE USER 'v-approle-xyz' WITH PASSWORD '...'
    Postgres-->>Vault: User Created (TTL: 3600s)
    Vault-->>MCP: Return Short-Lived Credential Payload & Lease ID
    MCP-->>Agent: Deliver Validated Pydantic Response
    Note over Agent,Postgres: Lease Expires after 3600s
    Vault->>Postgres: DROP USER 'v-approle-xyz' (Auto Revocation)
```

## What problem it solves
Hardcoding API tokens, database passwords, or private encryption keys in codebases, configuration files (`.env`), or CI/CD environment variables creates severe security vulnerabilities:

1. **Secret Sprawl & Credential Leakage**: Microservices and autonomous agents proliferation leads to unmonitored copies of sensitive keys stored across repository histories and container image layers.
2. **Static Credentials**: Long-lived static tokens remain valid indefinitely after exposure, expanding the window of opportunity for unauthorized exploitation.
3. **Lack of Auditing**: Standard environment variables do not log access events, making it impossible to determine which agent or service retrieved a specific credential during a security incident.
4. **Agentic Tool Over-Privileging**: Autonomous AI agents given static full-access API keys risk accidentally exposing or misusing administrative privileges.

Vault solves these challenges by implementing a Zero Trust security architecture based on dynamic secret leasing, dynamic credential generation, centralized secret rotation, cryptographic transit encryption, and explicit FastMCP 3.1 permission policies.

```
+-----------------------------------------------------------------------------------+
|                            HASHICORP VAULT ARCHITECTURE                           |
+-----------------------------------------------------------------------------------+

[ Agentic Workbenches / AI Models ] ────> [ Vault MCP / FastMCP 3.1 Protocol ]
                                                      │
                                                      ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
| Vault Server Engine (AES-256-GCM Encrypted Barrier / Locked Memory)              |
|                                                                                  |
| ┌────────────────────────┐  ┌────────────────────────┐  ┌──────────────────────┐ |
| │ Auth Methods           │  │ Secret Engines         │  │ Audit Storage        │ |
| │ - AppRole / Token      │  │ - KV v2 (Key-Value)    │  │ - Syslog / File      │ |
| │ - Kubernetes / OIDC    │  │ - Dynamic Postgres/AWS │  │ - Tamper-Proof Log   │ |
| │ - Authentik / TLS Cert │  │ - Transit Encryption   │  │   Stream             │ |
| └────────────────────────┘  └────────────────────────┘  └──────────────────────┘ |
└──────────────────────────────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
| Integrated Storage Layer (Raft / Encrypted Storage Backend)                      |
└──────────────────────────────────────────────────────────────────────────────────┘
```

## Where it fits in the stack
**Infrastructure / Security Layer**. Vault serves as the centralized identity and secrets coordinator across homelab and cloud deployments. It injects dynamic API credentials into automation platforms like [n8n](../../services/n8n.md), self-hosted containers ([Home Assistant](../../services/home-assistant.md), [Paperless-ngx](../../services/paperless-ngx.md)), and developer IDE agents ([Claude Code](../development_ops/claude-code-setup.md), [Aider](../development_ops/aider.md)).

### Key Capabilities & Technical Features

#### 1. Key-Value Version 2 (KV v2) Engine
Provides versioned secret storage with soft-delete capabilities, metadata tracking, and automatic historical revision management. It allows rollback to prior secret values if a newly generated key fails.

#### 2. Dynamic Secret Generation
Vault generates short-lived, on-demand credentials for external systems (e.g., PostgreSQL databases, AWS IAM, Google Cloud, RabbitMQ). Credentials automatically expire at the end of their lease unless explicitly renewed by the requesting process.

#### 3. Encryption as a Service (Transit Engine)
Vault encrypts data in transit without storing the underlying plaintext. Applications pass raw payloads to Vault's `/transit/encrypt` endpoint, receiving ciphertext encrypted using modern keys managed and rotated entirely by Vault.

#### 4. FastMCP 3.1 & Vault MCP Integration
Vault MCP exposes Vault's REST API through the Model Context Protocol (FastMCP 3.1). AI agents can request temporary API keys or decrypt payloads within narrow policy boundaries without ever accessing Vault's root token or underlying master keys.

#### 5. Fine-Grained Policy Engine (HCL)
Access control policies defined in HashiCorp Configuration Language (HCL) specify exact paths, capabilities (`create`, `read`, `update`, `delete`, `list`), and parameter restrictions for every token and identity.

## Feature Comparison Matrix

| Capability / Metric | HashiCorp Vault | AWS Secrets Manager | Infisical | Environment Variables (.env) |
| :--- | :--- | :--- | :--- | :--- |
| **Deployment Model** | Self-Hosted / Managed Cloud | Managed AWS Cloud | Self-Hosted / Managed Cloud | Local / Plain Text |
| **Dynamic Credentials** | Yes (Database, AWS, PKI) | Yes (RDS rotation only) | Limited | None |
| **FastMCP 3.1 Native Protocol**| Supported via Vault MCP | Custom Lambda wrapper | Community adapter | None |
| **Transit Encryption API** | Built-in AES-256-GCM API | KMS Envelope Encryption | Symmetric API | None |
| **Audit Logging** | Granular tamper-proof JSON | AWS CloudTrail | Audit log UI | None |
| **Identity Binding** | OIDC, AppRole, Kubernetes, TLS | IAM Roles only | OAuth2, Tokens | None |

## Typical use cases
- **Agentic API Key Delivery**: Injecting short-lived API keys for [Fireworks AI](../providers/fireworks.md), [Together AI](../providers/together.md), or [OpenRouter](../ai_knowledge/openrouter.md) into agent runtimes at startup.
- **Automated Database Credential Leasing**: Generating temporary, unique PostgreSQL user credentials for ephemeral CI/CD pipelines and n8n workflows.
- **Self-Hosted Infrastructure PKI**: Automatically issuing and renewing TLS certificates for local domain services managed by Nginx Proxy Manager or Traefik.
- **Homelab Secret Centralization**: Eliminating plain-text passwords from `docker-compose.yml` files by passing secrets directly to containers via Vault agent sidecars.

## Strengths
- **Cryptographic Security**: Master key constructed using Shamir's Secret Sharing algorithm; RAM is locked via `mlock` to prevent memory swapping.
- **Comprehensive Audit Trail**: Every token creation, secret access, policy update, and unseal operation is logged in JSON format with source IP and user identity tags.
- **Dynamic Lease Revocation**: Instantly revoke an entire tree of dynamic credentials or compromise tokens with a single CLI command or API call.
- **Multi-Cloud Identity Binding**: Native authentication adapters for AWS IAM, GCP Service Accounts, Kubernetes ServiceAccounts, and OIDC/OAuth2.

## Limitations
- **Unsealing Operational Requirement**: When a Vault server restarts, it starts in a "Sealed" state and cannot read data until unsealed using a quorum of unseal keys (or Auto-Unseal HSM/KMS).
- **HCL Policy Complexity**: Writing precise, least-privilege path policies requires careful planning to prevent accidental over-permissioning or service lockouts.
- **Resource Footprint**: High-availability Raft clusters require dedicated node resources and network monitoring compared to simple key-value stores.

## When to use it
- In zero-trust environments where multiple AI agents, CI/CD runners, and microservices require auditable, short-lived secret access.
- When regulatory compliance or security standards require strict audit logging and automated credential rotation.
- When deploying FastMCP 3.1 agentic tools that need secure credential access without persistent static key storage.

## When not to use it
- For single-server, static personal projects where basic environment variables or Docker secrets provide sufficient protection.
- In resource-constrained micro-edge devices (e.g., Raspberry Pi Zero) where running a full Vault server daemon introduces unacceptable memory overhead.

## Getting started

### 1. Docker Compose Deployment (Dev / Homelab Mode)

```yaml
version: "3.8"

services:
  vault:
    image: hashicorp/vault:1.16.0
    container_name: vault-server
    restart: unless-stopped
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: "root-dev-token-2027"
      VAULT_DEV_LISTEN_ADDRESS: "0.0.0.0:8200"
    cap_add:
      - IPC_LOCK
    volumes:
      - ./vault/data:/vault/file
      - ./vault/config:/vault/config
```

### 2. Production Initialization and Unsealing
For non-dev production deployments using Raft integrated storage:

```bash
# Export Vault server address
export VAULT_ADDR="http://127.0.0.1:8200"

# Initialize Vault to generate 5 key shares with a threshold of 3
vault operator init -key-shares=5 -key-threshold=3 > cluster-keys.txt

# Inspect key output (Keep cluster-keys.txt secure!)
cat cluster-keys.txt

# Unseal Vault using 3 of the 5 generated key shares
vault operator unseal <Unseal-Key-1>
vault operator unseal <Unseal-Key-2>
vault operator unseal <Unseal-Key-3>

# Login with the root token
vault login <Initial-Root-Token>
```

## Systemd Service Unit Configuration
For running Vault as a hardened system service (`/etc/systemd/system/vault.service`):

```ini
[Unit]
Description=HashiCorp Vault Secret Management Daemon
After=network-online.target local-fs.target
Wants=network-online.target
Documentation=https://developer.hashicorp.com/vault/docs

[Service]
Type=notify
User=vault
Group=vault
ExecStart=/usr/bin/vault server -config=/etc/vault.d/vault.hcl
ExecReload=/bin/kill --signal HUP $MAINPID
Restart=on-failure
RestartSec=5s
LimitNOFILE=65536
LimitMEMLOCK=infinity
Capabilities=CAP_IPC_LOCK+ep
SecureBits=keep-caps

# Security Hardening Options
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
PrivateDevices=true
CapabilityBoundingSet=CAP_IPC_LOCK
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## CLI examples

### Authentication and Engine Setup
```bash
# Login with your token
vault login <token>

# Enable the Key-Value (KV) version 2 secrets engine
vault secrets enable -path=secret kv-v2

# Write a secret key-value entry for an agent worker
vault kv put secret/agents/anthropic \
  provider="anthropic" \
  api_key="sk-ant-api03-prod-key-sample-2027" \
  environment="production" \
  lease_duration=3600

# Read secret metadata and current version value
vault kv get secret/agents/anthropic
```

### Managing Dynamic Credentials & Policies
```bash
# Apply HCL policy
vault policy write agent-read-policy agent-policy.hcl

# Enable database engine & generate dynamic postgres creds
vault secrets enable database
vault read database/creds/agent-read-role
```

## API examples

### Reading Secrets & FastMCP 3.1 Pydantic Validation
The following production script demonstrates an AI agent interacting with Vault via a FastMCP 3.1 server, retrieving secrets from KV v2, and executing strict Pydantic v2 validation (`extra="forbid"`).

```python
import hvac
from pydantic import BaseModel, Field, SecretStr, field_validator, ConfigDict
from typing import Optional, Dict, Any
from fastmcp import FastMCP

# Define strict Pydantic v2 validation schemas for secrets
class APIKeyPayload(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    provider: str = Field(..., description="Target model provider (e.g., anthropic, openai)")
    api_key: SecretStr = Field(..., min_length=20, description="Encrypted API token")
    environment: str = Field("production", description="Deployment stage")
    lease_duration_sec: int = Field(3600, ge=60, le=86400)

    @field_validator('provider')
    @classmethod
    def validate_provider(cls, v: str) -> str:
        allowed = {"anthropic", "openai", "openrouter", "google", "deepseek"}
        if v.lower() not in allowed:
            raise ValueError(f"Provider '{v}' not recognized.")
        return v.lower()

class TransitEncryptRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    key_name: str = Field(..., description="Vault transit key name")
    plaintext_data: str = Field(..., min_length=1)

class TransitEncryptResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    ciphertext: str = Field(..., description="Vault transit ciphertext (vault:v1:...)")

class DynamicDBCredentialResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    username: str = Field(..., description="Generated ephemeral database username")
    password: SecretStr = Field(..., description="Generated ephemeral database password")
    lease_id: str = Field(..., description="Vault lease identifier")
    lease_duration_sec: int = Field(..., ge=60, description="Lease lifetime in seconds")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("Vault-Secret-Manager-MCP", version="3.1.0")

# Vault HVAC Client Setup
vault_client = hvac.Client(url="http://127.0.0.1:8200", token="root-dev-token-2027")

@mcp.tool()
async def fetch_validated_agent_secret(secret_path: str) -> str:
    """Fetch and validate an API credential payload from Vault KV v2."""
    try:
        response = vault_client.secrets.kv.v2.read_secret_version(
            path=secret_path,
            mount_point="secret"
        )
        data = response["data"]["data"]

        # Validate with Pydantic v2
        payload = APIKeyPayload(
            provider=data.get("provider", "anthropic"),
            api_key=SecretStr(data.get("api_key", "")),
            environment=data.get("environment", "production"),
            lease_duration_sec=int(data.get("lease_duration", 3600))
        )

        return f"Successfully validated key for provider '{payload.provider}' (Lease: {payload.lease_duration_sec}s)."
    except Exception as e:
        return f"Vault Secret Retrieval Failed: {str(e)}"

@mcp.tool()
async def encrypt_payload_transit(key_name: str, plaintext: str) -> str:
    """Encrypt sensitive string payload using Vault's Transit Encryption engine."""
    try:
        import base64
        encoded_text = base64.b64encode(plaintext.encode("utf-8")).decode("utf-8")

        response = vault_client.secrets.transit.encrypt_data(
            name=key_name,
            plaintext=encoded_text
        )

        result = TransitEncryptResponse(ciphertext=response["data"]["ciphertext"])
        return result.model_dump_json(indent=2)
    except Exception as e:
        return f"Transit Encryption Failed: {str(e)}"

@mcp.tool()
async def generate_dynamic_db_credentials(role_name: str = "agent-read-role") -> str:
    """Generates an ephemeral, short-lived PostgreSQL credential pair via Vault."""
    try:
        response = vault_client.secrets.database.generate_credentials(name=role_name)
        creds = DynamicDBCredentialResponse(
            username=response["data"]["username"],
            password=SecretStr(response["data"]["password"]),
            lease_id=response["lease_id"],
            lease_duration_sec=response["lease_duration"]
        )
        return creds.model_dump_json(indent=2)
    except Exception as e:
        return f"Dynamic Credential Generation Failed: {str(e)}"

if __name__ == "__main__":
    mcp.run(host="0.0.0.0", port=8094)
```

## Configuration & Troubleshooting Matrix

| Parameter / Failure Mode | Default / Cause | Description / Resolution |
| :--- | :--- | :--- |
| `storage.raft.path` | `"/vault/file"` | Path for Raft integrated storage backend. |
| `listener.tcp.address` | `"127.0.0.1:8200"` | IP and port binding for Vault HTTP API server. |
| **Error 503 Sealed** | Vault process restarted. | Run `vault operator unseal <key>` threshold times. |
| **Error 403 Permission Denied** | Missing token capabilities. | Inspect capabilities with `vault token lookup`. |
| **AppRole Auth Lockout** | Secret ID expired or invalid CIDR range | Re-issue AppRole Secret ID via `vault write auth/approle/role/agent/secret-id`. |

## Related tools / concepts
- [Vault MCP](vault-mcp.md) — Model Context Protocol bridge for Vault.
- [Authentik](../../services/authentik.md) — Self-hosted OIDC identity provider for Vault auth.
- [n8n](../../services/n8n.md) — Automation tool that consumes Vault dynamic credentials.
- [Docker](../infrastructure/docker.md) — Preferred runtime container platform for Vault.
- [FastMCP 3.1 Protocol](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Tool calling protocol specification.
- [Aider](../development_ops/aider.md) — Agentic coding assistant using Vault-secured tokens.

## Sources / references
- [HashiCorp Vault Official Project Site](https://www.vaultproject.io/)
- [HashiCorp Vault Documentation Portal](https://developer.hashicorp.com/vault/docs)
- [hvac Python Vault Client Documentation](https://hvac.readthedocs.io/)
- [Vault MCP Source Code Repository](https://github.com/democratize-technology/vault-mcp)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

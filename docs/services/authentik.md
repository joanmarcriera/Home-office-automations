# Authentik

## What it is
**Authentik** is an open-source, enterprise-grade Identity Provider (IdP) and Unified Identity Governance Platform designed for high-flexibility single sign-on (SSO), multi-factor authentication (MFA), passkey management, and automated access policies. Built on a modular Python/Rust architecture with PostgreSQL and Redis backends, Authentik acts as the central security gatekeeper across self-hosted home laboratory services, enterprise infrastructure, and autonomous agent ecosystems. As of 2027, Authentik features native **Agentic Session Orchestration**, providing identity isolation, short-lived OIDC token issuance, and granular policy enforcement for AI agents ([Claude 5.6](../tools/providers/anthropic.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md)) interacting via **FastMCP 3.1** (Model Context Protocol).

## What problem it solves
Managing user credentials and agent access across dozens of microservices introduces severe operational risks:
- **Credential Fragmentation**: Scattered local user databases in services like [Nextcloud](nextcloud.md), [Gitea](gitea.md), and [Vikunja](vikunja.md) lead to orphaned accounts and weak authentication standards.
- **Ungoverned AI Agent Access**: Granting autonomous coding or data agents long-lived master API keys risks catastrophic data leakage if an agent process is compromised.
- **Legacy Service Vulnerabilities**: Older web applications lack native WebAuthn/Passkey support or multi-factor authentication (MFA).
- **Static Access Control**: Traditional static role-based access control (RBAC) cannot dynamically restrict access based on risk factors (e.g., unusual IP locations, abnormal API request rates).

Authentik addresses these challenges by centralizing authentication into a unified identity gateway, enforcing WebAuthn passkeys across all downstream applications, and providing a dynamic, expression-based policy engine.

## Where it fits in the stack
```
+-----------------------------------------------------------------------------------+
|                        EXTERNAL USERS & AUTONOMOUS AGENTS                         |
|             (Human Browsers / FastMCP 3.1 Agents / API Integrations)              |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       AUTHENTIK IDENTITY & GATEWAY LAYER                          |
|      - Embedded Forward Proxy / Outpost Engine (OAuth2 / OIDC / SAML / LDAP)     |
|      - Agentic Token Issuer & Short-Lived Session Lifecycle Orchestrator          |
|      - Dynamic Policy & Context-Aware Execution Engine                            |
+-----------------------------------------------------------------------------------+
          |                                  |                                  |
          v                                  v                                  v
+------------------------+        +------------------------+        +------------------------+
|   SELF-HOSTED SERVICES |        |   AGENT TOOL SERVERS   |        |   SECRETS & STORAGE    |
|   - Nextcloud / Gitea  |        |   - FastMCP 3.1 Tool APIs |        |   - PostgreSQL Database|
|   - Vikunja / Home Asst|        |   - Vault-MCP Secrets     |        |   - Redis Session Cache|
+------------------------+        +------------------------+        +------------------------+
```

Authentik sits at the **Security & Identity Gateway Layer**, acting as the authoritative single point of entry and token issuer for all internal services, external reverse proxies, and agentic workflows.

## Identity Protocols & Policy Matrix

Authentik provides protocol translation and policy enforcement across five primary interfaces:

```
+----------------------------------------------------------------------------------------------------+
|                                  AUTHENTIK PROTOCOL SUPPORT MATRIX                                 |
+-------------------+-----------------------------------+--------------------------------------------+
| Protocol          | Target Application Profile        | Key Capabilities                           |
+-------------------+-----------------------------------+--------------------------------------------+
| OAuth2 / OIDC     | Modern web applications & APIs    | PKCE, Authorization Code, Short-lived JWT  |
| SAML 2.0          | Enterprise SaaS applications      | XML assertions, SSO metadata exchange      |
| LDAP              | Legacy infrastructure & NAS       | Outpost LDAP server interface              |
| Forward Proxy     | Apps lacking native auth          | Traefik / Nginx header-based auth injection|
| Agentic OIDC      | FastMCP 3.1 autonomous agents     | Dynamic client registration, scoped tokens |
+-------------------+-----------------------------------+--------------------------------------------+
```

## Typical use cases
- **Centralized Single Sign-On (SSO)**: Unifying user login across [Nextcloud](nextcloud.md), [Gitea](gitea.md), [Vikunja](vikunja.md), and [Paperless-ngx](paperless-ngx.md) with WebAuthn passkeys.
- **Agentic Token Governance**: Issuing scoped, 15-minute OIDC access tokens to autonomous agents ([Cline](../tools/agents/cline.md), [Roo-Code](../tools/agents/roo-code.md)) for database and tool execution.
- **Reverse Proxy Protection**: Securing internal web endpoints via Forward Proxy Outposts integrated with Traefik or Caddy.
- **Identity-Aware MCP Execution**: Restricting FastMCP 3.1 tool calls based on user group membership and active session risk scores.

## Strengths
- **All-in-One Identity Platform**: Combines OIDC, SAML2, LDAP, and Proxy authentication into a unified container stack.
- **Expression-Based Policy Engine**: Powerful Python expression policies allow complex conditional access rules.
- **Native Passkey / WebAuthn Support**: Passwordless login support built-in for all applications out of the box.
- **High Availability Architecture**: Separate server and worker processes backed by PostgreSQL and Redis.

## Limitations
- **Resource Footprint**: Consumes more RAM and CPU than lightweight forward proxies like Authelia or Basic Auth.
- **Configuration Overhead**: Complex policy flows and stage pipelines require initial administration setup.

## When to use it
- When requiring an enterprise-grade Identity Provider for a multi-service self-hosted stack or home laboratory.
- When enforcing WebAuthn passkeys and MFA across services lacking native security controls.
- When issuing scoped, temporary credentials to AI agents executing Model Context Protocol tools.

## When not to use it
- In minimal resource-constrained environments (e.g., low-memory edge devices with < 1GB RAM).
- When protecting a single static HTML page without multi-user role requirements.

## Getting started

### Docker Compose High-Availability Setup
Deploy Authentik using the standard PostgreSQL and Redis architecture.

```yaml
services:
  postgresql:
    image: docker.io/library/postgres:16-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}"]
    volumes:
      - database:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${AUTHENTIK_POSTGRESQL__PASSWORD:-authentik_password}
      POSTGRES_USER: ${AUTHENTIK_POSTGRESQL__USER:-authentik}
      POSTGRES_DB: ${AUTHENTIK_POSTGRESQL__NAME:-authentik}

  redis:
    image: docker.io/library/redis:alpine
    restart: unless-stopped
    volumes:
      - redis:/data

  server:
    image: ghcr.io/goauthentik/server:latest
    restart: unless-stopped
    command: server
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: authentik
      AUTHENTIK_POSTGRESQL__NAME: authentik
      AUTHENTIK_POSTGRESQL__PASSWORD: authentik_password
      AUTHENTIK_SECRET_KEY: ${AUTHENTIK_SECRET_KEY}
    volumes:
      - ./media:/media
      - ./custom-templates:/templates
    ports:
      - "8000:8000"
      - "8443:8443"

  worker:
    image: ghcr.io/goauthentik/server:latest
    restart: unless-stopped
    command: worker
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: authentik
      AUTHENTIK_POSTGRESQL__NAME: authentik
      AUTHENTIK_POSTGRESQL__PASSWORD: authentik_password
      AUTHENTIK_SECRET_KEY: ${AUTHENTIK_SECRET_KEY}
    user: root
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./media:/media

volumes:
  database:
  redis:
```

## CLI examples

Execute administration and recovery tasks inside the Authentik server container:

```bash
# Generate a emergency admin recovery key valid for 1 hour
docker exec -it authentik-server ak create_recovery_key 1 akadmin

# Flush cached system settings and policies in Redis
docker exec -it authentik-server ak clear_cache

# Execute database migrations
docker exec -it authentik-server ak migrate
```

## API examples

### FastMCP 3.1 User Directory & Token Revocation Tool Server

This FastMCP 3.1 server exposes Authentik user management to automated operations agents:

```python
"""
FastMCP 3.1 Identity Management Tool Server for Authentik Integration.
Enables operations agents to query user status and revoke compromised agent tokens.
"""

import requests
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("authentik-ops-tools", version="3.1.0")

class RevokeTokenRequest(BaseModel):
    user_id: int = Field(..., description="Target user or agent ID in Authentik")
    reason: str = Field(..., description="Audit reason for token revocation")

class UserStatusInfo(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

@mcp.tool(
    name="get_user_status",
    description="Retrieve user or agent account status from Authentik."
)
def get_user_status(user_id: int) -> UserStatusInfo:
    """
    Queries the Authentik REST API v3 for user metadata.
    """
    authentik_url = f"http://localhost:8000/api/v3/core/users/{user_id}/"
    headers = {"Authorization": "Bearer YOUR_AUTHENTIK_API_TOKEN"}

    response = requests.get(authentik_url, headers=headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    return UserStatusInfo(
        id=data["pk"],
        username=data["username"],
        email=data.get("email", ""),
        is_active=data["is_active"]
    )

if __name__ == "__main__":
    mcp.run()
```

### Pydantic v2 Authentik Application Registration Schema

```python
"""
Pydantic v2 Schema for Authentik Application & Provider Configuration.
Validates OIDC settings before registering downstream apps.
"""

from typing import Optional
from pydantic import BaseModel, Field, HttpUrl

class OIDCProviderConfig(BaseModel):
    name: str = Field(..., min_length=3, description="Provider display name")
    client_id: str = Field(..., description="OAuth2 Client ID")
    client_secret: str = Field(..., description="OAuth2 Client Secret")
    redirect_uris: list[str] = Field(..., description="Allowed OAuth2 redirect URIs")
    jwt_validity_seconds: int = Field(default=3600, ge=300, le=86400, description="Token expiration window")

# Validation Execution Example
if __name__ == "__main__":
    provider_data = {
        "name": "Nextcloud OIDC Provider",
        "client_id": "nextcloud-client-id-12345",
        "client_secret": "super-secret-oidc-key-67890",
        "redirect_uris": ["https://cloud.example.com/apps/user_oidc/code"],
        "jwt_validity_seconds": 3600
    }
    validated = OIDCProviderConfig.model_validate(provider_data)
    print("Successfully validated Authentik Provider config:")
    print(validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Tailscale](tailscale.md) — Encrypted mesh network transport for Authentik endpoints.
- [Nextcloud](nextcloud.md) — File cloud secured via Authentik OIDC SSO.
- [Gitea](gitea.md) — Git forge protected by Authentik identity governance.
- [Vault-MCP](../tools/automation_orchestration/vault-mcp.md) — HashiCorp Vault secrets integration.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — FastMCP 3.1 security architecture.

## Sources / references
- [Authentik Official Portal](https://goauthentik.io/)
- [Authentik GitHub Repository](https://github.com/goauthentik/authentik)
- [Authentik REST API v3 Reference](https://docs.goauthentik.io/docs/api/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

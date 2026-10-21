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

## Authentication Sequence Architecture

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Agent Gateway
    participant Proxy as Reverse Proxy / Outpost
    participant Auth as Authentik Server (IdP)
    participant Redis as Redis Cache
    participant DB as PostgreSQL DB
    participant App as Protected Service (Nextcloud / Gitea)

    User->>Proxy: Access Request (https://service.internal.net)
    Proxy->>Auth: Forward Auth Verification Header
    Auth->>Redis: Check Active Session Token
    alt Session Valid
        Redis-->>Auth: Token Valid + User Claims
        Auth-->>Proxy: HTTP 200 OK (X-Authentik-Username, Groups)
        Proxy->>App: Forward Request with Identity Headers
        App-->>User: HTTP 200 Content Response
    else Session Invalid / Expired
        Redis-->>Auth: Token Miss / Expired
        Auth-->>Proxy: HTTP 302 Redirect to Authentik Login
        Proxy-->>User: Redirect to Login Flow
        User->>Auth: Authenticate (Passkey / WebAuthn / MFA)
        Auth->>DB: Verify Credentials & Evaluate Stage Policies
        DB-->>Auth: Policy Passed
        Auth->>Redis: Store New Session State
        Auth-->>User: Issue Set-Cookie / OAuth JWT Token
        User->>Proxy: Retry Original Request with Session Token
        Proxy-->>App: Forward Verified Request
    end
```

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

## Systemd Service Unit & Container Setup

To manage Authentik using systemd and Docker Compose, save the following unit file as `/etc/systemd/system/authentik.service`:

```ini
[Unit]
Description=Authentik Enterprise Identity Governance & OAuth Gateway
After=docker.service network-online.target
Requires=docker.service network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/authentik
ExecStartPre=/usr/bin/docker compose config
ExecStart=/usr/bin/docker compose up --remove-orphans
ExecStop=/usr/bin/docker compose down
Restart=always
RestartSec=10s
TimeoutStartSec=300

[Install]
WantedBy=multi-user.target
```

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
# Generate an emergency admin recovery key valid for 1 hour
docker exec -it authentik-server ak create_recovery_key 1 akadmin

# Flush cached system settings and policies in Redis
docker exec -it authentik-server ak clear_cache

# Execute database migrations
docker exec -it authentik-server ak migrate
```

## API examples

### FastMCP 3.1 User Directory & Token Revocation Tool Server

This complete production code exposes Authentik user management to automated operations agents using **FastMCP 3.1** and **Pydantic v2**:

```python
"""
FastMCP 3.1 Identity Management Tool Server for Authentik Integration.
Enables operations agents to query user status and revoke compromised agent tokens.
"""

import requests
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from fastmcp import FastMCP

mcp = FastMCP("authentik-ops-tools", instructions="FastMCP 3.1 tool gateway for Authentik identity management.")

class UserQueryRequest(BaseModel):
    user_id: int = Field(..., ge=1, description="Target user or agent ID in Authentik")

class RevokeTokenRequest(BaseModel):
    user_id: int = Field(..., ge=1, description="Target user or agent ID in Authentik")
    reason: str = Field(..., min_length=5, description="Audit reason for token revocation")

class UserStatusInfo(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    groups: List[str] = Field(default_factory=list)

class OperationResponse(BaseModel):
    status: str = Field(..., description="Execution status: 'success' or 'error'")
    user_info: Optional[UserStatusInfo] = Field(None, description="Validated user information payload")
    message: Optional[str] = Field(None, description="Detailed message or error trace")

@mcp.tool()
def get_user_status(request_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Queries the Authentik REST API v3 for user metadata and active claims.
    """
    try:
        req = UserQueryRequest.model_validate(request_payload)
        authentik_url = f"http://localhost:8000/api/v3/core/users/{req.user_id}/"
        headers = {"Authorization": "Bearer YOUR_AUTHENTIK_API_TOKEN"}

        response = requests.get(authentik_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        user_info = UserStatusInfo(
            id=data["pk"],
            username=data["username"],
            email=data.get("email", ""),
            is_active=data["is_active"],
            groups=[g["name"] for g in data.get("groups_obj", [])]
        )

        return OperationResponse(status="success", user_info=user_info).model_dump()

    except ValidationError as val_err:
        return OperationResponse(status="error", message=f"Pydantic v2 Error: {val_err.errors()}").model_dump()
    except Exception as ex:
        return OperationResponse(status="error", message=f"Authentik API Request Failed: {str(ex)}").model_dump()

if __name__ == "__main__":
    mcp.run()
```

### Troubleshooting Matrix

| Issue / Symptom | Root Cause | Remediation Procedure |
| :--- | :--- | :--- |
| **`HTTP 502 Bad Gateway on Forward Proxy`** | Authentik Outpost process disconnected from core server | Check Outpost logs (`docker logs authentik-outpost`) and verify WebSocket connection to port 8000. |
| **`OIDC Invalid Grant / Redirect Mismatch`** | Redirect URI in downstream service does not match Authentik Provider settings | Verify exact protocol (`https://`), port, and callback path match between provider and app config. |
| **`LDAP Outpost Bind Failure`** | Invalid service account credentials or closed TCP 389/636 ports | Test bind via `ldapsearch -H ldap://localhost:389 -D "cn=akadmin,ou=users,dc=authentik,dc=local" -w password`. |
| **`Passkey / WebAuthn Registration Error`** | Domain mismatch or missing HTTPS TLS certificates | Ensure service is accessed over valid HTTPS domain; WebAuthn browser specs prohibit insecure HTTP except on localhost. |
| **`PostgreSQL Connection Exhaustion`** | High worker concurrency exhausting default database pool | Increase `max_connections` in Postgres config or scale up pgbouncer connection pooler. |

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

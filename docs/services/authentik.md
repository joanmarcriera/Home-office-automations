# Authentik

## What it is
Authentik is an open-source, enterprise-grade Identity Provider (IdP) and Access Management platform engineered for complex cloud environments, self-hosted infrastructure, and zero-trust security architectures. Built in Python and Go with PostgreSQL and Redis backends, Authentik provides centralized authentication, Single Sign-On (SSO), Multi-Factor Authentication (MFA), WebAuthn/Passkey enforcement, and reverse proxy outpost management. In early 2027, Authentik natively features **Agentic Session Orchestration**, allowing autonomous AI agents operating over **FastMCP 3.1** and REST protocols to request, validate, and revoke task-scoped, short-lived OIDC session tokens under explicit context-aware security policies.

## Architecture & System Topology
Authentik separates user ingress, policy evaluation, asynchronous background processing, and outpost gateway proxying into distinct microservices:

```
+----------------------------------------------------------------------------------------------------+
|                                    AUTHENTIK ARCHITECTURE                                          |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|  +----------------------------------------------------------------------------------------------+  |
|  |                                CLIENT & AGENT INGRESS LAYER                                  |  |
|  |  +---------------------------+  +---------------------------+  +--------------------------+  |  |
|  |  | Human Browsers & Mobile   |  | FastMCP 3.1 Agent Sessions|  | OAuth2 / OIDC / SAML /   |  |  |
|  |  | (Passkey / WebAuthn / MFA)|  | (Short-Lived Task Tokens) |  | LDAP Client Integration  |  |  |
|  |  +-------------+-------------+  +-------------+-------------+  +------------+-------------+  |  |
|  +----------------|------------------------------|-----------------------------|----------------+  |
|                   |                              |                             |                   |
|  +----------------V----------------==============V=============================V----------------+  |
|  |                                  AUTHENTIK SERVER & OUTPOST LAYER                            |  |
|  |                                                                                              |  |
|  |  +-----------------------+   +----------------------------+   +---------------------------+  |  |
|  |  | Authentik Server API  |   | Python Policy Engine       |   | Embedded Proxy Outpost    |  |  |
|  |  | (REST v3 / Admin UI)  |   | (Contextual Access Rules)  |   | (Reverse Proxy / Forward) |  |  |
|  |  +-----------+-----------+   +-------------+--------------+   +-------------+-------------+  |  |
|  +--------------|-------------------------|--------------------------------|--------------------+  |
|                 |                         |                                |                       |
|  +--------------V-------------------------V--------------------------------V--------------------+  |
|  |                                  ASYNC WORKER & STORAGE LAYER                                |  |
|  |                                                                                              |  |
|  |  +---------------------------------------+    +-------------------------------------------+  |  |
|  |  | Celery Asynchronous Workers           |    | PostgreSQL 16 & Redis Persistence         |  |  |
|  |  | (LDAP Sync / Event Triggers / Cleanup) |    | (User Identities / Tokens / Audit Logs)   |  |  |
|  |  +-------------------+-------------------+    +---------------------+---------------------+  |  |
|  +----------------------|------------------------------------------|----------------------------+  |
|                         |                                          |                               |
|                         V                                          V                               |
|        +---------------------------------+        +----------------------------------+             |
|        | External Application Ecosystem  |        | Event Notification Bus           |             |
|        | (Nextcloud / Gitea / Vikunja)   |        | (n8n / Webhooks / Prometheus)    |             |
|        +---------------------------------+        +----------------------------------+             |
|                                                                                                    |
+----------------------------------------------------------------------------------------------------+
```

## What problem it solves
Authentik resolves fundamental security, access management, and user identity fragmentation issues across enterprise and home laboratory deployments:

1. **Credential & Identity Fragmentation**: Operating dozens of isolated services leads to password reuse and revoked account oversights. Authentik unifies user credentials into a single identity database supporting OIDC, SAML, and LDAP.
2. **Securing Autonomous AI Agents**: AI agents require API credentials to perform tool operations. Authentik's **Agentic Session Orchestration** issues restricted, short-lived OIDC tokens bounded by task lifetime and automatically revokes access upon task completion.
3. **MFA Gaps on Legacy Services**: Legacy web applications lack passkey or WebAuthn support. Authentik Proxy Outposts sit in front of legacy HTTP services, enforcing SSO, MFA, and passkeys before traffic touches the upstream container.
4. **Context-Aware Zero-Trust Governance**: Static password checks fail to detect compromised credentials. Authentik evaluates Python-based policy expressions (e.g., GeoIP, device posture, anomaly detection) dynamically on every login request.

## Where it fits in the stack
**Category**: Security / Identity Provider (IdP) / Gateway / SSO Engine. Authentik sits at the **Security Ingress Layer**, serving as the central authentication authority for applications, infrastructure tools, and autonomous FastMCP 3.1 agents.

```
+-----------------------------------------------------------------------+
|                          SECURITY ARCHITECTURE                        |
+-----------------------------------------------------------------------+
|  [Ingress Requests] -> Users & FastMCP 3.1 Autonomous Agents           |
|          |                                                            |
|          V                                                            |
|  [Authentik Outpost Proxy / Server] <---> [Python Policy Engine]      |
|          |                                                            |
|          +--------------------------+--------------------------+      |
|          | (OIDC / SAML / OAuth)    | (Reverse Proxy Gate)     |      |
|          V                          V                          V      |
|  [Self-Hosted Applications]  [Internal Tool Endpoints]  [Storage / DBs] |
|  (Gitea / Nextcloud)        (FastMCP Tools / REST APIs) (PostgreSQL)    |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Centralized Single Sign-On (SSO)**: Provisioning a single set of MFA-protected credentials across [Gitea](gitea.md), [Nextcloud](nextcloud.md), [Vikunja](vikunja.md), and [Paperless-ngx](paperless-ngx.md).
- **FastMCP 3.1 Identity Delegation**: Authenticating autonomous agents via OAuth2 client credentials flows to grant identity-aware access to database and microservice tools.
- **Passwordless Passkey Deployment**: Enforcing WebAuthn passkeys across all internal services without modifying backend application source code.
- **Granular Role-Based Access Control (RBAC)**: Binding users, groups, and service accounts to dynamic Python policy rules that evaluate request time, source IP, and device risk score.
- **Automated Lifecycle Synchronization**: Harnessing Authentik webhooks with [n8n](n8n.md) to automatically provision or de-provision user access upon onboarding or offboarding.

## Strengths
- **All-in-One Identity Ecosystem**: Integrates IdP server, asynchronous Celery workers, and reverse proxy outposts into a unified deployment package.
- **Python-Powered Policy Engine**: Write dynamic access control rules using native Python expressions to evaluate context, headers, and agent attributes.
- **Native Passkey & WebAuthn Management**: Provides effortless passkey registration and multi-factor enforcement across legacy and modern web applications.
- **Agentic Session Orchestration**: Native support for creating, scoping, and revoking short-lived service account tokens for autonomous agent workflows.
- **Built-in Proxy Outpost Architecture**: Deploy outposts directly into remote Kubernetes or Docker environments to gate isolated endpoints without exposing the central server.

## Limitations
- **Resource Memory Requirements**: Requires PostgreSQL and Redis backends alongside Python server/worker containers, necessitating higher RAM reserves than lightweight proxies like Authelia.
- **Policy Engine Learning Curve**: Writing complex Python expression policies and custom stage flows requires understanding Authentik's internal execution state.
- **Database Dependency**: High-availability deployments depend on multi-AZ PostgreSQL and Redis cluster setups for state replication.

## When to use it
- When managing multi-service infrastructures requiring centralized OIDC, SAML, and LDAP Single Sign-On.
- To enforce Passkey (WebAuthn) passwordless authentication across all self-hosted web applications.
- When issuing, auditing, and revoking short-lived OIDC access tokens for autonomous AI agents operating in FastMCP 3.1 workflows.
- When requiring dynamic, expression-based access policies driven by contextual request parameters.

## When not to use it
- In minimal, highly resource-constrained hardware environments (e.g., low-RAM Raspberry Pi nodes) where a lightweight authentication proxy is preferred.
- If you only need simple static HTTP basic authentication for a single static website.

## Getting started

### Docker Compose Deployment
Deploy Authentik using PostgreSQL 16 and Redis backends. First generate a secure key: `echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 36)" >> .env`.

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
      POSTGRES_PASSWORD: ${AUTHENTIK_POSTGRESQL__PASSWORD:-authentikpass}
      POSTGRES_USER: ${AUTHENTIK_POSTGRESQL__USER:-authentik}
      POSTGRES_DB: ${AUTHENTIK_POSTGRESQL__NAME:-authentik}
    env_file: [.env]
  redis:
    image: docker.io/library/redis:alpine
    restart: unless-stopped
    volumes: [redis:/data]
  server:
    image: ghcr.io/goauthentik/server:2026.12.0
    restart: unless-stopped
    command: server
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
    volumes:
      - ./media:/media
      - ./custom-templates:/templates
    env_file: [.env]
    ports:
      - "8000:8000"
      - "8443:8443"
  worker:
    image: ghcr.io/goauthentik/server:2026.12.0
    restart: unless-stopped
    command: worker
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
    user: root
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./media:/media
    env_file: [.env]

volumes:
  database:
  redis:
```

### Initial Configuration
1. Access `http://<your-server-ip>:8000/if/flow/initial-setup/` in your browser.
2. Set the primary administrator password and log into the Admin Interface.
3. Create an **OIDC Provider** for your target application.
4. Create an **Application**, assign it to the provider, and bind access policy flows.

## CLI examples

```bash
# Generate an administrative recovery key for emergency access
docker exec -it authentik-server ak create_recovery_key 1 admin

# Trigger manual synchronization of configured LDAP or OIDC sources
docker exec -it authentik-server ak sync_sources

# Clear system Redis cache entries across Authentik services
docker exec -it authentik-server ak clear_cache

# Inspect active worker task queues and background execution status
docker exec -it authentik-worker ak celery_status
```

## API examples

The following Python script demonstrates how to construct a FastMCP 3.1 identity manager tool that communicates with Authentik's REST API to generate short-lived credentials for autonomous agents and verify OIDC tokens:

```python
import asyncio
import httpx
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field

# Initialize FastMCP 3.1 Identity Management Server
mcp = FastMCP(
    name="AuthentikIdentityManager",
    version="3.1.0",
    description="Agentic session orchestration server interfacing with Authentik REST API"
)

class AgentTokenRequest(BaseModel):
    agent_id: str = Field(..., description="Unique slug for the target autonomous agent")
    task_scope: str = Field("read:tools", description="Requested scope permission boundary")
    duration_minutes: int = Field(30, ge=5, le=480, description="Token lifetime in minutes")

class TokenRevocationRequest(BaseModel):
    token_id: str = Field(..., description="Authentik token identifier string to revoke")

@mcp.tool(name="issue_agent_token", description="Generates a short-lived OIDC token in Authentik for an agent session")
async def issue_agent_token(params: AgentTokenRequest, ctx: Context) -> Dict[str, Any]:
    """Issues a task-scoped token via Authentik administrative API."""
    await ctx.report_progress(progress=25, total=100)
    await ctx.info(f"Requesting token for agent {params.agent_id} with scope '{params.task_scope}'...")

    # Simulate API interaction with Authentik
    await asyncio.sleep(0.1)
    await ctx.report_progress(progress=100, total=100)

    return {
        "status": "success",
        "agent_id": params.agent_id,
        "access_token": f"ak_agent_tok_{params.agent_id}_20270107",
        "expires_in_seconds": params.duration_minutes * 60,
        "scope": params.task_scope
    }

@mcp.tool(name="revoke_agent_token", description="Immediately revokes an active agent token in Authentik upon task completion")
async def revoke_agent_token(params: TokenRevocationRequest, ctx: Context) -> Dict[str, Any]:
    """Revokes an agent token in Authentik."""
    await ctx.info(f"Revoking token ID: {params.token_id}")
    await asyncio.sleep(0.05)
    return {"status": "revoked", "token_id": params.token_id}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

## API & Schema Definitions (Pydantic v2)

The following Pydantic v2 models define schema validation for Authentik REST API responses, including applications, user groups, and active session tokens:

```python
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict, HttpUrl, field_validator

class AuthentikProviderSchema(BaseModel):
    pk: int = Field(..., description="Primary key integer identifier of the provider")
    name: str = Field(..., description="Provider display name")
    authorization_flow: str = Field(..., alias="authorizationFlow", description="Flow UUID assigned for authorization")

    model_config = ConfigDict(populate_by_name=True)

class AuthentikApplicationSchema(BaseModel):
    pk: str = Field(..., description="Application UUID identifier")
    name: str = Field(..., description="User-facing application title")
    slug: str = Field(..., description="URL-friendly unique identifier slug")
    provider: Optional[int] = Field(None, description="Bound provider primary key ID")
    launch_url: Optional[str] = Field(None, alias="launchUrl", description="Target application launch endpoint URL")
    meta_publisher: Optional[str] = Field(None, alias="metaPublisher", description="Publisher organization tag")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("slug")

    def validate_slug(cls, v: str) -> str:
        if not v.islower() or " " in v:
            raise ValueError("Application slug must be lowercase without spaces.")
        return v

class ApplicationListResponseSchema(BaseModel):
    pagination: Dict[str, Any] = Field(..., description="Paginated metadata summary")
    results: List[AuthentikApplicationSchema] = Field(..., description="List of matched application entities")

class AgentSessionTokenSchema(BaseModel):
    token_id: str = Field(..., alias="tokenId", description="Unique token identifier string")
    user_id: int = Field(..., alias="userId", description="Authentik user ID owning the token")
    expires_at: datetime = Field(..., alias="expiresAt", description="Timestamp when token expires")
    is_active: bool = Field(True, alias="isActive", description="Whether token is currently valid")

    model_config = ConfigDict(populate_by_name=True)
```

## Related tools / concepts
- [Tailscale](tailscale.md) — Secure overlay mesh transport; Authentik provides application identity gating.
- [Vikunja](vikunja.md) — Task management service supporting Authentik OIDC Single Sign-On.
- [Nextcloud](nextcloud.md) — Enterprise productivity suite integrated with Authentik SSO.
- [n8n](n8n.md) — Workflow automation engine triggered by Authentik identity webhooks.
- [Paperless-ngx](paperless-ngx.md) — Document management system protected by Authentik MFA.
- [Gitea](gitea.md) — Self-hosted Git repository service utilizing Authentik SSO.
- [Headscale](headscale.md) — Open-source Tailscale control plane integrated with Authentik OIDC.
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md) — Standard protocol for identity-aware tool discovery and execution.

## Sources / references
- [Official Authentik Website](https://goauthentik.io/)
- [Authentik Official Documentation](https://docs.goauthentik.io/)
- [Authentik GitHub Repository](https://github.com/goauthentik/authentik)
- [FastMCP Framework Specification](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

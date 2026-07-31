# Authentik

## What it is
Authentik is an open-source Identity Provider (IdP) designed for extreme flexibility and modern security workflows. In November 2026, it natively supports **Agentic Session Orchestration**, allowing for granular, automated creation, monitoring, and revocation of user and autonomous agent/bot sessions. It supports a wide array of protocols including OAuth2, OpenID Connect (OIDC), SAML, and LDAP, making it the primary gatekeeper for agentic environments.

## What problem it solves
Managing separate credentials for dozens of self-hosted applications creates security risks and user friction. Authentik centralizes identity management, providing a single point of authentication for services like [Nextcloud](nextcloud.md), [Gitea](gitea.md), and [Vikunja](vikunja.md). It also injects modern security features like Multi-Factor Authentication (MFA) and Passkeys into legacy applications and provides **Gemini 4.0** or **Gemma 3**-driven policy reasoning for complex access rules.

## Where it fits in the stack
**Category**: Service / Security / Identity. Authentik sits at the **Security and Gateway layer**, acting as the primary gatekeeper for all homelab services and agentic tool endpoints. It integrates with **MCP 3.1** to provide identity-aware tool execution for autonomous agents.

## Typical use cases
- **Single Sign-On (SSO)**: One account to rule all self-hosted services.
- **Agentic Session Orchestration**: Automatically creating or revoking session tokens for agents based on task-specific requirements.
- **Passkey Enforcement**: Implementing industry-leading passwordless authentication across all internal services.
- **Context-Aware Policies**: Using **Gemma 3** to analyze login patterns and dynamically adjust security requirements.
- **Application Portal**: A centralized hub for accessing authorized services and agentic tools.

## Strengths
- **All-in-One Architecture**: Includes server, worker, and outpost in a single ecosystem.
- **Powerful Policy Engine**: Allows for complex rules based on IP, Geo-location, and agent behavior.
- **Native Passkey Support**: Seamless implementation of WebAuthn for all applications.
- **FastMCP 3.1 Integration**: High-performance outposts for securing distributed tool endpoints.
- **Customizable Flows**: Visually designed login and enrollment processes.

## Limitations
- **Resource Usage**: Requires more memory and CPU than simpler alternatives like Authelia.
- **Complexity**: The powerful policy engine has a steep learning curve.
- **Infrastructure Requirements**: Depends on PostgreSQL and Redis for operation.

## When to use it
- When you need a unified, enterprise-grade Identity Provider for a multi-service homelab.
- To implement Passkeys (WebAuthn) across all self-hosted applications.
- When providing secure, audited access to internal services for **Gemma 3** agents.
- For complex, context-aware access policies requiring AI-driven reasoning.

## When not to use it
- In extremely resource-constrained environments (e.g., low-RAM Raspberry Pi).
- If you only require simple, basic authentication for a single static page.

## Getting started

### Docker Compose (November 2026 Baseline)
Deploy Authentik using the official Docker Compose baseline. First, generate a secret key: `echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 36)" >> .env`.

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
      POSTGRES_PASSWORD: ${AUTHENTIK_POSTGRESQL__PASSWORD}
      POSTGRES_USER: ${AUTHENTIK_POSTGRESQL__USER:-authentik}
      POSTGRES_DB: ${AUTHENTIK_POSTGRESQL__NAME:-authentik}
    env_file: [.env]
  redis:
    image: docker.io/library/redis:alpine
    restart: unless-stopped
    volumes: [redis:/data]
  server:
    image: ghcr.io/goauthentik/server:latest
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
    image: ghcr.io/goauthentik/server:latest
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

### Hello World
1. Navigate to `http://<your-ip>:8000/if/admin/`.
2. Set the initial admin password.
3. Create a **Provider** (e.g., OIDC) for a test service.
4. Create an **Application** and bind it to the provider.
5. Access your newly secured service via the Authentik dashboard!

## CLI examples
Management tasks within the Authentik server container:

```bash
# Create a recovery key for the admin user
docker exec -it authentik-server ak create_recovery_key 1 admin

# Sync all LDAP or OIDC sources
docker exec -it authentik-server ak sync_sources

# Clear the Authentik system cache
docker exec -it authentik-server ak clear_cache
```

## API examples
Authentik features a comprehensive REST API (v3) for automated identity management.

### Python: Listing Applications and validation with Pydantic v2
This Python script accesses the Authentik API to query configured applications and validates response schema via **Pydantic v2**.

```python
import requests
from pydantic import BaseModel, Field
from typing import List, Optional

# Define validation schema using Pydantic v2
class AuthentikApplication(BaseModel):
    name: str = Field(..., description="The user-facing application name")
    slug: str = Field(..., description="The URL-friendly slug")
    provider: Optional[int] = Field(None, description="The ID of the bound provider")
    launch_url: Optional[str] = Field(None, description="The launch URL", alias="launch_url")

class ApplicationListResponse(BaseModel):
    results: List[AuthentikApplication]

def get_validated_applications(token: str) -> List[AuthentikApplication]:
    url = "http://localhost:8000/api/v3/core/applications/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Perform validation with Pydantic v2
    validated_data = ApplicationListResponse.model_validate(response.json())
    return validated_data.results
```

### FastMCP 3.1: Token Refresh Tool
```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("authentik-identity-manager");

mcp.addTool({
  name: "refresh_agent_token",
  description: "Refresh an OIDC token for an autonomous agent",
  parameters: { agentId: { type: "string" } },
  execute: async ({ agentId }) => {
    // Logic to call Authentik API for token refresh
    return { token: "new-oidc-token-november-2026", expiresAt: "2026-11-05T..." };
  }
});

mcp.serve();
```

## Related tools / concepts
- [Tailscale](tailscale.md) — For secure transport; Authentik handles identity.
- [Vikunja](vikunja.md) — Uses Authentik for OIDC-based authentication.
- [Nextcloud](nextcloud.md) — Centralized login via Authentik SSO.
- [n8n](n8n.md) — For automating user and agent lifecycle events.
- [Home Assistant](home-assistant.md) — Secure access management via Authentik.
- [Paperless-ngx](paperless-ngx.md) — Protecting documents with MFA.
- [Gitea](gitea.md) — Managing Git repositories with SSO.
- [Headscale](headscale.md) — Managing private mesh identities.
- [Ollama](ollama.md) — Authenticating agentic traffic to local LLM endpoints.
- [MCP 3.1](../tools/automation_orchestration/mcp.md) — Protocol for identity-aware tool and resource discovery.

## Sources / References
- [Official Website](https://goauthentik.io/)
- [Authentik Documentation](https://docs.goauthentik.io/)
- [GitHub Repository](https://github.com/goauthentik/authentik)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)

## Contribution Metadata
- Last reviewed: 2026-11-05
- Confidence: high

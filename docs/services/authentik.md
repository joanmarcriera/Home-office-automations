# Authentik

## What it is
Authentik is an open-source Identity Provider (IdP) designed for extreme flexibility and modern security workflows. In June 2026, version **2026.6** has introduced "Agentic Session Orchestration," allowing for granular, automated control of user and bot sessions. It supports a wide array of protocols including OAuth2, OpenID Connect (OIDC), SAML, and LDAP.

## What problem it solves
Managing separate credentials for dozens of self-hosted applications creates security risks and user friction. Authentik centralizes identity management, providing a single point of authentication for services like [Nextcloud](nextcloud.md), [Gitea](gitea.md), and [Vikunja](vikunja.md). It also injects modern security features like Multi-Factor Authentication (MFA) and Passkeys into legacy applications that don't natively support them.

## Where it fits in the stack
**Category**: Service / Security / Identity. Authentik sits at the **Security and Gateway layer**, acting as the primary gatekeeper for all homelab services and agentic tool endpoints.

## Typical use cases
- **Single Sign-On (SSO)**: One account to rule all self-hosted services.
- **MFA Injection**: Requiring TOTP or WebAuthn for access to a legacy router or dashboard.
- **User Enrollment**: Clean, branded sign-up flows for family members or colleagues.
- **Application Portal**: A centralized "hub" showing all authorized applications.
- **Agentic Session Revocation**: Automatically locking down an account via [n8n](n8n.md) if an agent detects suspicious activity.

## Strengths
- **All-in-One Architecture**: Includes server, worker, and outpost in a single, well-integrated ecosystem.
- **Powerful Policy Engine**: Allows for complex, context-aware access rules based on IP, Geo-location, or user groups.
- **Native Passkey Support**: Industry-leading implementation of passwordless authentication.
- **Flexible Outposts**: Simplifies integration with reverse proxies (Traefik, Nginx) for proxy-based authentication.
- **Customizable Flows**: Every step of the login, enrollment, or recovery process can be visually designed or scripted.

## Limitations
- **Resource Usage**: Requires more memory and CPU than simpler alternatives like Authelia.
- **Complexity**: The sheer power of its policy engine can be overwhelming for beginners.
- **Infrastructure Requirements**: Depends on PostgreSQL and Redis for operation.

## When to use it
- When you need a unified, enterprise-grade Identity Provider for a multi-service homelab.
- To implement Passkeys (WebAuthn) across all your self-hosted applications.
- When you require complex access policies (e.g., "only allow access from my home country").
- For providing secure, audited access to internal services for autonomous agents.

## When not to use it
- In extremely resource-constrained environments (e.g., a low-spec Raspberry Pi with limited RAM).
- If you only need simple, basic authentication for a single web page.

## Licensing and cost
- **Licensing**: Open Source (GPL-3.0).
- **Cost**: Free for self-hosting. Authentik Enterprise offers paid support and advanced features for organizations.
- **Self-hostable**: Yes, officially supported via Docker and Kubernetes.

## Getting started

### Docker Compose (v2026.6 Baseline)
Deploy Authentik using the official Docker Compose baseline. First, generate a secret key: `echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 36)" >> .env`.

```yaml
version: "3.4"

services:
  postgresql:
    image: docker.io/library/postgres:16-alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}"]
      start_period: 20s
      interval: 30s
      retries: 5
      timeout: 5s
    volumes:
      - database:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: ${AUTHENTIK_POSTGRESQL__PASSWORD}
      POSTGRES_USER: ${AUTHENTIK_POSTGRESQL__USER:-authentik}
      POSTGRES_DB: ${AUTHENTIK_POSTGRESQL__NAME:-authentik}
    env_file:
      - .env
  redis:
    image: docker.io/library/redis:alpine
    command: --save 60 1 --loglevel warning
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping | grep PONG"]
      start_period: 20s
      interval: 30s
      retries: 5
      timeout: 5s
    volumes:
      - redis:/data
  server:
    image: ghcr.io/goauthentik/server:2026.6
    restart: unless-stopped
    command: server
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: ${AUTHENTIK_POSTGRESQL__USER:-authentik}
      AUTHENTIK_POSTGRESQL__NAME: ${AUTHENTIK_POSTGRESQL__NAME:-authentik}
      AUTHENTIK_POSTGRESQL__PASSWORD: ${AUTHENTIK_POSTGRESQL__PASSWORD}
    volumes:
      - ./media:/media
      - ./custom-templates:/templates
    env_file:
      - .env
    ports:
      - "${COMPOSE_PORT_HTTP:-8000}:8000"
      - "${COMPOSE_PORT_HTTPS:-8443}:8443"
    depends_on:
      - postgresql
      - redis
  worker:
    image: ghcr.io/goauthentik/server:2026.6
    restart: unless-stopped
    command: worker
    environment:
      AUTHENTIK_REDIS__HOST: redis
      AUTHENTIK_POSTGRESQL__HOST: postgresql
      AUTHENTIK_POSTGRESQL__USER: ${AUTHENTIK_POSTGRESQL__USER:-authentik}
      AUTHENTIK_POSTGRESQL__NAME: ${AUTHENTIK_POSTGRESQL__NAME:-authentik}
      AUTHENTIK_POSTGRESQL__PASSWORD: ${AUTHENTIK_POSTGRESQL__PASSWORD}
    user: root
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./media:/media
      - ./certs:/certs
      - ./custom-templates:/templates
    env_file:
      - .env
    depends_on:
      - postgresql
      - redis

volumes:
  database:
    driver: local
  redis:
    driver: local
```

### Hello World
1. Navigate to `http://<your-ip>:8000/if/admin/`.
2. Set your initial admin password.
3. Create a **Provider** (e.g., OIDC) for a test application.
4. Create an **Application** and bind it to the provider to see your first SSO-enabled service.

## CLI examples
Perform management tasks within the Authentik server container:

```bash
# Create a recovery key for the admin user
docker exec -it authentik-server ak create_recovery_key 1 admin

# Sync all LDAP sources
docker exec -it authentik-server ak sync_ldaps

# Run database migrations manually
docker exec -it authentik-server ak migrate

# Clear the Authentik cache
docker exec -it authentik-server ak clear_cache
```

## API examples
Authentik features a comprehensive REST API for automated identity management.

### Python: Listing Applications via API
```python
import requests

URL = "http://localhost:8000/api/v3/core/applications/"
TOKEN = "YOUR_API_TOKEN"

def list_apps():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(URL, headers=headers)
    return response.json()

# Example usage
apps = list_apps()
for app in apps.get('results', []):
    print(f"Application: {app['name']}, Slug: {app['slug']}")
```

## Related tools / concepts
- [Tailscale](tailscale.md) — For secure transport; Authentik handles the identity.
- [Vikunja](vikunja.md) — Uses Authentik for OIDC-based user authentication.
- [Nextcloud](nextcloud.md) — Centralized login via Authentik SSO.
- [n8n](n8n.md) — For automating user lifecycle events (onboarding/offboarding).
- [Home Assistant](home-assistant.md) — Secure access management via Authentik.
- [Paperless-ngx](paperless-ngx.md) — Protecting sensitive documents with MFA.
- [Gitea](gitea.md) — For managing Git repositories with SSO.
- [Traefik](traefik.md) — For proxy-based authentication with Authentik Outposts.
- [Cloudflare Mesh](cloudflare-mesh.md) — For zero-trust networking integration.
- [Headscale](headscale.md) — Managing private mesh identities.
- [Ollama](ollama.md) — Authenticating agentic traffic to local LLM endpoints.

## Sources / References
- [Official Website](https://goauthentik.io/)
- [Authentik Documentation](https://docs.goauthentik.io/)
- [GitHub Repository](https://github.com/goauthentik/authentik)
- [Passkey (WebAuthn) Guide](https://docs.goauthentik.io/docs/stages/authenticator_webauthn/)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high

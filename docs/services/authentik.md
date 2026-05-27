# Authentik

Authentik is an open-source Identity Provider that emphasizes flexibility and versatility.

## What it is
Authentik is a comprehensive identity management solution that functions as an Identity Provider (IdP). It supports modern protocols like OAuth2, OpenID Connect (OIDC), and SAML, as well as legacy protocols like LDAP and Radius.

## What problem it solves
It centralizes user management across dozens of different self-hosted applications. Instead of managing separate usernames and passwords for [Nextcloud](nextcloud.md), [Gitea](gitea.md), and [Vikunja](vikunja.md), users log in once to Authentik. It also adds security layers like Multi-Factor Authentication (MFA) to applications that don't natively support it.

## Where it fits in the stack
Authentik sits at the **Security and Gateway Layer**. It often integrates with a reverse proxy (like Traefik or Nginx) to intercept requests and ensure the user is authenticated before they ever reach the internal application.

## Typical use cases
- **Single Sign-On (SSO)**: One account for all homelab services.
- **MFA Injection**: Requiring a YubiKey or TOTP code to access a legacy web app.
- **User Enrollment**: Providing a clean sign-up flow for family members or friends.
- **Application Portal**: A centralized dashboard showing all authorized apps.
- **Account Lockdown (v2026.5)**: Immediate session revocation and account deactivation in case of suspected compromise.

## Strengths
- **All-in-One**: Includes the server, worker, and outpost in a single ecosystem.
- **Extremely Flexible**: Custom flows and stages allow for complex logic.
- **Native Passkey Support**: Easy implementation of passwordless login with improved Secure Enclave support in 2026.
- **Outpost Architecture**: Simplifies integration with reverse proxies.
- **Enterprise-Grade Conditional Access**: Integration with Fleet and Google Chrome Device Trust for posture-based access.

## Limitations
- **Resource Intensive**: Requires more RAM and CPU than simpler alternatives like Authelia.
- **High Complexity**: The powerful policy engine has a steep learning curve.
- **Component Heavy**: Requires a database (Postgres) and a cache (Redis) to function.

## When to use it
- When you need a unified authentication provider for multiple services using OAuth2, SAML, or LDAP.
- When you want a highly customizable Identity Provider with a powerful policy engine.
- When you need to provide Single Sign-On (SSO) for legacy applications via an outpost.

## When not to use it
- When you need a very simple, lightweight authentication layer (consider [Authelia](https://www.authelia.com/) or simple reverse proxy basic auth).
- When you are not comfortable managing a complex service with multiple components (PostgreSQL, Redis, Worker, Server).

## Getting started

### Preparation
Generate a secret key and a PostgreSQL password:

```bash
echo "AUTHENTIK_SECRET_KEY=$(openssl rand -base64 36)" >> .env
echo "AUTHENTIK_POSTGRESQL__PASSWORD=$(openssl rand -base64 36)" >> .env
```

### Docker Compose (v2026.5 Baseline)
Create a `docker-compose.yml` file:

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
    image: ghcr.io/goauthentik/server:2026.5
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
    image: ghcr.io/goauthentik/server:2026.5
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

## CLI examples

Authentik management tasks can be performed using the `ak` command within the server container:

```bash
# Create a recovery key for a user
docker exec -it authentik-server-1 ak create_recovery_key 1 admin

# Sync LDAP sources
docker exec -it authentik-server-1 ak sync_ldaps

# Run migrations
docker exec -it authentik-server-1 ak migrate
```

## API examples

Authentik has a comprehensive REST API. Use an API Token for authentication:

```bash
# List all users
curl -X GET "http://localhost:8000/api/v3/core/users/" \
     -H "Authorization: Bearer <your_api_token>" \
     -H "Accept: application/json"

# v2026.5: Lock down a user account via API
curl -X POST "http://localhost:8000/api/v3/core/users/<user_id>/lockdown/" \
     -H "Authorization: Bearer <your_api_token>"
```

## Related tools / concepts
- [Tailscale](tailscale.md)
- [Headscale](headscale.md)
- [Nextcloud](nextcloud.md)
- [Gitea](gitea.md)
- [Vikunja](vikunja.md)
- [n8n](n8n.md) — For automating account lifecycle events
- [ChangeDetection.io](changedetection.md) — Monitoring security policy changes

## Family 2FA Onboarding

To secure family member accounts, it is recommended to enforce Two-Factor Authentication (2FA). Authentik supports TOTP (authenticator apps) and WebAuthn (Passkeys/Security Keys).

### Enforcing 2FA for Users
1. **Create a TOTP Stage**: In the Admin interface, go to *Flows and Stages* -> *Stages* and create a new *TOTP Authenticator Stage*.
2. **Update Enrollment Flow**: Add the TOTP stage to your default user enrollment flow to ensure new members set it up immediately.
3. **Policy-based Enforcement**: Create a *Policy* that checks if a user has a 2FA device registered. Apply this policy to sensitive applications to require 2FA on login.

### Passkey Support
Authentik natively supports WebAuthn. Family members can register their phone or a hardware key (like a YubiKey) as a Passkey under their user profile settings.

## Advanced Security Policies

Authentik's power lies in its Policy engine, allowing for sophisticated access control based on context.

### Geo-IP Blocking
To prevent logins from unexpected countries, you can use a Geo-IP policy.

1.  **Configure Geo-IP**: Ensure Authentik is configured with a MaxMind or IP2Location database.
2.  **Create Expression Policy**:
    ```python
    # Expression Policy: Only allow logins from Switzerland and local network

    # Allow local RFC1918 addresses
    if ak_is_in_network(context['http_request'].META['REMOTE_ADDR'], '192.168.0.0/16'):
        return True

    # Check country code from Geo-IP
    geo_data = context.get('geoip', {})
    if geo_data.get('country', {}).get('iso_code') == 'CH':
        return True

    ak_message("Access denied from your current location.")
    return False
    ```
3.  **Bind Policy**: Bind this policy to your "Main-Flow" or specific sensitive applications.

### Device Posture Checks (User-Agent Validation)
While not a substitute for mTLS or MDM, you can restrict access to specific browser types or known family devices.

```python
# Expression Policy: Restrict to specific Browser/OS
user_agent = context['http_request'].META.get('HTTP_USER_AGENT', '')

# Example: Only allow access from the family's preferred browser setup
if "Linux" in user_agent and "Firefox" in user_agent:
    return True

ak_message("Please use the approved family browser configuration for this service.")
return False
```

## LDAP Outpost Integration

Authentik provides an LDAP Outpost to allow legacy applications that only support LDAP to authenticate against Authentik's user database and policy engine.

### Configuration
1.  **Create an LDAP Provider**: Go to **Resources > Providers** and create an **LDAP Provider**.
    -   **Base DN**: `dc=ldap,dc=goauthentik,dc=io`
    -   **Bind Flow**: A flow that handles authentication (e.g., default-authentication-flow).
2.  **Create an LDAP Outpost**: Go to **Applications > Outposts** and create a new **Outpost**.
    -   **Type**: LDAP.
    -   **Service Connection**: Select your Docker or Kubernetes connection.
3.  **Deploy the Outpost**: Authentik will provide a Docker Compose snippet for the outpost. Run it alongside your main Authentik stack.

### Client Example (Python)
Legacy apps can then bind to the LDAP outpost (usually port 389 or 636):

```python
import ldap

# Configuration
LDAP_SERVER = "ldap://authentik-outpost:389"
BIND_DN = "cn=akadmin,ou=users,dc=ldap,dc=goauthentik,dc=io"
BIND_PASSWORD = "your_password"

try:
    conn = ldap.initialize(LDAP_SERVER)
    conn.simple_bind_s(BIND_DN, BIND_PASSWORD)
    print("LDAP Bind Successful")
except ldap.LDAPError as e:
    print(f"LDAP Error: {e}")
```

## Backlog
- [x] Perform quarterly technical freshness audit (2026-05-27).
- [x] Configure LDAP outpost for legacy apps.

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-05-27

## Sources / References
- [Authentik Official Site](https://goauthentik.io/)
- [Authentik Documentation](https://docs.goauthentik.io/)
- [Keycloak Official Site](https://www.keycloak.org/)

# Authentik

Authentik is an open-source Identity Provider that emphasizes flexibility and versatility.

## Description
It allows you to integrate various authentication sources and provide Single Sign-On (SSO) for all your applications.

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

### Docker Compose
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
    image: ghcr.io/goauthentik/server:latest
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
    image: ghcr.io/goauthentik/server:latest
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
```

## Links
- [Official Website](https://goauthentik.io/)
- [Documentation](https://docs.goauthentik.io/)

## Alternatives
- [Keycloak](https://www.keycloak.org/)
- [Authelia](https://www.authelia.com/)

## Family 2FA Onboarding

To secure family member accounts, it is recommended to enforce Two-Factor Authentication (2FA). Authentik supports TOTP (authenticator apps) and WebAuthn (Passkeys/Security Keys).

### Enforcing 2FA for Users
1. **Create a TOTP Stage**: In the Admin interface, go to *Flows and Stages* -> *Stages* and create a new *TOTP Authenticator Stage*.
2. **Update Enrollment Flow**: Add the TOTP stage to your default user enrollment flow to ensure new members set it up immediately.
3. **Policy-based Enforcement**: Create a *Policy* that checks if a user has a 2FA device registered. Apply this policy to sensitive applications to require 2FA on login.

### Passkey Support
Authentik natively supports WebAuthn. Family members can register their phone or a hardware key (like a YubiKey) as a Passkey under their user profile settings.

## Backlog
- Configure LDAP outpost for legacy apps.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-04-18

## Sources / References
- https://goauthentik.io/
- https://docs.goauthentik.io/
- https://www.keycloak.org/

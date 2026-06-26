# SSO Solutions Comparison (Self-Hosted)

## What it is
A comparative analysis of self-hosted Single Sign-On (SSO) and Identity and Access Management (IAM) solutions. These platforms enable users to use a single set of secure credentials to access multiple independent software systems within a homelab or enterprise environment. In June 2026, the focus has shifted toward high-performance, security-first identities like Kanidm and minimalist LDAP directories like LLDAP.

## What problem it solves
Managing separate usernames and passwords for dozens of self-hosted services (Nextcloud, Gitea, etc.) is insecure and leads to "password fatigue." SSO centralizes authentication, enables mandatory Multi-Factor Authentication (MFA) or WebAuthn across all services, and simplifies the lifecycle management (onboarding/offboarding) of users.

## Where it fits in the stack
SSO sits in the **Identity and Access** layer of the infrastructure stack. It typically integrates with a directory service (like LDAP or Kanidm's internal store) and provides standardized authentication protocols—OIDC (OpenID Connect), SAML 2.0, and OAuth2—to application-layer services.

## Typical use cases
- **Homelab Consolidation**: Unifying access to Gitea, Nextcloud, and Home Assistant dashboards.
- **Enterprise-Lite**: Providing OIDC/SAML for small business internal tools with professional-grade security.
- **Legacy Support**: Using LLDAP to provide authentication for older applications that only support the LDAP protocol.
- **Agentic Authentication**: Allowing Claude 4.8 or GPT-5.5 agents to authenticate securely via OIDC to retrieve data from private services.

## Strengths

### Authentik
- **Versatility**: Support for almost every modern protocol (OIDC, SAML, OAuth2, LDAP).
- **Outpost System**: Built-in proxy and LDAP outposts for protecting applications that don't natively support SSO.
- **Extensive UI**: Rich web-based interface for complex policy and flow management.

### Kanidm
- **Security-First**: Written in Rust with high security defaults (e.g., mandatory WebAuthn support).
- **Performance**: Extremely fast and lightweight compared to Java or Python-based alternatives.
- **Modern Architecture**: Built from the ground up to replace legacy tools like OpenLDAP.

### LLDAP
- **Simplicity**: Tiny resource footprint, perfect for low-power hardware like Raspberry Pi 5.
- **Ease of Setup**: Focused purely on providing a clean, modern LDAP interface.

## Limitations

### Authentik
- **Resource Intensive**: Requires significant RAM and CPU to run multiple containers (server, worker, PostgreSQL, Redis).
- **Complexity**: The flexibility comes with a steep learning curve for configuring "Flows" and "Stages."

### Kanidm
- **Strict Requirements**: Requires proper TLS/SSL setup and DNS configuration to function, which can be difficult for beginners.
- **Protocol Gap**: Primarily focuses on OIDC and LDAPS; SAML support is less mature than Authentik.

### LLDAP
- **Protocol Limited**: Only supports LDAP; requires a bridge (like Authelia or Authentik) to provide OIDC/SAML.

## When to use it
- Use **Authentik** if you need an all-in-one "Identity Provider" (IdP) that can handle everything from social logins to legacy LDAP proxying.
- Use **Kanidm** if you prioritize security and performance and prefer a modern, CLI-centric workflow for managing your "Source of Truth."
- Use **LLDAP** if you only need a simple, reliable directory for a few apps that support LDAP and want to keep resource usage minimal.

## When not to use it
- Avoid full SSO stacks for single-user setups; simple basic auth or Tailscale's built-in auth may suffice.
- Avoid **Authentik** on 1GB RAM nodes; it will likely crash or suffer from performance degradation.
- Avoid **LLDAP** if you need modern OIDC flows (unless paired with another tool).

## Getting started

### Authentik Setup
Deploy via Docker Compose:
```bash
docker compose up -d
# Access the initial setup flow
curl -X GET http://localhost:9000/if/flow/initial-setup/
```

### Kanidm Initialization
Initialize the server and retrieve the admin credentials:
```bash
kanidmd recover-account idm_admin
```

### LLDAP Deployment
Run the LLDAP container and access the management interface:
```bash
docker run -p 17170:17170 -p 3890:3890 lldap/lldap:latest
```

## CLI examples

### Authentik Management
While primarily UI-driven, Authentik exposes a CLI for system status:
```bash
ak system status
ak whoami
```

### Kanidm CLI
The `kanidm` CLI is the primary way to manage users and groups:
```bash
kanidm person create jules "Jules Agent"
kanidm group create automation-agents
kanidm group add-members automation-agents jules
```

### LLDAP CLI Integration
Using standard `ldapsearch` with LLDAP:
```bash
ldapsearch -H ldap://localhost:3890 -D "uid=admin,ou=people,dc=example,dc=com" -W -b "dc=example,dc=com"
```

## API examples

### OIDC Discovery Endpoint
All modern SSO providers expose a discovery URL for client configuration:
```text
GET https://sso.example.com/application/o/gitea/.well-known/openid-configuration
```

### Kanidm OIDC Client Creation via API
```bash
kanidm system oauth2 create gitea "Gitea Instance" https://gitea.example.com/oauth2/callback
```

### Authentik REST API
Authentik is fully API-driven; you can create users programmatically:
```bash
curl -H "Authorization: Bearer $API_TOKEN" \
     -X POST https://authentik.example.com/api/v3/core/users/ \
     -d '{"username": "newuser", "name": "New User", "email": "user@example.com"}'
```

## Related tools / concepts
- [Authentik](../services/authentik.md) — The primary all-in-one SSO recommendation for homelabs.
- [n8n](../services/n8n.md) — For automating user onboarding/offboarding workflows via API.
- [Tailscale](../services/tailscale.md) — For securing SSO endpoints and providing identity-based networking.
- [Authentik LDAP Outpost](../services/authentik.md) — Bridge OIDC-only IDPs to legacy LDAP apps.
- [OIDC vs SAML](../knowledge_base/patterns/tool-calling-and-mcp.md) — Understanding modern auth protocols.
- [Nextcloud](../services/nextcloud.md) — Example of a service requiring robust SSO integration.
- [Authelia](https://www.authelia.com/) — A lightweight alternative for proxy-based authentication.
- [Gitea](../services/gitea.md) — Integrates natively with OIDC and LDAP providers.
- [Authentik OIDC Provider](../services/authentik.md) — Connecting external apps to your identity store.
- [WebAuthn/FIDO2](../knowledge_base/home-lab-hardware-guide.md) — Passwordless standards supported by modern SSO.

## Sources / References
- [Authentik Documentation](https://docs.goauthentik.io/)
- [Kanidm Project Page](https://kanidm.github.io/kanidm/)
- [LLDAP GitHub Repository](https://github.com/lldap/lldap)
- [OAuth 2.0 and OpenID Connect Explained](https://openid.net/developers/specs/)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high

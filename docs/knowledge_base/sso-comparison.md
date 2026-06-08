# SSO Solutions Comparison (Self-Hosted)

## What it is
This document provides a comparative analysis of self-hosted Single Sign-On (SSO) and Identity and Access Management (IAM) solutions. These tools allow users to use a single set of credentials to access multiple independent software systems within a homelab or enterprise environment.

## What problem it solves
Managing separate usernames and passwords for dozens of self-hosted services (Nextcloud, Gitea, etc.) is insecure and cumbersome. SSO centralizes authentication, enables Multi-Factor Authentication (MFA) across all services, and simplifies user onboarding and offboarding.

## Where it fits in the stack
SSO sits in the **Identity and Access** layer of the infrastructure stack. It typically integrates with a directory service (like LDAP) or acts as the directory itself, providing authentication protocols like OIDC (OpenID Connect), SAML, and OAuth2 to application-layer services.

## Comparison Matrix

| Feature | Authentik | Kanidm | LLDAP (Lightweight) |
| :--- | :--- | :--- | :--- |
| **Primary Focus** | Modern, multi-protocol (OIDC, SAML, LDAP) | Identity-first, high security, Rust-based | Minimalist LDAP provider |
| **User Interface** | Comprehensive web-based admin & user portal | Modern web UI + robust CLI | Minimalist web UI |
| **Protocols** | OIDC, SAML, LDAP, OAuth2 | OIDC, LDAPS | LDAP only |
| **Ease of Use** | Medium (lots of features) | Medium (security-focused defaults) | High (for simple setups) |
| **Resource Usage** | High (multiple containers) | Low/Medium | Very Low |

## Typical use cases
- **Homelab Consolidation**: Unifying access to Gitea, Nextcloud, and Home Assistant.
- **Enterprise-Lite**: Providing OIDC/SAML for small business internal tools.
- **Legacy Support**: Using LLDAP to provide authentication for older apps that only support LDAP.

## Strengths
- **Authentik**: Extremely flexible, built-in outpost system for proxying non-SSO apps.
- **Kanidm**: High security standards, native support for WebAuthn, very fast Rust implementation.
- **LLDAP**: Very low footprint, extremely simple to configure, perfect for low-power hardware.

## Limitations
- **Authentik**: High resource consumption, can be overwhelming for beginners.
- **Kanidm**: Strict requirements for certificates and DNS, steep learning curve for advanced config.
- **LLDAP**: Limited to LDAP protocol (no native OIDC/SAML without a bridge like Authelia).

## When to use it
- Use **Authentik** if you need a "do everything" solution with a great UI.
- Use **Kanidm** if you prioritize security and performance and prefer a CLI-first workflow.
- Use **LLDAP** if you only need a simple directory for apps that support LDAP.

## When not to use it
- Don't use a full SSO stack if you only have 1-2 services (use simple basic auth).
- Don't use Authentik on a Raspberry Pi with low RAM (it will likely struggle).

## Getting started

### Authentik
The easiest way to start is via Docker Compose.
```bash
docker compose up -d
```
Access the initial setup at `http://<your-ip>:9000/if/flow/initial-setup/`.

### Kanidm
Initialize the server and create the admin account:
```bash
kanidmd recover-account idm_admin
```

### LLDAP
Deploy via Docker, then access the web UI at port `17170` to create your first user.

## CLI examples

### Authentik (ak CLI)
Authenticate and check session status:
```bash
ak config setup
ak system status
ak whoami
```

### Kanidm
Create a new person and add to a group:
```bash
kanidm person create john.doe "John Doe"
kanidm group create developers
kanidm group add-members developers john.doe
```

### LLDAP (lldap-cli)
List users and add a new user to a group:
```bash
lldap-cli user list
lldap-cli user group add jsmith "mail users"
```

## API examples

### OIDC Configuration (Generic)
Most SSO providers will provide a discovery endpoint:
```text
https://sso.example.com/application/o/app-name/.well-known/openid-configuration
```

### Kanidm OIDC Client Creation
```bash
kanidm system oauth2 create gitea "Gitea" https://gitea.example.com/oauth2/callback
```

### Authentik App Security
To protect an application with OIDC, you define a **Provider** and an **Application** in the Authentik UI, then use the Client ID and Secret in your app.

## Related tools / concepts
- [Authentik](../services/authentik.md): Modern all-in-one SSO.
- [n8n](../services/n8n.md): Automate user onboarding across SSO systems.
- [Home Assistant](../services/home-assistant.md): Integrate SSO for family members.
- [Tailscale](../services/tailscale.md): Secure your SSO endpoints.
- [Gitea](../services/gitea.md): Example service that integrates with SSO via OIDC/LDAP.
- [Nextcloud](../services/nextcloud.md): Supports both LDAP and OIDC for centralized auth.
- [Paperless-ngx](../services/paperless-ngx.md): Can be integrated with Authentik via proxy or OIDC.

## Sources / references
- [Authentik Official Docs](https://docs.goauthentik.io/)
- [Kanidm Official Docs](https://kanidm.github.io/kanidm/)
- [LLDAP GitHub](https://github.com/lldap/lldap)
- [Identity Management on Homelab (Reddit)](https://www.reddit.com/r/homelab/comments/17q8j9f/identity_management_and_sso_for_the_homelab/)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high

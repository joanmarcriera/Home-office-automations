# SSO Solutions Comparison (Self-Hosted)

## What it is
A comparative analysis of self-hosted Single Sign-On (SSO) and Identity and Access Management (IAM) solutions. These platforms enable users to use a single set of secure credentials to access multiple independent software systems within a homelab or enterprise environment. In early January 2027, the focus has shifted toward high-performance, security-first identities like Kanidm, minimalist LDAP directories like LLDAP, and native support for the FastMCP 3.1 Task Protocol for multi-agent credential delegation.

## What problem it solves
Managing separate usernames and passwords for dozens of self-hosted services (Nextcloud, Gitea, etc.) is insecure and leads to "password fatigue." SSO centralizes authentication, enables mandatory Multi-Factor Authentication (MFA) or WebAuthn across all services, and simplifies the lifecycle management (onboarding/offboarding) of users. For autonomous AI agent swarms (e.g., using Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, or Gemma 4), central SSO is crucial to handle programmatic access without exposing raw passwords.

## Where it fits in the stack
SSO sits in the **Identity and Access** layer of the infrastructure stack. It typically integrates with a directory service (like LDAP or Kanidm's internal store) and provides standardized authentication protocols—OIDC (OpenID Connect), SAML 2.0, and OAuth2—to application-layer services, as well as sandboxed agent authentication tokens.

## Typical use cases
- **Homelab Consolidation**: Unifying access to Gitea, Nextcloud, and Home Assistant dashboards.
- **Enterprise-Lite**: Providing OIDC/SAML for small business internal tools with professional-grade security.
- **Legacy Support**: Using LLDAP to provide authentication for older applications that only support the LDAP protocol.
- **Agentic Authentication**: Allowing Claude 5.6, Llama 4, Qwen 3.6 VL, or GPT-5.6 agents to authenticate securely via OIDC token exchange (FastMCP 3.1 Task Protocol) to retrieve data from private services without master keys.

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
All modern SSO platforms expose REST and OIDC APIs. Programmatic integration, token verification, and credential delegation are managed via strict schemas.

### 1. Robust User Provisioning & Token Exchange Validation (Python)
This script demonstrates programmatic user creation and OIDC token schema validation using strict Pydantic v2 schemas.

```python
import json
import requests
from datetime import datetime, timezone
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, EmailStr, HttpUrl

class SSOUser(BaseModel):
    username: str = Field(..., min_length=2, description="Unique login identifier")
    name: str = Field(..., description="Full display name")
    email: EmailStr = Field(..., description="User's primary email address")
    groups: List[str] = Field(default_factory=list)
    is_active: bool = Field(True)

class OIDCTokenExchange(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    expires_in: int = Field(..., ge=0)
    refresh_token: Optional[str] = None
    scope: str
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def provision_sso_user(api_url: str, token: str, user: SSOUser) -> dict:
    """Provisions a new user in the Identity Provider (e.g., Authentik)."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, data=user.model_dump_json(), headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        # Example validation of provisioned user schema
        new_agent = SSOUser(
            username="jules-agent",
            name="Jules Automation Agent",
            email="jules@example.com",
            groups=["automation-agents", "homelab-access"]
        )
        print("SSO User payload validated:", new_agent.model_dump_json(indent=2))

        # Example validation of received OIDC token exchange
        mock_token_response = {
            "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ...",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "openid profile email"
        }
        validated_token = OIDCTokenExchange.model_validate(mock_token_response)
        print("OIDC Token Exchange validated:", validated_token.model_dump_json(indent=2))

    except Exception as e:
        print("Validation Failed:", str(e))
```

### 2. OIDC Discovery Endpoint
All modern SSO providers expose a discovery URL for client configuration:
```text
GET https://sso.example.com/application/o/gitea/.well-known/openid-configuration
```

### 3. Kanidm OIDC Client Creation via API
```bash
kanidm system oauth2 create gitea "Gitea Instance" https://gitea.example.com/oauth2/callback
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
- Last reviewed: 2027-01-07
- Confidence: high

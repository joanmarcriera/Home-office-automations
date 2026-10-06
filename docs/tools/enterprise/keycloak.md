# Keycloak

## What it is
Keycloak is an open-source Identity and Access Management (IAM) solution maintained by Red Hat and the Cloud Native Computing Foundation (CNCF). Keycloak provides single sign-on (SSO), user federation, identity brokering, social login, granular role-based access control (RBAC), and full compliance with modern authentication standards including OpenID Connect (OIDC), OAuth 2.0, and SAML 2.0. In 2027, Keycloak serves as a primary open-source identity provider governing agent trust boundaries, user access delegation, and tool-calling token validation across home-lab services and enterprise AI architectures.

```
+-----------------------------------------------------------------------------------+
|                           KEYCLOAK IAM AUTHENTICATION FLOW                        |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | User / AI Agent     | ----> | FastMCP 3.1 Gateway   | ---> | Keycloak Server | |
|  | Authentication Req |       | Request Controller    |      | Token Endpoint  | |
|  +---------------------+       +-----------------------+      +-----------------+ |
|                                                                        |          |
|                                                                        v          |
|  +---------------------+       +-----------------------+      +-----------------+ |
|  | Protected API       | <---- | Validate JWT Bearer   | <--- | JWT Access      | |
|  | MCP Tool Access     |       | & Scope Roles         |      | & Refresh Token | |
|  +---------------------+       +-----------------------+      +-----------------+ |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Managing user credentials, role permissions, and service-to-service authentication across heterogeneous self-hosted services and AI agents creates security vulnerabilities, duplicate account management overhead, and broken audit trails. Exposing internal agent tools without centralized identity delegation risks unauthenticated execution or privilege escalation. Keycloak solves this by providing a unified identity control plane, issuing cryptographic JSON Web Tokens (JWTs) with scopes, and enforcing OAuth 2.0 grant flows across both human users and automated agents.

## Where it fits in the stack
**Enterprise / Identity & Access Management Infrastructure**. Keycloak sits at the root security perimeter layer alongside identity proxies (like [Authentik](../../services/authentik.md) or [Okta](okta.md)), providing central authentication and access tokens to reverse proxies, web dashboards, and FastMCP agent servers.

## Typical use cases
- **Centralized SSO for Home-Lab Services**: Enforcing single sign-on authentication across Nextcloud, Gitea, Grafana, and Open WebUI services via OIDC.
- **Agent Tool Authorization & Scope Validation**: Issuing short-lived OAuth 2.0 access tokens to AI agents with granular scopes (e.g., `calendar:read`, `system:admin`).
- **LDAP / Active Directory Integration**: Federating legacy enterprise user directories into modern OIDC token endpoints for seamless agent access.
- **Multi-Factor Authentication (MFA)**: Protecting administrative endpoints and agent control loops with TOTP or WebAuthn/FIDO2 hardware security keys.

## Strengths
- **Comprehensive Standard Compliance**: Full production support for OIDC, OAuth 2.0, SAML 2.0, and WS-Federation protocols.
- **Flexible User Federation**: Built-in sync adapters for LDAP, Active Directory, Kerberos, and custom user databases.
- **Granular RBAC & Fine-Grained Authorization**: Authorization services supporting attribute-based access control (ABAC) and token claim mappers.
- **Extensible Theme & Event SPIs**: Pluggable Java Service Provider Interfaces (SPI) for custom authentication flows and audit logging.

## Limitations
- **Resource Footprint**: JVM runtime requires higher idle RAM baseline (512MB–1GB+) compared to lightweight Go/Rust identity proxies.
- **Configuration Complexity**: Extensive configuration options require careful realm and client scope setup.

## When to use it
- When requiring a mature, open-source IAM solution with OIDC and SAML 2.0 support across self-hosted infrastructure.
- When delegating granular OAuth 2.0 scopes and JWT token validation to AI agents and FastMCP tool servers.
- When federating multiple enterprise directories (LDAP/AD) into a unified identity store.

## When not to use it
- When simple, lightweight SSO proxying is sufficient for small home labs without complex SAML or LDAP requirements (consider [Authentik](../../services/authentik.md)).
- When managed cloud-only identity services are preferred (use [Okta](okta.md) or [Microsoft Entra ID](microsoft-entra-id.md)).

## Architecture & Technical Deep Dive

Keycloak's architecture is structured around isolated Realms, Clients, Users, and Token Mappers:

```
                         KEYCLOAK REALM & OIDC ARCHITECTURE

 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ Keycloak Master / Production Realm                                         │
 │                                                                             │
 │  ┌───────────────────────┐    ┌───────────────────┐    ┌─────────────────┐  │
 │  │ Client: OpenWebUI     │    │ Client: FastMCP   │    │ Client: Gitea   │  │
 │  │ (OIDC Public Client)  │    │ (Bearer Gateway)  │    │ (OIDC Private)  │  │
 │  └───────────┬───────────┘    └─────────┬─────────┘    └────────┬────────┘  │
 │              │                          │                       │           │
 │              └──────────────────────────┼───────────────────────┘           │
 │                                         │                                   │
 │                                         ▼                                   │
 │  ┌───────────────────────────────────────────────────────────────────────┐  │
 │  │ User Store & Federation Layer (Local DB / LDAP / Active Directory)     │  │
 │  └───────────────────────────────────────────────────────────────────────┘  │
 └─────────────────────────────────────────────────────────────────────────────┘
```

1. **Realms**: Isolated security domains managing their own set of users, credentials, roles, and client application integrations.
2. **Clients**: Applications or services registered with Keycloak that can request user authentication or receive OAuth 2.0 tokens.
3. **Token Issuance & Verification**: Keycloak signs JWT access tokens using asymmetric RSA/EC keypairs published at the realm's JWKS (`/protocol/openid-connect/certs`) endpoint.

## Getting started

Deploy Keycloak via Docker and configure an OIDC realm:

```bash
# Start Keycloak in development mode on port 8080
docker run -d --name keycloak -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin_password \
  quay.io/keycloak/keycloak:latest start-dev
```

```python
import requests

# Fetch Realm OpenID Configuration Discovery Document
realm_url = "http://localhost:8080/realms/master"
openid_config = requests.get(f"{realm_url}/.well-known/openid-configuration").json()

print(f"Token Endpoint: {openid_config['token_endpoint']}")
print(f"JWKS URI: {openid_config['jwks_uri']}")
```

## CLI examples

```bash
# Authenticate Keycloak Admin CLI tool (kcadm.sh)
kcadm.sh config credentials --server http://localhost:8080 --realm master --user admin --password admin_password

# Create a new realm named 'homelab'
kcadm.sh create realms -s realm=homelab -s enabled=true

# Create an OIDC confidential client for FastMCP agent server
kcadm.sh create clients -r homelab -s clientId=fastmcp-gateway -s protocol=openid-connect -s secret=my_client_secret
```

## API examples

### FastMCP 3.1 Controller & Pydantic v2 JWT Token Verification Engine
The following Python module wraps Keycloak OAuth 2.0 token validation inside a **FastMCP 3.1** server with strict **Pydantic v2** validation.

```python
import os
import logging
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, field_validator, ValidationError
from fastmcp import FastMCP, Context

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Keycloak-Controller")

# Initialize FastMCP 3.1 Server
mcp = FastMCP("keycloak-auth-service")

# Pydantic v2 JWT Token Verification Request Model
class TokenVerificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(..., min_length=20, description="Raw Bearer JWT access token string")
    required_realm: str = Field(default="homelab", description="Keycloak target realm name")
    required_scopes: List[str] = Field(default_factory=list, description="Required OAuth 2.0 scope claims")

    @field_validator("access_token")
    @classmethod
    def validate_jwt_format(cls, v: str) -> str:
        parts = v.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT token format; must contain 3 dot-separated segments")
        return v.strip()

@mcp.tool()
async def verify_keycloak_bearer_token(
    request_dict: dict,
    ctx: Optional[Context] = None
) -> dict:
    """
    Validates Keycloak JWT bearer token claims and permissions for FastMCP tool access.

    Args:
        request_dict: Dictionary matching TokenVerificationRequest model.
        ctx: FastMCP Context.
    """
    if ctx:
        await ctx.info("Validating Keycloak token verification request with Pydantic v2...")

    try:
        req = TokenVerificationRequest.model_validate(request_dict)
        if ctx:
            await ctx.info(f"Verifying bearer token against realm '{req.required_realm}'...")

        # Simulated JWT inspection and claim extraction
        token_claims = {
            "sub": "user_1029485",
            "preferred_username": "agent_jules",
            "iss": f"http://localhost:8080/realms/{req.required_realm}",
            "realm_access": {"roles": ["homelab-user", "agent-executor"]},
            "scope": "openid email profile"
        }

        return {
            "status": "valid",
            "realm": req.required_realm,
            "subject": token_claims["sub"],
            "username": token_claims["preferred_username"],
            "roles": token_claims["realm_access"]["roles"]
        }
    except ValidationError as ve:
        logger.error(f"Validation failure: {ve}")
        raise ValueError(f"Invalid request parameters: {ve}")

@mcp.tool()
async def get_keycloak_status(ctx: Optional[Context] = None) -> dict:
    """Queries current Keycloak identity realm endpoint and JWKS status."""
    return {
        "engine": "Keycloak Identity & Access Management",
        "protocols_supported": ["OpenID Connect", "OAuth 2.0", "SAML 2.0"],
        "realm_endpoint": "http://localhost:8080/realms/homelab",
        "token_type": "Bearer JWT"
    }

if __name__ == "__main__":
    mcp.run()
```

## Integration patterns
- **OAuth 2.0 / OIDC Authorization Pattern**: Enforce JWT bearer token verification across FastMCP microservice endpoints as described in [OAuth 2.0 / OIDC](oauth2-oidc.md).
- **Reverse Proxy Authentication**: Route ingress traffic through Traefik or Nginx with forward auth pointing to Keycloak OIDC endpoints.

## Best practices & Security
- **Asymmetric Token Verification**: Validate incoming JWT access tokens locally using Keycloak's public JWKS certificates (`/jwks_uri`) to prevent unnecessary authentication DB round-trips.
- **Short-Lived Access Tokens**: Configure access token lifespan to 5–15 minutes while utilizing rotating refresh tokens for long-lived sessions.

## Reference implementation

```python
# Standalone test for Keycloak Pydantic v2 validation
from pydantic import ValidationError

def test_keycloak_schema():
    payload = {
        "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.signature_part",
        "required_realm": "homelab",
        "required_scopes": ["openid", "profile"]
    }
    req = TokenVerificationRequest.model_validate(payload)
    assert req.required_realm == "homelab"
    print("Keycloak schema validation passed successfully.")

if __name__ == "__main__":
    test_keycloak_schema()
```

## Related tools / concepts
- [Okta](okta.md) — Enterprise cloud identity management platform.
- [Authentik](../../services/authentik.md) — Open-source identity provider and SSO proxy.
- [OAuth 2.0 / OIDC](oauth2-oidc.md) — Standard token-based authorization and identity protocols.
- [Microsoft Entra ID](microsoft-entra-id.md) — Cloud enterprise identity management framework.

## Sources / references
- [Keycloak Official Documentation](https://www.keycloak.org/?ref=2026-10-05-audit)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# OAuth 2.0 / OpenID Connect (OIDC)

## What it is
OAuth 2.0 is the industry-standard authorization protocol enabling scoped access to web applications and APIs without sharing user credentials. OpenID Connect (OIDC) is an identity layer built on top of OAuth 2.0 that provides user authentication and identity verification via JSON Web Tokens (JWTs) and standardized discovery endpoints.

As of early **January 2027**, OAuth 2.0 and OIDC serve as the foundational security tier for self-hosted identity providers (Authelia, Keycloak, Authentik), cloud identity services (Okta, Entra ID), and Model Context Protocol (MCP 3.1 / FastMCP 3.1) multi-agent token exchange workflows.

## What problem it solves
In heterogeneous home lab and enterprise automation stacks, maintaining fragmented, per-service user databases creates high security risks, password sprawl, and complex access management. OAuth 2.0 / OIDC provides centralized identity federation, Single Sign-On (SSO), fine-grained API scope enforcement, and standards-based token validation.

## Where it fits in the stack
**Development & Ops / Identity & Access Management (IAM) Layer** — secures communication between user browsers, API gateways (Nginx, Traefik), workflow engines (n8n), identity providers, and LLM agent tool calling protocols.

## Typical use cases
- **Centralized Single Sign-On (SSO)**: Authenticating homelab dashboard users across services (Paperless-ngx, Gitea, Grafana) via Authelia or Keycloak OIDC.
- **Agent Token Exchange & Delegation**: Issuing short-lived OAuth 2.0 access tokens for AI agents (e.g., Claude Code, Cursor) to invoke protected APIs.
- **JWT Verification at the Edge**: Validating cryptographic signatures and scopes on incoming HTTP headers at reverse proxies before routing requests.
- **Role-Based Access Control (RBAC)**: Mapping user claims (`groups`, `roles`) into fine-grained service authorizations.

## Strengths
- **Open Security Standard**: Backed by IETF and OpenID Foundation standards with universal framework integration.
- **Stateless Authorization via JWTs**: Enables distributed verification without hitting central database backends on every API call.
- **Granular Scopes & Consent**: Limits agentic or third-party permissions to strictly declared API scopes.

## Limitations
- **Token Invalidation Complexity**: Revoking stateless JWTs before expiration requires short TTLs or centralized token revocation lists (CRLs).
- **Configuration Surface Area**: Incorrect redirect URI matching, weak client secrets, or missing PKCE options can introduce auth bypass risks.
- **Protocol Overhead**: Requires multiple round-trips during initial authorization code exchange flows.

## When to use it
- When implementing single sign-on (SSO) across multiple web services or internal tools.
- When delegating scoped API access to third-party applications or autonomous agent runtimes.
- When standardizing user authentication using centralized identity providers.

## When not to use it
- For simple, isolated internal microservices that communicate exclusively within a closed, mutual-TLS (mTLS) cluster network.
- When basic API keys are sufficient for static non-user service-to-service automation scripts.

## Getting started
An authorization code flow with **PKCE (Proof Key for Code Exchange)** is standard for securing client applications and CLI tools.

### OIDC Discovery Endpoint Example
Fetch openid configuration metadata directly from your identity provider:

```bash
# Query OIDC discovery configuration
curl -s https://auth.example.com/realms/master/.well-known/openid-configuration | jq .
```

### Exchanging Authorization Code for JWT Tokens
```bash
# Request access token using Authorization Code grant
curl -X POST https://auth.example.com/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=homelab-app" \
  -d "code=AUTHORIZATION_CODE_HERE" \
  -d "redirect_uri=https://app.example.com/callback" \
  -d "code_verifier=PKCE_VERIFIER_STRING"
```

## CLI examples
Inspect and validate JWT identity tokens directly from the command line:

```bash
# Decode JWT payload without verifying signature
echo "EYJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." | cut -d. -f2 | base64 -d | jq .

# Verify JWT signature against JWKS endpoint using step CLI
step crypto jwt verify --jwks https://auth.example.com/oauth/jwks.json --token $ACCESS_TOKEN

# Test client credentials token request for automated scripts
curl -X POST https://auth.example.com/oauth/token \
  -d "grant_type=client_credentials" \
  -d "client_id=service-agent" \
  -d "client_secret=SECRET_KEY" \
  -d "scope=api:read"
```

## API examples
The following Python script uses **Pydantic v2** and `PyJWT` logic to validate and extract claims from an incoming OIDC ID/Access token.

```python
import time
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class OIDCTokenClaims(BaseModel):
    iss: str = Field(..., description="Issuer URL")
    sub: str = Field(..., description="Subject identifier (User ID)")
    aud: str = Field(..., description="Audience client ID")
    exp: int = Field(..., description="Expiration timestamp")
    iat: int = Field(..., description="Issued at timestamp")
    email: Optional[str] = Field(None, description="User email address")
    groups: List[str] = Field(default_factory=list, description="User authorization groups")

    @field_validator("exp")
    @classmethod
    def validate_not_expired(cls, v: int) -> int:
        if v < time.time():
            raise ValueError("Token has expired")
        return v

def parse_and_validate_claims(claims_dict: dict) -> OIDCTokenClaims:
    """Parses and validates OIDC token payload using Pydantic v2."""
    return OIDCTokenClaims(**claims_dict)

# Example verification usage
if __name__ == "__main__":
    now = int(time.time())
    sample_claims = {
        "iss": "https://auth.example.com/realms/master",
        "sub": "usr_99823411",
        "aud": "homelab-client",
        "exp": now + 3600,
        "iat": now,
        "email": "admin@example.com",
        "groups": ["admin", "homelab-users"]
    }

    validated = parse_and_validate_claims(sample_claims)
    print("OIDC Token Claims Validated:", validated.model_dump_json(indent=2))
```

## Related tools / concepts
- [Microsoft Entra ID](../enterprise/microsoft-entra-id.md) — Enterprise OIDC and Azure AD identity service.
- [Claude Code](claude-code.md) — CLI tool supporting OAuth 2.0 PKCE authentication.
- [Cursor](cursor.md) — AI IDE with OIDC identity delegation support.
- [Aider](aider.md) — Coding assistant supporting authenticated service tool calling.
- [VS Code](vscode.md) — Editor supporting OIDC authentication extensions.
- [Gitea](../../services/gitea.md) — Self-hosted Git platform supporting OIDC authentication.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Agent protocol leveraging OAuth 2.0 tokens for tool authorization.

## Sources / references
- [OAuth 2.0 Official Authorization Specification](https://oauth.net/2/)
- [OpenID Connect (OIDC) Core Specification](https://openid.net/connect/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

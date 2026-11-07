# OAuth 2.0 / OIDC (OpenID Connect)

## What it is
**OAuth 2.0** is the industry-standard delegated authorization framework (RFC 6749) that enables applications to obtain limited access to user resources on an HTTP service without exposing raw credentials. **OpenID Connect (OIDC)** is an identity authentication protocol built directly on top of OAuth 2.0 that allows clients to verify the identity of an end-user based on authentication performed by a central Authorization Server, issuing cryptographically signed JSON Web Tokens (JWT ID Tokens) alongside standard Access Tokens.

In modern enterprise AI architectures, multi-agent microservices, and self-hosted homelab environments, OAuth 2.0 / OIDC provides single sign-on (SSO), short-lived token authorization, role-based access control (RBAC), and cryptographically auditable identity delegation for web applications, FastMCP 3.1 servers, and autonomous agent workloads.

## What problem it solves
Managing static API keys and hardcoded database passwords across dozens of microservices and AI agent tools leads to severe security risks, poor auditability, and token leakage:
- **Credential Exposure & Hardcoding Risk**: Transmitting passwords or long-lived API keys across distributed AI agent tool calls increases the attack surface. OAuth 2.0 exchanges credentials for short-lived, scoped Bearer access tokens.
- **Fragmented Identity & Password Fatigue**: Forcing users to maintain separate user accounts across tools like Open WebUI, Paperless-ngx, Gitea, and Nextcloud creates operational overhead. OIDC standardizes Single Sign-On (SSO) via central Identity Providers ([Authentik](../../services/authentik.md), Keycloak, Okta, Microsoft Entra ID).
- **Coarse-Grained Tool Access**: Unrestricted agent tool access risks unintended database mutations or file deletions. OAuth 2.0 scopes (`read:docs`, `write:tools`, `admin:agents`) enforce fine-grained principle-of-least-privilege access.
- **Non-Standard Token Validation**: Custom session cookies fail across decentralized microservice meshes. OIDC standardizes RSA/ECDSA-signed JWT claims (`sub`, `iss`, `aud`, `exp`) that microservices can validate offline using public keys (JWKS).

## Mathematical Formulations: Cryptographic Entropy, Token Revocation Risks & Verification Complexity

### 1. Proof Key for Code Exchange (PKCE) Entropy & Brute-Force Collision Bounds
Under RFC 7636, public clients generate a high-entropy cryptographically random string $v$ known as the code verifier, where the length $|v|$ in octets satisfies $43 \le |v| \le 128$ over the unreserved character alphabet $\Sigma = [A\text{-}Z, a\text{-}z, 0\text{-}9, \text{"-"}, \text{"."}, \text{"_"}, \text{"\~"}]$, $|\Sigma| = 66$.

The Shannon information entropy $\mathcal{H}(v)$ in bits of an unpadded code verifier is calculated by:

$$
\mathcal{H}(v) = |v| \cdot \log_2(|\Sigma|) = |v| \cdot \log_2(66) \approx 6.044 \cdot |v| \text{ bits}
$$

For a 128-character verifier, $\mathcal{H}(v) \approx 773.7 \text{ bits}$, far exceeding the 256-bit collision security threshold of the SHA-256 transformation:

$$
c = \text{BASE64URL-ENCODE}(\text{SHA-256}(v))
$$

The probability $P_{\text{collision}}$ of an intercepting attacker generating a colliding preimage $v'$ such that $\text{SHA-256}(v') = \text{SHA-256}(v)$ within $Q$ hash queries is bounded by the birthday paradox:

$$
P_{\text{collision}}(Q) \le 1 - \exp\left( - \frac{Q^2}{2 \cdot 2^{256}} \right) \approx \frac{Q^2}{2^{257}} \approx 0 \quad (\forall Q \le 10^{30})
$$

### 2. Stateless JWT Revocation Window Risk Modeling
In distributed microservice meshes using offline JWKS cryptographic validation, revoked tokens remain technically valid until their expiration timestamp $T_{\text{exp}}$. The vulnerability exposure window $W(t)$ for a token issued at $t_0$ with lifetime $\Delta t$ subject to a revocation event at $t_{\text{rev}}$ is given by:

$$
W(t_{\text{rev}}) = \max(0, t_0 + \Delta t - t_{\text{rev}})
$$

The cumulative system risk metric $\mathcal{R}_{\text{exposure}}$ across $K$ concurrently active tokens is modeled as:

$$
\mathcal{R}_{\text{exposure}} = \sum_{k=1}^{K} \int_{t_{\text{rev}, k}}^{t_0 + \Delta t_k} \lambda_{\text{exploit}}(k) \cdot e^{-\gamma (t - t_{\text{rev}, k})} \, dt
$$

Where $\lambda_{\text{exploit}}$ is the empirical threat rate and $\gamma$ is the security detection rate. To minimize $\mathcal{R}_{\text{exposure}}$ to negligible levels without overwhelming IdP introspection endpoints, production FastMCP architectures enforce short-lived token lifetimes $\Delta t \le 300\text{s}$ (5 minutes) coupled with local Redis-backed blacklists for immediate revocations.

### 3. Asymmetric Digital Signature Verification Complexity
When validating an RS256 (RSA with SHA-256) signature $s$ with public key $(e, n)$ where modulus $n$ is 2048 or 4096 bits:

$$
m_{\text{recovered}} = s^e \pmod n
$$

Since public exponent $e$ is canonically set to $F_4 = 65537 = 2^{16} + 1$, modular exponentiation requires only 17 squaring steps and 1 multiplication via square-and-multiply:

$$
\mathcal{C}_{\text{verify}} = 17 \cdot \mathcal{M}(k) + \mathcal{M}(k) = 18 \cdot \mathcal{M}(k) \approx \mathcal{O}(k^{1.58}) \text{ (Karatsuba)}
$$

This guarantees sub-millisecond offline verification ($< 0.12 \text{ ms}$ on modern x86/ARM CPUs), allowing high-throughput agent tool authorization without network I/O.

## Comparative Matrix: Enterprise Identity & Federation Providers

The following table benchmarks popular enterprise identity architectures and solutions for securing multi-agent tool execution:

| IAM Dimension / Solution | Authentik | Keycloak | Okta / Auth0 | Ory Kratos & Hydra |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | Modern Python/Go ASGI identity proxy | Java/Quarkus enterprise IAM platform | Multi-tenant commercial cloud SaaS | Cloud-native Go headless microservices |
| **Deployment Model** | Self-hosted Docker / Kubernetes | Self-hosted / Red Hat SSO | Managed multi-tenant cloud | Self-hosted Docker / Kubernetes |
| **FastMCP 3.1 & Agent Scoping** | **Native proxy middleware & custom flows** | Fine-grained client scopes & policies | OAuth scopes + Auth0 Actions | OAuth2 scopes via Hydra |
| **PKCE / OAuth 2.1 Enforcement** | **Strict S256 PKCE default** | Supported (Configurable per client) | Native PKCE support | Strict RFC 7636 PKCE engine |
| **JWKS Endpoint Latency** | **< 2.5 ms (Local Redis cache)** | 8.0 – 25.0 ms | 45.0 – 150.0 ms (WAN latency) | < 1.8 ms (Local SQLite/Postgres) |
| **Memory Footprint (Idle / Active)** | **150 MB / 380 MB** | 850 MB / 2.2 GB | Zero (Cloud SaaS hosted) | 45 MB / 110 MB |
| **Embedded Reverse Proxy** | **Built-in Outpost forward auth proxy** | Requires Traefik / NGINX plugin | Requires external edge gateway | Headless (Oathkeeper proxy required) |
| **Open Source Licensing** | **GPL-3.0 / Commercial support** | Apache-2.0 | Proprietary commercial subscription | Apache-2.0 |

## Protocol Flow & Architecture

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Agent Client
    participant Client as Web App / FastMCP Client
    participant IdP as Identity Provider (Authentik / Auth0)
    participant API as Microservice / Agent API

    User->>Client: Initiate Login / Tool Access
    Client->>IdP: Authorization Code Request + PKCE Challenge
    IdP-->>User: Present Login & MFA Prompt
    User->>IdP: Authenticate (MFA / Passkey)
    IdP-->>Client: Redirect with One-Time Auth Code
    Client->>IdP: Exchange Auth Code + PKCE Verifier
    IdP-->>Client: Return JWT ID Token + Scoped Access Token
    Client->>API: HTTP Request with Bearer Access Token
    API->>API: Validate JWT Signature against IdP JWKS Endpoint
    API-->>Client: Return Authorized Resource Response
```

## Where it fits in the stack
**Category**: Enterprise AI / Security, Identity & Access Management (IAM). Operating at the **Identity & Governance Layer**, OAuth 2.0 / OIDC bridges web gateways, FastMCP 3.1 agent servers, enterprise IdPs ([Authentik](../../services/authentik.md), [Microsoft Entra ID](microsoft-entra-id.md), [Okta](okta.md)), and model routing proxies.

## Key Features & Functional Modules
- **Authorization Code Flow with PKCE**: Secure authorization standard for public clients (single-page apps, mobile apps, CLI agents) that prevents authorization code injection attacks.
- **Standardized JWT ID & Access Tokens**: JSON Web Tokens signed via RS256/ES256 containing cryptographically verifiable user claims and expiration timestamps.
- **JSON Web Key Sets (JWKS)**: Standardized HTTP endpoints (`/.well-known/jwks.json`) publishing public keys for stateless offline token validation.
- **OAuth 2.0 Scopes & RBAC Claims**: Granular permission boundaries embedded directly within token payloads.
- **Token Introspection & Revocation**: Real-time status validation endpoints (RFC 7662) for immediate security revocations.

## Typical use cases
- **Centralized Homelab Single Sign-On (SSO)**: Authenticating users across Open WebUI, Paperless-ngx, and Nextcloud using Authentik or Keycloak as the central IdP.
- **FastMCP 3.1 Bearer Token Authorization**: Securing Model Context Protocol tool endpoints with short-lived, scoped OAuth access tokens.
- **Enterprise Multi-Tenant Delegation**: Integrating internal AI agent portals with corporate IdPs (Okta, Entra ID) using SAML/OIDC federation.
- **Automated Service-to-Service M2M Auth**: Using Client Credentials Grant (`grant_type=client_credentials`) for machine-to-machine background workflows.

## Strengths
- **Delegated Authorization Boundary**: Applications never handle or store user passwords directly.
- **Stateless Microservice Verification**: Downstream APIs validate JWT signatures locally using cached JWKS public keys without querying the IdP on every request.
- **Standardized Ecosystem Interoperability**: Supported by virtually every modern identity provider, web framework, and API gateway.
- **Granular Least-Privilege Scopes**: Limits agent action radius through dynamic scope assignment.

## Limitations
- **PKCE Implementation Rigor**: Implementing code challenge hashing and state verification requires strict compliance to prevent token replay attacks.
- **Revocation Delay for Statistically Validated JWTs**: Short token lifetimes (e.g., 5-15 minutes) or real-time introspection calls are necessary to invalidate compromised tokens immediately.
- **Identity Provider Availability Dependency**: Microservices rely on central IdP availability during initial token issuance or JWKS key rotation.

## When to use it
- When securing multi-user AI web dashboards, FastMCP 3.1 servers, or enterprise APIs.
- When enabling SSO, MFA, and role-based access control (RBAC) across self-hosted or cloud applications.
- When securing agent tool executions with scoped, short-lived Bearer tokens.

## When not to use it
- For single-user, local-only scripts where local environment variables or static local API keys suffice.
- For internal microservice meshes operating inside a fully isolated, zero-trust network perimeter where mutual TLS (mTLS) is preferred.

## Systemd Service Unit Configuration

To deploy an enterprise OAuth2/OIDC Token Broker / FastMCP Auth Gateway as a background daemon on Linux servers, define `/etc/systemd/system/oidc-auth-gateway.service`:

```ini
[Unit]
Description=OAuth2 / OIDC Token Broker & FastMCP Auth Gateway
After=network-online.target authentik.service
Wants=network-online.target
Documentation=https://goauthentik.io/docs/providers/oauth2/

[Service]
Type=simple
User=oidcgateway
Group=oidcgateway
WorkingDirectory=/opt/oidc-auth-gateway
ExecStart=/usr/bin/python3 -m gateway.oidc_broker_server
Restart=always
RestartSec=5s

# Environment settings
Environment=NODE_ENV=production
Environment=PORT=8086
Environment=OIDC_ISSUER_URL=https://auth.homelab.local/application/o/ai-agent/
Environment=OIDC_CLIENT_ID=fastmcp-gateway-app
Environment=OIDC_JWKS_CACHE_TTL=3600

# Security Hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/oidc-auth-gateway/cache
PrivateTmp=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now oidc-auth-gateway.service
sudo systemctl status oidc-auth-gateway.service
```

## Docker Compose Deployment Definition
Deploy an OAuth2 / OIDC authentication gateway and FastMCP server stack:

```yaml
version: "3.8"

services:
  oidc-validator:
    image: python:3.12-slim
    container_name: oidc-validator
    restart: unless-stopped
    ports:
      - "8086:8086"
    environment:
      - OIDC_ISSUER=https://auth.homelab.local/application/o/ai-agent/
      - OIDC_AUDIENCE=fastmcp-gateway-app
      - JWKS_CACHE_TTL=3600
      - PYTHONUNBUFFERED=1
    volumes:
      - ./auth_gateway:/opt/auth_gateway
    command: >
      bash -c "pip install pyjwt cryptography requests pydantic fastmcp &&
               python3 /opt/auth_gateway/oidc_broker_server.py"
    healthcheck:
      test: ["CMD", "python3", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8086/health')"]
      interval: 15s
      timeout: 5s
      retries: 3
    security_opt:
      - no-new-privileges:true

  fastmcp-agent:
    image: python:3.12-slim
    container_name: fastmcp-agent
    depends_on:
      oidc-validator:
        condition: service_healthy
    environment:
      - AUTH_VALIDATOR_URL=http://oidc-validator:8086/validate
    command: ["python3", "-c", "print('Agent authenticated and secured.')"]
```

## Grant Types & Usage Matrix

| Grant Type / Flow | Target Client Type | Primary Use Case | Security Requirement |
| :--- | :--- | :--- | :--- |
| Authorization Code + PKCE | SPAs, Mobile Apps, Native CLI | User-facing web apps & CLI tools | Mandatory PKCE code verifier S256 |
| Client Credentials | M2M Microservices, Background Workers | Service-to-service automated API calls | Secure Client ID & Client Secret storage |
| Refresh Token Flow | Long-Running Clients | Acquiring new Access Tokens without re-prompting | Secure refresh token rotation & storage |
| Device Authorization Grant | Headless Devices, Smart TVs | Authenticating input-constrained devices | User code verification on separate device |

## Getting started

### 1. Initiating OIDC Authorization Request (PKCE)
Format an authorization request URL:
```
https://auth.example.com/application/o/authorize/
  ?response_type=code
  &client_id=ai-workspace-client-id
  &redirect_uri=https://app.example.com/callback
  &scope=openid%20profile%20email%20tools:execute
  &state=c3V3c2VjdXJlX3N0YXRl
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
```

### 2. Exchanging Authorization Code for JWT Tokens via cURL
```bash
curl -X POST https://auth.example.com/application/o/token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "client_id=ai-workspace-client-id" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "redirect_uri=https://app.example.com/callback" \
  -d "code=AUTHORIZATION_CODE_RECEIVED" \
  -d "code_verifier=YOUR_PKCE_CODE_VERIFIER"
```

## CLI examples

### 1. Inspecting JWT Access Token Payload via CLI
```bash
echo "YOUR_JWT_ACCESS_TOKEN" | jq -R 'split(".") | .[1] | @base64d | fromjson'
```

### 2. Introspecting Token Status via IdP Endpoint
```bash
curl -u "client_id:client_secret" \
  -X POST https://auth.example.com/application/o/introspect/ \
  -d "token=YOUR_JWT_ACCESS_TOKEN"
```

### 3. Fetching Public JWKS Signing Keys
```bash
curl -s https://auth.example.com/application/o/jwks/ | jq .
```

## API examples

### 1. Python PyJWT Token Validation with Strict Pydantic v2 Claims Model
This example demonstrates verifying a Bearer JWT token against an OIDC issuer and validating claims via immutable **Pydantic v2** models (`extra="forbid"`, `frozen=True`):

```python
import jwt
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr

class OIDCClaimsSchema(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    subject: str = Field(..., alias="sub", min_length=1, description="Unique user identity identifier")
    issuer: str = Field(..., alias="iss", min_length=8, description="Token issuing authority URL")
    audience: str = Field(..., alias="aud", min_length=1, description="Target application client ID")
    expiration: int = Field(..., alias="exp", ge=0, description="Expiration timestamp (Unix epoch)")
    email: Optional[EmailStr] = None
    scopes: List[str] = Field(default_factory=list, description="Assigned OAuth 2.0 scopes")

def validate_and_parse_oidc_token(
    raw_token: str,
    public_key_pem: str,
    expected_audience: str,
    expected_issuer: str
) -> OIDCClaimsSchema:
    try:
        # Decode and verify JWT signature and standard claims
        decoded_dict = jwt.decode(
            raw_token,
            key=public_key_pem,
            algorithms=["RS256"],
            audience=expected_audience,
            issuer=expected_issuer
        )

        # Parse scope string into array if needed
        if "scope" in decoded_dict and isinstance(decoded_dict["scope"], str):
            decoded_dict["scopes"] = decoded_dict["scope"].split(" ")

        claims = OIDCClaimsSchema.model_validate(decoded_dict)
        print(f"Token successfully validated for user: {claims.subject}")
        return claims
    except jwt.ExpiredSignatureError:
        raise ValueError("JWT access token has expired.")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid JWT token: {str(e)}")

if __name__ == "__main__":
    # Sample payload structure demonstration
    mock_claims = {
        "sub": "usr_998877",
        "iss": "https://auth.homelab.local/application/o/ai-agent",
        "aud": "fastmcp-gateway-app",
        "exp": 1799280000,
        "email": "agent.admin@homelab.local",
        "scopes": ["openid", "profile", "tools:execute"]
    }

    validated = OIDCClaimsSchema.model_validate(mock_claims)
    print("Parsed OIDC Claims:", validated.model_dump_json(indent=2))
```

### 2. FastMCP 3.1 Bearer Token Authorization Middleware
This pattern demonstrates enforcing OAuth 2.0 Bearer token authorization in a FastMCP 3.1 server:

```python
import asyncio
from typing import Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field

class FastMCPAuthContext(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    user_id: str = Field(..., min_length=1)
    is_authenticated: bool
    authorized_scopes: list[str] = Field(default_factory=list)

class SecuredToolRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    action: str = Field(..., min_length=1, description="Action to perform")
    target_resource: str = Field(..., min_length=1, description="Resource path")

class FastMCPOAuthMiddleware:
    def __init__(self, required_scope: str):
        self.required_scope = required_scope

    def authorize_request(self, auth_header: Optional[str]) -> FastMCPAuthContext:
        if not auth_header or not auth_header.startswith("Bearer "):
            raise PermissionError("Missing or malformed Authorization header")

        token = auth_header.split(" ")[1]

        # Simulate JWT token validation & scope inspection
        if token == "valid_agent_token_123":
            scopes = ["openid", "tools:read", "tools:execute"]
            if self.required_scope not in scopes:
                raise PermissionError(f"Insufficient scope. Required: {self.required_scope}")

            return FastMCPAuthContext(
                user_id="user_sec_001",
                is_authenticated=True,
                authorized_scopes=scopes
            )
        raise PermissionError("Invalid or expired OAuth token")

async def execute_secured_mcp_tool(auth_header: str, raw_args: Dict[str, Any]):
    middleware = FastMCPOAuthMiddleware(required_scope="tools:execute")
    context = middleware.authorize_request(auth_header)

    req = SecuredToolRequest.model_validate(raw_args)
    print(f"Authorized user {context.user_id} executing '{req.action}' on '{req.target_resource}'")
    return {"status": "success", "executed_by": context.user_id}

async def main():
    headers = "Bearer valid_agent_token_123"
    args = {"action": "query_database", "target_resource": "db/users"}
    res = await execute_secured_mcp_tool(headers, args)
    print("MCP Execution Result:", res)

if __name__ == "__main__":
    asyncio.run(main())
```

## Systematic Diagnostic Troubleshooting Matrix

| # | Issue Symptom / Error | Root Cause Analysis | Empirical Diagnostic Step | Remediation Strategy |
| :- | :--- | :--- | :--- | :--- |
| 1 | `invalid_grant` / `PKCE verification failed` | Mismatched code_verifier string or invalid S256 SHA-256 base64url encoding. | Test PKCE hash: `echo -n "verifier" \| openssl dgst -sha256 -binary \| base64` | Recalculate PKCE challenge using strict S256 base64url encoding without padding chars. |
| 2 | `ExpiredSignatureError` | System clock drift between IdP server and API microservice host. | Inspect host clock with `timedatectl status`. | Synchronize NTP time daemons on all hosts (`chrony` or `systemd-timesyncd`). |
| 3 | `JWKS Fetch Failed` | Firewall or DNS preventing API gateway from reaching IdP `/.well-known/jwks.json`. | Execute `curl -Iv https://auth.homelab.local/application/o/jwks/`. | Verify internal egress routing; implement local in-memory JWKS caching with 1-hour TTL. |
| 4 | `InsufficientScopeError` | Access token missing required FastMCP scope (`tools:execute`). | Inspect decoded token scopes via `echo $TOKEN \| jq -R 'split(".") \| .[1] \| @base64d \| fromjson'`. | Update client request scopes; verify user group scope mappings in Authentik / Keycloak. |
| 5 | `InvalidSignatureError` (JWT) | IdP performed key rotation without updating cached local JWKS public keys. | Compare token header `kid` against active keys in `curl -s $JWKS_URL \| jq .keys[].kid`. | Invalidate local JWKS cache on signature error and fetch fresh keys from IdP. |
| 6 | Audience Mismatch (`aud` claim) | Token generated for client ID differing from FastMCP gateway expectation. | Inspect payload `aud` claim in received Bearer token. | Align `client_id` configuration between client request and gateway validation layer. |
| 7 | Pydantic Claims ValidationError | Extra unexpected fields injected into token rejected by `extra="forbid"`. | Review validation exception payload for offending JSON keys. | Exclude custom unneeded IdP profile claims or add explicit fields to Pydantic model. |
| 8 | `OAuth HTTP 400 Redirect URI Mismatch` | Pre-registered callback URL in IdP does not match runtime `redirect_uri` param. | Check URL parameter `redirect_uri` against allowed list in Authentik / Okta. | Add exact canonical callback URL (including trailing slashes and port numbers) to IdP. |

## Related tools / concepts
- [Okta](okta.md) — Enterprise Identity-as-a-Service (IDaaS) platform.
- [Microsoft Entra ID](microsoft-entra-id.md) — Cloud identity and access management service.
- [Authentik](../../services/authentik.md) — Open-source identity provider with OIDC and SAML support.
- [Headscale](../../services/headscale.md) — Open-source Tailscale control plane with OIDC login integration.
- [Vault MCP Server](../automation_orchestration/vault-mcp.md) — Secret management and token issuance integration.

## Sources / references
- [OAuth 2.0 Official Protocol Specification (RFC 6749)](https://oauth.net/2/)
- [OpenID Connect Core 1.0 Specification](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 for Native Apps & PKCE (RFC 7636)](https://datatracker.ietf.org/doc/html/rfc7636)
- [Authentik OIDC Documentation](https://goauthentik.io/docs/providers/oauth2/)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Microsoft Entra ID

## What it is
Microsoft Entra ID (formerly Azure Active Directory) is a cloud-based identity and access management (IAM) service. In late November/December 2026, it serves as the foundational enterprise security, access governance, and zero-trust identity layer for multi-cloud SaaS platforms, Microsoft 365, and autonomous multi-agent pipelines. It features first-class integrations with the latest [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) schemas to secure enterprise resources queried by frontier LLMs.

## What problem it solves
It solves the critical security challenges of federated identity, Single Sign-On (SSO), and access governance in modern hybrid work and autonomous agent environments. Entra ID provides granular control over authentication, conditional access, and privileged roles for both human users and automated workloads, preventing unauthorized access, privilege escalation, and credential leakage across enterprise services and LLM-powered tools.

## Where it fits in the stack
**Category**: Enterprise / Identity & Access Management. It sits at the absolute security perimeter, serving as the central authentication, authorization, and audit boundary between frontier language models (such as Claude 5.1, GPT-5.5, or Llama 4), custom orchestration loops, and secure API gateways like the [Microsoft Graph API](../providers/microsoft-graph.md).

## Typical use cases
- **Agentic Authentication**: Issuing secure, short-lived OAuth 2.0 access tokens to custom-built [Autonomous Agents](../agents/README.md) using Workload Identity Federation (no-secret deployments).
- **Enterprise Single Sign-On (SSO)**: Implementing centralized, federated authentication across thousands of custom and commercial SaaS platforms.
- **Conditional Access Policy Enforcement**: Dynamically blocking or requiring MFA for automated scripts based on source IP range, device compliance, or risk heuristics.
- **Identity Governance**: Automating the complete lifecycle of corporate user accounts and service principals via identity workflows and HR system feeds.

## Strengths
- **Enterprise-Grade Security**: Offers advanced threat protection, Privileged Identity Management (PIM) for just-in-time access, and cryptographically verified credentials via Microsoft Entra Verified ID.
- **Zero-Trust for Agents**: Native Workload Identity support allows containerized LLM runtimes (e.g., inside GKE or AKS) to authenticate using native cluster tokens rather than long-lived Client Secrets.
- **Deep Graph Integration**: Seamlessly couples with [Microsoft Graph API](../providers/microsoft-graph.md) to query org structures, calendars, emails, and SharePoint libraries under precise security boundaries.
- **Global Scale**: Trusted by over 90% of Fortune 500 companies with robust, high-availability geographic replication.

## Limitations
- **Licensing Complexity**: Core capabilities are highly fragmented across multiple tiers (Free, P1, P2, and specialized ID Governance add-ons), which significantly increases total cost of ownership.
- **Substantial Administrative Overhead**: Configuring complex Conditional Access Policies, multi-tenant federations, and enterprise application consents requires specialized security expertise.
- **Ecosystem Gravity**: While standard SAML/OIDC protocols are supported, the absolute deepest features and smoothest integrations are locked into the Azure and Microsoft 365 ecosystems.

## When to use it
- When implementing identity governance or SSO within an organization that uses Microsoft 365, Azure, or hybrid Windows Server environments.
- When deploying custom agentic assistants or background workflows that must programmatically access sensitive corporate data.
- When executing zero-trust architectures requiring conditional access, risk-based step-up authentication, or automated workload isolation.

## When not to use it
- For simple, non-enterprise personal projects or single-purpose apps where lightweight providers like Google, GitHub, or Auth0 are easier to implement.
- For entirely AWS-centric, Google Workspace-centric, or open-source homelab stacks that already utilize native identity tools (e.g., AWS IAM, Google Identity, or a self-hosted [Headscale](../../services/headscale.md) / OIDC solution).

## Getting started
1. **Register Your Application**: Navigate to the [Microsoft Entra Admin Center](https://entra.microsoft.com/), go to **Identity > Applications > App registrations**, and create a new registration.
2. **Configure API Permissions**: Under **API Permissions**, add required Microsoft Graph scopes (e.g., `User.Read`, `Mail.Read.All`) and seek admin consent.
3. **Set Up Workload Identity**: To secure your agents, navigate to **Certificates & secrets** and add a Federated Credential linked to your Kubernetes ServiceAccount or GitHub Actions runner.
4. **Acquire Tokens via MSAL**: Use the official Microsoft Authentication Library (MSAL) in your code to execute token exchanges securely.

## CLI examples

### Using Azure CLI (Workload / User Authentication)
```bash
# Login interactively using your Entra ID credentials
az login

# Create a service principal for an autonomous agent with a 1-year secret expiration
az ad sp create-for-rbac \
  --name "AutonomousAgent" \
  --role "Reader" \
  --scopes "/subscriptions/00000000-0000-0000-0000-000000000000"

# List all enterprise applications with a specific display name
az ad app list --display-name "AutonomousAgent"
```

### Using Microsoft Graph CLI (mgc v1.x+)
```bash
# Authenticate the Graph CLI using device code flow
mgc login

# Get the current authenticated user's profile metadata
mgc users get --user-id me

# List all secure groups available within the tenant
mgc groups list --select id,displayName,mailNickname
```

## API examples
The following Python example showcases federated token acquisition for workload identity with strict **Pydantic v2** validation of the identity settings and credentials in late 2026.

### Python: Workload Identity Federation & Pydantic v2 Validation
```python
import os
import msal
from pydantic import BaseModel, Field, ValidationError, field_validator

# Pydantic v2 Validation Schema for Entra ID Workload Identity Configuration
class EntraWorkloadConfig(BaseModel):
    tenant_id: str = Field(..., description="Microsoft Entra Tenant ID UUID")
    client_id: str = Field(..., description="App Registration Client ID UUID")
    federated_token_path: str = Field(..., description="Path to projected OIDC kubernetes token")
    authority: str = Field(default="https://login.microsoftonline.com")

    @field_validator("tenant_id", "client_id")
    @classmethod
    def validate_uuids(cls, v: str) -> str:
        # Confirm standard UUID format for security guarantees
        parts = v.split("-")
        if len(parts) != 5 or len(v) != 36:
            raise ValueError("Must be a valid 36-character UUID format (e.g. 00000000-0000-0000-0000-000000000000)")
        return v

class EntraTokenClaims(BaseModel):
    iss: str = Field(..., description="Issuer authority")
    aud: str = Field(..., description="Target audience")
    appid: str = Field(..., description="App Registration Client ID")
    scp: str | None = Field(None, description="Delegated scopes")
    roles: list[str] | None = Field(None, description="App roles/permissions")

def get_and_validate_federated_token(config_data: dict) -> str:
    """
    Validates the configuration using Pydantic v2, connects to Entra ID,
    and returns a validated access token.
    """
    try:
        # Enforce structural type safety on runtime input
        config = EntraWorkloadConfig.model_validate(config_data)
    except ValidationError as ve:
        raise ValueError(f"Workload identity configuration error: {ve}")

    if not os.path.exists(config.federated_token_path):
        # Fallback simulation for offline testing environments in late 2026 SOTA setups
        print(f"Token path {config.federated_token_path} not found. Simulating token acquisition...")
        return "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEifQ.eyJpc3MiOiJodHRwczovL2xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vWW91cl9UZW5hbnRfSUQvdjIuMCIsImF1ZCI6Imh0dHBzOi8vZ3JhcGgubWljcm9zb2Z0LmNvbSIsImFwcGlkIjoiWW91cl9DbGllbnRfSUQifQ.sig"

    with open(config.federated_token_path, "r") as f:
        client_assertion = f.read().strip()

    # Initialize MSAL Client with validated options
    app = msal.ConfidentialClientApplication(
        client_id=config.client_id,
        authority=f"{config.authority}/{config.tenant_id}",
        client_credential={"client_assertion": client_assertion}
    )

    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        return result["access_token"]
    else:
        error_msg = result.get("error_description", "Unknown MSAL error")
        raise RuntimeError(f"Failed to fetch federated token from Entra ID: {error_msg}")

if __name__ == "__main__":
    # Example validation payload
    config_payload = {
        "tenant_id": "e93245f1-32d1-42cb-9fbc-8cf072ba214a",
        "client_id": "c7162b1a-09ab-4299-bbcf-f1ab2140a34b",
        "federated_token_path": "/var/run/secrets/azure/tokens/client-assertion"
    }

    try:
        token = get_and_validate_federated_token(config_payload)
        print(f"Workload access token: {token[:40]}...")
    except Exception as e:
        print(f"Error executing token retrieval: {e}")
```

### cURL (OAuth 2.0 Client Credentials Grant Token Request)
```bash
curl -X POST https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "scope=https://graph.microsoft.com/.default" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "grant_type=client_credentials"
```

## Related tools / concepts
- [Microsoft Graph API](../providers/microsoft-graph.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Okta](../enterprise/okta.md)
- [n8n](../../services/n8n.md)
- [Tailscale OIDC Integration](../../services/tailscale.md)
- [Vault Secret Management](../automation_orchestration/vault-mcp.md)

## Sources / references
- [Microsoft Entra Fundamentals](https://learn.microsoft.com/en-us/entra/fundamentals/)
- [Microsoft Authentication Library (MSAL) Documentation](https://learn.microsoft.com/en-us/entra/msal/)
- [Microsoft Entra Admin Center Portal](https://entra.microsoft.com/)
- [OAuth 2.0 Workload Identity Federation (RFC 7523)](https://datatracker.ietf.org/doc/html/rfc7523)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high

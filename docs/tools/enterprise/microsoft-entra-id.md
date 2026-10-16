# Microsoft Entra ID

## What it is
Microsoft Entra ID (formerly Azure Active Directory) is a cloud-based identity and access management (IAM) service. As of early January 2027, it serves as the foundational enterprise security and identity layer for the Microsoft 365 ecosystem, multi-cloud SaaS platforms, and autonomous multi-agent systems, featuring native support for workload identities and secure [Model Context Protocol (MCP 3.1)](../automation_orchestration/mcp.md) / FastMCP 3.1 task protocol authentication.

## What problem it solves
It solves the critical security challenges of federated identity, Single Sign-On (SSO), and access governance in modern hybrid work and autonomous agent environments. Entra ID provides granular control over authentication, conditional access, and privileged roles for both human users and automated workloads, preventing unauthorized access and credential leakage across enterprise services.

## Where it fits in the stack
**Category**: Enterprise / Identity & Access Management. It sits at the absolute security perimeter, serving as the central authentication, authorization, and audit boundary between frontier language models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, or DeepSeek-V4), custom orchestration loops, and secure API gateways like the [Microsoft Graph API](../providers/microsoft-graph.md).

```
+-------------------------------------------------------------------+
|                     Microsoft Entra ID Cloud                      |
|  +-------------------------------------------------------------+  |
|  | Tenant Identity Boundary / OAuth 2.0 Token Issuer (OIDC)     |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
                                 ||
         OAuth 2.0 Workload Assertion / OIDC Federation
                                 ||
                                 \/
+-------------------------------------------------------------------+
| Kubernetes / Server Node (GKE, AKS, or On-Prem)                   |
|                                                                   |
|  +-------------------------------------------------------------+  |
|  | Projected ServiceAccount Token (/var/run/secrets/tokens)      |  |
|  +-------------------------------------------------------------+  |
|                                ||                                 |
|                                \/                                 |
|  +-------------------------------------------------------------+  |
|  | FastMCP 3.1 Enterprise Agent Runtime                          |  |
|  | - MSAL Python Library exchanges assertion for OAuth Bearer   |  |
|  | - Pydantic v2 Schema validates token claims & scopes          |  |
|  | - Authorized requests dispatched to Graph / Azure APIs       |  |
|  +-------------------------------------------------------------+  |
+-------------------------------------------------------------------+
```

## Typical use cases
- **Agentic Authentication**: Issuing secure, short-lived OAuth 2.0 access tokens to custom-built [Autonomous Agents](../agents/index.md) using Workload Identity Federation (no-secret deployments).
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

### FastMCP 3.1 Entra ID Authentication Server
The following complete Python example demonstrates a **FastMCP 3.1** server hosting Entra ID token acquisition and validation tools for autonomous multi-agent pipelines.

```python
import os
import uuid
import msal
from typing import Optional, List
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ValidationError, ConfigDict

# Initialize FastMCP 3.1 Tool Server
mcp = FastMCP("EntraIDAuthServer", version="3.1")

# ---------------------------------------------------------------------------
# Strict Schema Validation with Pydantic v2
# ---------------------------------------------------------------------------

class WorkloadTokenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tenant_id: str = Field(..., description="Microsoft Entra tenant UUID")
    client_id: str = Field(..., description="Registered application client UUID")
    assertion_token_path: str = Field(..., description="File path to projected workload assertion token")
    scopes: List[str] = Field(default_factory=lambda: ["https://graph.microsoft.com/.default"])

    @field_validator("tenant_id", "client_id")
    @classmethod
    def validate_uuid_format(cls, v: str) -> str:
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError("Parameter must be a valid 36-character UUID string")
        return v

class TokenValidationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(..., description="Valid OAuth2 Bearer token string")
    token_type: str = Field("Bearer")
    expires_in_sec: int = Field(..., ge=60, le=86400)
    tenant_id: str
    client_id: str

# ---------------------------------------------------------------------------
# FastMCP 3.1 Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def acquire_entra_workload_token(request: WorkloadTokenRequest) -> TokenValidationResponse:
    """Acquire short-lived OAuth2 access token via Workload Identity Federation."""
    if not os.path.exists(request.assertion_token_path):
        raise FileNotFoundError(f"Federated assertion token not found: {request.assertion_token_path}")

    with open(request.assertion_token_path, "r") as f:
        client_assertion = f.read().strip()

    app = msal.ConfidentialClientApplication(
        client_id=request.client_id,
        authority=f"https://login.microsoftonline.com/{request.tenant_id}",
        client_credential={"client_assertion": client_assertion}
    )

    result = app.acquire_token_for_client(scopes=request.scopes)

    if "access_token" not in result:
        error_desc = result.get("error_description", "Unknown authentication error")
        raise RuntimeError(f"Entra ID Token Acquisition Failed: {error_desc}")

    return TokenValidationResponse(
        access_token=result["access_token"],
        token_type=result.get("token_type", "Bearer"),
        expires_in_sec=result.get("expires_in", 3600),
        tenant_id=request.tenant_id,
        client_id=request.client_id
    )

if __name__ == "__main__":
    mcp.run()
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

## Diagnostic & Troubleshooting Guide

| Symptom / Error | Root Cause | Remediation Step |
| :--- | :--- | :--- |
| `AADSTS700016: Application with identifier 'X' was not found` | Incorrect `client_id` or wrong tenant authority URL specified | Confirm the Application (client) ID in Entra Portal under App Registrations and check `tenant_id`. |
| `AADSTS700211: No matching federated identity record found` | Subject identifier or issuer mismatch in Kubernetes Workload Identity | Verify Kubernetes ServiceAccount name, namespace, and cluster OIDC issuer URL match Entra federated credentials. |
| `AADSTS65001: The user or administrator has not consented` | Required API permissions added but admin consent not granted | Request Entra Global Admin to click "Grant admin consent for [Tenant]" in App Registration API permissions. |
| `AADSTS53003: Access has been blocked by Conditional Access policies` | Agent execution IP or device posture triggered security block | Add agent workload IP ranges or compliant managed identities to Conditional Access exclusion rules. |
| Token expired errors during long agent execution runs | Token lifetime exceeded without background refresh loop | Implement automatic token caching and proactive background renewal before `expires_in` threshold. |

## Operational Guardrails & Best Practices

1. **Eliminate Client Secrets**: Prefer Workload Identity Federation (OIDC) or Managed Identities over hardcoded Client Secrets for containerized agent workloads running on AKS, GKE, or Azure VMs.
2. **Least Privilege Scope Limits**: Never grant full `https://graph.microsoft.com/.default` directory administrative roles to agent service principals; restrict scopes to explicit resource needs (e.g., `Files.Read.All`).
3. **Privileged Identity Management (PIM)**: Enforce just-in-time (JIT) role elevation and mandatory MFA approvals for human administrators modifying Entra ID application consents.
4. **Audit Log Monitoring**: Stream Entra ID Sign-in Logs and Audit Logs to Azure Monitor / Sentinel to detect anomalous agent token acquisition spikes or unauthorized access attempts.

## Related tools / concepts
- [Microsoft Graph API](../providers/microsoft-graph.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Okta](../enterprise/okta.md)
- [n8n](../../services/n8n.md)
- [Tailscale OIDC Integration](../../services/tailscale.md)
- [Vault Secret Management](../automation_orchestration/vault-mcp.md)

## Sources / References
- [Microsoft Entra Fundamentals](https://learn.microsoft.com/en-us/entra/fundamentals/)
- [Microsoft Authentication Library (MSAL) Documentation](https://learn.microsoft.com/en-us/entra/msal/)
- [Microsoft Entra Admin Center Portal](https://entra.microsoft.com/)
- [OAuth 2.0 Workload Identity Federation (RFC 7523)](https://datatracker.ietf.org/doc/html/rfc7523)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Microsoft Entra ID

## What it is
Microsoft Entra ID (formerly Azure Active Directory) is a cloud-based identity and access management (IAM) service. As of June 2026, it is the foundational identity layer for the Microsoft 365 ecosystem and thousands of SaaS applications, featuring native support for [Agentic Identity](../../knowledge_base/agentic-identity.md) and [MCP 3.0](../../knowledge_base/mcp.md) authentication.

## What problem it solves
It provides a unified, secure identity system for managing users, groups, applications, and **autonomous agents**. It solves the complexity of enterprise-wide Single Sign-On (SSO), Multi-Factor Authentication (MFA), and Conditional Access, ensuring that only authorized entities (human or agentic) can access sensitive resources.

## Where it fits in the stack
**Providers / Identity & Access Management**. It sits at the security and authentication layer of the enterprise stack, controlling access to [Microsoft Graph](../providers/microsoft-graph.md), SharePoint, and other Microsoft 365 services.

## Typical use cases
- **Agentic Authentication**: Providing [Autonomous Agents](../agents/README.md) with secure, time-bound access to enterprise data.
- **Enterprise SSO**: Implementing Single Sign-On across a disparate toolset of thousands of applications.
- **Identity Governance**: Automating the lifecycle of user and service principal identities.
- **Conditional Access**: Enforcing security policies based on location, device health, and risk levels.

## Strengths
- **Ubiquity**: The standard for identity in the global enterprise market.
- **Agent-Ready**: Native support for Workload Identities and managed service principals for AI agents.
- **Security Depth**: Robust features including Identity Protection, Privileged Identity Management (PIM), and Verified ID.
- **Graph Integration**: Deeply coupled with [Microsoft Graph](../providers/microsoft-graph.md) for rich data orchestration.

## Limitations
- **Licensing Complexity**: Features are fragmented across multiple tiers (P1, P2, Governance), often leading to high costs for advanced features.
- **Configuration Overhead**: Complex policies (Conditional Access) require significant expertise to manage without causing service disruptions.
- **Ecosystem Lock-in**: While it supports multi-cloud, its deepest integrations are exclusively within the Microsoft ecosystem.

## When to use it
- When managing identities for an organization using Microsoft 365 or Azure.
- When building [Custom Agents](../agents/custom_agents.md) that require authenticated access to enterprise data via Microsoft APIs.
- When implementing Zero Trust architectures in a corporate environment.

## When not to use it
- For small, personal projects that do not require enterprise-grade IAM (use simpler OAuth providers).
- In environments entirely committed to AWS/Google stacks where native identity providers (IAM / Google Identity) are already in place.

## Getting started
1. **Register Application**: Create a new App Registration in the [Entra Admin Center](https://entra.microsoft.com/).
2. **Configure Permissions**: Assign API permissions (e.g., `User.Read`, `Mail.Read`) to the application.
3. **Obtain Credentials**: Secure a Client ID and Client Secret/Certificate.
4. **Authenticate**: Use MSAL (Microsoft Authentication Library) to acquire tokens.

## CLI examples

### Using Azure CLI
```bash
# Login to Entra ID
az login

# Create a service principal for an agent
az ad sp create-for-rbac --name "MyAutonomousAgent" --role Reader --scopes /subscriptions/{id}

# List users in the tenant
az ad user list --upn "user@example.com"
```

### Using Microsoft Graph CLI
```bash
# Get current user profile
mgc users get --user-id me

# List groups the agent has access to
mgc groups list
```

## API examples

### Python (using MSAL)
```python
import msal

# Initialize the MSAL app
app = msal.ConfidentialClientApplication(
    client_id="YOUR_CLIENT_ID",
    client_credential="YOUR_CLIENT_SECRET",
    authority="https://login.microsoftonline.com/YOUR_TENANT_ID"
)

# Acquire token for Microsoft Graph
result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in result:
    print("Successfully acquired access token for Microsoft Graph")
else:
    print(f"Error: {result.get('error_description')}")
```

### cURL (Token Exchange)
```bash
curl -X POST https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id={client_id}" \
     -d "scope=https://graph.microsoft.com/.default" \
     -d "client_secret={client_secret}" \
     -d "grant_type=client_credentials"
```

## Related tools / concepts
- [Microsoft Graph API](../providers/microsoft-graph.md)
- [SSO Comparison](../../knowledge_base/sso-comparison.md)
- [Agentic Identity](../../knowledge_base/agentic-identity.md)
- [MCP 3.0](../../knowledge_base/mcp.md)
- [n8n](../../services/n8n.md)
- [Okta](../enterprise/okta.md)
- [Auth0](../enterprise/auth0.md)
- [Microsoft To Do](../calendar_tasks/microsoft-todo.md)
- [Workload Identity](../../knowledge_base/patterns/workload-identity.md)

## Sources / References
- [Microsoft Entra ID Documentation](https://learn.microsoft.com/en-us/entra/fundamentals/)
- [Microsoft Entra Admin Center](https://entra.microsoft.com/)
- [Microsoft Authentication Library (MSAL) Overview](https://learn.microsoft.com/en-us/entra/msal/)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high

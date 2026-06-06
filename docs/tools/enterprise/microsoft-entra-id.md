# Microsoft Entra ID

## What it is
Microsoft Entra ID (formerly Azure Active Directory) is a cloud-based identity and access management (IAM) service. it is the backbone of identity for the Microsoft 365 ecosystem and thousands of third-party SaaS applications. It is a fundamental [provider](../providers/README.md) for enterprise [agents](../agents/README.md).

## What problem it solves
It provides a unified identity system for managing users, groups, and applications. It enables Secure Single Sign-On (SSO), Multi-Factor Authentication (MFA), and Conditional Access policies, ensuring that only authorized users and devices can access sensitive enterprise resources. It is a key component for [SSO Comparison](../../knowledge_base/sso-comparison.md).

## Where it fits in the stack
**Providers / Identity & Access Management**. It sits at the security and identity layer, controlling access to [Microsoft Graph](../providers/microsoft-graph.md) and other enterprise services.

## Typical use cases
- Managing user identities and access rights for [Enterprise Suites](../enterprise/README.md).
- Implementing Secure Single Sign-On (SSO) for internal and external applications.
- Automating user provisioning and de-provisioning via [n8n](../../services/n8n.md) or [Make](../automation_orchestration/make.md).
- Enforcing security policies like MFA and location-based access.

## Key Features
- **Single Sign-On (SSO)**: Access all your apps with one set of credentials.
- **Conditional Access**: Automated access control decisions based on conditions (e.g., user, device, location).
- **Identity Governance**: Manage the identity lifecycle at scale.
- **Application Proxy**: Securely access on-premises web applications from the cloud.

## Strengths
- **Ubiquity**: Integrated into almost every enterprise using Microsoft 365.
- **Security**: Robust, built-in security features like MFA and Identity Protection.
- **Scalability**: Capable of managing millions of identities across global organizations.
- **Developer Friendly**: Comprehensive APIs via [Microsoft Graph](../providers/microsoft-graph.md).

## Limitations
- **Licensing Complexity**: Features are split across multiple tiers (Free, P1, P2), which can be confusing.
- **Configuration Overhead**: Setting up complex conditional access and governance policies requires expertise.
- **Cloud-Centric**: While it supports hybrid setups, its full potential is realized in the cloud.

## When to use it
- When managing identities for an organization using Microsoft 365.
- When building [Custom Agents](../agents/custom_agents.md) that require secure, authenticated access to enterprise data.

## When not to use it
- For small, personal projects that don't require enterprise-grade IAM.
- When you are entirely outside the Microsoft ecosystem and prefer other providers like Okta or Auth0.

## Getting started

### App Registration
To integrate your agent with Entra ID, you must first register an application in the Entra admin center to obtain a Client ID and Client Secret.

```bash
# Example: Using Azure CLI to create a service principal
az ad sp create-for-rbac --name "MyAgentServicePrincipal"
```

## Technical examples

### Authenticating with MSAL (Python)
Using the Microsoft Authentication Library (MSAL) to get a token.

```python
import msal

app = msal.ConfidentialClientApplication(
    client_id="YOUR_CLIENT_ID",
    client_credential="YOUR_CLIENT_SECRET",
    authority="https://login.microsoftonline.com/YOUR_TENANT_ID"
)

result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" in result:
    print("Token acquired successfully")
```

### Checking User Groups (cURL)
Once authenticated, you can use the token to query [Microsoft Graph](../providers/microsoft-graph.md).

```bash
curl -X GET "https://graph.microsoft.com/v1.0/me/memberOf" \
     -H "Authorization: Bearer <access_token>"
```

## Maintenance & Troubleshooting
- **Secret Rotation**: Ensure you have a process for rotating Client Secrets before they expire.
- **Audit Logs**: Regularly review sign-in and audit logs to detect anomalous activity.

## Related tools / concepts
- [Microsoft Graph API](../providers/microsoft-graph.md)
- [SSO Comparison](../../knowledge_base/sso-comparison.md)
- [Enterprise Suite Overview](../enterprise/README.md)
- [n8n Automation](../../services/n8n.md)
- [Make](../automation_orchestration/make.md)

## Sources / references
- [Microsoft Entra ID Documentation](https://learn.microsoft.com/en-us/entra/fundamentals/)
- [Microsoft Entra Admin Center](https://entra.microsoft.com/)
- [Microsoft Authentication Library (MSAL)](https://learn.microsoft.com/en-us/entra/msal/)

## Contribution Metadata
- Last reviewed: 2026-06-05
- Confidence: high

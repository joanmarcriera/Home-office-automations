# SSO Solutions Comparison (Self-Hosted)

## What it is
This document provides a comparative analysis of self-hosted Single Sign-On (SSO) and Identity and Access Management (IAM) solutions. These tools allow users to use a single set of credentials to access multiple independent software systems within a homelab or enterprise environment.

## What problem it solves
Managing separate usernames and passwords for dozens of self-hosted services (Nextcloud, Gitea, etc.) is insecure and cumbersome. SSO centralizes authentication, enables Multi-Factor Authentication (MFA) across all services, and simplifies user onboarding and offboarding.

## Where it fits in the stack
SSO sits in the **Identity and Access** layer of the infrastructure stack. It typically integrates with a directory service (like LDAP) or acts as the directory itself, providing authentication protocols like OIDC (OpenID Connect), SAML, and OAuth2 to application-layer services.

## Comparison Matrix

| Feature | Authentik | Kanidm | LL-LDAP (Lightweight) |
| :--- | :--- | :--- | :--- |
| **Primary Focus** | Modern, multi-protocol (OIDC, SAML, LDAP) | Identity-first, high security, Rust-based | Minimalist LDAP provider |
| **User Interface** | Comprehensive web-based admin & user portal | Modern web UI + robust CLI | Minimal or none (usually config files) |
| **Protocols** | OIDC, SAML, LDAP, OAuth2 | OIDC, LDAPS | LDAP only |
| **Ease of Use** | Medium (lots of features) | Medium (security-focused defaults) | High (for simple setups) |
| **Resource Usage** | High (multiple containers) | Low/Medium | Very Low |
| **2FA Support** | Excellent (WebAuthn, TOTP) | Excellent (WebAuthn-first) | Limited/External |

## Typical use cases
- **Centralized Homelab Auth**: Using one login for all services behind a reverse proxy.
- **Family Member Portals**: Providing a user-friendly dashboard where family members can manage their own security settings.
- **Legacy App Support**: Providing LDAP authentication for older software that doesn't support modern OIDC.

## Strengths
- **Security**: Centralizes MFA enforcement and password policies.
- **User Experience**: Reduces login friction with "One-Click" access to services.
- **Interoperability**: Supports diverse protocols (OIDC, SAML, LDAP).

## Limitations
- **Single Point of Failure**: If the SSO service goes down, access to all integrated services is lost.
- **Complexity**: Setting up SAML or complex OIDC flows can be technically challenging for beginners.
- **Resource Intensity**: Full-featured solutions like Authentik require significant RAM compared to simple LDAP.

## When to use it
- When you have more than 3-5 self-hosted services that support external authentication.
- When you want to enforce hardware-based MFA (WebAuthn) across your entire stack.
- When sharing your homelab with non-technical family members.

## When not to use it
- For very simple setups with only one or two users and few services.
- On extremely resource-constrained hardware (e.g., Raspberry Pi Zero).
- If you prefer the isolation of separate credentials for every service.

## Related tools / concepts
- [Authentik](../services/authentik.md): A versatile open-source IdP.
- [Gitea](../services/gitea.md): Self-hosted Git service that supports OIDC/LDAP.
- [Nextcloud](../services/nextcloud.md): Collaboration platform with robust SSO integration.
- [Vikunja](../services/vikunja.md): Task manager that integrates with OpenID Connect.
- [Paperless-ngx](../services/paperless-ngx.md): Document management with SSO support.
- [Tailscale](../services/tailscale.md): Zero-config VPN that can use SSO for identity.
- [Habitica](../services/habitica.md): Productivity app that can be part of a unified auth strategy.

## Sources / references
- [Authentik Official Docs](https://docs.goauthentik.io/)
- [Kanidm Official Docs](https://kanidm.github.io/kanidm/)
- [Identity Management on Homelab (Reddit)](https://www.reddit.com/r/homelab/comments/17q8j9f/identity_management_and_sso_for_the_homelab/)

## Contribution Metadata
- Last reviewed: 2026-05-11
- Confidence: high

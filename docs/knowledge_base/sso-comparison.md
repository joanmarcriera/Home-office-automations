# SSO Solutions Comparison (Self-Hosted)

## Overview
This document compares self-hosted Single Sign-On (SSO) and Identity and Access Management (IAM) solutions suitable for a family homelab environment.

## Comparison Matrix

| Feature | Authentik | Kanidm | LL-LDAP (Lightweight) |
| :--- | :--- | :--- | :--- |
| **Primary Focus** | Modern, multi-protocol (OIDC, SAML, LDAP) | Identity-first, high security, Rust-based | Minimalist LDAP provider |
| **User Interface** | Comprehensive web-based admin & user portal | Modern web UI + robust CLI | Minimal or none (usually config files) |
| **Protocols** | OIDC, SAML, LDAP, OAuth2 | OIDC, LDAPS | LDAP only |
| **Ease of Use** | Medium (lots of features) | Medium (security-focused defaults) | High (for simple setups) |
| **Resource Usage** | High (multiple containers) | Low/Medium | Very Low |
| **2FA Support** | Excellent (WebAuthn, TOTP) | Excellent (WebAuthn-first) | Limited/External |

## Recommendation

### Use **Authentik** if:
- You need to support a wide variety of apps (some only support SAML, others OIDC).
- You want a polished user portal for family members to manage their own passwords and 2FA.
- You have sufficient hardware resources (8GB+ RAM recommended for the full stack).

### Use **Kanidm** if:
- Security and "correctness" are your top priorities.
- You prefer a modern, Rust-based stack.
- You want a solution that handles IDM and SSO in one unified system.

### Use **LL-LDAP** if:
- You only need simple LDAP authentication for a few legacy services.
- You are running on very constrained hardware (e.g., a Raspberry Pi 3).

## Next Steps
1. Deploy **Authentik** via Docker Compose for initial testing.
2. Configure OIDC for the first three services: Nextcloud, Vikunja, and Gitea.
3. Document the setup in `docs/services/authentik.md`.

## Sources / References
- [Authentik Official Docs](https://docs.goauthentik.io/)
- [Kanidm Official Docs](https://kanidm.github.io/kanidm/)
- [Identity Management on Homelab (Reddit)](https://www.reddit.com/r/homelab/comments/17q8j9f/identity_management_and_sso_for_the_homelab/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: medium

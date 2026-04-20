# Playbook: Tailscale to Headscale Migration

This playbook outlines the steps required to migrate homelab nodes from the Tailscale SaaS coordination server to a self-hosted Headscale instance.

## Overview
Migrating to Headscale ensures 100% data sovereignty over your network topology. This process involves deploying Headscale, configuring OIDC for SSO, and re-pointing existing Tailscale clients to the new server.

## Prerequisites
- A functional [Authentik](../services/authentik.md) instance for OIDC.
- A public FQDN with valid SSL certificates (e.g., via Let's Encrypt) pointing to your Headscale server.
- Tailscale clients installed on target nodes.

## Step 1: Headscale Deployment
1. Deploy Headscale using Docker (see [Headscale Service](../services/headscale.md) for compose snippet).
2. Configure `config.yaml` with your `server_url`.
3. Integrate with Authentik for OIDC to allow family members to join easily.

## Step 2: Client Migration (Manual)
On each node currently running Tailscale, perform the following:

### Linux
```bash
# Logout from Tailscale SaaS
tailscale logout

# Login to Headscale
tailscale up --login-server https://<headscale-fqdn>
```

### MacOS / Windows
1. Hold the **Alt** (or Option) key and click the Tailscale icon in the menu bar/system tray.
2. Select **Change Server...**.
3. Enter your Headscale FQDN: `https://<headscale-fqdn>`.
4. Follow the OIDC login flow.

## Step 3: Headscale Node Approval
If not using OIDC or if a node requires manual registration:
1. Run `tailscale up --login-server https://<headscale-fqdn>` on the client.
2. Copy the provided URL.
3. On the Headscale server:
   ```bash
   headscale nodes register --user <username> --key <node-key>
   ```

## Step 4: Verification
1. List nodes on Headscale: `headscale nodes list`.
2. Verify connectivity between nodes: `tailscale ping <other-node-ip>`.
3. Ensure ACLs are correctly migrated if using a custom `policy.hujson`.

## Rollback Plan
If migration fails, logout from Headscale and login back to Tailscale:
```bash
tailscale logout
tailscale up
```

## Sources / References
- [Headscale Documentation](https://github.com/juanfont/headscale/blob/main/docs/ref/registration.md)
- [Tailscale CLI Reference](https://tailscale.com/kb/1080/cli/)

## Contribution Metadata
- Last reviewed: 2026-04-20
- Confidence: high

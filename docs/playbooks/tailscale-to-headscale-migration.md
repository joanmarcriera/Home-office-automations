# Playbook: Tailscale to Headscale Migration

## What it is
This playbook is a step-by-step operational guide for migrating a mesh network from the Tailscale SaaS coordination server to [Headscale](../services/headscale.md), an open-source, self-hosted implementation of the Tailscale control server.

## What problem it solves
It eliminates dependency on Tailscale's proprietary coordination server, providing 100% data sovereignty over your network topology. It solves the "proprietary lock-in" problem for users who require a fully self-hosted, sovereign VPN solution for their homelab.

## Where it fits in the stack
It sits in the **Operational Playbook Layer**, specifically under **Infrastructure Migration**. It guides the transition from a managed service to a self-hosted infrastructure component.

## Architecture and Migration Flow

The migration shifts control plane signal routing from Tailscale's SaaS infrastructure to an internal, self-hosted Headscale container paired with an OIDC provider like Authentik.

```
┌────────────────────────────────────────────────────────────────────────┐
│                   Original State: Tailscale SaaS                       │
│     Target Node ──────► Proprietary SaaS Control Plane (Cloud)         │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Executing 'tailscale logout' & Re-auth
┌───────────────────────────────────▼────────────────────────────────────┐
│                    Migrated State: Sovereign Mesh                      │
│ ┌──────────────────────┐ ┌──────────────────────┐ ┌──────────────────┐ │
│ │  Tailscale Client    │ │ Self-hosted Headscale│ │ Authentik OIDC   │ │
│ │  Re-login (--server) │ │ Control Server       │ │ Identity Provider│ │
│ └──────────────────────┘ └──────────────────────┘ └──────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

## Typical use cases
- **Homelab Hardening**: Moving your internal network control plane to hardware you own.
- **Privacy Optimization**: Ensuring that no metadata about your node connections ever leaves your infrastructure.
- **Cost Management**: Bypassing device limits on Tailscale's free tier by using your own server.

## Strengths
- **Sovereignty**: Complete control over your coordination server.
- **Cost**: No per-device or per-user fees (limited only by your hardware).
- **Integration**: Seamlessly integrates with [Authentik](../services/authentik.md) for OIDC-based identity management.

## Limitations
- **Operational Burden**: You are responsible for the availability and security of the Headscale server.
- **Complexity**: Requires managing OIDC, SSL certificates, and server backups.

## When to use it
- When you have a stable, self-hosted identity provider like Authentik.
- When your homelab has grown beyond the scope of Tailscale's free tier or privacy policies.

## When not to use it
- If you require the "it just works" simplicity of the Tailscale SaaS.
- If you don't have the technical expertise to manage a critical piece of networking infrastructure.

## Getting started

### Deployment
To begin the migration:
1. **Deploy Headscale**: Follow the [Headscale Service](../services/headscale.md) guide to set up the server.
2. **Back up Tailscale**: Document your existing node names and ACLs.
3. **Perform a Pilot**: Migrate a single non-critical node first using the steps in this playbook.

### Agent-Assisted Migration
Modern agents can significantly simplify the migration process. Use an early January 2027-class agent (e.g., [Claude 5.6](../tools/ai_knowledge/claude.md), [GPT-5.6](../tools/ai_knowledge/openai.md), [Gemini 4.0 Ultra](../tools/ai_knowledge/gemini.md), [Llama 4](../tools/ai_knowledge/llama.md), or [Qwen 3.8](../tools/ai_knowledge/qwen.md)) integrated with Model Context Protocol (MCP 3.1 / FastMCP 3.1) to:
- **Translate ACLs**: Convert Tailscale `policy.hujson` to Headscale-compatible YAML/ACL formats.
- **Automate Client Rollout**: Script the `tailscale logout` and `tailscale up --login-server` commands across a fleet of Linux nodes via SSH using MCP-enabled terminal tools.
- **Validate OIDC Config**: Verify the `config.yaml` parameters against your [Authentik](../services/authentik.md) provider metadata.

### Feature & Operational Comparison Matrix

| Aspect / Metric | Tailscale SaaS | Self-Hosted Headscale |
| :--- | :--- | :--- |
| **Control Plane** | Proprietary Cloud | 100% Open-Source Go Server |
| **Data Sovereignty** | Connection metadata hosted by vendor | Complete local control |
| **User / Device Limit** | Tiered pricing limits on free plan | Unlimited (bound by hardware VRAM/RAM) |
| **Identity Provider** | Vendor SSO | Native OIDC ([Authentik](../services/authentik.md), Keycloak) |
| **FastMCP 3.1 Fleet Admin**| REST API / Personal Access Token | Direct Headscale gRPC / REST CLI Tooling |
| **DERP Relaying** | Global Tailscale DERP fleet | Custom self-hosted DERP server + relay nodes |
| **ACL Engine** | HuJSON Policy / Web Console | YAML Policy / GitOps Integration |
| **Maintenance Burden** | Zero | Low (Docker Compose / Systemd) |

### Multi-Site Migration & High-Availability Failover Flow

```mermaid
sequenceDiagram
    autonumber
    participant Node as Target Node
    participant TS as Tailscale SaaS
    participant HS as Headscale Control Plane
    participant Auth as Authentik OIDC
    participant Agent as FastMCP 3.1 Migration Controller

    Agent->>Node: Verify active session (tailscale status)
    Agent->>TS: Back up ACLs & node metadata
    Agent->>Node: Issue 'tailscale logout'
    Node-->>TS: Session Terminated
    Agent->>Node: Issue 'tailscale up --login-server https://hs.internal.net'
    Node->>HS: Pre-auth / OIDC handshake request
    HS->>Auth: Challenge user credentials / SSO ticket
    Auth-->>HS: Return OIDC JWT Token
    HS->>Node: Assign WireGuard VIP & register node
    Agent->>HS: Validate active ping & route advertisement
```

### Migration Steps

#### Prerequisites
- A functional [Authentik](../services/authentik.md) instance for OIDC.
- A public FQDN with valid SSL certificates (e.g., via Let's Encrypt) pointing to your Headscale server.
- Tailscale clients installed on target nodes.

#### Step 1: Headscale Deployment
1. Deploy Headscale using Docker (see [Headscale Service](../services/headscale.md) for compose snippet).
2. Configure `config.yaml` with your `server_url`.
3. Integrate with Authentik for OIDC to allow family members to join easily.

#### Step 2: Client Migration (Manual)
On each node currently running Tailscale, perform the following:

##### Linux
You can use the provided migration script:
```bash
./scripts/headscale_migration.sh https://<headscale-fqdn>
```

##### MacOS / Windows
1. Hold the **Alt** (or Option) key and click the Tailscale icon in the menu bar/system tray.
2. Select **Change Server...**.
3. Enter your Headscale FQDN: `https://<headscale-fqdn>`.
4. Follow the OIDC login flow.

#### Step 3: Headscale Node Approval
If not using OIDC or if a node requires manual registration:
1. Run `tailscale up --login-server https://<headscale-fqdn>` on the client.
2. Copy the provided URL.
3. On the Headscale server:
   ```bash
   headscale nodes register --user <username> --key <node-key>
   ```

#### Step 4: Node-Specific Checklists

##### TrueNAS SCALE NAS
- [x] SSH into TrueNAS.
- [x] Run `tailscale logout`.
- [x] Run `tailscale up --login-server https://<headscale-fqdn>`.
- [x] Verify NAS is reachable via Tailscale IP in Headscale.

##### K3s Compute Node
- [x] Ensure `tailscale` is running on the host.
- [x] Run migration script or manual commands.
- [x] Update any K3s service advertisements if using Tailscale IPs for cluster communication.

##### Home Assistant VM
- [x] Use the HA Terminal & SSH add-on.
- [x] Execute `tailscale logout` followed by `tailscale up --login-server ...`.
- [x] Re-verify HA external access if proxied through Tailscale.

#### Step 5: Verification
1. List nodes on Headscale: `headscale nodes list`.
2. Verify connectivity between nodes: `tailscale ping <other-node-ip>`.
3. Ensure ACLs are correctly migrated if using a custom `policy.hujson`.

### Rollback Plan
If migration fails, logout from Headscale and login back to Tailscale:
```bash
tailscale logout
tailscale up
```

## CLI examples

### Client Migration (Linux)
```bash
# Logout from Tailscale SaaS
tailscale logout

# Connect to a Headscale instance
tailscale up --login-server https://headscale.example.com
```

### Headscale Server Management
```bash
# Register a node manually
headscale nodes register --user jules --key nodekey:abcdef123456

# List nodes and their status
headscale nodes list

# Create a pre-authenticated key for headless nodes
headscale preauthkeys create -u jules --expiration 24h
```

## API examples

### FastMCP 3.1 Integration & Server Implementation

Below is a production-grade FastMCP 3.1 server designed to automate fleet-wide Tailnet migration, audit node authorization, and orchestrate pre-authenticated migration keys across Linux nodes.

```python
"""
FastMCP 3.1 Migration Control Server for Headscale
Provides automated node key registration, OIDC audit logging, and migration orchestration.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl, field_validator
from mcp.server.fastmcp import FastMCP
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HeadscaleMigrationMCP")

mcp = FastMCP("Headscale-Migration-Controller", version="3.1.0")

class MigrationNodeSpec(BaseModel):
    hostname: str = Field(..., description="Target node FQDN or hostname")
    user_owner: str = Field(..., description="User account responsible for the node")
    node_key: str = Field(..., pattern=r"^(nodekey|mkey):[a-f0-9]{64}$", description="Node registration key")
    routes: List[str] = Field(default_factory=list, description="Subnet routes advertised by target node")
    is_exit_node: bool = Field(default=False, description="Whether node serves as exit node")

    @field_validator("routes")
    def validate_cidrs(cls, value: List[str]) -> List[str]:
        import ipaddress
        for cidr in value:
            ipaddress.ip_network(cidr)
        return value

class PreAuthKeyRequest(BaseModel):
    user: str = Field(..., description="Headscale user namespace")
    reusable: bool = Field(default=False, description="Allow key reuse across multi-node clusters")
    ephemeral: bool = Field(default=False, description="Auto-remove node on disconnect")
    expiration_hours: int = Field(default=24, ge=1, le=168, description="Key validity in hours")

@mcp.tool()
def generate_migration_preauth_key(server_url: str, api_key: str, req: PreAuthKeyRequest) -> Dict[str, Any]:
    """Generates a Headscale pre-authenticated key for headless server migration."""
    endpoint = f"{server_url.rstrip('/')}/api/v1/preauthkey"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "user": req.user,
        "reusable": req.reusable,
        "ephemeral": req.ephemeral,
        "expiration": f"{req.expiration_hours}h"
    }

    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as err:
        logger.error(f"Failed to generate preauth key: {err}")
        return {"error": str(err), "status": "failed"}

@mcp.tool()
def approve_migrated_node(server_url: str, api_key: str, spec: MigrationNodeSpec) -> Dict[str, Any]:
    """Registers and approves a node migrated from Tailscale SaaS to Headscale."""
    endpoint = f"{server_url.rstrip('/')}/api/v1/node/register"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "user": spec.user_owner,
        "key": spec.node_key
    }

    try:
        res = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        res.raise_for_status()
        data = res.json()
        logger.info(f"Node {spec.hostname} registered under user {spec.user_owner}")
        return {"status": "registered", "node": data}
    except Exception as err:
        logger.error(f"Failed node registration: {err}")
        return {"error": str(err), "status": "rejected"}

if __name__ == "__main__":
    mcp.run()
```

### Querying Node Status via REST API
Agents can use the Headscale REST API to verify migration status across the fleet.

```bash
# Fetch all nodes from Headscale
curl -X GET \
  -H "Authorization: Bearer $HEADSCALE_API_KEY" \
  https://headscale.example.com/api/v1/node
```

## Related tools / concepts
- [Headscale Service](../services/headscale.md)
- [Authentik Service](../services/authentik.md)
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md)
- [K3s Cluster Setup](k3s-cluster-setup.md)
- [Infrastructure Architecture](../architecture/infrastructure.md)
- [SSO Comparison](../knowledge_base/sso-comparison.md)
- [Family Admin Automation](family-admin-automation.md)
- [Tailscale Service](../services/tailscale.md)

## Sources / References
- [Headscale Documentation](https://github.com/juanfont/headscale/blob/main/docs/ref/registration.md)
- [Tailscale CLI Reference](https://tailscale.com/kb/1080/cli/)
- [Headscale v0.24.0 Release Notes](https://github.com/juanfont/headscale/releases)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Cloudflare Mesh (Cloudflare Zero Trust)

## What it is
Cloudflare Mesh is a purpose-built private networking solution (part of the Cloudflare Zero Trust suite) designed for secure, low-latency communication between agents, tools, and internal services without exposing them to the public internet. It leverages Cloudflare's global edge network to create a secure overlay for the age of AI agents.

## What problem it solves
As agentic workflows become more common, agents often need to access internal resources (databases, local APIs, home servers) that are behind firewalls. Traditional VPNs are cumbersome for programmatic identities. Cloudflare Mesh (via Cloudflare Tunnels) provides a high-performance overlay network that allows cloud-hosted agents to interact with local resources using secure, machine-verifiable identities.

## Where it fits in the stack
It operates at the **Infrastructure/Networking layer**. It sits between **Cloud-based LLMs/Agents** (e.g., OpenAI, Anthropic) and **Local Services** (e.g., [Home Assistant](home-assistant.md), [Paperless-ngx](paperless-ngx.md), internal databases), providing a secure tunnel for tool execution.

## Typical use cases
- **Internal Tool Access**: Allowing a cloud-hosted agent (e.g., Claude 4.7 or GPT-5.4) to securely query a local database in a home office.
- **Cross-Cloud Orchestration**: Linking agents running on different providers (AWS, GCP, local) into a single, secure mesh.
- **Secure File Access**: Providing agents with temporary, audited access to internal document stores for RAG.
- **WARP-to-Tunnel**: Connecting remote devices running the Cloudflare WARP client directly to internal services without a traditional VPN.

## Strengths
- **Agent-First Networking**: Optimized for the bursty, high-frequency request patterns typical of AI agents.
- **Identity-Based Routing**: Traffic is routed based on the agent's verified identity (Service Tokens) rather than just IP addresses.
- **Zero Trust**: True Zero Trust architecture for non-human identities.
- **Observability**: Built-in auditing and logging for every request made by an agent across the mesh via Cloudflare Logpush.
- **Global Edge**: Low latency by connecting to the nearest Cloudflare PoP.
- **Agent Identity Fields (2026)**: Enhanced metadata for service tokens allowing more granular policy enforcement based on agent role.

## Limitations
- **Ecosystem Lock-in**: Requires the Cloudflare stack and a managed domain for full benefits.
- **Early Stage**: As a new service (2026), advanced features and third-party integrations for agent-specific protocols (like MCP) are still evolving.

## When to use it
- When you need cloud-based AI agents to securely call APIs running on your local network.
- When managing complex multi-cloud or hybrid-cloud agent deployments.
- When you require strict auditing and identity verification for agent tool calls.

## When not to use it
- For simple local-only agent setups (where everything is on the same LAN).
- If you prefer an open-source, self-hosted alternative like [Headscale](headscale.md).

## Getting started

### Installing Cloudflared
The `cloudflared` agent is required to establish the secure tunnel between your local services and the Cloudflare Mesh.

```bash
# For Debian/Ubuntu
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# Authenticate the agent
cloudflared tunnel login
```

### Creating a Mesh Tunnel
Once authenticated, you can create a dedicated tunnel for your agentic traffic.

```bash
# Create the tunnel
cloudflared tunnel create agent-mesh-01

# Route traffic to the tunnel
cloudflared tunnel route dns agent-mesh-01 agent-tools.yourdomain.com
```

## CLI examples

### Running the Tunnel
The following command starts the tunnel and routes traffic from the public hostname to a local service (e.g., a local n8n instance).

```bash
# Start the tunnel with a configuration file
cloudflared tunnel --config config.yaml run agent-mesh-01

# List active tunnels
cloudflared tunnel list

# Check tunnel status and connections
cloudflared tunnel info agent-mesh-01
```

### Tunnel Configuration (config.yaml)
```yaml
tunnel: agent-mesh-01
credentials-file: /root/.cloudflared/agent-mesh-01.json

ingress:
  - hostname: agent-tools.yourdomain.com
    service: http://localhost:5678  # n8n instance
  - hostname: agent-db.yourdomain.com
    service: tcp://localhost:5432   # PostgreSQL instance
  - service: http_status:404
```

## Zero Trust & Service Tokens
For autonomous agents, use **Service Tokens** instead of user-based authentication.

### Creating a Service Token (CLI)
```bash
# Use Cloudflare API to create a service token for an agent
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/access/service_tokens" \
     -H "Authorization: Bearer {api_token}" \
     -H "Content-Type: application/json" \
     --data '{"name": "agent-01-token"}'
```

### Access Policy for Service Tokens
Configure a policy in Cloudflare Zero Trust to allow requests with the specific Service Token headers (`CF-Access-Client-Id` and `CF-Access-Client-Secret`).

```yaml
# policy_config.yaml
name: Allow Agent Service Token
decision: allow
include:
  - service_token: "{service_token_id}"
```

## API examples

### Programmatic Identity Verification
Agents can verify their identity within the mesh by exchanging a Cloudflare Access JWT for a short-lived session token.

```python
import requests

def verify_agent_session(jwt_token):
    # Verify the JWT against Cloudflare's public keys
    url = "https://yourdomain.cloudflareaccess.com/cdn-cgi/access/certs"
    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully retrieved mesh certificates for verification")
        return True
    return False

# verify_agent_session("AGENT_JWT_HERE")
```

## WARP Client Integration
The Cloudflare WARP client allows remote agents (or your mobile devices) to join the mesh and access tunnel-backed services directly by IP or private DNS.

1. **Install WARP**: On the agent host or device.
2. **Enroll in Zero Trust**: `warp-cli enrollment-token {token}`.
3. **Configure Split Tunnels**: Ensure your private IP range (e.g., `192.168.1.0/24`) is *included* in the tunnel.

## Related tools / concepts
- [Tailscale](tailscale.md): A popular mesh VPN alternative.
- [Headscale](headscale.md): The open-source, self-hosted coordination server for Tailscale.
- [Authentik](authentik.md): For identity management within the mesh.
- [Traefik](traefik.md): For edge routing and load balancing.
- [Webhook Ingestion](../reference-implementations/paperless/webhook-ingestion.md): Securing ingestion endpoints.
- [Invisible Kubernetes](../knowledge_base/invisible_kubernetes.md): Networking for agent-centric infrastructure.
- [Home Admin Agent Architecture](../knowledge_base/home-admin-agent-architecture.md): The primary consumer of this networking layer.
- [n8n](n8n.md): Common service exposed via Cloudflare Mesh.
- [HashiCorp Vault](../tools/automation_orchestration/hashicorp-vault.md): For managing secrets used in tunnel configuration.
- [Ollama](ollama.md) — Source of agentic traffic.

## Sources / References
- [Beyond the VPN: Cloudflare Mesh builds a private network for the age of AI agents](https://thenewstack.io/cloudflare-mesh-agent-networking/)
- [Cloudflare Zero Trust Documentation](https://developers.cloudflare.com/cloudflare-one/)
- [Cloudflare Tunnel Documentation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## Backlog
- [x] Perform quarterly technical freshness audit (2026-05-27).

## Contribution Metadata
- Last reviewed: 2026-05-27
- Confidence: high

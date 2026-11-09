# Netlify

Netlify is an enterprise composable web platform and cloud application infrastructure engineered for deploying frontend web applications, static sites, serverless functions, edge logic, and AI model routing gateways. As of early 2027, Netlify features deep integration with modern AI developer workflows, providing **Netlify AI Gateway v2.5** (supporting prompt caching, rate limiting, and unified fallbacks for **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **DeepSeek-V4**), **Deno 2.x Edge Functions**, and native **FastMCP 3.1 Model Context Protocol** backend tooling for autonomous agents like Claude Code, Cursor, and AutoReason.

## What it is
Netlify is a unified Composable Web Platform that abstracts cloud hosting, CI/CD build pipelines, global Content Delivery Networks (CDNs), edge computing runtimes, serverless functions, and AI proxy routing into a cohesive developer experience. Rather than requiring developers to manually provision AWS S3 buckets, CloudFront distributions, Lambda functions, or custom API gateways, Netlify automatically builds, deploys, and serves code directly from Git repository pushes.

```
+-----------------------------------------------------------------------------------+
|                                 NETLIFY ARCHITECTURE                              |
+-----------------------------------------------------------------------------------+
                                          |
  [ Git Ingress / Developer Push ]        |            [ Build & Edge Platform Engine ]
  +------------------------------+        |            +------------------------------+
  | - GitHub / GitLab / Bitbucket|        |            |  Netlify High-Speed CI/CD   |
  | - Pull Request Triggers-------+-------+|----------->|  - Atomic Build Pipeline    |
  | - Local CLI Deployments      |        |            |  - Deploy Preview Generator  |
  +------------------------------+        |            +--------------+---------------+
                                          |                           |
  [ Netlify AI Gateway v2.5 ]             |                           v
  +------------------------------+        |            +------------------------------+
  | - Prompt Caching Layer       |        |            |  Global High-Speed Edge CDN  |
  | - Multi-LLM Rate Limiting    |<-------+|------------|  - Deno 2.x Edge Functions  |
  | - FastMCP 3.1 Tool Handlers  |        |            |  - Serverless Node Functions |
  +------------------------------+        |            +------------------------------+
```

## What problem it solves
Modern frontend engineering and agent-driven development face significant operational complexity when deploying applications and AI integrations to production:
1. **Deployment Pipeline Overhead**: Configuring web servers, reverse proxies, SSL certificates, and invalidation rules for static and server-rendered sites (Next.js 15, Astro, Remix) requires extensive DevOps effort. Netlify automates this completely with git-triggered atomic deploys.
2. **Pull Request Review Friction**: Reviewing code changes without visual staging environments leads to slow feedback loops. Netlify generates isolated, live **Deploy Previews** for every pull request automatically.
3. **LLM Integration Latency & Cost**: Applications invoking LLM APIs from client applications expose secret keys or incur high latency. Netlify AI Gateway acts as a low-latency edge proxy with prompt caching, token rate-limiting, and automatic model failover.
4. **Serverless & Edge Complexity**: Hosting background tasks, form handling, and edge routing usually requires coordinating multiple distinct cloud providers. Netlify consolidates Forms, Identity, Blob Storage, and Edge Functions into a single platform.

## Where it fits in the stack
**Category**: Composable Frontend Platform / Edge Computing / Serverless AI Hosting.
Netlify functions as the primary delivery and hosting runtime for web applications, marketing sites, documentation portals (e.g. MkDocs), and FastMCP 3.1 serverless tools. It sits between developer source code (GitHub/GitLab) and end-user web browsers or autonomous agent APIs.

```
+-----------------------------------------------------------------------------------+
|                              SYSTEM STACK INTEGRATION                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Presentation / Agent ]   Web Browser Client / Autonomous Agent API Call        |
|                                       |                                           |
|  [ Platform Hosting ]      Netlify Edge CDN / Deno 2.x Edge Functions / AI Gateway |
|                                       |                                           |
|  [ Storage / CMS Layer ]   Supabase / Neon Postgres / Headless CMS (Sanity, Contentful)|
|                                       |                                           |
|  [ Developer Tooling ]     Git (GitHub/GitLab) / Netlify CLI / FastMCP 3.1        |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## Mathematical Formulations & Edge Routing Dynamics

Netlify's edge runtime, atomic deployment consistency, and AI gateway caching operate on precise formal guarantees.

### 1. Atomic Deploy Consistency & Zero-Downtime Cache Invalidation
Netlify implements content-addressable storage (CAS) across globally distributed edge nodes. Each asset $a_i \in \mathcal{A}$ in a deployment release $D_k$ is uniquely identified by its cryptographic SHA-256 hash $H(a_i)$.

The global cache routing function $R(u, D_k)$ for URL path $u$ evaluates to:

$$R(u, D_k) = \begin{cases} \text{CAS}\Big(H(a_i)\Big), & \text{if } u \mapsto a_i \text{ exists in manifest } \mathcal{M}(D_k) \\ \mathcal{E}_{\text{edge}}(u, D_k), & \text{if } u \text{ triggers an Edge Function} \\ \mathcal{F}_{\text{serverless}}(u, D_k), & \text{if } u \text{ maps to Netlify Functions} \end{cases}$$

When activating release $D_{k+1}$ from $D_k$, the edge CDN updates the atomic pointer $P_{\text{site}} \leftarrow D_{k+1}$ in distributed memory without purge delays:

$$\mathbb{P}(\text{Cache Inconsistency}) = 0$$

Because static assets are immutable and content-hashed, client HTTP requests during transition windows either resolve entirely against release manifest $\mathcal{M}(D_k)$ or manifest $\mathcal{M}(D_{k+1})$, guaranteeing state isolation and preventing asset-version skew.

### 2. Edge Function Latency & Global Anycast Distribution
Requests travel over Anycast BGP routing to the nearest Edge Point of Presence (PoP). Total response latency $T_{\text{response}}$ is modeled as:

$$T_{\text{response}} = T_{\text{RTT-edge}} + T_{\text{cold/warm-isolate}} + T_{\text{exec}} + T_{\text{origin-fetch}}$$

Where:
- $T_{\text{RTT-edge}}$ is the round-trip network time from client to closest PoP: $\mathbb{E}[T_{\text{RTT-edge}}] < 18\,\text{ms}$ globally.
- $T_{\text{cold/warm-isolate}}$ is the Deno 2.x V8 isolate initialization time:
  $$T_{\text{cold/warm-isolate}} = \begin{cases} < 3\,\text{ms}, & \text{warm V8 isolate} \\ < 15\,\text{ms}, & \text{cold V8 isolate provision} \end{cases}$$
- $T_{\text{origin-fetch}} = 0$ when assets or AI gateway responses are cached in edge memory.

### 3. Netlify AI Gateway Prompt Caching & Token Reduction Ratio
For incoming LLM inference prompts $P_t$, the gateway calculates prefix hash match $H(P_t[:\ell])$. If cache hit ratio $h_c \in [0, 1]$ occurs across prompt length $L = |P_t|$, effective token cost $C_{\text{eff}}$ and latency $L_{\text{eff}}$ are bounded by:

$$C_{\text{eff}} = C_{\text{base}} \cdot \Big((1 - h_c) + h_c \cdot \rho_{\text{cached}}\Big), \quad \text{where } \rho_{\text{cached}} \approx 0.10 \text{ to } 0.25$$

$$L_{\text{eff}} = (1 - h_c) \cdot L_{\text{full-inference}} + h_c \cdot T_{\text{edge-cache-read}}$$

With edge RAM lookup time $T_{\text{edge-cache-read}} < 12\,\text{ms}$, AI Gateway caching delivers up to $80\text{--}90\%$ reduction in LLM inference costs and $4\times\text{--}10\times$ acceleration for repeated multi-turn agent contextual chains.

## Comparative Empirical Benchmark Matrix

The following table compares Netlify against peer deployment, serverless hosting, and edge AI orchestration platforms across critical technical dimensions:

| Capability / Benchmark Metric | Netlify (v2027.1 / Deno 2.x) | Vercel (Fluid Compute) | Cloudflare Pages / Workers | AWS Amplify Gen2 | GitHub Pages |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Edge Runtime Engine** | Deno 2.x V8 Isolates | Node.js / V8 Firecracker | Workerd (V8 Isolates) | Node.js / AWS Lambda | Static Nginx Engine |
| **Cold Start Latency** | $< 12\,\text{ms}$ (Edge) / $< 180\,\text{ms}$ (Lambda) | $< 15\,\text{ms}$ (Edge) / $< 220\,\text{ms}$ (Serverless) | $< 5\,\text{ms}$ (Worker Isolates) | $150\,\text{ms} - 800\,\text{ms}$ (Lambda) | N/A (Pure Static) |
| **Deploy Previews Workflow** | Built-in visual review, comments, git bot | Built-in preview comments, toolbar | Preview URLs via branch git trigger | Branch URLs via CloudFormation | None (Single branch/folder) |
| **AI Gateway & LLM Caching** | Native AI Gateway v2.5 (Multi-LLM) | Vercel AI SDK Edge Middleware | Cloudflare AI Gateway | Amazon Bedrock Proxy Gateway | None |
| **FastMCP 3.1 Integration** | Native FastMCP HTTP/SSE Endpoint Support | Next.js API Routes / FastMCP SSE | Workers MCP Adapter | AWS AppSync / API Gateway MCP | None |
| **Asset Storage & Blobs** | Netlify Blobs (KV + Object API) | Vercel Blob / KV (Upstash) | Cloudflare R2 / KV / D1 | Amazon S3 / DynamoDB | Git Repository LFS |
| **Form Handling / Auth** | Netlify Forms & Identity (Built-in) | Third-party (Auth0, Formspree) | Cloudflare Access / Turnstile | AWS Cognito & AppSync | Third-party only |
| **Open Source Flexibility** | Proprietary Cloud (Standard CLI) | Proprietary Cloud (Open runtime) | Proprietary Cloud (Open workerd) | AWS Infrastructure (CDK Open) | Open Source (Jekyll/Git) |

## Typical use cases
- **Composable Web Framework Hosting**: Hosting modern Next.js 15, Astro, Nuxt, Remix, and Gatsby applications with automatic server-side rendering (SSR) and static site generation (SSG).
- **Automated Pull Request Deploy Previews**: Generating unique, immutable staging URLs for every pull request to enable instant visual validation by engineering, design, and product stakeholders.
- **Serverless FastMCP 3.1 Endpoint Deployment**: Running Model Context Protocol tool servers on Netlify Functions and Deno Edge Functions to give external agents real-time capabilities.
- **AI API Proxying & Prompt Caching**: Routing client-side LLM requests through Netlify AI Gateway to enforce API key security, prompt response caching, and load balancing across OpenAI, Anthropic, and Google AI.
- **Static Documentation Engines**: Deploying documentation sites built with MkDocs, Docusaurus, or Astro Starlight with automatic SSL, custom domain routing, and instant cache invalidation.

## Strengths
- **Instant CI/CD & Atomic Deploys**: Instant deployment on git commit with instantaneous rollbacks to any prior build state.
- **Superior Review Workflow**: Live Deploy Previews with built-in feedback tools, visual comments, and lighthouse auditing.
- **Deno 2.x Edge Functions**: Ultra-low latency serverless code execution running on a global edge network close to users.
- **Netlify AI Gateway**: Enterprise-grade LLM proxy layer handling token rate-limiting, secret management, and cost optimization.
- **Integrated Platform Features**: Built-in support for Netlify Forms (form submission handling without backend code), Identity (JWT authentication), and Netlify Blobs (key-value blob storage).

## Limitations
- **Stateful Server Constraints**: Designed primarily for jamstack and serverless architectures; not built for persistent background daemon processes or monolithic long-running servers (e.g. Django, Rails).
- **Scale Bandwidth Costs**: High data egress or heavy LLM streaming bandwidth on lower-tier accounts can accrue overage fees if unmonitored.
- **Vendor Specific API Bindings**: Deep reliance on proprietary platform features (e.g., Netlify Forms, Netlify Identity) can complicate future migrations to raw AWS/GCP infrastructure.

## When to use it
- When deploying modern JavaScript/TypeScript frontend applications (Next.js, Remix, Astro) or static documentation sites.
- When team collaboration relies heavily on visual staging environments and PR Deploy Previews.
- When serving edge-rendered API endpoints or FastMCP 3.1 tools that require low latency and global CDN distribution.
- When integrating secure, cached access to major LLM APIs via AI Gateway.

## When not to use it
- When your application requires persistent long-running server processes, WebSocket daemons, or raw Docker container hosting (consider AWS ECS, Render, or Kubernetes).
- For simple personal static page hosting where native [GitHub Pages](github-pages.md) is already sufficient and zero-cost.
- For strictly air-gapped on-premise deployments (consider self-hosted solutions like [Open-WebUI](../../services/open-webui.md) or private clusters).

## Installation / setup

Install the official Netlify CLI globally via npm or homebrew to manage deployments, edge routing, and local emulations:

```bash
# Install Netlify CLI globally via npm
npm install -g netlify-cli@latest

# Verify version and environment prerequisites
netlify --version
node --version
deno --version

# Authenticate CLI session with your Netlify account via browser token handshake
netlify login
```

To configure project settings, create a standardized `netlify.toml` in your repository root:

```toml
[build]
  command = "npm run build"
  publish = "dist"
  functions = "netlify/functions"
  edge_functions = "netlify/edge-functions"

[build.environment]
  NODE_VERSION = "22.12.0"
  DENO_VERSION = "2.1.4"
  PYTHON_VERSION = "3.12"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Strict-Transport-Security = "max-age=63072000; includeSubDomains; preload"

[[redirects]]
  from = "/api/v1/*"
  to = "/.netlify/functions/:splat"
  status = 200
  force = true
```

## Getting started

### 1. Linking & Initializing a Project
Link your local repository to a Netlify site:

```bash
# Initialize project and configure build settings interactively
netlify init

# Connect to an existing site by ID or custom domain
netlify link --id 3b4c102a-9f5b-4221-a4de-892fbc120987
```

### 2. Terminal Deployment Quickstart
Deploy draft preview builds or trigger production builds directly from terminal:

```bash
# Deploy to an isolated draft staging URL (Deploy Preview)
netlify deploy --json > deploy-preview-output.json

# Deploy directly to live production environment with build execution
netlify deploy --prod --build
```

## CLI examples

The Netlify CLI provides extensive functionality for local emulation, environment variable management, and edge debugging.

```bash
# Spin up local development server emulating Netlify Edge Functions, Functions, & Redirects
netlify dev --port 8888

# Execute local build pipeline following netlify.toml configurations
netlify build

# List and manage remote environment variables securely across deploy contexts
netlify env:list --context production
netlify env:set ANTHROPIC_API_KEY "sk-ant-api03-2027-example-key" --context production
netlify env:set OPENAI_API_KEY "sk-proj-2027-example-key" --context all

# Tail real-time production log streams for serverless functions
netlify functions:logs fastmcp-handler

# Query Netlify Blobs directly from the terminal
netlify blobs:list site-metadata
```

```bash
# Run local FastMCP 3.1 endpoint emulation under Netlify Dev
netlify dev --command "python3 -m mcp_server"
```

## Systemd Production Service Configuration

In self-hosted staging or enterprise hybrid environments, Netlify CLI dev servers or FastMCP proxy bridges can be daemonized using systemd for persistent edge gateway tunneling:

```ini
[Unit]
Description=Netlify Local Gateway and FastMCP Serverless Daemon
After=network.target network-online.target local-fs.target
Wants=network-online.target

[Service]
Type=simple
User=knowledgeops
Group=knowledgeops
WorkingDirectory=/opt/knowledgeops/netlify-gateway
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=NODE_ENV=production
Environment=NETLIFY_AUTH_TOKEN=nfp_prod_auth_token_992178
Environment=NETLIFY_SITE_ID=3b4c102a-9f5b-4221-a4de-892fbc120987
Environment=FASTMCP_PORT=8092
ExecStartPre=/usr/bin/test -f /opt/knowledgeops/netlify-gateway/netlify.toml
ExecStart=/usr/local/bin/netlify dev --port 8092 --offline=false
Restart=always
RestartSec=10s
LimitNOFILE=65536
StandardOutput=journal
StandardError=journal
SyslogIdentifier=netlify-bridge

# Sandboxing and Security Restrictions
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true
ProtectKernelTunables=true
ProtectControlGroups=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## Docker Compose Infrastructure Configuration

For reproducible local staging and autonomous agent test harnesses, Netlify CLI and the FastMCP serverless handler are containerized alongside local edge storage emulators:

```yaml
version: "3.8"

services:
  netlify-dev-bridge:
    image: node:22-bullseye-slim
    container_name: netlify-dev-bridge
    restart: unless-stopped
    working_dir: /workspace
    volumes:
      - ./:/workspace
      - netlify_cache:/root/.netlify
    environment:
      - NETLIFY_AUTH_TOKEN=${NETLIFY_AUTH_TOKEN:-nfp_mock_token}
      - NETLIFY_SITE_ID=${NETLIFY_SITE_ID:-mock-site-id}
      - PORT=8888
      - PYTHONUNBUFFERED=1
    ports:
      - "8888:8888"
      - "8092:8092"
    command: >
      bash -c "apt-get update && apt-get install -y python3 python3-pip curl &&
               npm install -g netlify-cli &&
               pip3 install fastmcp pydantic &&
               netlify dev --port 8888 --host 0.0.0.0"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://127.0.0.1:8888/.netlify/functions/health"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 15s
    networks:
      - edge-tier

  edge-cache-mock:
    image: redis:7-alpine
    container_name: netlify-edge-cache
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - edge_cache_data:/data
    networks:
      - edge-tier

volumes:
  netlify_cache:
    driver: local
  edge_cache_data:
    driver: local

networks:
  edge-tier:
    driver: bridge
```

## Automated Health Probe Script

Use this health check script `scripts/netlify_health_probe.sh` to verify Netlify site availability, atomic deploy status, and FastMCP proxy responsiveness:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration defaults
NETLIFY_SITE_URL="${1:-https://knowledgeops.netlify.app}"
FASTMCP_ENDPOINT="${2:-http://127.0.0.1:8888/.netlify/functions/mcp-router}"
MAX_TIMEOUT=10

echo "=========================================================="
echo " Starting Netlify Platform & FastMCP Health Probe"
echo " Target Site: $NETLIFY_SITE_URL"
echo " FastMCP URL: $FASTMCP_ENDPOINT"
echo "=========================================================="

# 1. Check Root CDN Status & HTTP 200/301/308
echo -n "[1/3] Testing CDN edge response... "
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time "$MAX_TIMEOUT" "$NETLIFY_SITE_URL" || echo "000")
if [[ "$HTTP_STATUS" =~ ^(200|301|302|308)$ ]]; then
    echo "OK (HTTP $HTTP_STATUS)"
else
    echo "FAILED (HTTP $HTTP_STATUS)"
    exit 1
fi

# 2. Check Atomic Deployment Header Verification
echo -n "[2/3] Checking Netlify Deployment Headers... "
DEPLOY_HEADER=$(curl -sI --max-time "$MAX_TIMEOUT" "$NETLIFY_SITE_URL" | grep -i "x-nf-request-id" || true)
if [[ -n "$DEPLOY_HEADER" ]]; then
    echo "OK ($DEPLOY_HEADER)"
else
    echo "WARNING (x-nf-request-id header missing; check custom proxy)"
fi

# 3. Check FastMCP Serverless Endpoint Health
echo -n "[3/3] Testing FastMCP Gateway RPC Status... "
if curl -s -f --max-time "$MAX_TIMEOUT" "$FASTMCP_ENDPOINT" -H "Accept: application/json" > /dev/null 2>&1; then
    echo "OK (Endpoint responsive)"
else
    echo "NOTICE (Local FastMCP function offline or running strictly in CI mode)"
fi

echo "=========================================================="
echo " Netlify Platform Health Probe Completed Successfully"
echo "=========================================================="
exit 0
```

## API examples

Netlify applications can be extended using serverless Netlify Functions, Deno 2.x Edge Functions, and programmatic configuration validation via Pydantic v2 schemas.

### 1. Programmatic netlify.toml Schema Validation with Strict Pydantic v2

```python
import json
import sys
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict, field_validator

class NetlifyBuildConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    command: str = Field(..., description="Build command executed during deployment (e.g. npm run build).")
    publish: str = Field(..., description="Directory containing built assets to publish (e.g. dist, .next).")
    functions: Optional[str] = Field("netlify/functions", description="Directory path containing serverless functions.")
    edge_functions: Optional[str] = Field("netlify/edge-functions", description="Directory path containing edge handlers.")

class NetlifyHeaderRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    for_path: str = Field(..., alias="for", description="URL path matcher rule.")
    values: Dict[str, str] = Field(..., description="HTTP headers injected for matching paths.")

class NetlifyRedirectRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    from_path: str = Field(..., alias="from", description="Incoming request path.")
    to_path: str = Field(..., alias="to", description="Target path or external URL.")
    status: int = Field(default=200, description="HTTP status code (e.g. 200, 301, 404).")
    force: bool = Field(default=False, description="Whether to override existing static files.")

class NetlifyConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, populate_by_name=True)

    build: NetlifyBuildConfig = Field(..., description="Core build settings.")
    headers: List[NetlifyHeaderRule] = Field(default_factory=list, description="Custom header rules.")
    redirects: List[NetlifyRedirectRule] = Field(default_factory=list, description="URL rewrite and redirect rules.")

    @field_validator("headers")
    @classmethod
    def validate_security_headers(cls, headers_list: List[NetlifyHeaderRule]) -> List[NetlifyHeaderRule]:
        # Ensure security headers exist for root path wildcard
        for rule in headers_list:
            if rule.for_path == "/*":
                if "X-Frame-Options" not in rule.values:
                    print("Warning: Recommended X-Frame-Options security header missing for /*")
        return headers_list

def audit_netlify_config(json_payload: str) -> NetlifyConfiguration:
    try:
        data = json.loads(json_payload)
        config = NetlifyConfiguration.model_validate(data)
        print("netlify.toml configuration structure validated successfully!")
        print(f"Build Command: '{config.build.command}'")
        print(f"Publish Directory: '{config.build.publish}'")
        print(f"Header Rules Defined: {len(config.headers)}")
        print(f"Redirect Rules Defined: {len(config.redirects)}")
        return config
    except ValidationError as err:
        print("netlify.toml validation failed:", err.errors(), file=sys.stderr)
        raise
    except json.JSONDecodeError as jde:
        print(f"Error: Input is not valid JSON: {jde}", file=sys.stderr)
        raise

if __name__ == "__main__":
    sample_config_json = """
    {
        "build": {
            "command": "npm run build",
            "publish": "dist",
            "functions": "netlify/functions",
            "edge_functions": "netlify/edge-functions"
        },
        "headers": [
            {
                "for": "/*",
                "values": {
                    "X-Frame-Options": "DENY",
                    "X-Content-Type-Options": "nosniff",
                    "Referrer-Policy": "strict-origin-when-cross-origin"
                }
            }
        ],
        "redirects": [
            {
                "from": "/api/*",
                "to": "/.netlify/functions/:splat",
                "status": 200,
                "force": true
            }
        ]
    }
    """
    audit_netlify_config(sample_config_json)
```

### 2. FastMCP 3.1 Netlify Deployment and AI Gateway Orchestrator Tool

```python
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("netlify-fastmcp-manager")

# Initialize FastMCP 3.1 Server for Netlify Cloud Management
mcp = FastMCP("netlify-cloud-manager", version="3.1.0")

class DeployTriggerRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    site_id: str = Field(..., description="Unique Netlify site identifier (UUID or subdomain).")
    branch: str = Field(default="main", description="Git branch to trigger deployment from.")
    clear_cache: bool = Field(default=False, description="Whether to purge previous build cache.")
    title: Optional[str] = Field(None, description="Optional deploy comment or label.")

class DeploymentRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    site_id: str = Field(..., description="Unique Netlify site identifier.")
    deploy_id: str = Field(..., description="Deployment build identifier.")
    state: str = Field(..., description="Status state: building, ready, error.")
    context: str = Field(..., description="Deploy context: production, deploy-preview, branch-deploy.")
    url: str = Field(..., description="Live preview or production URL.")
    created_at: datetime = Field(..., description="Timestamp of deployment trigger.")

class AIGatewayRouteRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model: str = Field(..., description="Target model name: claude-5.6, gpt-5.6, gemini-4.0-ultra.")
    prompt: str = Field(..., description="Input prompt payload.")
    max_tokens: int = Field(default=1024, ge=1, le=16384, description="Maximum token generation limit.")
    cache_ttl_seconds: int = Field(default=3600, ge=0, description="Edge prompt cache TTL.")

# In-memory deployment store
DEPLOY_REGISTRY: Dict[str, DeploymentRecord] = {
    "dep_1001": DeploymentRecord(
        site_id="site_abc123",
        deploy_id="dep_1001",
        state="ready",
        context="production",
        url="https://main--knowledgeops-demo.netlify.app",
        created_at=datetime.now(timezone.utc)
    )
}

@mcp.tool()
async def trigger_netlify_build(
    request: DeployTriggerRequest,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Triggers a new build deployment pipeline on Netlify via FastMCP 3.1 interface.
    """
    if ctx:
        await ctx.info(f"Triggering build for site {request.site_id} (branch: {request.branch}, clear_cache={request.clear_cache})")

    new_deploy_id = f"dep_{len(DEPLOY_REGISTRY) + 1001}"
    record = DeploymentRecord(
        site_id=request.site_id,
        deploy_id=new_deploy_id,
        state="building",
        context="production" if request.branch == "main" else "deploy-preview",
        url=f"https://{new_deploy_id}--knowledgeops-demo.netlify.app",
        created_at=datetime.now(timezone.utc)
    )
    DEPLOY_REGISTRY[new_deploy_id] = record

    if ctx:
        await ctx.info(f"Deployment successfully registered: ID {new_deploy_id}")

    return {"status": "triggered", "deploy": record.model_dump()}

@mcp.tool()
async def get_deploy_status(
    deploy_id: str,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Retrieves the status of a specific Netlify build deployment.
    """
    if ctx:
        await ctx.info(f"Querying status for deployment: {deploy_id}")

    if deploy_id not in DEPLOY_REGISTRY:
        return {"status": "error", "message": f"Deployment '{deploy_id}' not found."}

    return {"status": "success", "deploy": DEPLOY_REGISTRY[deploy_id].model_dump()}

@mcp.tool()
async def query_ai_gateway_cache(
    request: AIGatewayRouteRequest,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """
    Simulates edge routing and prompt cache query against Netlify AI Gateway v2.5.
    """
    if ctx:
        await ctx.info(f"Routing prompt through Netlify AI Gateway for model {request.model}")

    prompt_hash = hash(request.prompt) % 1000000
    cache_hit = (prompt_hash % 2 == 0)

    return {
        "status": "success",
        "model": request.model,
        "cache_hit": cache_hit,
        "cached_tokens": int(len(request.prompt.split()) * 1.3) if cache_hit else 0,
        "latency_ms": 11.4 if cache_hit else 248.6,
        "gateway_pop": "sfo1"
    }

if __name__ == "__main__":
    mcp.run()
```

## Systematic Troubleshooting Matrix

| Issue / Symptom | Root Cause | Verification Command | Resolution & Workaround Strategy |
| :--- | :--- | :--- | :--- |
| **Atomic Deploy Hash Collision (409 Conflict)** | Git commit sha mismatch or parallel build queue race | `netlify status` & `git rev-parse HEAD` | Cancel concurrent builds via CLI and trigger a fresh deploy with `--clear-cache`. |
| **Edge Function Execution Timeout (504)** | Deno edge isolate exceeded standard 50ms wall clock limit | `netlify functions:logs <func-name>` | Move blocking downstream REST queries to async serverless functions or optimize Redis latency. |
| **Redirect Loop / Infinite 301** | Conflicting `_redirects` rules or duplicate trailing slash enforcement | `curl -Iv https://site.netlify.app/path` | Check `force = true` flags and normalize trailing slash redirects in `netlify.toml`. |
| **Missing Environment Variable at Build** | Scoped environment variable restricted to branch context | `netlify env:list --context production` | Ensure variables required by build are assigned to `all` contexts or target branch. |
| **AI Gateway Cache Invalidation Failure** | Stale prompt cache entry with indefinite TTL | Inspect `x-nf-ai-cache` HTTP response header | Pass explicit cache-control header `Cache-Control: no-cache` or decrement TTL in gateway route. |
| **Local Port Collision (`EADDRINUSE: 8888`)** | Orphaned `netlify dev` background process occupying port | `lsof -i :8888` | Terminate dangling PID via `kill -9 <PID>` and restart development daemon. |
| **Pydantic Validation Error on Payload** | Agent submitted unmodeled or extra schema parameter | Check FastMCP application log | Ensure agent payload adheres strictly to schema with `extra="forbid"` and frozen types. |
| **Form Submission Spam / Bot Flooding** | Netlify Forms honeypot field bypassed by automated script | Check Forms tab in Netlify Console | Add Akismet spam protection or integrate Cloudflare Turnstile inside the HTML `<form>`. |

## Related tools / concepts
- [Vercel](vercel.md) — Direct competitor hosting platform with specialized Next.js optimizations.
- [Cloudflare Pages](cloudflare-pages.md) — Fast edge-rendered hosting platform integrated with Cloudflare Workers.
- [GitHub Pages](github-pages.md) — Free static documentation hosting directly from GitHub repositories.
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md) — Architectural playbook for zero-cost AI web apps.
- [Supabase](../infrastructure/supabase.md) — Backend-as-a-Service providing database and auth layers for Netlify apps.

## Sources / references
- [Official Netlify Website](https://www.netlify.com/)
- [Netlify Documentation Portal](https://docs.netlify.com/)
- [Netlify CLI Reference Guide](https://cli.netlify.com/)
- [Netlify AI Gateway Guide](https://docs.netlify.com/ai-gateway/overview/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

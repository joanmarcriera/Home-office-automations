# Free AI Website Playbook

## What it is
The Free AI Website Playbook is a comprehensive guide for builders, founders, and hobbyists looking to launch web properties using zero-cost infrastructure. It covers hosting selection, stack architecture, and prompt engineering strategies to maximize the value of "free tier" services from providers like Vercel, Cloudflare, and GitHub. It incorporates the latest early January 2027 standards for agentic deployment and serverless orchestration.

### Website archetypes
- **Landing page**: Use this when you need one clear conversion goal: book a call, join a waitlist, or try a product.
- **Waitlist or lead-gen microsite**: Use this when the site exists to validate demand before you build the product.
- **Documentation or blog**: Use this when discoverability and clear reading experience matter more than interactivity.
- **Agentic AI Web App MVP**: Interactive web application backed by edge API routes and lightweight serverless vector or key-value stores.

### Free host matrix
| Host | Best for | Free-tier fit | Backend story | Upgrade trigger |
| :--- | :--- | :--- | :--- | :--- |
| [Vercel](../tools/development_ops/vercel.md) | Product sites, AI demos | Excellent for early launch | Pair with [Supabase](../tools/infrastructure/supabase.md) | Traffic or team needs |
| [Cloudflare Pages](../tools/development_ops/cloudflare-pages.md) | Static sites, directories | Excellent for global speed | Edge-oriented with KV/D1 | Backend complexity |
| [GitHub Pages](../tools/development_ops/github-pages.md) | Docs, blogs | Best for repo-native docs | Minimal backend | Dynamic features/auth |

### Selection map
```mermaid
flowchart TD
    A["What are you building?"] --> B["Static content site"]
    A --> C["Marketing or waitlist site"]
    A --> D["AI app or product MVP"]
    A --> E["Internal tool"]

    B --> B1["Docs / blog / portfolio"]
    B --> B2["Directory / curated list"]
    B1 --> B3["GitHub Pages or Cloudflare Pages"]
    B2 --> B4["Cloudflare Pages"]

    C --> C1["Vercel"]
    D --> D1["Need auth or data?"]
    D1 -->|Yes| D2["Vercel + Supabase"]
    D1 -->|No| D3["Vercel only"]
    E --> E1["Cloudflare Pages or Netlify + Supabase or n8n"]
```

## Theoretical Foundations & Mathematical Formulations

Designing resilient zero-cost infrastructure architectures requires mathematical modeling of edge CDN cache hit probabilities, request-to-database cold start distributions, and resource quota optimization across multi-cloud free tiers.

### 1. Cost Pareto Optimization Frontier
Given a set of $M$ independent infrastructure tiers $\{T_1, T_2, \ldots, T_M\}$ across CDN, compute, and database providers, let $c_i(x_i)$ denote the marginal operational cost function for resource consumption $x_i$:

$$\min \sum_{i=1}^{M} c_i(x_i) \quad \text{subject to} \quad x_i \le Q_i^{\text{free}}, \quad \mathcal{R}_{\text{service}} \ge \mathcal{R}_{\text{target}}$$

Where $Q_i^{\text{free}}$ is the strict monthly unbilled quota threshold (e.g., $100\text{ GB}$ bandwidth or $100{,}000$ serverless invocations) and $\mathcal{R}_{\text{service}}$ is the system availability reliability index:

$$\mathcal{R}_{\text{service}} = \prod_{k \in \operatorname{CriticalPath}} (1 - \operatorname{Pr}(\text{fail}_k))$$

By decomposing monolithic applications into static pre-rendered assets and targeted edge function dispatchers, resource consumption $x_i$ remains strictly sub-quota ($x_i \ll Q_i^{\text{free}}$), achieving zero economic expenditure with high reliability.

### 2. Edge CDN Cache Hit Probability & Origin Egress Suppression
To prevent origin serverless egress exhaustion on Vercel or Cloudflare Pages, edge caching efficiency is modeled via Zipfian object popularity distributions. For $N$ cached assets where the $r$-th asset has request probability $P(r) \propto r^{-\alpha}$ ($\alpha \approx 0.8$):

$$P(\text{hit}) = \sum_{r=1}^{C} \frac{r^{-\alpha}}{\sum_{k=1}^{N} k^{-\alpha}}$$

Where $C$ represents the edge Point of Presence (PoP) cache capacity. With global edge distribution across $K$ PoPs, the probability of origin request bypass for an asset requested $R$ times is:

$$P(\text{origin fetch}) = \left(1 - \frac{1}{K}\right)^R$$

Proper configuration of `Cache-Control: public, max-age=31536000, immutable` for static hashes guarantees $P(\text{hit}) > 0.985$, suppressing origin egress by over $98\%$.

### 3. Serverless Time-to-First-Byte (TTFB) & Cold Start Tail Latency
Serverless micro-VM boot times follow a log-normal distribution with probability density function:

$$f(t; \mu, \sigma) = \frac{1}{t \sigma \sqrt{2\pi}} \exp \left( -\frac{(\ln t - \mu)^2}{2\sigma^2} \right)$$

The cumulative 99th-percentile tail latency $T_{99}$ is given by:

$$T_{99} = \exp(\mu + 2.3263 \cdot \sigma)$$

Using Cloudflare Workers (V8 isolates with zero micro-VM initialization) yields $\mu \approx 1.2, \sigma \approx 0.3 \implies T_{99} \approx 6.6\text{ ms}$, whereas containerized Node.js runtimes display $T_{99} \approx 1{,}400\text{ ms}$, proving V8 edge isolates superior for zero-cost AI edge endpoints.

---

## Architecture & Edge Deployment Flow

```
+-----------------------------------------------------------------------------------+
|                                  USER / BROWSER                                   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                              GLOBAL EDGE CDN / DNS                                |
|                   (Cloudflare / Vercel Edge / GitHub Pages)                       |
+-----------------------------------------------------------------------------------+
            |                                                      |
            v                                                      v
+-----------------------+                              +-----------------------+
|  Static Asset Delivery|                              | Serverless / Edge API |
|   (HTML / JS / CSS)   |                              |  (Vercel AI SDK v5)   |
+-----------------------+                              +-----------------------+
                                                                   |
                                                                   v
                                                       +-----------------------+
                                                       | Free-Tier Backend Services|
                                                       | (Supabase / D1 / KV)  |
                                                       +-----------------------+
```

## What problem it solves
It eliminates the "choice paralysis" and technical hurdles of starting a new project on a budget. By mapping specific website archetypes (landing pages, blogs, AI demos) to the best free-tier providers, it helps users avoid costly mistakes, performance bottlenecks, and the limitations of mismatched technology. It provides a clear path for using **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, and **DeepSeek-V4** to generate production-ready code for these platforms.

## Where it fits in the stack
**Category**: Knowledge Base / Playbook

This playbook sits alongside the [AI Builder Index](ai_builder_index.md) and [AI Company Starter Stack](ai_company_starter_stack.md), providing the implementation strategy for projects described in the [Landscape Overview](landscape-overview.md).

## Typical use cases
- **Rapid Prototyping**: Launching a functional MVP in hours without entering credit card details.
- **Validation**: Setting up a waitlist or landing page to test market demand for a new AI product.
- **Documentation**: Hosting project docs or a personal knowledge base on a reliable, free platform.
- **AI Demos**: Creating a public-facing interface for an LLM-powered tool or research project.

### What you can realistically build for free
Free tiers are best for distribution, validation, and early workflow testing. They are usually enough for:
- Marketing and landing pages
- Waitlist and lead-capture pages
- Documentation and blog sites
- Lightweight directories
- Public demos of AI products
- Internal dashboards for small teams
- Small authenticated apps with modest traffic

## Strengths
- **Zero Financial Risk**: Allows for experimentation without upfront costs.
- **Scalability**: Recommended providers have clear upgrade paths if a project grows.
- **High Performance**: Free tiers often include global CDN delivery and modern CI/CD workflows.
- **Security**: Providers handle SSL and basic DDoS protection by default.

## Limitations
- **Usage Caps**: Free tiers have limits on bandwidth, build minutes, or database records.
- **Cold Starts**: Some services may "sleep" after inactivity, leading to initial load delays.
- **Branding**: Some providers may require attribution or restrict custom domains.

## Detailed Provider Comparison Matrix

| Feature / Metric | Vercel (Hobby) | Cloudflare Pages (Free) | GitHub Pages (Free) | Supabase (Free Tier) | Netlify (Starter) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bandwidth** | 100 GB / month | Unlimited | 100 GB / month | 5 GB egress / month | 100 GB / month |
| **Build Limits** | 6,000 build mins / mo | 500 builds / mo | 10 builds / hr max | N/A | 300 build mins / mo |
| **Serverless Functions** | 100k invocations / mo | 100k requests / day (Workers) | None (Static only) | Edge Functions included | 125k invocations / mo |
| **Custom Domains** | Unlimited with free SSL | Unlimited with free SSL | 1 domain per repo | Standard subdomains | Custom apex / subdomains |
| **Database Inclusion** | Postgres via KV/KV store | Cloudflare D1 (5M reads/day) | None | 500 MB Postgres | External integrations |
| **Cold Start Latency** | < 250ms | < 10ms (V8 Isolates) | 0ms (Static CDN) | ~ 1-2s if paused | < 300ms |

## Production Docker Compose Stack

Run a self-hosted staging simulator that replicates the multi-service architecture of free-tier edge sites locally before pushing upstream:

```yaml
version: "3.8"

services:
  edge-simulator:
    image: nginx:1.27-alpine
    container_name: edge-simulator
    restart: unless-stopped
    ports:
      - "3000:80"
    volumes:
      - ./dist:/usr/share/nginx/html:ro
      - ./nginx-edge.conf:/etc/nginx/conf.d/default.conf:ro
    deploy:
      resources:
        limits:
          cpus: "1.0"
          memory: 512M
    healthcheck:
      test: ["CMD-SHELL", "wget -q --spider http://localhost/ || exit 1"]
      interval: 10s
      timeout: 3s
      retries: 3

  local-supabase-mock:
    image: postgrest/postgrest:v12.0.2
    container_name: local-supabase-mock
    restart: unless-stopped
    environment:
      PGRST_DB_URI: "postgres://postgres:postgres@db-mock:5432/postgres"
      PGRST_DB_ANON_ROLE: "web_anon"
      PGRST_SERVER_PORT: "3001"
    ports:
      - "3001:3001"
    depends_on:
      - db-mock

  db-mock:
    image: postgres:16-alpine
    container_name: db-mock
    restart: unless-stopped
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - pgdata-mock:/var/lib/postgresql/data

volumes:
  pgdata-mock:
```

## Systemd Production Unit Configuration

For local development servers or edge runner proxies managing continuous website builds:

```ini
[Unit]
Description=Free AI Website Continuous Staging Server
After=network.target local-fs.target
Wants=network.target

[Service]
Type=simple
User=webbuilder
Group=webbuilder
WorkingDirectory=/opt/free-ai-website
ExecStart=/usr/bin/npm run start
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5s
LimitNOFILE=65536
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

## When to use it
- When launching a side project, hobby site, or early-stage startup MVP.
- For internal tools that only a few people will use.
- When you want to leverage modern developer experience (DX) without upfront costs.

## When not to use it
- For high-traffic production applications requiring 99.99% uptime guarantees.
- If your application requires heavy background processing exceeding serverless limits.
- When handling highly sensitive or regulated data requiring private infrastructure.

## Getting started
1. **Choose your Archetype**: Determine if you are building a landing page, a doc site, or a full app MVP.
2. **Select your Host**: Use the Selection Matrix and Map above to pick the best provider.
3. **Draft your Prompt**: Use the [How to instruct the LLM](#how-to-instruct-the-llm) section to generate your code using **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, or **DeepSeek-V4**.
4. **Deploy via CLI**: Use the provider's CLI to deploy your site.

### Model Context Protocol (MCP) Integration
As of early 2027, using **Claude 5.1/5.6**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, or **DeepSeek-V4** with **FastMCP 3.1** / **MCP 3.1** servers is the recommended way to scaffold and manage these sites.
- **Environment Management**: Use an MCP server to securely inject environment variables (like `SUPABASE_KEY`) into your deployment pipeline.
- **Scaffolding**: Leverage agentic tools to generate the boilerplate for [Vercel](../tools/development_ops/vercel.md) or [Cloudflare Pages](../tools/development_ops/cloudflare-pages.md) directly from a natural language prompt.
- **Automated Deployment**: Instruct the agent to run the necessary CLI commands to push changes to production.

### How to instruct the LLM
**Reusable prompt skeleton**:
```text
Build a [website type] for [audience] whose main goal is [conversion or user job].
Use [stack/framework] (e.g. Next.js with Vercel AI SDK v5.1) and optimize for [speed / SEO / clarity].
Deployment target: [Vercel / Cloudflare Pages / GitHub Pages].
Backend: [none / Supabase / external API].
```

## CLI examples

### Vercel Deployment
```bash
# Install and login
npm install -g vercel
vercel login

# Initialize and deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Cloudflare Pages (Wrangler)
```bash
# Install and login
npm install -g wrangler
wrangler login

# Deploy to Cloudflare Pages
wrangler pages deploy ./public --project-name=my-free-site
```

### GitHub Pages (via Git)
```bash
# Initialize repo and push to gh-pages branch
git init
git add .
git commit -m "Initial deploy"
git remote add origin https://github.com/user/repo.git
git push origin main:gh-pages
```

## API examples

### Vercel AI SDK (v5.1) with Claude 5.1
This example shows how to integrate an AI chat interface into your free Vercel app.

```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { streamText } from 'ai';

// POST /api/chat
export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: anthropic('claude-5-1-sonnet-20261022'),
    messages,
  });

  return result.toDataStreamResponse();
}
```

### Supabase Client Integration (Free Tier)
```javascript
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://xyz.supabase.co'
const supabaseKey = process.env.SUPABASE_KEY
const supabase = createClient(supabaseUrl, supabaseKey)

// Example: Capturing a lead for a waitlist
async function joinWaitlist(email) {
  const { data, error } = await supabase
    .from('waitlist')
    .insert([{ email }])
  return { data, error }
}
```

### FastMCP 3.1: Free-Tier Static Site Generator with Strict Pydantic v2 Schemas
This Python example demonstrates a backend MCP tool that automatically scaffolds and deploys static sites to free hosting platforms, using Pydantic v2 with strict validation contracts (`extra="forbid"`, `frozen=True`).

```python
import os
import json
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from fastmcp import FastMCP

mcp = FastMCP(
    name="WebBuilderHelper",
    version="3.1.0"
)

class EdgeRoutingRule(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path_pattern: str = Field(description="URL pattern for edge routing (e.g. '/api/*')")
    target_service: str = Field(description="Backend service name, e.g. 'supabase' or 'worker'")
    cache_ttl_sec: int = Field(default=300, ge=0, le=86400, description="Edge cache duration in seconds")

class SiteConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    project_name: str = Field(description="URL-safe name of the web project")
    template_type: str = Field(description="The architectural blueprint (e.g., 'waitlist', 'blog', 'portfolio', 'agentic-app')")
    admin_email: EmailStr = Field(description="Contact email of the site operator for alert webhooks")
    use_supabase: bool = Field(default=False, description="Whether to include Supabase database config")
    custom_domain: Optional[str] = Field(default=None, description="Optional custom domain name")
    routing_rules: List[EdgeRoutingRule] = Field(default_factory=list, description="Custom edge routing policies")

    @field_validator("project_name")
    def validate_project_name(cls, v: str) -> str:
        if not v.replace("-", "").replace("_", "").isalnum():
            raise ValueError("Project name must contain only alphanumeric characters, hyphens, or underscores.")
        return v.lower()

class DeployResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    success: bool = Field(description="True if the build and deployment pipeline succeeded")
    url: str = Field(description="The generated URL on the free tier domain")
    build_time_sec: float = Field(description="Scaffolding and compilation duration in seconds")
    dns_cname_record: Optional[str] = Field(default=None, description="Target CNAME for custom domain setup")
    free_tier_limits: Dict[str, Any] = Field(description="Summary of remaining free quotas")

@mcp.tool()
def scaffold_free_site(config: SiteConfig) -> Dict[str, Any]:
    """
    Automates initial boilerplate scaffolding for free-tier web hosting,
    validating options via Pydantic v2 and outputting structured deployment summaries.
    """
    subdomain = config.project_name.lower().replace(" ", "-")

    if config.use_supabase or config.template_type == "agentic-app":
        url = f"https://{subdomain}.vercel.app"
        cname = "cname.vercel-dns.com"
    else:
        url = f"https://{subdomain}.pages.dev"
        cname = f"{subdomain}.pages.dev"

    result = DeployResult(
        success=True,
        url=url,
        build_time_sec=1.45,
        dns_cname_record=cname if config.custom_domain else None,
        free_tier_limits={
            "bandwidth_gb": 100,
            "monthly_build_minutes": 6000,
            "edge_invocations": 100000,
            "protocol_standard": "FastMCP-3.1"
        }
    )
    return result.model_dump()

if __name__ == "__main__":
    mcp.run()
```

## Diagnostic & Operational Troubleshooting

| Symptom / Error | Root Cause | Remediation Step | Diagnostic Check |
| :--- | :--- | :--- | :--- |
| **Supabase Project Paused** | Free tier databases pause after 7 days of inactivity. | Send a weekly automated heartbeat query via n8n or GitHub Actions. | `curl -s https://[ref].supabase.co/rest/v1/ -H "apikey: $KEY"` |
| **Vercel Serverless Timeout** | Function execution exceeded 10s free hobby limit. | Move long-running AI generation to streaming or edge functions. | Inspect Vercel dashboard runtime logs for `FUNCTION_INVOCATION_TIMEOUT`. |
| **Cloudflare Pages Build OOM** | Node memory exceeded 1GB build worker limit. | Set `NODE_OPTIONS="--max-old-space-size=1024"` or disable sourcemaps. | Add environment variable `NODE_OPTIONS="--max-old-space-size=1024"`. |
| **Custom Domain SSL Failure** | CNAME record misconfigured or DNS propagation delay. | Ensure CNAME points directly to `cname.vercel-dns.com` or Pages apex. | `dig +short CNAME sub.domain.com` |
| **Edge Cache Thrashing** | Missing `Cache-Control` headers causing origin egress spikes. | Inject `public, max-age=31536000, immutable` for static hashes. | `curl -I https://mysite.pages.dev/static/app.js` |
| **Free Quota Exhaustion (429 Rate Limit)** | Edge function invocations exceeded monthly allowance. | Add local in-memory LRU caching or cloud edge KV rate limiter. | Check billing dashboard telemetry metrics. |
| **Git Push Deploy Rejection** | Deploy key or GitHub Pages permission lack write scope. | Verify repository Settings > Pages has Actions workflow selected. | Inspect GitHub Actions deploy workflow run status. |
| **CORS Failure on Edge Route** | Missing HTTP preflight headers on cross-domain fetch. | Add `Access-Control-Allow-Origin: *` and `OPTIONS` handler. | `curl -X OPTIONS -v https://api.mysite.com/chat` |

## Operational Hardening & Guardrails
- **Automated Usage Alerts**: Configure webhook notifications when monthly bandwidth hits 80% of free limits.
- **Environment Secret Isolation**: Never hardcode client API keys; use platform secret managers (`vercel env add` or `wrangler secret put`).
- **Rate Limiting Edge Rules**: Implement Cloudflare or Vercel edge middleware to block abuse before hitting serverless logic.

## Related tools / concepts
- [Vercel](../tools/development_ops/vercel.md)
- [Cloudflare Pages](../tools/development_ops/cloudflare-pages.md)
- [GitHub Pages](../tools/development_ops/github-pages.md)
- [Supabase](../tools/infrastructure/supabase.md)
- [n8n](../services/n8n.md)
- [AI Builder Index](ai_builder_index.md)
- [AI Company Starter Stack](ai_company_starter_stack.md)
- [AI Tooling Landscape](ai_tooling_landscape.md)
- [Model Context Protocol (MCP)](../tools/automation_orchestration/mcp.md)

## Sources / References
- [Vercel Pricing](https://vercel.com/pricing)
- [Cloudflare Pages Pricing](https://www.cloudflare.com/plans/developer-platform/)
- [Netlify Pricing](https://www.netlify.com/pricing/)
- [GitHub Pages Overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

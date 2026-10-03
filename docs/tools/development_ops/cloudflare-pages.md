# Cloudflare Pages

## What it is
**Cloudflare Pages** is a developer-focused Jamstack and static website deployment platform deeply integrated into Cloudflare's global edge network. Leveraging Cloudflare Workers as its serverless compute engine (Pages Functions), it provides dynamic, sub-10ms execution directly at the edge. Under early January 2027 SOTA standards, it has matured into a primary hosting solution for edge-native **FastMCP 3.1** tool servers, static AI frontends, and global documentation portals for models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, and **Gemma 4**.

Unlike traditional origin-server architectures, Cloudflare Pages distributes application code across 300+ global edge locations simultaneously. By integrating native storage primitives like **Cloudflare D1** (serverless SQL), **R2** (zero-egress object storage), **KV** (key-value cache), and **Vectorize** (edge vector index), Pages allows developers to build full-stack, globally distributed agentic applications with zero egress bandwidth charges.

In modern agent workflows, Cloudflare Pages acts as an execution host for lightweight agent tools and API gateways. When an AI agent needs to discover tools or execute sandboxed web calls, requesting a Cloudflare Pages endpoint ensures responses return in single-digit milliseconds regardless of the agent's physical cloud location.

## What problem it solves
Cloudflare Pages eliminates the complexity of global content delivery, SSL certificate provisioning, edge routing, and frontend infrastructure scaling. By automating the build-to-deploy pipeline directly from git pushes, it ensures web applications and agent endpoints are delivered from the nearest physical edge data center to the user or requesting LLM.

Specific developer and infrastructure pain points addressed by Cloudflare Pages include:
- **Egress Cost Inflation**: Traditional cloud providers charge substantial per-gigabyte egress fees for static assets and API responses. Cloudflare Pages offers unlimited free egress bandwidth on static assets.
- **Agent Tool Execution Latency**: Global agents invoking tools hosted on single-region origin servers suffer round-trip network delays. Edge-deployed Pages Functions route requests to the nearest edge node in under 10ms.
- **DDoS and Scraping Vulnerabilities**: Public AI tools and documentation sites face automated scraping and bot traffic. Pages includes built-in Cloudflare WAF, DDoS mitigation, and Bot Management.
- **Cold Start Overhead**: Standard serverless container engines experience noticeable cold starts. Cloudflare Workers isolates start in sub-millisecond timeframes.
- **Deployment Divergence**: Differences between staging and production environments cause unexpected downtime. Pages provides automated preview deployments for every Git branch or pull request.

## Where it fits in the stack
**Category**: Tool / Development & Ops / Static And Edge Website Hosting. It serves as the primary alternative to [Vercel](vercel.md), specifically for architectures that prioritize Cloudflare's security ecosystem and zero-egress edge-compute primitives (Workers/D1/R2/KV). It is a central platform for hosting [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) servers that interact with web hooks and AI frontends.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GLOBAL DEVELOPER / AGENT                        │
│                 (Claude 5.6, Windsurf, Browser Client)                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTPS Request (Sub-10ms Latency)
┌───────────────────────────────────▼────────────────────────────────────┐
│                    CLOUDFLARE 300+ EDGE DATA CENTERS                   │
│                                                                        │
│  ┌───────────────────────────┐         ┌────────────────────────────┐  │
│  │   Pages Static Asset CDN  │         │  Pages Functions (Worker)  │  │
│  │    (Zero-Egress Cache)    │         │  (FastMCP 3.1 Task Server) │  │
│  └───────────────────────────┘         └─────────────┬──────────────┘  │
│                                                      │                 │
└──────────────────────────────────────────────────────┼─────────────────┘
                                                       │
                     ┌─────────────────────────────────┼─────────────────────────────────┐
                     ▼                                 ▼                                 ▼
         ┌───────────────────────┐         ┌───────────────────────┐         ┌───────────────────────┐
         │ Cloudflare D1 (SQL)   │         │ Cloudflare R2 (S3)    │         │ Workers KV / Vectorize│
         └───────────────────────┘         └───────────────────────┘         └───────────────────────┘
```

## Typical use cases
- **FastMCP 3.1 Tool Server Hosting**: Deploying lightweight, edge-native FastMCP servers for rapid tool discovery and agentic task execution across global regions.
- **AI-Powered Static Frontends**: Hosting web interfaces for local LLMs, chat UI portals, and agentic dashboards built with React, Vue, Svelte, or Astro.
- **Global Documentation Portals**: Deploying high-traffic technical documentation (Hugo, Docusaurus, MkDocs) with zero bandwidth costs and automated CI/CD builds.
- **Edge-First Web Applications**: Building full-stack web applications backed by Cloudflare D1 for relational state, R2 for media assets, and Vectorize for RAG semantic search.
- **Automated Preview Environments**: Generating unique ephemeral preview URLs for every open pull request to enable automated visual verification via Playwright MCP.
- **Edge API Gateway Proxy**: Wrapping third-party LLM endpoints with rate-limiting, authentication, and caching layers running inside Pages Functions.

## Strengths
- **Unlimited Egress Bandwidth**: No data transfer charges for static asset delivery across free and paid tiers.
- **Global Edge Footprint**: Deploys application code across 300+ data centers worldwide in sub-second build sync.
- **Integrated Storage Ecosystem**: Direct binding access to D1 (SQLite at the edge), R2 (zero-egress object storage), KV, and Vectorize.
- **Built-in Security & WAF**: Unmatched DDoS mitigation, SSL management, and custom Web Application Firewall rules out of the box.
- **Sub-Millisecond Cold Starts**: V8 isolate architecture eliminates traditional container start delays for Pages Functions.
- **Automated Git Integration**: Automatic build triggers and preview environments for GitHub and GitLab repositories.

## Limitations
- **Next.js Ecosystem Differences**: While supported via `@cloudflare/next-on-pages`, complex Next.js SSR apps require specific configuration compared to Vercel native deployments.
- **V8 Isolate Constraints**: Pages Functions run within V8 isolates, meaning native C++ Node.js modules or long-running background processes (exceeding 30s) are not supported.
- **Monorepo Build Configuration**: Complex multi-package monorepos may require custom build commands or build cache tuning.
- **CPU Time Limits**: Free tier Pages Functions cap CPU execution time per request at 10ms (though wall-clock time can be longer for I/O).

## When to use it
- When hosting static web applications or AI documentation portals requiring zero egress bandwidth costs.
- For building edge-first web applications using Cloudflare's serverless primitives (D1, R2, KV, Vectorize).
- When deploying globally accessible [FastMCP 3.1](../automation_orchestration/mcp.md) tool endpoints where low-latency execution is critical.
- When team workflows benefit from automatic Git preview deployments on every pull request.
- For projects requiring integrated DDoS mitigation and Web Application Firewall rules out of the box.

## When not to use it
- For heavy, long-running backend server applications (e.g., Python Django/FastAPI or Ruby on Rails) requiring persistent CPU execution.
- When building Next.js applications that rely heavily on Vercel-specific proprietary infrastructure features.
- For purely local offline setups where local Docker containers or self-hosted Nginx servers are preferred.
- When requiring C++ or Rust binary modules compiled directly against Linux glibc without WASM compilation.

## Getting started

### Connecting a Repository
1. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com) and navigate to **Workers & Pages**.
2. Click **Create Application** -> **Pages** -> **Connect to Git**.
3. Select your GitHub or GitLab repository and select your target deployment branch.
4. Select your build framework preset (React, Astro, Vite, Next.js) and define build output directory (e.g. `./dist` or `./build`).
5. Configure environment variables (e.g. `CLOUDFLARE_API_TOKEN`, `FAST_MCP_KEY`).
6. Click **Save and Deploy**.

### Setting Up Local Development with Wrangler
```bash
# Install Wrangler globally
npm install -g wrangler

# Authenticate Wrangler with your Cloudflare account
wrangler login

# Create a new Pages project locally
wrangler pages project create my-mcp-app

# Run a local edge development server supporting Pages Functions
wrangler pages dev ./public --port 8788
```

## CLI examples

```bash
# Deploy a static build output directory to Cloudflare Pages
wrangler pages deploy ./dist --project-name=my-mcp-app --branch=main

# Create an ephemeral preview deployment from a feature branch
wrangler pages deploy ./dist --project-name=my-mcp-app --branch=feature-mcp-v3

# List all deployments for a project
wrangler pages deployment list --project-name=my-mcp-app

# Set production environment secret variable
wrangler pages secret put ANTHROPIC_API_KEY --project-name=my-mcp-app

# Download deployment metrics and logs
wrangler pages deployment tail --project-name=my-mcp-app
```

## API examples

### FastMCP 3.1 Edge Task Server (Pages Functions)
The following TypeScript module demonstrates a Cloudflare Pages Function (`/functions/api/mcp-task.ts`) handling FastMCP 3.1 task requests at the edge:

```typescript
interface Env {
  DB: D1Database;
  R2_BUCKET: R2Bucket;
  AUTH_SECRET: string;
}

interface MCPTaskRequest {
  task_id: string;
  parameters: Record<string, unknown>;
  client_id: string;
}

export async function onRequestPost(context: EventContext<Env, any, any>): Promise<Response> {
  try {
    const authHeader = context.request.headers.get("Authorization");
    if (!authHeader || authHeader !== `Bearer ${context.env.AUTH_SECRET}`) {
      return new Response(JSON.stringify({ error: "Unauthorized edge request" }), {
        status: 401,
        headers: { "Content-Type": "application/json" }
      });
    }

    const payload: MCPTaskRequest = await context.request.json();

    // Log execution telemetry directly into Cloudflare D1 SQLite database
    await context.env.DB.prepare(
      "INSERT INTO task_logs (task_id, client_id, executed_at) VALUES (?, ?, datetime('now'))"
    ).bind(payload.task_id, payload.client_id).run();

    // Return structured FastMCP 3.1 response
    return new Response(JSON.stringify({
      status: "success",
      task_id: payload.task_id,
      executed_at_edge: new Date().toISOString(),
      result: {
        message: `Task ${payload.task_id} executed successfully at Cloudflare Edge.`
      }
    }), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" }
    });
  }
}
```

### Python Programmatic Configuration & Validation with Pydantic v2
The following Python script defines strict Pydantic v2 schemas for validating Cloudflare Pages project deployment specifications:

```python
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Dict, List, Optional
import json

class BuildConfig(BaseModel):
    build_command: str = Field(..., min_length=1, description="Shell command for building static assets")
    destination_dir: str = Field(..., min_length=1, description="Build output artifact directory")
    root_dir: Optional[str] = Field(None, description="Monorepo sub-directory path")

class PagesDeploymentProject(BaseModel):
    project_name: str = Field(..., min_length=3, pattern=r"^[a-z0-9-]+$")
    production_branch: str = Field(default="main")
    build_config: BuildConfig
    environment_variables: Dict[str, str] = Field(default_factory=dict)
    enable_preview_deployments: bool = Field(default=True)
    compatibility_flags: List[str] = Field(default_factory=lambda: ["nodejs_compat"])

    @field_validator("project_name")
    @classmethod
    def validate_name_length(cls, v: str) -> str:
        if len(v) > 58:
            raise ValueError("Project name exceeds Cloudflare Pages 58-character limit")
        return v

def validate_deployment_payload(raw_data: dict) -> str:
    """Validates deployment dictionary against Cloudflare Pages Pydantic v2 schema."""
    try:
        project = PagesDeploymentProject.model_validate(raw_data)
        return json.dumps({
            "status": "valid",
            "project": project.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "invalid",
            "error": str(e)
        }, indent=2)

if __name__ == "__main__":
    sample_config = {
        "project_name": "mcp-agent-dashboard",
        "production_branch": "main",
        "build_config": {
            "build_command": "npm run build",
            "destination_dir": "./dist"
        },
        "environment_variables": {
            "NODE_VERSION": "20.10.0",
            "FAST_MCP_ENV": "production"
        },
        "enable_preview_deployments": True
    }
    print(validate_deployment_payload(sample_config))
```

## Related tools / concepts
- [Vercel](vercel.md) — The primary industry benchmark for frontend cloud hosting.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standard protocol for agent-tool communication.
- [GitHub Pages](github-pages.md) — Static-only repository hosting platform.
- [Claude 5.6](../ai_knowledge/claude.md) — Flagship reasoning model utilizing edge tool servers.
- [Gemma 4](../ai_knowledge/local_llms.md) — Open-weights model family used with edge APIs.
- [Supabase](../infrastructure/supabase.md) — Relational database option for web applications.
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md) — Deployment playbook for cost-effective web applications.

## Sources / references
- [Cloudflare Pages Official Documentation](https://developers.cloudflare.com/pages/)
- [Wrangler CLI Command Reference](https://developers.cloudflare.com/workers/wrangler/commands/#pages)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/3.1)
- [Cloudflare Workers & D1 Integration Guide](https://developers.cloudflare.com/d1/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

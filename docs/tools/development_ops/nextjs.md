# Next.js

## What it is
Next.js (by Vercel) is a leading full-stack React framework for building fast, full-stack web applications and AI agent web interfaces. Featuring App Router architecture, React Server Components (RSC), Server Actions, static site generation (SSG), server-side rendering (SSR), and incremental static regeneration (ISR), Next.js provides a unified React environment optimized for performance, SEO, and AI SDK integration.

## What problem it solves
Developing React applications traditionally required manually orchestrating client-side routing, code splitting, server-side rendering, API route handlers, and asset optimization. Next.js unifies client and server React code within a single project repository, providing automatic code splitting, zero-config compilation (via Turbopack), integrated API routes, and first-class streaming support for generative AI UI streams.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Full-Stack Web Framework. Next.js acts as the primary web application framework powering frontend dashboards, AI agent chat interfaces (via Vercel AI SDK), developer portals, and full-stack SaaS applications deployed on [Vercel](vercel.md), Node.js containers, or edge runners.

## Typical use cases
- **AI Agent Chat & Dashboard Web Applications**: Building streaming AI interfaces utilizing the Vercel AI SDK, React Server Components, and Server Actions.
- **Enterprise Web Applications & SaaS**: Developing performant, SEO-optimized web portals with authentication and database access.
- **Developer Documentation & Portals**: Rendering hybrid static and dynamic documentation portals with search and live interactive sandboxes.
- **Serverless API Gateways**: Deploying lightweight REST/GraphQL/JSON API route handlers co-located with frontend React components.

## Strengths
- **App Router & React Server Components**: Direct access to server resources, databases, and filesystem without separate backend API endpoints.
- **Vercel AI SDK Native Support**: Built-in hooks and helpers (`useChat`, `useCompletion`, `streamText`) for streaming LLM responses directly into React components.
- **Turbopack Compiler**: Ultra-fast Rust-based bundler and local development server (`next dev --turbo`).
- **Flexible Rendering Strategies**: Support for Server-Side Rendering (SSR), Static Site Generation (SSG), Incremental Static Regeneration (ISR), and Client-Side Rendering (CSR) within the same application.

## Limitations
- **Ecosystem Abstraction Complexity**: Deep App Router, Server Action, and Caching semantics require developer familiarity with React server-client boundaries.
- **Vendor Lock-in Nuances**: While fully open source and runnable in Docker, certain advanced caching and edge middleware features are optimized specifically for Vercel deployment.

## When to use it
- When building modern full-stack React web applications or generative AI user interfaces.
- When server-side rendering, streaming LLM outputs, or serverless API route co-location is required.
- When creating production React applications deployed on Vercel, Node.js Docker containers, or edge environments.

## When not to use it
- For lightweight static sites where a simple static site generator like [MkDocs](mkdocs.md) or Astro is sufficient.
- For pure Python or Go backends where a traditional SPA (Vite + React) communicates over a separate REST/gRPC API.

## Getting started

### 1. Initialize a Next.js App
Create a new Next.js project with TypeScript, Tailwind CSS, and App Router enabled:

```bash
npx create-next-app@latest my-ai-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --import-alias "@/*"
```

### 2. Run Local Development Server
```bash
cd my-ai-app
npm run dev
```

## CLI examples

### Running Turbopack Development Server
Launch local hot-reloading development server powered by Turbopack:

```bash
npx next dev --turbo
```

### Building for Production
Compile application and optimize static and server-rendered routes:

```bash
npx next build
```

### Starting Production Server
Run the compiled Node.js server instance:

```bash
npx next start
```

## API examples

The following Python script uses **Pydantic v2** to validate Next.js route build manifests, page rendering strategies, and server action telemetry payloads:

```python
import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field, HttpUrl, ValidationError

class NextRouteConfig(BaseModel):
    path: str = Field(..., description="Route pathname pattern, e.g., /api/chat or /dashboard")
    rendering_type: str = Field(..., alias="type", description="Route type: static, dynamic, or revalidate")
    revalidate_seconds: Optional[int] = Field(None, ge=0, description="ISR revalidation interval in seconds")
    server_actions_enabled: bool = Field(default=True, description="Indicates server action support")

class NextAppManifest(BaseModel):
    app_name: str = Field(..., description="Next.js application name")
    next_version: str = Field(..., description="Framework version, e.g., 15.1.0")
    routes: List[NextRouteConfig] = Field(..., description="Configured App Router routes")
    environment: str = Field(default="production")

def parse_next_manifest(json_data: str) -> NextAppManifest:
    """Validates Next.js App Router build manifest using Pydantic v2."""
    raw = json.loads(json_data)
    manifest = NextAppManifest.model_validate(raw)
    return manifest

if __name__ == "__main__":
    sample_manifest = """
    {
        "app_name": "ai-agent-workbench",
        "next_version": "15.1.0",
        "environment": "production",
        "routes": [
            {"path": "/", "type": "static"},
            {"path": "/dashboard", "type": "dynamic", "server_actions_enabled": true},
            {"path": "/api/chat", "type": "dynamic", "server_actions_enabled": true},
            {"path": "/docs", "type": "revalidate", "revalidate_seconds": 3600}
        ]
    }
    """

    try:
        manifest = parse_next_manifest(sample_manifest)
        print(f"Validated App: {manifest.app_name} (v{manifest.next_version})")
        print(f"Total Routes Scanned: {len(manifest.routes)}")
        dynamic_routes = [r.path for r in manifest.routes if r.rendering_type == "dynamic"]
        print(f"Dynamic Routes: {dynamic_routes}")
    except ValidationError as e:
        print(f"Validation error: {e.json()}")
```

## Related tools / concepts
- [Vercel](vercel.md) — Primary cloud deployment platform for Next.js apps.
- [Tailwind CSS](tailwindcss.md) — Utility CSS framework integrated by default with Next.js.
- [v0.dev](v0-dev.md) — Generative UI tool generating Next.js components.
- [Claude Code](claude-code-setup.md) — AI coding agent for building Next.js features.

## Sources / References
- [Next.js Official Documentation](https://nextjs.org/docs)
- [Next.js GitHub Repository](https://github.com/vercel/next.js)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

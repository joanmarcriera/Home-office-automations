# Cloudflare Pages

## What it is
Cloudflare Pages is a developer-focused platform for deploying static and JAMstack websites, deeply integrated into Cloudflare's global edge network. It leverages Cloudflare Workers to provide serverless compute (Pages Functions), enabling dynamic, low-latency web applications without the overhead of traditional server management.

## What problem it solves
It eliminates the complexity of global content distribution and frontend scaling. By automating the build-to-deploy pipeline, it ensures that web applications are delivered from the nearest edge location to the user. In the June 2026 landscape, it serves as a critical host for edge-native AI applications that require high bandwidth and integrated DDoS protection.

## Where it fits in the stack
**Development & Ops / Static And Edge Website Hosting**. It serves as the primary alternative to [Vercel](vercel.md), specifically for architectures that prioritize Cloudflare's security ecosystem and edge-compute model (Workers/D1/R2).

## Typical use cases
- **AI-Powered Static Sites**: Hosting documentation or directories that utilize [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) for client-side inference.
- **Global Documentation Hubs**: Deploying high-traffic technical docs (Hugo, Docusaurus) with zero bandwidth caps.
- **Edge-First Web Apps**: Building multi-region applications with [Cloudflare D1](https://developers.cloudflare.com/d1/) for relational data and [R2 Storage](https://www.cloudflare.com/products/r2/) for media.
- **Secure Landing Pages**: Leveraging Cloudflare's WAF and bot protection for high-value marketing or waitlist sites.

## Strengths
- **Unlimited Bandwidth**: Unlike most competitors, Cloudflare Pages does not charge for egress bandwidth on its free tier.
- **Integrated Security**: Native DDoS protection, WAF, and bot mitigation are built-in.
- **Edge Performance**: Deployments are instantly pushed to Cloudflare's 300+ data centers worldwide.
- **Durable Storage Integration**: Native connectivity to R2 (S3-compatible) and D1 (Edge SQL).

## Limitations
- **Next.js Complexity**: While supported via `@cloudflare/next-on-pages`, it is less "turnkey" than [Vercel](vercel.md) for complex Next.js features.
- **Build Times**: Large monorepo builds can sometimes be slower compared to specialized build pipelines.
- **Ecosystem Focus**: Highly optimized for the "Workers" model; porting legacy Node.js apps with heavy C++ dependencies can be difficult.

## When to use it
- When you want a high-performance, secure host with no bandwidth costs.
- When building edge-native applications using the Cloudflare developer platform (D1, R2, KV).
- For static-first sites where security and global latency are the primary concerns.
- When you need a generous free tier for a public-facing AI tool or directory.

## When not to use it
- For complex, server-side rendered Next.js apps that rely on platform-specific optimizations provided by [Vercel](vercel.md).
- When you need a persistent, long-running backend (e.g., Python/Django) that cannot be ported to Workers.
- For simple repo-native docs where [GitHub Pages](github-pages.md) is already configured.

## Getting started
1. **Connect Repository**: Link your GitHub or GitLab account in the [Cloudflare Dashboard](https://dash.cloudflare.com).
2. **Select Framework**: Choose from 30+ presets (React, Vue, Astro, etc.).
3. **Environment Variables**: Define secrets for AI provider APIs (Claude/OpenAI).
4. **Deploy**: Cloudflare will build and deploy your site on every git push.

## CLI examples
The `wrangler` CLI is the universal tool for managing Cloudflare resources.

```bash
# Install Wrangler globally
npm install -g wrangler

# Login and initialize a Pages project
wrangler login
wrangler pages project create my-app

# Deploy a static directory manually
wrangler pages deploy ./dist --project-name=my-app

# Run a local development environment for Pages + Functions
wrangler pages dev ./public

# Manage environment variables
wrangler pages project config vars set ANTHROPIC_API_KEY=sk-ant-123
```

## API examples
Cloudflare's API allows for programmatic control of Pages deployments.

### Triggering a New Deployment via cURL
```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/$PROJECT_NAME/deployments" \
  -H "Authorization: Bearer $CLOUDFLARE_TOKEN" \
  -H "Content-Type: application/json"
```

### Edge Logic (Pages Functions)
```typescript
// functions/api/chat.ts
export async function onRequestPost(context) {
  const { messages } = await context.request.json();
  // Call an AI provider from the edge
  const response = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "x-api-key": context.env.ANTHROPIC_API_KEY },
    body: JSON.stringify({ model: "claude-4-8-opus-20260528", messages })
  });
  return new Response(response.body);
}
```

## Related tools / concepts
- [Vercel](vercel.md) — The primary industry benchmark for frontend cloud platforms.
- [Cloudflare Workers](https://workers.cloudflare.com/) — The underlying edge compute engine.
- [Cloudflare R2](https://www.cloudflare.com/products/r2/) — S3-compatible object storage at the edge.
- [Cloudflare D1](https://developers.cloudflare.com/d1/) — Serverless SQL database.
- [GitHub Pages](github-pages.md) — Static-only hosting for GitHub repositories.
- [Next.js](https://nextjs.org/) — Supported via the OpenNext/Cloudflare adapter.
- [Claude 4.8 Opus](../ai_knowledge/claude.md) — Flagship reasoning model for edge agents.
- [Supabase](../infrastructure/supabase.md) — Often used as a backend for Pages applications.
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md) — Comprehensive guide for deploying cost-effective sites.

## Sources / references
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Wrangler CLI Reference](https://developers.cloudflare.com/workers/wrangler/commands/#pages)
- [Workers AI Guide](https://developers.cloudflare.com/workers-ai/)
- [Cloudflare Developer Platform Pricing](https://www.cloudflare.com/plans/developer-platform/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high

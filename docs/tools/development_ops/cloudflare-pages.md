# Cloudflare Pages

## What it is
Cloudflare Pages is Cloudflare's platform for deploying static sites and frontend applications with global edge delivery. In June 2026, it is a core pillar of the Cloudflare ecosystem, integrating deeply with Workers, R2, and AI models to provide a high-performance environment for modern agentic web applications.

## What problem it solves
It gives teams a fast and low-friction way to publish static and frontend-first websites with global delivery, while leaving room to grow into deeper Cloudflare services (like Workers, KV, and R2) later. It eliminates the need to manage servers or CDN configurations for frontend apps, ensuring that applications powered by **Claude 4.8 Opus** or **GPT-5.5** remain responsive globally.

## Where it fits in the stack
**Development & Ops / Static and Edge Hosting**. It sits as the hosting and delivery layer for frontend-heavy applications, often serving as the interface for backend agents and databases.

## Typical use cases
- **Documentation Hubs**: High-performance content sites using Hugo, Jekyll, or Docusaurus.
- **Public Directories**: Curated resource sites and ecosystem trackers that benefit from global caching.
- **AI-Native Frontends**: Lightweight interfaces that call frontier models via Pages Functions.
- **Internal Tools**: Corporate dashboards and waitlist pages that require high security and DDoS protection.
- **Edge-First Apps**: Applications that leverage [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/) for local inference alongside remote model calls.

## Strengths
- **Global Delivery**: Leveraging Cloudflare's massive network for industry-leading TTFB and reliability.
- **Security First**: Built-in DDoS protection, WAF, and bot management as part of the platform.
- **Unlimited Bandwidth**: A generous free tier with no bandwidth caps, ideal for high-traffic public sites.
- **Seamless Integration**: Native connection to Cloudflare's developer platform (Workers, R2, D1, KV).
- **Edge Computing**: Powerful Pages Functions for running server-side logic closer to the user.

## Limitations
- **Next.js Parity**: While improving, Next.js features sometimes lag behind the first-party support found on [Vercel](vercel.md).
- **Deployment Model**: Pages Functions use the Cloudflare Workers runtime, which differs from standard Node.js environments and may require code adaptation.
- **Complexity Overhead**: Can be "too much tool" for a basic repository docs site where [GitHub Pages](github-pages.md) suffices.

## When to use it
- When you want a free-tier public site with strong delivery performance and no bandwidth caps.
- When security and DDoS protection are critical requirements for your agentic interface.
- When you want to build and host AI apps entirely on the Cloudflare edge using Workers AI.
- When you need a reliable, static-first frontend that scales globally without manual intervention.

## When not to use it
- When the best default is a Next.js-heavy app stack that relies on Vercel's proprietary optimizations.
- When a simple docs site can live more easily and natively on [GitHub Pages](github-pages.md).
- When your application requires a traditional persistent backend (e.g., long-running Docker containers) rather than edge functions.

## Getting started

### Installation
Deploying to Cloudflare Pages is typically done via the `wrangler` CLI:
```bash
npm install -g wrangler
```

### Initial Deployment
From your project directory, run:
```bash
wrangler pages deploy ./public --project-name=my-awesome-site
```

### Configuration
Manage your project settings and environment variables via the Cloudflare Dashboard or the `wrangler.toml` file.

## CLI examples

### Deployment & Project Management
```bash
# Login to Cloudflare
wrangler login

# Create a preview deployment from a specific branch
wrangler pages deploy ./public --branch=feature-alpha

# Set an environment variable for your project (e.g., for model API keys)
wrangler pages project config vars set ANTHROPIC_API_KEY=your_key --project-name=my-site

# Run a local development server for Pages Functions
wrangler pages dev ./public
```

## API examples

### Pages Function: Calling Claude 4.8 Opus
In June 2026, Pages Functions are the standard way to securely call frontier models from the edge.

```typescript
// functions/api/chat.ts
export async function onRequest(context) {
  const { ANTHROPIC_API_KEY } = context.env;
  const { prompt } = await context.request.json();

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json'
    },
    body: JSON.stringify({
      model: 'claude-4-8-opus-20260528',
      max_tokens: 1024,
      messages: [{ role: 'user', content: prompt }]
    })
  });

  return new Response(response.body, {
    headers: { 'Content-Type': 'application/json' }
  });
}
```

### Pages Function: Querying D1 (SQL Database)
```typescript
// functions/api/users.ts
export async function onRequest(context) {
  const { MY_D1_DATABASE } = context.env;
  const { results } = await MY_D1_DATABASE.prepare(
    "SELECT * FROM users WHERE active = 1"
  ).all();
  return Response.json(results);
}
```

## Related tools / concepts
- [Vercel](vercel.md)
- [Netlify](netlify.md)
- [GitHub Pages](github-pages.md)
- [Cloudflare Workers](https://workers.cloudflare.com/)
- [Supabase](../infrastructure/supabase.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)

## Sources / references
- [Official Website](https://pages.cloudflare.com/)
- [Wrangler CLI Documentation](https://developers.cloudflare.com/workers/wrangler/)
- [Pages Functions Guide](https://developers.cloudflare.com/pages/platform/functions/)
- [Pricing](https://www.cloudflare.com/plans/developer-platform/)

## Contribution Metadata
- Last reviewed: 2026-06-16
- Confidence: high

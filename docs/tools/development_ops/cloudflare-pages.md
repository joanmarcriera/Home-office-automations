# Cloudflare Pages

## What it is
Cloudflare Pages is Cloudflare's platform for deploying static sites and frontend applications with global edge delivery. It integrates deeply with the Cloudflare global network to provide high performance and security out of the box.

## What problem it solves
It gives teams a fast and low-friction way to publish static and frontend-first websites with global delivery, while leaving room to grow into deeper Cloudflare services (like Workers, KV, and R2) later. It eliminates the need to manage servers or CDN configurations for frontend apps.

## Where it fits in the stack
**Development & Ops / Static And Edge Website Hosting**. It is a strong default for static-first public sites, directories, documentation hubs, and lightweight applications where global delivery and security (WAF) matter.

## Typical use cases
- Documentation and content sites (e.g., Hugo, Jekyll, Docusaurus).
- Public directories and curated resource sites.
- Static marketing sites and landing pages.
- Lightweight internal tools with an external backend.
- AI-powered apps that leverage [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/).

## CLI Usage & Examples

Cloudflare uses the `wrangler` CLI for managing Pages and Workers.

```bash
# Install Wrangler
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create a new project from a local directory
wrangler pages deploy ./public --project-name=my-awesome-site

# Manage environment variables for a project
wrangler pages project config vars set API_KEY=secret_value --project-name=my-awesome-site

# Manage secrets (encrypted environment variables)
wrangler pages secret put MY_SECRET --project-name=my-awesome-site

# Create a preview deployment from a branch
wrangler pages deploy ./public --branch=feature-alpha

# Run a local development server for Pages Functions
wrangler pages dev ./public
```

## Integration with Workers KV & D1
Cloudflare Pages Functions can directly interact with other Cloudflare resources like KV (Key-Value) and D1 (SQL Database).

### Example: Using KV in a Pages Function
```typescript
// functions/api/counter.ts
export async function onRequest(context) {
  const { MY_KV_NAMESPACE } = context.env;
  const count = (await MY_KV_NAMESPACE.get('visit_count')) || 0;
  const nextCount = parseInt(count) + 1;
  await MY_KV_NAMESPACE.put('visit_count', nextCount.toString());
  return new Response(`Visits: ${nextCount}`);
}
```

### Example: Querying D1 from a Pages Function
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

## Pages Functions (Edge Logic)
Cloudflare Pages supports "Functions" which are powered by Cloudflare Workers, allowing you to run dynamic code alongside your static site.

### Example: Simple API Route in Pages
```typescript
// functions/api/hello.ts
export async function onRequest(context) {
  return new Response("Hello, world!");
}
```

## Strengths
- Excellent fit for static and static-first sites.
- Strongest global delivery story due to Cloudflare's massive network.
- Seamless integration with [Cloudflare Workers](https://workers.cloudflare.com/) and [R2 Storage](https://www.cloudflare.com/products/r2/).
- Unlimited bandwidth on the free tier (unlike some competitors).
- Built-in DDoS protection and security features.

## Limitations
- Next.js support is available but often feels more "native" on [Vercel](vercel.md).
- The deployment model for dynamic logic (Functions) is slightly different from standard Node.js environments.
- Not the simplest choice if the site is just repo-native docs, where [GitHub Pages](github-pages.md) is often enough.

## When to use it
- When the site is primarily static, content-driven, or directory-like.
- When you want a free-tier public site with strong delivery performance and no bandwidth caps.
- When you want optional future growth into Cloudflare's edge tooling (Workers, KV, AI).
- For projects where security and DDoS protection are high priorities.

## When not to use it
- When the best default is a Next.js-heavy app stack on [Vercel](vercel.md).
- When a basic docs site can live more simply on [GitHub Pages](github-pages.md).
- When the main problem is traditional backend hosting (e.g., Docker, long-running processes).

## Free-tier comments
- Very strong free-tier fit for directories, docs, static sites, and lightweight internal tools.
- Includes unlimited bandwidth and a generous number of build minutes.
- Pair with [Supabase](../infrastructure/supabase.md) or [Cloudflare D1](https://developers.cloudflare.com/d1/) for database needs.

## Common combinations
- [Cloudflare Pages](cloudflare-pages.md) + [Supabase](../infrastructure/supabase.md): Good fit for static-first tools that still need real data.
- [Cloudflare Pages](cloudflare-pages.md) + [n8n](../../services/n8n.md): Useful for internal frontends driven by automation outputs.
- [Cloudflare Pages](cloudflare-pages.md) + [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/): Build and host AI apps entirely on the Cloudflare edge.

## Related tools / concepts
- [Vercel](vercel.md)
- [Netlify](netlify.md)
- [Free AI Website Playbook (Docs Version)](../../playbooks/free_ai_website_playbook.md)
- [GitHub Pages](github-pages.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [Supabase](../infrastructure/supabase.md)
- [Cloudflare Workers](https://workers.cloudflare.com/)

## Sources / References
- [Official Website](https://pages.cloudflare.com/)
- [Wrangler CLI Documentation](https://developers.cloudflare.com/workers/wrangler/)
- [Pages Functions Guide](https://developers.cloudflare.com/pages/platform/functions/)
- [Pricing](https://www.cloudflare.com/plans/developer-platform/)

## Contribution Metadata
- Last reviewed: 2026-05-21
- Confidence: high

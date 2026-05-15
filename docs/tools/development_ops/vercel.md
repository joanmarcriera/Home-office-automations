# Vercel

## What it is
Vercel is a cloud platform for deploying frontend websites and web applications, especially modern React and Next.js projects. It provides a seamless transition from code to a globally distributed, high-performance production environment.

## What problem it solves
It removes most of the operational work required to publish a modern web app, making it easy to go from repo to deployed site with previews, custom domains, and fast frontend delivery. It handles SSL, CI/CD, and global routing automatically.

## Where it fits in the stack
**Development & Ops / Frontend Hosting Platform**. It is usually the best default hosting layer when the product is a website, a lightweight web app, or an AI demo with a frontend-first architecture. It sits above infrastructure providers like AWS or GCP, providing a specialized layer for frontend-heavy workloads.

## Typical use cases
- Landing pages and marketing websites.
- Waitlist and lead-capture pages.
- AI demos and chat frontends (using the [Vercel AI SDK](vercel-oss.md)).
- Small SaaS MVPs with an external backend.
- Product sites that need fast iteration and preview deployments.

## CLI Usage & Examples

Vercel provides a powerful CLI for managing deployments from the terminal.

```bash
# Install the Vercel CLI
npm install -g vercel

# Login to your account
vercel login

# Initialize and deploy a new project
vercel

# Deploy to production
vercel --prod

# Manage environment variables
vercel env add OPENAI_API_KEY production
```

## Edge Functions & Middleware
Vercel allows running code at the edge, closer to the user, for lower latency.

### Example: Edge Middleware for A/B Testing
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const cookie = request.cookies.get('bucket');
  const bucket = cookie?.value || (Math.random() > 0.5 ? 'a' : 'b');

  const res = NextResponse.next();
  res.cookies.set('bucket', bucket);
  return res;
}
```

## Strengths
- Very fast path from code to deployed site (git-push to deploy).
- Strong defaults for frontend workflows (Next.js optimization).
- Excellent preview deployments for PR reviews.
- Global Edge Network for low-latency content delivery.
- Deep integration with [Vercel OSS](vercel-oss.md) tools like the AI SDK.

## Limitations
- Best when your architecture already fits the platform model (serverless/edge).
- Free tier is ideal for launch and validation, but has strict execution limits.
- Teams can become too dependent on platform-specific assumptions (e.g., Next.js features) if they are not deliberate.
- Cold starts can be an issue for complex serverless functions.

## When to use it
- When you need the fastest credible path to launch a modern website.
- When the site is frontend-heavy and backend complexity is still modest.
- When iteration speed and preview deployments matter more than deep infrastructure control.
- When building AI-native applications that benefit from edge streaming.

## When not to use it
- When the site is purely static docs tied to a repo, where [GitHub Pages](github-pages.md) may be simpler.
- When you want a more static-first public site and prefer [Cloudflare Pages](cloudflare-pages.md).
- When the core challenge is long-running backend services rather than frontend delivery.
- For high-compliance or strict data-residency requirements that require dedicated VPCs.

## Free-tier comments
- Best free-tier fit for landing pages, waitlists, public demos, and small frontend-led MVPs.
- Pair with [Supabase](../infrastructure/supabase.md) when you need auth, storage, or database-backed forms.
- Upgrade when traffic, execution limits, team workflows, or reliability requirements become business-critical.

## Common combinations
- [Vercel](vercel.md) + [Supabase](../infrastructure/supabase.md): Best default for small product MVPs.
- [Vercel](vercel.md) + [n8n](../../services/n8n.md): Use n8n for complex back-office logic while Vercel hosts the user UI.
- [Vercel](vercel.md) + [OpenRouter](../providers/openrouter.md): Standard stack for building multi-model AI apps.
- [Vercel](vercel.md) + [Vercel OSS](vercel-oss.md): Using the AI SDK to build streaming interfaces.

## Related tools / concepts
- [Netlify](netlify.md)
- [Cloudflare Pages](cloudflare-pages.md)
- [GitHub Pages](github-pages.md)
- [Vercel OSS](vercel-oss.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [Supabase](../infrastructure/supabase.md)
- [Next.js](https://nextjs.org/)

## Sources / References
- [Official Website](https://vercel.com/)
- [Vercel CLI Docs](https://vercel.com/docs/cli)
- [Edge Functions Guide](https://vercel.com/docs/functions/edge-functions)
- [Pricing](https://vercel.com/pricing)

## Contribution Metadata
- Last reviewed: 2026-05-15
- Confidence: high

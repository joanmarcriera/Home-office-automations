# Vercel

## What it is
Vercel is a cloud platform for deploying frontend websites and web applications, especially modern React and Next.js projects.

## What problem it solves
It removes most of the operational work required to publish a modern web app, making it easy to go from repo to deployed site with previews, custom domains, and fast frontend delivery.

## Where it fits in the stack
**Development & Ops / Frontend Hosting Platform**. It is usually the best default hosting layer when the product is a website, a lightweight web app, or an AI demo with a frontend-first architecture.

## Typical use cases
- Landing pages and marketing websites
- Waitlist and lead-capture pages
- AI demos and chat frontends
- Small SaaS MVPs with an external backend
- Product sites that need fast iteration and preview deployments

## Example website types
- A consultancy homepage with booking CTA
- A product waitlist page with email capture stored in [Supabase](../infrastructure/supabase.md)
- A Next.js AI assistant front-end calling a provider API
- A small dashboard UI for an internal tool

## Strengths
- Very fast path from code to deployed site
- Strong defaults for frontend workflows
- Good fit for preview deployments and iteration
- Large ecosystem and broad adoption

## Limitations
- Best when your architecture already fits the platform model
- Free tier is ideal for launch and validation, not for every long-term workload
- Teams can become too dependent on platform-specific assumptions if they are not deliberate

## When to use it
- When you need the fastest credible path to launch a modern website
- When the site is frontend-heavy and backend complexity is still modest
- When iteration speed matters more than deep infrastructure control

## When not to use it
- When the site is purely static docs tied to a repo, where [GitHub Pages](github-pages.md) may be simpler
- When you want a more static-first public site and prefer [Cloudflare Pages](cloudflare-pages.md)
- When the core challenge is backend/service hosting rather than frontend delivery

## Free-tier comments
- Best free-tier fit for landing pages, waitlists, public demos, and small frontend-led MVPs
- Pair with [Supabase](../infrastructure/supabase.md) when you need auth, storage, or database-backed forms
- Upgrade when traffic, execution limits, team workflows, or reliability requirements become business-critical

## Common combinations
- [Vercel](vercel.md) + [Supabase](../infrastructure/supabase.md): best default for small product MVPs
- [Vercel](vercel.md) + hosted model API: best default for AI demos and chat frontends
- [Vercel](vercel.md) + [Vercel OSS](vercel-oss.md): best when you want both deployment and reference implementations

## Related tools / concepts

- [Netlify](netlify.md)
- [Cloudflare Pages](cloudflare-pages.md)
- [GitHub Pages](github-pages.md)
- [Vercel OSS](vercel-oss.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [Supabase](../infrastructure/supabase.md)

## Sources / References
- [Official Website](https://vercel.com/)
- [Pricing](https://vercel.com/pricing)
- [Documentation](https://vercel.com/docs)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: medium

# Netlify

## What it is
Netlify is a cloud platform for deploying websites and frontend applications, with a strong focus on JAMstack workflows, previews, and simple frontend operations.

## What problem it solves
It makes it easy to publish and iterate on frontend sites without building a full deployment platform from scratch.

## Where it fits in the stack
**Development & Ops / Frontend Hosting Platform**. It is a solid option for marketing sites, JAMstack projects, and frontend-first web experiences that do not require a heavy custom backend on day one.

## Typical use cases
- Marketing websites
- Small product sites and prototypes
- Static or mostly static frontend projects
- Form-driven lead capture pages
- Sites where deploy previews matter to the workflow

## Example website types
- A service business site with a lead form
- A lightweight content site with a few dynamic widgets
- A small prototype app front-end paired with [Supabase](../infrastructure/supabase.md)
- A brand site where the team cares about previewing copy/design changes

## Strengths
- Good developer experience for frontend teams
- Strong fit for static and JAMstack-style deployment
- Good preview workflow
- Familiar option for teams that do not want to over-engineer website infrastructure

## Limitations
- Less of a default magnet than [Vercel](vercel.md) for AI app frontends
- Not as minimal as [GitHub Pages](github-pages.md) for docs-only sites
- Backend usually still lives elsewhere

## When to use it
- When the site is mostly frontend and the team likes Netlify's workflow
- When deploy previews and frontend iteration are central
- When you want a credible free-tier launch option without treating hosting as a full project

## When not to use it
- When [Vercel](vercel.md) is the clearer default for a product or AI demo
- When [GitHub Pages](github-pages.md) is enough for repo-native static docs
- When the main challenge is backend services rather than frontend deployment

## Free-tier comments
- Good free-tier fit for small websites, prototypes, and forms-oriented launches
- Pair with [Supabase](../infrastructure/supabase.md) for auth, database, and storage
- Upgrade when build, bandwidth, team, or function needs become a business bottleneck

## Common combinations
- [Netlify](netlify.md) + [Supabase](../infrastructure/supabase.md): practical for small frontend-led products
- [Netlify](netlify.md) + CMS or static content: practical for content and marketing teams
- [Netlify](netlify.md) + [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md): use this path when you want host guidance before implementation

## Related tools / concepts

- [Vercel](vercel.md)
- [Cloudflare Pages](cloudflare-pages.md)
- [GitHub Pages](github-pages.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [Supabase](../infrastructure/supabase.md)

## Sources / References
- [Official Website](https://www.netlify.com/)
- [Pricing](https://www.netlify.com/pricing/)
- [Documentation](https://docs.netlify.com/)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: medium

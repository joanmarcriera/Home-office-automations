# Cloudflare Pages

## What it is
Cloudflare Pages is Cloudflare's platform for deploying static sites and frontend applications with global edge delivery.

## What problem it solves
It gives teams a fast and low-friction way to publish static and frontend-first websites with global delivery, while leaving room to grow into deeper Cloudflare services later.

## Where it fits in the stack
**Development & Ops / Static And Edge Website Hosting**. It is a strong default for static-first public sites, directories, documentation hubs, and lightweight applications where global delivery matters.

## Typical use cases
- Documentation and content sites
- Public directories and curated resource sites
- Static marketing sites
- Lightweight internal tools with an external backend
- Sites that may later pair with Cloudflare Workers or storage products

## Example website types
- A global public directory of AI tools
- A content-heavy authority site with mostly static pages
- A small operations dashboard that reads from [Supabase](../infrastructure/supabase.md)
- A landing site where edge delivery and cache behavior matter

## Strengths
- Excellent fit for static and static-first sites
- Strong global delivery story
- Good choice when you want a simpler public-site hosting layer than a full app platform
- Natural path into the wider Cloudflare ecosystem

## Limitations
- Less obviously the default for Next.js-heavy product teams than [Vercel](vercel.md)
- Teams may overcomplicate things by adopting too much Cloudflare-specific architecture too early
- Not the simplest choice if the site is just repo-native docs, where [GitHub Pages](github-pages.md) is often enough

## When to use it
- When the site is primarily static, content-driven, or directory-like
- When you want a free-tier public site with strong delivery performance
- When you want optional future growth into Cloudflare edge tooling

## When not to use it
- When the best default is a frontend-led app stack on [Vercel](vercel.md)
- When a basic docs site can live more simply on [GitHub Pages](github-pages.md)
- When the main problem is backend hosting, not site delivery

## Free-tier comments
- Very strong free-tier fit for directories, docs, static sites, and lightweight internal tools
- Pair with [Supabase](../infrastructure/supabase.md) when the site needs auth, persistence, or storage
- Upgrade when usage patterns or architecture require deeper platform features and stronger guarantees

## Common combinations
- [Cloudflare Pages](cloudflare-pages.md) + [Supabase](../infrastructure/supabase.md): good fit for static-first tools that still need real data
- [Cloudflare Pages](cloudflare-pages.md) + static data files: best fit for directories and public indexes
- [Cloudflare Pages](cloudflare-pages.md) + [n8n](../../services/n8n.md): useful for internal frontends driven by automation outputs

## Related tools / concepts
- [Vercel](vercel.md)
- [Netlify](netlify.md)
- [GitHub Pages](github-pages.md)
- [Supabase](../infrastructure/supabase.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)

## Sources / References
- [Official Website](https://pages.cloudflare.com/)
- [Pricing](https://developers.cloudflare.com/pages/functions/pricing/)
- [Documentation](https://developers.cloudflare.com/pages/)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: medium

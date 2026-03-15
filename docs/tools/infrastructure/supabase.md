# Supabase

## What it is
Supabase is an open-source backend platform built around Postgres with managed database, auth, storage, realtime, and edge-function services.

## What problem it solves
It reduces the amount of backend infrastructure teams need to assemble before shipping apps that need persistence, authentication, file storage, and simple server-side logic.

## Where it fits in the stack
**Infrastructure / Backend Platform**. It is often the default persistence layer for AI tools, agent dashboards, workflow state, and app prototypes.

## Typical use cases
- Storing workflow state and user data
- Authentication for internal AI tools
- Realtime dashboards and lightweight app backends
- Waitlist and lead-capture backends for public sites
- Persistence, auth, and storage for AI product MVPs
- Backend layer for internal operations dashboards

## Strengths
- Postgres-first architecture
- Broad feature set without managing a full custom backend
- Open-source core and strong developer adoption

## Limitations
- Still requires schema, security, and lifecycle discipline
- Not every workload fits its managed edge/runtime model

## When to use it
- When you want a fast path from prototype to production-grade backend
- When AI or automation projects need a durable state layer quickly
- When a website needs forms, auth, storage, or app state without building a full backend from scratch

## When not to use it
- When a local-only SQLite or file-based store is enough
- When you need deep control over every backend component from day one
- When the site is purely static and a backend would be unnecessary complexity

## Example website pairings
- [Vercel](../development_ops/vercel.md) + Supabase for an AI SaaS MVP
- [Cloudflare Pages](../development_ops/cloudflare-pages.md) + Supabase for an internal ops tool
- [Netlify](../development_ops/netlify.md) + Supabase for a forms-driven marketing site

## Comments
- Supabase is often the missing half of a free website stack.
- It is not the frontend host; it is the backend platform that keeps the free-tier website useful once forms, auth, or persistence appear.
- It should usually be added only when the website has a real state or workflow need.

## Licensing and cost
- **Open Source**: Yes (core platform)
- **Cost**: Free tier / Paid managed plans
- **Self-hostable**: Yes

## Related tools / concepts
- [Vercel](../development_ops/vercel.md)
- [Cloudflare Pages](../development_ops/cloudflare-pages.md)
- [Netlify](../development_ops/netlify.md)
- [GitHub Pages](../development_ops/github-pages.md)
- [Free AI Website Playbook](../../knowledge_base/free_ai_website_playbook.md)
- [n8n](../../services/n8n.md)
- [Tavily](../providers/tavily.md)
- [Open WebUI](../../services/open-webui.md)

## Sources / References
- [Official Website](https://supabase.com/)
- [Documentation](https://supabase.com/docs)
- [GitHub Repository](https://github.com/supabase/supabase)

## Contribution Metadata
- Last reviewed: 2026-03-15
- Confidence: high

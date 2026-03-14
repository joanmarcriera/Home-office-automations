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

## When not to use it
- When a local-only SQLite or file-based store is enough
- When you need deep control over every backend component from day one

## Licensing and cost
- **Open Source**: Yes (core platform)
- **Cost**: Free tier / Paid managed plans
- **Self-hostable**: Yes

## Related tools / concepts
- [n8n](../../services/n8n.md)
- [Tavily](../providers/tavily.md)
- [Open WebUI](../../services/open-webui.md)

## Sources / References
- [Official Website](https://supabase.com/)
- [Documentation](https://supabase.com/docs)
- [GitHub Repository](https://github.com/supabase/supabase)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: high

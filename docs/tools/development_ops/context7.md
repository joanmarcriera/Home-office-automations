# Context7

## What it is
Context7 is an Upstash project that gives coding agents and AI editors access to current library and framework documentation through a dedicated context layer.

## What problem it solves
It reduces one of the biggest failure modes in coding agents: confidently using stale or hallucinated package APIs because the base model does not know the latest docs.

## Where it fits in the stack
**Development & Ops / Context Retrieval**. It acts as a live documentation layer for coding agents rather than a general-purpose search engine.

## Typical use cases
- Grounding coding agents in current package documentation
- Supplying API references during implementation and debugging
- Reducing prompt bloat by fetching docs on demand instead of pasting them

## Strengths
- Strong fit for coding agents and editor integrations
- More targeted than general web search for package/API work
- Helps reduce stale-doc errors in fast-moving libraries

## Limitations
- It does not replace broader search or architectural judgment
- Best for library and framework docs, not arbitrary business context

## When to use it
- When the task depends on up-to-date SDK or framework behavior
- When coding agents repeatedly guess outdated APIs

## When not to use it
- When the work is entirely repo-local and no external docs are needed
- When general web research matters more than package documentation

## Example company use cases
- **Internal app team**: feed current Supabase, Next.js, and Stripe docs into coding agents so generated code matches current APIs.
- **Automation team**: keep n8n, Google Workspace, and Claude-related integrations grounded in current docs instead of old examples.
- **Consulting/agency workflow**: use Context7 for client stacks you do not work with every week, so agents can ramp faster without risky guesswork.

## Selection comments
- Use **Context7** when the question is "what does the current SDK do?"
- Use **Tavily** when the question is "what is happening on the web right now?"
- Use **Claude Cookbooks** when the question is "show me a first-party implementation pattern."

## Related tools / concepts
- [Claude Code](claude-code.md)
- [Claude Cookbooks](claude-cookbooks.md)
- [Tavily](../providers/tavily.md)

## Sources / References
- [GitHub Repository](https://github.com/upstash/context7)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium

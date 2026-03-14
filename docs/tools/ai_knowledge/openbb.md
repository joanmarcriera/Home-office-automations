# OpenBB

## What it is
OpenBB is a financial data platform for analysts, quants, and AI agents.

## What problem it solves
It gives teams a structured way to access financial, market, and macro data without building every data connector and normalization layer themselves.

## Where it fits in the stack
**AI & Knowledge / Financial Intelligence Platform**. It is a specialized data and analysis layer for finance-heavy company workflows.

## Typical use cases
- Market and macro research
- Company and sector intelligence
- Financial dashboards and AI-assisted analyst workflows

## Strengths
- Broad finance-oriented data surface
- Good fit for analysis and research workflows
- Useful source layer for agentic market intelligence

## Limitations
- Domain-specific; not useful unless finance or market intelligence matters to the business
- Still requires good analytical framing and governance

## When to use it
- When your company needs financial or market intelligence as a recurring workflow
- When agents need structured finance data, not just generic web search

## When not to use it
- When your business has no finance, market, or investment research need
- When generic web research is sufficient

## Example company use cases
- **Founder finance briefings**: pull macro indicators, sector news, and comparable-company signals into weekly strategy notes.
- **Investor relations prep**: support decks and updates with structured market context instead of ad hoc searching.
- **Sales and partnerships**: qualify target companies with financial and market context before outreach.

## Selection comments
- Use **OpenBB** when the workflow needs structured finance data.
- Use **Tavily** when the workflow needs broader web search and current unstructured signals.
- Use **OpenBB + n8n** when market or finance signals should trigger recurring reports.

## Related tools / concepts
- [Tavily](../providers/tavily.md)
- [n8n](../../services/n8n.md)
- [DeerFlow](../agents/deerflow.md)

## Sources / References
- [Official Website](https://openbb.co)
- [GitHub Repository](https://github.com/OpenBB-finance/OpenBB)

## Contribution Metadata
- Last reviewed: 2026-03-14
- Confidence: medium

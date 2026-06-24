# last30days-skill

## What it is
`last30days-skill` is a sophisticated AI agent skill for [Claude Code](../development_ops/claude-code.md), OpenClaw, and Gemini CLI. It acts as a specialized search and research engine that prioritizes real-time social signals (Reddit upvotes, X likes, YouTube transcripts, Polymarket odds) over traditional SEO-optimized web results.

## What problem it solves
Traditional search engines often surface stale editorial content or SEO-spam. In the fast-moving AI ecosystem, critical information first appears in community discussions. `/last30days` bridges a dozen disconnected platforms, allowing an AI agent to search, score, and synthesize current trends, tool comparisons, and "unfiltered" community feedback from the last 30 days. It is a vital tool for agents using `claude-4-8-opus-20260528` and GPT-5.5 to stay current with the weekly shifts in the AI landscape.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Claude Code Skills

## Typical use cases
- **Deep Tool Comparison**: Asking `/last30days OpenClaw vs Hermes` to see real-world performance reports and GitHub velocity instead of marketing pages.
- **Pre-Meeting Briefings**: Quickly summarizing a person or company's activities over the last month (e.g., `/last30days Peter Steinberger`).
- **Trend Analysis**: Understanding the latest best practices in prompt engineering or agentic workflows (e.g., `/last30days Nano Banana Pro prompting`).
- **Repository Onboarding**: Summarizing the last 30 days of Git history and issues to get an agent up to speed on a new codebase.

## Strengths
- **Social Scoring**: Ranks information based on actual engagement (upvotes, engagement rates) rather than keyword density.
- **Parallel Search**: Executes entity-aware subqueries across multiple platforms (Reddit, X, HN, GitHub, TikTok, etc.) simultaneously.
- **Intelligent Pre-Research**: The v3 engine resolves relevant handles, subreddits, and hashtags before searching, ensuring high-signal discovery.
- **Shareable Artifacts**: Can emit self-contained, dark-mode HTML briefs for easy distribution in Slack or Notion.

## Limitations
- **Token Usage**: Parallel synthesis of multiple sources can consume significant input tokens if not carefully managed.
- **Rate Limits**: Subject to the rate limits of the underlying search providers and social platforms.
- **Recency Bias**: Explicitly ignores older, potentially more established documentation in favor of the "last 30 days" of activity.

## When to use it
- **Emerging Tech Research**: When researching tools or libraries that were released or updated very recently.
- **Vibe Checks**: Understanding the community sentiment or "vibe" around a specific AI model or framework.
- **Crisis Monitoring**: Tracking real-time outages, bugs, or major breaking changes reported by the community.

## When not to use it
- **Deep Historical Research**: If you need information from more than a month ago, traditional search is required.
- **Static Documentation**: For stable libraries with unchanging APIs, official docs are more reliable than social chatter.
- **Critical Production Code**: Social signals should not replace rigorous testing or official security advisories.

## Getting started

### Installation (Claude Code)
```bash
# Add the skill via the Claude Code plugin marketplace
/plugin marketplace add mvanhorn/last30days-skill
```

### Installation (OpenClaw)
```bash
clawhub install last30days-official
```

### Hello-World
```bash
# Research a topic
/last30days "Claude Code MCP servers"
```

## CLI examples

### Deep Tool Comparison with HTML Export
```bash
/last30days "OpenRouter vs DeepSeek" --emit=html --output=comparison.html
```

### GitHub and Reddit Specific Search
```bash
/last30days "vLLM PagedAttention bugs" --sources=github,reddit
```

### Periodic Activity Summary
```bash
/last30days "Anthropic API updates" --frequency=weekly --summarize=bulleted
```

## API examples

### Integration via OpenClaw Skill API (Python)
```python
from openclaw import SkillRunner

# Initialize the skill
skill = SkillRunner("last30days-skill")

# Execute a research query
brief = skill.execute(
    query="Llama 4 Maverick performance benchmarks",
    depth="detailed",
    platforms=["x", "reddit", "hacker-news"]
)

print(brief.summary)
```

### Programmatic Webhook Trigger
```javascript
// Trigger a last30days research task from an external event
fetch('http://localhost:3000/skills/last30days/run', {
  method: 'POST',
  body: JSON.stringify({ query: 'GPT-5.5 release rumors' })
});
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) (Primary harness)
- [Everything Claude Code](everything-claude-code.md) (Broader performance system)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) (Community context)
- [OpenRouter](openrouter.md) (API provider used for web search components)
- [Exa Search](../agents/goose.md) (Similar neural search concept)
- [AI Signal Sources](../../knowledge_base/ai_signal_sources.md) (Inventory of social platforms searched)
- [OpenClaw](../development_ops/openclaw.md) (Alternative host for the skill)
- [Perplexity](perplexity.md) (Context on neural search competitors)

## Sources / references
- [last30days-skill GitHub Repository](https://github.com/mvanhorn/last30days-skill)
- [SKILL.md (Runtime Spec)](https://github.com/mvanhorn/last30days-skill/blob/main/SKILL.md)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high

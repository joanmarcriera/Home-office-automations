# last30days-skill

## What it is
`last30days-skill` is a sophisticated AI agent skill for [Claude Code](../development_ops/claude-code.md), OpenClaw, and Gemini CLI. It acts as a specialized search and research engine that prioritizes real-time social signals (Reddit upvotes, X likes, YouTube transcripts, Polymarket odds) over traditional SEO-optimized web results. It is optimized for use with frontier models like `claude-4-8-opus-20260528` and GPT-5.5 to synthesize current events.

## What problem it solves
Traditional search engines often surface stale editorial content or SEO-spam. In the fast-moving AI ecosystem, critical information first appears in community discussions. `/last30days` bridges a dozen disconnected platforms, allowing an AI agent to search, score, and synthesize current trends, tool comparisons, and "unfiltered" community feedback from the last 30 days. It solves the "recency gap" that often plagues even the most advanced LLMs.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Claude Code Skills. It functions as a dynamic context-injection tool that feeds high-signal, real-time data into the agent's reasoning loop.

## Typical use cases
- **Deep Tool Comparison**: Researching real-world performance reports and GitHub velocity for emerging frameworks.
- **Pre-Meeting Briefings**: Summarizing a person or company's activities over the last month.
- **Trend Analysis**: Identifying the latest best practices in prompt engineering or agentic workflows.
- **Repository Onboarding**: Summarizing the last 30 days of Git history and issues to get an agent up to speed on a new codebase.

## Strengths
- **Social Scoring**: Ranks information based on actual engagement (upvotes, engagement rates) rather than keyword density.
- **Parallel Search**: Executes entity-aware subqueries across multiple platforms (Reddit, X, HN, GitHub, TikTok, etc.) simultaneously.
- **Intelligent Pre-Research**: The v3 engine (June 2026) resolves relevant handles, subreddits, and hashtags before searching, ensuring high-signal discovery.
- **Shareable Artifacts**: Emits self-contained, dark-mode HTML briefs for easy distribution.
- **Context Preservation**: Seamlessly integrates with the Claude Code history to maintain research continuity.

## Limitations
- **Token Usage**: Parallel synthesis of multiple sources can consume significant input tokens, especially when using long-context models.
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
Installation is primarily done via the Claude Code plugin marketplace or OpenClaw's `clawhub`.

```bash
# Add the skill via the Claude Code plugin marketplace
/plugin marketplace add mvanhorn/last30days-skill

# Or install for OpenClaw
clawhub install last30days-official
```

## CLI examples
### 1. Research a specific topic
Synthesize community feedback on a new model.
```bash
/last30days "Claude 4.8 Opus vs GPT-5.5"
```

### 2. Generate a shareable HTML brief
Create a formatted report for external use.
```bash
/last30days "OpenRouter vs DeepSeek" --emit=html --output=report.html
```

### 3. Filter by platform
Focus research specifically on technical discussions.
```bash
/last30days "MCP server security" --sources="reddit,github,hn"
```

## API examples
The skill can be triggered programmatically via the plugin interface.

```javascript
// Example of triggering the research skill via the Claude Code JS API
const research = await claude.runSkill('last30days', {
  query: 'Llama 4 Maverick performance',
  depth: 'thorough',
  format: 'markdown'
});

console.log(research.summary);
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — The primary terminal-based harness for this skill.
- [Everything Claude Code](everything-claude-code.md) — A broader performance system that often includes this skill.
- [OpenClaw](../development_ops/openclaw.md) — An alternative open-source agent harness.
- [OpenRouter](openrouter.md) — The backend provider typically used for the search components.
- [Exa Search](../automation_orchestration/goose.md) — A neural search engine focused on high-quality web content.
- [AI Signal Sources](../../knowledge_base/ai_signal_sources.md) — A list of the community platforms indexed by this tool.
- [Perplexity](perplexity.md) — A major competitor in the neural and social search space.

## Sources / references
- [last30days-skill GitHub Repository](https://github.com/mvanhorn/last30days-skill)
- [Official SKILL.md Runtime Specification](https://github.com/mvanhorn/last30days-skill/blob/main/SKILL.md)
- [Anthropic: Advanced Agentic Skills Guide](https://docs.anthropic.com/en/docs/agents-and-tools/skills)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high

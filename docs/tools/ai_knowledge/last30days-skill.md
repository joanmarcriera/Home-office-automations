# last30days-skill

## What it is
`last30days-skill` is a sophisticated AI agent skill for [Claude Code](../development_ops/claude-code.md), OpenClaw, and Gemini CLI. It acts as a specialized search and research engine that prioritizes real-time social signals (Reddit upvotes, X likes, YouTube transcripts, Polymarket odds) over traditional SEO-optimized web results.

## What problem it solves
Traditional search engines often surface stale editorial content or SEO-spam. In the fast-moving AI ecosystem, critical information first appears in community discussions. `/last30days` bridges a dozen disconnected platforms, allowing an AI agent to search, score, and synthesize current trends, tool comparisons, and "unfiltered" community feedback from the last 30 days.

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

## Getting started

### Installation (Claude Code)
```bash
# Add the skill via the Claude Code plugin marketplace
/plugin marketplace add mvanhorn/last30days-skill
```

### Basic Usage
```bash
# Research a topic
/last30days "Claude Code MCP servers"

# Generate a shareable HTML brief
/last30days "OpenRouter vs DeepSeek" --emit=html
```

### Installation (OpenClaw)
```bash
clawhub install last30days-official
```

## Technical details
- **Engine Architecture**: Built with Python 3.12+ and utilizes `yt-dlp` for YouTube transcript retrieval and a vendored Node.js client for X search.
- **Entity Resolution**: Bidirectional mapping between persons, companies, and their respective social/GitHub footprints.
- **Synthesis Engine**: Uses an "AI Agent Judge" to filter noise and cluster identical stories across multiple sources.
- **Privacy**: Operates locally on the user's machine; research data and API keys are not sent to external tracking servers.

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) (Primary harness)
- [Everything Claude Code](everything-claude-code.md) (Broader performance system)
- [Claude Skills Ecosystem](../agents/claude-skills-ecosystem.md) (Community context)
- [OpenRouter](openrouter.md) (API provider used for web search components)
- [Exa Search](../automation_orchestration/goose.md) (Similar neural search concept)

## Sources / references
- [last30days-skill GitHub Repository](https://github.com/mvanhorn/last30days-skill)
- [SKILL.md (Runtime Spec)](https://github.com/mvanhorn/last30days-skill/blob/main/SKILL.md)

## Contribution Metadata
- Last reviewed: 2026-05-17
- Confidence: high

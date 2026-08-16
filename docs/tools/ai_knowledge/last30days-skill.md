# last30days-skill

## What it is
`last30days-skill` is a highly optimized AI agent skill and search engine extension for Claude Code, OpenClaw, and custom command-line workflows. It functions as a specialized research assistant designed to prioritize real-time social signals (including Reddit upvotes, X engagement rates, YouTube transcripts, Polymarket odds, and Hacker News sentiment) over traditional search results, with native support for **FastMCP 3.1**.

## What problem it solves
Standard search engines often surface stale, generic editorial content or SEO-manipulated web results. In the rapidly evolving AI and software ecosystem, critical updates, bug reports, and novel methodologies first appear within developer communities. `/last30days` bridges these disconnected communication platforms, allowing frontier models like Claude 5.1, GPT-5.5, Gemini 4.0 Pro, and Llama 4 to search, rank, and synthesize authentic community discussions and technical trends from the last 30 days.

## Where it fits in the stack
**Category**: AI Assistants & Knowledge / Claude Code Skills. It functions as a FastMCP 3.1 server or native skill for terminal development environments, integrating with [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) for dynamic resource retrieval.

## Typical use cases
- **Deep Tool Comparison**: Querying `/last30days OpenClaw vs Hermes` to analyze real-world developer experience reports and commit velocities rather than marketing pages.
- **Pre-Meeting Briefings**: Instantly compiling a person's or company's technical and social contributions over the previous 30 days.
- **Outage and Bug Identification**: Finding immediate workarounds for newly introduced library bugs or service degradation (e.g., `/last30days vllm cuda 12.6 out of memory`).
- **Git History Synthesis**: Summarizing the last 30 days of issues, pull requests, and commits to onboard an AI agent to a codebase.

## Strengths
- **Social Signal Integration**: Ranks and filters results based on authentic developer engagement and sentiment analysis rather than standard keyword optimization.
- **Parallel Platform Ingestion**: Simultaneously queries GitHub, Hacker News, Reddit, and technical blogs using entity-aware subprocesses.
- **Smart Pre-Research**: Translates natural language queries into platform-optimized search syntax (hashtags, subreddits, user handles) automatically.
- **Modern Export Formats**: Emits interactive, responsive HTML reports, JSON structures, or clean Markdown files suitable for direct consumption by downstream models.

## Limitations
- **Token Consuming**: Synthesizing raw streams from multiple concurrent sources can quickly consume input tokens if limits are not strictly configured.
- **Rate-Limiting Susceptibility**: Strongly dependent on the API limits of external platforms (X, Reddit, GitHub), requiring robust caching mechanisms.
- **Recency Bias**: Intentionally overlooks mature documentation or long-standing guides in favor of information from the immediate 30-day window.

## When to use it
- When researching bleeding-edge software updates, frameworks, or newly released open-source models.
- When you need a "vibe check" on community reception or unexpected performance quirks of a new tool.
- When tracking live outages, active community-driven workarounds, or breaking API changes.

## When not to use it
- For historical academic research or reviewing stable, long-established APIs and concepts.
- When authoritative, official documentation is the primary requirement for production deployment.
- When building safety-critical systems where unverified social-media reports could introduce non-deterministic bugs.

## Getting started

### Installation (Claude Code Plugin)
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
# Research a specific technical topic
/last30days "Claude Code MCP servers"
```

## CLI examples

### Deep Tool Comparison with HTML Export
```bash
/last30days "OpenRouter vs DeepSeek V4" --emit=html --output=comparison.html
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
Using the modern Python SDK with strict Pydantic v2 schemas for robust input validation.

```python
from pydantic import BaseModel, Field, field_validator
from openclaw import SkillRunner
from typing import List, Optional

class SearchConfig(BaseModel):
    query: str = Field(..., min_length=3)
    platforms: List[str] = Field(default=["github", "reddit", "hacker-news"])
    max_results: Optional[int] = Field(default=15, ge=1)

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Query string cannot be blank")
        return v

# Initialize the skill
skill = SkillRunner("last30days-skill")

# Validate input schema
config = SearchConfig(
    query="Llama 4 Maverick performance benchmarks",
    platforms=["github", "reddit"]
)

# Execute research query
brief = skill.execute(
    query=config.query,
    depth="detailed",
    platforms=config.platforms
)

print(f"Summary: {brief.summary}")
```

### Programmatic Webhook Trigger (JavaScript)
Triggering a last30days research task programmatically from an external monitoring tool.

```javascript
// Post search request to local skill server
fetch('http://localhost:3000/skills/last30days/run', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'GPT-5.5 release dates and features',
    depth: 'comprehensive'
  })
})
.then(response => response.json())
.then(data => console.log('Research brief initialized:', data.task_id));
```

### FastMCP 3.1 Tool Schema (Agentic)
An agent using the Model Context Protocol (FastMCP 3.1) can call the skill using this standard JSON schema:

```json
{
  "tool": "last30days_search",
  "arguments": {
    "query": "Model Context Protocol FastMCP 3.1 updates",
    "sources": ["reddit", "hacker-news"],
    "limit": 10
  }
}
```

## Related tools / concepts
- [Claude Code](../development_ops/claude-code.md) — Primary terminal harness for the skill.
- [Everything Claude Code](everything-claude-code.md) — Comprehensive execution and optimization framework.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Standard protocol for skill and resource connection.
- [OpenRouter](openrouter.md) — API router used for executing backend neural queries.
- [AI Signal Sources](../../knowledge_base/ai_signal_sources.md) — Inventory of social platforms searched.
- [OpenClaw](../development_ops/openclaw.md) — Alternative orchestration engine for local skills.
- [Perplexity](../providers/perplexity.md) — Competitive neural search platform.
- [Valyu](valyu.md) — High-signal AI search endpoint.

## Sources / references
- [last30days-skill GitHub Repository](https://github.com/mvanhorn/last30days-skill)
- [SKILL.md (Runtime Spec)](https://github.com/mvanhorn/last30days-skill/blob/main/SKILL.md)
- [Anthropic Developer Portal: Building Claude Code Skills](https://docs.anthropic.com/claude/docs/code-skills)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

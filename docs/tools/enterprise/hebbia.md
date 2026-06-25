# Hebbia

## What it is
Hebbia is an AI-powered intelligence platform built for sophisticated reasoning and analysis over massive volumes of documents. It is specifically designed for high-stakes industries like finance, law, and corporate strategy where precision and cross-document synthesis are critical. As of June 2026, it serves as a primary "Reasoning Engine" for enterprise data using models like [Claude 4.8](../../tools/ai_knowledge/anthropic.md).

## What problem it solves
It addresses the "synthesis bottleneck." Instead of users manually reviewing thousands of pages of filings, transcripts, or contracts to find signals, Hebbia uses LLMs to reason across entire document sets simultaneously, providing structured answers with direct citations, significantly reducing time-to-insight for due diligence.

## Where it fits in the stack
**Category**: Enterprise AI / Analytical Layer. It sits above raw data storage as a specialized reasoning engine for complex research workflows.

## Typical use cases
- **Investment Research**: Analyzing earnings call transcripts and SEC filings for market-moving signals.
- **Legal Due Diligence**: Reviewing vast rooms of contracts to identify specific clauses or liabilities.
- **Corporate Strategy**: Sourcing buyer universes or building target lists based on complex criteria using **Hebbia Matrix** workflows.
- **Institutional Memory**: Converting past deal documents into "Skills" that automate future reasoning tasks.

## Strengths
- **Precision**: Focused on accuracy and audibility for "billion-dollar decisions."
- **Vertical Focus**: Deeply understands the specific workflows of finance and law.
- **Scale**: Capable of reasoning over millions of documents in a single session using the Matrix engine.
- **Citations & Verification**: Every answer is backed by direct, clickable links to the source document, ensuring 100% auditable results.

## Limitations
- **Vertical Specificity**: May be less effective for general creative or generic writing tasks.
- **Cost**: Institutional pricing targeted at large firms and high-value teams.
- **Closed Ecosystem**: Primarily a SaaS platform, which may not fit all self-hosted sovereignty requirements.

## When to use it
- When you need to synthesize information across hundreds of complex documents (PDFs, transcripts, filings).
- In high-stakes finance or legal environments where every AI claim must be auditable via direct citations.
- When you need a reasoning engine (Claude 4.8 or GPT-5.5 based) that understands professional terminology and complex financial structures.

## When not to use it
- For simple web-based questions that don't require deep document analysis (use [Perplexity](../ai_knowledge/perplexity.md)).
- If you are a small business or individual looking for a low-cost general-purpose AI assistant.
- For creative writing, marketing copy, or general brainstorming tasks.

## Getting started
Hebbia is a high-end enterprise SaaS platform. Access typically requires an institutional subscription.
1.  **Workspaces**: Create containers for specific research projects or document sets.
2.  **Matrix**: Initialize a high-dimensional analysis grid for cross-document synthesis.
3.  **Skills**: Select pre-defined reasoning patterns to standardize analysis across the team.

## CLI examples
> [!NOTE]
> Hebbia is primarily a web-based enterprise platform. Official CLI tools are generally restricted to institutional technical teams and are not publicly distributed as of June 2026.

## API examples

### Python (Triggering a Matrix Analysis)
```python
import requests

# Conceptual endpoint for Hebbia API v2 (2026)
API_URL = "https://api.hebbia.ai/v2/matrix/trigger"
API_TOKEN = "<INSTITUTIONAL_TOKEN>"

def run_matrix_analysis(project_id, skill_id):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {
        "project_id": project_id,
        "skill_id": skill_id,
        "callback_url": "https://hooks.yourfirm.com/hebbia-complete"
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    return response.json()
```

## Related tools / concepts
- [Bloomberg Terminal](https://www.bloomberg.com/professional/solution/bloomberg-terminal/)
- [Perplexity](../ai_knowledge/perplexity.md)
- [Glean](glean.md)
- [Fyxer AI](fyxer.md)
- [tldv](tldv.md)
- [Langfuse](../process_understanding/langfuse.md)
- [AgentOps](../process_understanding/agentops.md)
- [n8n](../../services/n8n.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude 4.8](../../tools/ai_knowledge/anthropic.md)

## Sources / References
- [Hebbia Official Website](https://www.hebbia.ai/)
- [Top AI Financial Research Platforms for 2026](https://www.hebbia.com/resources/financial-research-platforms)
- [Hebbia: What's New February 2026](https://www.hebbia.com/blog/the-disclosure-february-2026)
- [Hebbia Skills: Expertise at Institutional Scale](https://www.hebbia.com/blog/hebbia-skills-expertise-at-institutional-scale)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high

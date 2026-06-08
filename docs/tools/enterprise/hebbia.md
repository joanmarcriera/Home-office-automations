# Hebbia

## What it is
Hebbia is an AI-powered intelligence platform built for sophisticated reasoning and analysis over massive volumes of documents. It is specifically designed for high-stakes industries like finance, law, and corporate strategy where precision and cross-document synthesis are critical.

## What problem it solves
It addresses the "synthesis bottleneck." Instead of users manually reviewing thousands of pages of filings, transcripts, or contracts to find signals, Hebbia uses LLMs to reason across entire document sets simultaneously, providing structured answers with direct citations.

## Where it fits in the stack
**Enterprise Intelligence / Analytical Layer**. It sits above raw data storage as a specialized reasoning engine for complex due diligence and research workflows.

## Key Features
- **Hebbia Matrix**: A visual, collaborative workspace for running large-scale comparisons across thousands of documents simultaneously.
- **Hebbia Skills**: Converts institutional knowledge into scalable instructions that can be applied firm-wide to automate complex reasoning tasks.
- **Cross-Document Reasoning**: Ability to answer questions that require synthesizing information from multiple unrelated files (e.g., "Compare the risk factors across these 10 annual reports").
- **Finance-Tailored Chat**: Fine-tuned to respond using the tone and structure expected by finance professionals (e.g., GPT-5.5 and Claude 4.7 optimization).
- **Intelligent Data Selection**: Automatically detects and pulls in relevant data sources (e.g., Pitchbook, UK Companies House) based on the user's prompt.
- **Citations & Verification**: Every answer is backed by direct, clickable links to the source document, ensuring 100% auditable results.

## Typical use cases
- **Investment Research**: Analyzing earnings call transcripts and SEC filings for market-moving signals.
- **Legal Due Diligence**: Reviewing vast rooms of contracts to identify specific clauses or liabilities.
- **Corporate Strategy**: Sourcing buyer universes or building target lists based on complex criteria using Matrix workflows.

## Getting started
Hebbia is a high-end enterprise SaaS platform. Access typically requires an institutional subscription.

### Minimal Concepts
1.  **Workspaces**: Containers for specific research projects or document sets.
2.  **Matrix**: The high-dimensional analysis grid for cross-document synthesis.
3.  **Skills**: Pre-defined reasoning patterns used to standardize analysis.

### Analytical Example
Hebbia is used for extracting signals across multiple documents. A typical prompt might look like:

> "Extract all mentions of 'cybersecurity risk' across the provided 10-K filings for Batch 2026. Create a Matrix comparing the mitigation strategies mentioned by each company using our standard risk assessment Skill."

## CLI examples
> [!NOTE]
> Hebbia is primarily a web-based enterprise platform. Official CLI tools are generally restricted to institutional technical teams and are not publicly distributed.

## API examples
> [!NOTE]
> Hebbia provides a private REST API for institutional integration. Below is a conceptual snippet for triggering a Matrix update via a webhook pattern.

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

## Strengths
- **Precision**: Focused on accuracy and audibility for "billion-dollar decisions."
- **Vertical Focus**: Deeply understands the specific workflows of finance and law.
- **Scale**: Capable of reasoning over millions of documents in a single session using the Matrix engine.

## Limitations
- **Vertical Specificity**: May be less effective for general creative or generic writing tasks.
- **Cost**: Institutional pricing targeted at large firms and high-value teams.

## When to use it
- When you need to synthesize information across hundreds of complex documents (PDFs, transcripts, filings).
- In high-stakes finance or legal environments where every AI claim must be auditable via direct citations.
- When you need a reasoning engine (Claude 4.7 or GPT-5.5 based) that understands professional terminology and complex financial structures.

## When not to use it
- For simple web-based questions that don't require deep document analysis (use [Perplexity](../ai_knowledge/perplexity.md)).
- If you are a small business or individual looking for a low-cost general-purpose AI assistant.
- For creative writing, marketing copy, or general brainstorming tasks.

## Related tools / concepts
- [Bloomberg Terminal](https://www.bloomberg.com/professional/solution/bloomberg-terminal/) (Legacy incumbent)
- [Perplexity](../ai_knowledge/perplexity.md) (Generalist alternative for research)
- [Glean](glean.md) (Unified search across company SaaS apps)
- [Fyxer AI](fyxer.md) (Inbox and administrative management)
- [tldv](tldv.md) (Transcription and knowledge extraction from meetings)
- [Langfuse](../process_understanding/langfuse.md) (Observability for LLM analytical pipelines)
- [AgentOps](../process_understanding/agentops.md) (Monitoring for research agents)
- [n8n](../../services/n8n.md) (Automating data flows into research workspaces)
- [Coveo](coveo.md) (Enterprise search and relevance)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) (Standard for connecting tools to agents)

## Sources / References
- [Top AI Financial Research Platforms for 2026](https://www.hebbia.com/resources/financial-research-platforms)
- [Hebbia: What's New February 2026](https://www.hebbia.com/blog/the-disclosure-february-2026)
- [Hebbia Skills: Expertise at Institutional Scale](https://www.hebbia.com/blog/hebbia-skills-expertise-at-institutional-scale)

## Contribution Metadata
- Last reviewed: 2026-06-07
- Confidence: high

# Hebbia

## What it is
Hebbia is an AI-powered enterprise intelligence platform built for sophisticated reasoning and multi-document analysis over massive volumes of documents. It is specifically designed for high-stakes industries like finance, law, government, and corporate strategy where precision and cross-document synthesis are critical. As of early January 2027, it serves as a primary "Reasoning Engine" for enterprise data using state-of-the-art models like Claude 5.1 and GPT-5.5.

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
- When you need a reasoning engine (Claude 5.1 or GPT-5.5 based) that understands professional terminology and complex financial structures.

## When not to use it
- For simple web-based questions that don't require deep document analysis (use [Perplexity](../providers/perplexity.md)).
- If you are a small business or individual looking for a low-cost general-purpose AI assistant.
- For creative writing, marketing copy, or general brainstorming tasks.

## Getting started
Hebbia is a high-end enterprise SaaS platform. Access typically requires an institutional subscription.
1. **Workspaces**: Create containers for specific research projects or document sets.
2. **Matrix**: Initialize a high-dimensional analysis grid for cross-document synthesis.
3. **Skills**: Select pre-defined reasoning patterns to standardize analysis across the team.

## CLI examples
> [!NOTE]
> Hebbia is primarily a web-based enterprise platform. Official CLI tools are generally restricted to institutional technical teams and are not publicly distributed as of early January 2027. However, users can use standard curl or custom CLI helper scripts to trigger Hebbia workspace analyses.

### Triggering Matrix Run via Curl
```bash
curl -X POST "https://api.hebbia.ai/v2/matrix/trigger" \
  -H "Authorization: Bearer $HEBBIA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "proj_908123", "skill_id": "skill_extract_risk_factors"}'
```

## API examples

### Python (Triggering a Matrix Analysis with Pydantic v2 Schema Validation)
Trigger Hebbia Matrix analyses and validate response schemas using Pydantic v2:

```python
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class HebbiaMatrixTriggerPayload(BaseModel):
    project_id: str = Field(description="Hebbia workspace or project ID")
    skill_id: str = Field(description="Pre-defined reasoning pattern skill ID")
    callback_url: Optional[str] = Field(default=None, description="Webhook callback for async completion")

class HebbiaMatrixResponse(BaseModel):
    task_id: str = Field(description="Task tracking ID for the matrix job")
    status: str = Field(description="Current status of the job, e.g. queued or processing")
    estimated_duration_sec: int = Field(ge=0, description="Estimated time to completion in seconds")

def build_matrix_trigger_request(project_id: str, skill_id: str) -> dict:
    payload = HebbiaMatrixTriggerPayload(
        project_id=project_id,
        skill_id=skill_id,
        callback_url="https://hooks.yourfirm.com/hebbia-complete"
    )
    return payload.model_dump()

if __name__ == "__main__":
    request_data = build_matrix_trigger_request("proj_908123", "skill_extract_risk_factors")
    print(f"Validated Hebbia Request Payload for project '{request_data['project_id']}'")
```

### FastMCP 3.1 Integration Snippet
Expose Hebbia Matrix research triggers as a FastMCP 3.1 tool for enterprise agent workflows:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("HebbiaEnterpriseIntelligence")

class MatrixRunRequest(BaseModel):
    project_id: str = Field(description="Target project container ID")
    skill_id: str = Field(description="Hebbia Skill ID to apply across documents")

@mcp.tool()
def trigger_hebbia_matrix(request: MatrixRunRequest) -> dict:
    """Trigger a Hebbia Matrix cross-document analysis job."""
    return {
        "status": "queued",
        "task_id": "heb-task-2027-0912",
        "project_id": request.project_id,
        "skill_id": request.skill_id,
        "message": "Hebbia Matrix job successfully dispatched."
    }

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Bloomberg Terminal](https://www.bloomberg.com/professional/solution/bloomberg-terminal/)
- [Perplexity](../providers/perplexity.md)
- [Glean](glean.md)
- [Fyxer AI](fyxer.md)
- [tldv](tldv.md)
- [Langfuse](../process_understanding/langfuse.md)
- [AgentOps](../process_understanding/agentops.md)
- [n8n](../../services/n8n.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Anthropic](../providers/anthropic.md)

## Sources / References
- [Hebbia Official Website](https://www.hebbia.ai/)
- [Top AI Financial Research Platforms for 2026/2027](https://www.hebbia.com/resources/financial-research-platforms)
- [Hebbia Skills: Expertise at Institutional Scale](https://www.hebbia.com/blog/hebbia-skills-expertise-at-institutional-scale)

## Contribution Metadata
- Last reviewed: 2027-01-06
- Confidence: high

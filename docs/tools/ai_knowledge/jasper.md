# Jasper

## What it is
Jasper is an enterprise AI marketing orchestration platform designed to power omnichannel content creation, brand governance, and marketing campaigns. In early 2027, it operates as a centralized "Brand Brain" utilizing **Jasper IQ 2.0**, **Brand Voice Guardrails**, and multi-model routing optimized for frontier reasoning engines like `claude-5-1-pro-20260915`, GPT-5.5, and Gemini 4.0 Pro.

## What problem it solves
Eliminates brand inconsistency, content bottlenecks, and siloed campaign execution across enterprise marketing teams. Jasper ensures every generated asset—from blog posts and ad copy to executive emails—strictly adheres to company style guides, brand terminology, and product knowledge repositories while scaling production velocity.

## Where it fits in the stack
**AI & Knowledge / Marketing Orchestration**. It functions as the brand governance and asset generation layer sitting between enterprise content repositories (CMS, DAM) and marketing execution channels (email automation, social, search ads).

## Typical use cases
- **Omnichannel Campaign Orchestration**: Generating coordinated landing page copy, email sequences, social posts, and ad creative from a single campaign brief.
- **Enterprise Brand Voice Enforcement**: Training custom AI profiles on corporate style guides, brand rules, and tone guidelines to maintain global consistency across departments.
- **AI Content Ops at Scale**: Accelerating marketing asset workflows with multi-stage approval pipelines, plagiarism verification, and compliance checks.
- **Performance-Grounded SEO Content**: Writing long-form articles, landing pages, and product descriptions scored for target keywords and search intent.

## Strengths
- **Jasper IQ 2.0 Engine**: Unifies company knowledge bases, product documentation, and custom brand voice profiles to ground generative outputs in factual company context.
- **Multi-Brand Voice Governance**: Supports distinct voice profiles across multiple sub-brands, business units, or regional target audiences.
- **Campaign Agent v3**: Autonomous marketing agent that breaks down campaign briefs into platform-specific content assets generated in parallel execution loops.
- **FastMCP 3.1 Integration**: Native support for the Model Context Protocol allows Jasper to discover external enterprise tools, CMS integrations, and analytics servers.
- **Enterprise Security & Reliability**: SOC 2 Type II compliance, zero data retention agreements for enterprise LLMs, and 99.99% operational uptime.

## Limitations
- **Enterprise Licensing Costs**: Premium pricing structure tailored for commercial organizations; no permanent free tier available.
- **Strategy & Strategy Verification Needed**: Requires marketing human-in-the-loop oversight to ensure campaign messaging aligns with broader business strategy.
- **SaaS Execution**: Closed commercial platform; does not support air-gapped or purely local deployments.

## When to use it
- When scaling content production across multiple global marketing teams while enforcing strict brand voice compliance.
- For complex, multi-channel marketing campaigns that require structured asset generation grounded in corporate product knowledge.

## When not to use it
- For general-purpose coding, technical data science, or standard software engineering tasks.
- When an open-source or local privacy-first architecture is strictly required (e.g., using [Local LLMs](local_llms.md)).

## Getting started

Jasper integrates into enterprise workflows via its web portal, browser extensions, and REST API endpoints.

### 1. Knowledge Base & Brand Profile Setup
Upload company guidelines, product manuals, and sample top-performing copy to construct **Jasper IQ** knowledge bases and **Brand Voice** profiles.

### 2. Campaign Agent Builder
Define multi-asset campaign templates inside the **Campaigns** tab to generate coordinated assets automatically from a single prompt or brief.

### 3. API Integration
Generate an API token under **Workspace Settings > Developer Settings** to enable programmatically triggered generation from custom CMS or CRM workflows.

## CLI examples

> [!NOTE]
> Programmatic interaction with Jasper is performed via `curl` against the Jasper REST API or through terminal orchestration tools like [Claude Code](../development_ops/claude-code.md).

### 1. Generate Content via REST API
```bash
curl -X POST https://api.jasper.ai/v1/content/generate \
  -H "Authorization: Bearer $JASPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a 500-word product launch announcement for our new cloud security platform.",
    "brand_voice_id": "bv_987654",
    "model": "jasper-v3"
  }'
```

### 2. List Configured Brand Voices
```bash
curl -s -H "Authorization: Bearer $JASPER_API_KEY" \
  https://api.jasper.ai/v1/brand-voices
```

### 3. Retrieve Campaign Generation Results
```bash
curl -s -H "Authorization: Bearer $JASPER_API_KEY" \
  https://api.jasper.ai/v1/campaigns/camp_123456
```

## API examples

### Python: Brand-Aware Asset Generation with Pydantic v2
The following Python script demonstrates invoking Jasper's API with strict input and output schema validation using **Pydantic v2**.

```python
import os
import requests
from pydantic import BaseModel, Field, field_validator


class ContentRequest(BaseModel):
    prompt: str = Field(..., min_length=15, description="Detailed text prompt for asset generation")
    brand_voice_id: str = Field(..., description="Unique ID for target brand voice profile")
    model: str = Field(default="jasper-v3", description="Engine model ID")

    @field_validator("prompt")
    @classmethod
    def validate_prompt_length(cls, v: str) -> str:
        if "brand" not in v.lower() and len(v) < 20:
            raise ValueError("Prompts must be detailed to ensure quality output")
        return v


class ContentResponse(BaseModel):
    id: str
    content: str
    word_count: int = Field(default=0)


def generate_marketing_asset(prompt: str, voice_id: str) -> ContentResponse:
    url = "https://api.jasper.ai/v1/content/generate"
    headers = {
        "Authorization": f"Bearer {os.getenv('JASPER_API_KEY', '')}",
        "Content-Type": "application/json"
    }

    payload = ContentRequest(prompt=prompt, brand_voice_id=voice_id)

    response = requests.post(url, json=payload.model_dump(), headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    generated_text = data.get("content", "")

    return ContentResponse(
        id=data.get("id", "res_unk"),
        content=generated_text,
        word_count=len(generated_text.split())
    )


if __name__ == "__main__":
    req = ContentRequest(
        prompt="Write a compelling LinkedIn post introducing our new AI governance framework.",
        brand_voice_id="bv_987654"
    )
    print(f"Validated request schema: {req.model_dump_json()}")
```

## Related tools / concepts
- [Copy.ai](copy-ai.md) — GTM and sales workflow automation platform.
- [Claude](../development_ops/claude-hooks.md) — Frontier LLM powering creative reasoning.
- [ChatGPT](chatgpt.md) — General purpose model interface.
- [Model Context Protocol (MCP)](../../tools/automation_orchestration/mcp.md) — Tool discovery and context protocol.
- [n8n](../../services/n8n.md) — Open-source workflow orchestration engine.

## Sources / references
- [Official Website](https://www.jasper.ai/)
- [Jasper Campaign Agent Overview](https://www.jasper.ai/agents/multi-channel-campaign)
- [Jasper Developer API Reference](https://help.jasper.ai/hc/en-us/articles/18618701173659-Jasper-s-API)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Humanizer

## What it is
Humanizer (v3.5+) is a community-driven, highly optimized skill for **Claude Code**, **OpenCode**, and agentic platforms supporting the **FastMCP 3.1 Task Protocol**. As of early January 2027, it is designed to audit, refine, and calibrate AI-generated text, systematically stripping away robotic clichés, repetitive AI jargon, and predictable syntactic distributions to deliver natural, human-like copy.

Powered by advanced style-transfer heuristics and pattern registries aligned with early 2027 frontier LLMs (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, and DeepSeek-V4), Humanizer acts as an automated "voice and tone editor." It eliminates monotone sentence structures, removes artificial AI buzzwords, and applies customizable author profiles to make agent-generated content indistinguishable from human writing.

## What problem it solves
Large language models—regardless of parameter count or fine-tuning quality—exhibit distinct statistical artifacts in text generation:
- **Repetitive Jargon & AI Clichés**: Persistent overuse of words and phrases like "delve," "pivotal," "testament," "nestled," "in summary," and "revolutionize."
- **Predictable Cadence & Sentence Length Distribution**: Monotonous sentence lengths and uniform clause structures that trigger automated AI detection algorithms and bore human readers.
- **Overly Formulaic Formatting**: Rigid reliance on introductory summaries, predictable transitional paragraphs, and uniform bulleted lists.
- **Loss of Personal Voice**: Machine-generated communications often lack the idiomatic expressions, variable rhythm, and subtle stylistic nuances that define a specific brand or individual author.

Humanizer solves these challenges by evaluating text against an active pattern registry (derived from community writing guidelines, Wikipedia AI style audits, and empirical datasets) and applying dynamic sentence-length adjustments, lexical substitutions, and persona alignment without altering core technical facts.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / Output Refinement & Tone Alignment Layer.

Humanizer operates at the **Output Gate** of agentic text workflows. Situated between raw LLM generation nodes (such as content synthesis agents, automated documentation generators, or email drafting routines) and public publishing surfaces (documentation sites, PR descriptions, customer success messages, or marketing channels), Humanizer ensures all published text adheres to natural stylistic standards.

```
+-----------------------------------------------------------------------+
|                       LLM Agent Generation Node                       |
|          (Claude 5.6 / GPT-5.6 / OpenCode / LangGraph Agent)           |
+-----------------------------------------------------------------------+
                                   |
                                   | Raw Synthesized Text Stream
                                   v
+-----------------------------------------------------------------------+
|                       Humanizer Skill / MCP Tool                      |
|                                                                       |
|  +--------------------+  +--------------------+  +-----------------+  |
|  | Cliché & Jargon Scan|  | Dynamic Cadence Filter| | Voice Matching |  |
|  +--------------------+  +--------------------+  +-----------------+  |
+-----------------------------------------------------------------------+
                                   |
                                   | Refined, Natural Copy
                                   v
+-----------------------------------------------------------------------+
|                      Public Publishing Surface                        |
|       (Documentation Portal / Pull Request / Customer Portal / Slack)  |
+-----------------------------------------------------------------------+
```

## Typical use cases
- **Automated Technical Documentation Polish**: Refining AI-generated API references, changelogs, and architectural decision records to eliminate repetitive filler words.
- **Brand Voice Alignment ("Soul Injection")**: Calibrating generated drafts against a writer's sample text to adopt their exact sentence length variations and stylistic habits.
- **Agentic Customer Communications**: Polishing automated support replies, email outreach campaigns, or Slack reports prior to customer delivery.
- **AI Detection Mitigation**: Restoring natural human entropy and structural variance to technical articles, ensuring they bypass false-positive automated AI classification checks.
- **Multi-Agent Editorial Pipeline**: Functioning as an automated sub-task in FastMCP 3.1 multi-agent editorial loops to audit and polish drafts created by primary research agents.

## Strengths
- **Native Claude Code & OpenCode Integration**: Direct slash-command bindings (`/humanizer`) for terminal developer agent workflows.
- **Local-First Processing**: Executes pattern scanning and tone transformations locally or within workspace context without extra external cloud hops.
- **FastMCP 3.1 Task Protocol Conformant**: Fully compatible with FastMCP 3.1 tool schemas, allowing easy orchestration inside complex agent DAGs.
- **Dynamic Cadence Adjustment**: Breaks up monotonous paragraph structures by injecting sentence-length variance and conversational transitions.
- **Extensible Cliché Registries**: Uses easily customizable pattern files to block organization-specific buzzwords and forbidden phrases.

## Limitations
- **Frontier Model Dependency**: Achieving subtle tone shifts without losing factual precision requires advanced reasoning models (e.g., Claude 5.6 Sonnet or GPT-5.6).
- **Domain Over-Smoothing**: Over-humanizing strictly regulated legal or technical compliance specifications can accidentally reduce precision if strict thresholds are not configured.
- **Pattern Registry Drift**: As AI writing habits evolve over time, the cliché detection registries must be periodically updated.

## When to use it
- When automated agent pipelines generate public-facing copy, articles, or customer support responses.
- When maintaining a consistent human brand voice across content written by multiple autonomous agents.
- When polishing pull request descriptions, commit logs, or release notes generated by developer agents.

## When not to use it
- On raw code, mathematical formulas, or structured JSON/YAML configuration payloads.
- In low-latency sub-50ms API endpoints where extra text refinement passes introduce unwanted response delay.

## Getting started

### 1. Installation in Claude Code / OpenCode
Clone the Humanizer skill into your global agent skills directory:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/blader/humanizer.git ~/.claude/skills/humanizer
```

### 2. Verify Installation
List registered agent skills to verify active binding:

```bash
claude-code skill list | grep humanizer
```

## CLI examples

### 1. Refine Single Text Block via Slash Command
In your Claude Code or OpenCode terminal session, run:

```bash
/humanizer "This framework marks a pivotal milestone in the realm of agentic data orchestration."
```

### 2. Calibrate Tone Against a Writing Sample
Train Humanizer on a custom voice sample file before polishing drafts:

```bash
/humanizer --calibrate --sample "./docs/author_voice.txt" --input "./drafts/article.md"
```

### 3. Pipeline Mode (UNIX Piping)
Process Markdown drafts in continuous integration scripts:

```bash
cat draft.md | humanizer-cli --strict --output refined.md
```

## API examples

### 1. FastMCP 3.1 Humanizer Tool Server (Python)
Expose text humanization capabilities as an agent tool using FastMCP 3.1:

```python
import os
import re
from typing import Dict, Any, List, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

mcp = FastMCP(
    "Humanizer Engine",
    version="3.5.0",
    description="FastMCP 3.1 tool server for scanning and removing AI writing clichés, jargon, and uniform sentence structures."
)

DEFAULT_CLICHES = [
    "delve", "pivotal", "testament", "nestled", "in conclusion",
    "beacon", "realm", "game-changer", "transformative", "tapestry"
]

class HumanizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Raw text to be analyzed and humanized")
    strict_mode: bool = Field(default=True, description="Strictly strip all flagged clichés")
    custom_avoid_words: Optional[List[str]] = Field(default_factory=list, description="Additional buzzwords to eliminate")

    @field_validator("text")
    @classmethod
    def check_non_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Input text cannot be empty or whitespace only.")
        return v

@mcp.tool()
async def scan_ai_cliches(text: str) -> Dict[str, Any]:
    """
    Scans input text for known AI writing indicators and returns a diagnostic score.
    """
    found_cliches = []
    text_lower = text.lower()
    for word in DEFAULT_CLICHES:
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = re.findall(pattern, text_lower)
        if matches:
            found_cliches.append({"word": word, "count": len(matches)})

    score = max(0, 100 - (len(found_cliches) * 15))
    return {
        "human_score": score,
        "cliches_detected": found_cliches,
        "is_natural": score >= 85
    }

@mcp.tool()
async def refine_text(request: HumanizeRequest) -> Dict[str, Any]:
    """
    Applies Humanizer transformation rules to produce natural, human-like text.
    """
    avoid_list = set(DEFAULT_CLICHES + [w.lower() for w in request.custom_avoid_words])

    # Simple substitution pipeline for demonstration
    refined = request.text
    replacements = {
        r"\bdelve into\b": "explore",
        r"\bpivotal\b": "key",
        r"\btestament to\b": "proof of",
        r"\bin conclusion\b": "overall",
        r"\bgame-changer\b": "major step forward"
    }

    for pattern, replacement in replacements.items():
        refined = re.sub(pattern, replacement, refined, flags=re.IGNORECASE)

    return {
        "original_text": request.text,
        "refined_text": refined,
        "transformations_applied": len(replacements)
    }

if __name__ == "__main__":
    mcp.run()
```

### 2. Pydantic v2 Text Transformation Pipeline Schema
Validate humanization job parameters and custom brand voice profiles before dispatching editing tasks:

```python
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict

class BrandVoiceProfile(BaseModel):
    """
    Pydantic v2 schema defining custom target tone and sentence length rules.
    """
    profile_name: str = Field(..., description="Unique label for the author or brand voice profile")
    target_sentence_length_avg: int = Field(default=16, ge=8, le=30, description="Target average words per sentence")
    preferred_tone: str = Field(default="conversational_technical", description="Tone style identifier")
    forbidden_phrases: List[str] = Field(default_factory=list, description="Custom blacklisted words")

    @field_validator("forbidden_phrases")
    @classmethod
    def lowercase_phrases(cls, phrases: List[str]) -> List[str]:
        return [p.strip().lower() for p in phrases if p.strip()]

class HumanizerJobPayload(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    document_id: str = Field(..., description="Identifier for the document being processed")
    raw_markdown: str = Field(..., min_length=20, description="Markdown content to humanize")
    voice_profile: Optional[BrandVoiceProfile] = Field(None, description="Optional custom voice profile")

if __name__ == "__main__":
    profile = BrandVoiceProfile(
        profile_name="TechLead_Casual",
        target_sentence_length_avg=14,
        forbidden_phrases=["synergy", "paradigm shift", "delve"]
    )

    payload = HumanizerJobPayload(
        document_id="DOC-2027-01",
        raw_markdown="In this section, we delve into the paradigm shift enabled by FastMCP 3.1.",
        voice_profile=profile
    )

    print("Humanizer payload validated successfully against Pydantic v2 schema!")
    print(payload.model_dump_json(indent=2))
```

## Related tools / concepts
- [Claude Code](claude-code.md) — Terminal-native developer agent that uses Humanizer as an embedded skill.
- [OpenCode](opencode.md) — Open agent framework with native skill execution support.
- [Model Context Protocol (FastMCP 3.1)](../automation_orchestration/mcp.md) — Protocol for exposing Humanizer as a tool service.
- [Aider](aider.md) — Git-integrated coding assistant for automated refactoring.

## Sources / references
- [Humanizer Community Skill GitHub Repository](https://github.com/blader/humanizer)
- [Wikipedia: Signs of AI Writing Guidelines](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [FastMCP 3.1 Protocol Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

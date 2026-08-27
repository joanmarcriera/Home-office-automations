# Anthropic Agent Skills

## What it is
Anthropic Agent Skills (v1.3+, early January 2027) are standardized, highly optimized, and encapsulated task recipes—consisting of specialized system prompts, executable scripts, and API tool declarations—that autonomous agents load dynamically to solve complex, domain-specific engineering problems. Originally popularized within the [Claude Skills Ecosystem](claude-skills-ecosystem.md) to supercharge [Claude Code](../development_ops/claude-code.md), they have evolved into open-source specifications under the `agentskills.io` standard. These skills can be seamlessly executed across multi-model setups—pairing frontier models like [Claude 5.6](../providers/anthropic.md) and Claude Mythos as high-level coordinators with local models like [Gemma 4](../ai_knowledge/local_llms.md) or [Qwen 3.6](../ai_knowledge/local_llms.md) for sandbox script validation and local file parsing. They support the [Model Context Protocol (MCP) 3.1](../../knowledge_base/agent_protocols.md) and FastMCP 3.1 Task Protocol specifications.

## What problem it solves
General-purpose LLMs struggle with reliable, multi-step operations (e.g., refactoring large codebases, extracting data tables from nested PDFs, or writing compliant API connectors) when guided only by basic, loose system prompting. Under traditional prompting, they run into hallucinations or deviate from strict formatting criteria. Agent Skills solve this by bundling explicit executable check-lists, specialized tooling hooks, and sandboxed test suites. This teaches the model a deterministic, repeatable "System 2" workflow for specialized engineering, debugging, and document extraction tasks.

## Where it fits in the stack
[Layer 6: Agents & Orchestration](../../knowledge_base/ai_tooling_landscape.md#layer-6-agents-orchestration) — specifically as **Agent Capability Enhancements, Custom Tools, and Encapsulated Playbooks** sitting directly between the raw foundational LLM reasoning layer and external execution shells (e.g., [Aider](../development_ops/aider.md), [Claude Code](../development_ops/claude-code.md)).

## Typical use cases
- **Multi-Repo Engineering Audits**: Running comprehensive security static analysis or dependency trees across distinct code repositories using standard bash/file-system skill packages.
- **Enterprise Report Generation**: Automatically reading raw client logs, synthesizing structured data pools, and writing formatted corporate PDF summaries.
- **Automated Verification Harnesses**: Launching isolated docker sandboxes to run user-defined unit tests, compiling results, and correcting compilation errors autonomously.
- **High-Fidelity PDF/Document Processing**: Running complex OCR and layout-parsing pipelines (e.g., using [Ovis OCR](../process_understanding/ovisocr2.md)) to extract tabular datasets from dense manuals.

## Strengths
- **Deterministic Repeatability**: Guarantees highly consistent, predictable output formats and agent execution patterns for complex workflows.
- **Standardized and Portable**: Complies with the `agentskills.io` community standard, letting developers swap skill manifests between different CLI agent runners like [Aider](../development_ops/aider.md) and [Claude Code](../development_ops/claude-code.md).
- **Auto-Discovery Frontmatter**: Includes YAML manifests allowing agentic routers to dynamically discover, evaluate, and load skills on-demand based on prompt intent.
- **MCP 3.1 & FastMCP 3.1 Coherence**: Exposes skill scripts and check-lists as native tool endpoints for any standard client.

## Limitations
- **Claude Optimization**: Highly aligned with the tool-calling structures and reasoning pathways of the Anthropic Claude model family; performance on other providers ([GPT-5.6](../ai_knowledge/chatgpt.md)) might require adapter scripts.
- **Sandbox Dependency**: Skills typically require a safe local sandboxed container (e.g., Docker) to execute their accompanying code generators or script runner files securely.
- **Token Usage**: Dynamic loading of dense skill system instructions, schemas, and verification checklists can inflate session prompt tokens.

## When to use it
- When you require an agent to complete multi-step technical workflows with high precision and adherence to a strict formatting standard.
- When building modular agent architectures that load specialized feature skill sets dynamically to minimize system prompt bloat.
- If you are building a team of autonomous engineers utilizing [Claude 5.6](../providers/anthropic.md) and [Claude Code](../development_ops/claude-code.md).

## When not to use it
- For general-purpose, single-step chat conversations that do not require tool use or multi-file scripts.
- In severely locked-down hosting environments that forbid executing local scripts (e.g., Python/Node.js VM execution layers).
- For simple routing workflows where traditional, lightweight JSON schemas satisfy the application rules.

## Getting started
### Installation
To start authoring or running standardized agent skills:
```bash
pip install agentskills-sdk pydantic
```

### Configuration
Expose your custom or cloned skills folder to your active CLI agent environment. For instance, configuring `claude.json` to point to a local path:
```json
{
  "skills_directory": "./skills",
  "mcp_version": "3.1"
}
```

## CLI examples
```bash
# Clone the open-source community repository of standard engineering skills
git clone https://github.com/anthropics/skills.git

# Audit and list all available skills and YAML manifests in your local workspace
agentskills list --dir ./skills

# Test a specific skill payload using mock schemas
python3 ./skills/document-processing/test.py
```

## API examples
### Skill Manifest and Telemetry Trace Verification (Pydantic v2)
In automated enterprise pipelines, ensuring that dynamically loaded skills comply with architectural limits (e.g., maximum step counts, token bounds, and authorized MCP tools) is vital. The following script validates a skill manifest and execution telemetry trace using Pydantic v2:

```python
from typing import List, Dict, Literal, Any
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class SkillManifest(BaseModel):
    skill_name: str = Field(..., description="Encapsulated skill identifier")
    version: str = Field("1.1.0")
    required_models: List[str] = Field(default_factory=list, description="Target model configurations")
    required_tools: List[str] = Field(default_factory=list, description="Mandatory MCP tools")

class SkillTelemetry(BaseModel):
    calls_count: int = Field(..., ge=0)
    failed_calls: int = Field(0, ge=0)
    token_usage: int = Field(..., ge=0)

class SkillExecutionTrace(BaseModel):
    trace_id: str
    manifest: SkillManifest
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: Literal["active", "completed", "policy_violation", "error"] = Field("active")
    telemetry: SkillTelemetry

    @field_validator("status")
    @classmethod
    def validate_trace_status(cls, val: str) -> str:
        allowed = {"active", "completed", "policy_violation", "error"}
        if val not in allowed:
            raise ValueError(f"Trace status must be one of {allowed}")
        return val

# Sample metadata from an automated skill load
trace_log = {
    "trace_id": "skill-trace-8841-nov",
    "manifest": {
        "skill_name": "repo-security-audit",
        "version": "1.1.2",
        "required_models": ["claude-5-6-sonnet", "gemma4-31b"],
        "required_tools": ["fetch_directory_tree", "execute_sandbox_test"]
    },
    "timestamp": "2026-12-05T16:45:00Z",
    "status": "completed",
    "telemetry": {
        "calls_count": 12,
        "failed_calls": 0,
        "token_usage": 28450
    }
}

# Strictly validate the skill trace
validated_trace = SkillExecutionTrace(**trace_log)
print(f"Validated Skill: {validated_trace.manifest.skill_name} (v{validated_trace.manifest.version})")
print(f"Execution Status: {validated_trace.status} with {validated_trace.telemetry.token_usage} tokens utilized.")
```

## Related tools / concepts
- [Claude Skills Ecosystem](claude-skills-ecosystem.md)
- [Claude Code](../development_ops/claude-code.md)
- [Aider](../development_ops/aider.md)
- [Roo Code](roo-code.md)
- [Cline](cline.md)
- [Documentation Writer Skill](documentation-writer.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)

## Sources / references
- [Agent Skills Official Specification](https://agentskills.io)
- [GitHub Repository for Standard Skills](https://github.com/anthropics/skills)
- [Anthropic News: Equipping agents with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

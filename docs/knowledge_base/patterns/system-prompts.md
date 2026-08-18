# System Prompt Engineering

## What it is

- **Persona & Identity Declaration**: Explicitly defining the agent's identity, domain expertise, operational mission, and communication tone.
- **Guardrails & Boundary Enforcement**: Implementing strict negative constraints (what the model *must not* do) to prevent safety violations, policy bypasses, and out-of-scope actions.
- **Tool Instruction & Orchestration**: Providing dynamic tool manifests, parameter schemas, error recovery instructions, and multi-step tool call sequences.
- **Structured Output Formatting**: Specifying rigid output formats (JSON/YAML, strict Pydantic v2 validation schemas, XML tags for chain-of-thought reasoning).
- **Dynamic Context Ingestion**: Structuring context window sections for RAG document chunks, conversation history, user preferences, and state memory.


## What problem it solves
- Solves non-deterministic LLM output drift, hallucination, and tool formatting errors in production AI applications.
- Enforces strict operational guardrails, persona constraints, and structured JSON output schemas.

## Where it fits in the stack
- Sits in the **Agent Orchestration & Prompt Engineering** layer.
- Acts as the primary operational instruction interface between application logic and frontier LLM APIs.

## Typical use cases

- **Specialized Agent Personas**: Creating domain-specific personas (e.g., Code Reviewer, Security Auditor, Data Analyst, Technical Writer) used in suites like [Agency-Agents](../tools/agents/agency-agents.md).
- **Multi-Agent Orchestration Swarms**: Configuring system prompts for specialized sub-agents (Planner, Researcher, Coder, Verifier) in multi-agent frameworks.
- **Enterprise Regulatory Compliance**: Enforcing privacy policies, anti-hallucination guardrails, and compliance standards in customer-facing and internal assistant deployments.
- **Fast Router & Classifier Models**: Instructing high-speed router models (e.g., DeepSeek Flash Pro, Gemini 4.0 Flash) to categorize intent and route requests to downstream pipelines.


## Strengths

- **High Precision Steering**: Structured system prompts significantly reduce non-deterministic output drift and hallucination rates across complex tasks.
- **Zero-Retraining Adaptability**: Modify agent capabilities, corporate policy compliance, or tool interfaces instantly by updating prompt templates.
- **Protocol Alignment**: Seamlessly integrates FastMCP 3.1 tool schemas and structured outputs with native Pydantic v2 validation.


## Limitations

- **Context Window Overhead**: Highly detailed system prompts consume context window space, increasing token consumption costs and input processing latency.
- **Prompt Injection Risks**: System prompt instructions can still be vulnerable to adversarial user prompt injections if input sanitization is lacking.


## When to use it

- When building production AI applications requiring structured outputs, low latency, and reliable tool execution.
- When configuring agent persona suites for autonomous multi-agent orchestration frameworks.
- When enforcing enterprise safety guardrails and domain knowledge boundaries for LLM deployments.


## When not to use it
- When performing simple, unstructured text completions or raw semantic classification tasks.
- When context window token limits are severely constrained and static system instructions add unnecessary overhead.

## Getting started

```
+-------------------------------------------------------------------+
| System Prompt Engineering Pipeline                               |
|                                                                   |
|   +-------------------+    +----------------+    +------------+   |
|   | Base System       |    | Dynamic        |    | FastMCP    |   |
|   | Prompt Skeleton   | +  | Context / User | +  | 3.1 Tool   |   |
|   | (Role/Guardrails) |    | State Memory   |    | Schemas    |   |
|   +-------------------+    +----------------+    +------------+   |
+-------------------------------------------------------------------+
                                 ||
                 Jinja2 Templating / Pydantic Engine
                                 ||
                                 \/
+-------------------------------------------------------------------+
| Compiled Prompt Payload                                           |
|                                                                   |
|  [Cached System Prompt Block]                                     |
|  - Role: Senior Software Architect                                |
|  - Rules: Never invent non-existent APIs                          |
|  - Output: Strict Pydantic v2 JSON Schema                          |
|                                                                   |
|  [Dynamic Context Block]                                          |
|  - User Query & RAG Retrieval Snippets                            |
+-------------------------------------------------------------------+
                                 ||
                                 \/
+-------------------------------------------------------------------+
| LLM Execution & Output Validation                                 |
| - Emits JSON / Tool Calls                                         |
| - Validated via Pydantic v2 Schema                                |
+-------------------------------------------------------------------+
```


## CLI examples



## API examples

The following Python example demonstrates dynamic system prompt construction using Jinja2 templating, compiling agent instructions with system guardrails, and enforcing strict **Pydantic v2** validation on model responses.

```python
import json
from typing import List, Dict, Any
from jinja2 import Template
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Pydantic v2 Output & System Prompt Schema
# ---------------------------------------------------------------------------
class CodeReviewFeedback(BaseModel):
    file_path: str = Field(..., description="Target file path under review")
    issue_type: str = Field(..., description="Classification: 'security', 'bug', 'performance', or 'style'")
    description: str = Field(..., description="Detailed technical issue explanation")
    suggested_fix: str = Field(..., description="Corrected code snippet or remediation")

    @field_validator("issue_type")
    @classmethod
    def validate_type(cls, v: str) -> str:
        allowed = {"security", "bug", "performance", "style"}
        if v.lower() not in allowed:
            raise ValueError(f"issue_type must be one of {allowed}")
        return v.lower()

class SystemPromptConfig(BaseModel):
    role_name: str = Field(..., description="Primary persona identifier")
    domain: str = Field(..., description="Expertise domain")
    rules: List[str] = Field(..., min_items=1, description="Strict negative and operational constraints")
    tools: List[str] = Field(default=[], description="List of accessible MCP tools")

# ---------------------------------------------------------------------------
# System Prompt Templating & Compiler Engine
# ---------------------------------------------------------------------------
SYSTEM_PROMPT_TEMPLATE = """
# ROLE & IDENTITY
You are an expert {{ config.role_name }} specialized in {{ config.domain }}.

# OPERATIONAL RULES & GUARDRAILS
{% for rule in config.rules %}
- {{ rule }}
{% endfor %}

# AVAILABLE TOOLS
{% if config.tools %}
You have access to the following FastMCP 3.1 tools:
{% for tool in config.tools %}
- {{ tool }}
{% endfor %}
{% else %}
No external tools available for this session.
{% endif %}

# OUTPUT FORMAT
You must respond with a valid JSON array of review objects adhering to this schema:
{{ json_schema }}
"""

def compile_system_prompt(config_data: Dict[str, Any]) -> str:
    """Compile dynamic system prompt with rigid guardrails and JSON output schema."""
    config = SystemPromptConfig.model_validate(config_data)
    schema_json = json.dumps(CodeReviewFeedback.model_json_schema(), indent=2)

    template = Template(SYSTEM_PROMPT_TEMPLATE)
    compiled_prompt = template.render(config=config, json_schema=schema_json)
    return compiled_prompt.strip()

if __name__ == "__main__":
    prompt_config = {
        "role_name": "Principal Security Code Auditor",
        "domain": "Python & FastMCP 3.1 Microservices",
        "rules": [
            "Never ignore unhandled exceptions or generic 'except Exception' blocks.",
            "Enforce strict input validation using Pydantic v2 on all public API parameters.",
            "Do not suggest external dependencies outside the standard library or PyPI approved list."
        ],
        "tools": ["vector_search", "static_analyzer", "git_diff_reader"]
    }

    compiled = compile_system_prompt(prompt_config)
    print("=== COMPILED SYSTEM PROMPT ===")
    print(compiled)
    print("\nSystem prompt compiled successfully.")
```


## Related tools / concepts

- **[Agency-Agents](../tools/agents/agency-agents.md)**: Open-source repository of 110+ specialized system prompt personas.
- **[Claude Context Mode](../tools/development_ops/claude-context-mode.md)**: Optimizing system prompt window layouts for Anthropic Claude models.
- **[Inspect AI](../tools/benchmarking/inspect-ai.md)**: Benchmarking framework evaluating system prompt performance across safety suites.


## Sources / references

- [Anthropic System Prompt Engineering Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google Gemini System Instructions Documentation](https://ai.google.dev/gemini-api/docs/system-instructions)



## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

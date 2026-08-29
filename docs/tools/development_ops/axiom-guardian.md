# Axiom Guardian MCP Server

## What it is
An MCP server that implements challenge-based tool call validation using Natural Language Inference (NLI) and formal rule enforcement. Under early January 2027 SOTA standards, **Axiom Guardian v2.0** serves as a zero-trust policy engine integrated with the **FastMCP 3.1 Task Protocol**. It intercepts proposed agent actions across frontier models (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, **Gemma 4**, **DeepSeek-V4**, **Qwen 3.6 VL**) and verifies them against defined operational and security axioms before permitting tool execution.

## What problem it solves
Autonomous AI agents can experience goal drift, hallucinate parameters, or execute high-risk operations in complex production or homelab environments. Axiom Guardian shifts AI safety from passive system prompting ("Try to adhere to safety rules") to active, deterministic middleware enforcement ("Validate every action against formal axioms before tool execution"). If a proposed action contradicts an axiom, execution is halted until explicit justification or human approval is submitted.

## Where it fits in the stack
**Category**: [Development & Ops](index.md) / AI Guardrails & Governance. It functions as an inline safety middleware sitting between LLM tool-calling components (like [Windsurf](windsurf.md), [Claude Code](claude-code.md), or [NanoClaw](nanoclaw.md)) and target execution environments.

## Typical use cases
- **Production Guardrails**: Preventing agents from deleting production databases, modifying firewall rules, or exposing secret keys.
- **Compliance & Governance Audit**: Generating verifiable, signed audit trails of all agent actions and associated reasoning.
- **Human-in-the-Loop Challenge Escalation**: Forcing interactive justification prompts when an agent attempts destructive operations.
- **Dynamic Axiom Enforcement**: Modifying safety policies in real-time across running multi-agent swarms via FastMCP 3.1 endpoints.

## Strengths
- **Native FastMCP 3.1 Task Protocol**: Integrates seamlessly as a standard MCP middleware server with minimal overhead.
- **NLI-Based Contradiction Detection**: Uses high-fidelity NLI classifiers to detect implicit logical violations beyond simple keyword filtering.
- **Verifiable Audit Chains**: Logs every prompt, challenge, and user justification to an immutable append-only ledger.
- **Hot-Reloading Axioms**: Update rule sets dynamically without restarting active agent sessions.

## Limitations
- **Inference Latency Overhead**: Deep NLI checks add 50-150ms per tool invocation.
- **Language Domain**: Optimized primarily for English-language prompt and tool definitions.
- **Context Boundary Limits**: Extremely long multiline tool payloads require context truncation for fast NLI evaluation.

## When to use it
- When granting autonomous AI agents execution permissions over production databases, cloud APIs, or host terminals.
- In compliance-regulated enterprise environments requiring explicit human justification for automated system changes.
- For high-autonomy multi-agent swarms operating with minimal continuous human supervision.

## When not to use it
- In low-stakes local dev environments where safety checks create unnecessary developer friction.
- For high-frequency, sub-millisecond automated data pipelines where 50ms validation latency is unacceptable.
- When tool execution permissions are strictly restricted at the host RBAC layer.

## Getting started

### 1. Installation
```bash
pip install axiom-guardian-mcp
```

### 2. Axiom Definition (`axioms.yaml`)
```yaml
axioms:
  - id: "AXIOM-01"
    rule: "No production database tables may be dropped or truncated without explicit human confirmation."
    severity: "critical"
  - id: "AXIOM-02"
    rule: "All network configuration changes must preserve SSH and VPN access ports."
    severity: "high"
```

### 3. Start FastMCP 3.1 Guardian Server
```bash
AXIOMS_PATH="./axioms.yaml" python -m axiom_guardian_mcp --protocol fastmcp-3.1
```

## CLI examples

```bash
# Test a prompt against active axioms
axiom-guardian check --action "DROP TABLE production_users CASCADE;" --axioms ./axioms.yaml

# Hot-reload axiom configurations
axiom-guardian reload --axioms ./axioms.yaml
```

## API examples

### Programmatic Validation with Pydantic v2
The following Python module demonstrates modeling and validating Axiom Guardian configuration schemas under early January 2027 SOTA standards:

```python
from pydantic import BaseModel, Field
from typing import List
import json

class AxiomRule(BaseModel):
    id: str = Field(..., pattern=r"^AXIOM-[0-9]+$")
    rule: str = Field(..., min_length=10)
    severity: str = Field(default="high", pattern=r"^(critical|high|medium|low)$")

class AxiomGuardianConfig(BaseModel):
    axioms: List[AxiomRule] = Field(..., min_length=1)
    fail_closed: bool = Field(default=True)
    mcp_version: str = Field(default="3.1", pattern=r"^3\.1$")
    nli_endpoint: str = Field(..., pattern=r"^https?://.*$")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "axioms": [
                    {
                        "id": "AXIOM-101",
                        "rule": "The agent must not delete production database clusters.",
                        "severity": "critical"
                    }
                ],
                "fail_closed": True,
                "mcp_version": "3.1",
                "nli_endpoint": "http://localhost:8080/v1/nli"
            }
        }
    }

def validate_axiom_config(payload: dict) -> str:
    """Validates Axiom Guardian policy payload using Pydantic v2."""
    try:
        config = AxiomGuardianConfig.model_validate(payload)
        return json.dumps({
            "status": "success",
            "validated_config": config.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    test_payload = {
        "axioms": [
            {
                "id": "AXIOM-101",
                "rule": "The agent must not delete production database clusters without manual override.",
                "severity": "critical"
            }
        ],
        "fail_closed": True,
        "mcp_version": "3.1",
        "nli_endpoint": "http://localhost:8080/v1/nli"
    }
    print(validate_axiom_config(test_payload))
```

## Related tools / concepts
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Standard tool protocol for AI agents.
- [NanoClaw](nanoclaw.md) — Sandboxed personal assistant runtime.
- [OpenClaw](openclaw.md) — Agentic gateway and tool security framework.
- [Windsurf](windsurf.md) — Agentic IDE with FastMCP 3.1 support.

## Sources / References
- [Axiom Guardian GitHub Repository](https://github.com/democratize-technology/axiom-guardian)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/specification/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

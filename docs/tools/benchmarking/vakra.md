# VAKRA: Executable Benchmark for Enterprise Agents

## What it is
VAKRA (eValuating API and Knowledge Retrieval Agents) is a tool-grounded, executable benchmark designed to evaluate how well AI agents reason and act in enterprise-like environments. Unlike traditional benchmarks that test isolated skills, VAKRA measures **compositional reasoning** across APIs and documents, using full execution traces to assess multi-step workflow completion, fully updated for January 2027 SOTA standards.

## What problem it solves
It addresses the gap between surface-level tool competence and robust, end-to-end agent reliability. VAKRA provides an executable environment with over 8,000 locally hosted APIs across 62 domains, preventing models from relying on memorized outputs and forcing them to navigate real API interactions, multi-hop reasoning, and policy constraints. It solves the "hallucination" problem in tool-use by verifying results against actual databases using the **MCP 3.1** and **FastMCP 3.1** protocols.

## Where it fits in the stack
**Benchmarking / Agent Evaluation**. It is a primary framework for verifying "Agentic Shift" capabilities in production environments. It sits alongside frameworks like [OpenCompass](opencompass.md) but focuses specifically on tool-grounded reasoning for models like [Gemma 4](../ai_knowledge/local_llms.md), Claude 5.6, and GPT-5.6.

## Typical use cases
- **Agent Architecture Validation**: Testing if a new agentic framework (e.g., [OpenClaw](../development_ops/openclaw.md) or [Nanoclaw](../development_ops/nanoclaw.md)) can handle complex multi-step tasks.
- **Model Comparison**: Benchmarking different LLMs ([Gemma 4](../ai_knowledge/local_llms.md) vs GPT-5.6 or Claude 5.6) on their ability to use tools and follow policies.
- **Regression Testing**: Ensuring that updates to an agent's reasoning logic or system prompts don't break existing compositional capabilities.
- **Policy Compliance Auditing**: Verifying that agents strictly adhere to negative constraints (e.g., "Never share user PII").

## Strengths
- **Executable**: Unlike static benchmarks, VAKRA actually runs the tool calls to verify results against persistent databases.
- **Multi-Source Reasoning**: Specifically targets the hard problem of combining structured API data with unstructured document retrieval (RAG).
- **Trajectory-Level Replay**: Replays full agent traces against live tools to support multiple valid execution paths.
- **Deterministic Evaluation**: Locally hosted tools ensure responses are verifiable and consistent across runs.
- **FastMCP 3.1 Support**: Updated to support the latest high-performance Model Context Protocol tool definitions.

## Limitations
- **Environment Complexity**: Requires a complex self-hosted environment to run the 8,000+ mock APIs and persistent databases.
- **Resource Intensive**: Full trajectory replay can be computationally expensive and time-consuming for large-scale benchmarking.
- **Steep Learning Curve**: Configuring custom enterprise domains within VAKRA requires significant effort.

## When to use it
- When evaluating the reliability of AI agents intended for complex enterprise workflows (customer support, business intelligence, compliance).
- To identify specific failure modes in agentic reasoning, such as entity disambiguation or policy interpretation.
- For developers seeking a benchmark that reflects enterprise complexity rather than simple toy tasks.
- When verifying the safety and policy adherence of autonomous agentic loops.

## When not to use it
- For testing basic chat, summarization, or creative writing capabilities.
- If you lack the infrastructure or technical expertise to host the VAKRA executable environment.
- For simple "vibe-checks" of a model's general knowledge.

## Getting started

### Environment Setup
VAKRA requires a containerized environment to host its mock APIs.

```bash
# Clone the repository
git clone https://github.com/IBM/VAKRA.git
cd VAKRA

# Start the executable environment (requires Docker)
docker-compose up -d
```

### Running an Evaluation
Execute a benchmarking run against a target agent:

```bash
# Evaluate an agent running on port 18789
python run_eval.py --agent_url http://localhost:18789 --suite enterprise_composition
```

## CLI examples
VAKRA provides tools for trajectory analysis and environment management:

```bash
# List available domains and APIs
python tools/list_tools.py

# Replay a specific trajectory for debugging
python tools/replay_trajectory.py --trace_id "trace_20261219_001"

# Export evaluation metrics to JSON
python tools/export_metrics.py --run_id "run_456" --format json
```

## API examples
The VAKRA environment can be interacted with via its orchestrator API. This January 2027 SOTA update features strict **Pydantic v2** validation schemas to structure, trigger, and verify agent evaluations.

```python
from pydantic import BaseModel, Field, condecimal
from typing import List, Dict, Optional
from datetime import datetime

# Define strict Pydantic v2 schemas for VAKRA API execution
class VakraTask(BaseModel):
    task_id: str
    prompt: str = Field(..., min_length=10)
    policy_constraint: str = Field(default="PII_REDACTION_STRICT")
    max_steps: int = Field(default=10, ge=1, le=50)

class VakraApiCall(BaseModel):
    api_name: str
    parameters: Dict[str, str]
    execution_status: str = Field(..., pattern="^(SUCCESS|FAILED|TIMEOUT)$")

class VakraEvaluationReport(BaseModel):
    task_id: str
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    model_version: str = Field(..., description="Target model e.g. Claude 5.6 or GPT-5.6")
    api_calls: List[VakraApiCall]
    composition_score: condecimal(ge=0, le=1) = Field(..., description="Task path completion ratio")
    policy_breaches: int = Field(..., ge=0)
    passed: bool

# Programmatic evaluation processor using Pydantic v2
def process_vakra_run(payload: dict) -> VakraEvaluationReport:
    # Validate payload strictly against VAKRA schema
    report = VakraEvaluationReport.model_validate(payload)
    print(f"Validated VAKRA Run: {report.task_id}")
    print(f"Composition score: {report.composition_score * 100}% | Policy breaches: {report.policy_breaches}")
    if report.policy_breaches > 0:
        print("CRITICAL: Policy validation breached!")
    return report

# Mock payload returned from evaluating a GPT-5.6 agent on finance domain
mock_run = {
    "task_id": "vakra_fin_009",
    "model_version": "gpt-5.6-preview",
    "api_calls": [
        {"api_name": "get_account_balance", "parameters": {"acc_id": "998"}, "execution_status": "SUCCESS"},
        {"api_name": "convert_currency", "parameters": {"amount": "500", "to": "EUR"}, "execution_status": "SUCCESS"}
    ],
    "composition_score": 1.0,
    "policy_breaches": 0,
    "passed": True
}

validated_report = process_vakra_run(mock_run)
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — Software engineering benchmark.
- [HumanEval](human-eval.md) — Coding capability benchmark.
- [OpenCompass](opencompass.md) — General model evaluation platform.
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — Design patterns for VAKRA-ready tools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns evaluated by VAKRA.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — The standard for the tools VAKRA evaluates.
- [Gemma 4](../ai_knowledge/local_llms.md) — Local model frequently benchmarked with VAKRA.
- [LiteLLM](../../services/litellm.md) — Used to route model calls during VAKRA runs.
- [SharpAI Security Benchmark](sharp-ai.md) — High-level evaluator for robust agent tool-use security.

## Sources / references
- [IBM VAKRA GitHub](https://github.com/IBM/VAKRA)
- [IBM Newsroom: Introducing VAKRA Benchmark](https://www.ibm.com/new/announcements/introducing-vakra-benchmark)
- [Hugging Face Space: VAKRA Public Leaderboard](https://huggingface.co/spaces/ibm-research/vakra)
- [VAKRA: eValuating API and Knowledge Retrieval Agents (arXiv)](https://arxiv.org/abs/2505.17166)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

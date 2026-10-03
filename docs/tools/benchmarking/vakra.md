# VAKRA: Executable Benchmark for Enterprise Agents

## What it is
**VAKRA** (eValuating API and Knowledge Retrieval Agents) is a tool-grounded, executable benchmark designed to evaluate how well AI agents reason, plan, and act in enterprise-like environments. Unlike traditional benchmarks that test isolated skills or static multiple-choice questions, VAKRA measures **compositional reasoning** across thousands of real-time APIs and unstructured document repositories, using full execution traces to assess multi-step workflow completion under early January 2027 SOTA standards.

VAKRA operates an interactive multi-agent sandbox supporting **FastMCP 3.1** and **MCP 3.1** protocol bridges, allowing benchmark orchestrators to execute live tools against persistent databases, containerized microservices, and simulated third-party enterprise services. It evaluates frontier reasoning models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, and **Gemma 4**.

## What problem it solves
VAKRA addresses the critical gap between surface-level tool competence and robust, end-to-end agent reliability in enterprise production deployments. Traditional benchmarks suffer from three major shortcomings:
1. **Static Output Memorization**: LLMs frequently memorize test dataset answers during pre-training. VAKRA eliminates static leaks by requiring live state mutations in ephemeral target databases.
2. **Disconnected Tool Evaluation**: Single-step tool selection tests fail to capture complex multi-hop dependency chains where tool A's output modifies parameters for tool B and policy constraints dictate tool C's eligibility.
3. **Hallucinated Execution Success**: Static benchmarks grade generated JSON text rather than verifying whether the tool call actually succeeds against a backend API. VAKRA verifies state changes via live database queries.

VAKRA provides an executable environment with over 8,000 locally hosted mock APIs across 62 enterprise domains (e.g., core banking, healthcare EHR, ERP inventory, customer support ticketing, IT service management). It measures trajectory accuracy, parameter hallucination rate, recovery from transient API failures, and strict negative constraint adherence (e.g., "Never expose user PII or execute unapproved wire transfers").

## Where it fits in the stack
**Benchmarking / Agent Evaluation Framework**. VAKRA serves as the primary verification harness for validating agentic frameworks before deploying them into enterprise production environments. It sits alongside general benchmarks like [OpenCompass](opencompass.md) and code evaluators like [SWE-bench](swe-bench.md), but focuses specifically on compositional tool reasoning and policy compliance.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        VAKRA BENCHMARK HARNESS                         │
│                                                                        │
│  ┌───────────────────────────┐         ┌────────────────────────────┐  │
│  │   Task Scenario Generator │         │  Trajectory Replay Engine  │  │
│  │  (62 Enterprise Domains)  │         │  (Trace Collector & Audit) │  │
│  └─────────────┬─────────────┘         └─────────────┬──────────────┘  │
│                │                                     │                 │
│                ▼                                     ▼                 │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                   FastMCP 3.1 Gateway Router                     │  │
│  └──────┬──────────────────────┬──────────────────────┬─────────────┘  │
└─────────┼──────────────────────┼──────────────────────┼────────────────┘
          │                      │                      │
          ▼                      ▼                      ▼
┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐
│ Mock Enterprise   │  │ Vector Store /    │  │ Target Agent      │
│ APIs (8,000+ Endpts) │ RAG Document DB    │  │ (Claude 5.6/GPT5) │
└───────────────────┘  └───────────────────┘  └───────────────────┘
```

## Typical use cases
- **Agent Architecture Validation**: Testing whether a new agentic framework (e.g., [OpenClaw](../development_ops/openclaw.md), [Nanoclaw](../development_ops/nanoclaw.md), or [Smolagents](../frameworks/smolagents.md)) can execute complex multi-step workflows without entering infinite retry loops.
- **Model Selection & Comparison**: Benchmarking different LLMs ([Gemma 4](../ai_knowledge/local_llms.md) vs GPT-5.6 or Claude 5.6) on tool parameter accuracy, latency, and token efficiency.
- **Regression Testing in CI/CD**: Running automated VAKRA suites on every pull request to ensure prompt updates or agent graph refactors don't break enterprise workflows.
- **Policy Compliance Auditing**: Verifying that agents strictly adhere to negative constraints (e.g., refusing to bypass approval workflows or redact sensitive financial fields).
- **FastMCP 3.1 Tool Server Verification**: Testing custom enterprise MCP servers to ensure tool schema descriptions are unambiguously interpreted by target LLMs.

## Strengths
- **Fully Executable Sandbox**: Executes real tool calls against persistent containerized databases and API mocks rather than grading static text outputs.
- **Compositional Multi-Hop Tasks**: Mandates combining structured API interactions with unstructured document retrieval (V-RAG and textual RAG).
- **Trajectory-Level Replay**: Captures full execution traces, allowing deterministic playback and fine-grained error taxonomy analysis (e.g., schema violation vs logic error).
- **Deterministic & Air-Gapped**: Locally hosted mock APIs eliminate external API dependencies, network jitter, and third-party rate limits.
- **FastMCP 3.1 Native Integration**: Out-of-the-box support for the latest Model Context Protocol tool definitions and streaming responses.
- **Policy Breach Detection**: Explicitly tracks policy violations alongside task completion scores to quantify agent risk profiles.

## Limitations
- **Infrastructure Overhead**: Running the full 8,000+ API mock environment requires container orchestration (Docker Compose or Kubernetes) with significant RAM/CPU capacity.
- **Trajectory Evaluation Time**: Full multi-step execution traces take considerably longer to evaluate than static benchmark single-turn prompts.
- **Domain Adaptation Effort**: Customizing VAKRA scenarios for proprietary, non-standard enterprise APIs requires writing custom mock handlers and verification state checkers.

## When to use it
- When evaluating the operational safety and accuracy of AI agents built for enterprise workflows.
- To identify specific failure modes in agentic reasoning, such as entity disambiguation, tool call ordering, or policy interpretation.
- For AI engineering teams seeking an automated, reproducible benchmark that mirrors enterprise complexity rather than toy tasks.
- When verifying that agentic loops comply with strict security and privacy standards before going live.

## When not to use it
- For testing general chat, open-ended summarization, or creative writing capabilities.
- If you lack containerized testing infrastructure or technical bandwidth to run executable benchmarks.
- For rapid "vibe-checks" during initial prompt prototyping where light interactive testing suffices.

## Getting started

### Environment Setup
VAKRA requires a containerized environment to host its mock APIs and persistent state stores.

```bash
# Clone the official repository
git clone https://github.com/IBM/VAKRA.git
cd VAKRA

# Launch the executable benchmark environment via Docker Compose
docker compose -f docker-compose.yml up -d

# Verify all mock API containers and FastMCP gateways are healthy
python3 scripts/health_check.py
```

### Running an Evaluation Suite
Execute a benchmarking run against a target agent endpoint:

```bash
# Benchmark an agent running on port 18789 across the finance domain
python3 run_eval.py \
  --agent_url http://localhost:18789 \
  --suite enterprise_finance_composition \
  --mcp_protocol fastmcp_3.1 \
  --max_steps 20 \
  --output_dir ./reports/run_001
```

## CLI examples
VAKRA provides command-line utilities for managing test suites, inspecting trajectory logs, and exporting compliance analytics:

```bash
# List available domains, mock APIs, and scenario suites
python3 tools/list_tools.py --domain healthcare

# Replay a specific execution trajectory for deep debugging
python3 tools/replay_trajectory.py --trace_id "trace_20270107_fin_8821" --verbose

# Export comprehensive evaluation metrics and policy breach logs to JSON
python3 tools/export_metrics.py --run_id "run_fin_20270107" --format json --out report.json
```

## API examples

### FastMCP 3.1 VAKRA Benchmark Harness Server
The following Python module demonstrates hosting a FastMCP 3.1 server that exposes VAKRA evaluation harnesses and execution replay utilities programmatically:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import json
import uuid

# Initialize FastMCP 3.1 server for VAKRA evaluation harness
mcp = FastMCP(
    "VAKRA Benchmark Harness",
    instructions="Provides programmatic execution and auditing for VAKRA enterprise agent benchmarks."
)

class EvaluationRequest(BaseModel):
    agent_endpoint: str = Field(..., description="Target agent URL or FastMCP endpoint")
    domain_suite: str = Field(default="enterprise_composition", description="Target domain scenario suite")
    model_identifier: str = Field(..., description="Model under test e.g. claude-5.6-sonnet or gpt-5.6")
    max_steps_per_task: int = Field(default=15, ge=1, le=50)
    strict_policy_check: bool = Field(default=True)

class ApiCallRecord(BaseModel):
    tool_name: str
    parameters: Dict[str, str]
    execution_status: str = Field(..., pattern="^(SUCCESS|FAILED|POLICY_VIOLATION)$")
    response_bytes: int = Field(default=0)

class TrajectoryReport(BaseModel):
    task_id: str
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    model_identifier: str
    api_calls: List[ApiCallRecord]
    composition_score: float = Field(..., ge=0.0, le=1.0)
    policy_breaches: int = Field(default=0, ge=0)
    passed: bool

@mcp.tool(name="run_vakra_task")
def run_vakra_task(request: EvaluationRequest) -> TrajectoryReport:
    """Executes a single VAKRA scenario task against target agent endpoint and evaluates state mutations."""
    # Simulated execution trace verification for demonstration
    mock_calls = [
        ApiCallRecord(
            tool_name="get_customer_account",
            parameters={"account_id": "ACC-9921"},
            execution_status="SUCCESS",
            response_bytes=412
        ),
        ApiCallRecord(
            tool_name="transfer_funds",
            parameters={"from_acc": "ACC-9921", "to_acc": "ACC-4412", "amount": "150.00"},
            execution_status="SUCCESS",
            response_bytes=180
        )
    ]

    return TrajectoryReport(
        task_id="vakra_fin_trans_001",
        model_identifier=request.model_identifier,
        api_calls=mock_calls,
        composition_score=1.0,
        policy_breaches=0,
        passed=True
    )

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Evaluation Processor using Pydantic v2
The following Python script illustrates parsing, validating, and reporting VAKRA trajectory payloads strictly utilizing Pydantic v2 schemas:

```python
from pydantic import BaseModel, Field, condecimal, field_validator
from typing import List, Dict, Optional
from datetime import datetime

class VakraApiCall(BaseModel):
    api_name: str = Field(..., min_length=1)
    parameters: Dict[str, str] = Field(default_factory=dict)
    execution_status: str = Field(..., pattern="^(SUCCESS|FAILED|TIMEOUT|POLICY_VIOLATION)$")
    execution_time_ms: float = Field(..., ge=0.0)

class VakraEvaluationReport(BaseModel):
    task_id: str = Field(..., min_length=1)
    run_id: str = Field(..., min_length=1)
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    model_version: str = Field(..., description="Target model e.g. Claude 5.6 or GPT-5.6")
    api_calls: List[VakraApiCall] = Field(default_factory=list)
    composition_score: float = Field(..., ge=0.0, le=1.0, description="Task path completion ratio")
    policy_breaches: int = Field(..., ge=0)
    passed: bool

    @field_validator("passed")
    @classmethod
    def validate_passed_status(cls, v: bool, info) -> bool:
        # Strict rule: passed cannot be True if composition_score < 1.0 or policy_breaches > 0
        score = info.data.get("composition_score", 0.0)
        breaches = info.data.get("policy_breaches", 1)
        if v and (score < 1.0 or breaches > 0):
            raise ValueError("Task cannot be marked passed if score < 1.0 or policy breaches > 0")
        return v

def process_vakra_run(payload: dict) -> VakraEvaluationReport:
    """Validates raw execution report dictionary against strict Pydantic v2 schema."""
    report = VakraEvaluationReport.model_validate(payload)
    print(f"Validated VAKRA Run: {report.task_id} (Run ID: {report.run_id})")
    print(f"Model: {report.model_version} | Composition Score: {report.composition_score * 100:.1f}%")
    print(f"Total API Calls: {len(report.api_calls)} | Policy Breaches: {report.policy_breaches}")
    return report

if __name__ == "__main__":
    mock_payload = {
        "task_id": "vakra_fin_009",
        "run_id": "run_88192_eval",
        "model_version": "claude-5.6-sonnet",
        "api_calls": [
            {
                "api_name": "get_account_balance",
                "parameters": {"acc_id": "998"},
                "execution_status": "SUCCESS",
                "execution_time_ms": 142.5
            },
            {
                "api_name": "convert_currency",
                "parameters": {"amount": "500", "to": "EUR"},
                "execution_status": "SUCCESS",
                "execution_time_ms": 98.2
            }
        ],
        "composition_score": 1.0,
        "policy_breaches": 0,
        "passed": True
    }

    report = process_vakra_run(mock_payload)
    print("Schema validation successful!")
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — Software engineering benchmark for repository modifications.
- [HumanEval](human-eval.md) — Fundamental coding capability benchmark.
- [OpenCompass](opencompass.md) — Comprehensive model evaluation platform.
- [Agent Skills Best Practices](../../knowledge_base/patterns/skills-best-practices.md) — Design patterns for VAKRA-compliant tools.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Multi-agent orchestration patterns evaluated by VAKRA.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Tool protocol standard evaluated by VAKRA.
- [Gemma 4](../ai_knowledge/local_llms.md) — Frontier local model evaluated with VAKRA.
- [LiteLLM](../../services/litellm.md) — Model proxy router used in VAKRA test harnesses.
- [SharpAI Security Benchmark](sharp-ai.md) — Security benchmark for multi-agent tool access safety.

## Sources / references
- [IBM VAKRA GitHub Repository](https://github.com/IBM/VAKRA)
- [IBM Research: Introducing VAKRA Benchmark](https://www.ibm.com/new/announcements/introducing-vakra-benchmark)
- [Hugging Face Space: VAKRA Public Leaderboard](https://huggingface.co/spaces/ibm-research/vakra)
- [VAKRA: eValuating API and Knowledge Retrieval Agents (arXiv Paper)](https://arxiv.org/abs/2505.17166)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

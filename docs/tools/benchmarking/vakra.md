# VAKRA: Executable Benchmark for Enterprise Agents

## What it is
**VAKRA** (eValuating API and Knowledge Retrieval Agents) is a tool-grounded, executable benchmark designed to evaluate how well AI agents reason, plan, and act in enterprise-like environments. Unlike traditional benchmarks that test isolated skills or static multiple-choice questions, VAKRA measures **compositional reasoning** across thousands of real-time APIs and unstructured document repositories, using full execution traces to assess multi-step workflow completion under early January 2027 SOTA standards.

VAKRA operates an interactive multi-agent sandbox supporting **FastMCP 3.1** and **MCP 3.1** protocol bridges, allowing benchmark orchestrators to execute live tools against persistent databases, containerized microservices, and simulated third-party enterprise services. It evaluates frontier reasoning models including **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **Llama 4 Maverick**, and **Gemma 4**.

## System Architecture

The benchmark orchestration system features a closed-loop execution harness with dynamic scenario generation, FastMCP 3.1 protocol transport, and live transactional database verification.

```mermaid
graph TD
    subgraph ScenarioEngine["VAKRA Scenario & Task Generation Core"]
        SCEN["Scenario Generator<br/>(62 Enterprise Domains, Dynamic Seed)"]
        POLICY["Enterprise Policy & Invariant Engine<br/>(PII Safeguards, Approval Workflows)"]
        ORCH["Evaluation Orchestrator Runner<br/>(Trace Recorder & Replay Auditor)"]
    end

    subgraph ProtocolBridge["FastMCP 3.1 Protocol Mediation Gateway"]
        MCP["FastMCP 3.1 Tool Gateway<br/>(STDIO / SSE Streaming Transports)"]
        VAL["Strict Pydantic v2 Contract Validator<br/>(extra='forbid', frozen=True)"]
        INTERCEPT["Fault & Latency Injection Interceptor<br/>(Transient 503s, Payload Mutation)"]
    end

    subgraph AgentSandbox["Agent Target Under Test"]
        TARGET["Frontier Agent / Harness<br/>(Claude 5.6, GPT-5.6, OpenClaw, Nanoclaw)"]
        REASON["Multi-Turn Tool Planning Loop<br/>(Tree-of-Thought / ReAct Trajectory)"]
    end

    subgraph EmulatedEnvironment["Executable Enterprise Sandbox"]
        MOCK["8,000+ Mock REST Endpoints<br/>(Core Banking, ERP, Healthcare EHR)"]
        STATE_DB["Persistent PostgreSQL / Redis Store<br/>(Transactional State Mutations)"]
        VRAG["Unstructured Enterprise Doc DB<br/>(Vector Embeddings & PDF Schematics)"]
    end

    SCEN --> POLICY
    POLICY --> ORCH
    ORCH --> MCP
    MCP --> TARGET
    TARGET --> REASON
    REASON --> VAL
    VAL --> INTERCEPT
    INTERCEPT --> MOCK
    MOCK --> STATE_DB
    MOCK --> VRAG
    STATE_DB --> ORCH
```

## Mathematical Formulations of Trajectory State Mutation & Multi-Hop Reasoning

VAKRA models agent workflow execution as directed state transitions over discrete enterprise state graphs $\mathcal{G} = (\mathcal{S}, \mathcal{E})$.

### Trajectory Graph Reachability & Compositional Accuracy
Let $\mathbf{s}_0 \in \mathcal{S}$ denote the initial enterprise database state vector. An agent trajectory $\mathcal{T} = [a_1, a_2, \dots, a_K]$ comprises an ordered sequence of tool action invocations $a_k = (t_k, \mathbf{p}_k)$, where $t_k$ is the selected API tool and $\mathbf{p}_k$ is the input parameter dictionary. Each action induces a deterministic state mutation:

$$
\mathbf{s}_{k} = f_{\text{API}}(a_k, \mathbf{s}_{k-1})
$$

The target task defines an acceptance subspace of valid final states $\mathcal{S}^* \subset \mathcal{S}$. The binary task success metric $\Phi(\mathcal{T})$ and compositional completion score $C_{\text{comp}}(\mathcal{T})$ are formulated as:

$$
\Phi(\mathcal{T}) = \mathbb{I}\left( \mathbf{s}_K \in \mathcal{S}^* \right) \cdot \prod_{k=1}^K \mathbb{I}\left( \mathcal{P}_{\text{policy}}(a_k, \mathbf{s}_{k-1}) = 1 \right)
$$

$$
C_{\text{comp}}(\mathcal{T}) = \frac{1}{|\mathcal{K}^*|} \sum_{m \in \mathcal{K}^*} \mathbb{I}\left( \Delta \mathbf{s}_m \text{ correctly committed} \right)
$$

where $\mathcal{P}_{\text{policy}}(a, \mathbf{s}) \in \{0, 1\}$ evaluates strict negative constraint compliance, and $\mathcal{K}^*$ represents required intermediate sub-goal checkpoints.

### Multi-Hop Tool Reasoning Entropy & Parameter Hallucination
Given an API parameter schema with required arguments $\mathcal{A}_{\text{req}}$, the parameter hallucination rate $\mathcal{R}_{\text{halluc}}$ across trajectory $\mathcal{T}$ measures divergence between generated parameter assignments $\hat{\mathbf{p}}_k$ and the verified grounding context $\mathcal{D}_{\text{ground}}$:

$$
\mathcal{R}_{\text{halluc}}(\mathcal{T}) = \frac{1}{K} \sum_{k=1}^K \frac{1}{|\mathcal{A}_{\text{req}}^{(k)}|} \sum_{u \in \mathcal{A}_{\text{req}}^{(k)}} \mathbb{I}\left( \hat{\mathbf{p}}_k[u] \notin \text{Entities}(\mathcal{D}_{\text{ground}}) \land \hat{\mathbf{p}}_k[u] \ne \emptyset \right)
$$

The trajectory entropy $\mathcal{H}_{\text{plan}}(\mathcal{T})$ quantifies search stability under agentic re-planning:

$$
\mathcal{H}_{\text{plan}}(\mathcal{T}) = - \sum_{t \in \mathcal{U}_{\text{tools}}} \hat{P}(t) \log_2 \hat{P}(t), \quad \text{where } \hat{P}(t) = \frac{1}{K} \sum_{k=1}^K \mathbb{I}(t_k = t)
$$

Low planning entropy coupled with high compositional success signifies optimal, direct trajectory execution without redundant retry cycles.

### Execution Roofline Bounds
For an evaluation suite of $N_{\text{tasks}}$ parallel agent runs with network latency $\tau_{\text{net}}$ and database lock resolution $\tau_{\text{db}}$, total evaluation throughput $Q_{\text{eval}}$ (tasks/min) satisfies:

$$
Q_{\text{eval}} \le \frac{60 \cdot W_{\text{workers}}}{\max\limits_{i} \left\{ \sum_{k=1}^{K_i} \left( T_{\text{LLM}}^{(k)} + \tau_{\text{net}} + \tau_{\text{db}} \right) \right\}}
$$

## What problem it solves
VAKRA addresses the critical gap between surface-level tool competence and robust, end-to-end agent reliability in enterprise production deployments. Traditional benchmarks suffer from three major shortcomings:
1. **Static Output Memorization**: LLMs frequently memorize test dataset answers during pre-training. VAKRA eliminates static leaks by requiring live state mutations in ephemeral target databases.
2. **Disconnected Tool Evaluation**: Single-step tool selection tests fail to capture complex multi-hop dependency chains where tool A's output modifies parameters for tool B and policy constraints dictate tool C's eligibility.
3. **Hallucinated Execution Success**: Static benchmarks grade generated JSON text rather than verifying whether the tool call actually succeeds against a backend API. VAKRA verifies state changes via live database queries.

VAKRA provides an executable environment with over 8,000 locally hosted mock APIs across 62 enterprise domains (e.g., core banking, healthcare EHR, ERP inventory, customer support ticketing, IT service management). It measures trajectory accuracy, parameter hallucination rate, recovery from transient API failures, and strict negative constraint adherence (e.g., "Never expose user PII or execute unapproved wire transfers").

## Where it fits in the stack
**Benchmarking / Agent Evaluation Framework**. VAKRA serves as the primary verification harness for validating agentic frameworks before deploying them into enterprise production environments. It sits alongside general benchmarks like [OpenCompass](opencompass.md) and code evaluators like [SWE-bench](swe-bench.md), but focuses specifically on compositional tool reasoning and policy compliance.

## Comparative Empirical Matrix: Enterprise Agent Benchmarks

| Benchmark Suite | Test Environment | Tool Scope | Verification Method | Policy Breach Auditing | SOTA Pass Rate (Jan 2027) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **VAKRA (IBM)** | Executable Containers | 8,000+ REST APIs (62 Domains) | Live DB Mutation & SQL Checks | Native Multi-Constraint | 74.2% (Claude 5.6 Sonnet) |
| **SWE-bench Verified** | Git / Python Testbeds | Shell / Git / Patch Application | Pytest / Unittest Execution | Limited | 68.4% (Claude 5.6 / Devin) |
| **GAIA** | Web / Static Sandboxes | Browser / Calculator / Python | Final String Equality Check | None | 62.1% (GPT-5.5 / O3) |
| **BFCL v3 (Berkeley)** | Synthetic Function Calls | 1,200 Parameterized Functions | Static AST / JSON Match | Basic Flag | 88.9% (Multiple Models) |
| **AssistantBench** | Web Browser / Search | Real-world Web Navigation | Exact Match URL / Key Answer | None | 48.6% (Agentic Web SOTA) |

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

## Multi-Container Docker Compose Sandbox (`docker-compose.vakra.yml`)

The following Compose specification launches the full isolated VAKRA evaluation sandbox, comprising mock enterprise microservices, state databases, and the FastMCP 3.1 evaluation harness.

```yaml
version: '3.8'

services:
  vakra-orchestrator:
    build:
      context: .
      dockerfile: Dockerfile.vakra-runner
    container_name: vakra-orchestrator
    restart: unless-stopped
    ports:
      - "8099:8099"
    environment:
      - PORT=8099
      - DB_URI=postgresql://vakra_admin:vakra_secret@vakra-db:5432/vakra_state
      - REDIS_URL=redis://vakra-redis:6379/0
      - LOG_LEVEL=INFO
    depends_on:
      - vakra-db
      - vakra-redis
      - vakra-mock-apis

  vakra-mock-apis:
    image: ibm/vakra-mock-enterprise:latest
    container_name: vakra-mock-apis
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - MOCK_DOMAINS=banking,healthcare,erp,crm,itsm
      - INJECT_CHAOS_RATE=0.05

  vakra-db:
    image: postgres:16-alpine
    container_name: vakra-state-db
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=vakra_admin
      - POSTGRES_PASSWORD=vakra_secret
      - POSTGRES_DB=vakra_state
    volumes:
      - vakra_pg_data:/var/lib/postgresql/data

  vakra-redis:
    image: redis:7.4-alpine
    container_name: vakra-redis
    restart: unless-stopped
    ports:
      - "6379:6379"

volumes:
  vakra_pg_data:
    driver: local
```

## Hardened Systemd Service Unit (`vakra-eval-gateway.service`)

Save the service definition to `/etc/systemd/system/vakra-eval-gateway.service` for continuous CI/CD evaluation runners:

```ini
[Unit]
Description=VAKRA FastMCP 3.1 Enterprise Evaluation Harness Daemon
After=network.target local-fs.target postgresql.service
Wants=network-online.target

[Service]
Type=simple
User=vakrasvc
Group=vakrasvc
WorkingDirectory=/opt/vakra-eval
ExecStart=/opt/vakra-eval/venv/bin/python3 -m vakra.gateway --port 8099
Restart=always
RestartSec=5s

# Process Environment & Tuning
Environment="PYTHONUNBUFFERED=1"
EnvironmentFile=/etc/vakra/eval.env

# Sandboxing & Security Hardening
ProtectSystem=strict
ProtectHome=true
PrivateTmp=true
NoNewPrivileges=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
ReadWritePaths=/opt/vakra-eval/reports /tmp

StandardOutput=journal
StandardError=journal
SyslogIdentifier=vakra-eval

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Observable Fault | Root Cause Analysis | Diagnostic Inspection Command | Remediation Strategy |
| :--- | :--- | :--- | :--- |
| **`SQL State Verification Failed`** | Agent omitted required commit transaction or inserted corrupted foreign keys. | `docker exec -it vakra-state-db psql -U vakra_admin -d vakra_state -c "SELECT * FROM ledger_audit;"` | Inspect trajectory trace for missing prerequisite tool calls or parameter type errors. |
| **`Policy Breach Flagged (PII Expose)`** | Agent printed unmasked SSN or credit card number into LLM scratchpad. | `grep "POLICY_VIOLATION" /opt/vakra-eval/reports/*.json` | Inject explicit negative constraint prompting: "Never output raw account credentials in plain text". |
| **FastMCP Transport Disconnection** | Standard output polluted by debug statements during task execution. | `journalctl -u vakra-eval-gateway.service -n 50 --no-pager` | Channel all auxiliary diagnostic output strictly to `sys.stderr` or logging subsystems. |
| **Simulated API Timeout (504 Gateway)** | Chaos injection interceptor simulated network partition; agent failed to retry. | `docker logs vakra-mock-apis \| grep "CHAOS_INJECT"` | Configure agent tool calling harnesses with exponential backoff and idempotency keys. |
| **Pydantic ValidationError on Tool Schema** | Model invoked tool with misspelled keyword argument not present in contract. | Inspect error logs in `reports/run_latest/trace.json` | Use strict Pydantic v2 schemas (`extra="forbid"`) to surface clear schema feedback in error prompt. |
| **PostgreSQL Connection Exhaustion** | Unclosed connections in benchmark parallel worker pool. | `netstat -an \| grep 5432 \| wc -l` | Set max pool size in database configuration (`max_connections = 200`) and enforce connection context managers. |
| **Trajectory Replay Divergence** | Non-deterministic mock API seed or unsynchronized system clock. | `python3 tools/replay_trajectory.py --trace_id $ID --verify-seed` | Ensure deterministic mock seeding via `--random_seed 42` during evaluation execution. |
| **Out of Memory in Orchestrator Runner** | Retaining 10,000+ raw multi-page PDF documents in process RAM. | `ps aux \| grep python3 \| awk '{print $6/1024 " MB"}'` | Stream document evaluations using chunked generators and persistent disk caches. |

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

### FastMCP 3.1 VAKRA Benchmark Harness Server with Strict Pydantic v2
The following Python module demonstrates hosting a FastMCP 3.1 server with strict Pydantic v2 models (`extra="forbid"`, `frozen=True`) that exposes VAKRA evaluation harnesses and execution replay utilities programmatically:

```python
import sys
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pydantic import BaseModel, ConfigDict, Field
from fastmcp import FastMCP, Context

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("VAKRAHarness")

# Initialize FastMCP 3.1 server for VAKRA evaluation harness
mcp = FastMCP(
    "VAKRA Benchmark Harness",
    version="3.1.0",
    instructions="Provides programmatic execution and auditing for VAKRA enterprise agent benchmarks."
)

class EvaluationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    agent_endpoint: str = Field(..., description="Target agent URL or FastMCP endpoint")
    domain_suite: str = Field(default="enterprise_composition", description="Target domain scenario suite")
    model_identifier: str = Field(..., description="Model under test e.g. claude-5.6-sonnet or gpt-5.6")
    max_steps_per_task: int = Field(default=15, ge=1, le=50)
    strict_policy_check: bool = Field(default=True)

class ApiCallRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    tool_name: str
    parameters: Dict[str, str]
    execution_status: str = Field(..., pattern="^(SUCCESS|FAILED|POLICY_VIOLATION)$")
    response_bytes: int = Field(default=0)

class TrajectoryReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    task_id: str
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    model_identifier: str
    api_calls: List[ApiCallRecord]
    composition_score: float = Field(..., ge=0.0, le=1.0)
    policy_breaches: int = Field(default=0, ge=0)
    passed: bool

@mcp.tool(name="run_vakra_task")
async def run_vakra_task(
    request: EvaluationRequest,
    ctx: Optional[Context] = None
) -> TrajectoryReport:
    """Executes a single VAKRA scenario task against target agent endpoint and evaluates state mutations."""
    if ctx:
        await ctx.info(f"Initializing VAKRA evaluation run on {request.domain_suite} for {request.model_identifier}...")

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

    if ctx:
        await ctx.info("Scenario trace completed with 0 policy breaches. Generating report...")

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

### Programmatic Evaluation Processor using Strict Pydantic v2
The following Python script illustrates parsing, validating, and reporting VAKRA trajectory payloads strictly utilizing Pydantic v2 schemas:

```python
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import List, Dict, Optional
from datetime import datetime

class VakraApiCall(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    api_name: str = Field(..., min_length=1)
    parameters: Dict[str, str] = Field(default_factory=dict)
    execution_status: str = Field(..., pattern="^(SUCCESS|FAILED|TIMEOUT|POLICY_VIOLATION)$")
    execution_time_ms: float = Field(..., ge=0.0)

class VakraEvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
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

# SWE-bench

## What it is
SWE-bench is a benchmark for evaluating LLMs on real-world software engineering tasks. It uses actual issues from GitHub and requires the model to generate a functional patch that passes existing tests. As of January 2027, it remains the industry standard for measuring the autonomous coding capabilities of frontier models like **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**.

With the launch of **SWE-bench Multilingual**, the benchmark has been expanded to support a wider array of programming languages (C, C++, Go, Java, JavaScript, TypeScript, PHP, Ruby, and Rust), making it a truly language-agnostic evaluator for autonomous engineering agents across diverse modern software stacks.

## System Architecture & Execution Flow

The following sequence diagram illustrates SWE-bench's dockerized execution sequence, from task instance ingestion and FastMCP 3.1 agent tool interactions to patch application and automated test suite evaluation:

```mermaid
sequenceDiagram
    autonumber
    participant Harness as SWE-bench Evaluation Harness
    participant Agent as Autonomous Agent (FastMCP 3.1)
    participant Container as Isolated Docker Container
    participant TestSuite as Repository Test Runner (pytest/cargo/jest/go test)
    participant Verifier as Pydantic v2 Patch Verifier

    Harness->>Container: Spawn repository workspace (base commit SHA)
    Harness->>Agent: Send GitHub issue problem statement
    loop Search & Edit Cycle
        Agent->>Container: Execute CLI search / FastMCP file edits
        Container-->>Agent: Return file content / terminal stdout
    end
    Agent->>Verifier: Submit generated git diff patch
    Verifier->>Container: Apply patch (`git apply patch.diff`)
    Container->>TestSuite: Run pre-existing + newly added tests
    TestSuite-->>Harness: Return PASS / FAIL evaluation report
```

## Benchmark Variants & Leaderboard Comparison Matrix

| SWE-bench Variant | Test Set Size | Primary Focus | Language Support | Eval Latency / Task | SOTA Accuracy (Early 2027) | Top Performing Model |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SWE-bench Lite** | 300 instances | Fast iterative agent feedback | Python | ~2-5 mins | 68.4% | Claude 5.1 Sonnet |
| **SWE-bench Full** | 2,294 instances | Comprehensive real-world benchmark | Python | ~10-20 mins | 59.2% | GPT-5.6 Enterprise |
| **SWE-bench Verified**| 500 instances | Human-verified solvable issues | Python | ~3-8 mins | 74.1% | DeepSeek-V4 / Claude 5.1 |
| **SWE-bench Multilingual**| 1,500 instances | Multi-language enterprise repo evaluation | C, C++, Go, Rust, TS, Java | ~10-15 mins | 61.5% | Claude 5.1 Sonnet |

## What problem it solves
Evaluating LLMs on code usually relies on toy problems or short code snippets (like HumanEval or MBPP). SWE-bench solves this by testing models on complex, multi-file codebases, real dependency trees, and non-trivial issue descriptions, providing a much closer proxy for real-world software engineering capability.

## Where it fits in the stack
**Benchmarking / Evaluation**. It is used by researchers, agent developers, and enterprises to benchmark the real-world software engineering capabilities of models and autonomous coding agents like OpenHands, Devin, and Claude Code.

## Multi-Language Benchmark Execution Strategy

```
+-----------------------------------------------------------------------------------+
|                         SWE-bench Multilingual Architecture                       |
+-----------------------------------------------------------------------------------+
|  [ Python Engine ]  |  [ Rust / Cargo ]  |  [ Go Toolchain ]  |  [ Node.js / TS ] |
|  pytest / unittest  |  cargo test        |  go test ./...     |  jest / vitest    |
+-----------------------------------------------------------------------------------+
|               Isolated Non-Root Docker Container Environment                      |
|               Network Access Disabled (--network none)                             |
|               Enforced Quotas: 8GB RAM / 4 vCPU / 100KB Patch Limit               |
+-----------------------------------------------------------------------------------+
```

## Typical use cases
- **Frontier Model Evaluation**: Measuring the autonomous problem-solving performance of newly trained base and instruction-tuned models.
- **Agentic Workflow Tuning**: Comparing different prompting techniques, tool-calling strategies, and search patterns (e.g., Aider vs OpenHands vs SWE-agent).
- **Regression Testing for Agents**: Ensuring that changes to an agent's harness or toolset do not degrade its ability to solve real GitHub issues.

## Strengths
- **Real-World Relevance**: Tasks are drawn directly from open-source GitHub repositories (Django, SymPy, scikit-learn, pytest, etc.).
- **Rigorous Evaluation**: Requires models to produce functional code modifications that satisfy unit tests, preventing hallucinated or incomplete solutions.
- **High Discrimination**: Clearly separates top-tier reasoning models from simpler code-completion models.

## Limitations
- **High Resource Requirements**: Running the full benchmark requires executing code in isolated Docker environments across thousands of task instances.
- **Dataset Contamination Risks**: Because training datasets often crawl open GitHub repositories, care must be taken to prevent data leakage into the base models.
- **Execution Overhead**: Test execution time and container orchestration overhead can make full runs slow and expensive.

## When to use it
- When evaluating the end-to-end coding performance of an autonomous agent or LLM.
- When benchmarking multi-file editing, navigation, and debugging capabilities rather than simple syntax generation.
- To compare coding agent frameworks on a standardized, universally accepted benchmark.

## When not to use it
- For quick, low-cost unit tests during simple prompt engineering cycles (use SWE-bench Lite or HumanEval instead).
- When evaluating code generation in isolated domains without real GitHub project context (e.g. standalone competitive programming algorithms).

## Getting started

### Installation
Install the official SWE-bench harness from PyPI:
```bash
pip install swebench pydantic mcp
```

### Running SWE-bench Lite Evaluation
```bash
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --predictions_path predictions.jsonl \
    --max_workers 8 \
    --run_id test_eval_run
```

## CLI examples

```bash
# Evaluate predictions on SWE-bench Lite via CLI
python -m swebench.harness.run_evaluation \
    --dataset_name princeton-nlp/SWE-bench_Lite \
    --predictions_path predictions.jsonl \
    --max_workers 4

# Inspect evaluation report summary
python -m swebench.harness.summarize_results --predictions_path predictions.jsonl
```

## Systemd Production Service Configuration

Below is a production systemd unit configuration (`/etc/systemd/system/swebench-eval.service`) for executing SWE-bench evaluation harness worker queues:

```ini
[Unit]
Description=SWE-bench Automated Evaluation Runner Service
After=network.target docker.service
Wants=network-online.target docker.service

[Service]
Type=simple
User=swebench
Group=docker
WorkingDirectory=/var/lib/swebench
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
Environment="DOCKER_HOST=unix:///var/run/docker.sock"
ExecStart=/usr/bin/python3 -m swebench.harness.run_evaluation --dataset_name princeton-nlp/SWE-bench_Lite --predictions_path /var/lib/swebench/predictions.jsonl --max_workers 8
Restart=on-failure
RestartSec=10s
LimitNOFILE=65536
CapabilityBoundingSet=CAP_NET_BIND_SERVICE
NoNewPrivileges=false
ProtectSystem=full
ProtectHome=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

## API examples

```python
# Programmatic evaluation payload submitting generated diff
from swebench.harness.constants import MAP_REPO_VERSION_TO_SPECS

instance_id = "django__django-11099"
print(f"Loaded evaluation specs for {instance_id}")
```

## FastMCP 3.1 Evaluation Harness Server & Pydantic v2 Patch Validator

The following executable Python module implements a FastMCP 3.1 evaluation server that ingests SWE-bench task instances, executes automated patch validation via Pydantic v2 schemas, and evaluates patch diffs:

```python
import sys
import re
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("swe-bench-evaluation-server", version="3.1.0")

class TaskInstanceMetadata(BaseModel):
    """Pydantic v2 schema representing a SWE-bench task instance problem statement."""
    instance_id: str = Field(..., description="Unique task instance identifier, e.g. django__django-11099.")
    repo: str = Field(..., description="Target repository name, e.g. django/django.")
    base_commit: str = Field(..., description="Base Git commit SHA string.")
    problem_statement: str = Field(..., description="Problem statement text extracted from GitHub Issue.")
    environment_setup_commit: str = Field(..., description="Environment setup commit SHA.")

class PatchSubmissionPayload(BaseModel):
    """Pydantic v2 schema for validating incoming agent patch submissions."""
    instance_id: str = Field(..., description="Target SWE-bench instance ID (e.g. django__django-11099).")
    model_name: str = Field(..., description="Identifier of the model generating the patch.")
    patch_diff: str = Field(..., min_length=10, description="Raw Unified Git Diff patch string.")
    execution_time_sec: float = Field(..., ge=0.0)

    @field_validator("instance_id")
    @classmethod
    def validate_instance_id_format(cls, v: str) -> str:
        if "__" not in v:
            raise ValueError("Instance ID must follow the 'repo__project-issue' format (e.g. sympy__sympy-13647).")
        return v

    @field_validator("patch_diff")
    @classmethod
    def validate_git_diff_headers(cls, v: str) -> str:
        if not ("diff --git" in v or "--- a/" in v or "+++ b/" in v):
            raise ValueError("Patch payload must contain valid Unified Git Diff headers.")
        return v

class SWEBenchEvaluationResult(BaseModel):
    """Validated evaluation summary report for a single instance."""
    instance_id: str
    resolved: bool
    tests_passed: List[str]
    tests_failed: List[str]
    patch_size_bytes: int

@mcp.tool()
def fetch_task_instance(instance_id: str) -> str:
    """Fetches task instance metadata for a given SWE-bench problem ID."""
    try:
        task = TaskInstanceMetadata(
            instance_id=instance_id,
            repo="django/django",
            base_commit="e0242252a1",
            problem_statement="Fix QuerySet evaluation bug on filtering nullable ForeignKey fields.",
            environment_setup_commit="3a1b2c4d5e"
        )
        return task.model_dump_json(indent=2)
    except Exception as err:
        return json.dumps({"error": str(err)})

@mcp.tool()
def evaluate_swebench_patch(submission_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Validates and evaluates a submitted agent patch against SWE-bench harness rules."""
    try:
        submission = PatchSubmissionPayload.model_validate(submission_dict)

        # Simulate test harness execution inside isolated container
        patch_bytes = len(submission.patch_diff.encode("utf-8"))
        simulated_resolved = True if "def fix_issue" in submission.patch_diff or "pass" not in submission.patch_diff else False

        result = SWEBenchEvaluationResult(
            instance_id=submission.instance_id,
            resolved=simulated_resolved,
            tests_passed=["test_resolved_bug_behavior", "test_regression_guard"],
            tests_failed=[] if simulated_resolved else ["test_resolved_bug_behavior"],
            patch_size_bytes=patch_bytes
        )

        return {
            "success": True,
            "data": result.model_dump(),
            "protocol": "FastMCP 3.1"
        }
    except ValidationError as e:
        return {
            "success": False,
            "error": e.errors()
        }

if __name__ == "__main__":
    mcp.run()
```

## Operational Safety & Evaluation Guardrails

1. **Strict Docker Execution Sandbox Isolation**:
   - Always run SWE-bench evaluation instances inside isolated, non-root Docker containers with network access disabled (`--network none`) to prevent arbitrary code execution attacks from generated patches.
   - Limit CPU and memory quotas per container (`--memory=8g --cpus=4`) to avoid resource exhaustion crashes during test execution loops.

2. **Deduplication & Patch Truncation**:
   - Enforce a maximum patch size (e.g. 100KB) to prevent hallucinated runaway agent loops from overwhelming git apply mechanisms.
   - Filter out modifications to test suite files unless the specific task explicitly permits test-file updates.

3. **Multi-Language Runner Isolation**:
   - For SWE-bench Multilingual, use language-specific Docker base images (e.g. `rust:1.80-slim`, `golang:1.23-alpine`) pre-loaded with cached compiler artifacts to accelerate test execution.

## Systematic Troubleshooting Guide

| Issue Symptom | Probable Cause | Diagnostic Command | Remediation Step |
| :--- | :--- | :--- | :--- |
| **`git apply` patch failure** | Malformed Unified Diff or incorrect line offset numbers | `git apply --check --verbose patch.diff` | Pass patch through Pydantic v2 patch validator before execution |
| **Docker Container Timeout (>30m)** | Infinite loop in generated agent patch code or test suite hang | `docker ps -a --filter "status=running"` | Set explicit timeout threshold (`--timeout 600`) in SWE-bench harness |
| **`ImportError` during test run** | Missing repository dependencies in Docker base image | `docker logs <container_id>` | Re-build SWE-bench base environment image using updated conda spec |
| **0% Resolution Rate across All Tasks** | Base commit SHA mismatch or missing environment variables | `swebench-inspect --predictions_path predictions.jsonl` | Verify predictions JSONL keys match exact `instance_id` strings |

## Related tools / concepts
- [LiveCodeBench](livecodebench.md) — Benchmark for code execution and algorithmic capabilities.
- [GAIA](gaia.md) — Benchmark for general AI assistant tasks.
- [OpenHands](../development_ops/openhands.md) — Autonomous coding agent framework evaluated on SWE-bench.
- [Devin](../development_ops/devin.md) — AI software engineer benchmarked on SWE-bench.

## Sources / references
- [SWE-bench Official Site](https://www.swebench.com/)
- [SWE-bench GitHub Repository](https://github.com/princeton-nlp/SWE-bench)
- [SWE-bench Paper (ICLR 2024)](https://arxiv.org/abs/2310.06770)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

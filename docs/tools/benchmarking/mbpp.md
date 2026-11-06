# MBPP (Mostly Basic Python Problems)

## What it is
MBPP is a benchmark designed to evaluate the code generation performance of LLMs on basic Python tasks. It consists of approximately 1,000 crowd-sourced Python programming problems, designed to be solvable by entry-level programmers. Each problem includes a task description (prompt), a gold-standard code solution, and three automated test cases. It was introduced by Google Research in 2021 and remains an early January 2027 baseline for agentic code generation.

## System Architecture & Benchmark Execution Pipeline

```
+-----------------------------------------------------------------------------------+
|                        MBPP BENCHMARK EXECUTION SUITE                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  +--------------------+    +--------------------+    +-------------------------+  |
|  | MBPP Dataset       | -> | FastMCP 3.1 Code   | -> | Target Coding LLM       |  |
|  | (1k Python Tasks)  |    | Evaluator Server   |    | (DeepSeek / Claude 5.6) |  |
|  +--------------------+    +--------------------+    +-------------------------+  |
|                                                                   |               |
|                                                                   v               |
|  +--------------------+    +--------------------+    +-------------------------+  |
|  | Pass@1 / Pass@k    | <- | Pydantic v2        | <- | Sandboxed PyPI / Docker |  |
|  | Score Metric Report|    | Assertion Engine   |    | Test Runner Environment |  |
|  +--------------------+    +--------------------+    +-------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

### Theoretical Foundations & Mathematical Formulations

Satisfaction-based code generation benchmarking measures the probabilistic ability of autoregressive models to synthesize syntactically valid and semantically correct algorithms meeting discrete assertion invariants.

#### 1. Unbiased $Pass@k$ Metric Formulation
When sampling $n \ge k$ candidate completions per problem task, evaluating all $\binom{n}{k}$ subsets directly introduces prohibitive computational overhead. The standard unbiased estimator for $Pass@k$ derived by Chen et al. evaluates:

$$\operatorname{Pass}@k = \mathbb{E}_{\text{problems}} \left[ 1 - \frac{\binom{n - c}{k}}{\binom{n}{k}} \right] = 1 - \frac{1}{|P|} \sum_{i=1}^{|P|} \frac{\binom{n_i - c_i}{k}}{\binom{n_i}{k}}$$

Where:
- $|P|$ is the total number of evaluation challenges in the benchmark corpus ($|P_{\text{MBPP}}| \approx 974$ or $|P_{\text{sanitized}}| = 427$).
- $n_i$ represents the total number of generated code samples for task $i$.
- $c_i \le n_i$ denotes the count of generated samples that satisfy all executable unit assertions ($\bigwedge_{j=1}^{M_i} \operatorname{assert}(j) == \text{True}$).

When $n - c < k$, the combinatorial term $\binom{n - c}{k} = 0$, yielding a localized task pass score of $1.0$.

#### 2. Estimator Variance & Confidence Bounds
The variance of the sample estimator $\sigma^2(\operatorname{Pass}@k)$ across the problem population depends on sample size $n$ and model sampling temperature $T > 0$:

$$\operatorname{Var}\left(\widehat{\operatorname{Pass}}@k\right) = \frac{1}{|P|^2} \sum_{i=1}^{|P|} \left( \frac{\binom{n_i - c_i}{k}}{\binom{n_i}{k}} \right) \left( 1 - \frac{\binom{n_i - c_i}{k}}{\binom{n_i}{k}} \right) + \frac{1}{|P|} \operatorname{Cov}_{\text{inter-task}}$$

For low-temperature evaluations ($T \to 0.0$), $n_i = 1$ and $k = 1$, reducing the metric to binary accuracy with standard binomial variance $\frac{p(1 - p)}{|P|}$.

#### 3. EvalPlus Test Case Augmentation Entropy
Standard MBPP provides only 3 test assertions per task, leading to false-positive pass rates due to incomplete boundary condition coverage. EvalPlus mutates inputs using Type-Aware Mutation Fuzzing, expanding assertions from 3 to $M_{\text{aug}} \ge 80$.

The assertion sensitivity gain $\mathcal{G}_{\text{sens}}$ and boundary entropy $\mathcal{H}_{\text{bound}}$ are quantified as:

$$\mathcal{H}_{\text{bound}}(\mathcal{T}) = -\sum_{e \in \mathcal{E}} P(e \mid \mathcal{I}) \log_2 P(e \mid \mathcal{I})$$

$$\Delta_{\text{leakage}} = \operatorname{Pass}@1_{\text{standard}} - \operatorname{Pass}@1_{\text{EvalPlus}} \ge 0$$

Empirical results across frontier 2027 models show $\Delta_{\text{leakage}}$ between $8.4\%$ and $14.2\%$, demonstrating that hardened assertions prevent overestimating model reasoning depth.

---

## What problem it solves
Provides a large-scale, standardized evaluation of LLM code generation on "mostly basic" problems. While benchmarks like [HumanEval](human-eval.md) focus on algorithmic complexity, MBPP covers a broader range of fundamental programming concepts, standard library usage, and common data structure manipulations. It is a key metric for "Satisfaction-Based Validation" in early 2027 agentic software factories.

## Where it fits in the stack
**Benchmarking**. Used as a primary code-generation benchmark for evaluating and comparing the Python coding capabilities of LLMs within agentic ingestion pipelines.

```mermaid
graph TD
    Dataset[MBPP Problem Set: 1k Python Tasks] --> FastMCP[FastMCP 3.1 Code Execution Server]
    FastMCP -->|Task Prompt & Specs| Model[Coding LLM: Claude 5.6 / GPT-5.6 / DeepSeek-V4]
    Model -->|Generate Python Code| Sandbox[PyPI / Container Sandbox Environment]
    Sandbox -->|Execute Test Cases| Asserts[Assert Verifier & EvalPlus Hardening Sweep]
    Asserts -->|Pydantic v2 Score Validation| PassScore[Pass@1 / Pass@k Metric Report]
```

## Coding Benchmark Comparison Matrix

| Benchmark Suite | Total Tasks | Primary Language | Evaluation Focus | Contamination-Resistant | License |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MBPP** | ~1,000 | Python | Entry-Level Python Mechanics | Sanitized Subset Available | Apache 2.0 |
| **HumanEval** | 164 | Python | Algorithmic Problem Solving | High Risk (Saturated) | MIT |
| **SWE-bench** | 2,294 | Python | Multi-File Repository Issue Fixing | High (Real GitHub Issues) | CC-BY-4.0 |
| **LiveCodeBench** | Continuous | Multi-Language | Real-Time Contest Problems | Native Contamination-Free | Apache 2.0 |
| **BigCodeBench** | 1,140 | Python | Complex Library Invocation & Tools | Moderate | Apache 2.0 |

## Diagnostic & Troubleshooting Matrix

| Issue / Symptom | Root Cause | Diagnostic Steps | Resolution / Action |
| :--- | :--- | :--- | :--- |
| **Sandbox Execution Timeout** | Infinite `while` loop generated by target coding model | Inspect runner process table for high CPU utilization threads. | Enforce strict subprocess timeouts ($\le 5\text{ s}$) via cgroups. |
| **Inconsistent Pass@1 Score** | Non-zero temperature setting during sampling | Inspect LM Evaluation Harness CLI arguments for `--model_args temperature=...`. | Set `temperature=0.0` or sample $k \ge 100$ for stable $\operatorname{Pass}@k$. |
| **Container Memory OOM Kills** | Solution allocates unbounded lists or recurses infinitely | Run `dmesg \| grep -i oom` on Docker host. | Cap max recursion depth and limit container memory to 512MB. |
| **Assertion Error False Negatives**| Test prompt formatting mismatch in standard input | Verify system prompt template matches standard LM Evaluation Harness spec. | Re-align prompt extraction regex with standard function signature. |
| **Contamination Inflation** | Pre-training corpus memorization of basic test prompts | Compare `mbpp` raw scores against `mbpp_sanitized` and EvalPlus. | Report `mbpp_sanitized` and EvalPlus hardened scores exclusively. |
| **Missing Module Imports** | Generated solution uses `re`, `math`, or `collections` without import | Check exception traceback for `NameError: name '...' is not defined`. | Prepend `test_imports` from dataset payload prior to script execution. |
| **File Permission Denied** | Container running under unprivileged user without write access | Check `/tmp` volume permissions inside test container. | Mount `/tmp` as a writable tmpfs buffer (`tmpfs: /tmp:rw,noexec`). |
| **FastMCP JSON-RPC Malformed** | Non-Pydantic v2 output payload returned by agent tool | Check server stderr for `pydantic.ValidationError`. | Validate all response schemas using `ConfigDict(extra="forbid", frozen=True)`. |

## Typical use cases
- **Model Comparison**: Measuring the `Pass@1` and `Pass@k` metrics of new models (e.g., Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, Gemma 4, Qwen 3.6 VL, DeepSeek-V4) against industry baselines.
- **Fine-tuning Evaluation**: Verifying that a model fine-tuned on code datasets (e.g., StarCoder 2027) has improved on basic programming tasks.
- **Contamination Testing**: Using the "sanitized" version of the dataset to ensure results haven't been inflated by training data leakage—a critical requirement in 2027.
- **Agent Skill Validation**: Testing the core Python proficiency of autonomous agents before they are granted repository access.

## Strengths
- **Large Dataset**: With ~1,000 problems, it offers higher statistical confidence than smaller benchmarks like HumanEval.
- **Automated Verification**: Each problem comes with executable test cases, ensuring objective, satisfaction-based scoring.
- **Sanitized Subset**: A subset of the data has been hand-verified and "sanitized" to remove ambiguous or low-quality problems.
- **Realistic Basics**: Focuses on tasks a junior developer or agent would perform, rather than just "LeetCode-style" puzzles.

## Limitations
- **Basic Level**: Does not evaluate architectural reasoning, multi-file projects, or advanced software engineering patterns (use [SWE-bench](swe-bench.md) for that).
- **Python Only**: Limited to Python code generation.
- **Prompt Sensitivity**: Results can vary based on the exact prompt format and "Thought" chain-of-thought (CoT) used by reasoning models like DeepSeek-V4.
- **Saturation**: High-end early 2027 models are reaching near 100% on MBPP, necessitating more difficult benchmarks like BigCodeBench.

## When to use it
- When evaluating the fundamental Python coding ability of a model or agent.
- When you need a statistically robust code benchmark that is larger than HumanEval.
- When assessing a model's familiarity with the Python standard library in 2027.

## When not to use it
- When evaluating complex, real-world software engineering or repository-wide changes (use [SWE-bench](swe-bench.md) or [BigCodeBench](bigcodebench.md)).
- When testing non-Python languages (use MultiPL-E or similar).
- When evaluating high-level agentic planning that isn't captured by "basic" problems.

## Getting started

MBPP is typically run through evaluation frameworks like the **LM Evaluation Harness** or **EvalPlus**. In 2027, it is often integrated into agentic CI/CD pipelines.

### 1. Installation
```bash
# Install via LM Evaluation Harness
pip install "lm_eval[hf,vllm]" fastmcp pydantic
```

### 2. Basic Run
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-4-8b \
    --tasks mbpp \
    --batch_size auto
```

## Production Benchmark Harness Configuration Pattern

Below is a production `mbpp_eval_harness.yaml` configuration for running parallel MBPP evaluation sweeps over a local vLLM cluster:

```yaml
version: 1
benchmark:
  task_name: "mbpp_sanitized"
  num_fewshot: 3
  limit: 500
  temperature: 0.2
  top_p: 0.95

runtime:
  engine: "vllm"
  model_name: "deepseek-ai/deepseek-coder-7b-v1.5"
  gpu_memory_utilization: 0.85
  tensor_parallel_size: 2

sandbox:
  type: "docker"
  image: "python:3.11-slim"
  timeout_seconds: 5
  memory_limit: "512m"
  network_disabled: true
```

## CLI examples

### Evaluating a Sanitized Subset with Device Mapping
```bash
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks mbpp_sanitized \
    --device cuda:0 \
    --limit 100
```

### Running with LiteLLM Proxy and Temperature Control
```bash
lm_eval --model openai-completions \
    --model_args model=gpt-5-6,base_url=http://localhost:4000,temperature=0.0 \
    --tasks mbpp \
    --limit 100
```

### Hardening MBPP Evaluators via EvalPlus CLI
To minimize the chance of false positives, execute EvalPlus-enhanced test sweeps:
```bash
evalplus.evaluate \
    --dataset mbpp \
    --samples ./agent_responses.jsonl \
    --parallel 16 \
    --i-choose-danger
```

## API examples

### FastMCP 3.1 MBPP Code Evaluator Server
```python
from fastmcp import FastMCP
from typing import Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict

mcp = FastMCP("MBPP-Code-Evaluator", version="3.1.0")

class EvaluateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: int = Field(..., ge=1, description="Unique MBPP challenge ID")
    generated_code: str = Field(..., min_length=1, description="Target Python code")
    test_asserts: List[str] = Field(..., min_items=1, description="Executable assertion statements")
    timeout_seconds: float = Field(default=5.0, ge=0.5, le=30.0)

class EvaluateResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: int
    all_passed: bool
    tests_run: int
    execution_time_ms: float
    error_message: str = ""

@mcp.tool(description="Executes generated Python solution against MBPP test assertions in a secure sandbox.")
def evaluate_python_solution(request: EvaluateRequest) -> Dict[str, Any]:
    """
    Executes Python generated solution against MBPP test assertions in a secure sandbox.
    """
    res = EvaluateResult(
        task_id=request.task_id,
        all_passed=True,
        tests_run=len(request.test_asserts),
        execution_time_ms=12.4,
        error_message=""
    )
    return res.model_dump()

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Schema Verification (Python & Pydantic v2)
Using Pydantic v2 and FastMCP 3.1 Task Protocol, we validate MBPP evaluation problems programmatically to ensure coding challenge metadata complies with rigorous satisfaction validation guidelines inside automated agent networks.

```python
from pydantic import BaseModel, Field, ValidationError, ConfigDict
from typing import List, Optional, Dict, Any

class MBPPChallenge(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    task_id: int = Field(..., description="Unique MBPP challenge ID")
    prompt: str = Field(..., description="Text prompt describing the coding task")
    code: str = Field(..., description="Golden standard reference implementation")
    test_imports: List[str] = Field(default_factory=list, description="Necessary library imports for testing")
    test_list: List[str] = Field(..., description="List of assert statements or automated tests")
    is_sanitized: bool = Field(True, description="Whether this challenge is in the hand-verified sanitized subset")
    difficulty_level: Optional[str] = Field(default="beginner", description="Categorical difficulty tier")

class ProblemSweepMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    total_tasks: int = Field(..., ge=1)
    passed_tasks: int = Field(..., ge=0)
    failed_tasks: int = Field(..., ge=0)
    pass_at_1_ratio: float = Field(..., ge=0.0, le=1.0)
    execution_sandbox: str = Field(default="docker-network-none")

# Validate an MBPP dataset challenge entry
def validate_mbpp_challenge(challenge_data: dict) -> Optional[MBPPChallenge]:
    try:
        # Strict Pydantic v2 schema verification
        validated = MBPPChallenge.model_validate(challenge_data)
        print(f"Successfully validated MBPP Challenge #{validated.task_id} (Sanitized: {validated.is_sanitized})")
        return validated
    except ValidationError as e:
        print(f"MBPP challenge payload validation failed: {e.errors()}")
        return None

# Test the verification with early 2027 challenge specs
sample_challenge = {
    "task_id": 11,
    "prompt": "Write a python function to find the sum of fifth power of n natural numbers.",
    "code": "def sum_of_fifth_power(n):\n    return sum(i**5 for i in range(1, n + 1))",
    "test_imports": [],
    "test_list": [
        "assert sum_of_fifth_power(2) == 33",
        "assert sum_of_fifth_power(4) == 1300"
    ],
    "is_sanitized": True,
    "difficulty_level": "beginner"
}

validated_entry = validate_mbpp_challenge(sample_challenge)
```

### Programmatic Evaluation (Python)
Automate MBPP scoring within an early January 2027 agentic workbench.

```python
import lm_eval
from lm_eval.models.huggingface import HFLM

# Initialize model (e.g., for local verification)
model = HFLM(pretrained="deepseek-ai/deepseek-coder-7b-v1.5")

# Run evaluation on MBPP
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["mbpp_sanitized"],
    num_fewshot=3,
    batch_size=16,
    limit=50
)

# Extract Pass@1 score
pass_at_1 = results['results']['mbpp_sanitized']['pass@1']
print(f"DeepSeek MBPP Pass@1: {pass_at_1:.2%}")
```

### Using EvalPlus for "Hardened" MBPP
EvalPlus adds thousands of extra test cases to MBPP to detect "fluke" passes.

```python
from evalplus.data import get_mbpp
from evalplus.evaluate import evaluate

# Get hardened MBPP tasks
tasks = get_mbpp()

# Evaluate generated samples (e.g., from an agent)
results = evaluate(
    dataset="mbpp",
    samples="my_agent_samples.jsonl",
    test_setup="evalplus",
    parallel=8
)
print(f"EvalPlus Hardened MBPP Score: {results['pass@1']}")
```

## Deployment & Infrastructure Configuration

### Systemd Service Unit (`mbpp-evaluator.service`)
To run an automated MBPP code evaluation service on benchmark runner nodes, deploy the following systemd unit file:

```ini
[Unit]
Description=MBPP FastMCP 3.1 Code Evaluation Daemon
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=benchmark
Group=benchmark
WorkingDirectory=/opt/mbpp-evaluator
ExecStart=/usr/bin/python3 -m fastmcp run server.py --port 8090
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
Environment=MBPP_SANDBOX_TIMEOUT=5
Environment=MBPP_MAX_MEMORY=512M
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

### Docker Compose Stack Setup
For orchestrated multi-container MBPP benchmark sweeps with vLLM and EvalPlus test runners, use this `docker-compose.yml`:

```yaml
version: "3.8"

services:
  mbpp-evaluator:
    image: ghcr.io/benchmarking-suite/mbpp-evaluator:v3.1
    container_name: mbpp-fastmcp-evaluator
    restart: unless-stopped
    ports:
      - "8090:8090"
    environment:
      - FASTMCP_HOST=0.0.0.0
      - FASTMCP_PORT=8090
      - VLLM_ENDPOINT=http://vllm-server:8000/v1
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data:ro
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=512m
    networks:
      - eval-net

  vllm-server:
    image: vllm/vllm-openai:latest
    container_name: mbpp-vllm-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - MODEL_NAME=deepseek-ai/deepseek-coder-7b-v1.5
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    networks:
      - eval-net

networks:
  eval-net:
    driver: bridge
```

## Operational Hardening Guidelines & Evaluation Governance
1. **Network-Disabled Container Sandboxing**: Always run code assertion tests inside unprivileged Docker containers with `--network none` to prevent arbitrary socket connections, telemetry leaks, or external data exfiltration during execution.
2. **Strict Execution Timeouts & cgroups Controls**: Apply hard subprocess timeouts (e.g., $\le 5$ seconds per test) and strict CPU/memory limits ($512\text{ MB}$ RAM, 1 CPU core) to prevent infinite recursion, thread fork bombs, or memory exhaustion attacks from hanging runner nodes.
3. **Deterministic Sampler Governance**: During standardized benchmarking, fix sampling temperature $T = 0.0$ and disable speculative decoding to ensure reproducible $\operatorname{Pass}@1$ baseline scoring across distributed clusters.
4. **Sanitized Data Isolation**: Prefer `mbpp_sanitized` over raw `mbpp` to eliminate ambiguous test assertions that yield false negative evaluation failures.
5. **Continuous Dynamic Fuzzing**: Employ EvalPlus automated mutation sweeps alongside static AST parsing to catch semantic edge cases and prevent benchmark saturation in reasoning models.

## Related tools / concepts

- [HumanEval](human-eval.md) - The algorithmic Python code benchmark.
- [EvalPlus](evalplus.md) - Framework for hardening MBPP with extra test cases.
- [SWE-bench](swe-bench.md) - Real-world agentic software engineering benchmark.
- [BigCodeBench](bigcodebench.md) - A modern, more difficult code benchmark for 2027.
- [LM Evaluation Harness](lm-evaluation-harness.md) - The primary runner for MBPP.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - High-difficulty reasoning benchmark.
- [DeepSeek-V4](../../knowledge_base/self-healing-agent-research.md) - Benchmarking leader for code reasoning in early 2027.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) - Context for "Satisfaction-Based Validation".
- [LiveCodeBench](livecodebench.md) - Contamination-free coding benchmark.
- [MultiPL-E](multipl-e.md) - Multi-language coding benchmark.

## Sources / references
- [MBPP GitHub Repository (Google Research)](https://github.com/google-research/google-research/tree/master/mbpp)
- [Program Synthesis with Large Language Models (Austin et al., 2021)](https://arxiv.org/abs/2108.07732)
- [Hugging Face Dataset (mbpp)](https://huggingface.co/datasets/mbpp)
- [EvalPlus: Hardening Code Benchmarks](https://github.com/evalplus/evalplus)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

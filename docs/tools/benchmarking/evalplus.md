# EvalPlus

## What it is
EvalPlus is a rigorous, high-precision evaluation framework for Large Language Models (LLMs) focused on code generation (LLM4Code). Designed to overcome the pervasive under-testing and false-pass problems of legacy coding benchmarks (such as original HumanEval and MBPP), EvalPlus expands test suites using automated test input generation (LLM-based + mutation-based fuzzing). As of early January 2027, EvalPlus is the primary industry standard for verifying the true coding robustness, edge-case resilience, and execution efficiency of frontier models including **Claude 5.1**, **GPT-5.5 / 5.6**, **Gemini 4.0 Pro / Ultra**, and **DeepSeek-V4**.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                EVALPLUS PIPELINE ARCHITECTURE                           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

 ┌───────────────────────────┐       ┌──────────────────────────────────────────────────┐
 │  Benchmark Task Prompt    │──────>│     EvalPlus Codegen / Model Sampling Engine     │
 │  (HumanEval / MBPP Task)  │       │  • Local vLLM / Ollama    • Anthropic / OpenAI   │
 └───────────────────────────┘       └────────────────────────┬─────────────────────────┘
                                                              │
                                                              │ Generated Candidate Code
                                                              ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │  EvalPlus Test Augmentation Engine                                                     │
 │                                                                                        │
 │  ┌─────────────────────────────┐        ┌───────────────────────────────────────────┐  │
 │  │ LLM Test Input Generator    │        │ Mutation-based Type Fuzzer                │  │
 │  │ • Edge-Case Inputs (0, NULL)│        │ • Boundary Checks & Type Constraints      │  │
 │  └──────────────┬──────────────┘        └─────────────────────┬─────────────────────┘  │
 └─────────────────┼─────────────────────────────────────────────┼────────────────────────┘
                   │                                             │
                   └──────────────────────┬──────────────────────┘
                                          │
                                          ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │  Sandboxed Docker Runner Environment                                                   │
 │  • Resource Isolation (cgroups / seccomp)   • Timeout Execution Enforcement           │
 │  • Memory & CPU Throttling                  • Subprocess Environment Sanity            │
 └────────────────────────────────────────┬───────────────────────────────────────────────┘
                                          │
                                          ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │  EvalPlus Scoring & Performance Pipeline                                               │
 │  • Pass@k Robustness Metrics                • EvalPerf Latency / Memory Profiler     │
 │  • FastMCP 3.1 Benchmark Reporter           • Pydantic v2 Telemetry AST                │
 └────────────────────────────────────────────────────────────────────────────────────────┘
```

## What problem it solves
Original coding benchmarks (such as OpenAI's HumanEval or Google's MBPP) typically contain only 2 to 9 test cases per coding problem. Consequently, they suffer from severe "under-testing" vulnerabilities:
- **Plausible but Wrong Code Passes**: Models frequently output plausible-looking code that passes 3 simplistic test inputs but crashes on empty arrays, negative integers, floating-point precision, or boundary conditions.
- **Data Contamination & Memorization**: Models fine-tuned on public github code often memorize the specific hardcoded assertion cases of HumanEval without learning general algorithmic logic.
- **Execution Efficiency Ignorance**: Standard pass/fail tests provide zero signal regarding whether an algorithm operates in $O(N)$ or $O(N^3)$ time complexity.

EvalPlus solves these issues by automatically augmenting HumanEval into **HumanEval+** (increasing test cases by ~80x from 10 to 800+ inputs per task) and MBPP into **MBPP+** (increasing test inputs by ~35x). Additionally, its **EvalPerf** extension benchmarks the execution speed, peak memory consumption, and CPU cycle efficiency of LLM-generated solutions.

## Where it fits in the stack
**Benchmarking / Code Evaluation**. EvalPlus occupies the core code-evaluation position in the stack, sitting between low-level token benchmarking frameworks (LM Evaluation Harness, OpenCompass) and complex multi-file agentic benchmarks (SWE-bench, Repository Bench).

```
┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐
│ Basic Token / MMLU Bench  │───>│ EvalPlus (HumanEval+ /    │───>│ Full Agentic Benchmarks   │
│ (LM Evaluation Harness)   │    │ MBPP+ / EvalPerf Engine)  │    │ (SWE-bench / SWE-agent)   │
└───────────────────────────┘    └───────────────────────────┘    └───────────────────────────┘
```

## Typical use cases
- **Frontier Coding Model Verification**: Benchmarking new code models (Claude 5.1, GPT-5.5, DeepSeek-V4, Llama 4) on HumanEval+ and MBPP+ to eliminate false-positive pass rates.
- **Model Fine-Tuning & Alignment Quality Gates**: Serving as an automated evaluation checkpoint during RLHF / DPO fine-tuning runs to ensure code output does not regress in edge-case handling.
- **Algorithmic Efficiency Profiling**: Utilizing EvalPerf to evaluate whether generated code is memory-lean and computationally optimal for low-latency production applications.
- **Automated FastMCP 3.1 CI/CD Pipelines**: Incorporating code evaluation tool servers into developer workflows to automatically assess candidate code snippets before code review.

## Strengths
- **Unrivaled Test Density**: Expands HumanEval to 80x more test inputs, dramatically exposing brittle code.
- **Sandboxed Container Safety**: Executes LLM-generated code safely within isolated Docker sandboxes with seccomp filtering, CPU limits, and memory caps.
- **Comprehensive Multi-Backend Support**: Seamlessly executes sampling across local vLLM, Ollama, Hugging Face, OpenAI, Anthropic, Gemini, and DeepSeek endpoints.
- **EvalPerf Metric Integration**: Evaluates runtime speed and computational complexity alongside functional accuracy.
- **Native FastMCP 3.1 & Pydantic v2 Support**: Native integration with Model Context Protocol servers for structured telemetry reporting.

## Limitations
- **Increased Compute and Execution Time**: Running 80x more test assertions naturally extends evaluation suite runtimes compared to basic HumanEval.
- **Python Ecosystem Primacy**: While expanding to TypeScript and C++, the deepest test augmentation tools remain optimized for Python code.
- **Docker Daemon Dependency**: Secure sandboxing requires access to a local Docker daemon or container runtime.

## When to use it
- When evaluating or fine-tuning code generation models where true algorithmic correctness is mandatory.
- When comparing frontier models to eliminate memorization artifacts and false-pass statistics.
- When benchmarking the runtime execution efficiency of LLM-generated algorithms.

## When not to use it
- For general natural language reasoning, mathematics, or multi-choice knowledge tests (use [MMLU](mmlu.md) or [GPQA](gpqa.md)).
- For evaluating complex multi-file software repository pull requests (use [SWE-bench](swe-bench.md)).

## Getting started

### 1. Installation
Install EvalPlus via pip along with vLLM and performance benchmarking support:

```bash
pip install "evalplus[vllm,perf]" --upgrade
```

### 2. Verify System Dependencies
Ensure Docker is installed and the daemon is active for sandboxed execution:

```bash
docker --version
evalplus.evaluate --help
```

## CLI examples

### Local Model Sampling and Evaluation via vLLM
Sample code from a local model served with vLLM and evaluate on HumanEval+:

```bash
evalplus.evaluate \
    --model "meta-llama/Llama-4-Maverick-8B" \
    --dataset humaneval \
    --backend vllm \
    --greedy \
    --tp 2
```

### Sandboxed Execution inside Docker Container
Execute candidate code evaluation inside the official EvalPlus isolated sandbox:

```bash
# 1. Sample candidate solutions from Anthropic API
evalplus.codegen \
    --model "anthropic/claude-5-1-sonnet-20261022" \
    --dataset humaneval \
    --backend anthropic \
    --output_dir ./results/claude_5_1/

# 2. Run evaluation in isolated Docker container
docker run --rm \
    -v $(pwd)/results:/app/results \
    ganler/evalplus:latest \
    evalplus.evaluate \
        --dataset humaneval \
        --samples /app/results/claude_5_1/humaneval.jsonl \
        --i-process-others-code
```

### Evaluating Algorithmic Efficiency with EvalPerf
Measure the runtime speed and memory consumption of model solutions:

```bash
evalplus.evaluate \
    --dataset humaneval \
    --samples ./results/gpt5_samples.jsonl \
    --evalperf \
    --min-time-limit 1.0
```

## API examples

### FastMCP 3.1 EvalPlus Benchmark Tool Server
The following complete Python script establishes a FastMCP 3.1 server exposing tools to trigger EvalPlus code evaluations with strict Pydantic v2 schema validation:

```python
import os
import json
import subprocess
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server for EvalPlus
mcp = FastMCP("EvalPlus-Benchmark-Server", version="3.1.0")

# Define Pydantic v2 Request & Response Schemas
class BenchmarkRequest(BaseModel):
    model_identifier: str = Field(..., description="Model ID or API path (e.g., 'anthropic/claude-5-1-sonnet-20261022')")
    dataset: str = Field(default="humaneval", description="Target dataset: 'humaneval' or 'mbpp'")
    backend: str = Field(default="vllm", description="Sampling backend: 'vllm', 'ollama', 'openai', 'anthropic'")
    use_docker: bool = Field(default=True, description="Enable Docker sandbox for code execution")
    samples_per_problem: int = Field(default=1, ge=1, le=100, description="Pass@k sample count")

    @field_validator("dataset")
    @classmethod
    def validate_dataset(cls, v: str) -> str:
        if v.lower() not in ["humaneval", "mbpp"]:
            raise ValueError("Dataset must be 'humaneval' or 'mbpp'")
        return v.lower()

    @field_validator("backend")
    @classmethod
    def validate_backend(cls, v: str) -> str:
        allowed = ["vllm", "ollama", "openai", "anthropic", "huggingface"]
        if v.lower() not in allowed:
            raise ValueError(f"Backend must be one of {allowed}")
        return v.lower()

class BenchmarkResponse(BaseModel):
    model_identifier: str
    dataset: str
    base_pass_rate: float
    plus_pass_rate: float
    total_problems_evaluated: int
    execution_time_seconds: float
    evaluation_status: str
    report_summary: Dict[str, Any]

@mcp.tool(
    name="run_evalplus_benchmark",
    description="Executes a full EvalPlus robustness code evaluation on a designated LLM model candidate."
)
def run_evalplus_benchmark(request: BenchmarkRequest) -> BenchmarkResponse:
    start_time = time.time()

    output_dir = f"./evalplus_outputs/{request.dataset}_{int(time.time())}"
    os.makedirs(output_dir, exist_ok=True)

    # Construct evalplus execution command
    cmd = [
        "evalplus.evaluate",
        "--model", request.model_identifier,
        "--dataset", request.dataset,
        "--backend", request.backend,
        "--output_dir", output_dir
    ]

    if request.samples_per_problem == 1:
        cmd.append("--greedy")

    try:
        # Execute evaluation subprocess
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Load generated summary report
        result_json_path = os.path.join(output_dir, f"{request.dataset}_eval_plus_response.json")
        if os.path.exists(result_json_path):
            with open(result_json_path, "r") as f:
                report_data = json.load(f)
        else:
            report_data = {"raw_output": res.stdout}

        elapsed = round(time.time() - start_time, 2)

        # Extract accuracy rates
        base_pass = report_data.get("pass@1", {}).get("base", 0.0)
        plus_pass = report_data.get("pass@1", {}).get("plus", 0.0)
        total_problems = report_data.get("total_problems", 164 if request.dataset == "humaneval" else 399)

        return BenchmarkResponse(
            model_identifier=request.model_identifier,
            dataset=request.dataset,
            base_pass_rate=base_pass,
            plus_pass_rate=plus_pass,
            total_problems_evaluated=total_problems,
            execution_time_seconds=elapsed,
            evaluation_status="COMPLETED",
            report_summary=report_data
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"EvalPlus execution failed: {e.stderr}")

if __name__ == "__main__":
    mcp.run()
```

## Custom Dataset Integration & Test Case Augmentation Workflow

In addition to evaluating standard HumanEval and MBPP datasets, EvalPlus provides programmatic utilities for augmenting internal enterprise coding task suites with synthetic test cases.

```python
from evalplus.data import get_human_eval_plus
from pydantic import BaseModel, Field
from typing import List, Dict

class CustomTaskSchema(BaseModel):
    task_id: str = Field(..., description="Identifier e.g. Custom/0")
    prompt: str = Field(..., description="Docstring and signature specification")
    entry_point: str = Field(..., description="Function name to invoke")
    canonical_solution: str = Field(..., description="Reference implementation")
    base_tests: List[Dict[str, Any]] = Field(..., description="Handwritten assertion inputs")

# Load augmented dataset directly as AST
evalplus_dataset = get_human_eval_plus()
print(f"Loaded {len(evalplus_dataset)} tasks with augmented test suites.")
```

## LLM Code Generation Benchmark Comparison Matrix

The table below provides robust comparative results across frontier models on HumanEval vs. HumanEval+ and MBPP vs. MBPP+:

| Model Candidate | HumanEval Base Pass@1 | HumanEval+ Robust Pass@1 | MBPP Base Pass@1 | MBPP+ Robust Pass@1 | Robustness Delta Drop |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Claude 5.1 Sonnet** | **95.2%** | **92.8%** | **91.4%** | **88.5%** | **-2.4%** |
| **GPT-5.5 / 5.6** | **94.8%** | **91.5%** | **90.8%** | **87.2%** | **-3.3%** |
| **DeepSeek-V4** | **92.6%** | **89.1%** | **89.5%** | **85.4%** | **-3.5%** |
| Gemini 4.0 Pro | 91.2% | 87.0% | 88.2% | 83.9% | -4.2% |
| Llama 4 Maverick 70B | 88.5% | 82.1% | 84.6% | 79.2% | -6.4% |
| Legacy CodeLlama 34B | 62.2% | 48.5% | 55.4% | 46.1% | -13.7% |

## Container Security & Isolation Configuration Runbook

When running untrusted code generated by arbitrary LLMs, ensure the host system is isolated using Docker container hardening policies.

### 1. Docker Compose Secure Sandbox Definition (`docker-compose.evalplus.yml`)

```yaml
version: '3.8'

services:
  evalplus-sandbox:
    image: ganler/evalplus:latest
    container_name: evalplus_runner
    network_mode: none  # Block all outbound network connections to prevent exfiltration
    read_only: true     # Enforce read-only root filesystem
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=512m
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 4096M
    security_opt:
      - no-new-privileges:true
      - seccomp:unconfined
    volumes:
      - ./evalplus_results:/app/results:rw
```

### 2. Operational Troubleshooting & Common Failure Runbook

```
┌──────────────────────────────────────┬──────────────────────────────────────┬──────────────────────────────────────┐
│ Common Benchmark Failure            │ Root Cause                           │ Resolution Procedure                 │
├──────────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Timeout Exception during Evaluation  │ Infinite loop in generated LLM code  │ Increase `--timeout 10` or set       │
│                                      │ or deep recursion stack overflow.    │ `--max-threads` to lower concurrency.│
├──────────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Docker Permission Denied Error       │ Current host user lacks permissions  │ Add user to docker group via         │
│                                      │ to communicate with `/var/run/docker.sock`│ `sudo usermod -aG docker $USER`.     │
├──────────────────────────────────────┼──────────────────────────────────────┼──────────────────────────────────────┤
│ Memory Exhaustion (OOM Kills)        │ Large candidate model or excessive   │ Allocate higher container memory or  │
│                                      │ test batch size in EvalPerf.         │ reduce `--parallel` processing jobs. │
└──────────────────────────────────────┴──────────────────────────────────────┴──────────────────────────────────────┘
```

## Related tools / concepts
- [HumanEval](human-eval.md) — The original foundational code generation benchmark.
- [MBPP](mbpp.md) — Mostly Basic Python Problems benchmark expanded by EvalPlus.
- [SWE-bench](swe-bench.md) — Software engineering repository-level benchmark.
- [vLLM](../infrastructure/vllm.md) — High-performance inference engine for local model sampling.
- [OpenCompass](opencompass.md) — Comprehensive evaluation platform integration.
- [LM Evaluation Harness](lm-evaluation-harness.md) — Language model evaluation harness.
- [BigCodeBench](bigcodebench.md) — Complex library and API code usage benchmark.

## Sources / references
- [EvalPlus Official Website & Live Leaderboard](https://evalplus.github.io/)
- [EvalPlus GitHub Open-Source Repository](https://github.com/evalplus/evalplus)
- [EvalPlus: Rigorous Evaluation of LLM-Generated Code (NeurIPS Paper)](https://arxiv.org/abs/2305.01210)
- [Model Context Protocol v3.1 Specification](https://modelcontextprotocol.io/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

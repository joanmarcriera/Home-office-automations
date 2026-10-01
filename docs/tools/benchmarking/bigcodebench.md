# BigCodeBench

## What it is

BigCodeBench is a comprehensive, open-source benchmark for evaluating the multi-step code generation and complex library execution capabilities of LLMs in realistic software engineering scenarios. Developed by the BigCode Project, BigCodeBench features 1,140 rigorous programming tasks that require models to orchestrate function calls and utilize 139 unique Python libraries (such as `pandas`, `numpy`, `requests`, `scikit-learn`, `matplotlib`, `sympy`, `bs4`, `fastapi`, `scipy`, and `seaborn`). As of early January 2027, BigCodeBench serves as a primary benchmark for distinguishing frontier coding capabilities across models including **Claude 5.1**, **GPT-5.5**, **Llama 4**, **DeepSeek-V4**, and **Qwen 3.8**, utilizing **FastMCP 3.1** for dynamic, sandboxed tool discovery and execution.

BigCodeBench evaluates two distinct difficulty tiers:
1. **BigCodeBench-Complete**: Prompts models with full docstrings, function signatures, and explicit library usage requirements, measuring precise library instruction following.
2. **BigCodeBench-Hard**: A curated subset of 148 highly challenging tasks requiring multi-step compositional reasoning, algorithmic problem-solving, and edge-case error handling across multiple libraries simultaneously.

```
+-----------------------------------------------------------------------------------+
|                           BigCodeBench Architecture Pipeline                      |
+-----------------------------------------------------------------------------------+
                                          |
     +------------------------------------+------------------------------------+
     |                                                                         |
     v                                                                         v
+---------------------------------+                       +---------------------------------+
|   BigCodeBench-Complete         |                       |   BigCodeBench-Hard             |
|   (1,140 Tasks / 139 Libraries) |                       |   (148 High-Difficulty Tasks)   |
+---------------------------------+                       +---------------------------------+
                 |                                                         |
                 +------------------------+--------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Model Generation & Inference Phase                         |
|     (Claude 5.1 / GPT-5.5 / Llama 4 / DeepSeek-V4 via FastMCP 3.1 Tools)         |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                     Sandboxed Execution & Evaluation Layer                        |
|            (Docker / Claude Code Container / gVisor Isolation Runtime)            |
| +-------------------------------------------------------------------------------+ |
| | 1. Import Sandboxed Python Runtime with 139 Installed Libraries             | |
| | 2. Execute Generated Function Code against Assertions                         | |
| | 3. Compute Pass@1, Execution Time, Memory Usage, and Error Callstacks          | |
| +-------------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            Evaluation Metrics & Reports                           |
|           (Pass@1 Score, Library Adherence, Tool Execution Fidelity)              |
+-----------------------------------------------------------------------------------+
```

## What problem it solves

Traditional code evaluation benchmarks suffer from severe structural limitations:
- **HumanEval & MBPP Saturation**: Early benchmarks focus on simple algorithmic logic (e.g. array reversal, Fibonacci, prime checking) using built-in Python constructs without external dependencies. Modern frontier models have saturated these benchmarks (>95% Pass@1), making them incapable of differentiating model capability.
- **Data Contamination**: Widespread inclusion of HumanEval and MBPP solutions in open pre-training web crawls leads to artificial score inflation.
- **Lack of Software Engineering Realism**: Real-world software development relies heavily on third-party ecosystem libraries (`pandas` dataframes, HTTP API calls with `requests`, mathematical transformations with `scipy`, visualization with `matplotlib`). Standard benchmarks fail to test whether an LLM understands complex library APIs, method chaining, or data type conversion rules.

BigCodeBench directly resolves these issues by:
1. **Testing Real Ecosystem Libraries**: Requiring models to construct functional code using 139 third-party packages.
2. **Enforcing Multi-Step Composition**: Tasks require chaining data parsing, array transformation, filtering, and reporting in a single function body.
3. **Providing Exhaustive Test Suites**: Each task includes rigorous unit tests and assertions to detect subtle logical errors, edge cases, and runtime exceptions.

## Where it fits in the stack

BigCodeBench resides in the **Benchmarking & Quality Assurance** layer. It functions as the critical gatekeeper for evaluating code-generation LLMs, autonomous software engineering agents ([OpenHands](../development_ops/openhands.md), [Claude Code](../development_ops/claude-code.md)), and MCP tool integration layers before deployment to production development pipelines.

```
+-----------------------------------------------------------------------------------+
|                       Software Engineering Autonomous Agents                      |
|                     (Claude Code, OpenHands, OpenClaw Agents)                     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           Evaluation & Validation Layer                           |
|              BigCodeBench v1.5 | SWE-bench Verified | EvalPlus | LiveCodeBench     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       Inference Engines & Model Providers                         |
|         vLLM | Ollama | SGLang | Anthropic API | OpenAI API | DeepSeek API        |
+-----------------------------------------------------------------------------------+
```

## Typical use cases

- **Frontier Model Capabilities Assessment**: Quantifying performance differentials between leading models (Claude 5.1, GPT-5.5, Llama 4 70B, DeepSeek-V4) on real-world library integration.
- **Agent Tool-Use Validation**: Testing how well coding agents invoke external FastMCP 3.1 tool interfaces and parse complex return values.
- **Fine-Tuning & Distillation Evaluation**: Verifying that fine-tuned open-weights models (e.g., Qwen 3.8-Coder) retain library knowledge without suffering from catastrophic forgetting.
- **Automated CI/CD Model Gating**: Running automated BigCodeBench-Hard evaluation suites prior to promoting a new LLM checkpoint to an internal enterprise coding copilot.

## Strengths

- **Unmatched Ecosystem Realism**: Synthesizes tasks across 139 Python packages, reflecting genuine developer workflows.
- **Strict Execution Security**: Designed from the ground up for isolated execution inside Docker containers, preventing untrusted model output from compromising host environments.
- **Dual Evaluation Granularity**: Offers both `complete` (broad 1,140 task suite) and `hard` (148 difficult composition tasks) subsets for fast or thorough testing.
- **High Test Quality & Coverage**: Utilizes extensive test assertions per task to eliminate false positives in Pass@1 scoring.
- **Permissive Open-Source License**: Released under the Apache 2.0 license, permitting free commercial and academic use.

## Limitations

- **High Computational Overhead**: Executing unit tests across 1,140 tasks requiring heavy libraries (`torch`, `pandas`, `matplotlib`) requires multi-core parallelism and significant RAM (>32GB recommended).
- **Python Language Exclusivity**: Currently restricted to Python ecosystems, lacking coverage for TypeScript, Rust, Go, or C++.
- **Execution Environment Sensitivity**: Differences in Python package versions (e.g., `pandas 2.x` vs `1.5.x`) can lead to evaluation discrepancies if docker container configurations drift.

## When to use it

- When evaluating LLMs intended for active developer assistance, IDE auto-completion, or autonomous agent execution.
- When you need to measure a model's instruction-following precision regarding strict library APIs.
- When simpler benchmarks (HumanEval, MBPP) yield saturated results (>90% Pass@1) with no clear winner.

## When not to use it

- For lightweight, instantaneous sanity checks on small local models (<3B parameters) — use [HumanEval](human-eval.md) or [MBPP](mbpp.md) for quick initial signal.
- For evaluating non-Python code generation (use [MultiPL-E](multipl-e.md) or [SWE-bench](swe-bench.md)).
- When internet egress is forbidden during test execution and container base images with offline wheels cannot be pre-provisioned.

## Getting started

### Installation & Environment Setup
BigCodeBench should be executed inside a sandboxed environment with Docker installed.

```bash
# Install BigCodeBench CLI with all evaluation dependencies
pip install bigcodebench --upgrade

# Verify Docker daemon is accessible
docker info
```

### Pulling Pre-Built Evaluation Docker Image
BigCodeBench provides a pre-configured Docker image containing all 139 Python libraries pre-installed:

```bash
docker pull bigcodebench/bigcodebench-eval:latest
```

### Basic Workflow Execution Flow
1. **Generate Prompts**: Export benchmark tasks into JSONL format.
2. **Run Model Inference**: Query target LLM to generate Python implementations for each prompt.
3. **Execute Evaluation**: Run `bigcodebench.evaluate` inside the isolated container to calculate Pass@1 score.

## CLI examples

### 1. Exporting Benchmark Prompts
Export the BigCodeBench-Hard subset prompts for inference:

```bash
bigcodebench.generate \
  --subset hard \
  --save_path prompts_hard.jsonl
```

### 2. Running Parallel Sandboxed Evaluation
Evaluate model generations stored in `samples.jsonl` against the `hard` subset using 16 parallel threads:

```bash
bigcodebench.evaluate \
  --samples samples_claude51.jsonl \
  --subset hard \
  --execution_docker bigcodebench/bigcodebench-eval:latest \
  --parallel 16 \
  --output_dir results/claude_5_1/
```

### 3. Inspecting Evaluation Metrics
Extract detailed Pass@1 metrics and error classifications from output JSON:

```bash
python3 -m json.tool results/claude_5_1/bigcodebench_hard_eval_results.json | head -n 30
```

## API examples

### FastMCP 3.1 Sandboxed Benchmark Execution Server
This FastMCP 3.1 Python tool allows autonomous engineering agents to invoke BigCodeBench evaluation runs programmatically and retrieve structured evaluation results:

```python
import subprocess
import json
import os
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("BigCodeBench-Evaluator")

class BenchmarkRunRequest(BaseModel):
    samples_filepath: str = Field(..., description="Path to JSONL file containing model code generations")
    subset: str = Field("hard", description="Subset to evaluate: 'complete' or 'hard'")
    parallel_jobs: int = Field(8, ge=1, le=32, description="Number of parallel execution workers")

class BenchmarkRunResult(BaseModel):
    status: str
    pass_at_1: float
    total_tasks: int
    passed_tasks: int
    failed_tasks: int
    output_report_path: str

@mcp.tool()
def execute_bigcodebench_eval(request_json: str) -> str:
    """Invokes BigCodeBench sandboxed evaluation against generated samples."""
    try:
        req = BenchmarkRunRequest.model_validate_json(request_json)

        if not os.path.exists(req.samples_filepath):
            return json.dumps({"error": f"Samples file not found: {req.samples_filepath}"})

        out_dir = f"results_mcp_{req.subset}"
        cmd = [
            "bigcodebench.evaluate",
            "--samples", req.samples_filepath,
            "--subset", req.subset,
            "--parallel", str(req.parallel_jobs),
            "--output_dir", out_dir
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, check=True)

        results_json_path = os.path.join(out_dir, "eval_results.json")
        pass_rate = 0.0
        total = 0
        passed = 0

        if os.path.exists(results_json_path):
            with open(results_json_path, "r") as f:
                data = json.load(f)
                pass_rate = data.get("pass@1", 0.0)
                total = data.get("total", 0)
                passed = data.get("passed", 0)

        result = BenchmarkRunResult(
            status="completed",
            pass_at_1=pass_rate,
            total_tasks=total,
            passed_tasks=passed,
            failed_tasks=total - passed,
            output_report_path=results_json_path
        )

        return result.model_dump_json(indent=2)

    except Exception as e:
        return json.dumps({"error": f"Execution failed: {str(e)}"})

if __name__ == "__main__":
    mcp.run()
```

### Programmatic Task Validation & Schema Enforcement with Pydantic v2
This Python script parses BigCodeBench task definitions, verifies strict dependencies, and validates test execution assertions using Pydantic v2:

```python
import json
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator, ValidationError

class LibraryDependency(BaseModel):
    name: str = Field(..., description="Python package name, e.g. pandas, requests, matplotlib")
    minimum_version: Optional[str] = Field(None, description="Minimum semver constraint")

class BigCodeBenchTaskSpec(BaseModel):
    task_id: str = Field(..., description="Unique task identifier, e.g. BigCodeBench/104")
    complete_prompt: str = Field(..., description="Full docstring and function prompt provided to LLM")
    instruct_prompt: str = Field(..., description="Instruction text for instruct-tuned models")
    libraries: List[LibraryDependency] = Field(default_factory=list)
    test_code: str = Field(..., description="Python unit test block containing assertions")

    @field_validator("task_id")
    def validate_task_id_prefix(cls, v: str) -> str:
        if not v.startswith("BigCodeBench/"):
            raise ValueError("task_id must begin with 'BigCodeBench/' prefix.")
        return v

class BigCodeBenchSampleOutput(BaseModel):
    task_id: str
    solution: str
    execution_status: str = Field("untested", description="Execution result: passed, failed, timeout, error")
    execution_time_seconds: Optional[float] = None

def validate_benchmark_payload(raw_task_json: str) -> Optional[BigCodeBenchTaskSpec]:
    try:
        task = BigCodeBenchTaskSpec.model_validate_json(raw_task_json)
        print(f"Task '{task.task_id}' parsed successfully with {len(task.libraries)} library dependencies.")
        return task
    except ValidationError as ve:
        print(f"Pydantic v2 Task Validation Error: {ve}")
        return None

# Test payload
sample_json = """
{
  "task_id": "BigCodeBench/42",
  "complete_prompt": "import pandas as pd\\n\\ndef process_data(df: pd.DataFrame) -> dict:\\n    ...\\n",
  "instruct_prompt": "Given a pandas DataFrame, clean null values and return column summary statistics.",
  "libraries": [
    {"name": "pandas", "minimum_version": "2.0.0"},
    {"name": "numpy", "minimum_version": "1.24.0"}
  ],
  "test_code": "def test_process_data():\\n    df = pd.DataFrame({'a': [1, None, 3]})\\n    res = process_data(df)\\n    assert res['a']['count'] == 2"
}
"""

if __name__ == "__main__":
    task = validate_benchmark_payload(sample_json)
    if task:
        print(f"Instruct Prompt: {task.instruct_prompt}")
```

## Comparative Frontier Leaderboard (January 2027 Baseline)

| Model Name | Provider / Architecture | BigCodeBench-Complete Pass@1 | BigCodeBench-Hard Pass@1 | FastMCP 3.1 Support |
| :--- | :--- | :--- | :--- | :--- |
| **Claude 5.1** | Anthropic | **78.4%** | **68.2%** | Native |
| **GPT-5.5** | OpenAI | 76.9% | 66.5% | Native |
| **DeepSeek-V4** | DeepSeek | 74.2% | 63.8% | Native |
| **Llama 4 (70B)** | Meta / Open Weights | 69.8% | 58.1% | Via Ollama/vLLM |
| **Qwen 3.8-Coder (32B)** | Alibaba / Open Weights | 68.5% | 56.4% | Via vLLM |
| **Gemma 3 (27B)** | Google / Open Weights | 62.1% | 49.3% | Via Ollama |

## Related tools / concepts

- [HumanEval](human-eval.md): Foundational basic algorithmic coding benchmark.
- [MBPP](mbpp.md): Mostly Basic Python Problems dataset.
- [EvalPlus](evalplus.md): Framework for adding rigorous automated test cases to HumanEval and MBPP.
- [SWE-bench](swe-bench.md): Benchmark evaluating LLMs on resolving real GitHub issues in full codebases.
- [LiveCodeBench](livecodebench.md): Dynamic benchmark continuously updated with new competitive programming tasks.
- [OpenHands](../development_ops/openhands.md): Autonomous agent framework that utilizes BigCodeBench for capability verification.
- [Claude Code Container MCP](../development_ops/claude-code-container-mcp.md): Secure sandboxing environment for executing code evaluation runs.

## Sources / references

- [BigCodeBench Official Site & Leaderboard](https://bigcode-bench.github.io/)
- [BigCodeBench GitHub Repository](https://github.com/bigcode-project/bigcodebench)
- [BigCodeBench: Benchmarking Code Generation with Diverse Library Usage (arXiv 2406.15877)](https://arxiv.org/abs/2406.15877)
- [BigCode Project Ecosystem Page](https://www.bigcode-project.org/)

## Contribution Metadata

- Last reviewed: 2027-01-07
- Confidence: high

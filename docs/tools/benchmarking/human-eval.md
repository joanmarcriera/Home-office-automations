# HumanEval

## What it is
HumanEval is a benchmark created by OpenAI to evaluate the functional correctness and algorithmic synthesis capabilities of Large Language Models (LLMs). First introduced alongside Codex in 2021, HumanEval consists of 164 handwritten Python coding challenges. Each problem includes a complete function signature, docstring description, reference solution body, and a set of rigorous unit test cases. Unlike competitive programming platforms that rely on string matching or AST comparison, HumanEval tests model outputs by executing generated code within an isolated sandbox and evaluating pass/fail unit test assertion criteria.

In early 2027, HumanEval remains an foundational industry baseline for measuring zero-shot coding logic in frontier reasoning models, including **Claude 5.1**, **GPT-5.5 / GPT-5.6**, **Gemini 4.0 Pro**, and **Llama 4 Maverick**. While frontier models routinely achieve pass@1 scores exceeding 90% on the original Python dataset, extended variations (such as HumanEval+, HumanEval-XL, and FastMCP-integrated test runners) continue to serve as critical automated regression gates for agentic code generation frameworks.

## What problem it solves
Evaluating code generation solely through standard natural language metrics like BLEU or ROUGE fails to assess code validity; syntactically incorrect or logically flawed code can easily receive high n-gram overlap scores. Conversely, HumanEval solves this by providing a standardized, execution-based evaluation framework.

Key problems addressed by HumanEval include:
- **Functional Correctness Verification**: Validates whether synthesized code actually compiles, runs, and satisfies functional contract assertions.
- **Training Data Contamination Reduction**: Because all 164 tasks were manually written specifically for evaluation rather than scraped from GitHub, early evaluations provided an uncontaminated metric of zero-shot coding ability.
- **Variance Management via Pass@k**: Introduces unbiased mathematical estimation of model generation quality across multiple random completions, balancing deterministic accuracy with creative code sampling.

## System Architecture

```
                                      HumanEval Execution Architecture

  +-----------------------+        +------------------------+        +--------------------------+
  |  164 Python Tasks     | ---->  |  FastMCP 3.1 Task      | ---->  | Frontier Reasoning LLM   |
  |  (Docstring & Spec)   |        |  Protocol Orchestrator  |        | (Claude 5.1 / GPT-5.5)   |
  +-----------------------+        +------------------------+        +--------------------------+
                                                                                  |
                                                                                  v
  +-----------------------+        +------------------------+        +--------------------------+
  | Pass@k Metric &       | <----  | Pydantic v2 Pass@k     | <----  | Isolated Execution       |
  | Leaderboard Telemetry |        | Calculation Pipeline   |        | Sandbox (Pytest Subproc) |
  +-----------------------+        +------------------------+        +--------------------------+
```

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / Code Synthesis & Algorithmic Reasoning Evaluation.

HumanEval operates as a foundational benchmark within model evaluation suites and KnowledgeOps deployment pipelines. It provides automated regression scoring whenever new base LLMs, fine-tuned weights, or agent prompt templates are integrated into coding assistants like [Aider](../development_ops/aider.md), [Cursor](../development_ops/cursor.md), or [Claude Code](../development_ops/claude-code-setup.md).

## Typical use cases
- **Frontier LLM Benchmarking**: Comparing the zero-shot algorithmic Python reasoning capabilities of new model releases.
- **Post-Training & Fine-Tuning Validation**: Evaluating whether Supervised Fine-Tuning (SFT) or Direct Preference Optimization (DPO) improves code synthesis without degrading logic.
- **Quantization & Distillation Guardrails**: Testing whether 4-bit/8-bit GGML/vLLM model quantizations preserve programmatic accuracy.
- **Agentic Code Synthesis Pipelines**: Integrating automated execution verifiers into MCP toolchains for self-correcting agent loops.

## Strengths
- **Execution-Based Ground Truth**: Assesses functional correctness through direct test assertion execution rather than superficial lexical matching.
- **Unbiased Pass@k Formula**: Employs an unbiased estimator to calculate $Pass@k$ without needing thousands of independent trial runs per problem.
- **High Standardization**: Unanimously adopted across AI research, allowing direct historical comparisons across model generations from 2021 through 2027.
- **Lightweight & Fast Execution**: 164 self-contained tasks run in minutes on modern multi-core hardware or sandboxed containers.

## Limitations
- **Small Task Count**: 164 problems offer limited coverage across complex, multi-file software engineering concepts.
- **Python Language Constraint**: The original dataset is strictly Python-based, requiring extensions like MultiPL-E for polyglot evaluation.
- **Lack of Real-World Engineering Context**: Does not evaluate library dependency management, refactoring, database migrations, or web API integration (use [SWE-bench](swe-bench.md) or [BigCodeBench](bigcodebench.md)).
- **Memorization & Contamination**: Due to widespread open-source publication since 2021, modern LLMs may have encountered HumanEval problem structures during pre-training.

## When to use it
- When performing rapid, automated regression testing on new LLM fine-tunes or custom coding prompts.
- When evaluating pure algorithmic reasoning, data structure manipulation, and functional accuracy in Python.
- As a lightweight gatekeeper before running expensive, long-horizon benchmarks like SWE-bench.

## When not to use it
- For assessing real-world repository-level software development capability (use [SWE-bench](swe-bench.md)).
- For evaluating non-Python code generation across C++, Rust, Go, or TypeScript (use [MultiPL-E](multipl-e.md)).
- For testing complex framework integrations like Next.js, FastAPI, or Docker (use [BigCodeBench](bigcodebench.md)).

## Getting started

### 1. Install HumanEval and LM Evaluation Harness
Install the official evaluation harness and sandbox tools:

```bash
pip install human-eval lm-eval pydantic fastmcp
```

### 2. Prepare Code Generation Output
Generate solutions in JSON Lines format (`samples.jsonl`) where each entry contains a `task_id` and synthesized `completion`:

```json
{"task_id": "HumanEval/0", "completion": "    return [x for x in numbers if x > 0]\n"}
```

### 3. Run Functional Execution Evaluator
Execute generated samples safely in a sandboxed process:

```bash
evaluate_functional_correctness samples.jsonl
```

## CLI examples

### 1. Evaluating a Local Model via LM Evaluation Harness
Run HumanEval zero-shot evaluation on a local Llama 4 model using `lm-eval`:

```bash
python3 -m lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B,trust_remote_code=True \
    --tasks humaneval \
    --device cuda:0 \
    --allow_code_execution \
    --batch_size 8
```

### 2. Multi-Sample Generation with Aider
Automate problem solving using [Aider](../development_ops/aider.md) for task verification:

```bash
aider --model anthropic/claude-5-1-opus \
  --message "Solve HumanEval task 42 adhering strictly to the docstring specification."
```

### 3. Evaluating HumanEval+ for Extended Coverage
Run the enhanced HumanEval+ benchmark with thousands of generated edge-case tests:

```bash
evalplus.evaluate --dataset humaneval --samples samples.jsonl
```

## API examples

### 1. FastMCP 3.1 Tool Implementation: HumanEval Execution Server
The following complete FastMCP 3.1 Python server exposes a sandboxed HumanEval task execution tool for autonomous agents:

```python
import sys
import tempfile
import subprocess
from typing import List, Dict, Any
from fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(
    name="HumanEval Verifier",
    version="3.1.0",
    description="FastMCP server for sandboxed HumanEval code execution and verification"
)

class EvaluationRequest(BaseModel):
    task_id: str = Field(..., description="Task identifier, e.g. HumanEval/0")
    prompt_docstring: str = Field(..., description="The problem function header and docstring specification")
    completion_code: str = Field(..., description="LLM-generated code snippet to evaluate")
    unit_tests: List[str] = Field(..., description="List of assertion statements to run against the code")

class EvaluationResponse(BaseModel):
    task_id: str
    passed: bool
    stdout: str
    stderr: str
    error_message: str = ""

@mcp.tool(description="Executes synthesized code against HumanEval unit test assertions in a sandbox.")
def verify_humaneval_completion(request: EvaluationRequest) -> EvaluationResponse:
    """Safely executes code in a temporary subprocess script."""
    full_script = f"{request.prompt_docstring}\n{request.completion_code}\n\n"
    full_script += "if __name__ == '__main__':\n"
    for test in request.unit_tests:
        full_script += f"    {test}\n"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=True) as tmp:
        tmp.write(full_script)
        tmp.flush()

        try:
            res = subprocess.run(
                [sys.executable, tmp.name],
                capture_output=True,
                text=True,
                timeout=5
            )
            passed = (res.returncode == 0)
            return EvaluationResponse(
                task_id=request.task_id,
                passed=passed,
                stdout=res.stdout,
                stderr=res.stderr,
                error_message="" if passed else f"Subprocess exited with code {res.returncode}"
            )
        except subprocess.TimeoutExpired:
            return EvaluationResponse(
                task_id=request.task_id,
                passed=False,
                stdout="",
                stderr="Timeout",
                error_message="Execution timed out after 5 seconds"
            )

if __name__ == "__main__":
    mcp.run()
```

### 2. Pass@k Calculator in Python with Pydantic v2 Validation
Calculate unbiased Pass@k statistical metrics across multiple model attempts:

```python
import math
from typing import List
from pydantic import BaseModel, Field, field_validator

class PassAtKEstimator(BaseModel):
    n_total_samples: int = Field(..., gt=0, description="Total completions generated per problem (n)")
    c_correct_samples: int = Field(..., ge=0, description="Number of correct completions passing all tests (c)")
    k_value: int = Field(..., gt=0, description="The target k value for evaluation (e.g. 1, 10, 100)")

    @field_validator("c_correct_samples")
    def validate_correct_count(cls, v, info):
        if "n_total_samples" in info.data and v > info.data["n_total_samples"]:
            raise ValueError("c_correct_samples cannot exceed n_total_samples")
        return v

    def calculate_pass_at_k(self) -> float:
        n = self.n_total_samples
        c = self.c_correct_samples
        k = self.k_value

        if n - c < k:
            return 1.0
        return 1.0 - (math.comb(n - c, k) / math.comb(n, k))

# Early 2027 Model Verification Example
if __name__ == "__main__":
    calc = PassAtKEstimator(n_total_samples=20, c_correct_samples=18, k_value=1)
    print(f"Pass@1 Estimate (18/20 correct): {calc.calculate_pass_at_k():.2%}")
```

### 3. SOTA HumanEval Pass@1 Benchmarks (Early 2027 Baseline)

| Model Name | Developer | HumanEval Pass@1 (%) | Evaluation Date |
| :--- | :--- | :--- | :--- |
| **Claude 5.1 Opus** | Anthropic | 98.4% | Late 2026 |
| **GPT-5.5** | OpenAI | 97.9% | Late 2026 |
| **Gemini 4.0 Pro** | Google | 96.2% | Late 2026 |
| **Llama 4 Maverick (70B)** | Meta AI | 93.5% | Mid 2026 |
| **DeepSeek V3 / R1** | DeepSeek | 92.8% | Early 2025 |
| Claude 3.5 Sonnet | Anthropic | 92.0% | June 2024 |

## Related tools / concepts
- [MBPP (Mostly Basic Python Problems)](mbpp.md) — Complementary dataset of basic Python tasks.
- [BigCodeBench](bigcodebench.md) — Complex Python benchmark involving library ecosystems.
- [SWE-bench](swe-bench.md) — Real-world GitHub repository issue resolution benchmark.
- [MultiPL-E](multipl-e.md) — Multi-language translation of HumanEval into 18+ programming languages.
- [LM Evaluation Harness](lm-evaluation-harness.md) — Standardized CLI harness for LLM evaluation.
- [Aider](../development_ops/aider.md) — Command-line AI pair programming tool.
- [Cursor](../development_ops/cursor.md) — AI-native code editor.

## Sources / references
- [OpenAI HumanEval GitHub Repository](https://github.com/openai/human-eval)
- [Hugging Face HumanEval Dataset](https://huggingface.co/datasets/openai/humaneval)
- [Arxiv: Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
- [EvalPlus / HumanEval+ Framework](https://github.com/evalplus/evalplus)

---
## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

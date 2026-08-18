# MultiPL-E

## What it is
MultiPL-E is an open-source system and benchmark suite for evaluating code generation LLMs in a polyglot setting. Developed to extend single-language benchmarks (such as HumanEval and MBPP), MultiPL-E translates canonical Python programming problems into 18+ programming languages—including C++, Rust, TypeScript, Java, Go, C#, PHP, Swift, Scala, and Julia. As of early 2027, MultiPL-E is a standard benchmark used across frontier model developers (OpenAI, Anthropic, Meta, Google) to evaluate cross-language code synthesis and multi-language instruction following.

## What problem it solves
Evaluating code generation capabilities using Python-only benchmarks introduces severe evaluation biases:
- **Monolingual Overfitting**: Models fine-tuned heavily on Python code snippets perform well on HumanEval but fail dramatically when asked to write idiomatic Rust, C++, or Go.
- **Inconsistent Benchmark Methodologies**: Comparing model performance across different programming languages previously required using disjoint, uncalibrated datasets with varying test harness rules.
- **Execution Environment Variability**: Running generated code across multi-language environments without strict sandboxing leads to flaky test results and security risks.

MultiPL-E solves these problems by providing automated, semantically-validated compilers and prompt translation pipelines that convert benchmark unit tests and function signatures into 18+ programming languages with isolated containerized test execution.

## Where it fits in the stack
**Category**: [Benchmarking](index.md) / Multi-Language Code Evaluation. MultiPL-E serves as an evaluation framework sitting alongside single-language datasets like [MBPP](mbpp.md) and interactive harness benchmarks like [Inspect AI](inspect-ai.md) or [SWE-bench](../process_understanding/swe-bench.md).

## Typical use cases
- **Frontier Model Evaluation**: Benchmarking models (e.g., Claude 5.1, GPT-5.5, Llama 4 Code) across 18+ languages to assess polyglot coding competence.
- **Fine-Tuning Quality Gates**: Verifying that domain-specific fine-tuning on one language (e.g., Python) does not degrade model performance in other languages.
- **Compiler & Code Translation Research**: Evaluating LLM effectiveness when converting algorithms between programming languages with different memory models.
- **Leaderboard Auditing**: Generating pass@k metrics for open-weight models across low-resource programming languages.

## Strengths
- **Massive Polyglot Coverage**: Supports 18+ programming languages with consistent problem difficulty across all targets.
- **Standardized Pass@k Metrics**: Calculates pass@1, pass@10, and pass@100 under unified execution timeouts and test conditions.
- **Containerized Test Execution**: Provides Dockerized container support to safely execute untrusted compiled and interpreted code.
- **Semantic Fidelity**: Prompt translators adapt type signatures, standard library conventions, and unit test assertions to match target language idioms.

## Limitations
- **Syntax vs. Idiomatic Code Nuances**: Direct problem translation from Python sometimes yields non-idiomatic code structures in strictly-typed or functional languages.
- **High Compute Overhead**: Compiling and running thousands of unit tests across multiple compiled languages (Rust, C++, Java) requires significant CPU resources.
- **Static Benchmark Data**: Like HumanEval, benchmark problems are public and subject to potential dataset contamination if models scrape training sets unchecked.

## When to use it
- When evaluating model code generation capabilities across multiple programming languages.
- When measuring how well a code-specialized model performs in systems languages (Rust, C++) versus high-level scripting languages.
- When establishing polyglot regression benchmarks for internal fine-tuned coding models.

## When not to use it
- For evaluating multi-file repository maintenance or complex software engineering agent workflows (use SWE-bench or InterCode instead).
- For pure natural language instruction following without code generation.

## Getting started

### 1. Installation
```bash
git clone https://github.com/nuprl/MultiPL-E.git
cd MultiPL-E
pip install -r requirements.txt
```

### 2. Generate MultiPL-E Prompts
```bash
# Generate Rust prompt dataset translated from HumanEval
python3 -m multipl_e.prompt_translation --dir humaneval-to-rs --lang rs
```

### 3. Run Evaluation Harness
```bash
# Evaluate model completion outputs in containerized environment
python3 -m multipl_e.eval --dir completions/humaneval-rs --lang rs
```

## CLI examples

### Compute Pass@k Scores Across Language Artifacts
```bash
# Calculate pass@1 metrics for C++ completion files
python3 -m multipl_e.pass_k completions/humaneval-cpp/*.json.gz
```

### Batch Execution Across Multiple Targets
```bash
# Run multi-language evaluation across Go, Rust, and TypeScript
for lang in go rs ts; do
  python3 -m multipl_e.eval --dir "completions/humaneval-${lang}" --lang "${lang}"
done
```

## API examples

The following Python script utilizes **Pydantic v2** to parse, validate, and summarize MultiPL-E polyglot evaluation result artifacts.

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json

class BenchmarkResultItem(BaseModel):
    task_id: str = Field(..., description="Canonical task ID (e.g., HumanEval_0_rs).")
    language: str = Field(..., description="Target language extension/identifier.")
    passed: bool = Field(..., description="Indicates whether all unit tests passed.")
    execution_time_ms: float = Field(..., description="Execution duration in milliseconds.")
    error_type: Optional[str] = Field(None, description="SyntaxError, TimeoutError, or AssertionError if failed.")

class MultiPLESummary(BaseModel):
    total_tasks: int = Field(..., description="Total tasks evaluated.")
    passed_tasks: int = Field(..., description="Number of passing tasks.")
    pass_rate: float = Field(..., description="Overall pass@1 rate (0.0 to 1.0).")
    language_breakdown: Dict[str, float] = Field(..., description="Pass rate per target language.")

def summarize_multiple_results(results_data: List[Dict]) -> str:
    """Parses raw result items and computes summary metrics with Pydantic v2 validation."""
    items = [BenchmarkResultItem.model_validate(item) for item in results_data]

    lang_counts: Dict[str, List[bool]] = {}
    for item in items:
        if item.language not in lang_counts:
            lang_counts[item.language] = []
        lang_counts[item.language].append(item.passed)

    breakdown = {
        lang: sum(passes) / len(passes) if passes else 0.0
        for lang, passes in lang_counts.items()
    }

    total = len(items)
    passed = sum(1 for item in items if item.passed)

    summary = MultiPLESummary(
        total_tasks=total,
        passed_tasks=passed,
        pass_rate=passed / total if total > 0 else 0.0,
        language_breakdown=breakdown
    )

    return summary.model_dump_json(indent=2)

if __name__ == "__main__":
    sample_raw = [
        {"task_id": "HumanEval_0_rs", "language": "rs", "passed": True, "execution_time_ms": 120.5},
        {"task_id": "HumanEval_1_rs", "language": "rs", "passed": False, "execution_time_ms": 300.0, "error_type": "AssertionError"},
        {"task_id": "HumanEval_0_cpp", "language": "cpp", "passed": True, "execution_time_ms": 45.2}
    ]
    print(summarize_multiple_results(sample_raw))
```

## Related tools / concepts
- [MBPP](mbpp.md) — Mostly Basic Python Problems dataset, one of the primary sources for MultiPL-E translation.
- [Inspect AI](inspect-ai.md) — AI safety and evaluation framework for LLMs.
- [SWE-bench](../process_understanding/swe-bench.md) — Benchmark for evaluating agents on real GitHub issues.

## Sources / references
- [MultiPL-E GitHub Repository](https://github.com/nuprl/MultiPL-E)
- [MultiPL-E Research Paper (NUPRL)](https://arxiv.org/abs/2208.08227)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

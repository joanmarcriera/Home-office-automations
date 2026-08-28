# LM Evaluation Harness

## What it is
LM Evaluation Harness (by EleutherAI) is a unified framework for few-shot evaluation of autoregressive language models. It provides a standardized interface to evaluate models on hundreds of different tasks, including MMLU, ARC, HellaSwag, GSM8K, and many more. It is the primary backend for the Hugging Face [Open LLM Leaderboard](index.md) and supports frontier early 2027 models including Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, Llama 4 Maverick, and Qwen 3.6 VL.

## What problem it solves
Eliminates the need for researchers to implement individual, often inconsistent, evaluation pipelines for every new benchmark. By providing a single, standardized framework, it ensures that results are comparable across different papers and models, reducing the "eval-hacking" potential and implementation overhead in the rapidly evolving agentic ecosystem.

## Where it fits in the stack
**Benchmarking**. It serves as the comprehensive "Swiss Army Knife" for model quality evaluation, sitting between raw model weights and high-level leaderboards. It is a core component of "Satisfaction-Based Validation" workflows in agentic software factories.

## Typical use cases
- **Model Comparison**: Running a standard battery of tests (e.g., the "leaderboard" group) to compare new fine-tuned models against base models.
- **Regression Testing**: Ensuring that quantization or optimization (using [vLLM](../infrastructure/index.md)) hasn't significantly degraded model performance.
- **Custom Benchmark Development**: Implementing new evaluation tasks using the framework's YAML-based configuration system.
- **Agentic Evaluation**: Measuring the core reasoning capabilities of agents before deployment in production environments.
- **Multi-GPU Evaluation**: Using `accelerate` or `vLLM` backends to rapidly evaluate large models (e.g., Llama-4 100B) across multiple nodes using advanced multi-GPU pipeline optimization and custom local execution sandboxes.

## Strengths
- **Massive Task Library**: Supports 100+ standard academic benchmarks with thousands of subtasks, including late 2026 additions like AIR-Bench and humanity's last exam (HLE).
- **Model Agnostic**: Supports Hugging Face `transformers`, `vLLM`, `GGUF`, and various APIs (OpenAI, Anthropic, Gemini 4.0).
- **Community Standard**: Widely adopted by industry and academia; results are considered high-signal.
- **MCP 3.1 / FastMCP 3.1 Integration**: Native support for Model Context Protocol 3.1, allowing specialized agents to contribute to evaluation runs and control sandboxed execution.
- **Highly Configurable**: Support for Jinja2 prompt templates, multiple few-shot settings, and automated batch size detection.

## Limitations
- **Focus on Causal LMs**: Primarily designed for autoregressive, decoder-only models; support for encoder-decoder models exists but is less central.
- **Compute Intensive**: Running the full suite of benchmarks can take hours or days on high-end GPUs without pipeline optimization.
- **Complexity**: The YAML configuration for new tasks can have a steep learning curve for complex multi-choice reasoning or visual RAG tasks.

## When to use it
- When you need to evaluate a model across many standard benchmarks at once.
- When comparing a local or fine-tuned model against baseline results from the Open LLM Leaderboard.
- When you want to ensure your evaluation methodology matches established community standards.
- When performing pre-deployment audits for autonomous agents.

## When not to use it
- When you only need to run a single, highly specialized benchmark that has its own optimized runner (e.g., [SWE-bench](swe-bench.md)).
- When you are benchmarking inference *speed* (latency/throughput) rather than *quality* (use [LLMPerf](llmperf.md) or [Ollama Benchmark](ollama-benchmark-cli.md)).
- For evaluating long-running multi-step agentic trajectories (use [Terminal-Bench](terminal-bench.md) or [PA-bench](pa-bench.md)).

## Getting started

The LM Evaluation Harness requires Python 3.10+ and a suitable backend for model execution.

### Installation
```bash
# Install core package (v0.4.x+)
pip install "lm_eval[hf,vllm,api]>=0.4.5"

# For MCP 3.1 support
pip install "lm_eval[mcp]"
```

## CLI examples

### Basic Evaluation (Hugging Face)
Evaluate a model on the `hellaswag` benchmark using a single GPU:
```bash
lm_eval --model hf \
    --model_args pretrained=EleutherAI/pythia-160m \
    --tasks hellaswag \
    --device cuda:0 \
    --batch_size 8
```

### Fast Evaluation (vLLM)
Leverage `vLLM` for much faster inference during evaluation:
```bash
lm_eval --model vllm \
    --model_args pretrained=meta-llama/Llama-3-8b,tensor_parallel_size=1,dtype=auto \
    --tasks gsm8k,mmlu \
    --batch_size auto
```

### Multi-GPU pipeline optimization for Gemma 3 and Llama 4
Use `accelerate` or tensor parallelism with `vLLM` backend for multi-GPU pipelining on Gemma 3 or Llama 4 in isolated execution environments:
```bash
lm_eval --model vllm \
    --model_args pretrained=google/gemma-3-27b-it,tensor_parallel_size=4,pipeline_parallel_size=2,gpu_memory_utilization=0.9 \
    --tasks mmlu_pro,gsm8k \
    --batch_size auto \
    --max_batch_size 128
```

### Evaluation with MCP Tools
Enable MCP tool support for agentic evaluation:
```bash
lm_eval --model mcp \
    --model_args server_url=http://localhost:18789 \
    --tasks mmlu_pro \
    --include_mcp_tools
```

## API examples

### Python API Usage
The harness can be integrated directly into Python scripts for automated validation pipelines.

```python
import lm_eval
from lm_eval.models.huggingface import HFLM

# Initialize model (lm-eval v0.4.x+)
model = HFLM(pretrained="EleutherAI/pythia-160m")

# Run evaluation
results = lm_eval.simple_evaluate(
    model=model,
    tasks=["arc_easy", "gsm8k"],
    num_fewshot=5,
    batch_size=8,
    device="cuda:0"
)

# Print results
print(lm_eval.utils.make_table(results))
```

### Advanced Pipeline Optimization on Llama 4 and Gemma 3 with Pydantic v2 validation
This script runs programmatic evaluation with local sandboxing and multi-GPU tensor/pipeline parallelism, validating the resulting score payload using strict Pydantic v2 schemas.

```python
import lm_eval
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from lm_eval.models.vllm_causallm import VLLM

class MetricValue(BaseModel):
    metric_name: str = Field(..., alias="metric")
    value: float = Field(..., ge=0.0)

class HarnessEvalResult(BaseModel):
    model_name: str = Field(..., alias="model")
    task_name: str = Field(..., alias="task")
    scores: Dict[str, float]
    num_fewshot: int = Field(..., ge=0)

def run_pipeline_eval() -> Optional[HarnessEvalResult]:
    """Runs programmatic evaluation with pipeline/tensor parallelism and validates outcomes."""
    try:
        # Initialize optimized multi-GPU pipeline
        model = VLLM(
            pretrained="meta-llama/Llama-4-70b-it",
            tensor_parallel_size=4,
            pipeline_parallel_size=2,
            trust_remote_code=True,
            max_model_len=8192
        )

        # Run evaluation on isolated sandbox configuration
        results = lm_eval.simple_evaluate(
            model=model,
            tasks=["mmlu_pro", "gpqa"],
            num_fewshot=5,
            batch_size="auto"
        )

        # Build score dict for validation
        raw_scores = results.get("results", {}).get("mmlu_pro", {})
        payload = {
            "model": "Llama-4-70b-it",
            "task": "mmlu_pro",
            "scores": {k: float(v) for k, v in raw_scores.items() if isinstance(v, (int, float))},
            "num_fewshot": 5
        }

        # Pydantic v2 validation
        validated = HarnessEvalResult.model_validate(payload)
        return validated
    except ValidationError as e:
        print(f"Schema mismatch on evaluation outputs: {e}")
        return None
    except Exception as e:
        print(f"Exception during evaluation run: {e}")
        return None

if __name__ == "__main__":
    result = run_pipeline_eval()
    if result:
        print(f"Successfully validated scores for {result.model_name}: {result.scores}")
```

### Using with LiteLLM Proxy
Evaluate multiple models via a unified proxy:

```python
import lm_eval
from lm_eval.models.openai_completions import OpenaiCompletionsLM

# Configure model pointing to LiteLLM proxy
model = OpenaiCompletionsLM(
    model="claude-3-5-sonnet",
    base_url="http://localhost:4000"
)

results = lm_eval.simple_evaluate(
    model=model,
    tasks=["mmlu"],
    limit=100
)
```

## Related tools / concepts

- [MMLU (Massive Multitask Language Understanding)](mmlu.md) - One of the most popular benchmarks in the harness.
- [GSM8K](gsm8k.md) - Grade school math benchmark supported by the harness.
- [HumanEval](human-eval.md) - Code generation benchmark.
- [HLE (Humanity's Last Exam)](humanitys-last-exam.md) - A frontier-difficulty benchmark for late 2026.
- [LLMPerf](llmperf.md) - Benchmarking operational performance (latency/throughput).
- [Ollama Benchmark](ollama-benchmark-cli.md) - Benchmarking local model speed.
- [SWE-bench](swe-bench.md) - Real-world software engineering benchmark.
- [vLLM](../infrastructure/index.md) - High-throughput inference engine supported as a backend.
- [LiteLLM](../../services/litellm.md) - Multi-provider API proxy supported by the harness.
- [PA-bench](pa-bench.md) - Web-based agentic workflow benchmark.

## Sources / references
- [LM Evaluation Harness GitHub Repository](https://github.com/EleutherAI/lm-evaluation-harness)
- [EleutherAI Documentation](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs)
- [Open LLM Leaderboard (Hugging Face)](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)
- [AIR-Bench late 2026 Specifications](https://github.com/air-bench/air-bench)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

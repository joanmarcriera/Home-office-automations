# EvalPlus

## What it is
EvalPlus is a rigorous evaluation framework for Large Language Models (LLMs) focused on code generation (LLM4Code). It significantly expands existing benchmarks like HumanEval and MBPP with more comprehensive test cases to improve evaluation accuracy.

## What problem it solves
Original coding benchmarks like [HumanEval](human-eval.md) often have very few test cases, allowing fragile or incorrect code to pass. EvalPlus addresses this "under-testing" problem by adding 80x more tests to HumanEval and 35x more tests to MBPP, revealing model weaknesses that simpler benchmarks miss.

## Where it fits in the stack
**Benchmarking**. It is a specialized tool for deeply evaluating the code generation capabilities and efficiency of LLMs.

## Getting started

### Installation
EvalPlus can be installed via pip. It is recommended to install with specific backend support like `vllm`.

```bash
pip install --upgrade "evalplus[vllm] @ git+https://github.com/evalplus/evalplus"
# Or for the latest stable release
pip install "evalplus[vllm]" --upgrade
```

### Hello-world Evaluation
Run a greedy evaluation on HumanEval using a model served via [vLLM](../infrastructure/vllm.md):

```bash
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset humaneval \
                  --backend vllm \
                  --greedy
```

## CLI Usage and Configuration

EvalPlus provides two primary commands: `evalplus.evaluate` for end-to-end evaluation and `evalplus.codegen` for generation only.

### Common Flags
- `--model`: The model identifier (HuggingFace path or API name).
- `--dataset`: Choose between `humaneval` or `mbpp`.
- `--backend`: Specify the inference backend (`hf`, `vllm`, `openai`, `anthropic`, `google`, `bedrock`, `ollama`).
- `--greedy`: Use greedy decoding (temperature = 0).
- `--base-url`: Specify the API base URL for `openai` or `ollama` backends.
- `--tp`: Set tensor parallel size for `vllm`.

### Example: OpenAI-compatible Backend
```bash
evalplus.evaluate --model "deepseek-chat" \
                  --dataset humaneval \
                  --base-url https://api.deepseek.com \
                  --backend openai --greedy
```

## EvalPerf: Efficiency Evaluation

Beyond correctness, EvalPlus includes **EvalPerf** to measure the execution efficiency of LLM-generated code. This is critical for production use cases where performance matters as much as correctness.

### Setup for EvalPerf
```bash
pip install --upgrade "evalplus[perf,vllm]"
sudo sh -c 'echo 0 > /proc/sys/kernel/perf_event_paranoid' # Enable perf events
```

### Running Efficiency Benchmarks
```bash
evalplus.evalperf --model "ise-uiuc/Magicoder-S-DS-6.7B" --backend vllm
```

## Safe Execution via Docker

Executing LLM-generated code can be dangerous. EvalPlus supports running the evaluation within a sandbox using Docker to protect the host system.

```bash
# Generate samples locally
evalplus.codegen --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                 --dataset humaneval \
                 --backend vllm --greedy

# Execute in Docker container
docker run --rm --pull=always -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval \
           --samples /app/humaneval/ise-uiuc--Magicoder-S-DS-6.7B_vllm_temp_0.0.jsonl
```

## Evaluation Dataset Support

EvalPlus focuses on enhancing standard benchmarks:

| Benchmark | Enhanced Version | Improvement |
|---|---|---|
| [HumanEval](human-eval.md) | HumanEval+ | 80x more test cases |
| [MBPP](mbpp.md) | MBPP+ | 35x more test cases |
| Performance | EvalPerf | Efficiency-focused tasks |

It also provides "Mini" versions (e.g., HumanEval+ mini) for faster iterations when evaluating many model variants.

## Supported Backends

EvalPlus is highly flexible and supports a wide range of inference engines:
- **Local Inference**: `hf` (Transformers), [vLLM](../infrastructure/vllm.md), `gptqmodel`.
- **Local Serving**: [Ollama](../../services/ollama.md).
- **Cloud APIs**: OpenAI, Anthropic, Google Gemini, Amazon Bedrock.
- **Accelerators**: Intel Gaudi (via `hf_gaudi`).

## Typical use cases
- **Rigorous Coding Evaluation**: Testing a model's true coding ability beyond simple benchmarks.
- **Fragility Detection**: Identifying if a model's generated code is robust across many different inputs.
- **Code Efficiency Benchmarking**: Using EvalPerf to measure the execution speed of LLM-generated code.
- **Fine-tuning Validation**: Verifying that fine-tuned models maintain coding robustness.

## Strengths
- **High Rigor**: Expanded test suites (HumanEval+, MBPP+) significantly reduce false positives.
- **Multi-backend Support**: Native integration with [vLLM](../infrastructure/vllm.md), Hugging Face, and major cloud providers.
- **Security**: Official Docker images for isolated code execution.
- **Performance Focused**: Unique ability to benchmark code efficiency via EvalPerf.
- **Industry Standard**: Used by Meta (Llama 3.1), Alibaba (Qwen), and DeepSeek for their coding models.

## Limitations
- **Focus**: Primarily limited to Python and coding-specific tasks.
- **Execution Cost**: Running expanded test suites takes more compute time than original benchmarks.
- **Local Setup**: Some features (like EvalPerf) require sudo/root access or specific kernel configurations.

## When to use it
- When you are developing or fine-tuning an LLM for code generation and need high-confidence metrics.
- When you want to rank models based on their coding robustness and efficiency.
- When comparing against major industry models that use EvalPlus as a baseline.

## When not to use it
- For general knowledge or reasoning tasks (use [MMLU](mmlu.md) or [GPQA](gpqa.md) instead).
- For broad software engineering tasks involving multiple files (use [SWE-bench](swe-bench.md) instead).
- For quick, non-rigorous evaluations of simple code snippets.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [HumanEval](human-eval.md)
- [MBPP](mbpp.md)
- [SWE-bench](swe-bench.md)
- [MMLU](mmlu.md)
- [GPQA](gpqa.md)
- [vLLM](../infrastructure/vllm.md)
- [Ollama](../../services/ollama.md)

## Sources / References
- [Official Website](https://evalplus.github.io/)
- [GitHub Repository](https://github.com/evalplus/evalplus)
- [NeurIPS 2023 Paper](https://openreview.net/forum?id=1qvx610Cu7)
- [COLM 2024 Paper (EvalPerf)](https://openreview.net/forum?id=IBCBMeAhmC)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high

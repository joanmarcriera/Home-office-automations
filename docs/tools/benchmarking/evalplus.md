# EvalPlus

## What it is
EvalPlus is a rigorous evaluation framework for Large Language Models (LLMs) focused on code generation (LLM4Code). It significantly expands existing benchmarks like HumanEval and MBPP with more comprehensive test cases to improve evaluation accuracy.

## What problem it solves
Original coding benchmarks like [HumanEval](human-eval.md) often have very few test cases, allowing fragile or incorrect code to pass. EvalPlus addresses this "under-testing" problem by adding 80x more tests to HumanEval and 35x more tests to MBPP, revealing model weaknesses that simpler benchmarks miss.

## Where it fits in the stack
**Benchmarking**. It is a specialized tool for deeply evaluating the code generation capabilities and efficiency of LLMs.

## Typical use cases
- **Rigorous Coding Evaluation**: Testing a model's true coding ability beyond simple benchmarks.
- **Fragility Detection**: Identifying if a model's generated code is robust across many different inputs.
- **Code Efficiency Benchmarking**: Using the EvalPerf extension to measure the execution speed of LLM-generated code.

## Getting started

### Installation
You can install EvalPlus via pip. For full functionality including vLLM and performance benchmarking:

```bash
pip install "evalplus[vllm,perf]" --upgrade
```

### Hello-world: Functional Evaluation
To evaluate a model locally using the vLLM backend on the HumanEval dataset:

```bash
evalplus.evaluate --model "ise-uiuc/Magicoder-S-DS-6.7B" \
                  --dataset humaneval \
                  --backend vllm \
                  --greedy
```

## Technical details

### CLI Usage
EvalPlus provides several command-line tools for different stages of the evaluation pipeline:

- `evalplus.evaluate`: The primary entry point for end-to-end generation and evaluation.
- `evalplus.codegen`: Used for code generation only (useful when separation of concerns is needed).
- `evalplus.evalperf`: Specialized tool for code efficiency and performance benchmarking.

### Docker Execution (Safe Sandboxing)
For security, it is highly recommended to run the evaluation (which involves executing model-generated code) inside a Docker container:

```bash
# Generate samples locally first
evalplus.codegen --model "gpt-4o" --dataset humaneval --backend openai

# Run evaluation inside the EvalPlus sandbox
docker run --rm -v $(pwd)/evalplus_results:/app ganler/evalplus:latest \
           evalplus.evaluate --dataset humaneval \
           --samples /app/humaneval/openai--gpt-4o_temp_0.0.jsonl
```

### Supported Backends
EvalPlus supports a wide range of inference backends:
- **vLLM**: Highly optimized for local throughput.
- **Hugging Face**: Standard `transformers` implementation.
- **OpenAI / Anthropic / Gemini**: Cloud-based API providers.
- **Ollama**: Local model serving.
- **Bedrock / hf_gaudi**: Enterprise and specialized hardware support.

## Strengths
- **High Rigor**: Expanded test suites (HumanEval+, MBPP+) significantly reduce false positives.
- **Multi-backend Support**: Supports evaluation via vLLM, Hugging Face, OpenAI, Anthropic, Gemini, and Ollama.
- **Security**: Supports safe code execution within Docker containers to protect the host system.
- **Performance Evaluation**: Includes EvalPerf for measuring code efficiency.

## Limitations
- **Focus**: Primarily limited to Python and coding-specific tasks.
- **Execution Cost**: Running 80x more tests naturally takes more time and compute than the original benchmarks.

## When to use it
- When you are developing or fine-tuning an LLM for code generation and need high-confidence metrics.
- When you want to rank models based on their coding robustness and efficiency.
- When comparing against major industry models (many of which, like Llama 3.1 and Qwen 2.5, use EvalPlus).

## When not to use it
- For general knowledge or reasoning tasks (use [MMLU](mmlu.md) or [GPQA](gpqa.md) instead).
- For quick, non-rigorous evaluations of simple code snippets.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [HumanEval](human-eval.md)
- [MBPP](mbpp.md)
- [SWE-bench](swe-bench.md)
- [vLLM](../infrastructure/vllm.md)
- [OpenCompass](opencompass.md)
- [HELM](helm.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)

## Sources / References
- [Official Website](https://evalplus.github.io/)
- [GitHub Repository](https://github.com/evalplus/evalplus)
- [NeurIPS 2023 Paper](https://openreview.net/forum?id=1qvx610Cu7)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high

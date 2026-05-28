# HELM (Holistic Evaluation of Language Models)

## What it is
HELM (Holistic Evaluation of Language Models) is an open-source evaluation framework developed by Stanford University's Center for Research on Foundation Models (CRFM). It is designed to provide a comprehensive, transparent, and multi-dimensional assessment of Large Language Models (LLMs) and Multimodal Models.

## What problem it solves
LLM evaluation is often narrow, focusing only on accuracy for a few tasks. HELM addresses this by evaluating models across a wide range of "scenarios" (tasks) and "metrics" (accuracy, fairness, safety, efficiency, copyright, etc.), providing a holistic view of model behavior. It mitigates "leaderboard hacking" by using a broad, standardized scenario-metric grid.

## Where it fits in the stack
**Category**: [Benchmarking](index.md). It is the industry-standard framework used by researchers and regulators to perform deep-dive evaluations of foundation models before and after deployment.

## Typical use cases
- **Holistic Model Assessment**: Evaluating a new model version (e.g., Llama 4 or GPT-5.2) across accuracy, safety, and bias simultaneously.
- **Regulatory Compliance**: Using **AIR-Bench** (AI Safety Benchmark) to align model behavior with emerging government regulations and company policies.
- **VLM Benchmarking**: Using **VHELM** to evaluate vision-language models on visual reasoning and perception.
- **Safety and Fairness Auditing**: Specifically checking for toxicity and bias across 314+ granular risk categories in the lowest tier of the AIR-Bench taxonomy.

## Getting started

### Installation
It is recommended to install HELM into a virtual environment with Python >= 3.10.

```bash
# Install the base HELM package (v0.5.x for 2026 support)
pip install crfm-helm

# Install additional dependencies for multimodal (VHELM/HEIM) or specific metrics
pip install "crfm-helm[vlm,summarization]"
```

### Hello-world task
Evaluate GPT-2 on a small subset of the MMLU philosophy subject. Note that for 2026 versions, `trust_remote_code` is disabled by default for security; it must be explicitly enabled in `model_deployments.yaml` if needed.

```bash
# Run the benchmark (limited to 10 instances)
helm-run --run-entries mmlu:subject=philosophy,model=openai/gpt2 --suite my-suite --max-eval-instances 10

# Summarize the results
helm-summarize --suite my-suite

# View the results in the web UI
helm-server --suite my-suite
```
The results will be available at `http://localhost:8000/`.

## CLI Reference

HELM provides three primary CLI tools for the evaluation lifecycle:

### `helm-run`
Executes the evaluation. You can specify what to run using the `--run-entries` flag (for quick commands) or a `--conf-file` (for complex batch runs).

```bash
# Execute a specific scenario and model
helm-run --run-entries med_qa:model=openai/gpt2 --suite med-suite --max-eval-instances 10

# Execute using a configuration file
helm-run --conf-file run_entries.conf --suite production-suite
```

### `helm-summarize`
Processes the raw outputs from `helm-run` into a summary format that can be visualized or compared.

```bash
# Summarize a completed suite
helm-summarize --suite med-suite
```

### `helm-server`
Launches a local web server to browse the results.
- `--suite`: Specify the suite to serve.
- `--export-path`: (New in 2026) Export the results as a static website for hosting on GitHub Pages or an internal dashboard.

```bash
# Start the UI server and export to a directory
helm-server --suite med-suite --export-path ./docs/eval-report
```

## Specialized Evaluations (2026 Update)

HELM has expanded into specialized, high-concurrency domains:

- **HELM Capabilities**: A curated set of scenarios for measuring the general capabilities of the latest 2026 models (Grok 4.1, Claude 4.6, GPT-5.2).
- **AIR-Bench (AI Safety)**: The first safety benchmark aligned with global government regulations, featuring a four-tiered safety taxonomy.
- **VHELM (Vision-Language Models)**: Evaluates multimodal models like Gemini 3.1 Pro or Claude Opus 4.6 on visual perception and reasoning.
- **HEIM (Text-To-Image)**: Focuses on image generation models (Sora, Midjourney v7) for aesthetics and alignment.
- **MedHELM**: Specialized medical evaluation using MedQA and clinical reasoning scenarios.

## Strengths
- **Multi-dimensional**: Covers 314+ risk categories and dozens of performance metrics.
- **Security-First**: `trust_remote_code` is now disabled by default in `HuggingFaceClient`.
- **LiteLLM Integration**: (2026) Direct support for LiteLLM allows evaluating models across any provider without complex configuration.
- **Transparency**: Full visibility into prompts, model responses, and metric calculations.

## Limitations
- **High Complexity**: Setting up and running full HELM suites is computationally expensive.
- **API Dependency**: Extensive evaluations of closed models incur high API costs.
- **Infrastructure Requirements**: Local evaluation of large models requires significant VRAM (supported by [vLLM](../infrastructure/vllm.md)).

## When to use it
- When you need a highly rigorous, academic-grade evaluation of a foundation model.
- For safety and regulatory audits (using AIR-Bench).
- When participating in or reproducing results for major LLM leaderboards.

## When not to use it
- For quick, "vibe-check" style evaluations of a specific application prompt.
- For evaluating specific RAG pipelines (consider [RAGAS](https://github.com/explodinggradients/ragas) or [DeepEval](https://github.com/confident-ai/deepeval)).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free software (API/compute costs apply)

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [OpenCompass](opencompass.md)
- [MMLU](mmlu.md)
- [GPQA](gpqa.md)
- [Human Eval](human-eval.md)
- [GSM8K](gsm8k.md)
- [Chatbot Arena](chatbot-arena.md)
- [LangSmith](langsmith.md)
- [vLLM](../infrastructure/vllm.md)
- [LiteLLM](../../services/litellm.md)
- [AIR-Bench](https://crfm.stanford.edu/helm/air-bench/latest/)

## Sources / References
- [Official Website](https://crfm.stanford.edu/helm/)
- [GitHub Repository](https://github.com/stanford-crfm/helm)
- [Stanford CRFM Blog](https://crfm.stanford.edu/2022/11/17/helm.html)
- [AIR-Bench Safety Benchmark](https://crfm.stanford.edu/helm/air-bench/latest/)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high

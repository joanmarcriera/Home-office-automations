# HELM (Holistic Evaluation of Language Models)

## What it is
HELM (Holistic Evaluation of Language Models) is an open-source evaluation framework developed by Stanford University's Center for Research on Foundation Models (CRFM). It is designed to provide a comprehensive, transparent, and multi-dimensional assessment of Large Language Models (LLMs).

## What problem it solves
LLM evaluation is often narrow, focusing only on accuracy for a few tasks. HELM addresses this by evaluating models across a wide range of "scenarios" (tasks) and "metrics" (accuracy, fairness, safety, efficiency, etc.), providing a holistic view of model behavior rather than just a single score.

## Where it fits in the stack
**Benchmarking**. It is a major framework used by researchers and engineers to perform deep-dive evaluations of foundation models.

## Typical use cases
- **Holistic Model Assessment**: Evaluating a new model version across accuracy, safety, and bias simultaneously.
- **Comparison of Foundation Models**: Using standardized scenarios to compare models like GPT-4, Claude, and Llama on equal footing.
- **Safety and Fairness Auditing**: Specifically checking for toxicity and bias in model responses across different demographics.

## Getting started

### Installation

It is recommended to install HELM into a virtual environment with Python >= 3.10.

```bash
# Install the base HELM package
pip install crfm-helm

# Install additional dependencies for multimodal (VHELM/HEIM) support
pip install "crfm-helm[vlm]"
```

### Hello-world task

Evaluate GPT-2 on a small subset of the MMLU philosophy subject:

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
Launches a local web server to browse the results, inspect individual prompts, and view the leaderboard.

```bash
# Start the UI server
helm-server --suite med-suite
```

## Specialized Evaluations

HELM has expanded beyond general text models into specialized domains:

- **VHELM (Vision-Language Models)**: Evaluates VLMs on visual perception, reasoning, and safety. Uses benchmarks like MMMU and aggregates results across 9 distinct aspects.
- **HEIM (Holistic Evaluation of Text-To-Image Models)**: Focuses on image generation models, measuring alignment, quality, and aesthetics.
- **MedHELM**: A specialized version for medical tasks, incorporating datasets like MedQA to assess model performance in clinical contexts.

## Strengths
- **Multi-dimensional**: Moves beyond simple accuracy to include metrics like calibration, robustness, and fairness.
- **Scenario-Metric Grid**: Uses a systematic approach to ensure broad coverage of tasks.
- **Transparency**: Provides full visibility into the prompts used and the individual model responses.
- **Active Research**: Regularly updated by Stanford with new datasets and the latest models.

## Limitations
- **High Complexity**: Setting up and running full HELM evaluations is computationally expensive and complex.
- **API Dependency**: Many scenarios require access to external model APIs, which can incur high costs.
- **Learning Curve**: The framework's modularity makes it powerful but also harder to master than simpler evaluation scripts.

## When to use it
- When you need a highly rigorous, academic-grade evaluation of a foundation model.
- When you are concerned with safety, bias, or robustness in addition to raw performance.
- When participating in or reproducing results for major LLM leaderboards.

## When not to use it
- For quick, "vibe-check" style evaluations of a specific application prompt.
- If you have very limited compute or budget for API calls.
- For evaluating specific RAG pipelines (consider [RAGAS](https://github.com/explodinggradients/ragas) instead).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (but compute/API costs for running evals apply)
- **Self-hostable**: Yes

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

## Sources / References
- [Official Website](https://crfm.stanford.edu/helm/)
- [GitHub Repository](https://github.com/stanford-crfm/helm)
- [Stanford CRFM Blog](https://crfm.stanford.edu/2022/11/17/helm.html)

## Contribution Metadata
- Last reviewed: 2026-03-21
- Confidence: high

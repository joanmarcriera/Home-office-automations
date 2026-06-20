# HELM (Holistic Evaluation of Language Models)

## What it is
HELM (Holistic Evaluation of Language Models) is an open-source evaluation framework developed by Stanford University's Center for Research on Foundation Models (CRFM). It is designed to provide a comprehensive, transparent, and multi-dimensional assessment of Large Language Models (LLMs) and Vision-Language Models (VLMs). In June 2026, it is one of the most respected academic benchmarks for foundation models.

## What problem it solves
LLM evaluation is often narrow, focusing only on accuracy for a few tasks. HELM addresses this by evaluating models across a wide range of "scenarios" (tasks) and "metrics" (accuracy, fairness, safety, efficiency, etc.). It solves the problem of "performance gaming" by providing a holistic view of model behavior rather than just a single, easily-optimizable score.

## Where it fits in the stack
**Benchmarking Layer**. It is a major framework used by researchers and engineers to perform deep-dive evaluations of foundation models. It serves as the "gold standard" for academic-grade verification.

## Typical use cases
- **Holistic Model Assessment**: Evaluating a new model version (e.g., Llama-4-70B) across accuracy, safety, and bias simultaneously.
- **Comparison of Foundation Models**: Using standardized scenarios to compare models like GPT-5.5 and Claude 4.8 on equal footing.
- **Safety and Fairness Auditing**: Specifically checking for toxicity and bias in model responses across different demographics and languages.
- **Agentic Intelligence Testing**: Utilizing **AIR-Bench** (integrated in 2026) to measure multi-step reasoning and tool-use capabilities.

## Strengths
- **Multi-dimensional**: Moves beyond simple accuracy to include metrics like calibration, robustness, and fairness.
- **Scenario-Metric Grid**: Uses a systematic approach to ensure broad coverage of tasks.
- **Transparency**: Provides full visibility into the prompts used and the individual model responses.
- **LiteLLM Integration**: HELM v0.6+ supports [LiteLLM](../../services/litellm.md) as a backend, enabling benchmarking of any model compatible with the OpenAI API via a local proxy.
- **Academic Rigor**: Regularly updated by Stanford with new datasets and the latest models (v0.6.x as of June 2026).

## Limitations
- **High Complexity**: Setting up and running full HELM evaluations is computationally expensive and requires significant configuration.
- **API Dependency**: Many scenarios require access to external model APIs, which can incur high costs during large-scale runs.
- **Learning Curve**: The framework's modularity makes it powerful but also harder to master than simpler evaluation scripts like [OpenCompass](opencompass.md).

## When to use it
- When you need a highly rigorous, academic-grade evaluation of a foundation model's core capabilities.
- When you are concerned with safety, bias, or robustness in addition to raw performance.
- When participating in or reproducing results for major LLM research papers and leaderboards.
- For evaluating the general "intelligence" and "alignment" of a model before deploying it in agentic roles.

## When not to use it
- For quick, "vibe-check" style evaluations of a specific application prompt.
- If you have very limited compute or budget for API calls.
- For evaluating specific RAG pipelines (consider [RAGAS](../process_understanding/ragas.md) instead).
- If you need real-time monitoring of model performance in production (use [Braintrust](../process_understanding/braintrust.md) or [Arize](../process_understanding/arize-ai.md)).

## Getting started

### Installation
It is recommended to install HELM into a virtual environment with Python >= 3.11.

```bash
# Install the base HELM package (v0.6.x June 2026)
pip install crfm-helm

# Install additional dependencies for multimodal (VHELM/HEIM) support
pip install "crfm-helm[vlm]"
```

### Hello-world Evaluation
Evaluate a model (e.g., Llama-4-8B) on a small subset of the MMLU philosophy subject:

```bash
# Run the benchmark (limited to 10 instances)
helm-run --run-entries mmlu:subject=philosophy,model=meta/llama-4-8b --suite my-suite --max-eval-instances 10

# Summarize the results
helm-summarize --suite my-suite

# View the results in the web UI
helm-server --suite my-suite
```
The results will be available at `http://localhost:8000/`.

## CLI examples
HELM provides primary CLI tools for the evaluation lifecycle:

```bash
# Execute evaluation for medical QA
helm-run --run-entries med_qa:model=openai/gpt-5.5 --suite med-suite --max-eval-instances 10

# Run evaluation using a configuration file for complex batch runs
helm-run --conf-file run_entries.conf --suite production-suite

# Process raw outputs into summaries
helm-summarize --suite med-suite

# Start the web-based leaderboard UI
helm-server --suite med-suite --port 8080
```

## Specialized Evaluations (June 2026)
- **AIR-Bench**: Integrated for **Agentic Intelligence and Reasoning**, evaluating multi-step tasks and tool-use.
- **VHELM (Vision-Language Models)**: Evaluates VLMs on visual perception, reasoning, and safety (MMMU, etc.).
- **HEIM (Holistic Evaluation of Text-To-Image Models)**: Focuses on image generation models, measuring alignment and aesthetics.
- **MedHELM**: Specialized version for medical tasks, assessing clinical context performance.

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md) — Another major open-source benchmarking tool.
- [OpenCompass](opencompass.md) — Comprehensive evaluation platform from OpenMMLab.
- [VAKRA](vakra.md) — Executable benchmark for agentic tool-use.
- [MMLU](mmlu.md) / [GPQA](gpqa.md) — Core datasets used within HELM.
- [RAGAS](../process_understanding/ragas.md) — Specialized evaluation for RAG.
- [LiteLLM](../../services/litellm.md) — Recommended backend for routing HELM model calls.
- [Model Context Protocol](../../tools/automation_orchestration/mcp.md) — Standard for agentic tool integration.

## Sources / references
- [Official Website](https://crfm.stanford.edu/helm/)
- [GitHub Repository](https://github.com/stanford-crfm/helm)
- [Stanford CRFM Blog](https://crfm.stanford.edu/2022/11/17/helm.html)
- [arXiv: Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110)

## Contribution Metadata
- Last reviewed: 2026-06-20
- Confidence: high

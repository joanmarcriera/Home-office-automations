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

## Sources / References
- [Official Website](https://crfm.stanford.edu/helm/)
- [GitHub Repository](https://github.com/stanford-crfm/helm)
- [Stanford CRFM Blog](https://crfm.stanford.edu/2022/11/17/helm.html)

## Contribution Metadata
- Last reviewed: 2026-03-21
- Confidence: high

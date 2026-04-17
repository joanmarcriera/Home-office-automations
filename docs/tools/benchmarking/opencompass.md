# OpenCompass

## What it is
OpenCompass is a comprehensive, one-stop platform designed for evaluating the capabilities of large language models (LLMs) and vision-language models (VLMs). It provides a complete evaluation pipeline, including dataset preparation, evaluation scripts, and leaderboards.

## What problem it solves
Evaluating modern large models is complex, requiring diverse datasets and multiple evaluation paradigms (e.g., zero-shot, few-shot, CoT). OpenCompass standardizes this process, providing a reproducible and extensible framework that supports over 100 datasets and various model backends.

## Where it fits in the stack
**Benchmarking**. It serves as an evaluation toolkit and platform for comparing model performance across a wide range of tasks.

## Typical use cases
- **Model Development**: Benchmarking in-house models against industry standards during training.
- **Model Selection**: Comparing different open-source or API-based models to find the best fit for a specific application.
- **Academic Research**: Reproducing evaluation results for papers and contributing new datasets to the community.

## Strengths
- **Comprehensive Coverage**: Supports 100+ datasets covering linguistics, knowledge, reasoning, coding, and multi-modality.
- **Flexible Architecture**: Supports various evaluation paradigms (Zero-shot, Few-shot, CoT, LLM-as-a-judge).
- **High Performance**: Integrates with acceleration backends like vLLM, LMDeploy, and ModelScope for distributed evaluation.
- **Active Community**: Frequently updated with new benchmarks and model support.

## Limitations
- **Complexity**: The extensive configuration options and features can lead to a steeper learning curve for beginners.
- **Resource Intensive**: Running full-scale evaluations on large models requires significant local compute or API credits.

## When to use it
- When you need a standardized, reproducible way to evaluate models across dozens of different dimensions.
- When you want to contribute to or compare against public leaderboards (CompassRank).
- When evaluating Vision-Language Models (VLMs) alongside LLMs.

## When not to use it
- For very simple, single-task evaluations where a lightweight script might suffice.
- If you only need to evaluate basic RAG performance (consider [DeepEval](https://github.com/confident-ai/deepeval) or [RAGAS](https://github.com/explodinggradients/ragas) instead).

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Related tools / concepts
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [HELM](helm.md)
- [vLLM](../infrastructure/vllm.md)
- [Chatbot Arena](chatbot-arena.md)

## Sources / References
- [Official Website](https://opencompass.org.cn/)
- [GitHub Repository](https://github.com/open-compass/opencompass)
- [Introduction by Jimmy Song](https://jimmysong.io/ai/opencompass/)

## Contribution Metadata
- Last reviewed: 2026-03-21
- Confidence: high

# Model Comparison and Evaluation

Understanding how different AI models perform relative to each other is crucial for selecting the right tool for a specific task. This page provides a guide to the platforms, leaderboards, and metrics used to evaluate and compare Large Language Models (LLMs).

## Side-by-side Comparison Platforms

Interactive platforms allow users to test multiple models on the same prompt simultaneously, providing direct insight into their different reasoning styles and output qualities.

- **[Chatbot Arena (LMSYS)](../tools/benchmarking/chatbot-arena.md)**: A crowdsourced open platform where users chat with two anonymous models and vote on which one is better. This provides a "blind" test of human preference, which is often a more reliable indicator of general helpfulness than automated benchmarks.
- **[OpenRouter Playground](https://openrouter.ai/playground)**: While primarily an API aggregator, OpenRouter provides a playground where you can quickly switch between dozens of different models to compare their responses to the same prompt.

## Public Leaderboards

Leaderboards aggregate results from multiple benchmarks to provide a macro view of the AI landscape.

- **[LMSYS Arena Leaderboard](https://chat.lmsys.org/?leaderboard)**: The definitive leaderboard for human preference. It uses an Elo rating system (similar to chess) to rank models based on thousands of pairwise comparisons.
- **[Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)**: The primary leaderboard for open-source (open-weight) models. It evaluates models on a battery of automated benchmarks including MMLU, ARC, and GSM8K.
- **[LiveCodeBench](https://livecodebench.github.io/leaderboard.html)**: A leaderboard focused on code generation that uses problems from periodic competitive programming contests to prevent data contamination (where the model might have seen the test problems during training).

## Common Evaluation Metrics

When reviewing benchmark results, you will encounter several standardized metrics. Each focuses on a different aspect of model capability.

### General Knowledge and Reasoning
- **MMLU (Massive Multitask Language Understanding)**: Tests a model's knowledge across 57 subjects in STEM, the humanities, social sciences, and more. It is the most common "all-purpose" benchmark.
- **[GPQA (Graduate-Level Google-Proof Q&A)](../tools/benchmarking/gpqa.md)**: A very difficult benchmark written by experts (PhDs) in biology, physics, and chemistry. Designed to be hard even for non-expert humans with internet access.

### Mathematics
- **[GSM8K (Grade School Math 8K)](../tools/benchmarking/gsm8k.md)**: 8,500 grade-school math word problems. It tests multi-step arithmetic reasoning.
- **MATH**: More advanced mathematics problems ranging from algebra to calculus.

### Coding
- **[HumanEval](../tools/benchmarking/human-eval.md)**: 164 handwritten programming problems from OpenAI. Measures the ability to solve basic algorithmic tasks.
- **[MBPP (Mostly Basic Python Problems)](../tools/benchmarking/mbpp.md)**: Around 1,000 entry-level Python programming problems.
- **[SWE-bench](../tools/benchmarking/swe-bench.md)**: A high-bar benchmark where models must resolve real GitHub issues by providing functional code patches.

### Performance and Efficiency
- **Tokens per Second (TPS)**: A measure of inference speed.
- **Time to First Token (TTFT)**: How quickly the model starts generating a response after receiving a prompt.
- **[LLMperf](../tools/benchmarking/llmperf.md)**: A tool for measuring these operational metrics across different API providers.

### Core Metrics Defined
While benchmarks provide a score, they often rely on these underlying statistical metrics:
- **Accuracy / Exact Match (EM)**: The percentage of responses that are exactly correct (common in math and multiple-choice).
- **F1 Score**: A balance between precision (correctness) and recall (completeness), often used in classification or extraction tasks.
- **BLEU / ROUGE**: Automated metrics that measure text similarity between a model's output and a reference "gold standard" (common in translation and summarization).
- **Pass@k**: Used in coding benchmarks like [HumanEval](../tools/benchmarking/human-eval.md) to measure the probability that at least one of *k* generated samples passes all tests.

## Practical Interpretation

To choose the best model for your practical scenario, consider the following:

1.  **Define your "North Star" Metric**: If you are building a coding assistant, prioritize **SWE-bench** or **HumanEval** over general MMLU scores.
2.  **Look for Contamination-Resistance**: Be wary of models that show suspiciously high scores on older benchmarks like GSM8K while performing poorly on newer, private, or "live" benchmarks (like LiveCodeBench).
3.  **Human Preference vs. Automation**: A model might have a high MMLU score but feel "robotic" or overly verbose. Check the **Chatbot Arena Elo** for a sense of how the model actually feels to interact with.
4.  **Cost-Performance Tradeoff**: Use the **[API Pricing & Free Tier Matrix](api_pricing_free_tiers.md)** alongside these benchmarks to find the model that provides the necessary capability at the lowest cost.

For task-level routing decisions such as when to use Haiku vs Sonnet vs Opus, or GPT-5.4 `low` vs `medium` vs `high` vs `xhigh`, use the dedicated [Model Routing Guide](model_routing_guide.md).

## Related tools / concepts
- [Benchmarking Tool Catalogue](../tools/benchmarking/index.md)
- [Model Classes](model_classes.md)
- [LM Evaluation Harness](../tools/benchmarking/lm-evaluation-harness.md)
- [Qwen](../tools/ai_knowledge/qwen.md)

## Sources / References
- [Chatbot Arena (LMSYS)](https://chat.lmsys.org/)
- [Hugging Face Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)
- [LiveCodeBench](https://livecodebench.github.io/leaderboard.html)

## Contribution Metadata
- Last reviewed: 2026-03-06
- Confidence: high

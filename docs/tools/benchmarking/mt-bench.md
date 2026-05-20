# MT-Bench

## What it is
MT-Bench is a benchmark designed to evaluate the multi-turn conversational capabilities of Large Language Models (LLMs). It consists of 80 high-quality, multi-turn questions across eight categories: writing, roleplay, extraction, reasoning, math, coding, knowledge I (STEM), and knowledge II (humanities/social science).

## What problem it solves
Many traditional benchmarks only evaluate single-turn responses, failing to capture a model's ability to maintain context, follow instructions across multiple exchanges, and handle the dynamic nature of real-world conversations. MT-Bench specifically tests the "follow-up" capability of models.

## Where it fits in the stack
**Benchmarking**. It is a core component of the LMSYS FastChat evaluation framework, providing a more rigorous test of conversational flow than single-turn evaluations.

## Typical use cases
- **Conversational AI Evaluation**: Assessing how well a chatbot handles follow-up questions and maintains context.
- **Model Comparison**: Ranking chat-tuned models based on their ability to handle complex, multi-step instructions.
- **LLM-as-a-Judge Validation**: MT-Bench is often used with GPT-4 as a judge to provide automated, scalable scoring that correlates with human judgment.

## Getting started

### 1. Installation
MT-Bench is part of the `fastchat` repository.

```bash
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip install -e ".[model_worker,llm_judge]"
```

### 2. Generating Model Answers
Generate answers for the 80 questions in MT-Bench using your local model or API.

```bash
python fastchat/llm_judge/gen_model_answer.py \
    --model-path lmsys/vicuna-7b-v1.5 \
    --model-id vicuna-7b-v1.5
```

### 3. Grading with LLM-as-a-Judge
Use a strong model (like GPT-4) to grade the responses.

```bash
export OPENAI_API_KEY="your_api_key"
python fastchat/llm_judge/gen_judgment.py \
    --model-list vicuna-7b-v1.5 \
    --parallel 2
```

### 4. Viewing Results
```bash
python fastchat/llm_judge/show_result.py
```

## Technical Methodology
- **Two-Turn Structure**: Each question consists of an initial prompt and a pre-defined follow-up question that depends on the model's first answer.
- **Categories**: 10 questions per category (Writing, Roleplay, Extraction, Reasoning, Math, Coding, STEM, Humanities).
- **Scoring**: The judge model (GPT-4) assigns a score from 1 to 10 for each turn.
- **Reference Models**: Scores are often compared against "anchor" models like GPT-3.5 and GPT-4.

## Technical Architecture
MT-Bench uses the **LLM-as-a-Judge** paradigm.
- **Judge Model**: Usually GPT-4, which has been shown to have high agreement with human experts.
- **Prompt Templates**: The judge is given specific templates for "pairwise comparison" (comparing two models) or "single answer grading" (scoring one model).
- **Control for Biases**: Techniques like swapping the order of models in pairwise comparisons are used to mitigate "position bias."

## Strengths
- **Multi-turn Focus**: Specifically designed to test conversation depth.
- **Diverse Categories**: Covers a wide range of tasks from coding to roleplay.
- **Strong Human Correlation**: GPT-4 based scoring on MT-Bench shows over 80% agreement with human experts.
- **Open Dataset**: The questions and human judgments are publicly available for research.

## Limitations
- **Judge Bias**: If using an LLM as a judge, it may inherit the biases of that judge (e.g., preference for certain styles or lengths).
- **Small Sample Size**: With only 80 questions, the results can have higher variance than larger benchmarks.
- **Static Nature**: Like all fixed benchmarks, it risks data contamination as it is widely included in training sets.

## When to use it
- When evaluating chat-tuned models where multi-turn interaction is a primary use case.
- When you need an automated conversational benchmark that aligns closely with human preference.

## When not to use it
- For evaluating base (non-chat-tuned) models that are not designed for dialogue.
- When you only need to measure narrow technical capabilities like raw code execution or mathematical proof (use specialized benchmarks instead).

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) - The primary leaderboard for human preferences.
- [AlpacaEval](alpaca-eval.md) - Simulator-based evaluator for instruction following.
- [GSM8K](gsm8k.md) - Basic math reasoning.
- [MATH Benchmark](math-benchmark.md) - Advanced mathematical competition problems.
- [HumanEval](human-eval.md) - Core coding benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Standard framework for single-turn benchmarks.
- [OpenCompass](opencompass.md) - Comprehensive evaluation platform that supports MT-Bench.

## Sources / references
- [FastChat GitHub (LLM Judge)](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)
- [MT-Bench Paper: "Judging LLM-as-a-judge" (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [LMSYS Leaderboard](https://arena.lmsys.org/leaderboard)

## Contribution Metadata
- Last reviewed: 2026-05-20
- Confidence: high

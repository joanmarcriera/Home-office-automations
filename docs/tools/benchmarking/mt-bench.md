# MT-Bench

## What it is
MT-Bench is a benchmark designed to evaluate the multi-turn conversational capabilities of Large Language Models (LLMs). It consists of 80 high-quality, multi-turn questions across eight categories: writing, roleplay, extraction, reasoning, math, coding, knowledge I (STEM), and knowledge II (humanities/social science). In the June 2026 landscape, it remains a foundational metric for verifying the conversational consistency of frontier models like Claude 4.8 Opus and GPT-5.5.

## What problem it solves
Many traditional benchmarks only evaluate single-turn responses, failing to capture a model's ability to maintain context, follow instructions across multiple exchanges, and handle the dynamic nature of real-world conversations. MT-Bench specifically tests the "follow-up" capability of models, addressing the "goldfish memory" problem in earlier LLM generations.

## Where it fits in the stack
**Benchmarking**. It is a core component of the LMSYS FastChat evaluation framework, providing a more rigorous test of conversational flow than single-turn evaluations like MMLU.

## Typical use cases
- **Conversational AI Evaluation**: Assessing how well a chatbot handles follow-up questions and maintains context.
- **Model Comparison**: Ranking chat-tuned models (e.g., comparing Claude 4.8 vs. GPT-5.5) based on their ability to handle complex, multi-step instructions.
- **LLM-as-a-Judge Validation**: MT-Bench is often used with strong models as judges to provide automated, scalable scoring.

## Strengths
- **Multi-turn Focus**: Specifically designed to test conversation depth and instruction adherence over multiple turns.
- **Diverse Categories**: Covers a wide range of tasks from coding to roleplay, ensuring a balanced evaluation.
- **Strong Human Correlation**: Scoring on MT-Bench shows high agreement (over 80%) with human expert preferences.
- **Open Dataset**: The questions and human judgments are publicly available for transparency and research.

## Limitations
- **Judge Bias**: If using an LLM as a judge (e.g., GPT-4 or GPT-5.5), it may inherit the biases of that judge (e.g., preference for verbosity or certain styles).
- **Small Sample Size**: With only 80 questions, the results can have higher variance than larger benchmarks like AlpacaEval.
- **Static Nature**: Like all fixed benchmarks, it risks data contamination if questions are leaked into training sets.

## When to use it
- When evaluating chat-tuned models where multi-turn interaction is a primary use case.
- When you need an automated conversational benchmark that aligns closely with human preference.
- For internal testing of "System 2" reasoning models in conversational contexts.

## When not to use it
- For evaluating base (non-chat-tuned) models that are not designed for dialogue.
- When you only need to measure narrow technical capabilities like raw code execution (use [BigCodeBench](bigcodebench.md) instead).
- When high-stakes safety evaluation is the primary goal.

## Getting started

### 1. Installation
MT-Bench is part of the `fastchat` repository.

```bash
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip install -e ".[model_worker,llm_judge]"
```

### 2. Generating Model Answers
Generate answers for the 80 questions using your local model or API.

```bash
python fastchat/llm_judge/gen_model_answer.py \
    --model-path anthropic/claude-4-8-opus \
    --model-id claude-4-8-opus
```

### 3. Grading with LLM-as-a-Judge
Use a strong model (like GPT-5.5) to grade the responses.

```bash
export OPENAI_API_KEY="your_api_key"
python fastchat/llm_judge/gen_judgment.py \
    --model-list claude-4-8-opus \
    --parallel 4
```

## CLI examples
The FastChat evaluation suite provides several CLI tools for MT-Bench.

```bash
# Show results summary
python fastchat/llm_judge/show_result.py

# Generate answers for a specific category
python fastchat/llm_judge/gen_model_answer.py --category reasoning --model-id my-custom-model

# Run judgments in parallel to save time
python fastchat/llm_judge/gen_judgment.py --model-list model1 model2 --parallel 8

# Export judgments to a JSON file
python fastchat/llm_judge/gen_judgment.py --model-list model1 --output-file results.json
```

## API examples
While MT-Bench is primarily a CLI-driven benchmark, it can be integrated into Python evaluation pipelines.

```python
import json
from fastchat.llm_judge.common import load_questions, load_model_answers

# Load MT-Bench questions
questions = load_questions("fastchat/llm_judge/data/mt_bench/question.jsonl")

# Access a specific multi-turn question
first_question = questions[0]
print(f"Turn 1: {first_question['turns'][0]}")
print(f"Turn 2: {first_question['turns'][1]}")

# Custom logic to process model answers
answers = load_model_answers("fastchat/llm_judge/data/mt_bench/model_answer/claude-4-8-opus.jsonl")
```

## Technical Methodology
- **Two-Turn Structure**: Each question consists of an initial prompt and a pre-defined follow-up question that depends on the model's first answer.
- **Categories**: 10 questions per category (Writing, Roleplay, Extraction, Reasoning, Math, Coding, STEM, Humanities).
- **Scoring**: The judge model (GPT-4 or GPT-5.5) assigns a score from 1 to 10 for each turn.
- **Reference Models**: Scores are often compared against "anchor" models like GPT-3.5 and GPT-4.

## Technical Architecture
MT-Bench uses the **LLM-as-a-Judge** paradigm.
- **Judge Model**: Usually GPT-4 or GPT-5.5, which has been shown to have high agreement with human experts.
- **Prompt Templates**: The judge is given specific templates for "pairwise comparison" or "single answer grading."
- **Control for Biases**: Techniques like swapping the order of models in pairwise comparisons are used to mitigate "position bias."

## Related tools / concepts
- [Chatbot Arena](chatbot-arena.md) - The primary leaderboard for human preferences.
- [AlpacaEval](alpaca-eval.md) - Simulator-based evaluator for instruction following.
- [GSM8K](gsm8k.md) - Basic math reasoning benchmark.
- [MATH Benchmark](math-benchmark.md) - Advanced mathematical competition problems.
- [HumanEval](human-eval.md) - Core coding benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Standard framework for single-turn benchmarks.
- [OpenCompass](opencompass.md) - Comprehensive evaluation platform.
- [BigCodeBench](bigcodebench.md) - Realistic code generation benchmark.

## Sources / references
- [FastChat GitHub (LLM Judge)](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)
- [MT-Bench Paper: "Judging LLM-as-a-judge" (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [LMSYS Leaderboard](https://arena.lmsys.org/leaderboard)

## Contribution Metadata
- Last reviewed: 2026-06-15
- Confidence: high

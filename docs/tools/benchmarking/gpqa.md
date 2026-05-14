# GPQA (Graduate-Level Google-Proof Q&A)

## What it is
GPQA is a challenging benchmark for evaluating high-level reasoning and knowledge in LLMs. It consists of 448 multiple-choice questions written by experts (PhD-level) in biology, physics, and chemistry. The questions are designed to be "Google-proof," meaning they are difficult even for non-expert humans to solve with access to the internet. Key metrics include accuracy (percentage of correct answers) and self-consistency.

## What problem it solves
Measures whether LLMs possess deep, expert-level scientific knowledge and reasoning that cannot be trivially looked up, providing a more rigorous assessment than general knowledge benchmarks like MMLU which are increasingly appearing in training sets.

## Where it fits in the stack
**Benchmarking**. Used as a reference benchmark for evaluating advanced reasoning and scientific competence in state-of-the-art LLMs.

## Typical use cases
- Evaluating LLM performance on graduate-level scientific reasoning
- Comparing models on tasks that require genuine understanding rather than surface-level retrieval
- Assessing progress toward expert-level AI capabilities in STEM fields

## Strengths
- Questions are expert-written and verified to be genuinely difficult
- Covers multiple scientific disciplines (Biology, Physics, Chemistry)
- Resistant to simple retrieval-based strategies and internet search
- High correlation with actual reasoning ability in scientific domains

## Limitations
- Limited scale (448 questions), which may not cover all scientific sub-domains
- Focuses on "hard" sciences only; does not cover humanities or social sciences
- Multiple-choice format may not fully capture open-ended reasoning ability
- High barrier to entry for human verification (requires PhD-level experts)

## When to use it
- When comparing frontier LLMs on their ability to handle difficult, expert-level scientific questions
- When you need a benchmark that is resistant to memorization and search-engine shortcuts

## When not to use it
- When evaluating code generation or practical task completion (use HumanEval or SWE-bench)
- When you need broad general-knowledge evaluation for a non-expert audience (use MMLU instead)
- For testing basic conversational capabilities

## Getting started

GPQA is typically run using evaluation frameworks like the LM Evaluation Harness.

1. Clone the LM Evaluation Harness repository.
2. Install dependencies.
3. Run the GPQA task against your model:

```bash
python main.py \
    --model hf \
    --model_args pretrained=your-model-name \
    --tasks gpqa_main \
    --device cuda:0
```

## Technical examples

### Example Question Format
Questions are structured to test reasoning over multiple steps of scientific logic:

```json
{
  "question": "In a certain species of flowering plant, the locus for flower color has two alleles...",
  "explanation": "To solve this, we must first calculate the allele frequencies using the Hardy-Weinberg equilibrium...",
  "choice_a": "1/4",
  "choice_b": "1/2",
  "choice_c": "3/4",
  "choice_d": "1",
  "answer": "choice_c"
}
```

### Performance Comparison (Representative)
Frontier models typically show a significant gap between "Diamond" (expert-verified) and general accuracy:

| Model | GPQA Diamond (Acc) |
| :--- | :--- |
| Claude 3.5 Sonnet | ~59.4% |
| GPT-4o | ~53.6% |
| Claude 3 Opus | ~50.4% |
| Human (Non-expert) | ~34% |

## Related tools / concepts
- [MMLU (Massive Multitask Language Understanding)](mmlu.md)
- [GSM8K (Grade School Math 8K)](gsm8k.md)
- [HumanEval](human-eval.md)
- [DREAM: Deep Research Evaluation with Agentic Metrics](dream.md)
- [LM Evaluation Harness](lm-evaluation-harness.md)
- [Anthropic](../providers/anthropic.md)
- [OpenAI](../providers/openai.md)

## Sources / references
- [Arxiv Paper: GPQA: A Graduate-Level Google-Proof Q&A Benchmark](https://arxiv.org/abs/2311.12022)
- [GPQA Dataset on Hugging Face](https://huggingface.co/datasets/Idavidrein/gpqa)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high

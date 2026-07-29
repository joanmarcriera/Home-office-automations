# GSM8K (Grade School Math 8K)

## What it is
GSM8K is a benchmark for evaluating the multi-step mathematical reasoning capabilities of LLMs. It contains 8.5K high-quality grade school math word problems that require 2 to 8 steps of basic arithmetic to solve. As of late October / November 2026, it serves as the baseline for "Reasoning Density" in frontier models like **Claude 5.1** and **GPT-5.5**.

## What problem it solves
Provides a standardized way to measure whether LLMs can perform multi-step arithmetic reasoning. It moves beyond simple "calculator" tasks to test the model's ability to decompose a problem into logical steps, which is a fundamental building block for complex agentic planning and reliable tool use.

## Where it fits in the stack
**Benchmarking**. Serves as a widely used reference for evaluating mathematical reasoning and the efficacy of Chain-of-Thought (CoT) prompting.

## Typical use cases
- Benchmarking the reasoning capabilities of local models like **Llama 4** and **Qwen 3.6 Instruct**.
- Measuring the impact of specialized prompting (e.g., "Let's think step by step") on math accuracy.
- Regression testing for fine-tuned models to ensure logic hasn't degraded.
- Comparing the "reasoning tokens" efficiency of different model architectures.

## Strengths
- **Logical Decomposition**: Forces models to show their work, making it ideal for testing reasoning traces.
- **Unambiguous Scoring**: Exact Match (EM) scoring provides a clear, objective metric for success.
- **Wide Adoption**: Results are available for almost every model released since 2022, enabling long-term progress tracking.
- **Agentic Predictor**: High GSM8K scores often correlate with better performance in autonomous tool use and multi-step planning. It is widely used in **Model Context Protocol (MCP 3.1)** automated task protocol evaluation pipelines.

## Limitations
- **Level Cap**: Limited to grade-school math; does not test higher-level mathematics (calculus, linear algebra, etc.).
- **Contamination**: Significant evidence suggests newer models have "seen" these problems in their training data.
- **Rigidity**: Does not give credit for correct reasoning if the final arithmetic calculation is slightly off.

## When to use it
- When comparing LLMs on basic mathematical reasoning and logical consistency.
- When evaluating the effect of different prompting techniques on mathematical performance.
- For a quick "sanity check" of a model's basic logical abilities.

## When not to use it
- When you need to evaluate advanced mathematical reasoning (use [MATH Benchmark](math-benchmark.md) instead).
- When testing creative writing or coding-specific capabilities (use [HumanEval](human-eval.md) instead).
- For evaluating complex symbolic logic or theorem proving.

## Getting started

GSM8K is typically evaluated using the `lm-eval` harness or similar frameworks.

1. Install the LM Evaluation Harness: `pip install lm-eval`
2. Run the evaluation against a local model:
```bash
lm_eval --model hf \
    --model_args pretrained=models/llama-4 \
    --tasks gsm8k \
    --device cuda:0
```

## CLI examples

### 1. Running Evaluation with Few-Shot
Specify the number of examples to provide in the prompt:
```bash
lm_eval --model hf --tasks gsm8k --num_fewshot 5 --model_args pretrained=gpt2
```

### 2. November 2026 Model Evaluation (CoT)
Using the latest reasoning flags for frontier models:
```bash
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4,reasoning_format=cot \
    --tasks gsm8k \
    --num_fewshot 8 \
    --batch_size auto
```

### 3. Calculating EM Accuracy
A simple script to check accuracy from model output:
```bash
python3 -c "import json; data=[json.loads(l) for l in open('results.jsonl')]; print(sum(1 for d in data if d['correct'])/len(data))"
```

## API examples

### 1. Python: Prompting for Chain-of-Thought
Use **Claude 5.1** to solve a problem with explicit reasoning:

```python
from anthropic import Anthropic

client: Anthropic = Anthropic()
response = client.messages.create(
    model="claude-5-1-opus-20261031",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Question: Janet has 30 apples. She gives 10 to her neighbor and then buys 15 more. How many apples does she have now?\nAnswer: Let's think step by step."}]
)
print(response.content[0].text)
```

### 2. Python: Structured Parsing and Verification with Pydantic v2
Validate structured mathematical reasoning outputs using modern Pydantic v2 specifications and strict type-hints:

```python
import json
from typing import List
from pydantic import BaseModel, Field, TypeAdapter

class ReasoningStep(BaseModel):
    step_number: int = Field(..., description="The sequence number of the reasoning step.")
    explanation: str = Field(..., description="Detailed explanation of the logical step.")
    sub_calculation: str = Field(..., description="The mathematical calculation performed in this step.")

class MathSolution(BaseModel):
    reasoning_steps: List[ReasoningStep] = Field(..., description="Sequential steps to reach the solution.")
    final_numeric_answer: int = Field(..., description="The final single integer answer.")

# Simulated model JSON output response
raw_response: str = """{
  "reasoning_steps": [
    {"step_number": 1, "explanation": "Janet starts with 30 apples and gives 10 to her neighbor.", "sub_calculation": "30 - 10 = 20"},
    {"step_number": 2, "explanation": "She then buys 15 more apples.", "sub_calculation": "20 + 15 = 35"}
  ],
  "final_numeric_answer": 35
}"""

# Use Pydantic v2 TypeAdapter for validation
adapter: TypeAdapter[MathSolution] = TypeAdapter(MathSolution)
solution: MathSolution = adapter.validate_json(raw_response)

print(f"Validated Answer: {solution.final_numeric_answer}")
assert solution.final_numeric_answer == 35
```

### 3. Performance Metrics (November 2026 SOTA)
| Model | GSM8K (Maj@100) | Release Date |
| :--- | :--- | :--- |
| **Claude 5.1 Opus** | 99.4% | October 2026 |
| **GPT-5.5** | 99.1% | April 2026 |
| **Gemini 4.0 Ultra** | 98.7% | September 2026 |
| **Qwen 3.6 Instruct** | 97.9% | August 2026 |
| **Gemma 3 9B** | 96.2% | July 2026 |
| **Llama 4** | 95.8% | June 2026 |

## Related tools / concepts
- [MATH Benchmark](math-benchmark.md) - For advanced mathematical reasoning.
- [DREAM](dream.md) - Deep Research Evaluation with Agentic Metrics.
- [GPQA](gpqa.md) - Graduate-level science reasoning.
- [MMLU](mmlu.md) - Broad knowledge evaluation.
- [HumanEval](human-eval.md) - Code generation benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Standard tool for running GSM8K.
- [Claude](../ai_knowledge/claude.md) - High performer on reasoning tasks.
- [GPT-5.5](../ai_knowledge/openai.md) - SOTA reasoning benchmark.
- [Llama 4](../ai_knowledge/local_llms.md) - Benchmark target for local reasoning.

## Sources / references
- [OpenAI GSM8K GitHub Repository](https://github.com/openai/grade-school-math)
- [Hugging Face GSM8K Dataset](https://huggingface.co/datasets/openai/gsm8k)
- [Arxiv: Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)
- [LMSYS Benchmarking Suite](https://github.com/lm-sys)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high

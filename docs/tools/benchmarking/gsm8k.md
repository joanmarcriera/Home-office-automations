# GSM8K (Grade School Math 8K)

## What it is
GSM8K is a benchmark for evaluating the multi-step mathematical reasoning capabilities of LLMs. It contains 8.5K high-quality grade school math word problems that require 2 to 8 steps of basic arithmetic to solve. As of early January 2027, it serves as the baseline for "Reasoning Density" in frontier models like **Claude 5.1**, **GPT-5.5/5.6**, and **Gemini 4.0 Pro**.

## What problem it solves
Provides a standardized way to measure whether LLMs can perform multi-step arithmetic reasoning. It moves beyond simple "calculator" tasks to test the model's ability to decompose a problem into logical steps, which is a fundamental building block for complex agentic planning.

## Where it fits in the stack
**Benchmarking**. Serves as a widely used reference for evaluating mathematical reasoning and the efficacy of Chain-of-Thought (CoT) prompting.

## Typical use cases
- Benchmarking the reasoning capabilities of local models like **Llama 4 Maverick** and **Qwen 3.8**.
- Measuring the impact of specialized prompting (e.g., "Let's think step by step") on math accuracy.
- Regression testing for fine-tuned models to ensure logic hasn't degraded.
- Comparing the "reasoning tokens" efficiency of different model architectures (e.g., Gemini 4.0 Pro).

## Strengths
- **Logical Decomposition**: Forces models to show their work, making it ideal for testing reasoning traces.
- **Unambiguous Scoring**: Exact Match (EM) scoring provides a clear, objective metric for success.
- **Wide Adoption**: Results are available for almost every model released since 2022, enabling long-term progress tracking.
- **Agentic Predictor**: High GSM8K scores often correlate with better performance in autonomous tool use and multi-step planning.

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
- When testing creative writing or coding-specific capabilities.
- For evaluating complex symbolic logic or theorem proving.

## Getting started

GSM8K is typically evaluated using the `lm-eval` harness or similar frameworks.

1. Install the LM Evaluation Harness: `pip install lm-eval`
2. Run the evaluation against a local model:
```bash
lm_eval --model hf \
    --model_args pretrained=models/llama-4-maverick-8b \
    --tasks gsm8k \
    --device cuda:0
```

## CLI examples

### 1. Running Evaluation with Few-Shot
Specify the number of examples to provide in the prompt:
```bash
lm_eval --model hf --tasks gsm8k --num_fewshot 5 --model_args pretrained=gpt2
```

### 2. Model Evaluation with Chain-of-Thought
Using reasoning flags for frontier models:
```bash
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4-Maverick-70B,reasoning_format=cot \
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

client = Anthropic()
response = client.messages.create(
    model="claude-5-1-opus-20261031",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Question: Janet has 30 apples. She gives 10 to her neighbor and then buys 15 more. How many apples does she have now?\nAnswer: Let's think step by step."}]
)
print(response.content[0].text)
```

### 2. Validating Answer via Regex and Pydantic v2
Extract the final numerical answer from a model's reasoning trace and validate using a typed-safe Pydantic v2 structure:

```python
import re
from pydantic import BaseModel, Field

class MathResult(BaseModel):
    raw_output: str
    extracted_value: int | None = Field(default=None, description="The final extracted numerical answer")

def parse_output(text: str) -> MathResult:
    match = re.search(r"####\s*(-?\d+)", text)
    value = int(match.group(1)) if match else None
    return MathResult(raw_output=text, extracted_value=value)

model_output = "Therefore, she has #### 35 apples."
result = parse_output(model_output)
print(result.model_dump_json(indent=2))
```

### 3. Performance Metrics (Early 2027 Baseline)
| Model | GSM8K (Maj@100) | Release Baseline |
| :--- | :--- | :--- |
| **Claude 5.1 Opus** | 99.1% | Late 2026 |
| **GPT-5.5** | 98.9% | Late 2026 |
| **Gemini 4.0 Pro** | 98.4% | Late 2026 |
| **Llama 4 Maverick** | 96.5% | Mid 2026 |
| **Qwen 3.8 Instruct** | 96.1% | Late 2026 |

## Related tools / concepts
- [MATH Benchmark](math-benchmark.md) - For advanced mathematical reasoning.
- [DREAM](dream.md) - Deep Research Evaluation with Agentic Metrics.
- [GPQA](gpqa.md) - Graduate-level science reasoning.
- [MMLU](mmlu.md) - Broad knowledge evaluation.
- [HumanEval](human-eval.md) - Code generation benchmark.
- [LM Evaluation Harness](lm-evaluation-harness.md) - Standard tool for running GSM8K.
- [Claude](../ai_knowledge/claude.md) - High performer on reasoning tasks.
- [GPT-5.5](../ai_knowledge/openai.md) - SOTA reasoning benchmark.
- [Llama 4 Maverick](../ai_knowledge/local_llms.md) - Benchmark target for local reasoning.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) - Extending model planning capabilities.

## Sources / references
- [OpenAI GSM8K GitHub Repository](https://github.com/openai/grade-school-math)
- [Hugging Face GSM8K Dataset](https://huggingface.co/datasets/openai/gsm8k)
- [Arxiv: Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)
- [LMSYS Benchmarking Suite](https://github.com/lm-sys)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

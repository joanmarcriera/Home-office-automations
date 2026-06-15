# ASDiv (Academia Sinica Diverse MWP Dataset)

## What it is
ASDiv (Academia Sinica Diverse MWP Dataset) is a diverse corpus of 2,305 English Math Word Problems (MWPs) designed for evaluating the natural language understanding and mathematical reasoning capabilities of AI solvers. As of June 2026, it remains a critical benchmark for validating that frontier models like Claude 4.8 Opus and GPT-5.5 possess genuine semantic understanding rather than relying on surface-level pattern matching.

## What problem it solves
Many older MWP datasets suffer from limited linguistic diversity, allowing models to "cheat" by learning statistical shortcuts or over-fitting to specific phrasing. ASDiv addresses this by providing a broad range of text patterns and covering almost all problem types taught in elementary school (K-6), requiring models to map natural language to formal mathematical operations accurately.

## Where it fits in the stack
ASDiv is positioned in the **Benchmarking** layer of the AI stack. It serves as a specialized evaluation tool for mathematical reasoning and lexicon usage diversity, often used alongside general benchmarks like MMLU and code-centric ones like EvalPlus to provide a holistic view of model performance.

## Typical use cases
- **Model Evaluation**: Benchmarking the elementary-level mathematical reasoning of LLMs.
- **Prompt Engineering**: Testing the effectiveness of "Chain of Thought" (CoT) and multi-hop reasoning prompts.
- **Robustness Testing**: Measuring how models handle varied linguistic expressions of the same mathematical problem.
- **System 2 Validation**: Evaluating the reasoning capabilities of "thinking" models (e.g., DeepSeek R1 or Claude's context-extended modes).

## Strengths
- **High Diversity**: Features a wide range of vocabulary and sentence structures (Lexicon diversity).
- **Granular Annotation**: Each problem is annotated with its specific type (e.g., addition, subtraction, division) and difficulty grade.
- **Reliable Metric**: Includes a proposed metric for measuring the diversity of MWP corpora, ensuring a high bar for evaluation.
- **Open Access**: Available under a permissive MIT license, facilitating wide adoption in open-source evaluation harnesses.

## Limitations
- **Elementary Scope**: Primarily limited to elementary school mathematics (K-6 level), making it unsuitable for testing advanced calculus or linear algebra.
- **Language Constraint**: Currently only available in English, requiring translation for multi-lingual evaluation.
- **Static Dataset**: As a fixed corpus, it is susceptible to "benchmark contamination" if not handled carefully during model training.

## When to use it
- Use ASDiv when you need to verify that a model can handle varied phrasing in math problems without relying on superficial pattern matching.
- Use it to test a model's ability to perform multi-step sequential arithmetic and comparative logic.
- Ideal for validating the performance of Small Language Models (SLMs) on core reasoning tasks.

## When not to use it
- Do not use ASDiv for evaluating high-level university mathematics or specialized technical reasoning.
- Not intended for large-scale training (use GSM8K or synthetic datasets like those from [Glaive](../ai_knowledge/glaive.md) for that purpose).

## Getting started
ASDiv is most commonly accessed through the `lm-evaluation-harness` or directly from its GitHub repository. To begin using it, ensure you have the dataset files or an evaluation framework installed.

1. Clone the repository: `git clone https://github.com/chiahsuan/ASDiv.git`
2. Install the evaluation harness: `pip install lm-eval`
3. Prepare your model (e.g., a local model via Ollama or a remote API).

## CLI examples
The primary way to interact with ASDiv in a terminal environment is through evaluation tools.

### Running Evaluation with LM Eval Harness
```bash
# Run ASDiv evaluation on a local Llama-4 model
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-4-8B \
    --tasks asdiv \
    --device cuda:0 \
    --num_fewshot 5
```

### Inspecting Dataset Structure
```bash
# View the first few problems in the XML dataset
head -n 20 ASDiv/dataset/ASDiv.xml
```

## API examples
While ASDiv is a dataset, it is often integrated into evaluation pipelines programmatically.

### Loading ASDiv via Hugging Face Datasets
```python
from datasets import load_dataset

# Load the ASDiv dataset
dataset = load_dataset("chiahsuan/asdiv")

# Print a sample problem
sample = dataset['train'][0]
print(f"Problem: {sample['body']} {sample['question']}")
print(f"Formula: {sample['formula']}")
print(f"Answer: {sample['answer']}")
```

### Using ASDiv in a Custom Evaluation Loop
```python
import openai

# Mock evaluation loop for a Claude 4.8 model
def evaluate_asdiv(problem):
    response = openai.ChatCompletion.create(
        model="claude-4-8-opus-20260528",
        messages=[{"role": "user", "content": f"Solve this math problem: {problem}"}]
    )
    return response.choices[0].message.content

# Example problem from ASDiv
problem = "If a recipe calls for 3 cups of flour and 2 cups of sugar, how many more cups of flour than sugar are needed?"
print(evaluate_asdiv(problem))
```

## Related tools / concepts
- [GSM8K](../benchmarking/gsm8k.md) — High-quality elementary math word problems.
- [MATH Benchmark](math-benchmark.md) — More challenging mathematics benchmark.
- [MMLU](../benchmarking/mmlu.md) — Multi-task knowledge benchmark.
- [EvalPlus](../benchmarking/evalplus.md) — Enhanced code generation evaluation.
- [DREAM](../benchmarking/dream.md) — Agentic research evaluation framework.
- [Claude Code](../development_ops/claude-code.md) — Agentic coding tool using these benchmarks for self-correction.
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md) — A model optimized for reasoning tasks like those in ASDiv.

## Sources / references
- [ASDiv GitHub Repository](https://github.com/chiahsuan/ASDiv)
- [ASDiv: A Diverse Corpus for Math Word Problem Solving (ACL 2020)](https://aclanthology.org/2020.acl-main.92.pdf)
- [Hugging Face Dataset Page](https://huggingface.co/datasets/chiahsuan/asdiv)

## Contribution Metadata
- Last reviewed: 2026-06-12
- Confidence: high

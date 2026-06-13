# DSPy

## What it is
DSPy (Declarative Self-improving Language Programs, Pythonically) is a framework for algorithmically optimizing LLM prompts and weights. It separates the flow of your program (modules) from the parameters (LM prompts and weights) of each step.

## What problem it solves
Traditional LLM development involves manual prompt engineering ("prompt hacking"), which is brittle and doesn't scale. DSPy replaces this with a programming model where you define signatures and modules, and an optimizer automatically generates high-quality prompts or fine-tunes models to satisfy your requirements.

## Where it fits in the stack
**Framework / LLM Programming Layer**. It acts as a compiler for language model programs, bridging the gap between high-level logic and low-level prompt optimization.

## Typical use cases
- **Complex RAG Pipelines**: Optimizing retrieval and generation steps together.
- **Multi-hop Question Answering**: Managing state and logic across multiple LLM calls.
- **Self-Improving Agents**: Automatically refining agent prompts based on few-shot examples.
- **Agentic Workflows**: Building robust systems for frontier models like `claude-4-8-opus-20260528`.

## Strengths
- **Programmatic Control**: Define logic in Python rather than raw strings using **Signatures** (declarative specifications) and **Modules** (reusable components like `ChainOfThought` or `ReAct`).
- **Automatic Optimization**: Compilers (optimizers) like `BootstrapFewShotWithRandomSearch` generate effective prompts systematically.
- **Advanced Reasoning**: Support for `ProgramOfThought` where the model generates code to solve problems.
- **Assertions and Constraints**: Built-in `dspy.Assert` and `dspy.Suggest` to enforce runtime constraints on LLM outputs.
- **Model Agnostic**: Easily switch between different LMs and re-optimize the pipeline.

## Limitations
- **Learning Curve**: Requires a shift in mindset from manual prompting to systematic programming.
- **Optimization Overhead**: Running optimizers requires a training/validation dataset and can be time-consuming.
- **Complexity**: Debugging compiled programs can be more difficult than debugging raw prompts.

## When to use it
- When you are tired of manual prompt engineering.
- When you need a robust, reproducible, and optimizable LLM pipeline.
- When building production-grade RAG or agent systems that must adapt to different models.

## When not to use it
- For very simple, single-prompt applications.
- If you don't have even a small dataset to use for optimization.
- For purely experimental "chat-with-pdf" scripts that don't require high reliability.

## Getting started

### Installation
```bash
pip install dspy
```

### Minimal Python Example
```python
import dspy
lm = dspy.LM('openai/gpt-4o') # Or 'anthropic/claude-3-5-sonnet'
dspy.settings.configure(lm=lm)

class CoT(dspy.Signature):
    """Answer questions with chain of thought."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 10 and 50 words")

generate_answer = dspy.ChainOfThought(CoT)
pred = generate_answer(question="What is the capital of France?")
print(pred.answer)
```

## CLI examples
> [!NOTE]
> DSPy is primarily a library-based framework. Terminal interactions are typically handled via Python scripts or environment configuration.

```bash
# Example: Viewing the DSPy cache (if configured)
python -m dspy.utils.cache_viewer --port 8080

# Example: Running a DSPy script with specific environment variables
DSPY_CACHEDIR=./cache python my_dspy_app.py

# Example: Using the DSPy CLI for model benchmarking (if installed via extensions)
dspy-bench --model claude-4-8-opus-20260528 --task my_task.py
```

## API examples

### ProgramOfThought for Complex Logic
```python
import dspy

class MathSignature(dspy.Signature):
    """Solve math word problems."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="numerical result")

# Uses a Python interpreter internally to compute the answer
math_solver = dspy.ProgramOfThought(MathSignature)
result = math_solver(question="If I have 5 apples and buy 3 more, then double them, how many do I have?")
print(result.answer)
```

### Optimization with BootstrapFewShotWithRandomSearch
```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

# Define validation metric
def validate_context_and_answer(example, pred, trace=None):
    # Metric logic...
    return pred.answer == example.answer

# Initialize the optimizer
tp = BootstrapFewShotWithRandomSearch(
    metric=validate_context_and_answer,
    max_bootstrapped_demos=4,
    num_candidate_programs=10
)

# Compile against a training set for Claude 4.8
optimized_app = tp.compile(MyModule(), trainset=trainset)
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [AutoGen](autogen.md)
- [Haystack](haystack.md)
- [Smolagents](smolagents.md)
- [RAG Patterns](../../knowledge_base/patterns/rag.md)
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md)
- [Agentic RAG Flow](../process_understanding/ragflow.md)
- [Model Evaluation](../benchmarking/lm-evaluation-harness.md)

## Sources / References
- [Official Website](https://dspy-docs.vercel.app/)
- [GitHub](https://github.com/stanfordnlp/dspy)
- [DSPy: Compiling Declarative Language Model Programs](https://arxiv.org/abs/2310.03714)
- [DSPy 2026 Roadmap](https://dspy-docs.vercel.app/roadmap)

## Contribution Metadata

- Last reviewed: 2026-06-12
- Confidence: high

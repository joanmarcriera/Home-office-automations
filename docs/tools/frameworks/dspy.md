# DSPy

## What it is
DSPy (Declarative Self-improving Language Programs, Pythonically) is a framework for algorithmically optimizing LLM prompts and weights. It separates the flow of your program (modules) from the parameters (LM prompts and weights) of each step.

## What problem it solves
Traditional LLM development involves manual prompt engineering ("prompt hacking"), which is brittle and doesn't scale. DSPy replaces this with a programming model where you define signatures and modules, and an optimizer automatically generates high-quality prompts or fine-tunes models to satisfy your requirements.

## Where it fits in the stack
Framework

## Typical use cases
- **Complex RAG Pipelines**: Optimizing retrieval and generation steps together.
- **Multi-hop Question Answering**: Managing state and logic across multiple LLM calls.
- **Self-Improving Agents**: Automatically refining agent prompts based on few-shot examples.

## Strengths
- **Programmatic Control**: Define logic in Python rather than raw strings.
- **Automatic Optimization**: Compilers (optimizers) like `BootstrapFewShot` generate effective prompts.
- **Model Agnostic**: Easily switch between different LMs and re-optimize the pipeline.

## Core Concepts: Signatures and Modules
DSPy programs are built using two primary abstractions:
- **Signatures**: Declarative specifications of the input and output behavior. Instead of writing a prompt, you define *what* the module should do (e.g., `question -> answer`).
- **Modules**: Reusable components that implement a signature using specific strategies, such as `dspy.ChainOfThought`, `dspy.ReAct`, or `dspy.ProgramOfThought`.

## Advanced Reasoning: ProgramOfThought
`ProgramOfThought` is a module that handles complex tasks by generating a program (e.g., Python code) that computes the answer, rather than generating the answer directly.

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

## Systematic Optimization: BootstrapFewShotWithRandomSearch
For more robust optimization than the basic `BootstrapFewShot`, you can use random search to find the best set of few-shot examples across multiple candidates.

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

# Define validation metric
def validate_context_and_answer(example, pred, trace=None):
    # Metric logic...
    return True

# Initialize the optimizer
tp = BootstrapFewShotWithRandomSearch(
    metric=validate_context_and_answer,
    max_bootstrapped_demos=4,
    max_labeled_demos=4,
    num_candidate_programs=10,
    num_threads=4
)

# Compile the program against a training set
optimized_app = tp.compile(MyModule(), trainset=trainset)
```

## Assertions and Constraints
DSPy allows you to define assertions and suggestions within your modules to enforce constraints on the LLM's output.

```python
class MyModule(dspy.Module):
    def forward(self, question):
        prediction = self.generate_answer(question=question)
        dspy.Suggest(
            len(prediction.answer) < 100,
            "The answer is too long, please summarize."
        )
        return prediction
```

## Limitations
- **Learning Curve**: Requires a shift in mindset from manual prompting to systematic programming.
- **Optimization Overhead**: Running optimizers requires a training/validation dataset and can be time-consuming.

## When to use it
- When you are tired of manual prompt engineering.
- When you need a robust, reproducible, and optimizable LLM pipeline.

## When not to use it
- For very simple, single-prompt applications.
- If you don't have even a small dataset to use for optimization.

## Getting started

### Installation
```bash
pip install dspy
```

### Minimal Python Example
```python
import dspy
lm = dspy.OpenAI(model='gpt-3.5-turbo')
dspy.settings.configure(lm=lm)

class CoT(dspy.Signature):
    """Answer questions with chain of thought."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 10 and 50 words")

generate_answer = dspy.ChainOfThought(CoT)
pred = generate_answer(question="What is the capital of France?")
print(pred.answer)
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

## Contribution Metadata

- Last reviewed: 2026-05-17
- Confidence: high

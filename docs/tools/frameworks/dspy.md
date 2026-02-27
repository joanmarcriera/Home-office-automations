# DSPy

## What it is
DSPy (Declarative Self-improving Language Programs, Pythonically) is a framework for algorithmically optimizing LLM prompts and weights. It separates the flow of your program (modules) from the parameters (LM prompts and weights) of each step.

## What problem it solves
Traditional LLM development involves manual prompt engineering ("prompt hacking"), which is brittle and doesn't scale. DSPy replaces this with a programming model where you define signatures and modules, and an optimizer automatically generates high-quality prompts or fine-tunes models to satisfy your requirements.

## Where it fits in the stack
**Framework**. It sits between the raw LLM and the application logic, providing a structured way to build and optimize pipelines.

## Typical use cases
- **Complex RAG Pipelines**: Optimizing retrieval and generation steps together.
- **Multi-hop Question Answering**: Managing state and logic across multiple LLM calls.
- **Self-Improving Agents**: Automatically refining agent prompts based on few-shot examples.

## Strengths
- **Programmatic Control**: Define logic in Python rather than raw strings.
- **Automatic Optimization**: Compilers (optimizers) like `BootstrapFewShot` generate effective prompts.
- **Model Agnostic**: Easily switch between different LMs and re-optimize the pipeline.

## Limitations
- **Learning Curve**: Requires a shift in mindset from manual prompting to systematic programming.
- **Optimization Overhead**: Running optimizers requires a training/validation dataset and can be time-consuming.

## When to use it
- When you are tired of manual prompt engineering.
- When you need a robust, reproducible, and optimizable LLM pipeline.

## When not to use it
- For very simple, single-prompt applications.
- If you don't have even a small dataset to use for optimization.

## Licensing and cost
- **Open Source**: Yes (MIT License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started
```bash
pip install dspy
```

```python
import dspy

# Configure the LM
lm = dspy.OpenAI(model='gpt-3.5-turbo')
dspy.settings.configure(lm=lm)

# Define a signature
class CoT(dspy.Signature):
    """Answer questions with chain of thought."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 10 and 50 words")

# Use the module
generate_answer = dspy.ChainOfThought(CoT)
pred = generate_answer(question="What is the capital of France?")
print(pred.answer)
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md)
- [LlamaIndex](../ai_knowledge/llamaindex.md)
- [Prompt Engineering](https://home-toolset.riera.co.uk/knowledge_base/patterns/index.md)

## Sources / References
- [Official Website](https://dspy-docs.vercel.app/)
- [GitHub](https://github.com/stanfordnlp/dspy)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: high

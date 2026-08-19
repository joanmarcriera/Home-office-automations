# DSPy

## What it is
DSPy (Declarative Self-improving Language Programs, Pythonically) is an open-source framework for algorithmically optimizing LLM prompts, reasoning paths, and fine-tuning weights. It separates the program control flow (defined via modular Python modules) from the execution parameters (prompts, few-shot demonstrations, and model weights).

## What problem it solves
Traditional LLM engineering relies on manual, fragile prompt engineering ("prompt hacking"). DSPy replaces manual prompt design with a compiler-driven paradigm: developers specify declarative input/output interfaces (**Signatures**) and composition pipelines (**Modules**), while automatic optimizers (**Teleprompters**) generate optimal prompt templates, select few-shot exemplars, or fine-tune open-weights models (such as Llama 4 or Qwen 3.8) to meet specified quality metrics.

## Where it fits in the stack
**Framework / LLM Optimization & Programming Layer**. DSPy functions as a compiler layer between high-level application logic and low-level LLM providers. In early 2027 architectures, DSPy is widely used to optimize tool selection strategies for [FastMCP 3.1](../automation_orchestration/mcp.md) servers and complex multi-hop RAG architectures powered by models like **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0 Pro**.

## Typical use cases
- **Multi-Hop RAG Systems**: Jointly optimizing retrieval queries and synthesis prompts for multi-stage knowledge retrieval.
- **Agentic Tool Selection**: Programmatically optimizing tool choice and argument formatting for [FastMCP 3.1](../automation_orchestration/mcp.md) protocols.
- **Automated Few-Shot In-Context Learning**: Generating high-performing few-shot demonstrations using optimizers like `MIPROv2` or `BootstrapFewShotWithRandomSearch`.
- **Model Distillation**: Distilling reasoning traces from frontier models (**Claude 5.1**) into smaller, self-hosted open models (**Llama 4 Maverick**, **Qwen 3.8**) via automatic weight fine-tuning.

## Strengths
- **Declarative Programming Model**: Replaces brittle string prompts with structured Python type signatures and modules.
- **Algorithmic Prompt Optimization**: Automatically tunes prompts and few-shot examples based on quantitative metrics.
- **Model Agnostic & Portable**: Re-optimize the entire application pipeline instantly when switching between LLM providers (e.g., from GPT-5.5 to Claude 5.1).
- **Runtime Constraints**: Built-in `dspy.Assert` and `dspy.Suggest` enable strict validation and self-correction during model execution.
- **Late 2026/2027 Optimizers**: High-efficiency optimizers (`MIPROv2`, `AdaptiveSpectral`) that optimize complex programs with minimal training data.

## Limitations
- **Dataset Requirement**: Requires a small ground-truth dataset (typically 10–50 annotated or synthetic examples) to run optimizers effectively.
- **Optimization Overhead**: Running teleprompters incurs multiple LLM calls during the compilation phase.
- **Mindset Shift**: Developers must transition from raw string prompt design to objective evaluation metric design.

## When to use it
- When building complex multi-step pipelines or RAG applications where manual prompt tuning becomes unmaintainable.
- When systematically adapting an LLM application across multiple model providers or open-source checkpoints.
- When exact output formatting and reasoning trace reliability are critical to production operations.

## When not to use it
- For trivial, single-prompt applications where simple string templates are sufficient.
- When no evaluation metric or ground-truth dataset can be defined.
- For exploratory manual chatting or ad-hoc prototyping without repeatable evaluation steps.

## Getting started

### Installation
Install DSPy with modern dependencies:

```bash
pip install "dspy-ai>=2.5.0" pydantic>=2.10.0
```

### Minimal Python Example (Signatures & LMs)
```python
import dspy

# Configure modern frontier model
lm = dspy.LM('openai/gpt-5.5-preview')
dspy.settings.configure(lm=lm)

# Define declarative signature
class ExplainConcept(dspy.Signature):
    """Provide a clear, technical explanation of a complex AI concept."""
    concept: str = dspy.InputField(desc="Name of the AI concept or algorithm")
    target_audience: str = dspy.InputField(desc="Target domain expertise level")
    explanation: str = dspy.OutputField(desc="Structured technical summary under 100 words")

# Instantiate Chain-of-Thought module
explain_module = dspy.ChainOfThought(ExplainConcept)
result = explain_module(concept="Model Context Protocol", target_audience="Senior Software Engineer")
print(result.explanation)
```

## CLI examples

```bash
# Environment configuration for DSPy caching
export DSPY_CACHEDIR="./.dspy_cache"

# View DSPy cache statistics or run cache inspection utility
python3 -m dspy.utils.cache_viewer --port 8080

# Execute DSPy optimization benchmark script
python3 -m dspy.cli.evaluate --program pipeline.py --dataset dev_set.json
```

## API examples

### ProgramOfThought for Executable Python Code Generation
```python
import dspy

class CodeExecutionSignature(dspy.Signature):
    """Solve mathematical or data transformation problems by generating code."""
    problem_statement: str = dspy.InputField()
    result: str = dspy.OutputField(desc="Evaluated output from executed code")

# ProgramOfThought executes Python code internally to compute ground-truth outputs
pot_solver = dspy.ProgramOfThought(CodeExecutionSignature)
response = pot_solver(problem_statement="Calculate the compounding interest on $10,000 at 5% annually over 7 years.")
print(response.result)
```

### Automatic Teleprompter Compilation with MIPROv2
```python
from typing import Any, List
import dspy
from dspy.teleprompt import MIPROv2

class RAGPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")

    def forward(self, context: str, question: str) -> dspy.Prediction:
        return self.generate_answer(context=context, question=question)

def exact_match_metric(example: Any, pred: Any, trace: Any = None) -> bool:
    return bool(pred.answer.strip().lower() == example.answer.strip().lower())

trainset = [
    dspy.Example(context="FastMCP 3.1 was released in late 2026.", question="When was FastMCP 3.1 released?", answer="late 2026").with_inputs("context", "question")
]

# Compile pipeline using MIPROv2 optimizer
optimizer = MIPROv2(metric=exact_match_metric, auto="light")
compiled_pipeline = optimizer.compile(RAGPipeline(), trainset=trainset)
```

## Related tools / concepts
- [LangChain](../ai_knowledge/langchain.md) — Modular pipeline and agent orchestration framework.
- [LlamaIndex](../ai_knowledge/llamaindex.md) — Knowledge indexing and RAG data framework.
- [Haystack](haystack.md) — Production RAG and DAG component orchestration.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Protocol for standardized agent tool execution.
- [RAG Patterns](../../knowledge_base/patterns/rag-pattern.md) — Reference architectures for RAG systems.
- [Fine-tuning Open Models](../../knowledge_base/patterns/fine-tuning-open-models.md) — Model adaptation methodologies.

## Sources / references
- [DSPy Official Documentation](https://dspy-docs.vercel.app/)
- [DSPy GitHub Repository](https://github.com/stanfordnlp/dspy)
- [DSPy: Compiling Declarative Language Model Programs (arXiv)](https://arxiv.org/abs/2310.03714)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

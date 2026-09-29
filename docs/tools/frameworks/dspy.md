# DSPy

DSPy (Declarative Self-improving Python) is a framework for algorithmically compiling, optimizing, and evaluating declarative prompts and language model module chains.

## What it is
DSPy replaces brittle manual prompt engineering with programming abstractions. Instead of hand-crafting static string prompts, developers define task inputs and outputs using declarative signatures (e.g., `question -> answer` or `context, question -> rationale, answer`). DSPy then compiles these declarative programs by automatically synthesizing optimized prompt instructions, selecting few-shot examples, and fine-tuning model weights using automatic optimizers called **Teleprompters**.

As of 2027, DSPy is deeply integrated with **FastMCP 3.1** and **Pydantic v2**, enabling developers to build self-improving multi-agent workflows, tool-calling pipelines, and continuous optimization loops that adapt dynamically as model providers update underlying models (such as **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, or local **Llama 4 Maverick** weights).

## What problem it solves
Manual prompt engineering introduces severe software engineering flaws:
- **Fragility Across Model Releases**: Upgrading underlying LLM providers (e.g., from GPT-4 to GPT-5.5) frequently breaks hardcoded string prompts, requiring manual re-tuning.
- **Trial-and-Error Engineering**: Hand-tuning prompt instructions, formatting rules, and few-shot examples is non-systematic and difficult to scale across complex multi-step pipelines.
- **Lack of Programmatic Optimization**: Without systematic metrics and automatic teleprompters, developers cannot systematically optimize prompt performance on specific datasets.
- **Brittle Structured Output Parsing**: Handcrafted prompts regularly fail JSON formatting, breaking downstream API pipelines and Pydantic validation steps.

DSPy solves these issues by separating the program's logic (Signatures and Modules) from its rendering and optimization (Teleprompters and LMs), treating prompt optimization like compiling high-level code down to machine instructions.

## System Architecture

```
                                      DSPy Compilation & Teleprompter Pipeline

  +-----------------------+        +-----------------------------------+        +-----------------------------------+
  | Declarative Program   | ---->  | DSPy Program Execution Graph      | ---->  | Teleprompter / Optimizer          |
  | - dspy.Signature      |        | - dspy.ChainOfThought             |        | - BootstrapFewShotWithRandomSearch|
  | - Pydantic v2 Input   |        | - FastMCP 3.1 Tool Invocation     |        | - MIPROv2 (Instruction & Few-Shot)|
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
                                                                                                  |
                                                                                                  v
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
  | Evaluated Production  | <----  | Metric Validation Engine          | <----  | Compiled DSPy Executable          |
  | Agent Program         |        | - Pydantic v2 Output Assertion    |        | - Optimized Prompt Instructions   |
  | - FastMCP Tool Runner |        | - Domain-Specific Accuracy Metric |        | - Dynamically Selected Examples   |
  +-----------------------+        +-----------------------------------+        +-----------------------------------+
```

## Where it fits in the stack
In modern agentic architectures, DSPy functions as the **Declarative Agent Logic & Compilation Layer**:
1. **Model Framework Layer**: Sits above raw provider APIs (Anthropic, OpenAI, Ollama) and alongside frameworks like [LangChain](langchain.md) or [CrewAI](crewai.md).
2. **FastMCP Integration**: Compiles multi-step agent workflows that invoke FastMCP 3.1 tools, ensuring reliable tool argument generation.
3. **Continuous Optimization Layer**: Automates re-compilation of agent prompts when benchmark scores drop or dataset distributions shift.

## Typical use cases
- **Automated RAG Optimization**: Compiling Retrieval-Augmented Generation programs that systematically optimize passage retrieval, query rewriting, and answer generation.
- **Self-Improving Agent Systems**: Building autonomous agents that continuously optimize their prompt instructions and few-shot examples based on task feedback.
- **Structured JSON Synthesis**: Forcing models to generate Pydantic v2 schemas reliably across complex multi-turn reasoning chains.
- **Multi-Step Chain-of-Thought (CoT)**: Programmatically composing reasoning modules (`dspy.ChainOfThought`, `dspy.ReAct`, `dspy.ProgramOfThought`) into unified execution graphs.
- **Cross-Model Migration**: Re-compiling prompt pipelines automatically when switching between cloud models (Claude 5.1) and edge models (Llama 4 Maverick).

## Strengths
- **Modular and Declarative**: Program logic remains independent of specific prompt strings or model providers.
- **Systematic Prompt Optimization**: Teleprompters (MIPROv2, BootstrapFewShot) automatically optimize instructions and example sets against objective metrics.
- **Native Pydantic v2 Integration**: Seamless support for structured input and output models directly inside DSPy Signatures.
- **FastMCP 3.1 Compatibility**: Integrates easily with Model Context Protocol tool definitions and SSE microservices.
- **Reduced Human Maintenance**: Eliminates manual prompt engineering work when models update or task requirements evolve.

## Limitations
- **Optimization Overhead**: Compiling DSPy programs requires evaluating multiple candidate prompts over representative training samples, consuming API credits.
- **Requires Metric Definitions**: Requires clear, programmatic evaluation metrics (e.g., Exact Match, F1, or Pydantic validation) to guide the optimizer.
- **Learning Curve**: Requires shifting from string-concatenation thinking to object-oriented declarative programming.

## When to use it
- When building production agentic systems where manual prompt engineering is too fragile or time-consuming.
- When creating multi-step reasoning pipelines (RAG, CoT, ReAct) that require high accuracy and structured outputs.
- When regularly migrating or deploying across multiple LLM providers or local models.
- When you have a representative dataset and programmatic evaluation metric for continuous optimization.

## When not to use it
- For trivial, single-prompt applications where basic API calls suffice.
- When no dataset or evaluation metric exists to guide the teleprompter optimization process.

## Getting started

### Installation
Install DSPy alongside FastMCP and Pydantic:

```bash
pip install dspy-ai fastmcp pydantic
```

### Basic Declarative DSPy Program
Define a simple Chain-of-Thought program using DSPy signatures:

```python
import dspy

# Configure language model provider
lm = dspy.LM('anthropic/claude-5-1-opus-20261031', api_key="your_api_key")
dspy.configure(lm=lm)

# Define declarative signature
class MathReasoningSignature(dspy.Signature):
    """Solve grade-school math word problems step-by-step."""
    question: str = dspy.InputField(desc="The word problem text")
    answer: str = dspy.OutputField(desc="The final numerical answer preceded by '#### '")

# Instantiate module
cot_solver = dspy.ChainOfThought(MathReasoningSignature)

# Execute program
response = cot_solver(question="Janet has 30 apples. She gives 10 away and buys 15. How many does she have?")
print("Reasoning Rationale:", response.rationale)
print("Final Answer:", response.answer)
```

## CLI examples

### 1. Running DSPy Program Optimization Benchmark via CLI
Execute optimization runs across training datasets:

```bash
python3 -m dspy.cli optimize \
    --program ./agents/rag_agent.py \
    --trainset ./data/train_samples.json \
    --metric ./metrics/exact_match.py \
    --teleprompter MIPROv2 \
    --output ./compiled_rag_agent.json
```

### 2. Inspecting Compiled DSPy Prompt Instructions
Inspect the optimized prompt synthesized by the teleprompter:

```bash
python3 -c "
import dspy
program = dspy.load('./compiled_rag_agent.json')
print('Optimized Instruction:\n', program.demos[0] if hasattr(program, 'demos') else 'No demos')
"
```

## API examples

### 1. FastMCP 3.1 Service Exposing Compiled DSPy Program with Pydantic v2
The following complete Python application demonstrates how to wrap a compiled DSPy program inside a **FastMCP 3.1** microservice, using **Pydantic v2** for input/output schema validation:

```python
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict
import dspy
from typing import List, Optional
import os

mcp = FastMCP("DSPy-Agent-Optimization-Server")

# Configure DSPy global LM
lm = dspy.LM("openai/gpt-5.5-turbo", api_key=os.getenv("OPENAI_API_KEY", "sk-fake"))
dspy.configure(lm=lm)

class CodeAnalysisInput(BaseModel):
    model_config = ConfigDict(frozen=True)

    code_snippet: str = Field(..., description="Python source code to analyze")
    target_framework: str = Field(default="FastMCP 3.1", description="Target framework context")

class VulnerabilityReport(BaseModel):
    has_vulnerabilities: bool = Field(..., description="Whether vulnerabilities were detected")
    severity: str = Field(..., description="Severity level: LOW, MEDIUM, HIGH, CRITICAL")
    findings: List[str] = Field(default_factory=list, description="List of identified issues")
    suggested_fix: str = Field(..., description="Refactored code snippet addressing issues")

class CodeAuditSignature(dspy.Signature):
    """Analyze code for security vulnerabilities and output structured findings."""
    code: str = dspy.InputField(desc="Source code string")
    framework: str = dspy.InputField(desc="Target framework context")
    assessment: VulnerabilityReport = dspy.OutputField(desc="Structured Pydantic assessment report")

class DSPyCodeAuditorModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.auditor = dspy.ChainOfThought(CodeAuditSignature)

    def forward(self, code: str, framework: str):
        return self.auditor(code=code, framework=framework)

# Instantiate program
auditor_program = DSPyCodeAuditorModule()

@mcp.tool()
def audit_code_security(req: CodeAnalysisInput) -> str:
    """Audits code security using a compiled DSPy program and returns a Pydantic v2 JSON report."""
    result = auditor_program(code=req.code_snippet, framework=req.target_framework)
    assessment: VulnerabilityReport = result.assessment
    return assessment.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### 2. Compiling DSPy Program with Teleprompter (BootstrapFewShot)

```python
import dspy
from dspy.teleprompt import BootstrapFewShot

# Define dataset sample
train_data = [
    dspy.Example(question="What is 15 + 27?", answer="42").with_inputs("question"),
    dspy.Example(question="What is 100 - 37?", answer="63").with_inputs("question")
]

# Define validation metric function
def validate_math_answer(example, pred, trace=None):
    return example.answer.strip() in pred.answer.strip()

# Initialize teleprompter optimizer
teleprompter = BootstrapFewShot(
    metric=validate_math_answer,
    max_bootstrapped_demos=2,
    max_labeled_demos=2
)

# Uncompiled program
class SimpleMath(dspy.Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("question -> answer")
    def forward(self, question):
        return self.prog(question=question)

uncompiled_prog = SimpleMath()

# Compile program (synthesizes few-shot examples and instruction tweaks)
compiled_prog = teleprompter.compile(uncompiled_prog, trainset=train_data)

# Test compiled program
res = compiled_prog(question="What is 50 + 50?")
print("Compiled Output:", res.answer)
```

## Related tools / concepts
- [LangChain](langchain.md) — Framework for building application chains and agent tooling.
- [CrewAI](crewai.md) — Multi-agent orchestration framework.
- [Pydantic AI](pydantic-ai.md) — Agent framework built around Pydantic v2 schema validation.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open standard for extending model tool capabilities.
- [System Prompts](../../knowledge_base/system_prompts.md) — Deep knowledge guide on prompt engineering patterns.
- [Claude](../ai_knowledge/claude.md) — Anthropic frontier model platform.

## Sources / references
- [DSPy Official GitHub Repository](https://github.com/stanfordnlp/dspy)
- [DSPy Documentation Hub](https://dspy.ai/)
- [Arxiv: DSPy: Compiling Declarative Language Model Calls (Khattab et al.)](https://arxiv.org/abs/2310.03714)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

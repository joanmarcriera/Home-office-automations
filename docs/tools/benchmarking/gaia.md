# GAIA (General AI Assistants)

## What it is
GAIA (General AI Assistants) is a benchmark designed to evaluate General AI Assistants on non-trivial, multi-modal tasks. It consists of 450 carefully designed, high-fidelity questions that are conceptually simple for humans but extremely challenging for the most advanced AI systems. It is the gold standard for measuring 'System 2' reasoning, tool use, and long-horizon planning in autonomous agents.

## What problem it solves
Existing benchmarks often focus on synthetic reasoning, code syntax, or closed-book trivia. GAIA targets real-world, open-ended tasks that require fundamental human-like abilities: complex reasoning, multi-modality handling (text, spreadsheets, images, PDFs, audio), web browsing, and programmatic tool execution. It exposes the 'reasoning gap' in frontier models, serving as a reliable metric of actual operational utility.

## Where it fits in the stack
**Eval / Benchmarking**. It provides a high-signal evaluation standard for testing autonomous agents, VLMs, and multi-agent workflows. It is used to validate the 'Agentic Core' of systems built on frontier LLMs such as Claude 5.1, GPT-5.5, Gemini 4.0 Pro/Flash, Llama 4, Gemma 3, and Qwen 3.6.

## Typical use cases
- **Agent Architecture Benchmarking**: Comparing the performance of different agent runtimes and planning frameworks on realistic assistant tasks.
- **Multimodal VLM Testing**: Benchmarking the vision and document-understanding capabilities of multimodal models when interacting with complex charts, PDFs, and media assets.
- **Tool-Calling Verification**: Measuring an agent's ability to select, configure, and execute tools (e.g., Python interpreters, web browsers, and Model Context Protocol FastMCP 3.1 servers) correctly.
- **Long-Horizon Planning**: Evaluating an agent's ability to maintain state and recover from execution failures over multi-step tasks.

## Strengths
- **Non-synthetic & Real-World**: Tasks are grounded in actual web, document, and system scenarios.
- **Low Effort for Humans, High for AI**: Tasks are easily resolvable by a human in minutes, yet yield low scores for modern AI systems, clearly showing the agentic performance gap.
- **Contamination Resistant**: Questions require active reasoning, file processing, and execution rather than memory retrieval, making them highly resistant to pre-training memorization.
- **Diverse Modalities**: Integrates multimodal inputs (spreadsheets, audio files, images, PDFs) natively.

## Limitations
- **High API Execution Costs**: Running multi-step agent loops on GAIA tasks can incur significant LLM token costs.
- **Environment Fragility**: Web-browsing tasks can fail if target live websites change their layout, structure, or access controls.
- **Complex Sandbox Requirements**: Requires a robust sandbox environment (e.g., Docker) to safely run file operations and python tool executions.

## When to use it
- When evaluating the operational "generalist" and multi-modal capacity of an AI agent.
- To measure the performance improvements of multi-step planning or self-correction algorithms.
- When benchmarking an agent's integration with real-world file-parsing and execution tools.

## When not to use it
- For testing domain-specific expertise (such as medical, legal, or advanced financial compliance) unless it falls under general digital assistant skills.
- For lightweight or low-latency regression testing (use simpler benchmarks like MMLU-Pro instead).
- For evaluating base foundational models that have not been instruction-aligned or agent-tuned.

## Getting started
GAIA evaluations are typically orchestrated using the `inspect-ai` evaluation framework, which provides a structured sandboxed runner for executing agent benchmarks.

### 1. Installation
Install the `inspect-ai` framework along with the standardized `inspect-evals` package:
```bash
pip install inspect-ai inspect-evals
```

### 2. Configure Environment
Set up your LLM API keys and configure docker for safe execution of agent actions:
```bash
export ANTHROPIC_API_KEY="your-api-key"
export OPENAI_API_KEY="your-api-key"
```

## CLI examples

### Running GAIA Evaluations via Inspect
Run the full GAIA validation suite against a frontier model:
```bash
inspect eval inspect_evals/gaia --model anthropic/claude-5.1
```

### Filtering by Difficulty Levels
GAIA categorizes questions into three difficulty levels. You can target specific subsets to save cost or test specialized agent traits:
```bash
# Evaluate Level 1 (easiest, basic tool use)
inspect eval inspect_evals/gaia_level1 --model openai/gpt-5.5

# Evaluate Level 3 (hardest, multi-step long-horizon reasoning)
inspect eval inspect_evals/gaia_level3 --model anthropic/claude-5.1
```

### Running with Limited Samples
For faster feedback loops, limit the evaluation to a subset of samples:
```bash
inspect eval inspect_evals/gaia_level2 --limit 5 --model meta-llama/llama-4-70b-instruct
```

## API examples
You can execute and custom-parse GAIA evaluations programmatically using the Inspect Python API.

### Custom Evaluator Pipeline
```python
from inspect_ai import eval
from inspect_evals.gaia import gaia

# Execute validation on GAIA programmatically
results = eval(
    gaia(split="validation", subset="2023_all"),
    model="anthropic/claude-5.1",
    limit=10,
    max_tasks=2
)

# Extract and output performance statistics
for task in results:
    print(f"Task ID: {task.sample_id}")
    print(f"Status: {task.status}")
    if task.scores:
        accuracy = task.scores.get("accuracy")
        print(f"Score: {accuracy.value if accuracy else 'N/A'}")
```

### Programmatic Ingestion and Run Hook
Load and filter GAIA datasets programmatically within custom evaluation workflows, validating the payload using **Pydantic v2**:
```python
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class GAIAQuestion(BaseModel):
    task_id: str = Field(..., alias="task_id")
    question: str
    level: int = Field(..., ge=1, le=3)
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Validate standard GAIA evaluation schema using Pydantic v2
raw_data = {
    "task_id": "gaia-2026-level1-12",
    "question": "What is the total revenue of the company mentioned in the PDF?",
    "level": 1,
    "file_name": "annual_report.pdf",
    "file_type": "pdf"
}

question = GAIAQuestion.model_validate(raw_data)
print(f"Validated GAIA Level {question.level} Task: {question.task_id}")
```

## Related tools / concepts
- [PA-bench](./pa-bench.md) — Web navigation benchmark.
- [AssistantBench](./assistant-bench.md) — Multi-step web mission benchmark.
- [OSWorld](./os-world.md) — Desktop OS agent benchmark.
- [Humanity's Last Exam](./humanitys-last-exam.md) — Frontier reasoning benchmark.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Implementation patterns for GAIA-capable agents.
- [Tool Calling](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Foundational capability for GAIA tasks.
- [Inspect AI](./inspect-ai.md) — The framework used to run GAIA.

## Licensing and cost
- **Open Source**: Yes (CC-BY-SA 4.0).
- **Cost**: The benchmark dataset and evaluation software are open source. Executing agents over GAIA requires LLM API credits; Level 3 tasks can consume substantial tokens due to long execution loops.

## Sources / references
- [GAIA: A Benchmark for General AI Assistants (ArXiv)](https://arxiv.org/abs/2311.12983)
- [GAIA Project Website](https://gaia-benchmark.github.io/)
- [GAIA Leaderboard (Hugging Face)](https://huggingface.co/spaces/gaia-benchmark/leaderboard)

## Contribution Metadata
- Last reviewed: 2026-12-31
- Confidence: high

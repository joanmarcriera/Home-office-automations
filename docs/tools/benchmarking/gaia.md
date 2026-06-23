# GAIA (General AI Assistants)

## What it is
GAIA (General AI Assistants) is a benchmark designed to evaluate General AI Assistants. It consists of 450 non-trivial questions that are conceptually simple for humans but challenging for most advanced AI systems. It is the gold standard for measuring 'System 2' reasoning in agents as of June 2026.

## What problem it solves
Existing benchmarks often focus on narrow tasks or synthetic reasoning. GAIA targets real-world tasks that require fundamental abilities such as reasoning, multi-modality handling, web browsing, and tool-use proficiency. It aims to measure how well an agent can function as a general-purpose assistant, effectively identifying the 'reasoning gap' in frontier models.

## Where it fits in the stack
**Eval**. It provides a high-signal benchmark for testing autonomous agents and LLMs on multi-step, real-world tasks. It is frequently used to validate the 'Agentic Core' of systems built on Claude 4.8 and GPT-5.5.

## Typical use cases
- **Agent Benchmarking**: Comparing the performance of different agent architectures on realistic assistant tasks.
- **Tool-Use Proficiency**: Measuring an agent's ability to select and use external tools (browsers, interpreters, MCP 3.0 servers) correctly.
- **Reasoning Evaluation**: Testing long-horizon reasoning and planning in open-ended environments.
- **VLM Testing**: Benchmarking the vision capabilities of models when interacting with complex documents and images.

## Strengths
- **Non-synthetic**: Questions are grounded in real-world scenarios.
- **Ease for Humans**: Tasks are generally easy for a human to complete in a few minutes, making the performance gap with AIs very clear.
- **Multi-modal**: Requires handling text, images, and other file formats.
- **Robustness**: Designed to be hard to solve via pure memorization or "cheating" through data contamination.

## Limitations
- **Evaluation Difficulty**: Requires execution-based evaluation or human-in-the-loop for complex open-ended responses.
- **Environment Dependency**: Web-based tasks are subject to site changes.
- **High Friction**: Level 3 tasks can take significant time and API costs for agents to attempt.

## When to use it
- When you want to evaluate the "generalist" capability of an AI agent.
- When you need a benchmark that goes beyond simple RAG or coding.
- To measure progress in autonomous planning and tool execution.

## When not to use it
- For testing very specific domain expertise (e.g., medical, legal) unless it falls under general assistant tasks.
- For lightweight testing where a simpler benchmark (like MMLU-Pro) suffices.
- For low-latency regression testing.

## Getting started
GAIA evaluations are primarily executed using the `inspect-ai` framework, which provides a standardized environment for agentic benchmarks.

### 1. Installation
```bash
pip install inspect-ai inspect-evals
```

### 2. Basic Evaluation
Run the full GAIA validation set against a model:
```bash
inspect eval inspect_evals/gaia --model openai/gpt-5.5
```

## CLI examples

### Run Specific Difficulty Levels
GAIA is divided into levels 1, 2, and 3. You can run them individually:
```bash
# Run only Level 1 (easiest)
inspect eval inspect_evals/gaia_level1 --model anthropic/claude-4.8

# Run only Level 3 (hardest)
inspect eval inspect_evals/gaia_level3 --model anthropic/claude-4.8
```

### Limit Samples and Parallelism
For faster testing, limit the number of samples and control connection limits:
```bash
inspect eval inspect_evals/gaia --limit 10 --max-connections 5 --model openai/gpt-5.5
```

### Use Custom Prompts
Override the default prompt template to test different agent instructions:
```bash
inspect eval inspect_evals/gaia --model openai/gpt-5.5 -K input_prompt="Answer this: {question} using the provided file: {file}"
```

## API examples
You can integrate GAIA into your own Python evaluation pipelines using the Inspect API.

### Minimal Evaluation Script
```python
from inspect_ai import eval
from inspect_evals.gaia import gaia

# Run GAIA validation set
results = eval(
    gaia(split="validation", subset="2023_all"),
    model="openai/gpt-5.5",
    limit=5
)

# Access results
for result in results:
    print(f"Task ID: {result.sample_id}, Score: {result.scores['accuracy'].value}")
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
- **Open Source**: Yes (Apache 2.0 / CC-BY-SA 4.0)
- **Cost**: Free to use the benchmark, but requires LLM API credits. High-level tasks can be expensive due to multiple tool calls.

## Sources / References
- [GAIA: A Benchmark for General AI Assistants (ArXiv)](https://arxiv.org/abs/2311.12983)
- [GAIA Project Website](https://gaia-benchmark.github.io/)
- [GAIA Leaderboard (Hugging Face)](https://huggingface.co/spaces/gaia-benchmark/leaderboard)

## Contribution Metadata
- Last reviewed: 2026-06-23
- Confidence: high

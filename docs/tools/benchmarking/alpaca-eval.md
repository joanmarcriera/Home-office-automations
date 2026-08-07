# AlpacaEval

## What it is
AlpacaEval is an automatic evaluator for instruction-following language models. It is designed to be fast, cheap, and highly correlated with human preferences. As of late 2026, it serves as a critical performance baseline for frontier models like **Claude 5.1**, **GPT-5.5**, **Gemini 4.0 Pro**, **Llama 4**, and **Gemma 3**, measuring the win rate of a model's outputs against a reference model using an LLM-based automatic annotator.

## What problem it solves
Evaluation of instruction-following models typically requires human interaction, which is time-consuming, expensive, and difficult to replicate. AlpacaEval provides a replicable, automated proxy that allows developers to iterate quickly by simulating human preference judgments. It specifically addresses "verbosity bias" through length-controlled metrics and now incorporates the **MCP 3.1** and **FastMCP 3.1** protocol for automated benchmarking across diverse environments.

## Where it fits in the stack
[Layer 7: Evaluation & Guardrails](../../knowledge_base/ai_tooling_landscape.md#layer-7-evaluation-guardrails) — specifically as an **Automated Instruction-Following Benchmark**.

## Typical use cases
- **Model Development**: Running frequent evaluations during the training or fine-tuning process.
- **Comparative Analysis**: Measuring how a new model performs against established baselines like **Gemma 3**, **Qwen 3.6**, or **GPT-5.5**.
- **Prompt Engineering**: Testing the impact of different system prompts on model performance.
- **Automated Benchmarking**: Using the **MCP 3.1 Task Protocol** to trigger evaluations across distributed compute clusters.

## Strengths
- **Speed and Cost**: Can run in less than 5 minutes for under $10.
- **Human Correlation**: AlpacaEval 2.0 maintains a high Spearman correlation (>0.98) with Chatbot Arena.
- **Length Normalization**: Effectively mitigates the bias toward longer outputs using length-controlled win rates.
- **MCP 3.1 Compatibility**: Allows for standardized task execution, structural telemetry collection, and parallel evaluations.

## Limitations
- **Style over Substance**: Like many LLM-based evaluators, it may favor the style and tone of a response over its factual accuracy.
- **Instruction Breadth**: The evaluation set might not be representative of extremely complex or niche professional tasks.
- **Safety**: It does not measure model safety, toxicity, or potential for harm (use [SharpAI Security Benchmark](sharp-ai.md)).
- **Judge Bias**: The choice of "judge" model (e.g., using GPT-5.5 to judge GPT-5.5) can influence the results.

## When to use it
- When you need quick, automated feedback on model quality during development.
- When you want to see how a model's conversational performance aligns with human-perceived quality.
- For initial screening of model checkpoints before human evaluation.
- When benchmarking **Gemma 3** or other open-weights models against proprietary leaders.

## When not to use it
- For high-stakes decisions regarding model safety or final production release (use [SharpAI Security Benchmark](sharp-ai.md)).
- When you need to evaluate specific technical domains (e.g., medical, legal) that require expert verification.
- When evaluating non-instruction-following base models.
- For measuring factual correctness in extremely narrow or data-sensitive domains.

## Getting started

### 1. Installation
```bash
pip install alpaca_eval
```

### 2. Configuration
Set your API key for the evaluator model (e.g., OpenAI API for GPT-5.5 or Anthropic API for Claude 5.1).

```bash
export OPENAI_API_KEY="your_api_key"
```

### 3. Running an Evaluation
AlpacaEval requires a JSON or JSONL file containing the model's outputs for the evaluation set.

```bash
# Evaluate your model outputs
alpaca_eval --model_outputs 'path/to/your_model_outputs.json'
```

## CLI examples
Commonly used arguments for the `alpaca_eval` command:

```bash
# Basic evaluation
alpaca_eval --model_outputs 'outputs.json'

# Use a specific annotator (e.g., GPT-5.5)
alpaca_eval --model_outputs 'outputs.json' --annotator_config 'weighted_alpaca_eval_gpt5_5'

# Specify output directory
alpaca_eval --model_outputs 'outputs.json' --output_path './results'

# Run via MCP 3.1 Task Protocol
alpaca_eval run-task --task-file 'benchmarking_task.json' --protocol mcp3.1
```

## API examples
AlpacaEval can be used programmatically within Python workflows. This SOTA December 2026 example includes strict **Pydantic v2** validation to model, parse, and verify the AlpacaEval summary results.

```python
from pydantic import BaseModel, Field, condecimal
from typing import Dict, Any, Optional
from datetime import datetime

# Define schemas with strict Pydantic v2 validation
class LengthControlledWinRate(BaseModel):
    raw_win_rate: condecimal(ge=0, le=100)
    adjusted_win_rate: condecimal(ge=0, le=100)
    length_bias_coefficient: float = Field(..., description="Calculated factor of verbosity influence")

class AlpacaEvalRun(BaseModel):
    model_name: str
    judge_model: str = Field(default="gpt-5.5")
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    metrics: LengthControlledWinRate
    metadata: Dict[str, Any] = Field(default_factory=dict)

# Programmatic evaluation parser
def parse_and_verify_eval(data: dict) -> AlpacaEvalRun:
    # Strict validation of incoming benchmark execution results
    run = AlpacaEvalRun.model_validate(data)
    print(f"Successfully audited results for: {run.model_name}")
    print(f"Adjusted Win Rate against reference: {run.metrics.adjusted_win_rate}%")
    return run

# Mock benchmark outputs from Gemini 4.0 Pro run
gemini_run_output = {
    "model_name": "gemini-4.0-pro",
    "judge_model": "claude-5.1-sonnet",
    "metrics": {
        "raw_win_rate": 84.50,
        "adjusted_win_rate": 81.20,
        "length_bias_coefficient": 0.04
    },
    "metadata": {
        "dataset_version": "2.1",
        "mcp_agent": "FastMCP-3.1-Orchestrator"
    }
}

validated_run = parse_and_verify_eval(gemini_run_output)
```

## Related tools / concepts
- [Chatbot Arena](./chatbot-arena.md) - The "ground truth" human preference leaderboard.
- [MT-Bench](./mt-bench.md) - Multi-turn conversation benchmark.
- [MMLU](./mmlu.md) - Knowledge-based benchmark.
- [GPQA](./gpqa.md) - Expert-level reasoning benchmark.
- [LM Evaluation Harness](./lm-evaluation-harness.md) - Framework for running many benchmarks.
- [EvalPlus](./evalplus.md) - Robust code generation testing.
- [Gemma 3](../ai_knowledge/local_llms.md) - Local open-weights model evaluated using AlpacaEval.
- [Claude](../ai_knowledge/claude.md) - Suite of models analyzed by automatic judges.
- [SharpAI Security Benchmark](sharp-ai.md) - Robust security evaluator for agent tool access.

## Sources / references
- [GitHub Repository for AlpacaEval](https://github.com/tatsu-lab/alpaca_eval)
- [AlpacaEval 2.0 Paper (Dubois et al., 2024)](https://arxiv.org/abs/2404.04475)
- [Official Leaderboard Website](https://tatsu-lab.github.io/alpaca_eval/)
- [MCP 3.1 Task Protocol Specifications](https://mcp.dev/protocols/task-protocol)

## Contribution Metadata
- Last reviewed: 2026-12-19
- Confidence: high

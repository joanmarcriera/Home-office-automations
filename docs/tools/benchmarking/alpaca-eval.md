# AlpacaEval

## What it is
AlpacaEval is an automatic evaluator for instruction-following language models. It is designed to be fast, cheap, and highly correlated with human preferences. As of early 2027, it serves as a critical performance baseline for frontier models like **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Gemma 4**, measuring the win rate of a model's outputs against a reference model using an LLM-based automatic annotator.

---

## Architecture & System Topology

```
+---------------------------------------------------------------------------------------------------+
|                                 ALPACAEVAL 3.0 EVALUATION PIPELINE                                |
|                                                                                                   |
|  +--------------------+      +-------------------------+      +--------------------------------+  |
|  | AlpacaEval 805     |      | Candidate Model         |      | Reference Baseline Model       |  |
|  | Test Prompts       |----->| Outputs (Model A)       |----->| Outputs (GPT-4 / Claude 3.5)   |  |
|  +--------------------+      +-------------------------+      +--------------------------------+  |
|                                           |                                  |                    |
|                                           +----------------+-----------------+                    |
|                                                            |                                      |
|                                                            v                                      |
|  +---------------------------------------------------------------------------------------------+  |
|  |                            AUTOMATIC LLM JUDGE ENGINE (GPT-5.6 / Claude 5.6)               |  |
|  |                       Pairwise Preference Scoring & Swapped Order Pass                      |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                            |                                      |
|                                                            v                                      |
|  +---------------------------------------------------------------------------------------------+  |
|  |                        BIAS CORRECTION & STATISTICAL NORMALIZER                             |  |
|  |                 Length-Controlled Win Rate (LC-WR) & Position Swap De-biasing                |  |
|  +---------------------------------------------------------------------------------------------+  |
|                                                            |                                      |
|                                                            v                                      |
|  +---------------------------------------------------------------------------------------------+  |
|  |                         FASTMCP 3.1 SCORE AGGREGATOR & REPORTING LAYER                      |  |
|  |                      Telemetry Stream & Leaderboard JSON Schema Generation                  |  |
|  +---------------------------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------------------------+
```

---

## What problem it solves
Evaluation of instruction-following models typically requires human interaction, which is time-consuming, expensive, and difficult to replicate. AlpacaEval provides a replicable, automated proxy that allows developers to iterate quickly by simulating human preference judgments. It specifically addresses "verbosity bias" through length-controlled metrics and incorporates the **MCP 3.1** and **FastMCP 3.1** protocol for automated benchmarking across diverse environments.

1. **Human Evaluation Bottlenecks**: Replaces manual crowdsourced human preference grading with standardized LLM judges that run in minutes.
2. **Verbosity Exploitation**: Mitigates models "gaming" evaluations by generating excessively wordy responses through GLM-based Length-Controlled (LC) Win Rate adjustments.
3. **Inconsistent Judge Bias**: Addresses positional bias (favoring response A over B based on presentation order) via mandatory bidirectional prompt swapping passes.

---

## Where it fits in the stack
[Layer 7: Evaluation & Guardrails](../../knowledge_base/ai_tooling_landscape.md#layer-7-evaluation-guardrails) — specifically as an **Automated Instruction-Following Benchmark**.

---

## Typical use cases
- **Model Development**: Running frequent evaluations during the training or fine-tuning process.
- **Comparative Analysis**: Measuring how a new model performs against established baselines like **Gemma 4**, **Qwen 3.6 VL**, or **GPT-5.6**.
- **Prompt Engineering**: Testing the impact of different system prompts on model performance.
- **Automated Benchmarking**: Using the **FastMCP 3.1 Task Protocol** to trigger evaluations across distributed compute clusters.
- **RLHF / DPO Alignment Tuning**: Tracking win-rate trajectory across reward modeling iterations.

---

## Strengths
- **Speed and Cost**: Can run an 805-prompt evaluation in under 5 minutes for under $10 in API judge costs.
- **Human Correlation**: AlpacaEval 2.0/3.0 maintains a high Spearman correlation (>0.98) with Chatbot Arena ELO ratings.
- **Length Normalization**: Effectively mitigates the bias toward longer outputs using length-controlled win rates.
- **FastMCP 3.1 Compatibility**: Allows for standardized task execution, structural telemetry collection, and parallel evaluations.

---

## Limitations
- **Style over Substance**: Like many LLM-based evaluators, it may favor the style and tone of a response over its factual accuracy.
- **Instruction Breadth**: The evaluation set might not be representative of extremely complex or niche professional tasks.
- **Safety**: It does not measure model safety, toxicity, or potential for harm (use [SharpAI Security Benchmark](sharp-ai.md)).
- **Judge Bias**: The choice of "judge" model (e.g., using GPT-5.6 to judge GPT-5.6) can introduce subtle self-preference bias.

---

## When to use it
- When you need quick, automated feedback on model quality during development.
- When you want to see how a model's conversational performance aligns with human-perceived quality.
- For initial screening of model checkpoints before human evaluation.
- When benchmarking **Gemma 4** or other open-weights models against proprietary leaders.

---

## When not to use it
- For high-stakes decisions regarding model safety or final production release (use [SharpAI Security Benchmark](sharp-ai.md)).
- When you need to evaluate specific technical domains (e.g., medical, legal) that require expert verification.
- When evaluating non-instruction-following base models.
- For measuring factual correctness in extremely narrow or data-sensitive domains.

---

## Feature Comparison Matrix

| Metric / Benchmark | AlpacaEval 3.0 | Chatbot Arena (LMSYS) | MT-Bench | EvalPlus |
| :--- | :--- | :--- | :--- | :--- |
| **Evaluation Type** | Automated LLM Judge | Crowdsourced Human Preference | Multi-Turn LLM Judge | Unit Test Execution |
| **Execution Time** | < 5 Minutes | Days / Weeks (Continuous) | ~15 Minutes | ~10 Minutes |
| **Cost per Model Run** | ~$5 - $15 API Costs | Free (Crowdsourced) | ~$5 - $10 API Costs | $0 (Local Python Execution) |
| **Length Bias Control** | Length-Controlled Win Rate | Bradley-Terry ELO | None (Raw Grades 1-10) | N/A (Pass/Fail Tests) |
| **FastMCP 3.1 Protocol** | Native | N/A | Extension Available | Native |
| **Human Correlation** | r > 0.98 | Ground Truth | r ~ 0.85 | N/A |

---

## Cost Estimation & Latency Metrics

| Operation / Benchmark Step | API Token Usage | Mean Execution Time | Estimated Cost (GPT-5.6 Judge) |
| :--- | :--- | :--- | :--- |
| **Dataset Output Generation (805 prompts)**| ~450k Output Tokens | 2.5 Minutes | Depends on Candidate Model |
| **Single Order Preference Pass** | ~1.2M Input / 180k Output | 1.8 Minutes | ~$3.50 |
| **Position Swap Preference Pass** | ~1.2M Input / 180k Output | 1.8 Minutes | ~$3.50 |
| **Length-Control Regression Pass** | 0 Tokens (Local SciPy) | 450 ms | $0.00 |
| **Total Evaluation Run** | **~2.8M Total Tokens** | **< 5 Minutes** | **~$7.00 - $10.00** |

---

## Getting started

### 1. Installation
```bash
pip install alpaca_eval
```

### 2. Configuration
Set your API key for the evaluator model (e.g., OpenAI API for GPT-5.6 or Anthropic API for Claude 5.6).

```bash
export OPENAI_API_KEY="your_api_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
```

### 3. Running an Evaluation
AlpacaEval requires a JSON or JSONL file containing the model's outputs for the evaluation set.

```bash
# Evaluate your model outputs
alpaca_eval --model_outputs 'path/to/your_model_outputs.json'
```

---

## CLI examples

```bash
# Basic evaluation using default length-controlled judge
alpaca_eval --model_outputs 'outputs.json'

# Use a specific SOTA annotator config (e.g., GPT-5.6 or Claude 5.6)
alpaca_eval --model_outputs 'outputs.json' --annotator_config 'weighted_alpaca_eval_gpt5_6'

# Save detailed pairwise annotations to custom output directory
alpaca_eval --model_outputs 'outputs.json' --output_path './results_gemini4/' --is_save_leaderboard True

# Run via FastMCP 3.1 Task Protocol command wrapper
alpaca_eval run-task --task-file 'benchmarking_task.json' --protocol mcp3.1
```

---

## API examples

### Programmatic Evaluation & Schema Validation with Pydantic v2
The following complete Python FastMCP 3.1 server runs AlpacaEval benchmark validations, models result payloads using Pydantic v2, and computes length-controlled win rates:

```python
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, condecimal, ConfigDict
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP 3.1 Server
mcp = FastMCP("AlpacaEvalBenchmarkServer")

class LengthControlledMetrics(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    raw_win_rate: float = Field(..., ge=0.0, le=100.0, description="Unadjusted win rate percentage")
    length_controlled_win_rate: float = Field(..., ge=0.0, le=100.0, alias="lcWinRate", description="Length-controlled adjusted win rate")
    standard_error: float = Field(..., ge=0.0, description="Standard error of the win rate estimate")
    avg_output_length: int = Field(..., ge=1, description="Average output character length")

class AlpacaEvalRunPayload(BaseModel):
    model_name: str = Field(..., min_length=1)
    judge_model: str = Field(default="gpt-5.6")
    reference_model: str = Field(default="gpt-4-turbo")
    dataset_version: str = Field(default="3.0")
    executed_at: datetime = Field(default_factory=datetime.utcnow)
    metrics: LengthControlledMetrics
    metadata: Dict[str, Any] = Field(default_factory=dict)


@mcp.tool()
def validate_and_record_benchmark(eval_data: Dict[str, Any]) -> str:
    """
    Parses, validates, and records an AlpacaEval 3.0 benchmark execution run using Pydantic v2.
    """
    try:
        run = AlpacaEvalRunPayload.model_validate(eval_data)

        summary = {
            "status": "VALIDATED",
            "model": run.model_name,
            "judge": run.judge_model,
            "lc_win_rate": run.metrics.length_controlled_win_rate,
            "raw_win_rate": run.metrics.raw_win_rate,
            "length_bias_delta": round(run.metrics.raw_win_rate - run.metrics.length_controlled_win_rate, 2),
            "executed_at": run.executed_at.isoformat()
        }
        return json.dumps(summary, indent=2)
    except Exception as err:
        return json.dumps({"status": "VALIDATION_FAILED", "details": str(err)}, indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## Custom LLM Judge Setup & Rate Limits

To configure a custom judge (such as an internal or self-hosted model behind an OpenAI-compatible endpoint):

1. Create a custom annotator configuration file at `~/.alpaca_eval/annotators/custom_judge.yaml`:
```yaml
custom_judge:
  prompt_template: "alpaca_eval/src/alpaca_eval/evaluators/evaluator_configs/alpaca_eval_gpt4/alpaca_eval.txt"
  fn_completions: "openai_completions"
  completions_kwargs:
    model_name: "custom-local-llama4"
    model_api_base: "http://localhost:8000/v1"
    max_tokens: 2048
    temperature: 0.0
  batch_size: 16
```

2. Pass the custom configuration:
```bash
alpaca_eval --model_outputs 'outputs.json' --annotator_config 'custom_judge'
```

---

## Troubleshooting & Operational Diagnostics

### 1. Judge Rate Limit Errors (HTTP 429)
- **Symptom**: `alpaca_eval` crashes midway with `openai.RateLimitError` or `Anthropic.RateLimitError`.
- **Cause**: Exceeding concurrent completion limits on the LLM judge API.
- **Resolution**:
  Decrease parallel worker threads using the `--max_instances` or `--batch_size` parameter:
  ```bash
  alpaca_eval --model_outputs 'outputs.json' --max_instances 4
  ```

### 2. Format Parsing Failure in Annotations
- **Symptom**: High rate of `invalid_outputs` reported in the final summary output.
- **Cause**: Judge model failed to return strict `m` (model A wins) or `r` (reference wins) tokens.
- **Resolution**:
  Use SOTA judge models with high structured output compliance (e.g., `gpt-5.6` or `claude-5.6-sonnet`).

---

## Related tools / concepts
- [Chatbot Arena](./chatbot-arena.md) - The "ground truth" human preference leaderboard.
- [MT-Bench](./mt-bench.md) - Multi-turn conversation benchmark.
- [MMLU](./mmlu.md) - Knowledge-based benchmark.
- [GPQA](./gpqa.md) - Expert-level reasoning benchmark.
- [LM Evaluation Harness](./lm-evaluation-harness.md) - Framework for running many benchmarks.
- [EvalPlus](./evalplus.md) - Robust code generation testing.
- [Gemma 4](../ai_knowledge/local_llms.md) - Local open-weights model evaluated using AlpacaEval.
- [Claude](../ai_knowledge/claude.md) - Suite of models analyzed by automatic judges.
- [SharpAI Security Benchmark](sharp-ai.md) - Robust security evaluator for agent tool access.

---

## Sources / references
- [GitHub Repository for AlpacaEval](https://github.com/tatsu-lab/alpaca_eval)
- [AlpacaEval 2.0 Paper (Dubois et al., 2024)](https://arxiv.org/abs/2404.04475)
- [Official Leaderboard Website](https://tatsu-lab.github.io/alpaca_eval/)
- [FastMCP 3.1 Task Protocol Specifications](https://mcp.dev/protocols/task-protocol)

---

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

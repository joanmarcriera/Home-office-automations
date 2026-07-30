# LongCLI-Bench

## What it is
LongCLI-Bench is a specialized benchmark focused on evaluating AI agents in long-horizon programming tasks within command-line interfaces (CLIs). It measures an agent's ability to plan and execute multi-step engineering workflows that span dozens of terminal turns. As of November 2026, it is a key metric for evaluating high-autonomy tools like [Claude Code](../development_ops/claude-code-setup.md) which utilize [Model Context Protocol (MCP 3.1)](../../tools/automation_orchestration/mcp.md) for dynamic tool and task orchestration.

## What problem it solves
It addresses the gap in agent evaluation for realistic, multi-step software engineering tasks. Most existing benchmarks are limited by short horizons or lack of fine-grained metrics. LongCLI-Bench specifically tests for "stalling" behaviors, planning failures, and the ability to maintain state across long sessions in a terminal environment.

## Where it fits in the stack
**Eval / Benchmarking**. It is a specialized benchmark for evaluating the **Agentic** and **Execution** layers of AI coding systems.

## Typical use cases
- **Coding Assistant Benchmarking**: Testing tools like [Aider](../development_ops/aider.md) or [OpenHands](../development_ops/openhands.md) on complex, multi-tool tasks.
- **Failure Analysis**: Identifying specific points of failure in long-running CLI sessions to improve agent robustness.
- **Horizon Testing**: Measuring how many sequential steps an agent can take before losing context or diverging from the goal.
- **Human-Agent Collaboration Study**: Evaluating how partial human guidance (reference plans) affects success rates.

## Strengths
- **Long-Horizon focus**: Specifically targets tasks requiring sustained reasoning and multiple sequential actions.
- **Fine-Grained Scoring**: Pinpoints exactly where an agent stalls or deviates from the task requirements using step-level metrics.
- **State-Awareness**: Requires the agent to manage environment state (files, processes, variables) over many turns.
- **Contamination Resistance**: Uses fresh computer science assignments and custom tasks that are less likely to be in training data.

## Limitations
- **CLI-Centric**: Focused entirely on terminal interactions; does not evaluate GUI or web-based agency.
- **Environment Setup**: Requires a controlled shell environment, which can be complex to reproduce at scale.
- **High Latency**: Due to the multi-step nature, running a full evaluation pass is time-consuming compared to single-turn benchmarks.

## When to use it
- When testing agents designed for autonomous coding or complex system administration.
- When you need a rigorous evaluation of an agent's ability to follow multi-step instructions without stalling.
- When comparing the "planning depth" of different frontier models like **Claude 5.1**, **GPT-5.5**, or **Gemini 4.0**.

## When not to use it
- For testing general chat capabilities or single-turn information retrieval.
- When evaluation does not involve terminal or shell access.
- For quick, high-level model comparisons where [SWE-bench](swe-bench.md) or [HumanEval](human-eval.md) might suffice.

## Getting started
LongCLI-Bench requires a Python 3.10+ environment and access to a terminal emulator.

### 1. Installation
```bash
git clone https://github.com/finyorko/longcli-bench.git
cd longcli-bench
pip install -e .
```

### 2. Running a Baseline
Run a sample task using a local agent or a mock agent to verify the setup:
```bash
python run_eval.py --agent "mock" --task_id "refactor_001" --output_dir "./results"
```

## CLI examples
The following commands illustrate how to interact with the LongCLI-Bench harness.

```bash
# List all available tasks in the benchmark
python run_eval.py --list_tasks

# Run evaluation on a specific category (e.g., debugging) using Claude 5.1
python run_eval.py --agent "claude-code" --category "debugging" --model "claude-5-1-sonnet-20261022"

# Visualize results and generate a failure analysis report
python scripts/analyze_results.py --input_dir "./results" --format "html"
```

## API examples
You can integrate LongCLI-Bench into custom evaluation pipelines using its Python API.

### Initializing a Task
```python
from longcli_bench import TaskManager, AgentHarness

# Load a specific task instance
tm = TaskManager()
task = tm.get_task("refactor_001")

print(f"Goal: {task.goal}")
print(f"Steps: {len(task.reference_steps)}")
```

### Running an Agent Loop
```python
# Initialize the harness for a specific agent
harness = AgentHarness(agent_cmd="aider --message")

# Execute the agent against the task environment
result = harness.run_task(task)

print(f"Task Status: {result.status}")
print(f"Step Success Rate: {result.step_accuracy:.2%}")
```

### Telemetry and Session Verification via Pydantic v2
This Python script validates LongCLI-Bench agent execution sessions using **Pydantic v2** prior to exporting metrics for downstream OLAP ingestion:

```python
import json
from typing import Optional, List
from pydantic import BaseModel, Field, ValidationError, field_validator

class TerminalCommandRecord(BaseModel):
    command: str = Field(..., description="The exact shell command run by the agent")
    exit_code: int = Field(..., description="The return code of the shell execution")
    duration_seconds: float = Field(..., ge=0.0, description="Duration of command execution")

class LongCLIExecutionSession(BaseModel):
    session_id: str = Field(..., description="Unique UUID for the evaluation session")
    agent_name: str = Field(..., description="Name of the agent evaluated (e.g., claude-code)")
    model_name: str = Field(..., description="The underlying model (e.g., claude-5-1-sonnet)")
    steps_taken: int = Field(..., gt=0, description="Number of terminal turns taken")
    commands: List[TerminalCommandRecord] = Field(default_factory=list, description="Sequence of shell commands run")
    stalled: bool = Field(False, description="Did the agent enter a loop or stall?")
    final_success: bool = Field(False, description="Whether the agent achieved the task goal")

    @field_validator("steps_taken")
    @classmethod
    def validate_steps_match_commands(cls, value: int, info) -> int:
        # A simple validator checking consistency of turns vs commands list
        return value

def validate_telemetry(raw_json: str) -> Optional[LongCLIExecutionSession]:
    try:
        data = json.loads(raw_json)
        # Validate telemetry payload using Pydantic v2
        session = LongCLIExecutionSession.model_validate(data)
        return session
    except json.JSONDecodeError:
        print("Error: Invalid JSON syntax.")
    except ValidationError as e:
        print(f"Validation failed: {e.errors()}")
    return None
```

## Related tools / concepts
- [SWE-bench](swe-bench.md) — Real-world GitHub issue resolution.
- [Terminal-Bench](terminal-bench.md) — Tool-use evaluation in the CLI.
- [Aider](../development_ops/aider.md) — High-momentum terminal coding assistant.
- [Claude Code](../development_ops/claude-code-setup.md) — Primary target for long-horizon CLI testing.
- [OpenHands](../development_ops/openhands.md) — Open-source agent environment.
- [Plandex](../development_ops/plandex.md) — AI coding engine for complex tasks.
- [Benchmarking](index.md) — Core concepts in LLM evaluation.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for multi-step AI execution.

## Sources / references
- [GitHub Repository](https://github.com/finyorko/longcli-bench)
- [arXiv Preprint (arXiv:2602.14337)](https://arxiv.org/abs/2602.14337)
- [Hugging Face Paper Page](https://huggingface.co/papers/2602.14337)

## Contribution Metadata
- Last reviewed: 2026-11-03
- Confidence: high

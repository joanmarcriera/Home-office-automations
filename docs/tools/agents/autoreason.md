# AutoReason

## What it is
AutoReason (v2027.1.x+, early January 2027) is an autonomous reasoning framework by Nous Research designed to enable LLMs to perform complex, multi-step logical tasks with minimal human intervention. It implements advanced "Reasoning-as-a-Service" patterns, allowing models like Nous Hermes 4 (Llama 4 based), [Gemma 4](../ai_knowledge/local_llms.md), and [DeepSeek-V4](../providers/deepseek.md) to compete with proprietary reasoning models like the Claude 5.6 and Gemini 4.0 Ultra series.

## What problem it solves
It addresses the limitations of standard chain-of-thought prompting by providing a structured environment for iterative reasoning, verification, and correction. It helps LLMs navigate large "search spaces" in complex logic, mathematics, or code problems where the first answer is rarely the correct one, effectively reducing hallucinations through automated self-critique.

## Where it fits in the stack
**Category**: Agent / Reasoning Engine. It operates as an orchestration layer above the raw inference API, wrapping model calls in a "Verify-and-Correct" loop that integrates with external verification tools (interpreters, checkers, MCP servers).

## Typical use cases
- **Complex Logical Puzzles**: Problems requiring backtracking and testing multiple conflicting hypotheses.
- **Mathematical Theorem Proving**: Structured steps with rigorous automated verification requirements.
- **Code Debugging**: Identifying root causes by iteratively testing assumptions against a live execution environment.
- **Deep Research**: Multi-hop reasoning tasks where the results of one step fundamentally redefine the search parameters for the next.
- **Synthetic Data Generation**: Creating high-quality reasoning traces for fine-tuning smaller models like [Gemma 4](../ai_knowledge/local_llms.md).

## Strengths
- **Self-Correction**: Significantly reduces hallucinations by requiring the model to "show its work" and then programmatically check it via the **FastMCP 3.1 Task Protocol**.
- **Open-Source**: Developed with a focus on open-weight model compatibility (Nous Hermes, Llama 4, DeepSeek-V4, [Gemma 4](../ai_knowledge/local_llms.md)).
- **Structured Trace**: Provides a complete, auditable log of every reasoning step and correction.
- **Flexibility**: Can be integrated with any Python-based verification tool or FastMCP 3.1-enabled service.

## Limitations
- **High Token Consumption**: Iteration and verification loops can consume 5-10x more tokens than single-shot inference.
- **Inference Latency**: Not suitable for real-time human interaction; tasks often take seconds or minutes to converge.
- **Complexity**: Writing effective "verifiers" for new domains requires specialized prompt engineering and coding.

## When to use it
- **High-Stakes Logic**: When the cost of an incorrect logical step is high and multi-step verification is available.
- **Open-Weight Model Optimization**: When trying to achieve "reasoning" performance on par with proprietary models using local/open-weights.
- **Iterative Debugging**: For complex code issues where the agent must "test" a hypothesis and receive feedback from a runtime.
- **Non-Interactive Batch Tasks**: Ideal for "overnight" research or optimization tasks.

## When not to use it
- **Low-Latency Chat**: The iterative nature makes it too slow for standard conversational UI.
- **Simple Summarization**: For tasks that don't require logic (e.g., "summarize this email"), the overhead is unjustifiable.
- **Strict Budget Constraints**: High token usage makes it expensive for high-volume, low-value tasks.

## Getting started

### Installation
```bash
git clone https://github.com/NousResearch/autoreason.git
cd autoreason
pip install -r requirements.txt
```

### Basic Configuration
Configure the `config.yaml` to point to your preferred reasoning model (e.g., local Ollama instance or LiteLLM proxy).

## CLI examples
```bash
# Run the main experiment runner for a reasoning task
python run_reasoning.py --task "Prove the square root of 2 is irrational"

# Run the code-specific debugger on a local directory
python run_code_debug.py --path ./src/buggy_project

# Launch the reasoning-as-a-service FastMCP 3.1 server
python -m autoreason.mcp_server --port 18795
```

## API examples

### Example: Basic Reasoner Setup
```python
from autoreason import Reasoner

# Initialize with a high-reasoning model and a Python verifier
reasoner = Reasoner(
    model="nous-hermes-4-llama-4-70b",
    verifier="python_interpreter"
)
```

### Example: Pydantic v2 Reasoning Trace and Validation Schema
In rigorous automated self-critique workflows, AutoReason utilizes structured JSON schemas to trace, score, and correct intermediate steps. This program demonstrates validating this multi-hop reasoning sequence via **Pydantic v2**.

```python
import sys
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

# Define Pydantic v2 structures for reasoning hops
class ReasoningHop(BaseModel):
    hop_id: int = Field(..., description="Sequential index of the reasoning step")
    hypothesis: str = Field(..., description="Actionable hypothesis or mathematical step")
    evidence: str = Field(..., description="Grounded logic or execution outputs supporting this hop")
    status: Literal["SUCCESS", "FAILED", "INCONCLUSIVE"]

class ReasoningTrace(BaseModel):
    task: str = Field(..., description="The high-level prompt or problem to solve")
    hops: List[ReasoningHop]
    final_solution: Optional[str] = Field(None, description="The validated solution path")
    total_tokens_consumed: int = Field(..., gt=0)

    @field_validator('hops')
    @classmethod
    def check_sequential_integrity(cls, hops_list: List[ReasoningHop]) -> List[ReasoningHop]:
        # Validate that hops are sequential without jumps
        for i, hop in enumerate(hops_list):
            if hop.hop_id != i + 1:
                raise ValueError(f"Reasoning hops must be strictly sequential (expected hop_id {i + 1}, got {hop.hop_id}).")
        return hops_list

def validate_reasoning_trace(raw_trace: dict) -> None:
    try:
        validated_trace = ReasoningTrace.model_validate(raw_trace)
        print(f"Reasoning trace validated successfully for task: '{validated_trace.task}'")
        print(f"Total Hops Checked: {len(validated_trace.hops)}")
        print(f"Final Solution Validated: {validated_trace.final_solution is not None}")
    except Exception as e:
        print(f"Reasoning trace validation error: {e}", file=sys.stderr)

if __name__ == "__main__":
    print("Initializing AutoReason structured trace validation (Pydantic v2)...")

    # Mock data representing a verified self-correction trace
    mock_trace_payload = {
        "task": "Find the runtime bug in search routing algorithm",
        "hops": [
            {
                "hop_id": 1,
                "hypothesis": "Checking if division by zero occurs in weighted distance calculation.",
                "evidence": "Executed distance_calc with zero-distance node. Program threw ZeroDivisionError.",
                "status": "FAILED"
            },
            {
                "hop_id": 2,
                "hypothesis": "Introduce a epsilon-guard check before performing division in routing.",
                "evidence": "Applied fix and re-ran distance_calc. ZeroDivisionError successfully bypassed.",
                "status": "SUCCESS"
            }
        ],
        "final_solution": "Injected small epsilon float constant to distance denominator.",
        "total_tokens_consumed": 2450
    }

    validate_reasoning_trace(mock_trace_payload)
```

## Related tools / concepts
- [DeepSeek R1](../ai_knowledge/deepseek-r1.md)
- [Gemma 4](../ai_knowledge/local_llms.md)
- [Agno](agno.md)
- [Letta](letta.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Software Factories](../../knowledge_base/patterns/software-factories.md)
- [Prompt Requests](../../knowledge_base/patterns/prompt_requests.md)
- [Jules](../ai_knowledge/jules.md)
- [Claude](../ai_knowledge/claude.md)

## Sources / references
- [NousResearch/autoreason GitHub](https://github.com/NousResearch/autoreason)
- [Nous Research Blog: Iterative Reasoning Patterns](https://nousresearch.com/blog/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

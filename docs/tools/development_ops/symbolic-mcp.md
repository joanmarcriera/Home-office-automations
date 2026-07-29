# Symbolic MCP Server

## What it is
A secure, sandboxed symbolic execution engine for the Model Context Protocol that discovers edge cases and hidden bugs in Python code through mathematical path analysis. As of late October / November 2026, it is the premier formal verification tool for the MCP 3.1 ecosystem, optimized for integration with frontier models like Claude 5.1 and GPT-5.5.

## What problem it solves
Unlike traditional fuzzing (random inputs), symbolic execution treats inputs as symbolic variables and explores all possible execution paths algebraically using the Z3 solver. This provides mathematical guarantees of correctness and finds deep, hidden bugs that random testing might miss. It specifically addresses:
- **Logical Edge Cases**: Finding exact inputs that trigger rare branches or overflows.
- **Contract Verification**: Ensuring that AI-generated code adheres to strict type and logic contracts.
- **Trust Boundaries**: Proving that user-provided code cannot break the [LLM Trust Boundaries](../../knowledge_base/patterns/llm-trust-boundaries.md).

## Where it fits in the stack
**Tool / Eval**. It provides formal verification and path-sensitive analysis for Python code, acting as a critical validation layer for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- Formally verifying function contracts before deployment.
- Finding exact inputs that cause specific exceptions (e.g., `ZeroDivisionError`).
- Proving semantic equivalence between two different implementations (e.g., refactoring validation).
- Reachable code path enumeration and dead code detection.
- Automated generation of unit tests for 100% path coverage.

## Strengths
- **Path-sensitive analysis**: Explores all possible code paths, including nested logic.
- **Constraint solving**: Uses the latest Z3 solver to find precise trigger inputs.
- **Security Architecture**: Features whitelist-only module access, memory caps, and process isolation.
- **Stability**: Production-ready (v1.5.0+) with high test coverage and native MCP 3.1 support.
- **Efficiency**: Optimized for small-to-medium functions common in agentic tool-use.

## Limitations
- **Scaling Limits**: Practical limit for Z3 solver is approximately 10K lines of code per analysis unit.
- **Resource Intensive**: Requires significant memory for complex constraint solving.
- **Sandbox Restrictions**: Module whitelist is restricted to vetted modules to maintain security.
- **Language Support**: Currently restricted to Python (v3.11+).

## When to use it
- When you need mathematical proofs of code behavior.
- For high-stakes logic where random fuzzing is insufficient to find deep edge cases.
- During refactoring to ensure performance optimizations don't change behavior.
- When validating AI-generated functions from Claude 5.1 or GPT-5.5.

## When not to use it
- For very large codebases that exceed constraint solver capacity.
- When the code relies on complex external dependencies not in the module whitelist (e.g., native C extensions).
- For UI-heavy code or code involving non-deterministic IO (network, hardware).
- When simple unit testing is sufficient for the risk profile.

## Getting started

### 1. Installation
Install the server using `uv`:
```bash
uvx mcp-server-symbolic
```

### 2. Basic Verification
Verify a simple function to ensure the solver is active:
```bash
# Example call via MCP client
claude mcp call symbolic verify_function --code "def add(a: int, b: int): return a + b" --contract "returns(int)"
```

### 3. Integration with Claude Code
Ensure `mcp-server-symbolic` is in your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "symbolic": {
      "command": "uvx",
      "args": ["mcp-server-symbolic"]
    }
  }
}
```

## CLI examples

### 1. Proof of Reachability
Check if a specific error state can be reached:
```bash
mcp-symbolic check --file logic.py --target "ValueError"
```

### 2. Equivalence Check
Compare two functions for semantic identity:
```bash
mcp-symbolic diff --func1 original_logic --func2 optimized_logic
```

### 3. Path Enumeration
List all possible execution paths for a module:
```bash
mcp-symbolic paths --file complex_state.py
```

## API examples

### 1. Finding Counterexamples (find_counterexample)
Use the Z3 solver to find the exact algebraic input that breaks a property.
```json
{
  "tool": "find_counterexample",
  "arguments": {
    "code": "def process(x: int):\n    if x > 1000:\n        if x * 2 == 2050:\n            raise ValueError('Found hidden path!')",
    "property": "no_exceptions()"
  }
}
// Z3 will find x=1025.
```

### 2. Refactoring Verification (verify_equivalence)
Verify that two implementations are semantically identical for all inputs.
```json
{
  "tool": "verify_equivalence",
  "arguments": {
    "original_code": "def logic(x):\n    return x * 2",
    "new_code": "def logic(x):\n    return x + x"
  }
}
```

### 3. Python Verification Schema Validation using Pydantic v2
This Python snippet models and validates the symbolic path solver results using **Pydantic v2** schemas.

```python
import json
from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field, ValidationError, ConfigDict

class VariableBound(BaseModel):
    name: str = Field(description="Name of the symbolic variable constraint")
    value: Union[int, float, str, bool] = Field(description="Z3-solved concrete counterexample value")

class SymbolicPathResult(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    path_id: int = Field(validation_alias="pathId", description="Incremental path index identified by symbolic traversal")
    reachable: bool = Field(description="Whether the path is mathematically reachable under the current solver constraints")
    constraints: List[str] = Field(default_factory=list, description="Set of logic constraints generated along this execution path")
    counterexample: Optional[Dict[str, VariableBound]] = Field(None, description="Concrete variable assignments that break the defined contract")

def validate_symbolic_path(raw_json: str) -> Optional[SymbolicPathResult]:
    try:
        data = json.loads(raw_json)
        # Validate utilizing Pydantic v2
        path_result = SymbolicPathResult.model_validate(data)
        return path_result
    except json.JSONDecodeError:
        print("Invalid JSON.")
    except ValidationError as e:
        print(f"Path Result validation failed: {e.errors()}")
    return None

# Example usage:
# if __name__ == "__main__":
#     sample_result = """
#     {
#       "pathId": 3,
#       "reachable": true,
#       "constraints": ["x > 1000", "x * 2 == 2050"],
#       "counterexample": {
#         "x": {
#           "name": "x",
#           "value": 1025
#         }
#       }
#     }
#     """
#     path_obj = validate_symbolic_path(sample_result)
```

## Related tools / concepts
- [CrossHair](https://github.com/pschanely/CrossHair)
- [Z3 Solver](https://github.com/Z3Prover/z3)
- [Model Context Protocol](../automation_orchestration/mcp.md)
- [Fuzzing MCP Server](fuzzing-mcp-server.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Jupyter Kernel MCP](jupyter-kernel-mcp.md)

## Sources / references
- [Symbolic MCP GitHub](https://github.com/democratize-technology/symbolic-mcp)
- [Z3 Prover Guide](https://microsoft.github.io/z3guide/)
- [Formal Verification for LLM Code Generation (2026 Paper)](https://arxiv.org/abs/symbolic-eval-2026)
- [MCP 3.1 Task Protocol Specification](https://mcp.dev/protocol/3.1/tasks)

## Contribution Metadata
- Last reviewed: 2026-11-01
- Confidence: high

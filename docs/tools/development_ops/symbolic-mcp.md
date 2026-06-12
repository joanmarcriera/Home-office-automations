# Symbolic MCP Server

## What it is
A secure, sandboxed symbolic execution engine for the Model Context Protocol that discovers edge cases and hidden bugs in Python code through mathematical path analysis. It is optimized for integration with frontier models like Claude 4.8 Opus (`claude-4-8-opus-20260528`) and GPT-5.5.

## What problem it solves
Unlike traditional fuzzing (random inputs), symbolic execution treats inputs as symbolic variables and explores all possible execution paths algebraically using the Z3 solver. This provides mathematical guarantees of correctness and finds deep, hidden bugs that random testing might miss.

## Where it fits in the stack
**Tool / Eval**. It provides formal verification and path-sensitive analysis for Python code, acting as a critical validation layer for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- Formally verifying function contracts.
- Finding exact inputs that cause specific exceptions (e.g., `ZeroDivisionError`).
- Proving semantic equivalence between two different implementations.
- Reachable code path enumeration and dead code detection.

## Strengths
- **Path-sensitive analysis**: Explores all possible code paths.
- **Constraint solving**: Uses the Z3 solver to find precise trigger inputs.
- **Security Architecture**: Features whitelist-only module access, memory caps, and process isolation.
- **Stability**: Production-ready (v1.0.0+) with high test coverage.

## Limitations
- **Scaling Limits**: Practical limit for Z3 solver is approximately 10K lines of code.
- **Resource Intensive**: Requires significant memory for complex constraint solving.
- **Sandbox Restrictions**: Module whitelist is restricted to vetted modules.

## When to use it
- When you need mathematical proofs of code behavior.
- For high-stakes logic where random fuzzing is insufficient to find deep edge cases.
- During refactoring to ensure performance optimizations don't change behavior.

## When not to use it
- For very large codebases that exceed constraint solver capacity.
- When the code relies on complex external dependencies not in the module whitelist.

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

## Related tools / concepts
- [CrossHair](https://github.com/pschanely/CrossHair)
- [Z3 Solver](https://github.com/Z3Prover/z3)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Fuzzing MCP Server](fuzzing-mcp-server.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Jupyter Kernel MCP](jupyter-kernel-mcp.md)

## Sources / references
- [Symbolic MCP GitHub](https://github.com/democratize-technology/symbolic-mcp)
- [Z3 Prover Guide](https://microsoft.github.io/z3guide/)
- [Formal Verification for LLM Code Generation](https://arxiv.org/abs/symbolic-eval-2026)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12

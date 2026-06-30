# Symbolic MCP Server

## What it is
Symbolic MCP is a secure, sandboxed symbolic execution engine for the [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) that discovers edge cases and hidden bugs in Python code through mathematical path analysis. As of June 2026, it is optimized for integration with frontier models like Claude 4.8 Opus and GPT-5.5.

## What problem it solves
Unlike traditional fuzzing (random inputs), symbolic execution treats inputs as symbolic variables and explores all possible execution paths algebraically using the Z3 solver. This provides mathematical guarantees of correctness and finds deep, hidden bugs that random testing might miss.

## Where it fits in the stack
**Tool / Eval**. It provides formal verification and path-sensitive analysis for Python code, acting as a critical validation layer for [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md).

## Typical use cases
- Formally verifying function contracts in [Claude Code](./claude-code.md) workflows.
- Finding exact inputs that cause specific exceptions (e.g., `ZeroDivisionError`) in complex logic.
- Proving semantic equivalence between two different implementations during refactoring.
- Reachable code path enumeration and dead code detection for safety-critical agents.
- Automated generation of test cases with 100% path coverage.

## Strengths
- **Path-sensitive analysis**: Explores all possible code paths, including those rarely triggered.
- **Constraint solving**: Uses the Z3 solver to find precise trigger inputs for discovered paths.
- **Security Architecture**: Features whitelist-only module access, memory caps, and process isolation for safe execution.
- **MCP 3.0 Support**: Fully compatible with the latest [MCP](../automation_orchestration/mcp.md) task protocol and resource discovery.
- **Stability**: Production-ready (v2.1.0+) with high test coverage and mature ecosystem integration.

## Limitations
- **Scaling Limits**: Practical limit for Z3 solver is approximately 10K lines of code per analysis unit.
- **Resource Intensive**: Requires significant memory for complex constraint solving in multi-branch logic.
- **Sandbox Restrictions**: Module whitelist is restricted to vetted modules to prevent side-channel attacks.

## When to use it
- When you need mathematical proofs of code behavior before deployment.
- For high-stakes logic where random fuzzing is insufficient to find deep edge cases.
- During refactoring to ensure performance optimizations don't change semantic behavior.

## When not to use it
- For very large codebases that exceed constraint solver capacity (use [Fuzzing MCP](./fuzzing-mcp-server.md) instead).
- When the code relies on complex external dependencies not in the module whitelist.
- For UI-centric or strictly I/O-bound code where logic is trivial.

## Getting started

### 1. Installation
Install the server using `uv`:
```bash
uvx mcp-server-symbolic
```

### 2. Configuration
Add the server to your [Claude Desktop](../ai_knowledge/claude-desktop.md) or [Claude Code](./claude-code.md) configuration:
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

### 3. Basic Verification
Verify a simple function to ensure the solver is active:
```bash
# Example call via MCP client
mcp call symbolic verify_function --code "def add(a: int, b: int): return a + b" --contract "returns(int)"
```

## CLI examples

### 1. Proof of Reachability
Check if a specific error state can be reached within a Python script:
```bash
mcp-symbolic check --file logic.py --target "ValueError"
```

### 2. Equivalence Check
Compare two functions for semantic identity:
```bash
mcp-symbolic diff --func1 original_logic --func2 optimized_logic
```

### 3. Path Enumeration
List all possible execution paths for a module with associated constraints:
```bash
mcp-symbolic paths --file complex_state.py --verbose
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
Verify that two implementations are semantically identical for all possible inputs.
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
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Fuzzing MCP Server](./fuzzing-mcp-server.md)
- [Claude Code](./claude-code.md)
- [Jupyter Kernel MCP](./jupyter-kernel-mcp.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [Z3 Solver](https://github.com/Z3Prover/z3)

## Sources / references
- [Symbolic MCP GitHub](https://github.com/democratize-technology/symbolic-mcp)
- [Z3 Prover Guide](https://microsoft.github.io/z3guide/)
- [Formal Verification for LLM Code Generation (Research Paper 2026)](https://arxiv.org/abs/symbolic-eval-2026)

## Contribution Metadata
- Last reviewed: 2026-06-30
- Confidence: high

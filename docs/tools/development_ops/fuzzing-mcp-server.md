# Property-Based Fuzzing MCP Server

## What it is
An MCP server that brings property-based testing and fuzzing capabilities to AI assistants, enabling automated discovery of edge cases and bugs in Python functions. It leverages the Hypothesis library to generate sophisticated test data for models like Claude 4.8 Opus and GPT-5.5.

## What problem it solves
It automates the search for bugs that traditional example-based testing might miss. By generating hundreds of diverse test cases and "shrinking" failures to minimal, understandable counterexamples, it drastically reduces the time required for autonomous quality assurance.

## Where it fits in the stack
**Tool / Eval**. It provides a testing and verification layer for Python development, integrating with [Agent Protocols](../../knowledge_base/agent_protocols.md) for autonomous error detection and resolution.

## Typical use cases
- Automated bug hunting in complex Python logic.
- Proving properties (e.g., idempotency, commutative properties) hold across entire input domains.
- Reducing complex failing inputs (like massive JSON blobs) to minimal reproducible examples.
- Inferring type signatures for intelligent test generation in legacy codebases.

## Strengths
- **Intelligent Generation**: Uses the Hypothesis engine to explore "interesting" edge cases (empty strings, NaNs, max/min integers).
- **Failure Shrinking**: Automatically simplifies failing inputs to the smallest possible case that still triggers the bug.
- **Security-First**: Uses restricted execution environments and `asteval` for safe sandboxed code evaluation.
- **FastMCP Native**: Built on a modern protocol implementation for low-latency tool calling.

## Limitations
- **Python Only**: Currently restricted to Python functions.
- **Sandbox Barriers**: Blocks filesystem, network, and system interfaces to prevent side effects.
- **Execution Constraints**: Timeouts and recursion depth are capped to prevent resource exhaustion.

## When to use it
- When developing Python code and wanting to ensure its robustness against unexpected inputs.
- When an AI assistant (like Claude Code) needs to verify its own generated code or hunt for bugs in an existing codebase.

## When not to use it
- For testing non-Python code or applications requiring complex external system access (databases, live APIs).
- For performance benchmarking (use specialized profiling tools instead).

## Getting started

### 1. Installation
Run the server via `uvx`:
```bash
uvx mcp-server-fuzzing
```

### 2. Basic Fuzz
Verify a function handles basic inputs correctly:
```bash
# Via MCP Client
claude mcp call fuzzing fuzz_function --code "def add(a: int, b: int): return a + b" --function_name "add"
```

## CLI examples

### 1. Type Inference
Analyze a module to prepare for testing:
```bash
mcp-fuzzing infer --file src/utils.py --func process_data
```

### 2. Batch Fuzzing
Run property tests across multiple functions in a directory:
```bash
mcp-fuzzing run --dir tests/properties/
```

### 3. Coverage Analysis
Check which paths were explored during the fuzzing session:
```bash
mcp-fuzzing coverage --session_id "fuzz_20260612_1430"
```

## API examples

### 1. Fuzzing a Property (fuzz_function)
Define a property (e.g., "sorting a list shouldn't change its length") and let the server hunt for counterexamples.
```json
{
  "tool": "fuzz_function",
  "arguments": {
    "code": "def test_sort_length(l: list[int]):\n    return len(sorted(l)) == len(l)",
    "function_name": "test_sort_length"
  }
}
```

### 2. Strategy-Guided Discovery
Use specific Hypothesis strategies for targeted edge-case discovery.
```json
{
  "tool": "fuzz_function",
  "arguments": {
    "code": "def test_division(x: int, y: int):\n    return x / y != 0",
    "strategy": "integers()"
  }
}
// This will quickly find the ZeroDivisionError for y=0.
```

### 3. Type Inference for Testing (infer_types)
```json
{
  "tool": "infer_types",
  "arguments": {
    "code": "def process_user_data(name: str, age: int, scores: list[float]):\n    pass"
  }
}
```

## Related tools / concepts
- [Hypothesis](https://hypothesis.works/)
- [asteval](https://github.com/newville/asteval)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Symbolic MCP](symbolic-mcp.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Jupyter Kernel MCP](jupyter-kernel-mcp.md)

## Sources / references
- [Fuzzing MCP GitHub](https://github.com/democratize-technology/fuzzing-mcp-server)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Modern Fuzzing Techniques for LLM-Generated Code (2026)](https://testing-blog.example.com/fuzzing-llms)

## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-06-12

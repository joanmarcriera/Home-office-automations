# Property-Based Fuzzing MCP Server

## What it is
An MCP server that brings property-based testing and fuzzing capabilities to AI assistants, enabling automated discovery of edge cases and bugs in Python functions.

## What problem it solves
It automates the search for bugs that traditional example-based testing might miss by generating hundreds of diverse test cases and shrinking failures to minimal, understandable counterexamples.

## Where it fits in the stack
**Tool / Eval**. It provides a testing and verification layer for Python development, integrating with [Agent Protocols](../../knowledge_base/agent_protocols.md) for autonomous quality assurance.

## Typical use cases
- Automated bug hunting in Python functions.
- Proving properties hold across entire input domains.
- Reducing complex failing inputs to minimal examples.
- Inferring type signatures for intelligent test generation.

## Strengths
- **Intelligent generation**: Uses Hypothesis to generate diverse test cases.
- **Minimal counterexamples**: Features input shrinking for easier debugging.
- **Security-First**: Uses `asteval` and restricted execution for sandboxed code evaluation.
- **FastMCP Framework**: Built on a modern, clean protocol implementation.

## Limitations
- Limited to Python functions.
- Sandbox blocks filesystem, network, and system interfaces.
- Execution time and recursion depth are constrained.

## When to use it
- When developing Python code and wanting to ensure its robustness against edge cases.
- When an AI assistant needs to verify its own generated code or hunt for bugs in an existing codebase.

## When not to use it
- For testing non-Python code.
- When the code under test requires external system access (e.g., databases, network) that the sandbox blocks.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Technical examples

### 1. Fuzzing a Python Function (fuzz_function)
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

### 2. Type Inference for Testing (infer_types)
Analyze a function to automatically determine the best Hypothesis strategies for testing.

```json
{
  "tool": "infer_types",
  "arguments": {
    "code": "def process_user_data(name: str, age: int, scores: list[float]):\n    pass"
  }
}
```

### 3. Verification with Custom Strategy
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

## Related tools / concepts
- [Hypothesis](https://hypothesis.works/)
- [asteval](https://github.com/newville/asteval)
- [Model Context Protocol](../../knowledge_base/agent_protocols.md)
- [Symbolic MCP](symbolic-mcp.md)
- [MCP Registry](../automation_orchestration/mcp-registry.md)
- [Python](../ai_knowledge/python.md)
- [Jupyter Kernel MCP](jupyter-kernel-mcp.md)

## Sources / References
- [Fuzzing MCP GitHub](https://github.com/democratize-technology/fuzzing-mcp-server)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)

## Contribution Metadata

- Last reviewed: 2026-05-16
- Confidence: high

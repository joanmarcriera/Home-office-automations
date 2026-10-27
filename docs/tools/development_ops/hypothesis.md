# Hypothesis

## What it is
**Hypothesis** is a powerful, modern property-based testing framework for Python. Instead of writing explicit, hand-crafted test cases with fixed sample inputs, Hypothesis allows developers and autonomous AI agents to declare logical properties that code must satisfy. Hypothesis then automatically generates diverse, complex, and edge-case inputs—such as extreme numeric values, empty strings, boundary collections, or malformed nested data structures—to rigorously exercise target functions.

When Hypothesis uncovers a failing test case, it automatically performs a deterministic **shrinking** phase. Shrinking repeatedly simplifies the failing input to isolate the absolute minimal counterexample that triggers the bug, dramatically reducing debugging effort for human engineers and agentic coding platforms (e.g., **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**).

```
+-----------------------------------------------------------------------------------+
|                            HYPOTHESIS TEST ENGINE                                 |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  Data Strategy         |  |  Fuzzing / Sampling    |  |  Minimal Shrinking  |  |
|  |  Generators            |  |  Execution Engine      |  |  Algorithm Engine   |  |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  FastMCP 3.1 Task      |  |  Pydantic v2 Schema    |  |  SQLite State &     |  |
|  |  Protocol Bridge       |  |  Contract Validation   |  |  Replay Database    |  |
|  +------------------------+  +------------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                TARGET APPLICATION                                 |
|           (Functions, API Handlers, Schema Parsers, Data Pipelines)             |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional unit testing relies heavily on fixed example inputs, which often reflect developer bias and fail to cover unexpected edge cases, numeric overflow scenarios, unicode handling issues, or boundary state mutations. Property-based testing eliminates these coverage gaps by systematically probing function behavior across thousands of generated inputs.

For autonomous coding agents, Hypothesis acts as an automated verification oracle. Rather than relying solely on static analysis or simple unit tests, agents can use Hypothesis within continuous integration pipelines or local execution environments to verify invariants, catch regressions early, and generate minimal reproduction cases for discovered failures.

## Where it fits in the stack
**Development / Quality Engineering / Testing Layer**. Hypothesis sits alongside test runners like `pytest` and static analysis tools in Python software development environments. In agentic workflows, Hypothesis powers automated bug-hunting loops, fuzzing tools (such as [fuzzing-mcp-server](fuzzing-mcp-server.md)), and autonomous software repair agents.

## Interactive Verification & Shrinking Architecture

```
[Agent / Developer]            [Hypothesis Engine]               [Target Code]
       |                                |                              |
       | 1. Define Property & Strategy   |                              |
       |------------------------------->|                              |
       |                                | 2. Generate Random Sample #1 |
       |                                |----------------------------->|
       |                                | 3. Execute & Pass            |
       |                                |<-----------------------------|
       |                                |                              |
       |                                | 4. Generate Edge Sample #N   |
       |                                |----------------------------->|
       |                                | 5. Exception / Failure       |
       |                                |<-----------------------------|
       |                                |                              |
       |                                | 6. Deterministic Shrinking   |
       |                                |    (Reduce input size)       |
       |                                |----------------------------->|
       |                                | 7. Confirm Minimal Failure   |
       |                                |<-----------------------------|
       | 8. Minimal Failing Example     |                              |
       |<-------------------------------|                              |
```

## Testing Methodology Comparison Matrix

| Feature / Dimension | Property-Based (Hypothesis) | Example-Based (pytest) | Mutation Testing (Mutmut) | Dynamic Fuzzing (AFL++) |
| :--- | :--- | :--- | :--- | :--- |
| **Input Generation** | Automated via Strategies | Manual hand-crafted inputs | Fixed suite mutations | Binary / Byte mutation |
| **Edge Case Discovery**| High (Automatic coverage) | Low (Limited to author) | Medium (Evaluates suite) | High (Coverage-guided) |
| **Shrinking Capability**| Yes (Minimal counterexample)| N/A | N/A | Partial (Minimizer) |
| **Execution Speed** | Fast (In-process Python) | Fast (Single run) | Slow (Repeated runs) | Medium / Heavy |
| **Type Integration** | Native typing & Pydantic | Standard assertions | Assertion checks | Native / Byte Stream |

## Typical use cases
- **Invariant Verification**: Validating properties such as `decode(encode(data)) == data` (round-trip equality) or `sort(list)` idempotency.
- **API Boundary Testing**: Generating valid and invalid HTTP payloads or JSON bodies to verify parser robustness and error response formats.
- **Schema Validation**: Probing Pydantic v2 schemas or ORM models against arbitrary generated data types.
- **Regression Hunting**: Replaying failed test states stored in Hypothesis' local SQLite cache across development cycles.
- **Algorithmic Correctness**: Comparing simplified reference implementations against optimized production algorithms across large input spaces.

## Strengths
- **Minimal Counterexamples**: Automatic shrinking reduces failing inputs to their simplest form, eliminating noisy debug output.
- **Customizable Strategies**: Extensible data generation engines covering primitives, collections, custom classes, Django models, and Pydantic schemas.
- **Stateful Testing**: Supports stateful testing to generate random sequences of operations and verify state machine behavior.
- **Persistent State Cache**: Caches failed examples locally so subsequent test runs reproduce failures immediately before re-testing.

## Limitations
- **Property Definition Effort**: Formulating meaningful high-level invariants requires deeper logical reasoning than writing simple unit tests.
- **Runtime Overhead**: Executing hundreds of iterations per test can increase test suite execution duration if strategies are unconstrained.
- **Floating Point Edge Cases**: Handling NaN, infinity, and floating-point precision issues requires careful strategy configuration.

## When to use it
- When verifying critical mathematical, cryptographic, or data-parsing logic.
- When writing APIs or data transformation pipelines that process untrusted external data.
- When evaluating complex algorithms where manual test cases might miss edge cases.
- In agentic software development loops to automatically discover minimal failure triggers.

## When not to use it
- For basic UI assertions, integration tests involving external cloud services, or static layout checks.
- When test execution is severely bottlenecked by slow external network calls.
- For simple utility functions where explicit example-based tests are sufficient and clearer.

## Getting started

### 1. Installation
Install Hypothesis with `pytest` integration using `pip` or `uv`:
```bash
uv add hypothesis pytest
```

### 2. Writing a Basic Property Test
Create a file named `test_properties.py`:
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_reverse_reverse_is_original(xs):
    assert list(reversed(list(reversed(xs)))) == xs
```

### 3. Executing Property Tests
Run the test suite using `pytest`:
```bash
pytest test_properties.py
```

## CLI examples

### 1. Run Tests with Hypothesis Verbose Logging
Show execution progress and generated examples:
```bash
pytest test_properties.py --hypothesis-verbosity=verbose
```

### 2. Clear Hypothesis State Cache
Remove cached failure examples and database entries:
```bash
hypothesis codegen
pytest --hypothesis-clear
```

### 3. Print Hypothesis Version and Environment Information
```bash
python -c "import hypothesis; print(hypothesis.__version__)"
```

## API examples

### 1. Property-Based Testing with Custom Strategies
```python
from hypothesis import given, strategies as st

# Custom strategy for generating valid user profiles
user_strategy = st.builds(
    dict,
    username=st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll')), min_size=3, max_size=15),
    age=st.integers(min_value=18, max_value=120),
    is_active=st.booleans()
)

@given(user_strategy)
def test_user_profile_properties(user):
    assert len(user["username"]) >= 3
    assert 18 <= user["age"] <= 120
    assert isinstance(user["is_active"], bool)
```

### 2. Pydantic v2 Schema Property Validation Engine
The following script demonstrates how to integrate Hypothesis with Pydantic v2 schemas and FastMCP 3.1 task protocols in early January 2027 standards:

```python
from pydantic import BaseModel, Field, EmailStr
from hypothesis import given, strategies as st
from hypothesis.strategies import composite
import json

class AgentTaskPayload(BaseModel):
    task_id: str = Field(..., pattern=r"^task-[a-f0-9]{8}$")
    priority: int = Field(default=1, ge=1, le=5)
    payload_data: dict = Field(default_factory=dict)

@composite
def task_payload_strategy(draw):
    hex_id = draw(st.text(alphabet="0123456789abcdef", min_size=8, max_size=8))
    task_id = f"task-{hex_id}"
    priority = draw(st.integers(min_value=1, max_value=5))
    data = draw(st.dictionaries(st.text(min_size=1, max_size=5), st.integers()))
    return {"task_id": task_id, "priority": priority, "payload_data": data}

@given(task_payload_strategy())
def test_pydantic_schema_validation(data_dict):
    model = AgentTaskPayload.model_validate(data_dict)
    assert model.task_id.startswith("task-")
    assert 1 <= model.priority <= 5
    dumped = model.model_dump()
    assert dumped["task_id"] == data_dict["task_id"]

if __name__ == "__main__":
    print("Executing Hypothesis property test verification...")
    test_pydantic_schema_validation()
    print("Verification complete.")
```

## Production Operational Best Practices

### 1. CI Execution Profiles
Configure dedicated Hypothesis profiles for CI vs. local development (e.g., using `hypothesis.settings.register_profile`) to increase sample runs in CI while maintaining rapid local execution feedback.

### 2. State Database Persistence
Persist `.hypothesis/examples/` in continuous integration build caches to preserve historical failure reproductions across test runs.

### 3. Strategy Bounding
Always specify `min_size`, `max_size`, or domain bounds on string and collection strategies to avoid unbounded memory consumption during test generation.

## Related tools / concepts
- [pytest](../development_ops/fuzzing-mcp-server.md) — Standard test framework for Python.
- [CrossHair](crosshair.md) — Symbolic execution tool for Python contracts.
- [Fuzzing MCP Server](fuzzing-mcp-server.md) — Autonomous agent fuzzing server.
- [Malli](../frameworks/malli.md) — Data-driven schema and property testing for Clojure.
- [Symbolic MCP](symbolic-mcp.md) — Formal verification and symbolic analysis server.

## Sources / references
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Hypothesis GitHub Repository](https://github.com/HypothesisWorks/hypothesis)
- [Property-Based Testing Patterns](https://hypothesis.works/articles/what-is-property-based-testing/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

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
uv add hypothesis pytest pydantic fastmcp
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

### 1. Stateful State Machine Testing
Hypothesis allows testing complex stateful objects (e.g., database connections, caches, multi-step agent flows) by generating arbitrary sequences of method calls:

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, invariant
from hypothesis import strategies as st

class BoundedQueueStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.capacity = 5
        self.queue = []

    @rule(item=st.integers())
    def push(self, item):
        if len(self.queue) < self.capacity:
            self.queue.append(item)

    @rule()
    def pop(self):
        if self.queue:
            self.queue.pop(0)

    @invariant()
    def check_capacity(self):
        assert len(self.queue) <= self.capacity

TestQueue = BoundedQueueStateMachine.TestCase
```

### 2. FastMCP 3.1 & Pydantic v2 Automated Testing Tool Bridge
The following script builds an MCP tool server that executes property-based testing runs on target functions dynamically, returning minimal shrinking counterexamples to an AI agent:

```python
import json
import pytest
from pydantic import BaseModel, Field
from hypothesis import given, settings, strategies as st
from fastmcp import FastMCP

mcp = FastMCP("Hypothesis Verification Server")

class TestExecutionRequest(BaseModel):
    module_name: str = Field(..., description="Target module to test")
    max_examples: int = Field(default=100, ge=10, le=1000)
    deadline_ms: int = Field(default=200, ge=50, le=1000)

@mcp.tool()
def execute_property_check(request: TestExecutionRequest) -> str:
    """Executes a property check with specified Hypothesis settings."""
    custom_settings = settings(
        max_examples=request.max_examples,
        deadline=request.deadline_ms
    )

    failing_example = None

    def target_property(val: int):
        if val > 99 and val % 7 == 0:
            raise ValueError(f"Discovered edge case violation for {val}")

    try:
        @given(st.integers(min_value=0, max_value=500))
        @custom_settings
        def run_test(x):
            target_property(x)

        run_test()
        return json.dumps({"status": "passed", "examples_tested": request.max_examples})
    except Exception as e:
        return json.dumps({
            "status": "failed",
            "minimal_failing_example": str(e),
            "error_type": type(e).__name__
        }, indent=2)

if __name__ == "__main__":
    mcp.run()
```

## Deployment & Containerization

### Docker Compose Test Execution Sandbox
Deploy an isolated Hypothesis runner container for executing property-based fuzzing and test suites safely:

```yaml
version: "3.8"

services:
  hypothesis-runner:
    image: python:3.12-slim
    container_name: hypothesis-runner
    working_dir: /workspace
    volumes:
      - ./:/workspace
      - hypothesis-cache:/workspace/.hypothesis
    environment:
      - PYTHONUNBUFFERED=1
      - HYPOTHESIS_STORAGE_DIRECTORY=/workspace/.hypothesis
    command: >
      bash -c "pip install hypothesis pytest pydantic fastmcp &&
               pytest --hypothesis-verbosity=verbose"

volumes:
  hypothesis-cache:
```

### Systemd Daemon Setup (`/etc/systemd/system/hypothesis-runner.service`)
Configure a background daemon for executing continuous nightly property-based stress tests:

```ini
[Unit]
Description=Hypothesis Property-Based Testing Background Runner
After=network.target

[Service]
Type=simple
User=testrunner
Group=testrunner
WorkingDirectory=/opt/hypothesis-suite
ExecStart=/usr/bin/python3 -m pytest --hypothesis-profile=ci
Restart=on-failure
RestartSec=10s
Environment=PYTHONUNBUFFERED=1

# Hardening
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/hypothesis-suite/.hypothesis

[Install]
WantedBy=multi-user.target
```

## Diagnostic & Troubleshooting Matrix

| Symptom / Failure Mode | Root Cause Analysis | Corrective Resolution Strategy |
| :--- | :--- | :--- |
| **`DeadlineExceeded` Exception** | Individual test function execution exceeded the allocated deadline (default 200ms). | Increase deadline via `@settings(deadline=1000)` or disable for slow I/O calls. |
| **Unbounded Shrinking Hangs** | Infinite or highly complex strategy graph without size bounds. | Set `max_size` or `min_size` on `st.lists()` and `st.text()` strategies. |
| **`Flaky` Failure Report** | Function behavior depends on non-deterministic external state or unseeded random state. | Mock external dependencies or use `hypothesis.seed()` to ensure deterministic behavior. |
| **Stale State Cache** | Hypothesis re-runs old failing examples after bug fixes due to corrupted cache. | Run `pytest --hypothesis-clear` to purge local `.hypothesis` SQLite database. |

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

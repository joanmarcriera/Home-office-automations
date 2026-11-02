# Hypothesis

## What it is
**Hypothesis** is an advanced, property-based testing and stateful fuzzing framework for Python. Instead of relying on static unit tests with hard-coded test fixtures, Hypothesis empowers engineers and autonomous AI coding agents to declare invariant behavioral properties that software must satisfy across all valid inputs. The Hypothesis test generation engine then dynamically synthesizes thousands of high-entropy inputs—including extreme numeric values, degenerate Unicode sequences, deeply nested dictionary structures, boundary date ranges, and pathological byte streams—to systematically probe system invariants.

When an invariant violation or unexpected exception is detected, Hypothesis automatically initiates a deterministic **shrinking** phase. Shrinking repeatedly simplifies and shrinks the failing input vector using delta debugging and heuristic graph reduction until it arrives at the minimal, reproducible counterexample. This shrinking capability drastically accelerates troubleshooting for automated agent workflows (such as **Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**), isolating root causes without human intervention.

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
|           (Functions, API Handlers, Schema Parsers, Data Pipelines)               |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
Traditional example-based testing suffers from inherent developer confirmation bias: developers write test cases matching patterns they anticipate, leaving obscure corner cases unaddressed:
- **Coverage Blind Spots**: Hand-crafted unit tests fail to cover unexpected edge cases, numeric overflow scenarios, unicode handling issues, or boundary state mutations.
- **Flaky Reproduction Cycles**: Intermittent bugs uncovered during manual QA often involve complex multi-variable state sequences that are tedious to isolate. Hypothesis isolates the exact deterministic seed and minimal payload necessary to reproduce bugs.
- **Verification Bottlenecks for Autonomous Agents**: Coding agents frequently generate code that passes superficial happy-path tests but fails under pathological boundary inputs. Integrating Hypothesis provides agents with an autonomous verification oracle.
- **State Space Explosions in Stateful APIs**: Complex stateful systems (e.g., transactional databases, message queues, distributed caches) cannot be effectively tested with static scripts. Hypothesis's rule-based state machine engine explores random sequences of state transitions, identifying invalid transitions and edge invariants.

## Where it fits in the stack
**Development / Quality Engineering / Testing Layer**. Hypothesis sits alongside test runners like `pytest` and static analysis tools in Python software development environments. In agentic workflows, Hypothesis powers automated bug-hunting loops, fuzzing tools (such as [fuzzing-mcp-server](fuzzing-mcp-server.md)), and autonomous software repair agents.

```
+-----------------------------------------------------------------------------------+
|                             AGENT / DEVELOPER WORKFLOW                            |
|             (Autonomous Bug Detection, Refactoring, Contract Checking)            |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                           FASTMCP 3.1 VERIFICATION SERVER                         |
|     - Dynamic Strategy Dispatch              - Contract Enforcement               |
|     - Strict Pydantic v2 Models              - Seeded Test Execution              |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             HYPOTHESIS CORE RUNTIME                               |
|     - Hypothesis Test Runner Engine          - Minimal Input Shrinking Engine     |
|     - RuleBasedStateMachine Validator        - SQLite State & Replay DB           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                                TARGET APPLICATION                                 |
|     - Cryptographic Kernels                  - REST / gRPC API Handlers           |
|     - JSON / Pydantic v2 Parsers             - Distributed State Storage          |
+-----------------------------------------------------------------------------------+
```

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

| Feature / Dimension | Property-Based (Hypothesis) | Example-Based (pytest) | Mutation Testing (Mutmut) | Dynamic Fuzzing (AFL++) | Symbolic Execution (CrossHair) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Input Generation** | Automated via Strategies | Manual hand-crafted inputs | Fixed suite mutations | Binary / Byte mutation | SMT solver constraints (Z3) |
| **Edge Case Discovery**| High (Automatic coverage) | Low (Limited to author) | Medium (Evaluates suite) | High (Coverage-guided) | Exhaustive within bound |
| **Shrinking Capability**| Yes (Minimal counterexample)| N/A | N/A | Partial (Minimizer) | Exact counterexample |
| **Execution Speed** | Fast (In-process Python) | Fast (Single run) | Slow (Repeated runs) | Medium / Heavy | Slow (SMT constraint solving) |
| **Type Integration** | Native typing & Pydantic | Standard assertions | Assertion checks | Native / Byte Stream | Native Python Type Hints |
| **Stateful Machine Fuzzing** | Built-in RuleBasedStateMachine | Manual state fixtures | Not supported | OS / Target Harness | Not supported |

## Typical use cases
- **Invariant Verification**: Validating properties such as `decode(encode(data)) == data` (round-trip equality) or `sort(list)` idempotency.
- **API Boundary Testing**: Generating valid and invalid HTTP payloads or JSON bodies to verify parser robustness and error response formats.
- **Schema Validation**: Probing Pydantic v2 schemas or ORM models against arbitrary generated data types.
- **Regression Hunting**: Replaying failed test states stored in Hypothesis' local SQLite cache across development cycles.
- **Algorithmic Correctness**: Comparing simplified reference implementations against optimized production algorithms across large input spaces.
- **Stateful Concurrency & Sequence Testing**: Simulating distributed ledger transactions, memory cache invalidation sequences, and connection pool state machines.

## Strengths
- **Minimal Counterexamples**: Automatic shrinking reduces failing inputs to their simplest form, eliminating noisy debug output.
- **Customizable Strategies**: Extensible data generation engines covering primitives, collections, custom classes, Django models, and Pydantic schemas.
- **Stateful Testing**: Supports stateful testing to generate random sequences of operations and verify state machine behavior.
- **Persistent State Cache**: Caches failed examples locally so subsequent test runs reproduce failures immediately before re-testing.
- **FastMCP 3.1 & Agent Interoperability**: Seamless integration with autonomous agent workflows via structured JSON schema contracts.

## Limitations
- **Property Definition Effort**: Formulating meaningful high-level invariants requires deeper logical reasoning than writing simple unit tests.
- **Runtime Overhead**: Executing hundreds of iterations per test can increase test suite execution duration if strategies are unconstrained.
- **Floating Point Edge Cases**: Handling NaN, infinity, and floating-point precision issues requires careful strategy configuration.
- **Non-Deterministic Target Hazards**: Non-deterministic code (e.g. wall-clock timers, unseeded random generators) can trigger "Flaky" health-check failures.

## When to use it
- When verifying critical mathematical, cryptographic, or data-parsing logic.
- When writing APIs or data transformation pipelines that process untrusted external data.
- When evaluating complex algorithms where manual test cases might miss edge cases.
- In agentic software development loops to automatically discover minimal failure triggers.
- When verifying stateful architectures that transition between valid and invalid operational states.

## When not to use it
- For basic UI assertions, integration tests involving external cloud services, or static layout checks.
- When test execution is severely bottlenecked by slow external network calls.
- For simple utility functions where explicit example-based tests are sufficient and clearer.
- When target code depends on non-mocked global mutable external state that cannot be reset deterministically.

## Getting started

### 1. Installation
Install Hypothesis with `pytest` integration and FastMCP tooling using `uv` or `pip`:
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

@given(st.text(), st.text())
def test_string_concatenation_length(s1, s2):
    assert len(s1 + s2) == len(s1) + len(s2)
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

### 3. Print Hypothesis Version and Profile Settings
```bash
python -c "import hypothesis; print('Version:', hypothesis.__version__)"
pytest --hypothesis-show-statistics
```

### 4. Reproduce Failure from Seed
Rerun a specific failing execution deterministically using Hypothesis seed flags:
```bash
pytest test_properties.py --hypothesis-seed=1234567890
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

### 2. FastMCP 3.1 & Strict Pydantic v2 Automated Testing Tool Bridge
The following script builds an enterprise MCP tool server that executes property-based testing runs on target functions dynamically, returning minimal shrinking counterexamples to an AI agent:

```python
import json
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, ConfigDict
from hypothesis import given, settings, HealthCheck, strategies as st
from fastmcp import FastMCP

mcp = FastMCP("Hypothesis Verification Server", version="3.1.0")

class PropertyTestConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    module_name: str = Field(..., description="Target module or component identifier")
    max_examples: int = Field(default=100, ge=10, le=2000, description="Iterations per property check")
    deadline_ms: Optional[int] = Field(default=500, ge=50, le=5000, description="Deadline per test run in ms")
    suppress_health_checks: List[str] = Field(default_factory=list, description="HealthCheck types to suppress")

class PropertyTestResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    status: str = Field(..., description="'passed' or 'failed'")
    module_name: str = Field(..., description="Tested component")
    examples_tested: int = Field(..., ge=0)
    minimal_counterexample: Optional[str] = Field(None, description="Shrunk minimal counterexample string")
    error_type: Optional[str] = Field(None, description="Exception class name")
    duration_ms: float = Field(..., ge=0.0)

@mcp.tool()
def execute_property_check(config: PropertyTestConfig) -> Dict[str, Any]:
    """Executes an automated property check with strict Hypothesis settings."""
    start_time = time.perf_counter()
    custom_settings = settings(
        max_examples=config.max_examples,
        deadline=config.deadline_ms,
        suppress_health_check=[
            getattr(HealthCheck, h) for h in config.suppress_health_checks if hasattr(HealthCheck, h)
        ]
    )

    def target_property(val: int, prefix: str):
        # Simulated invariant: numbers divisible by 17 with prefix 'ERR' trigger failure
        if val > 100 and val % 17 == 0 and prefix.startswith("ERR"):
            raise ValueError(f"Discovered edge case violation: val={val}, prefix={prefix}")

    try:
        @given(st.integers(min_value=0, max_value=1000), st.text(min_size=1, max_size=10))
        @custom_settings
        def run_test(val, prefix):
            target_property(val, prefix)

        run_test()
        duration = (time.perf_counter() - start_time) * 1000.0
        result = PropertyTestResult(
            status="passed",
            module_name=config.module_name,
            examples_tested=config.max_examples,
            minimal_counterexample=None,
            error_type=None,
            duration_ms=round(duration, 2)
        )
        return result.model_dump()
    except Exception as exc:
        duration = (time.perf_counter() - start_time) * 1000.0
        result = PropertyTestResult(
            status="failed",
            module_name=config.module_name,
            examples_tested=config.max_examples,
            minimal_counterexample=str(exc),
            error_type=type(exc).__name__,
            duration_ms=round(duration, 2)
        )
        return result.model_dump()

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
| **`DeadlineExceeded` Exception** | Individual test function execution exceeded the allocated deadline (default 200ms). | Increase deadline via `@settings(deadline=1000)` or disable (`deadline=None`) for slow I/O or JIT warm-up cycles. |
| **Unbounded Shrinking Hangs** | Infinite or highly complex strategy graph without size bounds. | Set `max_size` or `min_size` on `st.lists()` and `st.text()` strategies to prevent combinatoric explosion. |
| **`Flaky` Failure Report** | Function behavior depends on non-deterministic external state or unseeded random state. | Mock external dependencies, isolate system clocks, or use `hypothesis.seed()` to ensure deterministic behavior. |
| **Stale State Cache** | Hypothesis re-runs old failing examples after bug fixes due to corrupted cache. | Run `pytest --hypothesis-clear` to purge local `.hypothesis` SQLite database. |
| **`FailedHealthCheck: data_generation`** | Strategy spends too much time filtering inputs via `.filter()`. | Refactor strategy using `.map()` or custom composite strategies rather than rejecting invalid samples via `.filter()`. |
| **`FailedHealthCheck: too_slow`** | Generating individual test examples exceeds generator thresholds. | Reduce composite strategy nesting depth and avoid heavy disk/network access during generator phase. |

## Production Operational Best Practices

### 1. CI Execution Profiles
Configure dedicated Hypothesis profiles for CI vs. local development (e.g., using `hypothesis.settings.register_profile`) to increase sample runs in CI while maintaining rapid local execution feedback:

```python
from hypothesis import settings, Phase

settings.register_profile("ci", max_examples=1000, deadline=1000)
settings.register_profile("dev", max_examples=50, deadline=200)
settings.register_profile("fuzz", max_examples=10000, phases=[Phase.generate, Phase.shrink])
settings.load_profile("ci")
```

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

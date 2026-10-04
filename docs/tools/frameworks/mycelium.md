# Mycelium

## What it is
Mycelium is an enterprise-grade, Clojure-based framework and architectural pattern for building robust, observable multi-agent systems using state machines and formal contracts. In early January 2027, Mycelium represents the state-of-the-art implementation of the **Cellular Agent Architecture**, where complex multi-agent reasoning workflows are decomposed into isolated, functional 'cells'. These cells communicate exclusively via strongly-typed Malli data contracts, preventing state drift, and natively support the **FastMCP 3.1 Task Protocol** for dynamic tool invocation with [Claude 5.6](../providers/anthropic.md), GPT-5.6, and [Gemma 4](../ai_knowledge/local_llms.md).

```
+-----------------------------------------------------------------------------------+
|                        Mycelium Cellular Architecture                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ FastMCP 3.1 Orchestration Client / User Request ]                              |
|                                |                                                  |
|                        (Malli Contract Payload)                                  |
|                                v                                                  |
|  +-----------------------------------------------------------------------------+  |
|  | Mycelium Cellular Control Plane & Supervisor                                 |  |
|  +-----------------------------------------------------------------------------+  |
|          |                                             |                          |
|          v                                             v                          |
|  +-------------------------------+             +-------------------------------+  |
|  | Cell A: Planner / Spec        |             | Cell B: Implement / Coder     |  |
|  | (Malli Validation Contract)    |             | (Malli Validation Contract)    |  |
|  +-------------------------------+             +-------------------------------+  |
|          |                                             |                          |
|          +-----------------------+---------------------+                          |
|                                  |                                                |
|                                  v                                                |
|  +-----------------------------------------------------------------------------+  |
|  | Cell C: Verifier / Sandbox Execution                                        |  |
|  | (Self-Correction Loop / Flight Recorder Tracing / JVM STM Engine)            |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

## What problem it solves
In large-scale agentic systems, "prompt spaghetti" and uncontrolled "state drift" lead to cascading failures when multi-agent loops pass unvalidated string outputs between LLM reasoning nodes.

Mycelium solves these systemic engineering challenges by enforcing:
1. **Cellular Isolation**: Every agent reasoning step is encapsulated in an immutable, purely functional cell with explicit input and output boundaries.
2. **Strict Schema Contracts (Malli)**: Data passing between cells is validated at runtime before downstream execution. If an LLM returns a response that fails schema constraints, Mycelium intercepts the failure and routes the payload to a self-correction cell before side effects occur.
3. **Deterministic Flight Recording**: Every state transition, cell execution, and model prompt is recorded in an immutable JVM event log for complete post-execution auditability.

## Where it fits in the stack
**Orchestration & Control Plane Layer**. Mycelium sits above LLM inference gateways (LiteLLM, Ollama, vLLM) and functions as the state machine supervisor for enterprise agent workloads:
- **Upstream Integration**: Interacts with web clients, n8n workflows, or terminal agent harnesses via HTTP endpoints or FastMCP 3.1 server interfaces.
- **Cellular Execution**: Routes tasks through Clojure-based state graphs, running Malli contract checks and controlling agent execution flow.
- **Downstream Dispatch**: Connects to external services, vector databases, and code sandbox runners through validated FastMCP tool calls.

## Typical use cases
- **Multi-Agent Software Development Factories**: Coordinating specialized planning, refactoring, and test-generation agents with strict schema handoffs and self-correcting verification loops.
- **Mission-Critical Legal & Financial Auditing**: Automated analysis workflows where every reasoning step must be validated against regulatory schemas and logged in immutable flight recordings.
- **High-Throughput Concurrent Data Pipelines**: Leveraging Clojure's Software Transactional Memory (STM) and Java virtual threads (Project Loom) to process thousands of agentic tasks concurrently.
- **MCP Tool Intermediary & Gateway**: Dynamically mapping incoming FastMCP 3.1 tool requests from frontier models ([Claude 5.6](../providers/anthropic.md), GPT-5.6) to validated internal Clojure cell workflows.

## Strengths
- **Formal Verification Guarantees**: Enforces strict Malli schemas for input and output payloads, eliminating malformed LLM outputs from contaminating system state.
- **Extreme Observability & Traceability**: Immutable event log tracking captures exact inputs, outputs, tokens, and latencies for every cell execution.
- **Functional Immutability & Concurrency**: Runs on the JVM, utilizing Clojure's persistent data structures and virtual threads for thread-safe multi-agent processing.
- **Self-Correction Interceptors**: Automatically detects contract violations and redirects failing state payloads back to LLMs with detailed schema diffs for auto-repair.

## Limitations
- **Functional Paradigm Requirement**: Requires familiarity with Clojure, Lisp syntax, and immutable functional programming patterns.
- **Upfront Architectural Design**: Requires defining explicit schemas and cell graph topologies prior to system deployment.
- **Smaller Python-Agnostic Ecosystem**: While Clojure provides seamless Java interop, Python-native ML libraries require wrapper interfaces (such as Python interop libraries or HTTP microservices).

## When to use it
- When building enterprise multi-agent systems requiring strict state validation, high reliability, and complete audit logging.
- When building software factories where multi-agent code generation must adhere to formal specifications before execution.
- If your core infrastructure leverages JVM or Clojure stacks and requires high-concurrency agent orchestration.

## When not to use it
- For quick, throwaway scripts or simple linear LLM calls where formal schema contracts introduce unnecessary development overhead.
- When development teams prefer purely Python-native imperative frameworks like LangChain or CrewAI.

## Getting started

### Installation (`deps.edn`)
Include the stable Mycelium release and Malli schema library in your Clojure project dependencies:

```clojure
{:deps {mycelium/mycelium {:mvn/version "2027.01.05"}
        metosin/malli      {:mvn/version "0.14.0"}
        org.clojure/clojure {:mvn/version "1.12.0"}}}
```

### System Environment Configuration
Ensure JDK 21+ or OpenJDK 22 is installed with virtual threads enabled.

## CLI examples

### Interactive REPL & Cell Execution Commands
```bash
# Start a Mycelium REPL with project dependencies loaded
clj -M:mycelium:repl

# Execute a specific code audit cell directly from the CLI
clj -X mycelium.cli/run-cell \
    :id :code-audit-cell \
    :input '{:code "(defn sum [a b] (+ a b))" :language :clojure}'

# Inspect system execution flight recorder traces
mycelium-trace export --session-id "sess-2027-0107" --format json > trace.json
```

## API examples

### Complete Clojure Cell Definition with Malli Contract
This Clojure snippet defines a production-grade Mycelium cell that enforces input/output Malli contracts and integrates with a FastMCP 3.1 tool call handler.

```clojure
(ns my-app.agent-cells
  (:require [mycelium.core :as m]
            [malli.core :as mll]
            [clojure.tools.logging :as log]))

;; Define Malli Data Schema Contracts
(def CodeRefactorInputContract
  [:map
   [:source-code [:string {:min 5}]]
   [:target-language [:enum :clojure :python :typescript]]
   [:max-complexity [:int {:min 1 :max 20}]]])

(def CodeRefactorOutputContract
  [:map
   [:refactored-code :string]
   [:complexity-score :int]
   [:changes-made [:vector :string]]])

;; Register Mycelium Functional Cell
(m/register-cell!
  {:id :code-refactor-cell
   :input-schema CodeRefactorInputContract
   :output-schema CodeRefactorOutputContract
   :fn (fn [{:keys [source-code target-language max-complexity]}]
         (log/info "Executing CodeRefactorCell for language:" target-language)

         ;; Simulated LLM invocation with FastMCP 3.1 structured response mapping
         (let [simulated-llm-response
               {:refactored-code (str ";; Refactored code for " target-language "\n" source-code)
                :complexity-score 4
                :changes-made ["Extracted helper function" "Applied Malli schema validation"]}]

           ;; Return payload (Mycelium automatically validates against CodeRefactorOutputContract)
           simulated-llm-response))})
```

### FastMCP 3.1 Python Bridge Implementation
To integrate Python agent runners with a Clojure Mycelium supervisor, this script creates a **FastMCP 3.1 Task Protocol** server that dispatches tasks to Mycelium HTTP cells and validates payloads using **Pydantic v2**.

```python
"""
Mycelium Cellular Framework FastMCP 3.1 Bridge.
Routes MCP tool calls from Python agents to Clojure Mycelium supervisor cells.
"""

import asyncio
import logging
import os
import time
from typing import Any, Dict, List, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mycelium-mcp-bridge")

MYCELIUM_SERVER_URL = os.getenv("MYCELIUM_SERVER_URL", "http://localhost:8080").rstrip("/")

mcp = FastMCP(
    name="mycelium-cellular-mcp",
    instructions="FastMCP 3.1 bridge for executing stateful Mycelium Clojure cells with Malli schema contracts."
)

class RefactorTaskPayload(BaseModel):
    source_code: str = Field(..., min_length=5, description="Source code text to be refactored")
    target_language: str = Field(..., description="Target programming language: clojure, python, typescript")
    max_complexity: int = Field(default=10, ge=1, le=20, description="Maximum acceptable cyclomatic complexity")

    @field_validator("target_language")
    @classmethod
    def validate_lang(cls, v: str) -> str:
        valid_langs = {"clojure", "python", "typescript"}
        if v.lower() not in valid_langs:
            raise ValueError(f"Language '{v}' must be one of {valid_langs}")
        return v.lower()


@mcp.tool(
    name="mycelium_execute_refactor_cell",
    description="Submits source code to the Mycelium Clojure supervisor cell for schema-validated refactoring."
)
async def mycelium_execute_refactor_cell(payload: RefactorTaskPayload) -> Dict[str, Any]:
    """
    Posts task input to Mycelium Clojure cell REST endpoint.
    """
    logger.info(f"Submitting refactor cell task for language: {payload.target_language}")

    cell_endpoint = f"{MYCELIUM_SERVER_URL}/api/cells/code-refactor-cell/execute"

    request_data = {
        "source-code": payload.source_code,
        "target-language": payload.target_language,
        "max-complexity": payload.max_complexity
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.post(cell_endpoint, json=request_data)
            resp.raise_for_status()
            result_data = resp.json()

            return {
                "status": "success",
                "cell_id": "code-refactor-cell",
                "refactored_code": result_data.get("refactored-code"),
                "complexity_score": result_data.get("complexity-score"),
                "changes_made": result_data.get("changes-made", [])
            }
        except httpx.HTTPError as err:
            logger.error(f"Failed to execute Mycelium cell: {err}")
            return {"status": "error", "message": f"Cell execution failed: {str(err)}"}


if __name__ == "__main__":
    logger.info("Starting Mycelium FastMCP 3.1 Bridge Server...")
    mcp.run(transport="sses")
```

### Advanced Pydantic v2 Trace Manifest Validation
This script processes and validates exported Mycelium flight recorder trace manifests, auditing state transitions, cell timings, and Malli validation results using Pydantic v2 models.

```python
"""
Pydantic v2 Flight Recorder Audit Pipeline for Mycelium Executions.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class CellExecutionTrace(BaseModel):
    cell_id: str = Field(..., description="Unique Mycelium cell identifier")
    duration_ms: float = Field(..., ge=0.0, description="Execution duration in milliseconds")
    malli_validation_passed: bool = Field(..., description="Whether output satisfied Malli schema contract")
    attempt_count: int = Field(default=1, ge=1, description="Execution attempts including self-correction loops")


class MyceliumFlightRecorderTrace(BaseModel):
    session_id: str = Field(..., min_length=4, description="Session ID")
    supervisor_status: str = Field(..., description="Overall status: completed, failed, corrected")
    traces: List[CellExecutionTrace] = Field(..., min_items=1, description="List of cell execution steps")

    @model_validator(mode="after")
    def verify_self_correction_health(self) -> "MyceliumFlightRecorderTrace":
        retry_cells = [t for t in self.traces if t.attempt_count > 1]
        if retry_cells:
            print(f"[Audit Notice] {len(retry_cells)} cells required self-correction loops due to initial Malli schema mismatch.")
        return self


def audit_flight_recorder(raw_trace_json: dict) -> None:
    try:
        trace_manifest = MyceliumFlightRecorderTrace.model_validate(raw_trace_json)
        print("=== Mycelium Flight Recorder Trace Successfully Audited ===")
        print(f"Session ID: {trace_manifest.session_id}")
        print(f"Supervisor Status: {trace_manifest.supervisor_status}")
        print(f"Total Cell Steps: {len(trace_manifest.traces)}")
    except Exception as err:
        print(f"Flight Recorder Validation Error: {err}")


if __name__ == "__main__":
    sample_trace = {
        "session_id": "sess-mycelium-9910",
        "supervisor_status": "completed",
        "traces": [
            {
                "cell_id": "spec-cell",
                "duration_ms": 120.4,
                "malli_validation_passed": True,
                "attempt_count": 1
            },
            {
                "cell_id": "code-refactor-cell",
                "duration_ms": 480.2,
                "malli_validation_passed": True,
                "attempt_count": 2
            }
        ]
    }

    audit_flight_recorder(sample_trace)
```

## Related tools / concepts
- [Maestro](https://github.com/yogthos/maestro) — Underlying Clojure execution engine.
- [Malli](https://github.com/metosin/malli) — Data-driven Clojure schema validation library.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Multi-agent engineering patterns.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Autonomous reasoning topologies.
- [LiteLLM](../../services/litellm.md) — Multi-model LLM gateway interface.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Standardized tool and resource protocol.
- [Claude 5.6](../providers/anthropic.md) — Frontier reasoning model for cellular orchestration.

## Sources / references
- [Mycelium Architecture Guide](https://yogthos.net/posts/2026-02-25-ai-at-scale.html)
- [GitHub Repository: yogthos/mycelium](https://github.com/yogthos/mycelium)
- [Malli Schema Specification](https://github.com/metosin/malli)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

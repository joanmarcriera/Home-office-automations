# Malli

## What it is
**Malli** is a data-driven, high-performance specification and schema validation library for Clojure and ClojureScript. Designed around first-class data structures (Malli schemas are pure Clojure vectors), Malli provides declarative schema definition, fast data validation, value coercion, JSON Schema transformation, and property-based test generation via [Hypothesis](../development_ops/hypothesis.md) or Clojure's test.check.

In modern multi-agent systems and agentic platforms (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**), Malli provides runtime boundary validation and schema serialization, ensuring structured tool calls, agent responses, and FastMCP 3.1 task payloads satisfy strict type contracts before execution.

Key capabilities include:
- **Vector-Based Schema ASTs**: Pure EDN/Clojure data structure definitions (`[:map [:id :uuid] [:status [:enum :active :paused]]]`) that can be transformed, inspected, and serialized at runtime.
- **Ahead-of-Time (AOT) Compilation**: Compiles declarative schema vectors into high-throughput JVM bytecode and optimized predicate functions.
- **Bi-directional Value Coercion**: Automates data coercion across HTTP query strings, JSON payloads, and relational database records.
- **Dynamic FastMCP 3.1 Tool Schema Generation**: Exports Malli vector ASTs to JSON Schema formats for seamless MCP 3.1 tool calling and Pydantic v2 cross-language validation.
- **Property-Based Value Generation**: Automatically generates synthetic valid/invalid test payloads via `test.check` and Hypothesis bridges.

```
+-----------------------------------------------------------------------------------+
|                                 MALLI SCHEMA ENGINE                               |
|                                                                                   |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  Data Vector Schema    |  |  Runtime Coercion      |  |  JSON Schema & OpenAPI|  |
|  |  Declarations          |  |  Validation Engine     |  |  Export Generators  |  |
|  +------------------------+  +------------------------+  +---------------------+  |
|  |  FastMCP 3.1 Task      |  |  Pydantic v2 Interop   |  |  Property-Based     |  |
|  |  Protocol Validator    |  |  Contract Engine       |  |  Value Generators   |  |
|  +------------------------+  +------------------------+  +---------------------+  |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                             AGENT / APPLICATION BOUNDARY                          |
|         (Structured LLM Outputs, Tool Arguments, API Endpoints, Databases)         |
+-----------------------------------------------------------------------------------+
```

### Mathematical Foundations of Schema Vector AST Validation & Lattice Type Theory

Malli treats schema evaluation as membership verification within a bounded distributive type lattice $\mathcal{L} = (\mathcal{T}, \sqsubseteq, \sqcup, \sqcap, \bot, \top)$.

#### 1. Lattice Ordering & Schema Subsumption
Let $\mathcal{T}$ denote the universe of schema types, where $\bot$ represents the empty type (`:nothing`) and $\top$ represents the universal type (`:any`). For any two schemas $S_1, S_2 \in \mathcal{T}$, $S_1$ is a subtype of $S_2$ (subsumption denoted $S_1 \sqsubseteq S_2$) if and only if every valid value under $S_1$ is valid under $S_2$:

$$
S_1 \sqsubseteq S_2 \iff \forall v \in \mathcal{V}, \quad (v \models S_1 \implies v \models S_2)
$$

The meet ($\sqcap$, conjunction/intersection via `[:and ...]`) and join ($\sqcup$, disjunction/union via `[:or ...]`) operations satisfy:

$$
v \models (S_1 \sqcap S_2) \iff v \models S_1 \land v \models S_2
$$

$$
v \models (S_1 \sqcup S_2) \iff v \models S_1 \lor v \models S_2
$$

#### 2. Regular Expression Sequence Derivatives
When validating heterogeneous sequences and vectors (e.g., `[:cat :keyword [:* :int] :string]`), Malli computes Brzozowski derivatives $\partial_a(R)$ over sequence expressions $R$:

$$
\partial_a(R) = \{ w \in \Sigma^* \mid a w \in R \}
$$

The membership predicate $\delta(R)$ determines whether the empty sequence $\epsilon$ belongs to $R$:

$$
\delta(\epsilon) = \text{true}, \quad \delta(a) = \text{false}, \quad \delta(R_1 \cdot R_2) = \delta(R_1) \land \delta(R_2)
$$

This allows linear time validation $\mathcal{O}(N)$ over arbitrary length sequential tool payloads emitted by LLMs.

#### 3. Generator Distribution Entropy in Property-Based Fuzzing
When sampling synthetic test fixtures from a schema $S$, the probability density function $P(v \mid S)$ over generated values $v \in \mathcal{V}_S$ is optimized to maximize Shannon entropy $\mathcal{H}(S)$ across edge-case boundary conditions:

$$
\mathcal{H}(S) = -\sum_{v \in \mathcal{V}_S} P(v \mid S) \log_2 P(v \mid S)
$$

Ensuring boundary cases (e.g., empty strings, MAX_INT, boundary decimals, nulls) receive non-zero exploration probability $\min_{v \in \text{Edges}} P(v \mid S) \ge \epsilon > 0$.

## Architecture & Schema Validation Flow
Malli processes validation by compiling pure vector AST declarations into optimized validator functions that execute against incoming nested data structures.

```mermaid
graph TD
    A[Agent Tool Request / JSON Payload] -->|Parse EDN / JSON| B[Malli Coercion Engine]
    B -->|String / Type Matchers| C[Coerced Data Map]
    C -->|Evaluate Vector AST| D[Compiled Malli Validator]
    D -->|Valid Payload| E[Dispatch Application Logic / Tool Execution]
    D -->|Invalid Payload| F[Humanize Error Generator]
    F -->|Formatted JSON Error Vector| G[Agent Self-Correction Prompt Loop]
```

## Detailed Execution Sequence

```mermaid
sequenceDiagram
    autonumber
    participant Agent as Autonomous LLM Agent
    participant Gateway as FastMCP 3.1 Gateway
    participant Malli as Malli Validator (Clojure Service)
    participant Core as Functional Core System

    Agent->>Gateway: Send Tool Execution Request (`{:task/id "tsk-101"}`)
    Gateway->>Malli: Transmit Vector Schema & Data Payload
    Malli->>Malli: Coerce Types (String -> UUID, String -> Double)
    Malli->>Malli: Evaluate Structural Constraints
    alt Validation Succeeded
        Malli-->>Gateway: Return Coerced Typed Map
        Gateway->>Core: Execute Target Function
        Core-->>Gateway: Return System Output
        Gateway-->>Agent: Send Success Response
    else Validation Failed
        Malli-->>Gateway: Return Humanized Error Structure (`malli.error/humanize`)
        Gateway-->>Agent: Prompt with Structured Correction Instructions
    end
```

## What problem it solves
LLM tool execution and multi-agent message routing require strict structural contracts to prevent runtime type exceptions and invalid parameter passing. Traditional schema libraries often rely on opaque class hierarchies or slow reflection, making dynamically configured schema generation difficult.

Malli represents schemas as pure data structures (e.g., `[:map [:user/id :uuid] [:user/email :string]]`), allowing AI agents to generate, inspect, transform, and validate API payload schemas dynamically at runtime.

## Where it fits in the stack
**Frameworks / Schema & Contract Layer**. Malli provides boundary validation for Clojure backends, agent frameworks (like [Mycelium](mycelium.md)), and microservice API routes. It serves the functional Clojure ecosystem in much the same way [Pydantic](pydantic.md) serves Python.

## Clojure Vector Schema Syntax & Custom Registries
Malli schemas are pure data vectors that compose recursively:
- **Primitives**: `:string`, `:int`, `:double`, `:boolean`, `:keyword`, `:uuid`, `:qualified-keyword`.
- **Combinators**: `[:map ...]`, `[:vector ...]`, `[:set ...]`, `[:tuple ...]`, `[:enum ...]`, `[:maybe ...]`, `[:and ...]`, `[:or ...]`.
- **Properties Map**: `{optional: true}`, `{min: 1}`, `{max: 100}`, `{description: "User display name"}`.
- **Custom Schema Registries**: Registering global domain types into a Malli registry map:
  ```clojure
  (def custom-registry
    (m/default-schemas
      {:user/id :uuid
       :user/role [:enum :admin :operator :guest]}))
  ```

## Property-Based Test Generation & Hypothesis Interop
Because Malli schemas are declarative data structures, Malli can automatically instantiate random, structurally valid test data streams using Clojure's `test.check` generator library. This enables end-to-end property testing for multi-agent workflows and allows cross-language fuzz testing when paired with Python's [Hypothesis](../development_ops/hypothesis.md) framework.

## Schema & Validation Library Comparison Matrix

| Feature / Dimension | Malli (Clojure) | Clojure Spec 2 | Pydantic v2 (Python) | Zod (TypeScript) | TypeBox (TypeScript) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Representation** | **Pure Data Vectors** | Macro Definitions | Python Classes | TypeScript Chainable AST | JSON Schema Objects |
| **Serializable** | **Yes (Pure EDN / JSON)**| No (Functions/Macros)| Via JSON Schema export | Via Zod-to-JSON-Schema | Native JSON Schema |
| **Value Coercion** | **Built-in (HTTP/JSON)**| Manual wrappers | Built-in (Type casting) | Built-in (Coerce methods)| Manual Cleaners |
| **Performance** | **Fast (AOT Bytecode)**| Medium | Native C/Rust core | Fast V8 execution | Extremely Fast |
| **Generator Support**| **Automatic test.check**| Automatic test.check| Via Hypothesis strategy| Via polyfills / plugins | JSON-Schema-Faker |
| **FastMCP 3.1 Bridge**| **EDN Vector AST Bridge**| Custom Macro Wrapper | Native Pydantic v2 | Zod Schema Adapter | Direct JSON Schema |
| **Strict Schema Mode**| **Yes (`:closed true`)**| Disallowed keys error| `extra='forbid'` | `.strict()` | `additionalProperties: false` |

## Typical use cases
- **Structured LLM Tool Call Validation**: Validating that JSON tool call parameters emitted by LLMs conform to declared tool schemas.
- **Dynamic OpenAPI / JSON Schema Generation**: Exporting Clojure Malli schemas to standard JSON Schema specs for LLM prompt injection.
- **API Endpoint Coercion**: Converting incoming HTTP request string queries into typed Clojure integers, UUIDs, and keywords.
- **Database Entity Contracts**: Enforcing entity relationships and column constraints in functional data pipelines.
- **Agent Payload Contract Negotiation**: Exposing schema definitions as EDN data structures over FastMCP 3.1 endpoints.
- **Multi-tenant Domain Boundary Checks**: Dynamically loading customer-specific Malli schemas from EDN files or database records without re-compiling source code.

## Strengths
- **Data-Driven Architecture**: Schemas are pure Clojure data vectors, allowing simple manipulation, filtering, and programmatic creation.
- **High Performance**: Compiles schema validators into optimized execution functions for high throughput.
- **Rich Ecosystem Generators**: Automatically produces sample data values and property-based test generators from schema definitions.
- **Extensible Coercion**: Supports custom string, JSON, and database coercion matchers out of the box.
- **Bi-directional Transformations**: Easily converts back and forth between Malli vector definitions, JSON Schemas, and OpenAPI 3.1 specs.

## Limitations
- **Language Focus**: Primary design is tailored for Clojure and ClojureScript.
- **Learning Curve**: Requires familiarity with Clojure vector syntax and functional schema transformation patterns.
- **Interoperability Overhead**: Calling Malli validators from non-JVM runtimes requires JSON/EDN socket bridges or REST endpoints.

## When to use it
- When developing Clojure backends or multi-agent systems requiring strict, data-driven validation.
- When you need to generate dynamic JSON Schemas at runtime to guide LLM response structures.
- For high-throughput Clojure microservices where schema validation performance is critical.
- When sharing schema declarations as data vectors between client and server layers.

## When not to use it
- In purely Python-based AI agent stacks (use [Pydantic v2](pydantic.md) or [PydanticAI](pydantic-ai.md) instead).
- In TypeScript or Node.js microservices (use Zod or TypeBox instead).
- Legacy JVM applications constrained to old Java reflection frameworks.

## Getting started

### 1. Clojure Dependency Setup
Add Malli to your `deps.edn`:
```clojure
{:deps {metosin/malli {:mvn/version "0.14.0"}}}
```

### 2. Basic Validation Example
```clojure
(ns my-app.schema
  (:require [malli.core :as m]))

(def UserSchema
  [:map
   [:id :uuid]
   [:name :string]
   [:email [:re #"^[^@]+@[^@]+$"]]
   [:role {:optional true} [:enum :admin :user]]])

;; Validate a map
(m/validate UserSchema {:id #uuid "d290f1ee-6c54-4b01-90e6-d701748f0851"
                        :name "Alice"
                        :email "alice@example.com"})
;; => true
```

## CLI examples

### 1. Run Clojure Validation Tests
```bash
clj -M:test
```

### 2. Export Malli Schema to JSON Schema via Clojure REPL
```bash
clj -e "(require '[malli.json-schema :as json-schema]) (println (json-schema/transform [:map [:x :int]]))"
```

### 3. Generate Random Sample Data from Malli Schema
```bash
clj -e "(require '[malli.generator :as mg]) (println (mg/generate [:map [:user/id :uuid] [:user/score :int]]))"
```

## API examples

### 1. Coercion & Schema Generation in Clojure
```clojure
(ns my-app.coercion
  (:require [malli.core :as m]
            [malli.transform :as mt]
            [malli.error :as me]))

(def OrderSchema
  [:map
   [:order-id :uuid]
   [:quantity :int]
   [:price :double]])

;; Coerce string values from HTTP parameters into typed Clojure values
(defn parse-and-validate-order [raw-input]
  (let [coerced (m/decode OrderSchema raw-input (mt/string-transformer))]
    (if (m/validate OrderSchema coerced)
      {:status :success :data coerced}
      {:status :error :errors (me/humanize (m/explain OrderSchema coerced))})))
```

### 2. Advanced FastMCP 3.1 & Python Pydantic v2 Bridge
The following FastMCP 3.1 Python server translates EDN-styled Malli schema vectors into dynamic Pydantic v2 schemas (`extra="forbid"`, `frozen=True`) for cross-language verification:

```python
import sys
import json
import logging
from typing import Dict, Any, List, Optional
import mcp.server.fastmcp as fastmcp
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, create_model, ConfigDict

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("MalliBridgeFastMCP")

mcp_server = FastMCP(
    "Malli Schema Bridge Server",
    version="3.1.0",
    instructions="Bridges Clojure Malli data vector schemas into FastMCP 3.1 validation models."
)

class MalliSchemaBridgeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_name: str = Field(..., description="Target schema identifier (e.g. 'UserTaskSchema')")
    vector_schema: List[Any] = Field(..., description="Malli vector schema definition (e.g. [':map', [':id', ':string']])")
    data_payload: Dict[str, Any] = Field(..., description="Input JSON payload to validate")

class MalliSchemaBridgeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    valid: bool
    schema_name: str
    validated_data: Optional[Dict[str, Any]] = None
    errors: Optional[str] = None
    mcp_version: str = "3.1"

@mcp_server.tool()
async def validate_malli_payload(request: MalliSchemaBridgeRequest, ctx: Context) -> str:
    """Validates an incoming JSON dictionary against a Clojure Malli vector schema representation."""
    await ctx.report_progress(10, 100)
    ctx.info(f"Parsing Malli schema vector for '{request.schema_name}'")

    type_map = {
        ":string": str,
        ":int": int,
        ":double": float,
        ":boolean": bool,
        ":uuid": str
    }

    fields = {}
    if len(request.vector_schema) > 1 and request.vector_schema[0] == ":map":
        for entry in request.vector_schema[1:]:
            if isinstance(entry, list) and len(entry) >= 2:
                field_key = str(entry[0]).lstrip(":")
                field_type_str = str(entry[1])
                target_type = type_map.get(field_type_str, str)
                fields[field_key] = (target_type, ...)

    await ctx.report_progress(50, 100)
    ctx.info("Building dynamic Pydantic v2 model from Malli fields...")

    try:
        DynamicModel = create_model(
            request.schema_name,
            __config__=ConfigDict(extra="forbid", frozen=True),
            **fields
        )
        validated_instance = DynamicModel(**request.data_payload)

        await ctx.report_progress(100, 100)
        res = MalliSchemaBridgeResponse(
            valid=True,
            schema_name=request.schema_name,
            validated_data=validated_instance.model_dump(),
            mcp_version="3.1"
        )
        return res.model_dump_json(indent=2)
    except Exception as exc:
        ctx.warning(f"Validation failed for schema '{request.schema_name}': {exc}")
        res = MalliSchemaBridgeResponse(
            valid=False,
            schema_name=request.schema_name,
            errors=str(exc),
            mcp_version="3.1"
        )
        return res.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp_server.run(transport="stdio")
```

## Docker Compose Deployment Definition

```yaml
version: "3.8"

services:
  malli-validator-service:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: malli-validator-service
    restart: unless-stopped
    ports:
      - "8009:8009"
    environment:
      - JVM_OPTS=-Xmx512m
      - PORT=8009
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8009/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    networks:
      - agent-schema-net

networks:
  agent-schema-net:
    driver: bridge
```

## Systemd Production Daemon Unit Definition
Save unit file to `/etc/systemd/system/malli-validator.service`:

```ini
[Unit]
Description=Malli Schema Validator Microservice
After=network.target

[Service]
Type=simple
User=malli-user
WorkingDirectory=/opt/malli-service
ExecStart=/usr/bin/java -jar /opt/malli-service/target/malli-service-standalone.jar
Restart=always
RestartSec=3s
Environment="PORT=8009"
Environment="JVM_OPTS=-Xmx512m"

# Security Hardening Settings
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true
PrivateTmp=true
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

### Automated Daemon Health Probe Script
Production probe script for CI/CD runners and Kubernetes liveness checks:

```python
#!/usr/bin/env python3
"""Automated Health Verification Probe for Malli Validator Service."""

import sys
import time
import requests

PROBE_URL = "http://127.0.0.1:8009/health"

def run_probe(retries: int = 3, timeout_sec: float = 2.0) -> bool:
    for attempt in range(1, retries + 1):
        try:
            start_time = time.monotonic()
            resp = requests.get(PROBE_URL, timeout=timeout_sec)
            elapsed_ms = (time.monotonic() - start_time) * 1000
            if resp.status_code == 200:
                print(f"[OK] Malli validator healthy (latency: {elapsed_ms:.1f}ms)")
                return True
            else:
                print(f"[WARN] Attempt {attempt}: Received HTTP {resp.status_code}")
        except requests.RequestException as e:
            print(f"[WARN] Attempt {attempt}: Connection failed ({e})")
        time.sleep(1.0)
    print("[ERROR] Malli validator health check failed after maximum retries.")
    return False

if __name__ == "__main__":
    if not run_probe():
        sys.exit(1)
```

## Diagnostic & Troubleshooting Matrix

| Issue Symptom / Error | Root Cause | Verification Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **`Schema Parsing Exception`** | Invalid vector AST structure | `clj -e "(require '[malli.core :as m]) (m/schema [:map])"` | Ensure vector declarations start with valid schema type keyword (`:map`, `:vector`, `:tuple`). |
| **`Coercion Mismatch`** | Raw string cannot be coerced to target keyword/UUID | Inspect raw input map in REPL | Verify transformer matchers (`mt/string-transformer` or `mt/json-transformer`) are explicitly passed. |
| **`Humanize Error Null`** | Custom schema lacks explanation formatter | `m/explain schema data` | Check schema syntax or register custom error formatter for domain types. |
| **`JVM Memory Pressure`** | Massive schema generation loop in property tests | `top -b -n 1 \| grep java` | Bound generator size using `mg/generate schema {:size 10}`. |
| **`JSON Schema Export Failure`** | Custom predicate function cannot be serialized | Inspect schema for inline lambda functions | Use named Malli registry properties instead of opaque anonymous functions. |
| **`FastMCP Bridge Type Error`** | Unmapped Clojure keyword in Python interop bridge | Inspect `type_map` dictionary in FastMCP server | Register custom type handler in Python Pydantic bridge. |
| **`EXTRA_KEYS_DISALLOWED_FAIL`** | Closed map received unrecognized keys from agent output | `(m/explain [:map {:closed true} ...] data)` | Filter out extraneous parameters or loosen map schema constraint. |
| **`RECURSIVE_SCHEMA_OVERFLOW`** | Self-referential schema AST lacks recursive delay wrapper | Check schema tree for circular definition | Wrap recursive references using `[:schema {:registry ...} :ref]` lazy combinator. |

## Related tools / concepts
- [Mycelium](mycelium.md) — Clojure multi-agent framework utilizing Malli schemas.
- [Maestro](maestro.md) — Thread pool and task execution engine for Clojure.
- [Pydantic](../frameworks/pydantic.md) — Python data validation and settings management.
- [PydanticAI](../frameworks/pydantic-ai.md) — Agent framework built on Pydantic schemas.

## Sources / references
- [Malli GitHub Repository](https://github.com/metosin/malli)
- [Metosin Malli Documentation](https://cljdoc.org/d/metosin/malli/CURRENT)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

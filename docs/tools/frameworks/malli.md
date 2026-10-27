# Malli

## What it is
**Malli** is a data-driven, high-performance specification and schema validation library for Clojure and ClojureScript. Designed around first-class data structures (Malli schemas are pure Clojure vectors), Malli provides declarative schema definition, fast data validation, value coercion, JSON Schema transformation, and property-based test generation via [Hypothesis](../development_ops/hypothesis.md) or Clojure's test.check.

In modern multi-agent systems and agentic platforms (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Ultra**, **DeepSeek-V4**, and **Llama 4**), Malli provides runtime boundary validation and schema serialization, ensuring structured tool calls, agent responses, and FastMCP 3.1 task payloads satisfy strict type contracts before execution.

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

## What problem it solves
LLM tool execution and multi-agent message routing require strict structural contracts to prevent runtime runtime type exceptions and invalid parameter passing. Traditional schema libraries often rely on opaque class hierarchies or slow reflection, making dynamically configured schema generation difficult.

Malli represents schemas as pure data structures (e.g., `[:map [:user/id :uuid] [:user/email :string]]`), allowing AI agents to generate, inspect, transform, and validate API payload schemas dynamically at runtime.

## Where it fits in the stack
**Frameworks / Schema & Contract Layer**. Malli provides boundary validation for Clojure backends, agent frameworks (like [Mycelium](mycelium.md)), and microservice API routes. It serves the functional Clojure ecosystem in much the same way [Pydantic](pydantic.md) serves Python.

## Schema Validation & Coercion Flow

```
[Agent / External API]          [Malli Validation Engine]           [Application Logic]
          |                                 |                                 |
          | 1. Send Raw JSON Payload        |                                 |
          |-------------------------------->|                                 |
          |                                 | 2. Validate Vector Schema       |
          |                                 | 3. Coerce Types (String -> UUID)|
          |                                 |                                 |
          |                                 |---[ If Valid ]----------------->|
          |                                 |                                 | 4. Process Safe Data
          |                                 |                                 |<-----------------
          |                                 |---[ If Invalid ]----------------|
          |                                 |                                 |
          | 5. Return Human/AI Error Vector |                                 |
          |<--------------------------------|                                 |
```

## Schema & Validation Library Comparison Matrix

| Feature / Dimension | Malli (Clojure) | Clojure Spec | Pydantic v2 (Python) | Zod (TypeScript) |
| :--- | :--- | :--- | :--- | :--- |
| **Representation** | Pure Data Vectors | Macro Definitions | Python Classes | TypeScript Chainable AST |
| **Serializable** | Yes (Pure EDN / JSON) | No (Functions/Macros)| Via JSON Schema export | Via Zod-to-JSON-Schema |
| **Value Coercion** | Built-in (HTTP/JSON)| Manual wrappers | Built-in (Type casting) | Built-in (Coerce methods)|
| **Performance** | Fast (Ahead-of-time) | Medium | Native C/Rust core | Fast V8 execution |
| **Generator Support**| Automatic test.check| Automatic test.check| Via Hypothesis strategy| Via polyfills / plugins |

## Typical use cases
- **Structured LLM Tool Call Validation**: Validating that JSON tool call parameters emitted by LLMs conform to declared tool schemas.
- **Dynamic OpenAPI / JSON Schema Generation**: Exporting Clojure Malli schemas to standard JSON Schema specs for LLM prompt injection.
- **API Endpoint Coercion**: Converting incoming HTTP request string queries into typed Clojure integers, UUIDs, and keywords.
- **Database Entity Contracts**: Enforcing entity relationships and column constraints in functional data pipelines.

## Strengths
- **Data-Driven Architecture**: Schemas are pure Clojure data vectors, allowing simple manipulation, filtering, and programmatic creation.
- **High Performance**: Compiles schema validators into optimized execution functions for high throughput.
- **Rich Ecosystem Generators**: Automatically produces sample data values and property-based test generators from schema definitions.
- **Extensible Coercion**: Supports custom string, JSON, and database coercion matchers out of the box.

## Limitations
- **Language Focus**: Primary design is tailored for Clojure and ClojureScript.
- **Learning Curve**: Requires familiarity with Clojure vector syntax and functional schema transformation patterns.

## When to use it
- When developing Clojure backends or multi-agent systems requiring strict, data-driven validation.
- When you need to generate dynamic JSON Schemas at runtime to guide LLM response structures.
- For high-throughput Clojure microservices where schema validation performance is critical.

## When not to use it
- In purely Python-based AI agent stacks (use [Pydantic v2](pydantic.md) or [PydanticAI](pydantic-ai.md) instead).
- In TypeScript or Node.js microservices (use Zod or TypeBox instead).

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

## API examples

### 1. Coercion & Schema Generation in Clojure
```clojure
(ns my-app.coercion
  (:require [malli.core :as m]
            [malli.transform :as mt]))

(def OrderSchema
  [:map
   [:order-id :uuid]
   [:quantity :int]
   [:price :double]])

;; Coerce string values from HTTP parameters into typed Clojure values
(defn parse-order [raw-input]
  (m/decode OrderSchema raw-input (mt/string-transformer)))
```

### 2. FastMCP 3.1 & Pydantic v2 Python Interop Model
The following Python script demonstrates how a Python agent service models and verifies a Malli schema contract payload under early January 2027 FastMCP 3.1 standards:

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json

class MalliSchemaDeclaration(BaseModel):
    schema_name: str = Field(..., pattern=r"^[a-zA-Z0-9._/-]+$")
    vector_definition: List[Any] = Field(..., min_length=2)
    description: str = Field(default="")

class MalliValidationResult(BaseModel):
    valid: bool
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    coerced_payload: Optional[Dict[str, Any]] = None

def validate_malli_interop(schema_name: str, definition: list) -> str:
    """Validates Malli schema declaration structure using Pydantic v2."""
    try:
        decl = MalliSchemaDeclaration(
            schema_name=schema_name,
            vector_definition=definition,
            description="Agent tool input validation contract"
        )
        return json.dumps({
            "status": "success",
            "schema": decl.model_dump()
        }, indent=2)
    except Exception as e:
        return json.dumps({
            "status": "error",
            "validation_errors": str(e)
        }, indent=2)

if __name__ == "__main__":
    sample_malli_vector = [":map", [":agent/id", ":string"], [":agent/priority", ":int"]]
    print(validate_malli_interop("AgentTaskContract", sample_malli_vector))
```

## Production Operational Best Practices

### 1. Ahead-Of-Time (AOT) Schema Compilation
Pre-compile frequently executed Malli schemas into compiled validator functions (`m/validator`) during service startup to eliminate runtime schema parsing overhead.

### 2. Informative Error Reporting
Use `malli.error/humanize` to format detailed validation failures into structured JSON error arrays suitable for LLM self-correction prompts.

### 3. Schema Registry Standardization
Maintain a centralized namespace or database store for shared Malli schemas across microservices to enforce consistent multi-agent data boundaries.

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

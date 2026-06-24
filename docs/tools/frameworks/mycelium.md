# Mycelium

## What it is
Mycelium is a Clojure-based framework and architectural pattern for building robust, observable AI systems using state machines and formal contracts. As of June 2026, it is the primary implementation of the 'Cellular Agent Architecture', where complex workflows are decomposed into isolated, functional 'cells' that communicate via strongly-typed Malli schemas.

## What problem it solves
It eliminates 'prompt spaghetti' and 'state drift' in complex agentic systems by enforcing strict boundaries between reasoning nodes. It provides a formal harness for LLMs to operate within, ensuring that agentic outputs are validated against machine-readable contracts before execution. This makes multi-step agentic reasoning predictable and debuggable at scale.

## Where it fits in the stack
**Orchestration / Control Plane**. Mycelium sits above the LLM inference layer (LiteLLM, Claude 4.8) and acts as the supervisor for agentic state. It is often used as the 'logical backbone' for systems where reliability and auditability are prioritized over rapid, ad-hoc prototyping.

## Typical use cases
- **Multi-Agent Coding Factories**: Coordinating specialized agents for planning, implementation, and testing with strict handoff protocols.
- **Mission-Critical Decision Support**: Systems where every agentic reasoning step must be traceable and validated against a schema.
- **Complex State Management**: Workflows that require long-running persistence, recursive nesting, and high-fidelity 'flight recording' (telemetry).
- **Functional AI Pipelines**: Leveraging Clojure's immutability and concurrency for high-throughput agentic tasks.

## Strengths
- **Formal Verification**: Uses Malli schemas for input/output validation, preventing malformed LLM responses from causing cascading failures.
- **High Observability**: Every state transition and cell execution is recorded in a structured trace, enabling precise root-cause analysis of agentic errors.
- **Composable Architecture**: Cells can be nested and reused as components in larger graphs, facilitating a modular 'LEGO-like' system design.
- **Agent-Friendly Structure**: The explicit 'ceremony' of Mycelium provides clear structural cues that improve frontier model performance (e.g., Claude 4.8 Opus).

## Limitations
- **Functional Paradigm**: Requires proficiency in Clojure and functional programming, which may pose a barrier for teams focused on Python-native AI ecosystems.
- **Upfront Complexity**: Designing a system with Mycelium requires more initial architectural planning than simple imperative loops.
- **Library Ecosystem**: While growing, the Clojure AI library ecosystem is smaller than Python's, though Mycelium facilitates easy Java/Python interop.

## When to use it
- When building large-scale, production-grade agentic systems that require high reliability and observability.
- When your architecture demands formal data contracts and state machine-based orchestration.
- If your environment already utilizes JVM/Clojure and requires native AI integration.

## When not to use it
- For simple scripts, linear pipelines, or quick prototypes where the architectural overhead is unnecessary.
- If your team is not comfortable with functional programming or Lisp-like syntax.
- When near-instantaneous developer velocity in Python is prioritized over long-term system stability.

## Getting started

### Installation (deps.edn)
Add the June 2026 stable release to your Clojure project:
```clojure
{:deps {mycelium/mycelium {:mvn/version "2026.6.12"}}}
```

### Basic Cell Definition
A Cell is the atomic unit of logic in Mycelium, consisting of an ID, schemas, and a handler function.
```clojure
(require '[mycelium.core :as m]
         '[malli.core :as ml])

(def CodeAuditCell
  {:id :code-audit
   :input-schema [:map [:code :string] [:standard :keyword]]
   :output-schema [:map [:status :keyword] [:issues [:vector :string]]]
   :fn (fn [{:keys [code standard]}]
         ;; Logic to call Claude 4.8 via LiteLLM
         {:status :success :issues []})})
```

## CLI examples

### Running a Mycelium Node
Mycelium nodes are typically started via the Clojure CLI or as part of a larger Uberjar deployment.
```bash
# Start a Mycelium REPL for interactive agent development
clj -M:mycelium:repl

# Execute a specific cell mission from the CLI
clj -X mycelium.cli/run-cell :id :code-audit :input '{:code "(defn x [] 1)" :standard :clojure}'
```

### Inspection and Tracing
```bash
# Export the latest execution trace for visualization
mycelium-trace export --id last --format json > trace.json
```

## API examples

### Schema-Driven Agent Handoff
Mycelium ensures that data passing between agents (cells) is always valid.
```clojure
(def AgentContract
  [:map
   [:intent [:enum :refactor :debug :feature]]
   [:context :string]
   [:priority [:int {:min 1 :max 5}]]])

;; Mycelium intercepts the output of an LLM call, validates it against AgentContract,
;; and automatically triggers a 'Self-Correction' cell if the validation fails.
(m/register-cell!
  {:id :agent-dispatcher
   :output-schema AgentContract
   :fn (fn [in] (llm-call :claude-4.8 (build-prompt in)))})
```

### n8n Connection Pattern
- **Pattern**: Mycelium as the 'Brain', n8n as the 'Hands'.
- **Workflow**: n8n receives a webhook -> forwards payload to Mycelium API -> Mycelium runs complex state machine logic -> Mycelium sends command back to n8n for execution (e.g., Slack, Email).

## Related tools / concepts
- [Maestro](https://github.com/yogthos/maestro) (underlying engine)
- [Malli](https://github.com/metosin/malli) (data-driven schemas)
- [Software Factories](../../knowledge_base/patterns/software-factories.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [LiteLLM](../../services/litellm.md)
- [MCP 3.0](../automation_orchestration/mcp.md)
- [AG2](../frameworks/ag2.md)
- [Cognician](../frameworks/cognician.md)
- [Functional Programming for AI](../../knowledge_base/functional-ai-patterns.md)
- [Multi-Agent Contract Architecture](../../architecture/multi_agent_knowledgeops.md)

## Sources / references
- [Mycelium: Building Predictable AI at Scale (yogthos.net)](https://yogthos.net/posts/2026-02-25-ai-at-scale.html)
- [GitHub: yogthos/mycelium](https://github.com/yogthos/mycelium)
- [Clojure for the Agentic Era (2026 Whitepaper)](https://clojure.org/news/2026/01/15/agentic-clojure)
- [Malli Schema Specification](https://github.com/metosin/malli)

## Contribution Metadata

- Last reviewed: 2026-06-22
- Confidence: high

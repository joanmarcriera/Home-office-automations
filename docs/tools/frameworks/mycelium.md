# Mycelium

## What it is
Mycelium is an enterprise-grade, Clojure-based framework and architectural pattern for building robust, observable AI systems using state machines and formal contracts. As of late November/December 2026, it is the primary implementation of the 'Cellular Agent Architecture', where complex, multi-turn reasoning workflows are decomposed into isolated, functional 'cells' that communicate exclusively via strongly-typed Malli schemas.

## What problem it solves
It eliminates 'prompt spaghetti' and 'state drift' in complex agentic systems by enforcing strict boundaries and data contracts between reasoning nodes. By providing a formal harness for LLMs, Mycelium ensures that agentic outputs are validated against machine-readable contracts before execution, preventing raw LLM hallucination from causing cascading downstream failures. This makes multi-step agentic reasoning predictable, testable, and debuggable at scale.

## Where it fits in the stack
**Orchestration / Control Plane**. Mycelium sits above the LLM inference layer (LiteLLM, Claude 5.1, GPT-5.5, Gemini 4.0, Llama 4, and Gemma 3) and acts as the supervisor for agentic state. It is often used as the 'logical backbone' for enterprise environments where reliability, strict verification, and deep observability are prioritized over rapid, ad-hoc prototyping.

## Typical use cases
- **Multi-Agent Coding Factories**: Coordinating specialized, specialized agents for planning, implementation, and testing with strict handoff protocols and contract-based verification.
- **Mission-Critical Decision Support**: Systems where every agentic reasoning step must be traceable, auditable, and validated against a schema before triggering real-world side effects.
- **Complex State Management**: Workflows that require long-running persistence, recursive nesting, and high-fidelity 'flight recording' (telemetry) for multi-agent loops.
- **Functional AI Pipelines**: Leveraging Clojure's immutability, software transactional memory (STM), and concurrency for high-throughput, fault-tolerant agentic tasks.
- **MCP-Orchestrated Environments**: Dynamically routing tasks from Model Context Protocol (MCP 3.1/FastMCP 3.1) clients to specialized Clojure cells for secure execution.

## Strengths
- **Formal Verification**: Uses Malli schemas for input/output validation, preventing malformed or hallucinated LLM responses from propagating.
- **High Observability**: Every state transition and cell execution is recorded in a structured trace, enabling precise root-cause analysis of agentic errors and latency bottlenecks.
- **Composable Architecture**: Cells can be nested and reused as components in larger graphs, facilitating a modular 'LEGO-like' system design.
- **Agent-Friendly Structure**: The explicit 'ceremony' of Mycelium provides clear structural cues that improve frontier model performance (e.g., Claude 5.1, GPT-5.5).
- **Native Concurrency**: Built on the JVM, leveraging Clojure's lightweight threads and immutable data structures for concurrent execution without race conditions.

## Limitations
- **Functional Paradigm**: Requires proficiency in Clojure and functional programming, which may pose a steep learning curve for teams focused on Python-native AI ecosystems.
- **Upfront Complexity**: Designing a system with Mycelium requires more initial architectural planning than simple imperative loops or basic LangChain chains.
- **Library Ecosystem**: While growing, the Clojure AI library ecosystem is smaller than Python's, although Mycelium facilitates easy Java/Python interop to close this gap.

## When to use it
- When building large-scale, production-grade agentic systems that require high reliability, observability, and strict schema compliance.
- When your architecture demands formal data contracts and state machine-based orchestration to manage multi-agent handoffs.
- If your environment already utilizes JVM/Clojure and requires native, high-performance AI integration.

## When not to use it
- For simple scripts, linear pipelines, or quick prototypes where the architectural overhead is unnecessary.
- If your development team is not comfortable with functional programming or Lisp-like syntax.
- When near-instantaneous developer velocity in Python is prioritized over long-term system stability and formal verification.

## Getting started

### Installation (deps.edn)
Add the late 2026 stable release to your Clojure project:
```clojure
{:deps {mycelium/mycelium {:mvn/version "2026.11.30"}}}
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
         ;; Logic to call Claude 5.1 via LiteLLM or an MCP server
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

### Schema-Driven Agent Handoff (Malli Contract Validation)
Mycelium ensures that data passing between agents (cells) is always valid using Malli schemas, which provide runtime verification similar to Python's Pydantic.

```clojure
(require '[malli.core :as ml]
         '[mycelium.core :as m])

;; Define strict Malli schema contract
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
   :fn (fn [in]
         ;; Calls frontier models (e.g., Claude 5.1) and returns mapped result
         (let [raw-response (m/llm-call :claude-5-1 (m/build-prompt in))]
           ;; Output will be strictly validated against output-schema (AgentContract) by Mycelium
           raw-response))})
```

### Model Context Protocol (MCP 3.1 / FastMCP 3.1) Client Integration
Mycelium cells can interact directly with MCP servers to discover and consume tools in real-time, matching modern agent paradigms.
```clojure
;; Initialize an MCP client connection within the cellular framework
(def mcp-client (m/init-mcp-client! {:uri "http://localhost:3011/mcp"}))

(m/register-cell!
  {:id :mcp-tool-executor
   :input-schema [:map [:tool-name :string] [:arguments :map]]
   :output-schema [:map [:result :string]]
   :fn (fn [{:keys [tool-name arguments]}]
         (let [response (m/call-mcp-tool mcp-client tool-name arguments)]
           {:result (:content response)}))})
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
- [MCP 3.1](../automation_orchestration/mcp.md)
- [Tool Calling and MCP](../../knowledge_base/patterns/tool-calling-and-mcp.md)
- [AG2](ag2.md)
- [LangGraph](langgraph.md)
- [Smolagents](smolagents.md)
- [Pydantic AI](pydantic-ai.md)
- [CrewAI](crewai.md)

## Sources / references
- [Mycelium: Building Predictable AI at Scale (yogthos.net)](https://yogthos.net/posts/2026-02-25-ai-at-scale.html)
- [GitHub: yogthos/mycelium](https://github.com/yogthos/mycelium)
- [Clojure for the Agentic Era (2026 Whitepaper)](https://clojure.org/news/2026/01/15/agentic-clojure)
- [Malli Schema Specification](https://github.com/metosin/malli)

## Contribution Metadata
- Last reviewed: 2026-12-11
- Confidence: high

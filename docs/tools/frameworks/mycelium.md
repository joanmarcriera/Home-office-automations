# Mycelium

## What it is
Mycelium is a Clojure-based framework and architectural pattern designed for building complex, large-scale AI applications using state machines and formal contracts. It emphasizes structural clarity and explicit state management to make agentic workflows predictable and observable.

## What problem it solves
It addresses "context rot" and cognitive saturation in LLM agents by decomposing complex software into isolated, stable subassemblies. By separating routing logic (orchestration) from implementation details (cells), it ensures that both humans and agents work within manageable, bounded contexts. It prevents the common "spaghetti prompt" problem in large agentic systems.

## Where it fits in the stack
**Framework / Pattern**. It provides the structural blueprint for how agents and code interact within a larger system. It sits above the LLM provider layer as an orchestration and validation harness.

## Typical use cases
- **Complex Agentic Systems**: Building software where LLMs manage multiple interdependent tasks (e.g., a multi-agent coding assistant).
- **Large-Scale Functional Applications**: Leveraging Clojure's strengths for robust, observable AI workflows in production environments.
- **Self-Correcting Loops**: Using formal contracts (Malli) to validate agent output and provide immediate, structured feedback to the model.

## Strengths
- **Observability**: Every state transition is traced, providing a "flight recorder" for agentic workflows, making it easy to debug why an agent deviated from its path.
- **Strict Contracts**: Uses Malli schemas to enforce inputs and outputs, preventing hallucinated data structures from breaking downstream nodes.
- **Recursive Design**: Systems built with Mycelium can themselves be treated as individual cells in larger graphs, enabling infinite nesting.
- **Agent Synergy**: Designed to thrive on the "ceremony" and structural planning that humans find tedious but LLMs find clarifying.

## Limitations
- **Language Barrier**: Requires knowledge of Clojure and functional programming paradigms, which has a steeper learning curve than Python.
- **Initial Overhead**: Requires more upfront architectural planning compared to ad-hoc "if-statement" based logic or simpler frameworks like LangChain.
- **Ecosystem**: Smaller community and fewer pre-built "tools" compared to the massive Python AI ecosystem.

## When to use it
- For mission-critical AI applications where reliability, traceability, and observability are paramount.
- When building systems that are too complex for a single LLM context window to manage effectively.
- If your stack already leverages JVM or Clojure and you need a native AI orchestration layer.

## When not to use it
- For simple, linear scripts or small prototypes where the architectural overhead isn't justified.
- If your development team is not comfortable with Clojure or functional patterns and needs to move quickly with Python.

## Licensing and cost
- **Open Source**: Yes (Eclipse Public License)
- **Cost**: Free
- **Self-hostable**: Yes

## Getting started

### Installation
You will need Leiningen or the Clojure CLI installed.
```bash
# Using Clojure CLI, add to deps.edn
{:deps {mycelium/mycelium {:git/url "https://github.com/yogthos/mycelium" :sha "..."}}}
```

### Basic Architecture
Mycelium organizes logic into **Cells**. A cell is a pure function wrapped in a schema:
```clojure
(require '[mycelium.core :as m]
         '[malli.core :as ml])

(def DocumentSummaryCell
  {:id :doc-summary
   :input-schema [:map [:content :string]]
   :output-schema [:map [:summary :string]]
   :fn (fn [{:keys [content]}]
         ;; Logic to call LLM goes here
         {:summary "Summary of document..."})})
```

## Technical Examples

### Malli Contract Validation
Ensuring the agent returns valid JSON that matches the expected schema:
```clojure
(def SearchResultSchema
  [:map
   [:title :string]
   [:url :string]
   [:relevance [:double {:min 0 :max 1}]]])

;; Mycelium automatically validates cell output against this schema
;; and can trigger a retry/correction loop if it fails.
```

### n8n Connection Pattern
While Mycelium is code-first, it can be triggered from n8n to handle complex sub-workflows:
- **Node**: Execute Command (running a Clojure script) or HTTP Request (calling a Mycelium-based API).
- **Pattern**: n8n handles the external integration (Email/Slack), while Mycelium handles the high-logic state transitions and validation.

## Related tools / concepts
- [Maestro](https://github.com/yogthos/maestro) (underlying workflow engine)
- [Malli](https://github.com/metosin/malli) (data-driven schemas)
- [Orchestration](../automation_orchestration/index.md)
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md)
- [System Prompts](../../knowledge_base/system_prompts.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md)

## Sources / References
- [Managing Complexity with Mycelium](https://yogthos.net/posts/2026-02-25-ai-at-scale.html)
- [Mycelium GitHub](https://github.com/yogthos/mycelium)

## Contribution Metadata

- Last reviewed: 2026-06-01
- Confidence: high

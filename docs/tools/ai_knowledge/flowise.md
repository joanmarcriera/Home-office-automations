# Flowise

## What it is
Flowise is an open-source visual builder for LLM applications. Built on top of LangChain, it provides a drag-and-drop interface to create complex chains, agents, and RAG pipelines.

## What problem it solves
It lowers the barrier to entry for building LLM applications by providing a no-code/low-code interface. It enables rapid prototyping and allows non-developers or technical product managers to iterate on prompt engineering and workflow logic visually.

## Where it fits in the stack
**Orchestration / Builder Layer**. It sits above your LLM providers and vector databases, serving as the "brain" and interface for your AI applications.

## Typical use cases
- **Customer Support Bots**: Building RAG-powered bots that answer questions based on company documentation.
- **Workflow Prototyping**: Quickly testing different LangChain components (retrievers, agents, tools) before committing to code.
- **Internal Tools**: Creating specialized assistants for data extraction, summarization, or translation that team members can use via a simple UI.
- **Agentic Workflows**: Designing agents with access to custom tools (APIs, calculators, search).

## Strengths
- **Visual Programming**: Makes complex LangChain logic intuitive and easy to reason about.
- **Self-Hostable**: Can be deployed easily via Docker, ensuring data privacy for local homelab use.
- **Extensibility**: Supports custom tools and JavaScript snippets for complex logic.
- **Integrated API**: Automatically generates REST endpoints for every chatflow you build.

## Limitations
- **LangChain Coupling**: If a feature isn't in LangChain (or hasn't been integrated into Flowise yet), it can be difficult to implement.
- **Version Management**: Managing changes and rollbacks to visual flows can be more challenging than versioning code.
- **Resource Usage**: Running the Flowise server and its UI adds overhead compared to a lightweight script.

## When to use it
- When you want to build and iterate on LLM applications visually.
- When you need to provide a GUI for team members to interact with AI workflows.
- For rapid prototyping of RAG and agentic systems.

## When not to use it
- When you need maximum programmatic flexibility or want to use frameworks like [LlamaIndex](llamaindex.md) or [DSPy](../frameworks/dspy.md).
- For simple scripts where the overhead of a visual builder is unnecessary.

## Getting started

### 1. Installation and Startup
The easiest way to run Flowise is via Docker:

```bash
docker run -d --name flowise -p 3000:3000 flowiseai/flowise
```

Alternatively, use `npx`:

```bash
npx flowise start
```

### 2. Building Your First Flow
1. Open `http://localhost:3000` in your browser.
2. Click "Add New" to create a chatflow.
3. Drag components from the sidebar (e.g., "OpenAI Chat Model", "Recursive Character Text Splitter", "In-Memory Vector Store").
4. Connect the components and click "Save".

## API examples

### Triggering a Prediction via REST API
Every chatflow can be triggered via a POST request.

```bash
curl -X POST "http://localhost:3000/api/v1/prediction/<CHATFLOW_ID>" \
     -H "Content-Type: application/json" \
     -d '{
            "question": "What are the benefits of using a visual builder?",
            "overrideConfig": {
                "temperature": 0.5
            }
         }'
```

### Passing External Variables
You can pass variables into your flows (e.g., a user ID or session context) that can be used within prompt templates.

```bash
curl -X POST "http://localhost:3000/api/v1/prediction/<CHATFLOW_ID>" \
     -H "Content-Type: application/json" \
     -d '{
            "question": "Summarize my last orders",
            "overrideConfig": {
                "vars": {
                    "user_id": "12345"
                }
            }
         }'
```

## Related tools / concepts
- [LangFlow](../frameworks/langflow.md)
- [Dify](dify.md)
- [LangChain](langchain.md)
- [AnythingLLM](anythingllm.md)
- [LobeHub](lobehub.md)
- [n8n](../../services/n8n.md)
- [Rivet](../frameworks/rivet.md)
- [Superinterface](../frameworks/superinterface.md)

## Sources / references
- [Flowise Official Documentation](https://docs.flowiseai.com/)
- [Flowise GitHub Repository](https://github.com/FlowiseAI/Flowise)
- [Flowise Cloud](https://flowiseai.com/)

## Contribution Metadata

- Last reviewed: 2026-05-14
- Confidence: high

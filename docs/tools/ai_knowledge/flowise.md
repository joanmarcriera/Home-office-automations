# Flowise

## What it is
Flowise is an open-source UI visual tool to build customized LLM flows. It is built on top of LangChain and allows you to create complex LLM chains and agents using a drag-and-drop interface.

## What problem it solves
Makes it possible to build and iterate on LLM chains and agent workflows visually, without needing to write LangChain code directly.

## Where it fits in the stack
AI & Knowledge — provides a no-code visual builder for LLM pipelines that can integrate with local Ollama models and other stack components.

## Typical use cases
- Building chatbot flows with retrieval-augmented generation
- Prototyping LangChain-based agent workflows via drag-and-drop
- Implementing support chatbots backed by local documentation

## Strengths
- Open-source and self-hostable
- Drag-and-drop interface built on the mature LangChain ecosystem
- Supports a wide range of LLM providers and vector stores

## Limitations
- Tightly coupled to LangChain, which may limit flexibility with other frameworks
- Visual interface can become unwieldy for very complex flows
- Debugging issues may require understanding the underlying LangChain code

## When to use it
- When you want a visual way to build and test LangChain-based LLM flows
- When non-technical users need to create or modify LLM pipelines

## When not to use it
- When you need full programmatic control or want to use a framework other than LangChain
- When the application is simple enough that a few lines of code suffice

## Related tools / concepts
- [Dify](dify.md)
- [LangFlow](https://github.com/langflow-ai/langflow)

## Getting started

Install Flowise globally via npm and start it:

```bash
# Install Flowise globally
npm install -g flowise

# Start Flowise
npx flowise start
```

Once running, you can access the UI at `http://localhost:3000`.

## API examples

### Calling a Flowise Chatflow via REST

You can interact with your deployed chatflows using the Prediction API.

```bash
curl -X POST "http://localhost:3000/api/v1/prediction/{your-chatflow-id}" \
     -H "Content-Type: application/json" \
     -d '{
            "question": "How do I set up a vector store in Flowise?",
            "overrideConfig": {
                "returnSourceDocuments": true
            }
         }'
```

## Sources / references
- [Official Website](https://flowiseai.com/)
- [GitHub Repository](https://github.com/FlowiseAI/Flowise)

## Contribution Metadata

- Last reviewed: 2026-03-01
- Confidence: medium

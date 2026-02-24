# Flowise

## What it is
Flowise is an open-source visual tool to build customized LLM orchestration flows and AI agents.

## What problem it solves
It provides a drag-and-drop interface for the LangChain framework, making it easier to visualize and build complex agentic chains without writing extensive code.

## Where it fits in the pipeline
**Reason / Orchestrate / Act**

## Typical use cases (in this homelab / family automation context)
- **Agent Prototyping**: Rapidly testing different tool combinations for a home automation agent.
- **Visual Chatbots**: Building a chatbot that can search through your local codebase or documentation.
- **Multi-Agent Systems**: Designing flows where multiple specialized agents collaborate on a task.

## Integration points
- **LangChain**: Directly uses LangChain components under the hood.
- **External Tools**: Connects to various search APIs, databases, and LLM providers.
- **Webhooks**: Can be triggered by or send data to external automation hubs like n8n.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free (Self-hosted)
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Extremely rapid development cycle for agentic flows.
- Visual debugging of complex chains.
- High modularity.

## Limitations
- Less flexible than pure code for extremely custom logic.
- Performance can be an issue for very large, complex flows.

## Alternatives / Related tools
- **Dify**
- **LangFlow**
- **LangChain** (Code-first)

## Links
- [Official Website](https://flowiseai.com/)
- [GitHub](https://github.com/FlowiseAI/Flowise)

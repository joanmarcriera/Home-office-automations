# Ollama

## What it is
Ollama is a tool that allows you to run open-source large language models (LLMs), such as Llama 3, Mistral, and Gemma, locally on your own machine.

## What problem it solves
It simplifies the process of downloading and running LLMs, removing the need for cloud subscriptions and ensuring your data never leaves your home network.

## Where it fits in the pipeline
**Reason / Act**

## Typical use cases (in this homelab / family automation context)
- **Local AI Assistant**: Providing a backend for local chat interfaces or home automation logic.
- **Privacy-First Summarization**: Summarizing sensitive family documents without uploading them to the cloud.
- **Code Assistance**: Serving as the backend for VS Code extensions like Continue or Aider.

## Related Playbooks
- [Email to Calendar](../../../playbooks/email-to-calendar.md)
- [AI-Assisted Dev Workflow](../../../playbooks/dev-workflow-ai-assisted.md)

## Integration points
- **OpenHands / Aider**: As a model provider for local development agents.
- **n8n**: Using the Ollama node for AI-powered workflow automation.
- **Paperless-AI**: Providing the reasoning engine for semantic search.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Extremely easy to install and use.
- Supports a wide variety of state-of-the-art open models.
- Efficient memory management and hardware acceleration support.

## Limitations
- Performance is limited by local hardware (GPU/RAM).
- Model quality for very complex reasoning may lag behind top-tier proprietary models.

## Alternatives / Related tools
- **LocalAI**
- **LM Studio**
- **vLLM**

## Links
- [Official Website](https://ollama.com/)
- [GitHub](https://github.com/ollama/ollama)

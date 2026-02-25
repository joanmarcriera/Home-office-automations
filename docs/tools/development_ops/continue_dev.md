# Continue.dev

## What it is
Continue is an open-source AI code assistant that allows you to use any LLM as a pair programmer inside VS Code and JetBrains.

## What problem it solves
Provides an open-source alternative to GitHub Copilot, giving users full control over which models they use (local or cloud) and how their data is handled.

## Where it fits in the pipeline
**Act (Development)**

## Typical use cases (in this homelab / family automation context)
- Using a local model via **Ollama** to assist with coding without sending data to the cloud.
- Building custom "slash commands" to automate repetitive homelab management tasks.

## Integration points
- **Ollama**: First-class support for local LLM usage.
- **LiteLLM**: For connecting to a variety of cloud model providers.
- **IDE Extensions**: Available for VS Code and JetBrains.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free (Software) + Model costs (if using cloud APIs)
- **Free tier**: N/A (Self-hosted/Plugin)
- **Self-hostable**: Yes (The assistant logic and local models)

## Strengths
- Transparent and customizable.
- Model agnostic.
- Strong support for local-first development.

## Limitations
- Requires more setup than "turnkey" alternatives.
- Local performance depends on user hardware.

## Alternatives / Related tools
- **GitHub Copilot**
- **Cursor**
- **Aider**

## Links
- [Official Website](https://continue.dev)
- [GitHub](https://github.com/continuedev/continue)

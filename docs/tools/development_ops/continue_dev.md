# Continue.dev

## What it is
An open-source AI code assistant that brings the power of LLMs to VS Code and JetBrains. It allows you to use any LLM (local via Ollama or remote via API) for code completion, chat, and editing.

## What problem it solves
Gives developers flexibility to choose their own LLM backend (including local models) for AI-assisted coding, avoiding vendor lock-in to a single provider.

## Where it fits in the stack
**Development & Ops**. Serves as an open-source, model-agnostic AI coding layer inside VS Code and JetBrains.

## Typical use cases
- AI code completion using local Ollama models
- Chat-based coding assistance with any LLM provider
- Multi-file editing with context from the repository

## Strengths
- Open source and model-agnostic
- Supports local LLMs via Ollama
- Available for both VS Code and JetBrains

## Limitations
- Requires configuration to connect to local or remote models
- Completion quality depends on the chosen model

## When to use it
- When you want AI code assistance with local LLMs (e.g., via Ollama)
- When you need an open-source alternative to proprietary coding assistants

## When not to use it
- When you prefer a turnkey, zero-configuration AI editor experience
- When you need a fully integrated AI-native editor (consider Cursor or Zed)

## Getting started

Continue is available as an extension for VS Code and JetBrains.

1. **Install**: Search for "Continue" in your IDE's extension marketplace.
2. **Configure**: Click the gear icon in the Continue sidebar to open `config.json`.
3. **Select Model**: Choose a provider (e.g., Ollama, Anthropic, OpenAI) to start chatting.

## Usage examples

### config.json with Ollama
Configure Continue to use a local model via Ollama:
```json
{
  "models": [
    {
      "title": "Ollama Llama 3",
      "provider": "ollama",
      "model": "llama3"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Starcoder 2",
    "provider": "ollama",
    "model": "starcoder2:3b"
  }
}
```

### Custom Slash Commands
Add custom behavior by defining slash commands in `config.json`:
```json
{
  "customCommands": [
    {
      "name": "test",
      "description": "Write a unit test for the selected code",
      "prompt": "Write a comprehensive unit test for this code using Jest: {{{ input }}}"
    }
  ]
}
```

## Related tools / concepts
- [Cursor](cursor.md)
- [Zed](zed.md)

## Sources / references
- [Official Website](https://www.continue.dev/)
- [GitHub Repository](https://github.com/continuedev/continue)

## Contribution Metadata

- Last reviewed: 2026-02-27
- Confidence: medium

# OpenAI Codex

## What it is
OpenAI's coding-specialized model line and related coding-agent surfaces. In current routing terms, this is the lane to use when the task is strongly code-centric rather than broad general reasoning.

## What problem it solves
Provides a specialized language model and tooling surface for code generation, editing, and implementation-oriented coding assistance.

## Where it fits in the stack
**Development & Ops**. Functions as the underlying model powering several AI coding assistants.

## Typical use cases
- Powering code completion tools (e.g., GitHub Copilot)
- Generating code from natural language descriptions
- Translating between programming languages
- Editing or refactoring an existing codebase
- Writing tests and implementation scaffolds

## Strengths
- Code-specialized behavior
- Useful when you want code editing bias rather than general chat behavior
- Strong fit for code generation, refactors, and test-writing loops

## Limitations
- Proprietary; no self-hosting option
- Not the best default for broad research, planning, or mixed non-code reasoning
- Should be treated as a specialized lane, not the universal default

## Model routing

Use `gpt-5.3-codex` when:
- the task is mostly code
- you want source-editing behavior
- you are building inside an IDE, CLI, or code agent flow

Do not use it when:
- the task is mainly research
- the task is business analysis with some incidental code
- you actually need the broader deliberate reasoning of GPT-5.4

Best pairings:
- default coding lane: [Anthropic Sonnet](../providers/anthropic.md)
- hard reasoning escalation: [OpenAI](../ai_knowledge/openai.md) with GPT-5.4 `high`
- central policy: [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## When to use it
- When using GitHub Copilot or other tools built on Codex
- When evaluating code-specialized models against general-purpose LLMs
- When the task is code-centric enough to justify a specialized coding lane

## When not to use it
- When you need a self-hosted or open-source code model
- When the task is not primarily code
- When a general reasoning model is better suited to the work

## Getting started

While Codex is primarily an API-based model, it can be used via CLI tools like `codex-cli` or similar wrappers.

```bash
# Install a Codex-compatible CLI wrapper
npm install -g codex-cli

# Set your OpenAI API Key
export OPENAI_API_KEY=your-key-here

# Run a simple query
codex "Create a python function to scrape a website"
```

## CLI examples

### codex with local models
Some wrappers allow redirecting Codex-style requests to local inference servers:
```bash
# Configure CLI to point to a local Ollama instance instead of OpenAI
codex config set base_url http://localhost:11434/v1
codex config set model codellama
```

### sandboxed execution
Run generated code in a restricted environment to prevent system damage. This is particularly useful for agents that can execute the code they generate:
```bash
# Execute with sandboxing flags (if supported by the CLI tool)
codex --execute --full-auto --sandbox=docker "Calculate the first 1000 prime numbers"

# Use with Open Interpreter for more advanced, automated sandboxed execution
# This allows the LLM to run code in a secure E2B or Docker container
interpreter --local --model codellama --sandbox
```

## Related tools / concepts
- [Llama 3 (Fine-tuned for code)](https://ollama.com/library/llama3)
- [StarCoder](https://github.com/bigcode-project/starcoder)
- [OpenAI](../ai_knowledge/openai.md)
- [Anthropic](../providers/anthropic.md)
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md)

## Sources / references
- [OpenAI Codex](https://openai.com/codex/)
- [OpenAI Models Overview](https://platform.openai.com/docs/models)

## Contribution Metadata

- Last reviewed: 2026-03-15
- Confidence: medium

# Promptfoo

## What it is
Promptfoo is an open-source CLI tool and library for evaluating, testing, and securing LLM prompts and models. It allows you to run systematic test cases across multiple providers and models.

## What problem it solves
It solves the problem of "prompt regression" by providing a framework for regression testing. It allows you to quantify how changes to a prompt affect output quality across many different test cases.

## Where it fits in the stack
**Benchmarking / Eval**.

## Typical use cases
- **Prompt Comparison**: Testing the same input against 10 different versions of a prompt.
- **Model Comparison**: Testing the same prompt against GPT-4o, Claude 3.5, and Llama 3.1.
- **CI/CD Integration**: Automatically running a test suite before deploying a prompt change.
- **Security Testing**: Running "jailbreak" or "injection" tests against prompts.

## Strengths
- **Fast and Local**: Runs entirely on your machine; no external platform required.
- **Flexible Assertions**: Support for JS, Python, and LLM-graded assertions.
- **Extensive Provider Support**: Works with OpenAI, Anthropic, Ollama, LocalAI, and more.

## Limitations
- **CLI-First**: While it has a web viewer, the core experience is command-line based.
- **Setup Effort**: Requires defining test cases in YAML or JSON.

## When to use it
- To systematically improve the reliability of your LLM prompts.
- To prevent regressions when updating models or prompts in an automation workflow.

## When not to use it
- For one-off, casual chats with an LLM.

## Getting started

Initialize a new project:
```bash
npx promptfoo init
```

Run an evaluation:
```bash
npx promptfoo eval
```

View results:
```bash
npx promptfoo view
```

## Licensing and cost
- **Open Source**: Yes (MIT).
- **Cost**: Free.
- **Self-hostable**: Yes.

## Related tools / concepts
- [Braintrust](../process_understanding/braintrust.md)
- [LangSmith](langsmith.md)
- [OpenCompass](opencompass.md)

## Sources / References
- [Official Website](https://www.promptfoo.dev/)
- [Promptfoo GitHub](https://github.com/promptfoo/promptfoo)

## Contribution Metadata
- Last reviewed: 2026-05-06
- Confidence: high

# Sourcegraph Cody

## What it is
Cody is an AI coding assistant from Sourcegraph that uses your entire codebase for context to help you write and understand code.

## What problem it solves
It specializes in "code graph" awareness, meaning it has a deep understanding of how different parts of your repository relate to each other, leading to more accurate answers.

## Where it fits in the pipeline
**Act (Development)**

## Typical use cases (in this homelab / family automation context)
- Asking questions about how a specific home automation service interacts with other parts of the system.
- Generating unit tests that respect existing project patterns.

## Integration points
- **Sourcegraph**: Works best when combined with Sourcegraph's code search capabilities.
- **IDE Extensions**: VS Code, IntelliJ.
- **LLMs**: Can use Anthropic's Claude, OpenAI's GPT, etc.

## Licensing and cost
- **Open Source**: The core extension is open source.
- **Cost**: Freemium
- **Free tier**: Yes (Limited queries)
- **Self-hostable**: Yes (via Sourcegraph instance)

## Strengths
- Excellent codebase context retrieval.
- Transparent reasoning process.
- Integration with powerful code search.

## Limitations
- Best experience requires a Sourcegraph backend.

## Alternatives / Related tools
- **Cursor**
- **GitHub Copilot**

## Links
- [Official Website](https://sourcegraph.com/cody)
- [GitHub](https://github.com/sourcegraph/cody)

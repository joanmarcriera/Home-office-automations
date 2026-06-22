# GPT Engineer

## What it is
GPT Engineer is an AI tool that can build entire applications from a single prompt. It focuses on the "bootstrapping" phase of development, where it asks clarifying questions to refine requirements before generating a complete, functional codebase. As of June 2026, **v2.x** has introduced deep integration with **WebContainer** technology, allowing for real-time, full-stack previews directly in the browser.

## What problem it solves
Reduces the time to bootstrap a new project by generating a complete codebase from a natural language description. It solves the "configuration hell" and boilerplate overhead associated with starting new applications, specifically optimized for prototypes, MVPs, and rapid full-stack iteration using the latest June 2026 framework standards.

## Where it fits in the stack
**Development & Ops**. Functions as an AI-driven project scaffolding and code generation tool. It is often the first tool used in the "Software Factory" pipeline, bridging the gap between initial ideation and a functional, previewable application.

## Typical use cases
- **Rapid Prototyping**: Generating a full project codebase from a single intent.
- **Full-stack Previews**: Using WebContainer integration to see a running version of the app immediately after generation.
- **Microservices Scaffolding**: Generating boilerplate for complex microservices with standardized API contracts.
- **Architectural Exploration**: Quickly generating variations of a project to compare different framework approaches.

## Strengths
- **End-to-end Generation**: Creates complete, runnable projects rather than just snippets.
- **Iterative Logic**: Interactive clarifying questions significantly improve output quality compared to "one-shot" generators.
- **WebContainer Integration**: Native support for in-browser execution and preview of generated full-stack apps.
- **Open Source**: Transparent logic and community-driven improvements.
- **v2.x Performance**: Optimized for frontier models like Claude 4.8 and GPT-5.5, ensuring higher-fidelity architectural decisions.

## Limitations
- **Maintenance**: Generated code can be difficult to maintain if the logic is complex or non-standard.
- **Hallucinations**: Like all LLM tools, it may occasionally use deprecated libraries or invent non-existent APIs.
- **Scalability**: Best suited for small-to-medium projects; large-scale systems still require significant manual architectural design.
- **Compute Intensity**: Full-stack generation and WebContainer previews require significant client-side resources.

## When to use it
- When bootstrapping a new project from scratch (Greenfield development).
- When rapid prototyping is more important than production-hardened code.
- For learning new frameworks by seeing how the AI structures a project.
- When you need a "live" preview of a generated application immediately.

## When not to use it
- When making incremental changes to an existing codebase (use [Aider](aider.md) or [Plandex](plandex.md) instead).
- When precise, enterprise-grade control over code structure and security is required from day one.
- For high-security applications where AI-generated code must undergo rigorous manual auditing.

## Getting started
### Installation
GPT Engineer v2.x can be installed via pip or run directly via npx for the latest web-based features.

```bash
# Install via pip
pip install gpt-engineer

# Or run via npx for WebContainer-enabled projects
npx gpt-engineer
```

### Basic Workflow
1. **Create a project folder**: `mkdir my-app && cd my-app`
2. **Initialize**: `gpt-engineer .`
3. **Prompt**: Enter your requirements when prompted (e.g., "A React-based dashboard for home energy monitoring").

## CLI examples
### Project Generation
```bash
# Generate a project in the current directory using a specific model
gpt-engineer . --model claude-4.8-opus
```

### Clarification Mode
```bash
# Force the clarification loop to ensure detailed specs
gpt-engineer . --steps clarify
```

### Headless Generation
```bash
# Run without interactive prompts for CI/CD pipelines
gpt-engineer . --prompt "A FastAPI backend for a book inventory" --no-interactive
```

## API examples
### Programmatic Initialization (Python)
```python
from gpt_engineer.core.ai import AI
from gpt_engineer.core.steps import gen_code

def build_app(prompt_text):
    ai = AI(model_name="gpt-5.5-preview")
    # Execute the generation steps
    dbs = gen_code(ai, prompt_text)
    return dbs.workspace.path

if __name__ == "__main__":
    path = build_app("A simple todo app using Flask and SQLite")
    print(f"App generated at: {path}")
```

### WebContainer Preview Hook (JavaScript)
```javascript
import { GPTEngineer } from '@gpt-engineer/sdk';

const gpte = new GPTEngineer({ apiKey: 'your-api-key' });

async function generateAndPreview() {
  const project = await gpte.generate("A portfolio site for a photographer");
  // The SDK automatically handles the WebContainer mounting
  await project.preview();
}
```

## Related tools / concepts
- [Plandex](plandex.md) — For complex, multi-step code migrations.
- [OpenHands](openhands.md) — Autonomous agentic platform for general tasks.
- [Codeium](codeium.md) — Real-time AI autocomplete and refactoring.
- [Aider](aider.md) — Terminal-based pair programming and editing.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — The architectural pattern for automated code generation.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns for multi-step AI tasks.
- [Claude Code](claude-code.md) — High-fidelity interactive coding agent.
- [WebContainer API](https://webcontainers.io/) — The underlying technology for in-browser previews.

## Sources / references
- [GPT Engineer GitHub Repository](https://github.com/AntonOsika/gpt-engineer)
- [Official Documentation](https://gpt-engineer.readthedocs.io/)
- [WebContainer Integration Guide](https://gpt-engineer.readthedocs.io/en/latest/webcontainers.html)
- [GPT Engineer v2.0 Release Notes](https://github.com/AntonOsika/gpt-engineer/releases/tag/v2.0.0)

## Contribution Metadata
- Last reviewed: 2026-06-22
- Confidence: high

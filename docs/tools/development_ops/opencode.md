# Oh My OpenAgent (OmO) / oh-my-opencode

## What it is
Operating under the SUL 1.0 license, it provides a powerful developer cockpit, combining local developer servers, AST analyzers, and agent planners to convert terminal prompts into high-success-rate edits. As of early 2027, OmO features full support for **FastMCP 3.1**, stateful agent loops, and frontier models including [Claude 5.6](../providers/anthropic.md), [GPT-5.6](../providers/openai.md), [Gemini 4.0 Ultra](../ai_knowledge/gemini.md), [DeepSeek-V4](../ai_knowledge/local_llms.md), [Qwen 3.8](../ai_knowledge/qwen.md), and [Llama 4](../ai_knowledge/local_llms.md).

## What problem it solves
It tackles the "harness problem" in AI engineering, where advanced reasoning models fail not due to intelligence limitations, but because they are bottlenecked by low-fidelity shell interactions, poor context caching, or rigid file-editing APIs. OmO provides programmatic safeguards, including AST-guided syntax validations, multi-threaded codebase indexing, and multi-model consensus routing. This ensures that agents running on **Claude 5.6**, **GPT-5.6**, **DeepSeek-V4**, **Llama 4**, or **Qwen 3.8** execute modifications with high precision.

## Where it fits in the stack
**Development & Ops / Agent Harness Layer**. OmO represents an open, customizable, terminal-based alternative to proprietary "walled garden" developer engines like [Claude Code](claude-code.md), cursor-based IDEs, or [Windsurf](windsurf.md).

## Typical use cases
- **Multi-File Structural Refactoring**: Decomposing monolithic backend directories into micro-libraries using automated AST modifications.
- **Autonomous Feature Delivery**: Initiating `ultrawork` execution loops that plan changes, write unit tests, run lints, and perform self-healing until code passes validation.
- **Deep Codebase Diagnostics**: Querying complex repository patterns using LSP-integrated semantic search models to root-cause intermittent test failures.
- **Standardized Context Management**: Setting up deep, hierarchical `AGENTS.md` boundaries across directories to provide localized rules to downstream agents.

## Key Agents (The Sisyphus Team)
OmO features a specialized multi-agent division of labor called the **Sisyphus Team**:
- **Sisyphus**: The master coordinator. Evaluates intermediate outputs, manages states, and drives execution until tasks are validated.
- **Hephaestus**: The heavy-lifting compiler and developer. Explores directory layouts and applies localized search-and-replace edits using AST hashing algorithms.
- **Prometheus**: The architect and requirement collector. Interviews developers on complex prompts to construct unambiguous execution plans.
- **Oracle**: The deep reasoner. Solves complex logical bottlenecks, validates code syntax, and analyzes runtime errors.
- **Librarian**: The contextual database manager. Retrieves relevant code blocks and parses local `AGENTS.md` rules.
- **Explore**: The external search researcher. Uses Exa and other search FastMCP engines to look up package documentation or API specifications.

## Strengths
- **Surgical Code Editing**: Employs structural code hashing to apply edits precisely, avoiding line-drift errors common in simple regex-based replacements.
- **Multi-Provider Consensus**: Supports routing tasks to the best-suited model engine (e.g., calling **Claude 5.6** for reasoning, and **Qwen 3.8** for rapid syntax generation).
- **First-Class FastMCP 3.1 Protocols**: Seamlessly hosts Model Context Protocol (FastMCP 3.1) servers to grant agents access to terminal commands, databases, and memory engines.
- **Advanced AST and LSP Integration**: Uses `ast-grep` and Language Server Protocols (LSP) to perform type-aware edits and semantic symbol searches.
- **Fully Self-Hostable**: Free from vendor lock-in; connects to local model infrastructures like [Llama 4](../ai_knowledge/local_llms.md) via llama.cpp or Ollama.

## Limitations
- **Substantial Initial Setup**: Requires managing and configuring API keys for multiple providers to achieve optimal performance.
- **High Token Consumption**: Running complex multi-agent parallel loops can consume a high volume of input and output tokens.
- **Exclusively Terminal-Centric**: Lacks a primary visual graphical editor, making it less appealing to developers who prefer GUI-focused IDEs.

## When to use it
- When implementing extensive, multi-file code modifications that require semantic type awareness.
- When building a fully open, self-hosted AI developer environment using local open-weight model architectures.
- For complex software migration tasks where agents must compile, test, and resolve issues autonomously.

## When not to use it
- For quick, single-file edits or simple script creations where a direct web-chat client is faster to access.
- If your environment requires a full-fledged visual GUI or deep, out-of-the-box VS Code extensions.
- In low-bandwidth or cost-constrained situations where running parallel agent loops is too expensive.

## Getting started

### Installation
Install the Oh My OpenAgent CLI globally via your preferred package manager (Node or Bun environments):

```bash
npm install -g oh-my-opencode
```

### Initializing the Repository Workspace
Generate standard hierarchal agent instruction files and index symbols in your target project directory:

```bash
/init-deep
```

### Running Basic Queries
Initiate a single-shot terminal request with your active developer model:

```bash
omo "Review our standard testing files and summarize current coverage gaps"
```

## CLI examples

### Starting an Autonomous Coding Loop
Initialize the `ultrawork` loop to implement a feature, run tests, and self-heal automatically:

```bash
ultrawork "Implement an authenticated web-hook receiver with signature verification"
```

### Starting an Architecture Interview
Launch an interactive planning session with Prometheus to gather project context and design specifications:

```bash
/start-work
```

### Executing an Uninterrupted Recovery Loop
Run a continuous self-healing loop to fix linting, formatting, or compiler errors:

```bash
/ulw-loop "Analyze all build output errors and resolve them"
```

### Troubleshooting the Installation
Perform a local diagnostics check to verify API keys, LSP connections, and MCP settings:

```bash
bunx oh-my-opencode doctor
```

## API examples

### Python Automation Wrapper with Pydantic v2
Executing OmO CLI tasks programmatically and parsing execution manifests using Pydantic v2:

```python
import subprocess
import json
from pydantic import BaseModel, Field

class OmoExecutionReport(BaseModel):
    task_id: str = Field(description="Unique task execution ID")
    status: str = Field(description="Execution status (success/failure)")
    modified_files: list[str] = Field(default_factory=list, description="List of files modified by OmO")
    summary: str = Field(description="Task execution summary")

def run_omo_task(prompt: str) -> OmoExecutionReport:
    cmd = ["omo", "--json", prompt]
    # Simulated execution response for illustration
    mock_output = json.dumps({
        "task_id": "omo-2027-8891",
        "status": "success",
        "modified_files": ["src/auth/webhook.py", "tests/test_webhook.py"],
        "summary": "Implemented HMAC signature verification for incoming webhooks."
    })
    data = json.loads(mock_output)
    return OmoExecutionReport(**data)

report = run_omo_task("Implement HMAC signature verification")
print(report.model_dump_json(indent=2))
```

### FastMCP 3.1 Integration Example
TypeScript API snippet for integrating OmO tasks into FastMCP servers:

```typescript
import { Sisyphus } from "oh-my-openagent/core";

async function runAutomation() {
  // Construct a detailed planning task
  const task = await Sisyphus.plan({
    instruction: "Refactor core database connection layers to utilize modern connection pooling",
    workspace: "./src/db"
  });

  // Execute the planning, compiling, and validation stages autonomously
  const executionReport = await task.execute();
  console.log(`Task status: ${executionReport.success ? 'Success' : 'Failure'}`);
}

runAutomation();
```

## Related tools / concepts
- [Aider](aider.md) — Terminal-centric Git-integrated editing assistant.
- [Claude Code](claude-code.md) — Anthropic's agentic command-line developer.
- [Windsurf](windsurf.md) — Multi-agent developer IDE.
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md) — Open tool-calling protocol.
- [OpenHands](openhands.md) — Browser-based open-source software agent framework.
- [Llama 4](../ai_knowledge/local_llms.md) — State-of-the-art open-weights model engine.
- [Claude](../providers/anthropic.md) — SOTA model developer interface.
- [Gemini](../ai_knowledge/gemini.md) — Multimodal foundation model family.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Industry-standard agent design patterns.

## Sources / references
- [Oh My OpenAgent Project Codebase on GitHub](https://github.com/code-yeongyu/oh-my-openagent)
- [The Harness Problem: Why Agent Interfaces Matter](https://blog.can.ac/2026/02/12/the-harness-problem/)
- [Oh My OpenCode Developer Documentation Hub](https://opencode.ai/docs/)
- [FastMCP 3.1 & MCP 3.0 Task Protocol Specification](https://modelcontextprotocol.io/spec/3.0)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

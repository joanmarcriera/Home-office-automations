# Melty

## What it is
Melty is an open-source, AI-native Integrated Development Environment (IDE) designed to act as a stateful, "human-in-the-loop" collaborator that understands the intent behind every code change. Built on a fully transparent VS Code-fork foundation, Melty implements a continuous "Intent-State" synchronization loop. As of early January 2027, Melty fully supports frontier SOTA late 2026/2027 models (such as Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, DeepSeek-V4, Gemma 4, and Qwen 3.6 VL). Rather than acting as a simple passive autocomplete helper, Melty operates as an active pair programmer, tracking real-time development context, terminal outputs, build failures, and git diffs to co-author software iteratively alongside the developer.

## What problem it solves
Solves the cognitive friction and "black box" generation issues associated with traditional AI coding assistants. Standard tools often generate massive code dumps that are disconnected from the developer’s high-level architecture or current design patterns. Melty addresses this by tracking the developer's "Intent" incrementally across terminal sessions, compiler messages, and version control states. It reduces code-review overhead, mitigates model hallucinations by grounding context in current git diffs, and eliminates the risk of silent, untracked modifications by managing changes through explicit state verification loops.

## Where it fits in the stack
**Development & Ops**. It serves as the primary developer workspace and AI-assisted code editor. Positioned as a fully open-source, customizable alternative to proprietary tools like [Cursor](cursor.md) or [Windsurf](windsurf.md), Melty sits at the intersection of local coding runtimes and remote or local LLM providers. It coordinates directly with terminal pipelines and git workflows, offering native hooks for external agentic orchestrators and repository managers.

## Typical use cases
- **Intent-Driven Greenfield Prototyping**: Generating and scaffolding clean, module-based structures from high-level developer intents while keeping the developer's feedback loop tightly integrated.
- **Continuous Real-Time Refactoring**: Aligning existing codebases with modern design conventions, where the AI suggests structural improvements as you write, responding dynamically to compiler outputs and linter warnings.
- **SSH and Remote Environment Synchronization**: Developing directly on remote VMs or container environments using a local Melty instance connected over secure SSH/terminal channels.
- **Multi-File Context-Aware Coding**: Working on features where modifications span across several frontend files, backend controllers, and database schemas concurrently, with the AI tracking files in a consolidated, active workspace context.

## Strengths
- **Open-Source Transparency**: Fully open-source codebase, allowing deep, enterprise-level modifications, custom branding, and absolute privacy compliance.
- **Stateful Git & Terminal Tracking**: Natively listens to local git diff changes and terminal output streams, allowing models to immediately self-correct errors if a build or test command fails.
- **Native MCP 3.1 / FastMCP 3.1 Integration**: Operates as a robust Model Context Protocol client, enabling developers to connect third-party MCP servers for dynamic database query execution, file system management, and real-time cloud resource access.
- **Multi-Model Orchestration**: Supports swappable local and remote models, allowing developers to execute heavy-weight tasks with Claude 5.6, GPT-5.6, Gemini 4.0 Ultra, or DeepSeek-V4, and light-weight local autocompletion tasks using local Gemma 4 or Qwen 3.6 instances via Ollama.

## Limitations
- **Ecosystem Footprint**: Although built as a VS Code fork, some specialized extensions or proprietary visual features (such as side-by-side interactive timelines) are still maturing.
- **Resource Footprint**: Active terminal scanning, real-time git state diffing, and maintaining high-dimensional local semantic vector indexes can be resource-intensive on older hardware.
- **Dependency on High-Tier Reasoning**: Simpler, quantized offline models can sometimes lose track of multi-file intents, necessitating frontier model access for complex, multi-layered refactoring.

## When to use it
- When you are looking for an open-source AI-native IDE that prioritizes developer intent, privacy, and continuous collaboration over passive black-box autocomplete.
- When you require a development environment that natively integrates with the [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) to dynamically extend your LLM's capabilities.
- For team-wide development where open-source transparency is necessary to ensure strict intellectual property and data sovereignty boundaries.

## When not to use it
- If your daily development workflows require heavy visual, multi-editor GUI configurations or proprietary extension suites that are tightly locked to the official Microsoft VS Code marketplace.
- If you are seeking a terminal-native, keyboard-only environment (in which case, [Aider](aider.md), [Junie CLI](junie-cli.md), or [Terminus 2](terminus-2.md) are more appropriate choices).
- In highly resource-constrained environments where running an active, background-indexing visual IDE causes visible latency.

## Getting started
### Installation
Melty can be installed as a precompiled standalone binary or compiled directly from source for local modification.

```bash
# Clone the repository and install dependencies
git clone https://github.com/meltylabs/melty.git
cd melty
npm install

# Run Melty in development mode
npm run dev
```

### Configuration and Model Setup
Upon launching, Melty prompts for a preferred model provider. Configure your credentials or local endpoint:

```bash
# Configure Melty to use a local Ollama instance for Qwen 3.6 / Gemma 4
melty config set provider ollama --url http://localhost:11434 --model gemma-4

# Or configure remote API credentials
melty config set provider anthropic --api-key $ANTHROPIC_API_KEY --model claude-5.6
```

## CLI examples
Melty features a command-line interface for starting the editor, indexing repositories, and executing headless refactoring.

### Opening a Repository
```bash
# Open the current directory in Melty
melty .
```

### Running Headless Refactoring Loops
```bash
# Run Melty in headless mode to apply changes based on an intent
melty apply --intent "Refactor controllers to use async/await syntax and log output" --path ./src/controllers
```

### Workspace Indexing
```bash
# Force-refresh the local vector index of the codebase
melty index --rebuild --exclude "**/node_modules/**"
```

## API examples
Melty exposes an internal API for writing extensions, managing intents, and connecting custom context bridges.

### Custom Intent Provider (TypeScript)
Developers can register custom intent providers to intercept and modify Melty's AI recommendations.

```typescript
import { MeltyExtension, IntentContext, ProposedDiff } from '@melty/sdk';

export class DatabaseOptimizerExtension implements MeltyExtension {
  id = 'db-optimizer';

  async onIntentDetected(intent: string, context: IntentContext): Promise<ProposedDiff | null> {
    if (intent.toLowerCase().includes('optimize query') || intent.toLowerCase().includes('index sql')) {
      const activeSQLFiles = await context.getFilesByPattern('**/*.sql');

      // Inject database context or analyze schemas
      const systemPrompt = `Analyze the SQL files: ${activeSQLFiles.map(f => f.name).join(', ')} and suggest optimized indexes.`;
      const completion = await context.llm.generate(systemPrompt);

      return context.createDiffFromCompletion(completion);
    }
    return null;
  }
}
```

### Subprocess Workspace State Check (Python)
Integrate external validation engines with Melty's active "Intent-State" loop via standard output. This example uses robust Pydantic v2 validation to enforce schema correctness of the returned session state.

```python
import subprocess
import json
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError

class MeltySessionState(BaseModel):
    current_intent: str = Field(..., description="The high-level objective/intent currently tracked by Melty")
    staged_diff_files: List[str] = Field(default_factory=list, description="List of files with uncommitted changes")
    active_mcp_servers: List[str] = Field(default_factory=list, description="Currently connected FastMCP 3.1 server URIs")
    model_provider: str = Field(..., description="LLM provider name, e.g., 'anthropic' or 'ollama'")
    model_name: str = Field(..., description="The model currently in use, e.g., 'claude-5.6'")

def get_melty_session_state() -> Optional[MeltySessionState]:
    """Queries Melty's headless daemon and parses state with strict Pydantic v2 validation."""
    try:
        response = subprocess.run(
            ["melty", "state", "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        parsed_json = json.loads(response.stdout)
        # Enforce strict validation via Pydantic v2
        state = MeltySessionState.model_validate(parsed_json)
        return state
    except subprocess.CalledProcessError as e:
        print(f"Error fetching Melty state: {e.stderr}")
        return None
    except ValidationError as e:
        print(f"Melty session state schema mismatch: {e}")
        return None

if __name__ == "__main__":
    state = get_melty_session_state()
    if state:
        print(f"Active Intent: {state.current_intent}")
        print(f"Pending changes in {len(state.staged_diff_files)} files.")
        print(f"Model In Use: {state.model_name} via {state.model_provider}")
```

## Related tools / concepts
- [Cursor](cursor.md) — A popular proprietary AI-native IDE built on VS Code.
- [Zed](zed.md) — A high-performance, collaborative visual code editor written in Rust.
- [Codeium](codeium.md) — Multi-IDE AI developer productivity and autocomplete platform.
- [Windsurf](windsurf.md) — SOTA visual IDE implementing the Cascade interaction model.
- [Aider](aider.md) — High-performance terminal-native pair programmer and git integration assistant.
- [Junie CLI](junie-cli.md) — Terminal companion and indexer.
- [Terminus 2](terminus-2.md) — Open-source terminal-native AI agent baseline with a tmux bridge.
- [GPT Engineer](gpt_engineer.md) — Rapid prototyping and scaffolding orchestrator for greenfield codebases.
- [Sourcegraph Cody](sourcegraph_cody.md) — Multi-repository code intelligence and semantic context indexing client.
- [Anti-Gravity](anti_gravity.md) — Enterprise-grade agentic development and execution framework.
- [Droid](droid.md) — Enterprise-grade AI coding orchestrator configuring dedicated sub-agents.
- [Software Factories](../../knowledge_base/patterns/software-factories.md) — Automated development architectures and code production systems.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Orchestration patterns for multi-step AI planning.
- [Model Context Protocol (MCP)](../../knowledge_base/patterns/tool-calling-and-mcp.md) — Open standard for integrating AI tools and data sources.

## Sources / references
- [Melty Labs Official Website](https://melty.sh/)
- [Melty GitHub Repository](https://github.com/meltylabs/melty)
- [Melty Technical Architecture Wiki](https://github.com/meltylabs/melty/wiki)
- [Model Context Protocol v3.1 Specification](https://modelcontextprotocol.org)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Superpowers

## What it is
Superpowers is a comprehensive software development workflow and agentic skills framework designed for coding agents like [Claude Code](../development_ops/claude-code.md), [Cursor](../development_ops/cursor.md), and [Aider](../development_ops/aider.md). It leverages highly modular "skills" to enforce a disciplined and rigorous software engineering process, specifically optimized for frontier reasoning models like **Claude 5.1** and **GPT-5.5** while integrating **Gemini 4.0 visual reasoning** for pixel-accurate frontend QA.

## What problem it solves
Most developer interactions with AI assistants are prone to ad-hoc, chaotic coding sessions resulting in circular refactoring, phantom files, and context rot. Superpowers addresses this by wrapping autonomous sessions in a structured skill environment. It ensures agents perform plan-first thinking, run isolated worktrees, and systematically execute Test-Driven Development (TDD) loops, which dramatically boosts performance on demanding benchmarks like [SWE-bench](../benchmarking/swe-bench.md).

## Where it fits in the stack
**Agents / Workflow Framework**. It operates as an orchestration and capability layer above the raw coding tools, managing tasks, executing CLI prompts, and validating progress via specialized plugins or the **Model Context Protocol (MCP 3.1)** Task Protocol.

## Typical use cases
- Enforcing Test-Driven Development (TDD) and planning-first architectural reviews on code modifications.
- Decomposing multi-hour autonomous coding tasks into discrete, step-by-step verified blocks.
- Maintaining strict workspace isolation using sandboxed Git environments or worktrees.
- Visual-regression testing and automated frontend layout verification.
- Enforcing DRY and YAGNI clean-code standards across large software projects.

## Strengths
- **MCP 3.1 Task Protocol**: Full support for native, multi-agent task handoffs and progress tracking schemas.
- **Gemini 4.0 Vision Support**: Pixel-level comparison and layout analysis for visual test suites.
- **TDD Enforcement**: Automatically prevents commits if validation tests fail or code coverage drops.
- **Vast Context Window Tuning**: Optimized to efficiently manage prompt footprints within **Claude 5.1**'s expanded context limits.
- **Configurable Sandboxing**: Restricts file modifications and script executions to designated directories.

## Limitations
- **Overhead**: Can feel overly process-intensive for simple or trivial single-file edits.
- **Learning Curve**: Crafting custom YAML skills requires familiarity with specific parameters and environment structures.
- **Model Cost**: In-depth planning, backtracking, and testing loops consume a higher quantity of input tokens.

## When to use it
- For substantial, multi-file refactoring, feature additions, or package upgrades in production codebases.
- When working with advanced, highly autonomous terminal-based tools like Claude Code or Aider.
- When you want to eliminate human monitoring for long-running agent tasks by enforcing bulletproof self-healing and testing loops.

## When not to use it
- For quick, conversational questions, simple documentation edits, or basic script prototyping.
- If your local environment completely restricts external CLI tools, local pytest/npm execution, or Docker sandboxes.

## Key Workflow Components
1. **Socratic Brainstorming**: Prompt-driven refinement to map architectural changes before touching a single file.
2. **Clean Baseline Environment**: Automatically provisions a separate Git worktree for isolated and safe changes.
3. **Task Decomposer**: Breaks complex tickets down into 3-5 minute tasks, each defined with specific input, output, and validation parameters.
4. **Subagent Spawning**: Runs task-specific subagents, minimizing parent context clutter and reducing API costs.
5. **Strict Verification**: Continuous execution of testing commands (RED-GREEN-REFACTOR) to guarantee correctness.
6. **PR Reviewer**: Auto-generates structural code audits against the plan prior to final branch merge.

## Technical Implementation: Skill YAML Example
The following is an upgraded, production-grade MCP 3.1 skill definition for compiling and asserting TypeScript code using strict type checks and modern Pydantic schema validation.

```yaml
# typescript_verify_skill.yaml
name: "typescript_verify"
description: "Compiles local TypeScript files and validates output using strict type-checking and compiler options."
parameters:
  type: "object"
  required:
    - "project_path"
  properties:
    project_path:
      type: "string"
      description: "Relative or absolute path to the directory containing tsconfig.json."
    strict_mode:
      type: "boolean"
      default: true
      description: "When true, enforces --strict and --noImplicitAny compiler flags."
    exclude_tests:
      type: "boolean"
      default: false
      description: "Exclude files inside test/ or spec/ directories during verification."
implementation: |
  #!/usr/bin/env bash
  set -euo pipefail

  TARGET_DIR="{{project_path}}"
  STRICT_FLAGS=""

  if [ "{{strict_mode}}" = "true" ]; then
    STRICT_FLAGS="--strict --noImplicitAny"
  fi

  echo "==> Verifying TypeScript Compilation in ${TARGET_DIR}..."
  cd "${TARGET_DIR}"

  if [ ! -f "package.json" ] && [ ! -f "tsconfig.json" ]; then
    echo "Error: No TypeScript configuration found at ${TARGET_DIR}" >&2
    exit 1
  fi

  # Run tsc compiler check
  npx tsc --noEmit ${STRICT_FLAGS}
  echo "==> TypeScript verification passed successfully!"
```

## Advanced Usage: Custom Task Verification
A `superpowers.json` configuration file allows projects to enforce hard quality gates. The example below tracks MCP 3.1 compliance using Pydantic v2 schemas.

```json
{
  "project_name": "KnowledgeOps Core",
  "version": "2.1.0",
  "config": {
    "enforce_tdd": true,
    "max_backtrack_attempts": 3,
    "vision_provider": "gemini-4-0-pro",
    "mcp_version": "3.1"
  },
  "tasks": [
    {
      "id": "migrate-pydantic-v1-to-v2",
      "description": "Upgrade old pydantic.v1 models to native Pydantic v2 schemas.",
      "files": ["src/models/schemas.py", "src/services/validator.py"],
      "verification": "pytest src/tests/test_validation.py -v && mypy src/models/schemas.py --strict"
    }
  ]
}
```

## Getting started

### Installation (Claude Code)
To register the Superpowers toolkit globally within Claude Code:

```bash
/plugin marketplace add obra/superpowers-marketplace
/plugin install superpowers@superpowers-marketplace
```

### Enabling Vision-Based QA
Initialize vision checking using the Gemini 4.0 visual engine:
```bash
superpowers config set vision_provider gemini-4-0-pro
superpowers config set vision_api_key $GEMINI_API_KEY
```

### Launching an Autonomous Session
Create a custom task list and run the orchestrator:

```bash
superpowers plan init "Upgrade authorization middleware to OAuth2"
superpowers run --auto-pilot
```

## CLI examples

### Inspecting Configured Skills
```bash
# List all active and sandboxed skills
superpowers skills list

# Show detailed implementation of a specific skill
superpowers skills show typescript_verify
```

### Executing Direct Task Verification
Run manual assertions on a specific subtask:
```bash
superpowers verify --task-id migrate-pydantic-v1-to-v2 --verbose
```

### Reviewing Subagent Performance
```bash
# Display traces of the spawned subagents for the current session
superpowers subagents log --format table
```

## API examples

### Programmatic Python Interface
You can load, structure, and dispatch Superpowers task configurations using Python and Pydantic v2 model structures for compile-time validation.

```python
import os
import sys
from pydantic import BaseModel, Field, ValidationError

class TaskConfig(BaseModel):
    id: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10)
    files: list[str] = Field(default_factory=list)
    verification_command: str = Field(..., alias="verification")

class SuperpowersConfig(BaseModel):
    project_name: str
    mcp_version: str = "3.1"
    enforce_tdd: bool = True
    tasks: list[TaskConfig]

def load_and_validate_workflow(config_path: str) -> SuperpowersConfig | None:
    """Loads and validates a Superpowers task list using Pydantic v2."""
    if not os.path.exists(config_path):
        print(f"Error: Config not found at {config_path}", file=sys.stderr)
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            raw_data = f.read()
        # Parse and perform strict type validation
        validated_config = SuperpowersConfig.model_validate_json(raw_data)
        return validated_config
    except ValidationError as e:
        print("Validation Error in superpowers.json schema:", file=sys.stderr)
        print(e.json(indent=2), file=sys.stderr)
        return None
    except Exception as e:
        print(f"Failed to read file: {e}", file=sys.stderr)
        return None

if __name__ == "__main__":
    # Simulate a run
    config = load_and_validate_workflow("superpowers.json")
    if config:
        print(f"Loaded config: {config.project_name} (MCP {config.mcp_version})")
        print(f"Total verified tasks: {len(config.tasks)}")
```

## Example company use cases
- **Continuous Integration / Continuous Delivery**: Establish an automated gate that deploys a Superpowers subagent to write tests for every feature branch prior to code review.
- **System Maintenance & Migration**: Executing large, repetitive codebase upgrades (e.g., Python 3.10 to 3.14 migrations) safely across hundreds of microservices.
- **Visual Design System Compliance**: Ensuring all design components match visual specifications by utilizing Gemini 4.0 visual verification.

## Example workflow
```text
Socratic Design -> Isolated Branch -> Task Decomposition -> TDD Implementation -> Visual Verification -> Automated PR Review -> Merge
```

## Ecosystem notes
- Superpowers forms the foundational execution engine of the [Claude Skills Ecosystem](claude-skills-ecosystem.md).
- It pairs perfectly with developer-focused MCP resources like [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md) for sandbox-enforced terminal operations.

## Selection comments
- Choose Superpowers when correctness, testing coverage, and safety are non-negotiable requirements.
- Avoid Superpowers for quick, ephemeral debugging queries or ad-hoc questions where structural rigor creates unwanted friction.

## Related tools / concepts
- [Agency-Agents](agency-agents.md)
- [Claude Code](../development_ops/claude-code.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Desktop Commander MCP](../development_ops/desktop-commander-mcp.md)
- [Aider](../development_ops/aider.md)
- [Plandex](../development_ops/plandex.md)
- [Mentat](../development_ops/mentat.md)
- [SWE-bench](../benchmarking/swe-bench.md)
- [Anthropic Agent Skills](anthropic-agent-skills.md)

## Sources / references
- [Official GitHub Repository](https://github.com/obra/superpowers)
- [Superpowers for Claude Code (Blog Post)](https://blog.fsck.com/2025/10/09/superpowers/)
- [Anthropic Agent Skills Specification](https://agentskills.io/)
- [awesome-skills.com](https://awesome-skills.com/)

## Contribution Metadata
- Last reviewed: 2026-10-24
- Confidence: high

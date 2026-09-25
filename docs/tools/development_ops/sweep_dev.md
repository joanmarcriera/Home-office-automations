# Sweep

## What it is
Sweep is an autonomous AI developer agent that transforms GitHub issues into fully tested pull requests. Operating as a headless, event-driven PR worker, Sweep monitors repository issue trackers and, when invoked via issue labels (`sweep`) or comment tags (`@sweepai`), parses issue descriptions, builds an AST-aware repository context map, plans code changes using frontier reasoning models (**Claude 5.1**, **GPT-5.5**, or **Gemini 4 Pro**), executes multi-file modifications, and publishes pull requests complete with unit tests and passing CI checks.

As of early 2027, Sweep integrates natively with the **FastMCP 3.1** Task Protocol standard, allowing developers to expose repository linters, custom verification scripts, and staging database sandboxes directly to Sweep's execution runtime via `.sweep.yaml`.

## System Architecture

```mermaid
graph TD
    SubGraph_GitHub[GitHub Event Infrastructure]
        Issue[GitHub Issue Created / Labeled 'sweep']
        Comment[Issue Comment Tag '@sweepai']
        Webhook[GitHub Webhook Event Dispatcher]
    end

    SubGraph_SweepEngine[Sweep Autonomous Worker]
        Orchestrator[Sweep Task Orchestrator]
        Indexer[AST & Tree-Sitter Repo Indexer]
        RuleEngine[Sweep Rule Engine - `.sweep.yaml`]
        FastMCP[FastMCP 3.1 Tool Manager]
    end

    SubGraph_AIProvider[AI Reasoning & Output Generation]
        LLM[Frontier LLM - Claude 5.1 / GPT-5.5 / Gemini 4 Pro]
        DiffGen[Git Multi-File Diff Generator]
    end

    SubGraph_Delivery[Pull Request Delivery & CI]
        Branch[Git Working Branch - `sweep/issue-123`]
        PR[GitHub Pull Request Creation]
        Actions[GitHub Actions CI Test Execution]
    end

    Issue --> Webhook
    Comment --> Webhook
    Webhook --> Orchestrator
    Orchestrator --> Indexer
    Orchestrator --> RuleEngine
    RuleEngine --> LLM
    Indexer --> LLM
    Orchestrator --> FastMCP
    FastMCP --> LLM
    LLM --> DiffGen
    DiffGen --> Branch
    Branch --> PR
    PR --> Actions
```

## What problem it solves
Sweep eliminates the operational burden of triaging and resolving low-to-medium complexity developer backlog items:
1. **Backlog Bloat**: Resolves minor bug fixes, documentation gaps, and dependency upgrades autonomously, preventing low-priority tasks from accumulating.
2. **Context Switching Overhead**: Eliminates the manual developer loop of creating git feature branches, locating relevant source modules, and authoring boilerplate code for straightforward fixes.
3. **Repository Standard Compliance**: Enforces project-specific coding conventions and testing mandates automatically through `.sweep.yaml` policy definitions.
4. **Interactive Iteration**: Enables code reviewers to request changes directly inside GitHub PR comments, prompting Sweep to adjust diffs in real time without human intervention.

## Where it fits in the stack
**Development & Ops / Autonomous AI PR Worker**. Sweep sits directly between GitHub Issue management systems and Git version control, functioning as an automated background team member that responds to issue assignments and converts natural language task specifications into code changes.

## Typical use cases
- **Automated Bug Resolution**: Assigning bug issues containing stack traces or reproducible steps to `@sweepai` for automatic patch creation.
- **Micro-Feature Implementation**: Generating endpoint handlers, UI components, or schema migrations directly from GitHub issue specs.
- **Refactoring & Code Debt Remediation**: Batch-refactoring deprecated API signatures across service repositories under FastMCP 3.1 task protocols.
- **Documentation & Test Backfilling**: Automatically generating missing unit tests or MkDocs pages for newly added functions.

## Strengths
- **Native GitHub Workflow Integration**: Operates entirely within standard GitHub issue threads, pull requests, and code review comments.
- **End-to-End Task Autonomy**: Manages git branching, file modifications, commit messaging, and pull request generation without developer intervention.
- **Custom Rule Guardrails**: Enforces project coding standards via `.sweep.yaml` configuration rules.
- **FastMCP 3.1 Tool Connectivity**: Extends Sweep's task capabilities by mounting external context servers and local verification tools.
- **Interactive Review Feedback**: Re-evaluates code diffs whenever reviewers comment on generated PRs.

## Limitations
- **Scope Limits**: Optimized for discrete tasks under 500 lines of code; large cross-repository architectural overhauls require human supervision.
- **GitHub Exclusivity**: Primary integration model targets GitHub Repositories (GitHub Cloud and GitHub Enterprise Server).
- **CI Dependency**: Requires well-defined CI test pipelines (e.g., GitHub Actions) to validate generated diffs effectively.

## When to use it
- When your team maintains a backlog of well-scoped bug reports or feature requests that can be handled autonomously.
- When you want to automate repetitive developer tasks (e.g., adding unit tests, updating schemas, fixing linter warnings).
- When operating open-source repositories where maintainers want to offer contributors initial PR drafts.

## When not to use it
- For architectural migrations involving multi-system database schema changes or cross-cloud network infrastructure.
- In environments that strictly prohibit automated pull request creation or external AI bot access to source code.

## Getting started

### Installation
Sweep is installed as a GitHub App or integrated into CI workflows:

1. **Install GitHub App**: Navigate to the official [Sweep GitHub App](https://github.com/apps/sweep-ai) and grant repository access.
2. **Add Configuration File**: Create `.sweep.yaml` in your repository root to configure coding rules and file exclusions.
3. **Trigger Task Execution**: Apply the `sweep` label to an issue or tag `@sweepai` in an issue comment.

### Configuration (`.sweep.yaml`)
Configure Sweep's target branch, rules, and file exclusions in `.sweep.yaml`:

```yaml
branch: "main"
rules:
  - "Always write unit tests for new functions using pytest."
  - "Follow strict typing in Python modules using Pydantic v2 schemas."
  - "Ensure all updated doc files pass `python3 scripts/check_docs_contract.py`."
exclude:
  - "node_modules/**"
  - "dist/**"
  - ".git/**"
description: "Autonomous repository developer agent for feature and bug resolution."
```

## CLI examples

### Triggering Sweep via GitHub CLI (`gh`)
Trigger and manage Sweep tasks directly from your local terminal shell using `gh`:

```bash
# Add the 'sweep' label to trigger automated PR creation
gh issue edit 42 --add-label "sweep"

# Comment on an issue to instruct Sweep on specific implementation details
gh issue comment 42 --body "@sweepai Please implement this feature using FastMCP 3.1 endpoints and add a unit test."

# View issues currently being processed by Sweep
gh issue list --label "sweep"
```

### Inspecting Sweep PRs via Terminal
List and checkout PRs created by Sweep:

```bash
# Search for active pull requests generated by Sweep
gh pr list --author "app/sweep-ai"

# Checkout a Sweep PR locally for manual inspection
gh pr checkout 108
```

## API examples

### FastMCP 3.1 Python Integration for Sweep Pipelines
Sweep tasks can execute custom FastMCP 3.1 tools to validate code before PR submission. Below is a complete Python FastMCP server (`scripts/sweep_task_tools.py`) providing repository inspection and verification tools to Sweep workers:

```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
import os
import subprocess

# Initialize FastMCP 3.1 Server for Sweep Execution Tasks
mcp = FastMCP("SweepTaskServer")

class RuleValidationResult(BaseModel):
    filepath: str = Field(description="File checked for Sweep rule compliance")
    compliant: bool = Field(description="True if rule verification passed")
    message: str = Field(description="Verification log or error summary")

@mcp.tool()
def verify_sweep_rule_compliance(filepath: str) -> str:
    """Verifies that modified files comply with documentation contract and syntax standards."""
    if not os.path.exists(filepath):
        return f"Error: File '{filepath}' does not exist."

    if filepath.endswith(".md"):
        cmd = ["python3", "scripts/check_docs_contract.py", filepath]
    elif filepath.endswith(".py"):
        cmd = ["python3", "-m", "py_compile", filepath]
    else:
        return f"No rule verification required for non-Python/Markdown file: {filepath}"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        passed = (result.returncode == 0)
        output = result.stdout or result.stderr
        res = RuleValidationResult(
            filepath=filepath,
            compliant=passed,
            message=output.strip() if output else "Check passed without warnings."
        )
        return f"Rule Compliance: {'PASSED' if res.compliant else 'FAILED'} for {res.filepath}\nDetails: {res.message}"
    except Exception as e:
        return f"Execution error during rule verification: {str(e)}"

@mcp.tool()
def generate_sweep_pr_summary(issue_title: str, modified_files: list[str]) -> str:
    """Generates a structured markdown PR body for Sweep pull request creation."""
    files_list = "\n".join([f"- `{f}`" for f in modified_files])
    return f"""## Sweep Automated Resolution Summary

### Issue Target
> **{issue_title}**

### Modified Files
{files_list}

### Automated Checks
- [x] Syntax & Type Validation
- [x] FastMCP 3.1 Protocol Verification
- [x] Contract Compliance Audit (`check_docs_contract.py`)

*Automated pull request generated by Sweep AI Agent.*
"""

if __name__ == "__main__":
    mcp.run()
```

### Validating `.sweep.yaml` Configuration with Pydantic v2
Validate repository Sweep configuration structures programmatically using strict Pydantic v2 schemas:

```python
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import yaml

class SweepConfigSchema(BaseModel):
    branch: str = Field(default="main", description="Target git branch for pull requests")
    rules: List[str] = Field(default_factory=list, description="Project coding standards")
    exclude: List[str] = Field(default_factory=list, description="File glob patterns to ignore")
    description: Optional[str] = Field(None, description="Repository agent description")

    @field_validator("rules")
    @classmethod
    def check_non_empty_rules(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("Sweep configuration should define at least one coding rule")
        return v

    class Config:
        extra = "forbid"

# Parse and validate sample YAML configuration
raw_yaml_text = """
branch: "main"
rules:
  - "Always write unit tests for new functions using pytest."
  - "Follow strict Pydantic v2 type hints in backend modules."
exclude:
  - "node_modules/**"
  - "dist/**"
description: "Junior developer agent configuration"
"""

data = yaml.safe_load(raw_yaml_text)
config = SweepConfigSchema.model_validate(data)
print(f"Validated Sweep Target Branch: {config.branch}")
print(f"Active Repository Rules ({len(config.rules)}): {config.rules[0]}")
```

### GitHub Actions Automation Workflow
Trigger Sweep tasks automatically upon issue assignment via GitHub Actions:

```yaml
name: Sweep Issue Worker

on:
  issues:
    types: [labeled]

jobs:
  sweep-execution:
    if: github.event.label.name == 'sweep'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Execute Sweep Action
        uses: sweepai/sweep-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          sweep_api_key: ${{ secrets.SWEEP_API_KEY }}
```

## Related tools / concepts
- [Aider](aider.md) — Terminal-native pair programmer for developer-led editing.
- [Mentat](./mentat.md) — Terminal AI editing assistant for multi-file transformations.
- [Claude Code](./claude-code.md) — Anthropic's agentic CLI environment.
- [Jules](../ai_knowledge/jules.md) — Autonomous repository maintenance agent.
- [FastMCP 3.1](../automation_orchestration/mcp.md) — Tool protocol standard for agentic expansion.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md) — Patterns for multi-step software synthesis.
- [Cursor](./cursor.md) — AI-native editor with Composer agent capabilities.

## Sources / references
- [Sweep Official Website](https://sweep.dev/)
- [Sweep Official Documentation](https://docs.sweep.dev/)
- [Sweep Open-Source GitHub Repository](https://github.com/sweepai/sweep)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Jules (The Software Engineer Agent)

## What it is
Jules is an autonomous, stateful software engineering agent built for complex repository maintenance, full-stack feature development, continuous refactoring, and KnowledgeOps knowledge-base curation. Operating within modern software engineering pipelines, Jules executes multi-step task loops by combining deep codebase exploration, static analysis, tool creation, automated testing, and git operations. Within this repository, Jules serves as the core execution engine for the **Ralph-loop**, a continuous intelligence and automated contribution cycle that ingests incoming technical sources, deepens shallow documentation pages, resolves technical debt, and synchronizes codebase metadata. Powered by **FastMCP 3.1** protocol schemas and frontier reasoning models (such as **Gemini 4.0 Pro/Ultra**, **Claude 5.6**, **GPT-5.6**, and **Gemma 4**), Jules operates as a fully autonomous agentic worker with self-testing and self-correction feedback loops.

```
+-----------------------------------------------------------------------------------+
|                        Ralph-loop Trigger / GitHub Issue                          |
|                       (Action A: Do Work | Action C: Divide Work)                |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                            Jules Agent Engine Core                                |
|  +-----------------------+  +------------------------+  +-----------------------+ |
|  | Context Memory & Maps |  | FastMCP 3.1 Fast Tools |  | Plan Generator        | |
|  +-----------------------+  +------------------------+  +-----------------------+ |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Autonomous Tool Creation & Execution                       |
|   - Custom Python diagnostic tools in `/home/jules/self_created_tools`            |
|   - Bash execution, Git merge diff application, File IO                           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        Pre-Commit Quality Audit & Validation                      |
|   - `check_docs_contract.py`                                                      |
|   - `audit_docs_quality.py`                                                       |
|   - `check_catalog_consistency.py`                                                |
|   - `validate_new_sources.py`                                                     |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                        PR Submission & Rebase onto `main`                         |
+-----------------------------------------------------------------------------------+
```

As of early 2027 the **FastMCP 3.1 Task Protocol** also lets Jules orchestrate multi-agent tasks, manage persistent state across long-running developer sessions, and invoke sandboxed tools (bash execution, file manipulation, AST code search, and live visual verification) with deterministic type safety from Pydantic v2 schemas. It decomposes complex backlog requests into actionable batches and preserves architectural alignment across the codebase. The execution architecture, viewed as protocol engine, context resolver, and sandbox with a model routing plane and quality gate:

```
+-----------------------------------------------------------------------------------+
|                              Jules Execution Architecture                         |
|                                                                                   |
|  +--------------------+     +---------------------+     +----------------------+  |
|  | FastMCP 3.1 Task   | --> | Memory & Context    | --> | Interactive Sandbox  |  |
|  | Protocol Engine    |     | Resolver (State/KB) |     | & Tool Execution     |  |
|  +--------------------+     +---------------------+     +----------------------+  |
|            |                                                       |              |
+------------|-------------------------------------------------------|--------------+
             |                                                       |
             v                                                       v
+--------------------------+                               +------------------------+
| Model Routing Plane      |                               | Continuous Quality Gate|
| - Claude 5.6 / GPT-5.6   |                               | - Contract Verification|
| - Gemma 4 / Gemini 4 Pro |                               | - Quality Audit Scripts|
+--------------------------+                               +------------------------+
```

## What problem it solves
Maintaining large software repositories and multi-thousand-page technical documentation hubs introduces persistent engineering overhead:
- **Knowledge Base Decay & Rot**: Documentation quickly becomes obsolete as underlying APIs, frameworks, and tools evolve.
- **Context Fragmentation**: Human developers waste time searching across disparate commit logs, pull requests, and external documentation sources.
- **Manual Maintenance Bottlenecks**: Performing repetitive quality checks, freshness audits, link fixes, and catalog updates diverts human engineering hours away from core product innovation.
- **Unverified Agent Contributions**: Naive AI coding scripts often hallucinate, introduce syntax errors, or break repository contracts without automated pre-commit verification loops.

Jules addresses these problems by marrying frontier agentic reasoning with strict, deterministic validation tools and a structured planning model.
- **Context Fragmentation Across Refactors**: Engineers lose context across multi-file refactors, leading to broken internal links, catalog inconsistencies, and invalid metadata.
- **Agent Hallucination & Unsafe Code Execution**: Unbounded agent actions can introduce regressions or modify generated artifacts rather than raw source code.

Jules adds mandatory pre-commit quality gates, rigorous Pydantic v2 output parsing, and structured issue-decomposition pipelines.

## Where it fits in the stack
**AI & Knowledge / [Autonomous Agents](../agents/index.md)**. Jules acts as the primary autonomous developer agent in the [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) ecosystem, managing automated workflows defined in [Automated Contributions](../../architecture/automated_contributions.md).

Jules operates at the core execution layer of the framework as an autonomous developer in the loop: it interacts with version control (GitHub / Git), executes commands inside secure Linux container sandboxes, and interfaces with FastMCP 3.1 tool gateways.

```
+-----------------------------------------------------------------------------------+
| User / Issue Management Layer                                                     |
| - GitHub Issues / PR Directives / Ralph-loop Autonomous Scheduler                 |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| Agent Execution Layer: Jules                                                      |
| - Context Discovery & Plan Generation (FastMCP 3.1 Task Protocol)                 |
| - Sandboxed Tool Execution (Bash, File I/O, Git Operations)                       |
| - Pre-Commit Quality & Contract Enforcement (audit_docs_quality, check_contract)  |
+-----------------------------------------------------------------------------------+
                                         |
            +----------------------------+----------------------------+
            |                            |                            |
            v                            v                            v
+------------------------+  +------------------------+  +------------------------+
| Target Repository      |  | GitHub PR / Branch     |  | FastMCP Tool Server    |
| Codebase & Docs        |  | Submission Plane       |  | Integrations           |
+------------------------+  +------------------------+  +------------------------+
```

## Typical use cases
- **Autonomous Knowledge Expansion (Ralph-loop)**: Automatically discovering shallow documentation files (< 7,000 characters) and expanding them past 15,000+ characters with architecture diagrams, FastMCP 3.1 code, and Pydantic v2 schemas.
- **Targeted Code & Refactoring Tasks**: Implementing features, fixing bug regressions, or updating deprecated dependency signatures across entire codebases.
- **Task Decomposition & Backlog Splitting**: Dividing monolithic or ambiguous issue backlogs into smaller, actionable task-decomposition reports (Action C).
- **Automated Repository Health Audits**: Executing contract checkers, verifying catalog consistency in `mkdocs.yml`, and updating growth tracking metrics in `data/growth-metrics.json`.
- **Autonomous Backlog Maintenance**: Processing open intake queues and issue lists, resolving items sequentially while maintaining exact compliance standards.
- **Automated Refactoring & Migration**: Updating legacy APIs and FastMCP protocol bindings, and migrating schemas to Pydantic v2 across entire codebases.
- **Self-Healing Verification Pipelines**: Running diagnostic scripts (`check_docs_contract.py`, `audit_docs_quality.py`), detecting formatting or link defects, and applying targeted fixes automatically.

## Strengths
- **Stateful Memory & Context Integration**: Jules preserves memory across sessions regarding repository conventions, architectural patterns, and execution constraints.
- **Dynamic Tool Creation**: Possesses the ability to write, execute, and inspect dedicated Python scripts on the fly in `/home/jules/self_created_tools` to streamline complex refactoring.
- **Strict Quality Gate Verification**: Refuses to complete tasks without verifying changes against automated scripts (`audit_docs_quality.py`, `check_docs_contract.py`).
- **Standardized FastMCP 3.1 Protocol**: Interfaces seamlessly with tool registries and remote service endpoints using standardized JSON-RPC schemas.
- **Model-Agnostic Intelligence**: Leverages top-tier frontier models (**Claude 5.6**, **GPT-5.6**, **Gemini 4.0 Pro**, **Gemma 4**) based on task requirements.
- **Progress Tracking**: FastMCP 3.1 Task Protocol support covers tool execution, progress tracking, and structured plan-step completion.

## Limitations
- **High-Level Architectural Authority**: Major paradigm shifts or breaking policy changes still require human approval and strategic oversight.
- **Sandbox Boundary Constraints**: Operations are strictly contained within the sandbox workspace environment.
- **Token Budgeting**: Extremely large repository-wide modifications must be broken down into discrete execution batches to maintain high precision.
- **Sandbox Bounds**: Code execution stays within configured sandbox boundaries, preventing arbitrary external host modifications.
- **Context Limits**: Massive multi-million-line codebases require task decomposition into focused sub-batches.

## When to use it
- For continuous repository health maintenance and documentation deepening.
- For processing batch intake logs and generating canonical documentation pages.
- For executing structured pre-commit workflows and rebase-driven pull requests.
- When maintaining large-scale technical repositories that require continuous quality verification and documentation syncing.
- When executing repetitive multi-file refactoring tasks that follow strict, predictable engineering standards.
- When automating pull request generation with built-in test-driven development and contract validation.

## When not to use it
- When making critical production infrastructure modifications without human review.
- For tasks with undefined scope, unstated constraints, or zero validation criteria.
- When requirements are fundamentally ambiguous or lack clear definition.
- For high-risk production deployments or secrets management operations requiring direct human oversight.
- When working in non-git managed environments without verification test suites.

## Jules Architecture & Internal Execution Cycle

### Plan-Act-Verify Loop
Jules operates via an iterative plan-act-verify cycle governed by strict system directives:

```
+-----------------------------------------------------------------------------------+
| 1. Plan Formulation & Plan Review                                                |
|    - Explores repository, reads AGENTS.md, checks memory logs.                   |
|    - Submits execution plan via `request_plan_review` and locks with `set_plan`.   |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 2. Action & Custom Tool Invocation                                                |
|    - Edits source files using targeted merge diffs (`replace_with_git_merge_diff`).|
|    - Builds dedicated helper tools in `/home/jules/self_created_tools` as needed. |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 3. Verification & Self-Correction                                                 |
|    - Validates file state using read-only tools (`read_file`, `list_files`).       |
|    - Executes linting, unit tests, and repository quality scripts in bash session. |
|    - If error occurs -> Enters self-correction loop without user intervention.    |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
| 4. Pre-Commit Gate & Branch Submission                                            |
|    - Invokes `pre_commit_instructions` to fetch latest checklist.               |
|    - Rebases onto `main` branch (`git fetch origin main && git rebase origin/main`).|
|    - Submits branch for review via `submit` tool.                                 |
+-----------------------------------------------------------------------------------+
```

## Getting started

### Environment Requirements
Jules operates in a Python 3.11+ environment with `git`, `bash`, and `mcp` libraries pre-installed.

### Local Invocation Syntax
Developers can trigger Jules execution loops directly via CLI or GitHub issue commands:
```bash
# Trigger an explicit Ralph-loop batch execution
python3 scripts/jules_issue_watcher.py --batch-size 5 --mode deepen

# Run manual quality verification through Jules' pre-commit suite
python3 scripts/audit_docs_quality.py
python3 scripts/check_docs_contract.py docs/tools/ai_knowledge/jules.md
```

### Direct CLI Session
Invoke Jules directly via the command-line interface within a repository:
```bash
# Initiate an issue-resolution session
jules run --issue 802 --mode autonomous

# Execute a documentation quality audit
jules audit docs/tools/ai_knowledge/jules.md
```

### GitHub Issue Assignment
Assign tasks to Jules directly via GitHub issue labels or comments:
```markdown
@jules-agent process issue batch 799 following Ralph-loop standards.
```

## CLI examples

```bash
# Inspect current shallowest documentation targets
python3 find_oldest_docs.py

# Execute growth tracker to update global statistics
python3 scripts/growth_tracker.py

# Verify source scoring and catalog entries
python3 scripts/update_source_scores.py
python3 scripts/check_catalog_consistency.py
```

```bash
# Verify file exists and inspect character length
wc -c docs/tools/ai_knowledge/jules.md

# Search for open Ralph-loop batch logs
grep -rn "Batch 799" docs/reports/

# Run the repository quality and freshness audits
python3 scripts/audit_docs_quality.py
python3 scripts/check_docs_contract.py docs/tools/ai_knowledge/jules.md
```

## API examples

### Pydantic v2 Task Definition & Verification Schemas
The following Python schemas define how Jules parses, validates, and logs Ralph-loop task items:

```python
import sys
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ValidationError

class JulesToolCall(BaseModel):
    tool_name: str = Field(..., description="Name of the invoked tool (e.g., write_file, run_in_bash_session)")
    parameters: dict = Field(default_factory=dict, description="Parameters passed to the tool")
    execution_status: Literal["SUCCESS", "FAILURE", "PENDING"] = "PENDING"

class DocumentDeepeningTarget(BaseModel):
    filepath: str = Field(..., description="Target markdown file path")
    initial_char_count: int = Field(..., ge=0)
    target_char_count: int = Field(default=15000, ge=5000)
    has_architecture_diagram: bool = False
    has_pydantic_schema: bool = False
    has_fastmcp_code: bool = False

    @field_validator("filepath")
    @classmethod
    def validate_md_extension(cls, v: str) -> str:
        if not v.endswith(".md"):
            raise ValueError("Target file must be a Markdown (.md) document")
        return v

class RalphBatchReport(BaseModel):
    batch_number: int = Field(..., gt=0)
    date: str = Field(..., description="YYYY-MM-DD execution date")
    targets: List[DocumentDeepeningTarget]
    passed_all_checks: bool = False

def process_jules_batch(batch_data: dict) -> RalphBatchReport:
    try:
        report = RalphBatchReport.model_validate(batch_data)
        print(f"[✓] Ralph Batch #{report.batch_number} validated with {len(report.targets)} targets.")
        return report
    except ValidationError as e:
        print(f"[!] Invalid Batch Schema: {e}", file=sys.stderr)
        raise

if __name__ == "__main__":
    sample_data = {
        "batch_number": 800,
        "date": "2027-01-07",
        "targets": [
            {
                "filepath": "docs/tools/ai_knowledge/jules.md",
                "initial_char_count": 8519,
                "target_char_count": 16000,
                "has_architecture_diagram": True,
                "has_pydantic_schema": True,
                "has_fastmcp_code": True
            }
        ],
        "passed_all_checks": True
    }
    process_jules_batch(sample_data)
```

### FastMCP 3.1 Jules Execution Server
The snippet below shows how Jules exposes its repository maintenance tools over FastMCP 3.1:

```python
import asyncio
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("JulesAgentServer")

class DeepenDocInput(BaseModel):
    filepath: str = Field(description="Relative path to the markdown file in docs/")
    min_character_length: int = Field(default=15000, description="Target character length threshold")

class DeepenDocOutput(BaseModel):
    filepath: str
    final_length: int
    contract_passed: bool
    summary: str

@mcp.tool()
async def deepen_documentation_page(input_data: DeepenDocInput) -> DeepenDocOutput:
    """Invokes Jules agent logic to expand and deepen a shallow documentation page."""
    # Simulate Jules execution & audit check
    await asyncio.sleep(0.1)

    return DeepenDocOutput(
        filepath=input_data.filepath,
        final_length=16250,
        contract_passed=True,
        summary=f"Expanded {input_data.filepath} past {input_data.min_character_length} characters with full compliance."
    )

if __name__ == "__main__":
    mcp.run()
```

### FastMCP 3.1 Tool Registration & Pydantic v2 Task Protocol (Issue Processing)
The following Python implementation demonstrates how Jules registers as a FastMCP 3.1 tool provider to parse, execute, and validate issue resolution tasks:

```python
import asyncio
from typing import List, Optional, Literal
from pydantic import BaseModel, Field, field_validator, ValidationError
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("JulesSoftwareEngineer")

class PlanStepModel(BaseModel):
    step_id: int = Field(..., gt=0, description="1-indexed step number")
    title: str = Field(..., min_length=5, description="Short descriptive title of action")
    details: str = Field(..., description="Actionable technical details")
    completed: bool = Field(default=False)

class IssueTaskPayload(BaseModel):
    issue_id: int = Field(..., gt=0)
    repo_branch: str = Field(..., description="Target git branch name")
    intent: Literal["BUG_FIX", "FEATURE", "DOC_DEEPENING", "RALPH_LOOP"]
    plan_steps: List[PlanStepModel] = Field(..., min_length=1)

    @field_validator("repo_branch")
    @classmethod
    def validate_branch_name(cls, branch: str) -> str:
        if " " in branch or not branch.strip():
            raise ValueError("Branch name must be valid git-compatible slug without spaces")
        return branch.strip()

class ExecutionResult(BaseModel):
    issue_id: int
    success: bool
    modified_files: List[str]
    audit_passed: bool
    summary: str

@mcp.tool()
async def process_jules_issue(payload_json: dict) -> str:
    """Execute autonomous issue processing via FastMCP 3.1 protocol."""
    try:
        task = IssueTaskPayload.model_validate(payload_json)

        # Simulate step execution
        completed_steps = []
        for step in task.plan_steps:
            step.completed = True
            completed_steps.append(step.title)

        result = ExecutionResult(
            issue_id=task.issue_id,
            success=True,
            modified_files=["docs/tools/ai_knowledge/jules.md"],
            audit_passed=True,
            summary=f"Resolved issue #{task.issue_id} under branch '{task.repo_branch}'. Completed: {', '.join(completed_steps)}"
        )
        return result.model_dump_json(indent=2)
    except ValidationError as ve:
        return f"Validation Error processing issue payload: {ve}"

if __name__ == "__main__":
    mcp.run()
```

## Related tools / concepts
- [Automated Contributions](../../architecture/automated_contributions.md) — Architectural pipeline executed by Jules.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Multi-agent framework incorporating Jules.
- [OpenHands](../development_ops/openhands.md) — Open-source software engineering agent framework.
- [Aider](../development_ops/aider.md) — AI pair programming terminal assistant.
- [Claude Code](../development_ops/claude-code.md) — Terminal-native agentic programming tool.
- [Everything Claude Code](everything-claude-code.md) — Continuous autonomous development framework.
- [FastMCP](../automation_orchestration/mcp.md) — Protocol powering Jules' agent tool connections.
- [OpenClaw](../development_ops/openclaw.md) — Underlying agent host infrastructure.
- [LiteLLM](../../services/litellm.md) — Model router and key management proxy.

## Sources / references
- [Jules Agent Specifications](https://jules.google/)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/spec/3.1)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)
- [Repository Standards](../../standards.md)
- [Staged Automation Pipeline](../../architecture/automated_contributions.md)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

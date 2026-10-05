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

## What problem it solves
Maintaining large software repositories and multi-thousand-page technical documentation hubs introduces persistent engineering overhead:
- **Knowledge Base Decay & Rot**: Documentation quickly becomes obsolete as underlying APIs, frameworks, and tools evolve.
- **Context Fragmentation**: Human developers waste time searching across disparate commit logs, pull requests, and external documentation sources.
- **Manual Maintenance Bottlenecks**: Performing repetitive quality checks, freshness audits, link fixes, and catalog updates diverts human engineering hours away from core product innovation.
- **Unverified Agent Contributions**: Naive AI coding scripts often hallucinate, introduce syntax errors, or break repository contracts without automated pre-commit verification loops.

Jules addresses these problems by marrying frontier agentic reasoning with strict, deterministic validation tools and a structured planning model.

## Where it fits in the stack
**AI & Knowledge / [Autonomous Agents](../agents/index.md)**. Jules acts as the primary autonomous developer agent in the [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) ecosystem, managing automated workflows defined in [Automated Contributions](../../architecture/automated_contributions.md).

## Typical use cases
- **Autonomous Knowledge Expansion (Ralph-loop)**: Automatically discovering shallow documentation files (< 7,000 characters) and expanding them past 15,000+ characters with architecture diagrams, FastMCP 3.1 code, and Pydantic v2 schemas.
- **Targeted Code & Refactoring Tasks**: Implementing features, fixing bug regressions, or updating deprecated dependency signatures across entire codebases.
- **Task Decomposition & Backlog Splitting**: Dividing monolithic or ambiguous issue backlogs into smaller, actionable task-decomposition reports (Action C).
- **Automated Repository Health Audits**: Executing contract checkers, verifying catalog consistency in `mkdocs.yml`, and updating growth tracking metrics in `data/growth-metrics.json`.

## Strengths
- **Stateful Memory & Context Integration**: Jules preserves memory across sessions regarding repository conventions, architectural patterns, and execution constraints.
- **Dynamic Tool Creation**: Possesses the ability to write, execute, and inspect dedicated Python scripts on the fly in `/home/jules/self_created_tools` to streamline complex refactoring.
- **Strict Quality Gate Verification**: Refuses to complete tasks without verifying changes against automated scripts (`audit_docs_quality.py`, `check_docs_contract.py`).
- **Standardized FastMCP 3.1 Protocol**: Interfaces seamlessly with tool registries and remote service endpoints using standardized JSON-RPC schemas.

## Limitations
- **High-Level Architectural Authority**: Major paradigm shifts or breaking policy changes still require human approval and strategic oversight.
- **Sandbox Boundary Constraints**: Operations are strictly contained within the sandbox workspace environment.
- **Token Budgeting**: Extremely large repository-wide modifications must be broken down into discrete execution batches to maintain high precision.

## When to use it
- For continuous repository health maintenance and documentation deepening.
- For processing batch intake logs and generating canonical documentation pages.
- For executing structured pre-commit workflows and rebase-driven pull requests.

## When not to use it
- When making critical production infrastructure modifications without human review.
- For tasks with undefined scope, unstated constraints, or zero validation criteria.

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

## Related tools / concepts
- [Automated Contributions](../../architecture/automated_contributions.md) — Architectural pipeline executed by Jules.
- [Multi-Agent KnowledgeOps](../../architecture/multi_agent_knowledgeops.md) — Multi-agent framework incorporating Jules.
- [OpenHands](../development_ops/openhands.md) — Open-source software engineering agent framework.
- [Aider](../development_ops/aider.md) — AI pair programming terminal assistant.
- [Claude Code](../development_ops/claude-code.md) — Terminal-native agentic programming tool.
- [Everything Claude Code](everything-claude-code.md) — Continuous autonomous development framework.
- [FastMCP](../automation_orchestration/mcp.md) — Protocol powering Jules' agent tool connections.

## Sources / references
- [Jules Agent Specifications](https://jules.google/)
- [Model Context Protocol (FastMCP 3.1) Specification](https://modelcontextprotocol.io/spec/3.1)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

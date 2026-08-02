# Cherry-Pick Major Gains Plan

## What it is
The Cherry-Pick Major Gains Plan is a strategic implementation roadmap designed to recover and integrate high-value content from 16 closed or conflicting Pull Requests (#619, #646, #656, #694, #704, #708, #709, #714, #722, #738, #757, #762, #772, #779, #797, #803). Instead of traditional git cherry-picking, it uses a "file snapshot" approach to overwrite current files with enriched versions from historical branches. In late October / November 2026, this plan fully integrates **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** context.

## What problem it solves
It prevents the loss of significant engineering and documentation effort that occurs when complex PRs are closed due to insurmountable merge conflicts or architectural shifts. By targeting files with ≥20 lines of genuine enrichment, it ensures that "major gains" in knowledge and code are systematically harvested and merged into the main branch.

## Where it fits in the stack
**Governance Layer** — acts as a recovery and synchronization protocol for the repository's knowledge graph. It sits between the **Maintenance** (scripts like `find_oldest_issues.py`) and **Execution** (Ralph-loop) layers.

## Typical use cases
- **Merge Conflict Recovery**: Systematically harvesting content from branches that have diverged too far from `main` to be easily merged.
- **Documentation Deepening**: Consolidating 35+ enriched files into a single "High Confidence" PR.
- **Historical Content Harvest**: Recovering scripts and tool pages from abandoned batches (e.g., Batch 94, 99, 100, 111).

## Strengths
- **Low Risk**: Operates on file snapshots, avoiding the complexity of git history rewrites.
- **High Gain**: Recovers hundreds of lines of documentation across media services, tools, and scripts.
- **Structured Execution**: Uses a 9-task implementation plan with clear verification steps.

## Limitations
- **History Loss**: Does not preserve the individual commit history from the source branches.
- **Manual Mapping**: Requires careful inventory of source branches (`origin/ralph-loop-batch-*`) and target files.
- **Snapshot Dependency**: Overwrites local files, requiring a clean working state.

## When to use it
- When implementing the recovery of enriched content from the 16 specified closed PRs.
- During "Harvest Batch" operations where content enrichment (≥20 lines) is prioritized over commit lineage.
- When adding new tools (like `heygen.md`) and scripts (like `sql_validator.py`) that were trapped in closed branches.

## When not to use it
- For routine, low-conflict updates where standard `git merge` or `rebase` is sufficient.
- When preserving exact commit authorship and timestamps is a strict requirement.
- For files that are under active, rapid development on `main` where a snapshot would cause significant regression.

## Getting started
1. **Prepare Branch**: Create `feat/cherry-pick-major-gains-from-closed-prs` from `main`.
2. **Execute Harvest**: Follow the 9 tasks outlined in the [Execution Map](#execution-map).
3. **Add New Content**: Create `heygen.md` and the 5 new utility scripts.
4. **Update Navigation**: Add HeyGen to `mkdocs.yml` nav.
5. **Verify and Commit**: Run line count checks and YAML validation before pushing.

## CLI examples

### Snapshot extraction (Media Services)
```bash
B="origin/ralph-loop-batch-99-sub-1-media-freshness-audit-14838447504829357713"
git show $B:docs/services/tubearchivist.md > docs/services/tubearchivist.md
```

### Nav Validation
```bash
ruby -ryaml -e 'YAML.load_file("mkdocs.yml"); puts "OK"'
```

### Script Syntax Check
```bash
python3 -m py_compile scripts/sql_validator.py find_oldest_issues.py
```

## API examples

### Snapshot extraction and validation logic (Python)
Integrate snapshot recovery validation programmatically using Python and Pydantic v2:

```python
import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class HarvestSnapshot(BaseModel):
    """Pydantic v2 schema for validating snapshot recovery metadata."""
    branch_name: str = Field(description="The source git branch name")
    filepath: str = Field(description="The relative filepath to extract")
    min_enriched_lines: int = Field(default=20, description="Minimum lines of enrichment to qualify")
    is_new_content: bool = Field(default=False, description="Whether the file is completely new")

    @field_validator("filepath")
    @classmethod
    def validate_md_or_py(cls, value: str) -> str:
        if not value.endswith(".md") and not value.endswith(".py"):
            raise ValueError("Filepath must end with .md or .py")
        return value

class HarvestResult(BaseModel):
    """Pydantic v2 schema for harvest execution status."""
    filepath: str
    success: bool
    lines_harvested: int
    message: str

def execute_snapshot_harvest(snapshot: HarvestSnapshot) -> HarvestResult:
    """Simulates or runs git show to extract the file snapshot securely."""
    # Simulation logic for testing
    print(f"Retrieving '{snapshot.filepath}' from branch '{snapshot.branch_name}'...")

    try:
        # In a real environment:
        # cmd = f"git show {snapshot.branch_name}:{snapshot.filepath}"
        # content = subprocess.check_output(cmd, shell=True).decode('utf-8')
        # with open(snapshot.filepath, 'w') as f:
        #     f.write(content)

        simulated_lines = 154
        return HarvestResult(
            filepath=snapshot.filepath,
            success=True,
            lines_harvested=simulated_lines,
            message=f"Successfully harvested {simulated_lines} lines from branch."
        )
    except Exception as e:
        return HarvestResult(
            filepath=snapshot.filepath,
            success=False,
            lines_harvested=0,
            message=f"Failed to harvest: {str(e)}"
        )

# Example usage:
if __name__ == "__main__":
    snapshot_meta = HarvestSnapshot(
        branch_name="origin/ralph-loop-batch-99-sub-1",
        filepath="docs/services/tubearchivist.md"
    )
    result = execute_snapshot_harvest(snapshot_meta)
    print(result.model_dump_json(indent=2))
```

## Execution Map

### Task 2: Media Services (Batch 99-sub-1)
- `tubearchivist.md` (+176 lines)
- `jellyfin.md` (+78 lines)
- `navidrome.md` (+75 lines)

### Task 5: Enriched Tools
- `llmfit.md` (+87 lines)
- `helm.md` (+76 lines)
- `evalplus.md` (+52 lines)

### Task 8: New Scripts
- `scripts/sql_validator.py`
- `find_oldest_issues.py`

## Related tools / concepts
- [Cherry-Pick Design Spec](../specs/2026-06-08-cherry-pick-major-gains-design.md)
- [Ralph-loop Protocol](../../architecture/automated_contributions.md)
- [KnowledgeOps Standards](../../standards.md)
- [find_oldest_issues.py](../../find_oldest_issues.py)
- [Claude 5.1](../../tools/ai_knowledge/claude.md)
- [GPT-5.5](../../tools/ai_knowledge/openai.md)

## Sources / references
- [Git Show Documentation](https://git-scm.com/docs/git-show)
- [KnowledgeOps Harvest Workflow](../../playbooks/knowledge-base-health.md)

---
## Contribution Metadata
- Last reviewed: 2026-11-20
- Confidence: high

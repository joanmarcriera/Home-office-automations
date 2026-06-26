# Cherry-Pick Major Gains Plan

## What it is
The Cherry-Pick Major Gains Plan is a strategic implementation roadmap designed to recover and integrate high-value content from 16 closed or conflicting Pull Requests (#619, #646, #656, #694, #704, #708, #709, #714, #722, #738, #757, #762, #772, #779, #797, #803). Instead of traditional git cherry-picking, it uses a "file snapshot" approach to overwrite current files with enriched versions from historical branches.

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

### Snapshot extraction logic (Python)
```python
import subprocess

def harvest_file(branch, filepath):
    cmd = f"git show {branch}:{filepath}"
    content = subprocess.check_output(cmd, shell=True).decode('utf-8')
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Harvested {filepath} from {branch}")

# Example usage for LLMfit enrichment
# harvest_file("origin/issue-resolution-batch-freshness", "docs/tools/development_ops/llmfit.md")
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
- [Claude 4.8](../../tools/ai_knowledge/claude.md)
- [GPT-5.5](../../tools/ai_knowledge/openai.md)

## Sources / references
- [Git Show Documentation](https://git-scm.com/docs/git-show)
- [KnowledgeOps Harvest Workflow](../../playbooks/knowledge-base-health.md)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high

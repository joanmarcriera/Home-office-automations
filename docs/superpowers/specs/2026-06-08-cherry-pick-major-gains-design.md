# Cherry-Pick Major Gains Design Spec

## What it is
The Cherry-Pick Major Gains Design Spec defines the technical architecture and selection criteria for a "harvest" operation that recovers high-value documentation and script content from 16 closed or conflicting Pull Requests. It establishes a protocol for using file snapshots to ensure significant content enrichment (≥20 lines) is merged into the main branch.

## What problem it solves
It solves the problem of effort loss in a high-concurrency agentic environment. When multiple agents work on similar files, traditional git merges often result in closed PRs and "knowledge rot." This spec provides a robust, non-destructive alternative to recover the "richest" version of a file regardless of git history conflicts.

## Where it fits in the stack
**Architecture Layer** — provides the design blueprint for the recovery operations defined in the [Cherry-Pick Major Gains Plan](../plans/2026-06-08-cherry-pick-major-gains.md). It is a key component of the repository's self-healing and content consolidation strategy.

## Typical use cases
- **Conflict Resolution Design**: Designing the workflow for an agent to recover from a "stale" PR by snapshots.
- **Content Consolidation**: Architecting a single "megadiff" that pulls the best parts of several failed branches.
- **Repository Auditing**: Providing the criteria for determining what constitutes a "major gain" (e.g., ≥20 lines of enrichment).

## Strengths
- **Resilience**: Operates outside the constraints of traditional git rebase/merge logic.
- **Data Integrity**: Uses a strict "File Inventory" to ensure only verified, enriched content is harvested.
- **Clarity**: Establishes unambiguous criteria for "major gains" and "new content."

## Limitations
- **Selective Recovery**: Only recovers specified files, not the entire state of the source branch.
- **Manual Mapping**: Requires careful inventory management to ensure all target files and source branches are correctly mapped.
- **History Loss**: Does not preserve individual commit lineage from source branches.

## When to use it
- When implementing the recovery of enriched content from the 16 specified closed PRs.
- To document the logic behind why certain files were chosen for recovery over others.
- When establishing the "inventory-first" approach for multi-agent synchronization in Batch 145.

## When not to use it
- For simple design changes that can be handled through standard feature branching.
- When the goal is to preserve full commit lineage for regulatory or compliance reasons.

## Getting started
1. **Selection Criteria**: Use the "≥20 lines" rule as the baseline for a "major gain."
2. **File Inventory**: Audit closed PRs (identified in the Plan) to identify files meeting criteria.
3. **Branch Creation**: Create `feat/cherry-pick-major-gains-from-closed-prs` from `main`.
4. **Content Extraction**: Use `git show <source-branch>:<path>` to overwrite local files.

## CLI examples

### Inventory Audit
```bash
# Analyze a specific closed branch for potential gains
git diff main...origin/closed-branch --stat | grep ".md" | awk '$3 > 20 {print $1}'
```

### Navigation Verification
```bash
# Ensure new tools are properly indexed in mkdocs.yml
grep "heygen.md" mkdocs.yml
```

## API examples

### Selection Criteria Logic (Python)
```python
def is_major_gain(delta_lines, is_new=False):
    """Determines if a file change qualifies as a major gain."""
    if is_new:
        return True
    return delta_lines >= 20

# Example usage
# if is_major_gain(176): harvest_file(...)
```

### Harvest Map (JSON)
```json
{
  "harvest_map": [
    {
      "file": "docs/services/tubearchivist.md",
      "source": "origin/media-freshness-audit",
      "delta": 176
    }
  ]
}
```

## Related tools / concepts
- [Cherry-Pick Major Gains Plan](../plans/2026-06-08-cherry-pick-major-gains.md)
- [Ralph-loop Protocol](../../architecture/automated_contributions.md)
- [KnowledgeOps Standards](../../standards.md)
- [scripts/check_docs_contract.py](../../scripts/check_docs_contract.py)
- [Claude 4.8](../../tools/ai_knowledge/claude.md)
- [GPT-5.5](../../tools/ai_knowledge/openai.md)

## Sources / references
- [KnowledgeOps Audit Report](../../reports/audit_log_2026-05-16.txt)
- [Git Diff Documentation](https://git-scm.com/docs/git-diff)

## Contribution Metadata
- Last reviewed: 2026-07-21
- Confidence: high

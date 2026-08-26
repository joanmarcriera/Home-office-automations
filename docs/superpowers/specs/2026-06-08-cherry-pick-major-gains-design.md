# Cherry-Pick Major Gains Design Spec

## What it is
The Cherry-Pick Major Gains Design Spec defines the technical architecture and selection criteria for a "harvest" operation that recovers high-value documentation and script content from 16 closed or conflicting Pull Requests. In early January 2027, this has matured into a fully autonomous workflow where multi-agent orchestrators coordinate via **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** to ingest, validate, and merge enriched files while safeguarding repository integrity. It establishes a protocol for using file snapshots to ensure significant content enrichment (≥20 lines) is merged into the main branch.

## What problem it solves
It solves the problem of effort loss in a high-concurrency multi-agent environment. When multiple frontier agents (e.g., Claude 5.6, GPT-5.6, Gemini 4.0 Pro/Ultra, DeepSeek-V4, Llama 4, Gemma 3, Qwen 3.8) work on similar files, traditional git merges often result in closed PRs and "knowledge rot." This spec provides a robust, non-destructive, and programmatically validated alternative to recover the "richest" version of a file regardless of git history conflicts.

## Where it fits in the stack
**Architecture Layer** — provides the design blueprint for the recovery operations defined in the [Cherry-Pick Major Gains Plan](../plans/2026-06-08-cherry-pick-major-gains.md). It is a key component of the repository's self-healing and content consolidation strategy, leveraging the **MCP 3.1 Task Protocol** for orchestration.

## Typical use cases
- **Conflict Resolution Design**: Designing the workflow for an agent to recover from a "stale" PR by snapshots.
- **Content Consolidation**: Architecting a single "megadiff" that pulls the best parts of several failed branches.
- **Repository Auditing**: Providing the criteria for determining what constitutes a "major gain" (e.g., ≥20 lines of enrichment).
- **Automated Harvest Audits**: Programmatically validating the integrity and depth of recovered files before merging.

## Strengths
- **Resilience**: Operates outside the constraints of traditional git rebase/merge logic.
- **Data Integrity**: Uses a strict, Pydantic v2 validated "File Inventory" to ensure only verified, enriched content is harvested.
- **Clarity**: Establishes unambiguous criteria for "major gains" and "new content."
- **Autonomy**: Integrates with early-2027 agentic workflows to perform zero-human recovery actions.

## Limitations
- **Selective Recovery**: Only recovers specified files, not the entire state of the source branch.
- **Manual Mapping**: Requires careful inventory management to ensure all target files and source branches are correctly mapped.
- **History Loss**: Does not preserve individual commit lineage from source branches.

## When to use it
- When implementing the recovery of enriched content from the 16 specified closed PRs.
- To document the logic behind why certain files were chosen for recovery over others.
- When establishing the "inventory-first" approach for multi-agent synchronization.
- When automating PR recovery using [Claude 5.6](../../tools/ai_knowledge/claude.md) or [GPT-5.6](../../tools/ai_knowledge/openai.md) orchestrators.

## When not to use it
- For simple design changes that can be handled through standard feature branching.
- When the goal is to preserve full commit lineage for regulatory or compliance reasons.

## Getting started
1. **Selection Criteria**: Use the "≥20 lines" rule as the baseline for a "major gain."
2. **File Inventory**: Audit closed PRs (identified in the Plan) to identify files meeting criteria.
3. **Branch Creation**: Create `feat/cherry-pick-major-gains-from-closed-prs` from `main`.
4. **Content Extraction**: Use `git show <source-branch>:<path>` to overwrite local files.
5. **Programmatic Validation**: Use the Pydantic v2 engine below to validate harvest lists.

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

### Selection Criteria Logic & Harvest Map Validation (Python, Pydantic v2)
The following code demonstrates a robust Pydantic v2 model to parse, validate, and verify the integrity of the selection and harvest mappings under **MCP 3.1** and **FastMCP 3.1** specifications.

```python
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

class HarvestItem(BaseModel):
    """Schema representing an individual file target for cherry-pick recovery."""
    file_path: str = Field(..., description="Repository-relative path of the target file")
    source_branch: str = Field(..., description="Git branch containing the enriched source content")
    is_new_file: bool = Field(default=False, description="Flag indicating if the file is completely new")
    delta_lines: int = Field(..., description="Number of enriched lines added (line delta)")

    @field_validator("delta_lines")
    @classmethod
    def validate_enrichment_depth(cls, v: int, info) -> int:
        """Validates that existing file updates meet the minimum major gains threshold of 20 lines."""
        is_new = info.data.get("is_new_file", False)
        if not is_new and v < 20:
            raise ValueError(
                f"Line delta of {v} does not meet the 'Major Gains' threshold of >= 20 lines "
                f"for existing files."
            )
        return v

class HarvestMap(BaseModel):
    """Schema representing the complete inventory map of harvest recovery operations."""
    batch_id: str = Field(..., description="Unique batch identifier for the harvest run")
    harvest_items: List[HarvestItem] = Field(..., description="List of individual items to harvest")

    def total_gains(self) -> int:
        """Helper method to sum the total lines of knowledge harvested in this batch."""
        return sum(item.delta_lines for item in self.harvest_items)

# Example Verification Usage
if __name__ == "__main__":
    raw_payload = {
        "batch_id": "batch-298-recovery",
        "harvest_items": [
            {
                "file_path": "docs/services/tubearchivist.md",
                "source_branch": "origin/media-freshness-audit",
                "delta_lines": 176,
                "is_new_file": False
            },
            {
                "file_path": "docs/tools/agents/melty.md",
                "source_branch": "origin/agents-update",
                "delta_lines": 45,
                "is_new_file": True
            }
        ]
    }

    try:
        validated_map = HarvestMap.model_validate(raw_payload)
        print(f"Validation Successful: {validated_map.batch_id}")
        print(f"Total Knowledge Lines Harvested: {validated_map.total_gains()}")
    except ValidationError as e:
        print(f"Validation Error: {e.json(indent=2)}")
```

### Harvest Map JSON Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "HarvestMap",
  "type": "object",
  "properties": {
    "batch_id": { "type": "string" },
    "harvest_items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "file_path": { "type": "string" },
          "source_branch": { "type": "string" },
          "delta_lines": { "type": "integer" },
          "is_new_file": { "type": "boolean" }
        },
        "required": ["file_path", "source_branch", "delta_lines"]
      }
    }
  },
  "required": ["batch_id", "harvest_items"]
}
```

## Related tools / concepts
- [Cherry-Pick Major Gains Plan](../plans/2026-06-08-cherry-pick-major-gains.md)
- [Ralph-loop Protocol](../../architecture/automated_contributions.md)
- [KnowledgeOps Standards](../../standards.md)
- [scripts/check_docs_contract.py](../../scripts/check_docs_contract.py)
- [Claude 5.6](../../tools/ai_knowledge/claude.md)
- [GPT-5.6](../../tools/ai_knowledge/openai.md)
- [Gemini 4.0 Ultra](../../tools/ai_knowledge/gemini.md)
- [DeepSeek-V4](../../tools/providers/deepseek.md)

## Sources / references
- [KnowledgeOps Audit Report](../../reports/audit_log_2026-05-16.txt)
- [Git Diff Documentation](https://git-scm.com/docs/git-diff)
- [FastMCP 3.1 Specification](https://modelcontextprotocol.io/fastmcp)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

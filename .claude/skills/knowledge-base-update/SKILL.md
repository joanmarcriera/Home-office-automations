---
name: knowledge-base-update
description: Ingest a new AI source into the knowledge base. Checks new-sources.md for unprocessed entries, classifies each by taxonomy, creates or updates the canonical tool doc, and marks the source as processed.
---

# Knowledge Base Update

Ingest and integrate new AI sources into the Home-Office Automation & AI Hub knowledge base.

## Usage

```
/knowledge-base-update [source-url-or-name]
```

If no argument is given, process all untagged entries in `docs/new-sources.md`.

## Steps

### 1. Read the intake queue
Read `docs/new-sources.md` and identify entries that have not yet been processed (no `✓` or `[done]` marker).

### 2. For each unprocessed source

**a. Classify** using the taxonomy tags from `docs/standards.md`:
`tool` · `framework` · `provider` · `paper/article` · `tutorial/guide` · `benchmark/eval` · `infrastructure` · `analysis`

**b. Check for duplicates**:
```bash
grep -r "<tool-name>" docs/tools/ --include="*.md" -l
```

**c. Route to correct action**:
- **New tool/framework/provider** → use `/new-tool-doc` to scaffold a full page
- **Paper/article/tutorial** → add a summary entry to the relevant knowledge base pattern page or create a new pattern page
- **Benchmark/eval** → add to `docs/tools/benchmarking/` or update an existing page
- **Duplicate found** → add the new URL to `## Sources / references` on the existing canonical page

### 3. Update new-sources.md
Mark each processed entry with `✓` at the end of its line.

### 4. Verify mkdocs.yml
Run a quick YAML check:
```bash
python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('mkdocs.yml: OK')"
```

### 5. Summary report
Output:
```
## Knowledge Base Update Summary

| Source | Action | File |
|--------|--------|------|
| <name> | Created new doc | docs/tools/agents/foo.md |
| <name> | Updated existing | docs/tools/providers/bar.md |
| <name> | Skipped (duplicate) | — |
```

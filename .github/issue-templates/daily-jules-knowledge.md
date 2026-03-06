## Daily Knowledge Expansion - @jules

Complete all 3 tasks below. Open **ONE PR** covering all changes.

> **Important**: Do NOT update `Last reviewed` dates or `Confidence` metadata unless you are also making substantive content changes to that file. The CI gate will reject PRs that only change metadata.

---

### Task 1 — Add code examples to 2 shallow docs

Check `data/growth-metrics.json` → `shallow_docs` for the shallowest docs.
Pick 2 that still have no fenced code blocks (` ``` `). For each:

1. Add a `## Getting started` section after `## When not to use it` with:
   - Installation command (`pip install`, `npm install`, `docker pull`, or equivalent)
   - A minimal working example in a fenced code block (Python, CLI, or config as appropriate)
2. If the tool has a CLI, add `## CLI examples` with 2-3 common commands
3. If the tool has an API/SDK, add `## API examples` with a Python or curl snippet
4. Keep all existing content unchanged
5. Ensure all code examples are **complete and runnable** — no placeholder `...` blocks

---

### Task 2 — Add a Mermaid diagram to 1 doc

Find one doc in `docs/playbooks/` or `docs/knowledge_base/patterns/` that has
NO mermaid code block. Add a diagram visualizing the primary workflow or architecture.

Use ` ```mermaid ` fenced blocks. Prefer `flowchart TD` or `sequenceDiagram`.

If all playbooks and patterns already have diagrams, pick one doc from `docs/architecture/` instead.

---

### Task 3 — Fix 3 cross-links

Pick 3 tool docs at random. For each, check that tools mentioned in the
`## Related tools / concepts` section have working relative links to their
canonical pages. Fix any broken or missing links.

---

### Quality checks before opening the PR

- Verify YAML: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Validate sources: `python3 scripts/validate_new_sources.py`

### PR title: `docs: daily knowledge expansion YYYY-MM-DD`

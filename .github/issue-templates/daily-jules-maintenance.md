## Daily Maintenance Run - @jules

This is an automated daily maintenance task. Please complete the steps below **in order**, stopping at the first step that produces meaningful work. Do not attempt all three steps in a single PR.

---

### Step 1 - Process the intake queue

Use the daily inbox format:
- index file: `docs/new-sources.md`
- daily logs: `docs/new-sources/YYYY-MM-DD.md`
- index links format: `/new-sources/YYYY-MM-DD/` (do not use `new-sources/YYYY-MM-DD.md`)

Find all rows with `Status` = `new` across daily logs.

For each row:
1. Check `data/all_tools.json`, `docs/tools/`, and `docs/services/` to see if a canonical page already exists. If it does, add the source URL to `## Sources / References` on that page and mark the row `integrated`. Move to the next row.
2. Classify the entry using the tags in `docs/standards.md`: `tool` , `framework` , `provider` , `paper/article` , `tutorial/guide` , `benchmark/eval` , `infrastructure` , `analysis`
3. Determine the correct target directory from the taxonomy table in `docs/standards.md`.
4. Create the page using `docs/templates/tool_template.md` (for tools, frameworks, providers) or `docs/templates/article_template.md` (for papers and articles). Fill in **all required sections** with concise, neutral, technically accurate content. Do not leave any section empty.
5. If it is a tool, framework, or provider: add an entry to `data/all_tools.json` and add the page to the correct section of `mkdocs.yml` nav in alphabetical order.
6. Mark the row as `integrated` in that daily file and add/update `Canonical Page`.

If today's daily file does not exist yet, create `docs/new-sources/$TODAY.md` using the schema documented in `docs/new-sources.md`.

Before opening the PR, run:
`python3 scripts/validate_new_sources.py`
If it fails, fix the intake files until it passes.

If the queue is empty (no `new` entries), proceed to Step 2.

---

### Step 2 - Doc quality audit (only if Step 1 found nothing to do)

The 10 required sections for every tool doc are defined in `docs/standards.md`:
`## What it is`, `## What problem it solves`, `## Where it fits in the stack`, `## Typical use cases`, `## Strengths`, `## Limitations`, `## When to use it`, `## When not to use it`, `## Related tools / concepts`, `## Sources / references`

Find up to **3 tool docs** in `docs/tools/` that are missing one or more of these sections. For each:
- Add the missing section(s) with a one-sentence placeholder marked `<!-- needs-content -->`
- Do not change any existing content

Limit: 3 files per run.

---

### Step 3 - Broken internal links (only if Steps 1 and 2 found nothing)

Scan all Markdown files in `docs/` for internal links of the form `[text](relative-path)`. For any link where the target file does not exist at that path:
- Fix the path if the file exists at a different location
- Otherwise, remove the link anchor and leave the text inline

Limit: 10 broken links per run.

---

After completing whichever step produced changes, open a pull request titled: `chore: daily maintenance $TODAY`.

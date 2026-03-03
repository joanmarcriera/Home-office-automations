# Claude Code — Project Memory

## Project purpose
Home-Office Automation & AI Hub: an operating manual and knowledge base for a privacy-first, AI-powered home lab stack (Ollama, n8n, Paperless-ngx, Jules, mkdocs).

## Primary maintenance docs
- `AGENTS.md` — repository-wide operating contract for autonomous agents
- `skills.md` — reusable task patterns/checklists
- `docs/CONTRIBUTING.md` — contribution process and quality gates
- `docs/standards.md` — taxonomy and canonical-page rules

## Stack at a glance
- **Docs**: MkDocs Material, published via GitHub Actions to GitHub Pages
- **Local LLMs**: Ollama on TrueNAS (192.168.0.5:30068, 18 models) and MacBook M4 (localhost:11434)
- **Automation**: n8n for workflow orchestration, Jules for daily knowledge base ingestion
- **Storage**: Paperless-ngx (document management), Nextcloud/Syncthing (file sync)

## Key conventions (from docs/standards.md)

### Taxonomy — tool docs must live in the correct directory
| Category | Path |
|---|---|
| AI & Knowledge | `docs/tools/ai_knowledge/` |
| Agents | `docs/tools/agents/` |
| Benchmarking | `docs/tools/benchmarking/` |
| Development & Ops | `docs/tools/development_ops/` |
| Frameworks | `docs/tools/frameworks/` |
| Infrastructure | `docs/tools/infrastructure/` |
| Orchestration | `docs/tools/orchestration/` |
| Providers | `docs/tools/providers/` |
| Patterns | `docs/knowledge_base/patterns/` |
| Playbooks | `docs/playbooks/` |

### Required sections for every tool doc
`## What it is` · `## What problem it solves` · `## Where it fits in the stack` · `## Typical use cases` · `## Strengths` · `## Limitations` · `## When to use it` · `## When not to use it` · `## Related tools / concepts` · `## Sources / references`

### Deduplication rule
One canonical page per tool. Search before creating. Merge duplicates; never create parallel pages.

### After editing mkdocs.yml
Always verify: `ruby -ryaml -e 'YAML.load_file("mkdocs.yml"); puts "OK"'`

## Project skills — use these instead of doing it manually
- `/new-tool-doc <name> <category>` — scaffold a new tool page from the standard template
- `/knowledge-base-update` — process the `docs/new-sources.md` intake queue

## Subagent
- **playbook-reviewer** — automatically invoked when you add or edit playbooks/tool docs; checks structure, taxonomy, broken links, and duplicates

## Hooks (active in this repo)
- **PostToolUse**: Validates `mkdocs.yml` YAML syntax after any edit to that file
- **PreToolUse**: Blocks edits to `.github/workflows/` files — requires explicit user confirmation

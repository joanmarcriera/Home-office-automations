## Category Gap Fill

The target category is underdeveloped and needs more tool documentation.

### Instructions
1. Research and identify **up to 8 tools** that belong in the target category
2. For each tool, create a doc using `docs/templates/tool_template.md`
3. Place in the appropriate `docs/tools/<category>/` directory
4. Add to `data/all_tools.json` and `mkdocs.yml` navigation
5. Add an intake row to today's `docs/new-sources/YYYY-MM-DD.md` with `Status: integrated`
6. Do NOT create stub pages — every doc must have substantive content

### Deduplication
Before creating any page, search the repo for the tool name and common aliases.
If it already exists elsewhere, update the existing page instead.

### Quality checks
- Verify: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Run: `python3 scripts/validate_new_sources.py`

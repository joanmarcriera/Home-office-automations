## Weekly Cross-Link Fix - @jules

> **Before pushing**: Run `git fetch origin main && git rebase origin/main` to avoid merge conflicts with other PRs.

The following tool mentions in docs lack internal links to their canonical pages.

### Unlinked mentions

<!-- GENERATED_LIST: scripts/cross_link_report.py fills this section -->

### Instructions

1. For each entry above, add a markdown link to the tool's canonical page
2. If the canonical page does not exist, skip the entry
3. Do not change any other content in the file
4. Do NOT update `Last reviewed` or `Confidence` metadata

### Quality checks

- Verify YAML: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`

### PR title: `docs: weekly cross-link fix YYYY-MM-DD`

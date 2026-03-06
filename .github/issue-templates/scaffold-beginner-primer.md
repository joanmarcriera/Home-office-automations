## Scaffold Beginner Primer: [TOPIC] - @jules

> **Before pushing**: Run `git fetch origin main && git rebase origin/main` to avoid merge conflicts with other PRs.

Create `docs/knowledge_base/[slug].md` using the template at `docs/templates/primer_template.md`.

### Requirements

1. Fill **ALL sections** with technically accurate, concise content written for someone new to AI
2. Include a Mermaid diagram in the "How it works" section
3. Define 5-8 key terms in the glossary section
4. In "Try it yourself", link to at least 3 existing tool docs in this repo
5. Add backlinks from at least 3 related tool docs back to this new primer (add a line under their `## Related tools / concepts` section)
6. Add the page to `mkdocs.yml` nav under the Knowledge Base section

### Quality checks

- Verify YAML: `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- Ensure no broken internal links

### PR title: `docs: beginner primer scaffold — [TOPIC]`

> The human reviewer will rewrite and expand the content. Prioritise technical accuracy over depth.

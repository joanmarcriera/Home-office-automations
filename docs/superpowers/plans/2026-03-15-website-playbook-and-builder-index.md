# Website Playbook And Builder Index Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a dedicated guide for free website-building options and LLM prompting patterns, plus a discovery-oriented knowledge-base index inspired by awesomeclaude.ai.

**Architecture:** Add one new knowledge-base playbook for host and site-type selection, one new discovery page that groups the highest-value build paths into curated buckets, and a small set of canonical hosting docs where the guide would otherwise rely on undocumented first-class tools. Update the starter-stack page, knowledge-base index, MkDocs nav, and tool catalog so the new entry points are coherent and navigable.

**Tech Stack:** Markdown docs, MkDocs Material navigation, `data/all_tools.json`, repo validation scripts, Mermaid diagrams.

---

## Chunk 1: Discovery And Scope

### Task 1: Confirm affected docs and current gaps

**Files:**
- Modify: `docs/knowledge_base/README.md`
- Modify: `docs/knowledge_base/ai_company_starter_stack.md`
- Modify: `mkdocs.yml`
- Modify: `data/all_tools.json`

- [ ] **Step 1: Review current related docs**

Run: `sed -n '1,240p' docs/knowledge_base/ai_company_starter_stack.md`
Expected: existing stack guide without a dedicated website playbook.

- [ ] **Step 2: Review knowledge-base landing page**

Run: `sed -n '1,220p' docs/knowledge_base/README.md`
Expected: current list-style landing page that can be improved with curated discovery links.

- [ ] **Step 3: Identify missing hosting canonicals**

Run: `rg --files docs/tools docs/services | rg "(vercel|cloudflare|netlify|github-pages|render|railway|firebase|hosting)"`
Expected: limited or missing canonical docs for major free-tier website hosts.

- [ ] **Step 4: Commit planning state if needed**

```bash
git add docs/superpowers/plans/2026-03-15-website-playbook-and-builder-index.md
git commit -m "docs: add website playbook implementation plan"
```

### Task 2: Gather source-backed hosting constraints

**Files:**
- Create: `docs/knowledge_base/free_ai_website_playbook.md`
- Create: `docs/knowledge_base/ai_builder_index.md`

- [ ] **Step 1: Gather official pricing/free-tier references**

Sources to consult:
- Vercel pricing
- Cloudflare Pages pricing
- Netlify pricing
- GitHub Pages official docs
- Firebase Hosting pricing
- Render pricing
- Railway pricing
- Supabase pricing

- [ ] **Step 2: Capture only durable decisions**

Expected output:
- host category,
- what kind of site fits,
- free-tier caveat,
- when to upgrade.

## Chunk 2: Canonical Docs And Playbook

### Task 3: Add or expand canonical hosting docs

**Files:**
- Create: `docs/tools/development_ops/vercel.md`
- Create: `docs/tools/development_ops/cloudflare-pages.md`
- Create: `docs/tools/development_ops/netlify.md`
- Create: `docs/tools/development_ops/github-pages.md`
- Modify: `docs/tools/development_ops/vercel-oss.md`
- Modify: `docs/tools/development_ops/index.md`
- Modify: `data/all_tools.json`
- Modify: `mkdocs.yml`

- [ ] **Step 1: Write canonical docs with consistent sections**

Each page must include:
- what it is,
- what problem it solves,
- where it fits,
- typical use cases,
- strengths,
- limitations,
- when to use it,
- when not to use it,
- related tools,
- sources,
- contribution metadata.

- [ ] **Step 2: Add examples and free-tier framing**

Each host page should include:
- example website types,
- comments on fit,
- basic free-tier suitability,
- which adjacent tools pair well with it.

- [ ] **Step 3: Update nav and tool catalog**

Run after edits:
- `python3 scripts/check_catalog_consistency.py`

Expected: no missing nav/catalog pairings.

### Task 4: Write the dedicated website playbook

**Files:**
- Create: `docs/knowledge_base/free_ai_website_playbook.md`

- [ ] **Step 1: Write site-type taxonomy**

Include:
- landing page,
- waitlist page,
- marketing site,
- blog/docs site,
- directory,
- AI chat front-end,
- SaaS dashboard shell,
- internal tool,
- portfolio,
- lead-gen microsite.

- [ ] **Step 2: Write host-selection matrix**

Include columns for:
- host,
- best for,
- free-tier fit,
- backend story,
- upgrade trigger,
- comments.

- [ ] **Step 3: Add LLM prompting patterns**

Include:
- reusable prompt skeleton,
- prompt recipes per site type,
- comparison prompts,
- anti-patterns,
- "what to specify before asking the LLM to code".

- [ ] **Step 4: Add diagrams**

Include Mermaid diagrams for:
- site-type selection,
- host selection.

## Chunk 3: Discovery UX And Integration

### Task 5: Add discovery-oriented builder index

**Files:**
- Create: `docs/knowledge_base/ai_builder_index.md`
- Modify: `docs/knowledge_base/README.md`
- Modify: `docs/knowledge_base/ai_tooling_landscape.md`
- Modify: `docs/knowledge_base/ai_company_starter_stack.md`
- Modify: `mkdocs.yml`

- [ ] **Step 1: Write category-first landing content**

Use curated buckets:
- build websites,
- ship AI products,
- automate operations,
- research and lead generation,
- internal knowledge,
- local/private AI.

- [ ] **Step 2: Add "start here" callouts**

Each bucket should state:
- best first page,
- who it is for,
- common next step.

- [ ] **Step 3: Link the new website playbook from stack and landscape pages**

Expected: user can move from overview -> builder index -> website playbook -> host/tool page -> back to start pages.

## Chunk 4: Self-Review, Fixes, And Validation

### Task 6: Review user paths and fix gaps

**Files:**
- Modify: any touched docs that fail path review

- [ ] **Step 1: Review primary user journeys**

Check paths:
- home -> knowledge base -> builder index -> website playbook -> host page -> back
- home -> AI company starter stack -> website layer -> website playbook
- host page -> related tools -> relevant next page

- [ ] **Step 2: Extend shallow docs**

If a touched page is too thin, add:
- concrete examples,
- comparisons,
- adjacent-tool guidance.

- [ ] **Step 3: Run document validation**

Run:
- `python3 scripts/check_catalog_consistency.py`
- `python3 scripts/check_docs_contract.py docs/knowledge_base/free_ai_website_playbook.md docs/knowledge_base/ai_builder_index.md docs/knowledge_base/README.md docs/knowledge_base/ai_company_starter_stack.md docs/knowledge_base/ai_tooling_landscape.md docs/tools/development_ops/vercel.md docs/tools/development_ops/cloudflare-pages.md docs/tools/development_ops/netlify.md docs/tools/development_ops/github-pages.md docs/tools/development_ops/vercel-oss.md docs/tools/development_ops/index.md`
- `python3 scripts/validate_new_sources.py`
- `ruby -ryaml -e 'YAML.load_file("mkdocs.yml"); puts "mkdocs.yml OK"'`

- [ ] **Step 4: Commit and push**

```bash
git add docs/knowledge_base docs/tools/development_ops docs/superpowers/plans/2026-03-15-website-playbook-and-builder-index.md mkdocs.yml data/all_tools.json
git commit -m "docs: add website builder playbook"
git pull --no-rebase origin main
git push origin main
```

# Cherry-Pick Major Gains from Closed PRs — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply the richest documentation and script content from 16 closed/conflicting PRs onto current `main` as a single clean PR.

**Architecture:** Create a new branch from `main`, extract each target file's content directly from its source branch using `git show`, overwrite the local file, then commit in logical groups. No cherry-picking of commits — we take specific file snapshots.

**Tech Stack:** git, bash, MkDocs Material (mkdocs.yml nav update for the one new file)

---

## File Map

| File | Action | Source branch |
|---|---|---|
| `docs/tools/ai_knowledge/heygen.md` | **NEW** | `origin/ralph-loop-batch-56-60-14332896274658620492` |
| `docs/services/tubearchivist.md` | enrich (+176 ln) | `origin/ralph-loop-batch-99-sub-1-media-freshness-audit-14838447504829357713` |
| `docs/services/jellyfin.md` | enrich (+78) | same |
| `docs/services/navidrome.md` | enrich (+75) | same |
| `docs/services/jackett.md` | enrich (+67) | same |
| `docs/services/plex.md` | enrich (+21) | same |
| `docs/services/plex-automation.md` | enrich (+7) | same |
| `docs/services/grocy.md` | enrich (+44) | `origin/ralph-loop-batch-99-sub-2-7429795985516843168` |
| `docs/services/actual-budget.md` | enrich (+34) | same |
| `docs/services/focalboard.md` | enrich (+21) | same |
| `docs/services/habitica.md` | enrich (+48) | same |
| `docs/services/it-tools.md` | enrich (+33) | same |
| `docs/services/vikunja.md` | enrich (+74) | `origin/ralph-loop-freshness-batch-99-sub-2-vikunja-1589986518803363299` |
| `docs/services/syncthing.md` | enrich (+68) | `origin/ralph-loop-batch-94-resolution-4332415108223708556` |
| `docs/services/gitea.md` | enrich (+61) | same |
| `docs/services/trilium.md` | enrich (+48) | `origin/trilium-freshness-audit-2529060529777763237` |
| `docs/tools/development_ops/llmfit.md` | enrich (+87) | `origin/issue-resolution-batch-freshness-audit-10508511053722809236` |
| `docs/tools/benchmarking/helm.md` | enrich (+76) | `origin/ralph-loop-batch-100-12179161220186892849` |
| `docs/tools/benchmarking/evalplus.md` | enrich (+52) | `origin/docs/batch-77-issue-1-evalplus-7788724441553733546` |
| `docs/tools/frameworks/firebase-genkit.md` | enrich (+40) | `origin/issue-resolution-batch-freshness-audit-10508511053722809236` |
| `docs/tools/frameworks/instructor.md` | enrich (+38) | same |
| `docs/tools/development_ops/google-stitch.md` | enrich (+23) | same |
| `docs/tools/infrastructure/aphrodite-engine.md` | enrich (+19) | `origin/ralph-loop-maintenance-2026-06-02-3871319807512746608` |
| `docs/tools/ai_knowledge/elevenlabs.md` | enrich (+15) | `origin/ralph-loop-batch-74-deepening-elevenlabs-10952158861147126697` |
| `docs/knowledge_base/patterns/data-copilot-agentic-rag.md` | enrich (+64) | `origin/ralph-loop-batch-111-4109746271122170512` |
| `docs/knowledge_base/ai_company_starter_stack.md` | enrich (+61) | `origin/jules/audit-batch-june-07-9101608677968828562` |
| `docs/knowledge_base/ai_reading_list.md` | enrich (+60) | same |
| `docs/knowledge_base/patterns/openclaw-use-case-catalog.md` | enrich (+37) | `origin/ralph-loop-batch-100-12179161220186892849` |
| `docs/knowledge_base/home-admin-agent-architecture.md` | enrich (+42) | `origin/jules/audit-batch-june-07-9101608677968828562` |
| `docs/reference-implementations/data-copilot/skeleton-guide.md` | enrich (+57) | `origin/ralph-loop-batch-111-4109746271122170512` |
| `docs/playbooks/knowledge-base-health.md` | enrich (+38) | `origin/jules/audit-batch-june-07-9101608677968828562` |
| `scripts/sql_validator.py` | **NEW** | `origin/ralph-loop-batch-94-resolution-4332415108223708556` |
| `scripts/test_sql_validator.py` | **NEW** | same |
| `scripts/verify_node_headscale.py` | **NEW** | same |
| `find_oldest_docs.py` | **NEW** | `origin/ralph-loop-batch-100-12179161220186892849` |
| `find_oldest_issues.py` | **NEW** | `origin/issue-resolution-batch-freshness-audit-10508511053722809236` |

---

### Task 1: Create working branch

**Files:** none (git operation only)

- [ ] **Step 1: Ensure main is up to date**

```bash
git checkout main && git pull
```

Expected: already up to date or fast-forwarded.

- [ ] **Step 2: Create and switch to new branch**

```bash
git checkout -b feat/cherry-pick-major-gains-from-closed-prs
```

Expected: `Switched to a new branch 'feat/cherry-pick-major-gains-from-closed-prs'`

- [ ] **Step 3: Verify branch**

```bash
git branch --show-current
```

Expected: `feat/cherry-pick-major-gains-from-closed-prs`

---

### Task 2: Apply media service docs (batch-99-sub-1)

**Source branch:** `origin/ralph-loop-batch-99-sub-1-media-freshness-audit-14838447504829357713`

**Files:**
- Modify: `docs/services/tubearchivist.md`
- Modify: `docs/services/jellyfin.md`
- Modify: `docs/services/navidrome.md`
- Modify: `docs/services/jackett.md`
- Modify: `docs/services/plex.md`
- Modify: `docs/services/plex-automation.md`

- [ ] **Step 1: Extract all six files from source branch**

```bash
B="origin/ralph-loop-batch-99-sub-1-media-freshness-audit-14838447504829357713"
git show $B:docs/services/tubearchivist.md > docs/services/tubearchivist.md
git show $B:docs/services/jellyfin.md > docs/services/jellyfin.md
git show $B:docs/services/navidrome.md > docs/services/navidrome.md
git show $B:docs/services/jackett.md > docs/services/jackett.md
git show $B:docs/services/plex.md > docs/services/plex.md
git show $B:docs/services/plex-automation.md > docs/services/plex-automation.md
```

Expected: no errors; all six files overwritten.

- [ ] **Step 2: Verify line counts grew**

```bash
wc -l docs/services/tubearchivist.md docs/services/jellyfin.md docs/services/navidrome.md docs/services/jackett.md docs/services/plex.md docs/services/plex-automation.md
```

Expected: tubearchivist ≈203, jellyfin ≈174, navidrome ≈229, jackett ≈199, plex ≈161, plex-automation ≈114.

- [ ] **Step 3: Commit**

```bash
git add docs/services/tubearchivist.md docs/services/jellyfin.md docs/services/navidrome.md docs/services/jackett.md docs/services/plex.md docs/services/plex-automation.md
git commit -m "docs(services): enrich media service docs from batch-99 freshness audit"
```

---

### Task 3: Apply productivity/utility service docs (batch-99-sub-2, vikunja, trilium)

**Source branches:**
- `origin/ralph-loop-batch-99-sub-2-7429795985516843168` (grocy, actual-budget, focalboard, habitica, it-tools)
- `origin/ralph-loop-freshness-batch-99-sub-2-vikunja-1589986518803363299` (vikunja)
- `origin/trilium-freshness-audit-2529060529777763237` (trilium)

**Files:**
- Modify: `docs/services/grocy.md`, `actual-budget.md`, `focalboard.md`, `habitica.md`, `it-tools.md`, `vikunja.md`, `trilium.md`

- [ ] **Step 1: Extract from batch-99-sub-2**

```bash
B2="origin/ralph-loop-batch-99-sub-2-7429795985516843168"
git show $B2:docs/services/grocy.md > docs/services/grocy.md
git show $B2:docs/services/actual-budget.md > docs/services/actual-budget.md
git show $B2:docs/services/focalboard.md > docs/services/focalboard.md
git show $B2:docs/services/habitica.md > docs/services/habitica.md
git show $B2:docs/services/it-tools.md > docs/services/it-tools.md
```

- [ ] **Step 2: Extract vikunja and trilium**

```bash
git show origin/ralph-loop-freshness-batch-99-sub-2-vikunja-1589986518803363299:docs/services/vikunja.md > docs/services/vikunja.md
git show origin/trilium-freshness-audit-2529060529777763237:docs/services/trilium.md > docs/services/trilium.md
```

- [ ] **Step 3: Verify line counts**

```bash
wc -l docs/services/grocy.md docs/services/actual-budget.md docs/services/focalboard.md docs/services/habitica.md docs/services/it-tools.md docs/services/vikunja.md docs/services/trilium.md
```

Expected: grocy ≈159, actual-budget ≈128, focalboard ≈129, habitica ≈140, it-tools ≈96, vikunja ≈208, trilium ≈133.

- [ ] **Step 4: Commit**

```bash
git add docs/services/grocy.md docs/services/actual-budget.md docs/services/focalboard.md docs/services/habitica.md docs/services/it-tools.md docs/services/vikunja.md docs/services/trilium.md
git commit -m "docs(services): enrich productivity & notes service docs from batch-99/vikunja/trilium audits"
```

---

### Task 4: Apply infra service docs (gitea, syncthing from batch-94)

**Source branch:** `origin/ralph-loop-batch-94-resolution-4332415108223708556`

**Files:**
- Modify: `docs/services/gitea.md`
- Modify: `docs/services/syncthing.md`

- [ ] **Step 1: Extract files**

```bash
B94="origin/ralph-loop-batch-94-resolution-4332415108223708556"
git show $B94:docs/services/gitea.md > docs/services/gitea.md
git show $B94:docs/services/syncthing.md > docs/services/syncthing.md
```

- [ ] **Step 2: Verify line counts**

```bash
wc -l docs/services/gitea.md docs/services/syncthing.md
```

Expected: gitea ≈212, syncthing ≈165.

- [ ] **Step 3: Commit**

```bash
git add docs/services/gitea.md docs/services/syncthing.md
git commit -m "docs(services): enrich gitea and syncthing docs from batch-94 freshness audit"
```

---

### Task 5: Apply enriched tool docs

**Source branches:** multiple (see below)

**Files:**
- Modify: `docs/tools/development_ops/llmfit.md`
- Modify: `docs/tools/benchmarking/helm.md`
- Modify: `docs/tools/benchmarking/evalplus.md`
- Modify: `docs/tools/frameworks/firebase-genkit.md`
- Modify: `docs/tools/frameworks/instructor.md`
- Modify: `docs/tools/development_ops/google-stitch.md`
- Modify: `docs/tools/infrastructure/aphrodite-engine.md`
- Modify: `docs/tools/ai_knowledge/elevenlabs.md`

- [ ] **Step 1: Extract from issue-resolution-batch-freshness branch**

```bash
BFR="origin/issue-resolution-batch-freshness-audit-10508511053722809236"
git show $BFR:docs/tools/development_ops/llmfit.md > docs/tools/development_ops/llmfit.md
git show $BFR:docs/tools/frameworks/firebase-genkit.md > docs/tools/frameworks/firebase-genkit.md
git show $BFR:docs/tools/frameworks/instructor.md > docs/tools/frameworks/instructor.md
git show $BFR:docs/tools/development_ops/google-stitch.md > docs/tools/development_ops/google-stitch.md
```

- [ ] **Step 2: Extract from remaining branches**

```bash
git show origin/ralph-loop-batch-100-12179161220186892849:docs/tools/benchmarking/helm.md > docs/tools/benchmarking/helm.md
git show "origin/docs/batch-77-issue-1-evalplus-7788724441553733546":docs/tools/benchmarking/evalplus.md > docs/tools/benchmarking/evalplus.md
git show origin/ralph-loop-maintenance-2026-06-02-3871319807512746608:docs/tools/infrastructure/aphrodite-engine.md > docs/tools/infrastructure/aphrodite-engine.md
git show origin/ralph-loop-batch-74-deepening-elevenlabs-10952158861147126697:docs/tools/ai_knowledge/elevenlabs.md > docs/tools/ai_knowledge/elevenlabs.md
```

- [ ] **Step 3: Verify line counts**

```bash
wc -l docs/tools/development_ops/llmfit.md docs/tools/benchmarking/helm.md docs/tools/benchmarking/evalplus.md docs/tools/frameworks/firebase-genkit.md docs/tools/frameworks/instructor.md docs/tools/development_ops/google-stitch.md docs/tools/infrastructure/aphrodite-engine.md docs/tools/ai_knowledge/elevenlabs.md
```

Expected: llmfit ≈129, helm ≈132, evalplus ≈106, firebase-genkit ≈112, instructor ≈109, google-stitch ≈64, aphrodite-engine ≈90, elevenlabs ≈124.

- [ ] **Step 4: Commit**

```bash
git add docs/tools/development_ops/llmfit.md docs/tools/benchmarking/helm.md docs/tools/benchmarking/evalplus.md docs/tools/frameworks/firebase-genkit.md docs/tools/frameworks/instructor.md docs/tools/development_ops/google-stitch.md docs/tools/infrastructure/aphrodite-engine.md docs/tools/ai_knowledge/elevenlabs.md
git commit -m "docs(tools): enrich tool docs — llmfit, helm, evalplus, firebase-genkit, instructor, aphrodite-engine"
```

---

### Task 6: Apply knowledge base and patterns

**Source branches:** batch-111, batch-100, audit-batch-june-07

**Files:**
- Modify: `docs/knowledge_base/patterns/data-copilot-agentic-rag.md`
- Modify: `docs/knowledge_base/ai_company_starter_stack.md`
- Modify: `docs/knowledge_base/ai_reading_list.md`
- Modify: `docs/knowledge_base/patterns/openclaw-use-case-catalog.md`
- Modify: `docs/knowledge_base/home-admin-agent-architecture.md`
- Modify: `docs/reference-implementations/data-copilot/skeleton-guide.md`
- Modify: `docs/playbooks/knowledge-base-health.md`

- [ ] **Step 1: Extract from batch-111**

```bash
B111="origin/ralph-loop-batch-111-4109746271122170512"
git show $B111:docs/knowledge_base/patterns/data-copilot-agentic-rag.md > docs/knowledge_base/patterns/data-copilot-agentic-rag.md
git show $B111:docs/reference-implementations/data-copilot/skeleton-guide.md > docs/reference-implementations/data-copilot/skeleton-guide.md
```

- [ ] **Step 2: Extract from batch-100**

```bash
B100="origin/ralph-loop-batch-100-12179161220186892849"
git show $B100:docs/knowledge_base/patterns/openclaw-use-case-catalog.md > docs/knowledge_base/patterns/openclaw-use-case-catalog.md
```

- [ ] **Step 3: Extract from audit-batch-june-07**

```bash
BJUN="origin/jules/audit-batch-june-07-9101608677968828562"
git show $BJUN:docs/knowledge_base/ai_company_starter_stack.md > docs/knowledge_base/ai_company_starter_stack.md
git show $BJUN:docs/knowledge_base/ai_reading_list.md > docs/knowledge_base/ai_reading_list.md
git show $BJUN:docs/knowledge_base/home-admin-agent-architecture.md > docs/knowledge_base/home-admin-agent-architecture.md
git show $BJUN:docs/playbooks/knowledge-base-health.md > docs/playbooks/knowledge-base-health.md
```

- [ ] **Step 4: Verify line counts**

```bash
wc -l docs/knowledge_base/patterns/data-copilot-agentic-rag.md docs/knowledge_base/ai_company_starter_stack.md docs/knowledge_base/ai_reading_list.md docs/knowledge_base/patterns/openclaw-use-case-catalog.md docs/knowledge_base/home-admin-agent-architecture.md docs/reference-implementations/data-copilot/skeleton-guide.md docs/playbooks/knowledge-base-health.md
```

Expected: data-copilot-agentic-rag ≈177, ai_company_starter_stack ≈306, ai_reading_list ≈140, openclaw-use-case-catalog ≈133, home-admin-agent-architecture ≈138, skeleton-guide ≈89, knowledge-base-health ≈149.

- [ ] **Step 5: Commit**

```bash
git add docs/knowledge_base/patterns/data-copilot-agentic-rag.md docs/knowledge_base/ai_company_starter_stack.md docs/knowledge_base/ai_reading_list.md docs/knowledge_base/patterns/openclaw-use-case-catalog.md docs/knowledge_base/home-admin-agent-architecture.md docs/reference-implementations/data-copilot/skeleton-guide.md docs/playbooks/knowledge-base-health.md
git commit -m "docs(kb): enrich knowledge base — agentic-rag, starter-stack, reading-list, openclaw catalog, home-admin arch"
```

---

### Task 7: Add new heygen.md and update mkdocs.yml

**Files:**
- Create: `docs/tools/ai_knowledge/heygen.md`
- Modify: `mkdocs.yml` (add nav entry)

- [ ] **Step 1: Extract heygen.md from source branch**

```bash
git show origin/ralph-loop-batch-56-60-14332896274658620492:docs/tools/ai_knowledge/heygen.md > docs/tools/ai_knowledge/heygen.md
```

- [ ] **Step 2: Verify file was created with content**

```bash
wc -l docs/tools/ai_knowledge/heygen.md
head -5 docs/tools/ai_knowledge/heygen.md
```

Expected: ≈80 lines; first line `# HeyGen`.

- [ ] **Step 3: Add HeyGen to mkdocs.yml nav (alphabetically between Heretic/ARA and HoloTab)**

Open `mkdocs.yml`. Find the line:
```yaml
          - Heretic / ARA: tools/ai_knowledge/heretic-ara.md
```
Insert immediately after it:
```yaml
          - HeyGen: tools/ai_knowledge/heygen.md
```

- [ ] **Step 4: Validate mkdocs.yml YAML syntax**

```bash
ruby -ryaml -e 'YAML.load_file("mkdocs.yml"); puts "OK"'
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add docs/tools/ai_knowledge/heygen.md mkdocs.yml
git commit -m "docs(tools): add HeyGen AI video platform doc and nav entry"
```

---

### Task 8: Add new scripts

**Source branch:** `origin/ralph-loop-batch-94-resolution-4332415108223708556` (sql scripts), `origin/ralph-loop-batch-100-12179161220186892849` (find_oldest_docs.py), `origin/issue-resolution-batch-freshness-audit-10508511053722809236` (find_oldest_issues.py)

**Files:**
- Create: `scripts/sql_validator.py`
- Create: `scripts/test_sql_validator.py`
- Create: `scripts/verify_node_headscale.py`
- Create: `find_oldest_docs.py`
- Create: `find_oldest_issues.py`

- [ ] **Step 1: Extract scripts from batch-94**

```bash
B94="origin/ralph-loop-batch-94-resolution-4332415108223708556"
git show $B94:scripts/sql_validator.py > scripts/sql_validator.py
git show $B94:scripts/test_sql_validator.py > scripts/test_sql_validator.py
git show $B94:scripts/verify_node_headscale.py > scripts/verify_node_headscale.py
```

- [ ] **Step 2: Extract utility scripts**

```bash
git show origin/ralph-loop-batch-100-12179161220186892849:find_oldest_docs.py > find_oldest_docs.py
git show origin/issue-resolution-batch-freshness-audit-10508511053722809236:find_oldest_issues.py > find_oldest_issues.py
```

- [ ] **Step 3: Verify all five files exist and are non-empty**

```bash
wc -l scripts/sql_validator.py scripts/test_sql_validator.py scripts/verify_node_headscale.py find_oldest_docs.py find_oldest_issues.py
```

Expected: all files > 10 lines each.

- [ ] **Step 4: Commit**

```bash
git add scripts/sql_validator.py scripts/test_sql_validator.py scripts/verify_node_headscale.py find_oldest_docs.py find_oldest_issues.py
git commit -m "scripts: add sql_validator, verify_node_headscale, find_oldest_docs/issues utilities"
```

---

### Task 9: Push branch and open PR

- [ ] **Step 1: Push branch to origin**

```bash
git push -u origin feat/cherry-pick-major-gains-from-closed-prs
```

- [ ] **Step 2: Verify final diff stats**

```bash
git diff main...HEAD --stat | tail -5
```

Expected: 35 files changed, several hundred insertions.

- [ ] **Step 3: Open PR**

```bash
gh pr create --title "docs: apply major gains from 16 closed PRs" --body "$(cat <<'EOF'
## Summary

Extracts the richest documentation and script content from 16 PRs that were closed due to merge conflicts, and applies it cleanly on top of current `main`.

**Selection criteria:** files where the branch version had ≥20 more lines than main (genuine content enrichment), new files not present in main, and new utility scripts.

- **1 new tool doc**: `heygen.md` (HeyGen AI video platform) + mkdocs.yml nav entry
- **15 enriched service docs**: tubearchivist (+176 ln), vikunja, navidrome, syncthing, gitea, jellyfin, jackett, habitica, grocy, trilium, actual-budget, focalboard, plex, it-tools, plex-automation
- **8 enriched tool docs**: llmfit, helm, evalplus, firebase-genkit, instructor, google-stitch, aphrodite-engine, elevenlabs
- **7 enriched KB/patterns/playbooks**: data-copilot-agentic-rag, ai_company_starter_stack, ai_reading_list, openclaw-use-case-catalog, home-admin-architecture, skeleton-guide, knowledge-base-health
- **5 new scripts**: sql_validator.py, test_sql_validator.py, verify_node_headscale.py, find_oldest_docs.py, find_oldest_issues.py

## Source PRs

Closed PRs: #619, #646, #656, #694, #704, #708, #709, #714, #722, #738, #757, #762, #772, #779, #797, #803

## Test plan

- [ ] YAML validation passes: `ruby -ryaml -e 'YAML.load_file("mkdocs.yml"); puts "OK"'`
- [ ] `heygen.md` renders correctly in nav
- [ ] All modified files are longer than their previous main versions
- [ ] Scripts are syntactically valid: `python3 -m py_compile scripts/sql_validator.py scripts/test_sql_validator.py scripts/verify_node_headscale.py find_oldest_docs.py find_oldest_issues.py`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Expected: PR URL printed to stdout.

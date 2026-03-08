#!/usr/bin/env python3
"""
Open up to N scoped Jules sprint issues (one open issue per worker slot).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from typing import Any


LANES = [
    {
        "worker": "W1",
        "focus": "Services (A-H)",
        "scope": [
            "docs/services/actual-budget.md",
            "docs/services/audiobookshelf.md",
            "docs/services/authentik.md",
            "docs/services/changedetection.md",
            "docs/services/diskover.md",
            "docs/services/drawio.md",
            "docs/services/element.md",
            "docs/services/excalidraw.md",
            "docs/services/focalboard.md",
            "docs/services/gitea.md",
            "docs/services/grocy.md",
            "docs/services/habitica.md",
            "docs/services/home-assistant.md",
            "docs/services/homebox.md",
        ],
    },
    {
        "worker": "W2",
        "focus": "Services (I-P)",
        "scope": [
            "docs/services/immich.md",
            "docs/services/inventory.md",
            "docs/services/it-tools.md",
            "docs/services/jackett.md",
            "docs/services/jellyfin.md",
            "docs/services/kiwix.md",
            "docs/services/linkwarden.md",
            "docs/services/litellm.md",
            "docs/services/mealie.md",
            "docs/services/metube.md",
            "docs/services/minecraft.md",
            "docs/services/n8n.md",
            "docs/services/navidrome.md",
            "docs/services/nextcloud.md",
            "docs/services/ollama.md",
            "docs/services/omni-tools.md",
            "docs/services/open-webui.md",
            "docs/services/paperless-ai.md",
            "docs/services/paperless-ngx.md",
            "docs/services/plex.md",
            "docs/services/portracker.md",
        ],
    },
    {
        "worker": "W3",
        "focus": "Services (Q-Z)",
        "scope": [
            "docs/services/qbittorrent.md",
            "docs/services/radicale.md",
            "docs/services/rclone-automation.md",
            "docs/services/searXNG.md",
            "docs/services/speedtest.md",
            "docs/services/storj.md",
            "docs/services/syncthing.md",
            "docs/services/tailscale.md",
            "docs/services/tika.md",
            "docs/services/trilium.md",
            "docs/services/tubearchivist.md",
            "docs/services/vikunja.md",
            "docs/services/whisper.md",
        ],
    },
    {
        "worker": "W4",
        "focus": "AI knowledge and providers",
        "scope": [
            "docs/tools/ai_knowledge/",
            "docs/tools/providers/",
        ],
    },
    {
        "worker": "W5",
        "focus": "Development and ops tools",
        "scope": [
            "docs/tools/development_ops/",
        ],
    },
    {
        "worker": "W6",
        "focus": "Benchmarks, infra, frameworks, orchestration",
        "scope": [
            "docs/tools/benchmarking/",
            "docs/tools/infrastructure/",
            "docs/tools/frameworks/",
            "docs/tools/agents/",
            "docs/tools/orchestration/",
            "docs/tools/automation_orchestration/",
            "docs/tools/process_understanding/",
        ],
    },
    {
        "worker": "W7",
        "focus": "Playbooks and reference implementations",
        "scope": [
            "docs/playbooks/",
            "docs/reference-implementations/",
        ],
    },
    {
        "worker": "W8",
        "focus": "Knowledge base and architecture",
        "scope": [
            "docs/knowledge_base/",
            "docs/architecture/",
        ],
    },
    {
        "worker": "W9",
        "focus": "Intake, taxonomy, registry consistency",
        "scope": [
            "docs/new-sources.md",
            "docs/new-sources/",
            "docs/standards.md",
            "data/all_tools.json",
            "mkdocs.yml",
        ],
    },
]


def run_gh(args: list[str], repo: str) -> str:
    env = os.environ.copy()
    cmd = ["gh"] + args + ["--repo", repo]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
    return result.stdout.strip()


def json_issue_list(search: str, repo: str) -> list[dict[str, Any]]:
    out = run_gh(
        ["issue", "list", "--label", "jules-sprint", "--state", "open", "--search", search, "--json", "number,title"],
        repo,
    )
    if not out:
        return []
    return json.loads(out)


def build_body(worker: str, focus: str, scope: list[str]) -> str:
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    scope_lines = "\n".join(f"- `{item}`" for item in scope)
    return f"""## Jules Sprint {worker} - Autonomous Improvement

Run window: 2-week sprint. Generated at {today}.

### Focus lane
{focus}

### Allowed scope (hard boundary)
{scope_lines}

### Mission
Improve the repository with additive, source-backed updates emphasizing:
- FREE/open AI tooling where possible
- local AI and local LLM usage patterns
- token-efficiency and value-per-token guidance
- broad provider ecosystem coverage

### Non-negotiable rules
1. Additive-only: do NOT remove files/sections/content.
2. Edit only files in allowed scope (except required registry/nav updates when creating a new canonical page).
3. If work overlaps a recently changed file (last 24h), pick another file in scope.
4. Max 6 files changed.
5. One coherent intent only.

### Suggested work order
1. Pick 1-2 shallow docs in your scope and deepen with runnable examples.
2. Add 1-2 high-signal sources and a brief “What changed” note.
3. Improve related-tool links within scope.
4. If scope includes intake/registry, process up to 3 `new` intake rows.

### Required checks before opening PR
- `python3 -c "import yaml; yaml.safe_load(open('mkdocs.yml')); print('OK')"`
- `python3 scripts/validate_new_sources.py`
- `python3 scripts/check_catalog_consistency.py`
- `CHANGED_DOCS=$(git diff --name-only origin/main...HEAD | grep '^docs/.*\\.md$' || true); if [ -n "$CHANGED_DOCS" ]; then python3 scripts/check_docs_contract.py $CHANGED_DOCS; fi`

### PR title
`docs: jules sprint {worker} YYYY-MM-DD HHMM UTC`
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Open scoped Jules sprint issues.")
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--target-workers", type=int, default=9, help="Max worker slots to keep open")
    args = parser.parse_args()

    target = max(1, min(args.target_workers, len(LANES)))
    created = 0

    for lane in LANES[:target]:
        worker = lane["worker"]
        existing = json_issue_list(f'"[{worker}] Jules Sprint"', args.repo)
        if existing:
            print(f"Skip {worker}: open sprint issue already exists.")
            continue

        title = f"[{worker}] Jules Sprint - {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H%M UTC')}"
        body = build_body(worker, lane["focus"], lane["scope"])
        run_gh(
            ["issue", "create", "--title", title, "--label", "jules", "--label", "jules-sprint", "--body", body],
            args.repo,
        )
        created += 1
        print(f"Created sprint issue for {worker}.")

    print(f"Done. Created {created} issue(s).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        raise SystemExit(exc.returncode)

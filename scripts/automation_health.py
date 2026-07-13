#!/usr/bin/env python3
"""
Automation health watchdog — observability + transient-failure recovery.

The unattended pipeline has many scheduled lanes that can fail (OpenRouter
blips, GitHub API hiccups) or silently stop (GitHub disables schedules on
inactive repos, a lane keeps erroring). Nothing surfaced that before: you had
to browse the Actions tab. This watchdog:

  1. Discovers every scheduled workflow by scanning .github/workflows/*.yml
     for cron triggers (new lanes are covered automatically).
  2. Checks each lane's latest completed run and the age of its last success,
     with a stall threshold derived from the lane's own cadence
     (daily -> 2 days, weekly -> 9 days, monthly -> 35 days).
  3. Flags workflows GitHub has disabled (manual or 60-day inactivity).
  4. Auto-reruns a failed run's failed jobs ONCE (attempt 1, <24h old) so
     transient failures self-heal without waiting a full schedule cycle.
  5. Maintains ONE singleton `automation-health`-labelled issue: opened or
     updated in place while lanes need attention, closed when all green.

Usage:
  python3 scripts/automation_health.py            # scan + rerun + issue upkeep
  python3 scripts/automation_health.py --dry-run  # report only, no writes
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOWS_DIR = REPO_ROOT / ".github" / "workflows"

HEALTH_LABEL = "automation-health"
ISSUE_MARKER = "<!-- automation-health-report -->"
FAILING_CONCLUSIONS = {"failure", "timed_out", "startup_failure"}
RERUN_MAX_AGE_HOURS = 24

# Stall thresholds by cadence: a lane is stalled when its last successful run
# is older than this, i.e. it has missed several of its own schedule slots.
STALL_THRESHOLDS = {
    "daily": timedelta(days=2),
    "weekly": timedelta(days=9),
    "monthly": timedelta(days=35),
}

CRON_RE = re.compile(r"^\s*-\s*cron:\s*[\"']?([0-9*,/\- ]+?)[\"']?\s*(?:#.*)?$")


def run_gh(args: list[str], check: bool = True) -> str:
    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY")
    cmd = ["gh", *args]
    # gh infers the repo from the cwd git remote for local runs; in Actions we
    # pass it explicitly (except for `gh api`, whose paths name the repo).
    if repo and args[0] != "api":
        cmd += ["--repo", repo]
    result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if result.returncode != 0 and check:
        raise RuntimeError(result.stderr.strip() or f"gh {args[0]} failed")
    return result.stdout


def cadence_of(cron: str) -> str:
    """Classify a cron expression as daily/weekly/monthly by its date fields."""
    fields = cron.split()
    if len(fields) != 5:
        return "daily"  # be strict rather than miss a stall
    _minute, _hour, dom, _month, dow = fields
    if dom != "*":
        return "monthly"
    if dow != "*":
        return "weekly"
    return "daily"


def discover_scheduled_workflows() -> list[dict]:
    """Every workflow with a cron trigger, with its tightest stall threshold."""
    lanes = []
    for wf in sorted(WORKFLOWS_DIR.glob("*.yml")):
        text = wf.read_text(encoding="utf-8")
        crons = [m.group(1).strip() for line in text.splitlines()
                 if (m := CRON_RE.match(line))]
        if not crons:
            continue
        name_match = re.search(r"^name:\s*[\"']?(.+?)[\"']?\s*$", text, re.MULTILINE)
        cadences = {cadence_of(c) for c in crons}
        # Most frequent cadence wins: a lane that also runs daily must not get
        # a monthly grace period.
        cadence = ("daily" if "daily" in cadences
                   else "weekly" if "weekly" in cadences else "monthly")
        lanes.append({
            "file": wf.name,
            "name": name_match.group(1) if name_match else wf.name,
            "crons": crons,
            "cadence": cadence,
            "threshold": STALL_THRESHOLDS[cadence],
        })
    return lanes


def workflow_states() -> dict[str, str]:
    """Map workflow file name -> GitHub state (active / disabled_*)."""
    out = run_gh(["api", "repos/{owner}/{repo}/actions/workflows",
                  "--paginate", "--jq", ".workflows[] | {path, state}"])
    states = {}
    for line in out.splitlines():
        item = json.loads(line)
        states[Path(item["path"]).name] = item["state"]
    return states


def recent_runs(workflow_file: str) -> list[dict]:
    out = run_gh(["run", "list", "--workflow", workflow_file, "--limit", "20",
                  "--json", "databaseId,conclusion,status,createdAt,attempt"])
    return json.loads(out) if out.strip() else []


def parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def assess_lane(lane: dict, state: str | None, runs: list[dict],
                now: datetime, dry_run: bool) -> dict:
    """Return a health verdict for one lane, dispatching a one-shot rerun if due."""
    result = {"lane": lane, "status": "ok", "notes": [], "rerun": None}

    if state is None:
        # Exists locally but not on the default branch yet (e.g. this very
        # branch adds it). It will register on merge; nothing to check.
        result["notes"].append("not registered on GitHub yet — skipping run checks")
        return result
    if state != "active":
        result["status"] = "problem"
        result["notes"].append(f"workflow is `{state}` on GitHub — schedule is not running")

    completed = [r for r in runs if r["status"] == "completed"]
    if not completed:
        result["notes"].append("no completed runs found yet")
        return result

    latest = completed[0]
    last_success = next((r for r in completed if r["conclusion"] == "success"), None)

    if last_success is None:
        result["status"] = "problem"
        result["notes"].append("no successful run in the last 20 runs")
    else:
        age = now - parse_ts(last_success["createdAt"])
        if age > lane["threshold"]:
            result["status"] = "problem"
            result["notes"].append(
                f"stalled: last success {age.days}d ago (threshold {lane['threshold'].days}d)")

    if latest["conclusion"] in FAILING_CONCLUSIONS:
        result["status"] = "problem"
        result["notes"].append(f"latest run concluded `{latest['conclusion']}`")
        run_age = now - parse_ts(latest["createdAt"])
        running = any(r["status"] != "completed" for r in runs)
        if (latest["attempt"] == 1
                and run_age < timedelta(hours=RERUN_MAX_AGE_HOURS)
                and not running):
            if dry_run:
                result["rerun"] = f"would rerun failed jobs of run {latest['databaseId']}"
            else:
                try:
                    run_gh(["run", "rerun", str(latest["databaseId"]), "--failed"])
                    result["rerun"] = f"auto-rerun dispatched for run {latest['databaseId']}"
                except RuntimeError as exc:
                    result["rerun"] = f"rerun failed: {exc}"
            result["notes"].append(result["rerun"])
        elif latest["attempt"] > 1:
            result["notes"].append("already rerun once — needs a human look")

    return result


def build_report(results: list[dict], now: datetime) -> str:
    icon = {"ok": "✅", "problem": "❌"}
    lines = [ISSUE_MARKER, "# Automation health report",
             f"_Scanned {now.strftime('%Y-%m-%d %H:%M UTC')} by `automation-health.yml`._", ""]
    problems = [r for r in results if r["status"] == "problem"]
    if problems:
        lines.append("## Lanes needing attention")
        for r in problems:
            lines.append(f"- {icon['problem']} **{r['lane']['name']}** (`{r['lane']['file']}`)")
            for note in r["notes"]:
                lines.append(f"    - {note}")
        lines.append("")
    lines.append("## All monitored lanes")
    for r in results:
        note = f" — {'; '.join(r['notes'])}" if r["notes"] else ""
        lines.append(f"- {icon[r['status']]} {r['lane']['name']} ({r['lane']['cadence']}){note}")
    lines.append("")
    lines.append("_This issue is maintained automatically: it is updated in place while "
                 "problems persist and closed when every lane is green again._")
    return "\n".join(lines)


def find_health_issue() -> int | None:
    out = run_gh(["issue", "list", "--state", "open", "--label", HEALTH_LABEL,
                  "--json", "number"])
    issues = json.loads(out) if out.strip() else []
    return issues[0]["number"] if issues else None


def ensure_health_label() -> None:
    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY")
    probe = subprocess.run(["gh", "api", f"repos/{repo}/labels/{HEALTH_LABEL}"]
                           if repo else
                           ["gh", "api", "repos/{owner}/{repo}/labels/" + HEALTH_LABEL],
                           capture_output=True, text=True)
    if probe.returncode != 0:
        run_gh(["label", "create", HEALTH_LABEL, "--color", "b60205",
                "--description", "Singleton automation health report issue"])


def sync_issue(results: list[dict], report: str, dry_run: bool) -> None:
    problems = sum(1 for r in results if r["status"] == "problem")
    existing = find_health_issue()

    if problems == 0:
        if existing is None:
            print("All lanes green; no health issue open. Nothing to do.")
        elif dry_run:
            print(f"DRY RUN: would close health issue #{existing} (all lanes green).")
        else:
            run_gh(["issue", "close", str(existing), "--comment",
                    "All monitored lanes are green again — closing automatically."])
            print(f"Closed health issue #{existing} (all lanes green).")
        return

    title = f"Automation health: {problems} lane(s) need attention"
    if dry_run:
        action = f"update #{existing}" if existing else "open a new issue"
        print(f"DRY RUN: {problems} problem lane(s); would {action} titled {title!r}.")
        return

    ensure_health_label()
    if existing is None:
        run_gh(["issue", "create", "--title", title, "--body", report,
                "--label", HEALTH_LABEL])
        print(f"Opened health issue: {title}")
    else:
        run_gh(["issue", "edit", str(existing), "--title", title, "--body", report])
        print(f"Updated health issue #{existing}: {title}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Scheduled-lane health watchdog.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Report only: no reruns, no issue writes.")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    lanes = discover_scheduled_workflows()
    if not lanes:
        print("No scheduled workflows found — nothing to monitor.", file=sys.stderr)
        return 1
    states = workflow_states()

    results = []
    for lane in lanes:
        state = states.get(lane["file"])
        runs = recent_runs(lane["file"]) if state is not None else []
        results.append(assess_lane(lane, state, runs, now, args.dry_run))

    report = build_report(results, now)
    print(report)
    sync_issue(results, report, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

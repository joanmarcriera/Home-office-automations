#!/usr/bin/env python3
"""
Move failed Google Jules issues out of the active automation lane.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys

BLOCKED_LABEL = "jules-blocked"
CONTROL_PREFIXES = (
    "daily maintenance run - ",
    "daily knowledge expansion - ",
    "process jules backlog - ",
    "weekly deepening:",
    "category gap fill:",
)
FAILURE_MARKER = "failed to create a task"
HYGIENE_COMMENT = (
    "Automation hygiene: Google Jules reported task-creation failure, so this issue "
    "was moved from `jules` to `jules-blocked`. Remove `jules-blocked` and re-add "
    "`jules` when you want to retry it."
)


def run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "gh command failed")
    return result.stdout


def ensure_blocked_label(repo: str) -> None:
    try:
        run_gh(["api", f"repos/{repo}/labels/{BLOCKED_LABEL}"])
    except RuntimeError:
        run_gh(
            [
                "label",
                "create",
                BLOCKED_LABEL,
                "--repo",
                repo,
                "--color",
                "d29922",
                "--description",
                "Issues blocked because Google Jules failed to create a task",
            ]
        )


def is_control_issue(title: str) -> bool:
    title_lower = title.lower()
    return any(title_lower.startswith(prefix) for prefix in CONTROL_PREFIXES)


def has_failed_task_comment(issue: dict) -> bool:
    for comment in issue.get("comments", []):
        author = (comment.get("author") or {}).get("login", "")
        body = (comment.get("body") or "").lower()
        if author == "google-labs-jules" and FAILURE_MARKER in body:
            return True
    return False


def has_automation_hygiene_comment(issue: dict) -> bool:
    for comment in issue.get("comments", []):
        body = comment.get("body") or ""
        if body == HYGIENE_COMMENT:
            return True
    return False


def main() -> int:
    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        print("REPO or GITHUB_REPOSITORY must be set.", file=sys.stderr)
        return 1

    ensure_blocked_label(repo)

    issues = json.loads(
        run_gh(
            [
                "issue",
                "list",
                "--repo",
                repo,
                "--state",
                "open",
                "--label",
                "jules",
                "--limit",
                "200",
                "--json",
                "number,title",
            ]
        )
    )

    quarantined = 0
    for issue in issues:
        if is_control_issue(issue.get("title", "")):
            continue

        number = str(issue["number"])
        details = json.loads(
            run_gh(
                [
                    "issue",
                    "view",
                    number,
                    "--repo",
                    repo,
                    "--json",
                    "comments,labels,title",
                ]
            )
        )

        if not has_failed_task_comment(details):
            continue

        run_gh(
            [
                "issue",
                "edit",
                number,
                "--repo",
                repo,
                "--remove-label",
                "jules",
                "--add-label",
                BLOCKED_LABEL,
            ]
        )

        if not has_automation_hygiene_comment(details):
            run_gh(
                [
                    "issue",
                    "comment",
                    number,
                    "--repo",
                    repo,
                    "--body",
                    HYGIENE_COMMENT,
                ]
            )

        quarantined += 1
        print(f"Quarantined issue #{number}: {details.get('title', '')}")

    print(f"Quarantined {quarantined} failed Jules issue(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

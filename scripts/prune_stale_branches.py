#!/usr/bin/env python3
"""
Prune stale remote branches — safely, capped, dry-run by default.

Bot lanes (Jules, ralph-loop audits, freshness batches) leave one branch per PR
behind; GitHub's "auto-delete head branches" does not cover PRs merged by the
GITHUB_TOKEN or closed unmerged, so hundreds accumulate. This deletes a branch
ONLY when every safety rule holds:

  Never touched:
    - the default branch, `gh-pages`, anything under `automation/`, and any
      branch matching --keep (regex, repeatable) or a classic protection rule
    - the head OR base branch of any OPEN pull request (deleting a base branch
      would close the PRs stacked on it)
    - branches whose tip commit is younger than --min-age-days (an agent may
      have just pushed and not opened its PR yet)

  Deleted only if one of:
    - merged: every commit on the branch is already in the default branch
      (GraphQL compare: behindBy == 0), or
    - closed-PR: its most recent PR is MERGED or CLOSED and the branch tip is
      still exactly that PR's head commit (nothing pushed after it closed).
      Commits stay reachable through the PR (refs/pull/N/head) and the branch
      can be restored from the PR page.

At most --max-deletions branches are deleted per run (oldest first), so a bad
rule can never mass-delete. Without --apply nothing is written.

Usage:
  python3 scripts/prune_stale_branches.py                       # dry run (default)
  python3 scripts/prune_stale_branches.py --apply --max-deletions 50
  REPO=owner/name python3 scripts/prune_stale_branches.py --json

Needs `gh` authenticated with contents:write (delete) / read (dry run).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

ALWAYS_KEEP = [r"^gh-pages$", r"^automation/"]

REFS_QUERY = """
query($owner: String!, $name: String!, $cursor: String, $base: String!) {
  repository(owner: $owner, name: $name) {
    refs(refPrefix: "refs/heads/", first: 50, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name
        branchProtectionRule { id }
        target { ... on Commit { oid committedDate } }
        compare(headRef: $base) { behindBy }
        associatedPullRequests(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes { number state headRefOid }
        }
      }
    }
  }
}
"""

OPEN_PRS_QUERY = """
query($owner: String!, $name: String!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequests(states: OPEN, first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes { headRefName baseRefName headRepository { nameWithOwner } }
    }
  }
}
"""


def gh(args: list[str]) -> str:
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"gh {' '.join(args[:2])} failed")
    return result.stdout


def graphql(query: str, **variables: str | None) -> dict:
    args = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if value is not None:
            args += ["-f", f"{key}={value}"]
    data = json.loads(gh(args))
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:500])
    return data["data"]


def paged(query: str, path: str, **variables: str) -> list[dict]:
    """Collect every node of a paginated connection (path = repository.<conn>)."""
    nodes, cursor = [], None
    while True:
        data = graphql(query, cursor=cursor, **variables)["repository"][path]
        nodes += data["nodes"]
        if not data["pageInfo"]["hasNextPage"]:
            return nodes
        cursor = data["pageInfo"]["endCursor"]


def classify(ref: dict, default: str, keep: list[re.Pattern], open_refs: set[str],
             cutoff: datetime) -> tuple[str, str]:
    """Return (verdict, reason); verdict is 'delete' or 'keep'."""
    name = ref["name"]
    if name == default:
        return "keep", "default branch"
    if any(p.search(name) for p in keep):
        return "keep", "protected name"
    if ref.get("branchProtectionRule"):
        return "keep", "branch protection rule"
    if name in open_refs:
        return "keep", "head/base of an open PR"
    target = ref.get("target") or {}
    if not target.get("committedDate"):
        return "keep", "tip is not a commit"
    tip_date = datetime.fromisoformat(target["committedDate"].replace("Z", "+00:00"))
    if tip_date > cutoff:
        return "keep", "tip too recent"
    prs = (ref.get("associatedPullRequests") or {}).get("nodes") or []
    if any(pr["state"] == "OPEN" for pr in prs):
        return "keep", "open PR"
    compare = ref.get("compare") or {}
    if compare.get("behindBy") == 0:
        return "delete", "merged (all commits in default branch)"
    if prs and prs[0]["state"] in ("MERGED", "CLOSED") and prs[0]["headRefOid"] == target["oid"]:
        return "delete", f"PR #{prs[0]['number']} {prs[0]['state'].lower()}, tip unchanged since"
    return "keep", "unmerged commits without a closed PR"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--apply", action="store_true", help="Actually delete (default: dry run).")
    parser.add_argument("--max-deletions", type=int, default=50, help="Per-run cap (default 50).")
    parser.add_argument("--min-age-days", type=float, default=3, help="Skip tips younger than this.")
    parser.add_argument("--keep", action="append", default=[], help="Extra regex of branches to keep.")
    parser.add_argument("--json", action="store_true", help="Print a JSON summary at the end.")
    args = parser.parse_args()

    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        repo = gh(["repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"]).strip()
    owner, name = repo.split("/", 1)
    default = gh(["api", f"repos/{repo}", "--jq", ".default_branch"]).strip()

    keep = [re.compile(p) for p in ALWAYS_KEEP + args.keep]
    open_refs: set[str] = set()
    for pr in paged(OPEN_PRS_QUERY, "pullRequests", owner=owner, name=name):
        open_refs.add(pr["baseRefName"])
        if (pr.get("headRepository") or {}).get("nameWithOwner") == repo:
            open_refs.add(pr["headRefName"])

    refs = paged(REFS_QUERY, "refs", owner=owner, name=name, base=default)
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.min_age_days)

    candidates, kept = [], {}
    for ref in refs:
        verdict, reason = classify(ref, default, keep, open_refs, cutoff)
        if verdict == "delete":
            candidates.append((ref["target"]["committedDate"], ref["name"], reason))
        else:
            kept[reason] = kept.get(reason, 0) + 1
    candidates.sort()  # oldest tip first

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"[{mode}] {repo}: {len(refs)} branches scanned, {len(candidates)} deletable, "
          f"cap {args.max_deletions} per run.")
    for reason, count in sorted(kept.items(), key=lambda kv: -kv[1]):
        print(f"  kept {count:4d}: {reason}")

    deleted, failed = [], []
    for tip, branch, reason in candidates[: max(args.max_deletions, 0)]:
        if not args.apply:
            print(f"  would delete {branch}  ({reason}; tip {tip[:10]})")
            continue
        try:
            gh(["api", "-X", "DELETE", f"repos/{repo}/git/refs/heads/{branch}"])
            deleted.append(branch)
            print(f"  deleted {branch}  ({reason}; tip {tip[:10]})")
        except RuntimeError as exc:  # e.g. already gone; keep going
            failed.append(branch)
            print(f"  WARNING: could not delete {branch}: {exc}")
    remaining = max(len(candidates) - args.max_deletions, 0)
    if remaining:
        print(f"{remaining} more deletable branch(es) left for later runs (cap reached).")
    print(f"Summary: candidates={len(candidates)} deleted={len(deleted)} failed={len(failed)} "
          f"mode={mode}")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(f"### Branch cleanup ({mode})\n\n- scanned: {len(refs)}\n"
                     f"- deletable: {len(candidates)}\n- deleted this run: {len(deleted)}\n"
                     f"- failed: {len(failed)}\n- per-run cap: {args.max_deletions}\n")
    if args.json:
        print(json.dumps({"scanned": len(refs), "candidates": len(candidates),
                          "deleted": deleted, "failed": failed, "kept": kept}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

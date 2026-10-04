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
    - the base of any open PR (deleting it would close the PRs stacked on it)
      and the head of any open PR whose head repository is THIS repository
    - branches whose tip commit is younger than --min-age-days (an agent may
      have just pushed and not opened its PR yet)

  Deleted only if one of:
    - merged: every commit on the branch is already in the default branch
      (GraphQL compare: behindBy == 0), or
    - closed-PR: its most recent PR *from this repository and this exact ref*
      is MERGED or CLOSED and the branch tip is still that PR's head commit
      (nothing pushed after it closed). Commits stay reachable through the PR
      (refs/pull/N/head) and the branch can be restored from the PR page.

  PR matching is always by (head repository, head ref name) — never by name
  alone — so a fork PR whose head branch happens to share a name with a branch
  here can neither protect it nor make it look "closed".

  Deletion is a compare-and-swap (GraphQL updateRefs with beforeOid = the tip
  that was evaluated): if anyone pushed to the branch since the scan, GitHub
  rejects the delete. The open-PR set is also re-read right before deleting.

At most --max-deletions branches are deleted per run (oldest first), so a bad
rule can never mass-delete. Without --apply nothing is written.

Usage:
  python3 scripts/prune_stale_branches.py                       # dry run (default)
  python3 scripts/prune_stale_branches.py --apply --max-deletions 50
  REPO=owner/name python3 scripts/prune_stale_branches.py --json

Needs `gh` authenticated with contents:write (delete) / read (dry run).
Tests: python3 -m unittest scripts/test_prune_stale_branches.py
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
ZERO_OID = "0" * 40

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
        associatedPullRequests(first: 10, orderBy: {field: UPDATED_AT, direction: DESC}) {
          nodes { number state headRefName headRefOid headRepository { nameWithOwner } }
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

# Atomic compare-and-swap delete: rejected unless the ref still points at $before.
DELETE_MUTATION = """
mutation($repo: ID!, $ref: GitRefname!, $before: GitObjectID!) {
  updateRefs(input: {repositoryId: $repo, refUpdates: [
    {name: $ref, beforeOid: $before, afterOid: "%s", force: false}
  ]}) { clientMutationId }
}
""" % ZERO_OID


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


def head_repo(pr: dict) -> str | None:
    return (pr.get("headRepository") or {}).get("nameWithOwner")


def open_pr_refs(prs: list[dict], repo: str) -> set[str]:
    """Branch names in `repo` that an open PR depends on.

    Base branches always live in `repo`. A head branch only counts when the
    PR's head repository is `repo` itself: a fork PR's head is a branch in the
    fork, even if it shares a name with one here.
    """
    refs: set[str] = set()
    for pr in prs:
        refs.add(pr["baseRefName"])
        if head_repo(pr) == repo:
            refs.add(pr["headRefName"])
    return refs


def own_prs(ref: dict, repo: str) -> list[dict]:
    """The ref's PRs whose head is exactly (repo, ref name), newest first."""
    prs = (ref.get("associatedPullRequests") or {}).get("nodes") or []
    return [pr for pr in prs
            if head_repo(pr) == repo and pr.get("headRefName") == ref["name"]]


def classify(ref: dict, default: str, keep: list[re.Pattern], open_refs: set[str],
             cutoff: datetime, repo: str) -> tuple[str, str]:
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
    if not target.get("committedDate") or not target.get("oid"):
        return "keep", "tip is not a commit"
    tip_date = datetime.fromisoformat(target["committedDate"].replace("Z", "+00:00"))
    if tip_date > cutoff:
        return "keep", "tip too recent"
    prs = own_prs(ref, repo)
    if any(pr["state"] == "OPEN" for pr in prs):
        return "keep", "open PR"
    compare = ref.get("compare") or {}
    if compare.get("behindBy") == 0:
        return "delete", "merged (all commits in default branch)"
    if prs and prs[0]["state"] in ("MERGED", "CLOSED") and prs[0]["headRefOid"] == target["oid"]:
        return "delete", f"PR #{prs[0]['number']} {prs[0]['state'].lower()}, tip unchanged since"
    return "keep", "unmerged commits without a closed PR"


def delete_if_unchanged(repo_id: str, branch: str, oid: str) -> None:
    """Delete refs/heads/<branch> only if it still points at `oid` (atomic CAS)."""
    graphql(DELETE_MUTATION, repo=repo_id, ref=f"refs/heads/{branch}", before=oid)


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
    meta = json.loads(gh(["api", f"repos/{repo}"]))
    default, repo_id = meta["default_branch"], meta["node_id"]

    keep = [re.compile(p) for p in ALWAYS_KEEP + args.keep]
    open_refs = open_pr_refs(paged(OPEN_PRS_QUERY, "pullRequests", owner=owner, name=name), repo)
    refs = paged(REFS_QUERY, "refs", owner=owner, name=name, base=default)
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.min_age_days)

    candidates, kept = [], {}
    for ref in refs:
        verdict, reason = classify(ref, default, keep, open_refs, cutoff, repo)
        if verdict == "delete":
            candidates.append((ref["target"]["committedDate"], ref["name"],
                               ref["target"]["oid"], reason))
        else:
            kept[reason] = kept.get(reason, 0) + 1
    candidates.sort()  # oldest tip first

    mode = "APPLY" if args.apply else "DRY RUN"
    print(f"[{mode}] {repo}: {len(refs)} branches scanned, {len(candidates)} deletable, "
          f"cap {args.max_deletions} per run.")
    for reason, count in sorted(kept.items(), key=lambda kv: -kv[1]):
        print(f"  kept {count:4d}: {reason}")

    batch = candidates[: max(args.max_deletions, 0)]
    if args.apply and batch:
        # Re-read just before writing: a PR opened since the scan protects its branches.
        open_refs = open_pr_refs(paged(OPEN_PRS_QUERY, "pullRequests", owner=owner, name=name), repo)

    deleted, failed, skipped = [], [], []
    for tip, branch, oid, reason in batch:
        if not args.apply:
            print(f"  would delete {branch} @ {oid[:8]}  ({reason}; tip {tip[:10]})")
            continue
        if branch in open_refs:
            skipped.append(branch)
            print(f"  skipped {branch}: an open PR now uses it")
            continue
        try:
            delete_if_unchanged(repo_id, branch, oid)
            deleted.append(branch)
            print(f"  deleted {branch} @ {oid[:8]}  ({reason}; tip {tip[:10]})")
        except RuntimeError as exc:  # moved since the scan, or already gone
            failed.append(branch)
            print(f"  WARNING: not deleted {branch}: {exc}")
    remaining = max(len(candidates) - args.max_deletions, 0)
    if remaining:
        print(f"{remaining} more deletable branch(es) left for later runs (cap reached).")
    print(f"Summary: candidates={len(candidates)} deleted={len(deleted)} failed={len(failed)} "
          f"skipped={len(skipped)} mode={mode}")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(f"### Branch cleanup ({mode})\n\n- scanned: {len(refs)}\n"
                     f"- deletable: {len(candidates)}\n- deleted this run: {len(deleted)}\n"
                     f"- failed: {len(failed)}\n- per-run cap: {args.max_deletions}\n")
    if args.json:
        print(json.dumps({"scanned": len(refs), "candidates": len(candidates),
                          "deleted": deleted, "failed": failed, "skipped": skipped,
                          "kept": kept}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

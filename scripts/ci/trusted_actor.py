#!/usr/bin/env python3
"""trusted_actor.py — list only PRs/issues opened by a trusted identity.

Why: the automation lanes decide "is there already an open bot PR / control
issue?" (and therefore whether to throttle, skip, merge or close) from gh
listings. Matching on title or branch name lets anyone open a look-alike PR or
issue — from a fork, or as a drive-by issue — that pauses a lane or gets picked
up by the auto-merger. Identity is the only signal an outsider cannot forge.

Trusted means:
  * the author is the repository owner (a plain user login, never a bot), or
    one of the known automation bots in TRUSTED_BOTS — recognised only in the
    forms GitHub itself sets for apps: "app/<slug>" (gh JSON), "<slug>[bot]"
    (REST/search) or "<slug>" with is_bot=true (GraphQL). A *user* account that
    merely calls itself "github-actions" is not trusted;
  * for PRs additionally: the head branch lives in this repository
    (isCrossRepository == false), i.e. the PR is not from a fork.

Untrusted volume can never trip or starve a decision: `list` asks GitHub for
each trusted author separately (`gh ... list --author <login>`), so outsiders'
items are never in the result window at all — they cannot push a genuine
control issue off the page, and there is no count of theirs to inflate. Every
record is then re-checked locally (identity + fork) as defence in depth.

Usage:
  # PRs/issues by trusted actors, as one JSON array on stdout:
  python3 scripts/ci/trusted_actor.py list prs --state open \
      --fields number,title --bot-heuristic [--exclude-rollup] [--head BRANCH]
  python3 scripts/ci/trusted_actor.py list issues --state open \
      --fields number,title [--label jules] [--search "Daily Maintenance Run"]

  # Filter an already-fetched listing (stdin JSON array -> stdout), e.g. a
  # single issue from an event payload; requires `author` (+ isCrossRepository
  # for PRs):
  gh issue view 12 --json number,author | jq -c '[.]' \
    | python3 scripts/ci/trusted_actor.py filter issues

  --fields         gh --json fields you need; author/isCrossRepository and the
                   heuristic's fields are added automatically.
  --bot-heuristic  keep only PRs that look like automation PRs (title / body
                   marker / `jules` label / branch name / Jules author). This
                   is THE single definition of "bot PR" for the lanes.
  --exclude-rollup drop the shared automation/weekly-rollup PR (it has its own
                   merge lane).

The repository ("owner/name") comes from --repo, else $REPO, else
$GITHUB_REPOSITORY. Dropped records are reported as GitHub ::notice:: lines.

Fail-safe: a genuine lookup error (gh exits non-zero, unparsable or malformed
output, no repository, or a trusted author's OWN listing filling the whole
page — something only trusted actors control) prints an ::error:: line and
exits 2 with no stdout. Callers run under `set -euo pipefail`, so the lane step
fails visibly: no duplicate is created, nothing is silently paused, and the
automation-health watchdog reports and retries the failed run.

Exit codes: 0 ok (possibly empty array), 2 lookup/input error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

# Known automation identities, as GitHub App slugs. Derived from the repo's
# history (`gh pr list --state all --json author` / `gh issue list ...`):
# github-actions opens the control issues and rollup PRs; Jules (Google Labs)
# comments on and may open PRs as its own app.
TRUSTED_BOTS = ("github-actions", "google-labs-jules")

ROLLUP_BRANCH = "automation/weekly-rollup"

# Per-author page size. Only a trusted author's own matching items count toward
# it, so hitting it is an anomaly worth failing on, not attacker-controllable.
PAGE_LIMIT = 1000

# "Looks like an automation PR" heuristic, formerly copy-pasted into five
# workflows (pr-hygiene, jules-auto-merge, process-jules-backlog,
# daily-jules-maintenance, daily-jules-knowledge). Only applied to trusted PRs.
BOT_TITLE_RE = re.compile(
    r"daily maintenance|daily knowledge|weekly|cross-link|primer|"
    r"automated resolution|freshness audit", re.IGNORECASE)
BOT_BODY_RE = re.compile(r"PR created automatically by Jules", re.IGNORECASE)
BOT_BRANCH_RE = re.compile(
    r"jules|daily-maintenance|daily-knowledge|jules-sprint|weekly-deepen|"
    r"cross-link|primer|auto-fix|ralph-loop|freshness-audit|audit-batch|batch-",
    re.IGNORECASE)
BOT_LABEL = "jules"


class InputError(Exception):
    """The lookup failed or returned something we cannot decide on."""


def bot_slug(author: dict) -> str | None:
    """Return the app slug if `author` is a GitHub App/bot identity, else None."""
    login = author.get("login") or ""
    if login.startswith("app/"):
        return login[len("app/"):]
    if login.endswith("[bot]"):
        return login[:-len("[bot]")]
    if author.get("is_bot") is True:
        return login
    return None


def is_trusted_author(author: object, owner: str) -> bool:
    """True when `author` (a gh author object) is the owner or a known bot."""
    if not isinstance(author, dict):
        return False  # null author = deleted account ("ghost"): not trusted
    slug = bot_slug(author)
    if slug is not None:
        return slug in TRUSTED_BOTS
    return (author.get("login") or "").lower() == owner.lower()


def trusted_search_logins(owner: str) -> list[str]:
    """Logins to pass to `gh ... list --author`. `<slug>[bot]` is the form gh
    accepts for apps on BOTH PRs and issues (`app/<slug>` silently matches
    nothing for issues)."""
    return [owner] + [f"{slug}[bot]" for slug in TRUSTED_BOTS]


def looks_like_bot_pr(pr: dict) -> bool:
    labels = pr.get("labels") or []
    author = pr.get("author") or {}
    return bool(
        BOT_TITLE_RE.search(pr.get("title") or "")
        or BOT_BODY_RE.search(pr.get("body") or "")
        or any(isinstance(l, dict) and l.get("name") == BOT_LABEL for l in labels)
        or BOT_BRANCH_RE.search(pr.get("headRefName") or "")
        or bot_slug(author) == "google-labs-jules")


def required_fields(kind: str, bot_heuristic: bool, exclude_rollup: bool) -> list[str]:
    fields = ["number", "author"]
    if kind == "prs":
        fields.append("isCrossRepository")
        if bot_heuristic or exclude_rollup:
            fields.append("headRefName")
        if bot_heuristic:
            fields += ["title", "body", "labels"]
    return fields


def filter_items(items: object, kind: str, owner: str, *, bot_heuristic=False,
                 exclude_rollup=False, notice=lambda msg: None) -> list[dict]:
    """Return the trusted subset of a gh listing. Raises InputError if malformed.

    Untrusted records are simply dropped: how many there are never matters."""
    if not isinstance(items, list):
        raise InputError("gh output is not a JSON array")
    fields = required_fields(kind, bot_heuristic, exclude_rollup)
    kept = []
    for item in items:
        if not isinstance(item, dict):
            raise InputError("gh output contains a non-object record")
        missing = [f for f in fields if f != "number" and f not in item]
        if missing:
            raise InputError(f"{kind} #{item.get('number', '?')} lacks field(s) "
                             f"{', '.join(missing)} — add them to the gh --json list")
        num = item.get("number", "?")
        author = item.get("author")
        login = author.get("login", "<none>") if isinstance(author, dict) else "<none>"
        if kind == "prs":
            if exclude_rollup and item.get("headRefName") == ROLLUP_BRANCH:
                continue
            if bot_heuristic and not looks_like_bot_pr(item):
                continue  # an ordinary PR: not relevant
            if item.get("isCrossRepository") is not False:
                notice(f"Ignoring PR #{num} by {login}: head branch is in a fork")
                continue
        if not is_trusted_author(author, owner):
            notice(f"Ignoring {kind[:-1]} #{num}: author {login} is not a trusted actor")
            continue
        kept.append(item)
    return kept


def list_trusted(kind: str, repo: str | None, *, state="open", fields=(),
                 search=None, label=None, head=None, bot_heuristic=False,
                 exclude_rollup=False, limit=PAGE_LIMIT, allow_truncated=False,
                 runner=None, notice=lambda msg: None) -> list[dict]:
    """List PRs/issues authored by trusted actors only (one gh call per author),
    newest first.

    Raises InputError on any genuine lookup failure. With allow_truncated=True a
    full page is accepted (callers that only need the most recent items)."""
    runner = runner or subprocess.run  # injectable for tests
    owner = repo_owner(repo)
    json_fields = list(dict.fromkeys(
        [*required_fields(kind, bot_heuristic, exclude_rollup), *fields]))
    merged: dict[int, dict] = {}
    for login in trusted_search_logins(owner):
        cmd = ["gh", "pr" if kind == "prs" else "issue", "list", "--repo", repo,
               "--state", state, "--author", login, "--limit", str(limit),
               "--json", ",".join(json_fields)]
        if search:
            cmd += ["--search", search]
        if label:
            cmd += ["--label", label]
        if head:
            cmd += ["--head", head]
        try:
            res = runner(cmd, capture_output=True, text=True, check=False)
        except OSError as exc:
            raise InputError(f"could not run gh: {exc}") from exc
        if res.returncode != 0:
            raise InputError(f"gh {kind} list --author {login} failed: "
                             f"{(res.stderr or '').strip()[:300]}")
        try:
            page = json.loads(res.stdout or "")
        except json.JSONDecodeError as exc:
            raise InputError(f"unparsable gh output for --author {login}: {exc}") from exc
        if not isinstance(page, list):
            raise InputError(f"gh output for --author {login} is not a JSON array")
        if len(page) >= limit and not allow_truncated:
            raise InputError(f"trusted author {login} alone has {len(page)}+ matching "
                             f"{kind}; the page (--limit {limit}) may be truncated")
        for item in page:
            if not (isinstance(item, dict) and isinstance(item.get("number"), int)):
                raise InputError("gh output contains a record without a number")
            merged.setdefault(item["number"], item)
    items = sorted(merged.values(), key=lambda i: i["number"], reverse=True)
    return filter_items(items, kind, owner, bot_heuristic=bot_heuristic,
                        exclude_rollup=exclude_rollup, notice=notice)


def repo_owner(repo: str | None) -> str:
    if not repo or "/" not in repo:
        raise InputError("repository unknown — pass --repo or set REPO/GITHUB_REPOSITORY")
    return repo.split("/", 1)[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    for mode in ("list", "filter"):
        p = sub.add_parser(mode)
        p.add_argument("kind", choices=["prs", "issues"])
        p.add_argument("--repo", default=os.environ.get("REPO")
                       or os.environ.get("GITHUB_REPOSITORY"))
        p.add_argument("--bot-heuristic", action="store_true")
        p.add_argument("--exclude-rollup", action="store_true")
        if mode == "list":
            p.add_argument("--state", default="open",
                           choices=["open", "closed", "merged", "all"])
            p.add_argument("--fields", default="", help="comma-separated gh --json fields")
            p.add_argument("--search")
            p.add_argument("--label")
            p.add_argument("--head")
    args = parser.parse_args(argv)

    def notice(msg: str) -> None:
        print(f"::notice::trusted_actor: {msg}", file=sys.stderr)

    try:
        if args.mode == "list":
            kept = list_trusted(
                args.kind, args.repo, state=args.state,
                fields=[f for f in args.fields.split(",") if f],
                search=args.search, label=args.label, head=args.head,
                bot_heuristic=args.bot_heuristic, exclude_rollup=args.exclude_rollup,
                notice=notice)
        else:
            owner = repo_owner(args.repo)
            raw = sys.stdin.read()
            if not raw.strip():
                raise InputError("empty input (the lookup probably failed)")
            try:
                items = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise InputError(f"unparsable input: {exc}") from exc
            kept = filter_items(items, args.kind, owner, bot_heuristic=args.bot_heuristic,
                                exclude_rollup=args.exclude_rollup, notice=notice)
    except InputError as exc:
        print(f"::error::trusted_actor: {exc}. Refusing to decide on an unverified "
              "listing (no issue created, lane not paused) — failing so the "
              "automation-health watchdog reports it.", file=sys.stderr)
        return 2
    json.dump(kept, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

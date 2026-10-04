#!/usr/bin/env python3
"""trusted_actor.py — keep only PRs/issues opened by a trusted identity.

Why: the automation lanes decide "is there already an open bot PR / control
issue?" (and therefore whether to throttle, skip, merge or close) from gh
listings. Matching on title or branch name alone lets anyone open a look-alike
PR or issue — from a fork, or as a drive-by issue — that pauses a lane (or,
worse, gets picked up by the auto-merger). Identity is the only signal an
outsider cannot forge, so every such decision first passes the listing
through this filter.

Trusted means:
  * the author is the repository owner (a plain user login, never a bot), or
    one of the known automation bots in TRUSTED_BOTS — recognised only in the
    forms GitHub itself sets for apps: "app/<slug>" (gh listings),
    "<slug>[bot]" (REST) or "<slug>" with is_bot=true (GraphQL). A *user*
    account that merely calls itself "github-actions" is not trusted;
  * for PRs additionally: the head branch lives in this repository
    (isCrossRepository == false), i.e. the PR is not from a fork.

Usage (stdin = the JSON array printed by `gh ... --json`, stdout = the
trusted subset, same objects, same order):

  gh pr list --repo "$REPO" --state open --limit 200 \
      --json number,title,body,labels,headRefName,author,isCrossRepository \
    | python3 scripts/ci/trusted_actor.py prs --limit 200 --bot-heuristic [--exclude-rollup]

  gh issue list --repo "$REPO" --state open --limit 200 --json number,title,author \
    | python3 scripts/ci/trusted_actor.py issues --limit 200

  prs              requires fields: author, isCrossRepository
  --bot-heuristic  also keep only PRs that look like automation PRs (title /
                   body marker / `jules` label / branch name / Jules author);
                   then also requires: title, body, labels, headRefName.
                   This is THE single definition of "bot PR" for the lanes.
  --exclude-rollup drop the shared automation/weekly-rollup PR (it has its own
                   merge lane).
  --limit N        the --limit given to gh. A listing of N or more records may
                   be truncated — e.g. by an outsider filing many look-alikes
                   to push the real control issue off the page, which would
                   cause a duplicate — so it is treated as an error. Always
                   pass the same N to gh and here.
  issues           requires field: author

The repository ("owner/name") comes from --repo, else $REPO, else
$GITHUB_REPOSITORY. Untrusted items are dropped and reported on stderr as
GitHub ::notice:: lines.

Fail-safe: on malformed input (gh failed and printed nothing / non-JSON /
missing fields / no repository) it prints an ::error:: line naming the reason
and exits 2 with no stdout. Callers run under `set -euo pipefail`, so the lane
step fails visibly — no duplicate issue is created, and nothing is silently
paused: the failed run is what the automation-health watchdog reports and
retries.

Exit codes: 0 ok (possibly empty array), 2 lookup/input error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Known automation identities, as GitHub App slugs. Derived from the repo's
# history (`gh pr list --state all --json author` / `gh issue list ...`):
# github-actions opens the control issues and rollup PRs; Jules (Google Labs)
# comments on and may open PRs as its own app.
TRUSTED_BOTS = frozenset({"github-actions", "google-labs-jules"})

ROLLUP_BRANCH = "automation/weekly-rollup"

# "Looks like an automation PR" heuristic, formerly copy-pasted into five
# workflows (pr-hygiene, jules-auto-merge, process-jules-backlog,
# daily-jules-maintenance, daily-jules-knowledge). Only applied AFTER the
# identity check, so it now only classifies trusted PRs.
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
    """The listing could not be trusted to be complete/correct."""


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


def require(item: dict, fields: tuple[str, ...], kind: str) -> None:
    missing = [f for f in fields if f not in item]
    if missing:
        raise InputError(
            f"{kind} #{item.get('number', '?')} lacks field(s) {', '.join(missing)}"
            " — add them to the gh --json list")


def looks_like_bot_pr(pr: dict) -> bool:
    labels = pr.get("labels") or []
    author = pr.get("author") or {}
    return bool(
        BOT_TITLE_RE.search(pr.get("title") or "")
        or BOT_BODY_RE.search(pr.get("body") or "")
        or any(isinstance(l, dict) and l.get("name") == BOT_LABEL for l in labels)
        or BOT_BRANCH_RE.search(pr.get("headRefName") or "")
        or bot_slug(author) == "google-labs-jules")


def filter_items(items: object, kind: str, owner: str, *, bot_heuristic=False,
                 exclude_rollup=False, limit: int | None = None,
                 notice=lambda msg: None) -> list[dict]:
    """Return the trusted subset of a gh listing. Raises InputError if malformed
    or (with `limit`) possibly truncated."""
    if not isinstance(items, list):
        raise InputError("gh output is not a JSON array")
    if limit is not None and len(items) >= limit:
        raise InputError(f"gh returned {len(items)} records with --limit {limit}; "
                         "the listing may be truncated")
    fields: tuple[str, ...] = ("author",)
    if kind == "prs":
        fields += ("isCrossRepository",)
        if bot_heuristic or exclude_rollup:
            fields += ("headRefName",)
        if bot_heuristic:
            fields += ("title", "body", "labels")
    kept = []
    for item in items:
        if not isinstance(item, dict):
            raise InputError("gh output contains a non-object record")
        require(item, fields, kind)
        num = item.get("number", "?")
        login = (item.get("author") or {}).get("login", "<none>") \
            if isinstance(item.get("author"), dict) else "<none>"
        if kind == "prs":
            if exclude_rollup and item.get("headRefName") == ROLLUP_BRANCH:
                continue
            if bot_heuristic and not looks_like_bot_pr(item):
                continue  # an ordinary PR: not relevant, not suspicious
            if item.get("isCrossRepository") is not False:
                notice(f"Ignoring PR #{num} by {login}: head branch is in a fork")
                continue
        if not is_trusted_author(item.get("author"), owner):
            notice(f"Ignoring {kind[:-1]} #{num}: author {login} is not a trusted actor")
            continue
        kept.append(item)
    return kept


def repo_owner(repo: str | None) -> str:
    if not repo or "/" not in repo:
        raise InputError("repository unknown — pass --repo or set REPO/GITHUB_REPOSITORY")
    return repo.split("/", 1)[0]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("kind", choices=["prs", "issues"])
    parser.add_argument("--repo", default=os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--bot-heuristic", action="store_true")
    parser.add_argument("--exclude-rollup", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args(argv)

    def notice(msg: str) -> None:
        print(f"::notice::trusted_actor: {msg}", file=sys.stderr)

    try:
        owner = repo_owner(args.repo)
        raw = sys.stdin.read()
        if not raw.strip():
            raise InputError("empty gh output (the listing call probably failed)")
        try:
            items = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise InputError(f"unparsable gh output: {exc}") from exc
        kept = filter_items(items, args.kind, owner, bot_heuristic=args.bot_heuristic,
                            exclude_rollup=args.exclude_rollup, limit=args.limit,
                            notice=notice)
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

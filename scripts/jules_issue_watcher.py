#!/usr/bin/env python3
"""
Jules Issue Watcher
Searches for issues mentioning "jules" and ensures they are labeled for processing.
If no specific instructions are found, it directs Jules to organize the information.

Only issues opened by a trusted actor (repo owner / known automation bots, see
scripts/ci/trusted_actor.py) are queued: an outsider's issue mentioning
"jules" must not become work for an agent with write access. The owner can
still queue any issue by adding the `jules` label by hand.

Usage: REPO=owner/name python3 scripts/jules_issue_watcher.py
       (REPO falls back to $GITHUB_REPOSITORY, set in Actions)
"""

import os
import subprocess
import json
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "ci"))
import trusted_actor  # noqa: E402


def run_gh_command(args):
    """Runs a gh command and returns the output."""
    try:
        result = subprocess.run(['gh'] + args, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command {' '.join(args)}: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: 'gh' CLI not found. This script requires the GitHub CLI.")
        return None

def has_explicit_instructions(title, body):
    """
    Checks if the issue contains explicit instructions for Jules.
    Uses a list of action verbs commonly used in Jules prompts.
    """
    action_verbs = [
        'refactor', 'add', 'fix', 'create', 'update', 'remove', 'delete',
        'implement', 'write', 'generate', 'upgrade', 'check', 'setup',
        'analyze', 'identify', 'find', 'convert', 'initialize', 'bootstrap',
        'diagnose', 'trace', 'why'
    ]

    content = (title + " " + body).lower()

    # Check for keywords
    for verb in action_verbs:
        if re.search(r'\b' + verb + r'\b', content):
            return True

    # Check for direct mentions with a command-like structure (e.g. "@jules do X")
    if re.search(r'@jules\s+\w+', content):
        return True

    return False

GUIDANCE_COMMENT = (
    "@jules This issue mentions you but doesn't seem to have a specific command. "
    "Per the repository's automated maintenance policy, please assume this issue "
    "is providing new information to be organized. Review the content and update "
    "the repository's documentation or data files (e.g., data/all_tools.json, docs/services/) "
    "accordingly."
)

JULES_MENTION = re.compile(r"\bjules\b", re.IGNORECASE)


def trusted_comment_text(number, owner):
    """Bodies of the issue's comments written by trusted actors only.

    Outsiders can comment on any issue: their text is never used to decide
    whether (or how) to queue work for Jules. Returns None if the lookup fails.
    """
    raw = run_gh_command(['issue', 'view', str(number), '--json', 'comments'])
    if raw is None:
        return None
    try:
        comments = json.loads(raw).get('comments', [])
    except (json.JSONDecodeError, AttributeError):
        return None
    kept = [c.get('body') or "" for c in comments
            if isinstance(c, dict) and trusted_actor.is_trusted_author(c.get('author'), owner)]
    skipped = len(comments) - len(kept)
    if skipped:
        print(f"Issue #{number}: ignoring {skipped} comment(s) from untrusted authors.")
    return " ".join(kept)


def process_issue(issue, owner):
    """Queue one trusted issue for Jules. Returns "labelled", "skipped" or "error".

    Issue text is only ever matched against regexes here and passed to gh as
    list arguments (no shell); titles are never echoed to the log, where a
    crafted "::command::" line could be read as a workflow command.
    """
    number = issue['number']
    if not trusted_actor.is_trusted_author(issue.get('author'), owner):
        return "skipped"  # defence in depth: list_trusted already filtered
    title = issue.get('title') or ""
    body = issue.get('body') or ""
    comments = trusted_comment_text(number, owner)
    if comments is None:
        print(f"::warning::Could not read comments of issue #{number}; skipping it this run.")
        return "error"
    trusted_text = f"{title} {body} {comments}"
    # The search also matches "jules" in ANY comment: require the mention to
    # come from trusted text, so an outsider cannot queue an owner's issue.
    if not JULES_MENTION.search(trusted_text):
        print(f"Issue #{number}: 'jules' only mentioned by untrusted authors; skipping.")
        return "skipped"

    print(f"Adding 'jules' label to issue #{number}...")
    if run_gh_command(['issue', 'edit', str(number), '--add-label', 'jules']) is None:
        return "error"
    if not has_explicit_instructions(title, f"{body} {comments}"):
        print(f"No explicit instructions detected for issue #{number}. Adding organizational guidance.")
        if run_gh_command(['issue', 'comment', str(number), '--body', GUIDANCE_COMMENT]) is None:
            return "error"
    else:
        print(f"Explicit instructions detected for issue #{number}. Jules will follow them.")
    return "labelled"


def main():
    # Search for issues mentioning "jules" that are open and don't have the "jules" label.
    # We use -label:jules to avoid re-processing issues we've already labeled.
    # The search API is used to find "jules" in title, body, or comments.
    search_query = "jules -label:jules is:open"
    repo = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY")

    print(f"Searching for issues with query: {search_query}")
    # Trusted authors only, queried server-side: outsiders' issues never
    # enter the window (see scripts/ci/trusted_actor.py).
    try:
        owner = trusted_actor.repo_owner(repo)
        issues = trusted_actor.list_trusted(
            "issues", repo, state="open", search=search_query, fields=["title", "body"],
            notice=lambda msg: print(f"::notice::{msg}"))
    except trusted_actor.InputError as exc:
        print(f"::error::trusted_actor: {exc}")
        sys.exit(1)

    if not issues:
        print("No new issues found mentioning 'jules'.")
        return

    results = [process_issue(issue, owner) for issue in issues]
    print(f"Watcher summary: {results.count('labelled')} labelled, "
          f"{results.count('skipped')} skipped, {results.count('error')} error(s).")
    if "error" in results:
        sys.exit(1)  # fail visibly so the watchdog notices

if __name__ == "__main__":
    main()

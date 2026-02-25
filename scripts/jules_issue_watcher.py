#!/usr/bin/env python3
"""
Jules Issue Watcher
Searches for issues mentioning "jules" and ensures they are labeled for processing.
If no specific instructions are found, it directs Jules to organize the information.
"""

import subprocess
import json
import sys
import re

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

def main():
    # Search for issues mentioning "jules" that are open and don't have the "jules" label.
    # We use -label:jules to avoid re-processing issues we've already labeled.
    # The search API is used to find "jules" in title, body, or comments.
    search_query = "jules -label:jules is:open"

    print(f"Searching for issues with query: {search_query}")
    issues_json = run_gh_command(['issue', 'list', '--search', search_query, '--json', 'number,title,body'])

    if issues_json is None:
        sys.exit(1)

    try:
        issues = json.loads(issues_json)
    except json.JSONDecodeError:
        print("Failed to decode JSON from gh output.")
        sys.exit(1)

    if not issues:
        print("No new issues found mentioning 'jules'.")
        return

    for issue in issues:
        number = issue['number']
        title = issue['title']
        body = issue['body'] or ""

        print(f"Processing issue #{number}: {title}")

        # Fetch comments to include in the heuristic
        comments_json = run_gh_command(['issue', 'view', str(number), '--json', 'comments'])
        full_content = body
        if comments_json:
            try:
                comments_data = json.loads(comments_json)
                for comment in comments_data.get('comments', []):
                    full_content += " " + (comment.get('body') or "")
            except json.JSONDecodeError:
                pass

        # 1. Add 'jules' label to trigger the agent
        print(f"Adding 'jules' label to issue #{number}...")
        run_gh_command(['issue', 'edit', str(number), '--add-label', 'jules'])

        # 2. If no explicit instructions, add a guiding comment
        if not has_explicit_instructions(title, full_content):
            print(f"No explicit instructions detected for issue #{number}. Adding organizational guidance.")
            comment = (
                "@jules This issue mentions you but doesn't seem to have a specific command. "
                "Per the repository's automated maintenance policy, please assume this issue "
                "is providing new information to be organized. Review the content and update "
                "the repository's documentation or data files (e.g., data/all_tools.json, docs/services/) "
                "accordingly."
            )
            run_gh_command(['issue', 'comment', str(number), '--body', comment])
        else:
            print(f"Explicit instructions detected for issue #{number}. Jules will follow them.")

if __name__ == "__main__":
    main()

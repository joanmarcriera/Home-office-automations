#!/usr/bin/env python3
"""PreToolUse guard: ask for confirmation before editing .github/workflows/.

Usage: registered in .claude/settings.json; reads the hook JSON on stdin.
The path is resolved (realpath) and compared component-wise, case-insensitively,
so `.github//workflows`, `./`, `../` and case tricks cannot bypass it.
Fails closed: unparseable input also asks.
"""
import json
import os
import sys


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


try:
    path = str(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))
except Exception:
    ask("Workflow guard could not parse hook input; confirm this edit")

parts = [x.lower() for x in os.path.realpath(os.path.join(os.getcwd(), path)).split(os.sep)]
if any(parts[i:i + 2] == [".github", "workflows"] for i in range(len(parts))):
    ask("Workflow file edits require explicit user confirmation: " + path)

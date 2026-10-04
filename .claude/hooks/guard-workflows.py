#!/usr/bin/env python3
"""PreToolUse guard: ask for confirmation before editing protected paths.

Usage: registered in .claude/settings.json as
  python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-workflows.py" || exit 2
(the `|| exit 2` makes a crash or a missing python3 BLOCK instead of passing).

Protected: .github/workflows/, .claude/hooks/, .claude/settings*.json.
Paths are resolved (realpath) and compared component-wise, case-insensitively, so
`.github//workflows`, `./`, `../` and case tricks cannot bypass it. Reads file_path,
notebook_path and path from tool_input. Fails closed: any error asks.
Limit: edits made through Bash (sed -i, tee, ...) are not visible to this hook.
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


def protected(parts):
    for i in range(len(parts) - 1):
        if parts[i:i + 2] in ([".github", "workflows"], [".claude", "hooks"]):
            return True
        if parts[i] == ".claude" and parts[i + 1].startswith("settings") and parts[i + 1].endswith(".json"):
            return True
    return False


try:
    tool_input = json.load(sys.stdin).get("tool_input", {})
    paths = [str(tool_input[k]) for k in ("file_path", "notebook_path", "path") if tool_input.get(k)]
    for path in paths:
        parts = [x.lower() for x in os.path.realpath(os.path.join(os.getcwd(), path)).split(os.sep)]
        if protected(parts):
            ask("Edit of a protected path requires explicit user confirmation: " + path)
except SystemExit:
    raise
except Exception as exc:  # fail closed
    ask("Guard error (%s); confirm this edit" % type(exc).__name__)

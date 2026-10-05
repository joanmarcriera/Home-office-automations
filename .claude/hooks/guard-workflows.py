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
import unicodedata


def ask(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


def canon(component):
    """Fold a path component the way a case/normalisation-insensitive filesystem would:
    drop invisible format chars (zero-width etc.), strip trailing dots/spaces, then
    casefold under every Unicode normalisation form. Returns the set of folded forms."""
    comp = "".join(ch for ch in component if unicodedata.category(ch) != "Cf").rstrip(". ")
    return {unicodedata.normalize(f, comp).casefold() for f in ("NFC", "NFD", "NFKC", "NFKD")}


def protected(parts):
    folded = [canon(x) for x in parts]
    for i in range(len(folded) - 1):
        if ".github" in folded[i] and "workflows" in folded[i + 1]:
            return True
        if ".claude" in folded[i] and "hooks" in folded[i + 1]:
            return True
        if ".claude" in folded[i] and any(f.startswith("settings") and f.endswith(".json") for f in folded[i + 1]):
            return True
    return False


def variants(path):
    """Every plausible resolution of `path`, so the guard and the editing tool cannot
    disagree: raw/expanded/NFC/NFD forms, resolved against both the hook's cwd and
    $CLAUDE_PROJECT_DIR, with and without symlink resolution."""
    bases = {os.getcwd(), os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()}
    for form in {path, path.strip(), os.path.expanduser(path)}:
        for norm in ("NFC", "NFD"):
            f = unicodedata.normalize(norm, form)
            for base in bases:
                joined = os.path.join(base, f)
                yield os.path.normpath(joined)
                yield os.path.realpath(joined)


try:
    tool_input = json.load(sys.stdin).get("tool_input", {})
    paths = [str(v) for k, v in tool_input.items()
             if k in ("file_path", "notebook_path", "path") or k.endswith("_path")]
    paths += [str(e.get("file_path", "")) for e in tool_input.get("edits", []) if isinstance(e, dict)]
    for path in filter(None, paths):
        if "\x00" in path:
            ask("Path contains a NUL byte; confirm this edit: " + repr(path))
        for v in variants(path):
            if protected(v.split(os.sep)):
                ask("Edit of a protected path requires explicit user confirmation: " + path)
except SystemExit:
    raise
except Exception as exc:  # fail closed
    ask("Guard error (%s); confirm this edit" % type(exc).__name__)

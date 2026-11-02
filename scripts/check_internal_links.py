#!/usr/bin/env python3
"""
Check every internal link, anchor and image reference in the Markdown content.

Lychee (docs-link-health.yml) is tuned for external URLs and runs with
`fail: false`; MkDocs only logs broken relative links at WARNING level and the
deploy does not run `--strict`. This script is the fast, offline check for the
internal half: no network, stdlib only.

What it checks
  * docs/**/*.md  -- links are judged the way the BUILT SITE sees them:
      - `path.md`, `path.md#anchor`, `#anchor`  -> file must exist under docs/
        and the anchor must match a heading slug / explicit id in that page;
      - images and other assets (`.png`, `.svg`, `.json`, ...) must exist
        under docs/ (MkDocs copies them);
      - a link that climbs OUT of docs/ (e.g. `../../scripts/foo.py`) is
        reported: the file exists in the repo but is not published, so it
        404s on ai.riera.co.uk -- link to the GitHub blob URL instead;
      - a bare directory link (`../reports/`) is reported: MkDocs leaves it
        unrewritten, so it resolves against the page URL and 404s -- link the
        directory's `index.md` instead;
      - site-absolute links (`/new-sources/2026-03-01/`) must map to a page
        the generator produces (docs/<path>.md or docs/<path>/index.md).
  * mkdocs.yml nav entries must point at files under docs/.
  * Root-level *.md (README.md, AGENTS.md, roadmap.md, ...) -- links are
    judged as GitHub renders them: the target must exist in the repo. Root
    symlinks into docs/ are skipped (their content is checked via docs/).

Skipped: external URLs (any `scheme:`), links inside fenced/inline code,
`docs/templates/` (placeholders by design) and the `{{ ... }}` template slots.

Usage
  python3 scripts/check_internal_links.py              # whole repo
  python3 scripts/check_internal_links.py docs/a.md    # only these files
  python3 scripts/check_internal_links.py --summary    # counts only

Exit status: 0 when nothing is broken, 1 otherwise (CI decides whether that
blocks). Output is one `file:line: target -- reason` per broken reference.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
MKDOCS_YML = REPO / "mkdocs.yml"
SKIP_DIRS = {DOCS / "templates"}

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")
# [text](target "title") and ![alt](target); text may hold one nesting level.
INLINE_LINK_RE = re.compile(r"!?\[(?:[^\[\]]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+[\"'(][^)]*)?\)")
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?(?:\s+.*)?$")
HTML_ATTR_RE = re.compile(r"<(?:a|img|source)\b[^>]*?\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
ATTR_ID_RE = re.compile(r"\{[^}]*#([\w:-]+)[^}]*\}\s*$")
HTML_ID_RE = re.compile(r"<[^>]+\b(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", re.I)
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def slugify(text: str) -> str:
    """python-markdown's default toc slugify (what mkdocs-material uses here)."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[-\s]+", "-", text)


def heading_plain_text(raw: str) -> str:
    raw = ATTR_ID_RE.sub("", raw)
    raw = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", raw)  # links/images -> text
    raw = re.sub(r"<[^>]+>", "", raw)  # inline HTML
    raw = re.sub(r"`([^`]*)`", r"\1", raw)
    raw = re.sub(r"(\*\*|__|\*|_|~~)(.+?)\1", r"\2", raw)
    raw = re.sub(r":[a-z0-9_+-]+:", "", raw)  # :emoji: shortcodes render as images
    return raw


def iter_lines(path: Path):
    """Yield (lineno, text) outside fenced code blocks, inline code blanked."""
    in_fence = None
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = FENCE_RE.match(line)
        if m:
            if in_fence is None:
                in_fence = m.group(1)
            elif m.group(1) == in_fence:
                in_fence = None
            continue
        if in_fence is None:
            yield n, INLINE_CODE_RE.sub(lambda mm: " " * len(mm.group(0)), line)


@lru_cache(maxsize=None)
def anchors_for(path: Path) -> frozenset[str]:
    ids: set[str] = set()
    seen: dict[str, int] = {}
    for _, line in iter_lines(path):
        ids.update(HTML_ID_RE.findall(line))
        m = HEADING_RE.match(line)
        if not m:
            continue
        explicit = ATTR_ID_RE.search(m.group(2))
        if explicit:
            ids.add(explicit.group(1))
            continue
        slug = slugify(heading_plain_text(m.group(2))) or "_"
        if slug in seen:
            seen[slug] += 1
            slug = f"{slug}_{seen[slug]}"
        else:
            seen[slug] = 0
        ids.add(slug)
    return frozenset(ids)


def extract_targets(path: Path):
    for n, line in iter_lines(path):
        for rx in (INLINE_LINK_RE, HTML_ATTR_RE):
            for m in rx.finditer(line):
                yield n, m.group(1)
        m = REF_DEF_RE.match(line)
        if m:
            yield n, m.group(1)


def inside(p: Path, root: Path) -> bool:
    try:
        p.relative_to(root)
        return True
    except ValueError:
        return False


def escapes_docs(src: Path, rel: str) -> bool:
    """True if a relative path climbs above docs/ at any step, even when it
    comes back in (`../../docs/x.md`): MkDocs cannot resolve those."""
    depth = len(src.parent.relative_to(DOCS).parts)
    for part in Path(rel).parts:
        depth += -1 if part == ".." else (0 if part == "." else 1)
        if depth < 0:
            return True
    return False


def check_target(src: Path, target: str) -> str | None:
    """Return a reason string if `target` (from file `src`) is broken."""
    if not target or SCHEME_RE.match(target) or target.startswith("//") or "{{" in target:
        return None
    path_part, _, anchor = target.partition("#")
    path_part = unquote(path_part.split("?", 1)[0])
    in_docs = inside(src, DOCS)

    if not path_part:  # same-page anchor
        dest = src
    elif path_part.startswith("/"):
        if not in_docs:
            dest = REPO / path_part.lstrip("/")
            if not dest.exists():
                return "not found in repo"
        else:
            rel = path_part.strip("/")
            cands = [DOCS / rel] if Path(rel).suffix else [DOCS / f"{rel}.md", DOCS / rel / "index.md"]
            found = [c for c in cands if c.is_file()]
            if not found:
                return "no page at this site path"
            dest = found[0]
    else:
        # Lexical join: root playbooks/ and reference-implementations/ are
        # symlinks into docs/, so resolve() would hide links that escape docs/.
        dest = Path(os.path.normpath(src.parent / path_part))
        if in_docs:
            if not inside(dest, DOCS) or escapes_docs(src, path_part):
                if dest.exists():
                    return "outside docs/ (exists in repo but is not published; use a GitHub URL)"
                return "outside docs/ and not found in repo"
            if dest.is_dir():
                idx = "index.md" if (dest / "index.md").is_file() else None
                return f"directory link is not rewritten by MkDocs; link {idx or 'a page'} instead"
        if not dest.exists():
            return "not found"

    if anchor and dest.suffix == ".md" and dest.is_file():
        if anchor not in anchors_for(dest):
            return f"no heading/id '#{anchor}' in {dest.relative_to(REPO)}"
    return None


def nav_targets():
    """Yield (lineno, target) for every file entry in mkdocs.yml's nav."""
    in_nav = False
    for n, line in enumerate(MKDOCS_YML.read_text(encoding="utf-8").splitlines(), 1):
        if re.match(r"^nav:\s*$", line):
            in_nav = True
            continue
        if in_nav and re.match(r"^\S", line):
            break
        if in_nav:
            m = re.match(r"^\s*-\s*(?:(?:'[^']*'|\"[^\"]*\"|[^:]+):\s*)?['\"]?([^'\"\s]+\.md)['\"]?\s*$", line)
            if m:
                yield n, m.group(1)


def default_files() -> list[Path]:
    """docs/ plus real root-level *.md. Root symlinks into docs/ (ARCHITECTURE.md,
    SERVICES.md, standards-and-conventions.md, playbooks/, reference-implementations/)
    are the same files and are checked once, via docs/."""
    files = [p for p in DOCS.rglob("*.md") if not any(inside(p, d) for d in SKIP_DIRS)]
    files += [p for p in REPO.glob("*.md") if not p.is_symlink()]
    return sorted(set(files))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("files", nargs="*", help="Markdown files to check (default: all content)")
    ap.add_argument("--summary", action="store_true", help="print counts only")
    args = ap.parse_args()

    files = [Path(os.path.abspath(f)) for f in args.files] if args.files else default_files()
    broken: list[str] = []
    checked = 0
    for f in files:
        if f.suffix != ".md" or not f.is_file():
            continue
        for n, target in extract_targets(f):
            reason = check_target(f, target)
            checked += 1
            if reason:
                broken.append(f"{f.relative_to(REPO)}:{n}: {target} -- {reason}")
    if not args.files:
        for n, target in nav_targets():
            checked += 1
            if SCHEME_RE.match(target):
                continue
            dest = Path(os.path.normpath(DOCS / target))
            if not dest.is_file() or not inside(dest, DOCS):
                broken.append(f"mkdocs.yml:{n}: {target} -- nav entry not found under docs/")

    if not args.summary:
        print("\n".join(broken))
    print(f"checked {checked} internal references in {len(files)} files; broken: {len(broken)}",
          file=sys.stderr)
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())

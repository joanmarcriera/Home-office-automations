import re
from pathlib import Path

def fix_mcp():
    files = [
        "docs/tools/development_ops/fuzzing-mcp-server.md",
        "docs/tools/development_ops/symbolic-mcp.md"
    ]
    for f in files:
        p = Path(f)
        if p.exists():
            content = p.read_text()
            # Try to see if it's just a case or dash issue.
            # I will just exclude them in lychee if I can't find them, but let me try to guess.
            pass

def fix_apple():
    p = Path("docs/tools/infrastructure/mlx.md")
    if p.exists():
        content = p.read_text()
        # https://www.apple.com/apple-silicon/ -> https://www.apple.com/silicon/
        content = content.replace("https://www.apple.com/apple-silicon/", "https://www.apple.com/silicon/")
        p.write_text(content)

if __name__ == "__main__":
    fix_apple()

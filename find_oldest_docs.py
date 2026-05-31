import pathlib
import re
from datetime import datetime

def extract_last_reviewed(path):
    try:
        content = path.read_text(encoding="utf-8")
        match = re.search(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", content)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def main():
    docs = list(pathlib.Path("docs").rglob("*.md"))
    results = []
    for doc in docs:
        if "reports" in str(doc) or "templates" in str(doc) or "index.md" in str(doc) or "README.md" in str(doc):
            continue
        date_str = extract_last_reviewed(doc)
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                results.append((doc, date_obj))
            except ValueError:
                pass

    results.sort(key=lambda x: x[1])
    for doc, date in results[:10]:
        print(f"{date.strftime('%Y-%m-%d')} - {doc}")

if __name__ == "__main__":
    main()

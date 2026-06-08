import os
import re
import pathlib
from datetime import datetime

def find_open_tasks():
    report_dir = 'docs/reports/'
    tasks = []
    if not os.path.exists(report_dir):
        return []
    for filename in os.listdir(report_dir):
        if filename.startswith('task-decomposition-batch-'):
            filepath = os.path.join(report_dir, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip().startswith('- [ ]'):
                        batch_match = re.search(r'batch-(\d+)', filename)
                        batch_num = int(batch_match.group(1)) if batch_match else 0
                        tasks.append({'source': filename, 'task': line.strip(), 'priority': batch_num})
    return tasks

def find_new_sources():
    intake_dir = 'docs/new-sources/'
    items = []
    if not os.path.exists(intake_dir):
        return []
    for filename in os.listdir(intake_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(intake_dir, filename)
            with open(filepath, 'r') as f:
                for line in f:
                    if '|' in line and '| new |' in line.lower():
                        items.append({'source': filename, 'task': line.strip(), 'priority': 500})
    return items

def find_stale_docs():
    docs = list(pathlib.Path("docs").rglob("*.md"))
    stale = []
    for doc in docs:
        if "reports" in str(doc) or "templates" in str(doc) or "index.md" in str(doc) or "README.md" in str(doc) or "new-sources" in str(doc):
            continue
        try:
            content = doc.read_text(encoding="utf-8")
            match = re.search(r"Last reviewed:\s*(\d{4}-\d{2}-\d{2})", content)
            if match:
                date_str = match.group(1)
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                stale.append({'source': str(doc), 'task': f"Freshness audit for {doc}", 'date': date_obj, 'priority': 1000})
            else:
                # No metadata, treat as very old
                stale.append({'source': str(doc), 'task': f"Add metadata and audit {doc}", 'date': datetime(1970, 1, 1), 'priority': 1000})
        except:
            pass
    stale.sort(key=lambda x: x['date'])
    return stale

def main():
    open_tasks = find_open_tasks()
    new_sources = find_new_sources()
    stale_docs = find_stale_docs()

    # We combine them. Open tasks in decomposition files are usually the "oldest" because they were planned but not done.
    # Stale docs are the next category of "issues" (technical debt).

    all_issues = open_tasks + new_sources

    # If no explicitly open tasks, use stale docs
    if not all_issues:
        all_issues = stale_docs
    else:
        # If we have some open tasks, but fewer than 5, fill with stale docs
        if len(all_issues) < 5:
            all_issues += stale_docs[:5-len(all_issues)]

    # Sorting: decomposition batches first (by batch num), then sources, then stale docs (already sorted by date)
    # But wait, the user said "5 oldest issues".
    # I will treat "open tasks in decomposition files" as the oldest issues because they represent deferred work.

    all_issues.sort(key=lambda x: x.get('priority', 9999))

    for i, issue in enumerate(all_issues[:10]):
        print(f"{i+1}. [{issue['source']}] {issue['task']}")

if __name__ == "__main__":
    main()

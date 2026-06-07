import os
import sys
import re

def find_oldest_issues(directory, limit=5):
    files = sorted([f for f in os.listdir(directory) if f.endswith('.md')])
    open_issues = []

    # Prioritize 2026-06-01.md as it seems to be the current active log based on memory
    active_file = "2026-06-01.md"
    if active_file in files:
        # Move it to the front to process it first if it has open items
        files.remove(active_file)
        files.insert(0, active_file)

    for filename in files:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if '|' in line and ('| new |' in line or '| open |' in line):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 5:
                        open_issues.append({
                            'file': filename,
                            'title': parts[1],
                            'url': parts[2],
                            'status': parts[4],
                            'line_index': i
                        })
                if len(open_issues) >= limit:
                    return open_issues
    return open_issues

if __name__ == "__main__":
    issues = find_oldest_issues('docs/new-sources/')
    for issue in issues:
        print(f"{issue['file']}: {issue['title']} ({issue['status']})")

import os
import re

new_sources_dir = 'docs/new-sources/'
new_items = []

for filename in os.listdir(new_sources_dir):
    if filename.endswith('.md'):
        filepath = os.path.join(new_sources_dir, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '|' in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 5:
                        # Status is parts[4] because split('|') on "| A | B |" gives ['', ' A ', ' B ', '']
                        status = parts[4].lower()
                        if status == 'new':
                            new_items.append((filename, line.strip()))

if new_items:
    print(f"Found {len(new_items)} new items:")
    for file, item in new_items:
        print(f"{file}: {item}")
else:
    print("No items with 'Status: new' found.")

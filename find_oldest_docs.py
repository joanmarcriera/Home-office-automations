import os
import re
from datetime import datetime

def get_last_reviewed(filepath):
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            match = re.search(r'Last reviewed: (\d{4}-\d{2}-\d{2})', content)
            if match:
                return match.group(1)
    except Exception:
        pass
    return None

docs = []
for root, dirs, files in os.walk('docs'):
    for file in files:
        if file.endswith('.md'):
            path = os.path.join(root, file)
            lr = get_last_reviewed(path)
            if lr:
                docs.append((path, lr))

docs.sort(key=lambda x: x[1])
for path, lr in docs[:20]:
    print(f"{lr}: {path}")

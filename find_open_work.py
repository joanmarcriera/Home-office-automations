import os
import re

def main():
    triage_path = 'docs/reports/ralph-loop-triage.md'
    if not os.path.exists(triage_path):
        print(f"Triage report not found at {triage_path}")
        return

    with open(triage_path, 'r') as f:
        triage_content = f.read()

    # Find all batches
    batches = []
    for filename in os.listdir('docs/reports/'):
        if filename.startswith('task-decomposition-batch-'):
            # Handle cases like 39-40
            batch_id = filename.replace('task-decomposition-batch-', '').replace('.md', '')
            batches.append(batch_id)

    print(f"Found {len(batches)} batches in reports.")

    open_batches = []
    for b in batches:
        # Search for Batch X in the triage report and check its status
        # Match "Batch 35" specifically
        pattern = rf"Batch {b}\b.*?\| (.*?) \|"
        match = re.search(pattern, triage_content, re.IGNORECASE)
        if match:
            status = match.group(1).strip()
            if "Resolved" not in status and "Closed" not in status:
                open_batches.append((b, status))
        else:
            # Maybe it's mentioned as Issue #X
            open_batches.append((b, "Not found in triage"))

    print(f"Open or untracked batches: {len(open_batches)}")
    for b, status in sorted(open_batches):
        print(f"Batch {b}: {status}")

if __name__ == "__main__":
    main()

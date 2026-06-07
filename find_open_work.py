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
        # The table format is | Issue # | Title | Status | Notes |
        # Status is in the third column (index 2 if we skip the first empty split)
        # Match "**Batch 35**" or "Batch 35" in the first column
        pattern = rf"Batch {b}\b.*?\|.*?\| (.*?) \|"
        match = re.search(pattern, triage_content, re.IGNORECASE)
        if match:
            status = match.group(1).strip()
            if "Resolved" not in status and "Verified & Closed" not in status:
                open_batches.append((b, status))
        else:
            # Check if it's in a list or elsewhere
            open_batches.append((b, "Not found in triage table"))

    print(f"Open or untracked batches: {len(open_batches)}")
    for b, status in sorted(open_batches):
        print(f"Batch {b}: {status}")

if __name__ == "__main__":
    main()

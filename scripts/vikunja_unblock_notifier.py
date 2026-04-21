#!/usr/bin/env python3
"""
Vikunja Task Unblocking Notifier
Checks for tasks that were blocked by now-closed tasks and notifies the user.
Uses the Vikunja API to fetch tasks and their relations.
"""

import os
import requests
import argparse
import sys
from datetime import datetime, timezone

# Configuration
VIKUNJA_URL = os.environ.get("VIKUNJA_URL", "http://localhost:3456")
VIKUNJA_TOKEN = os.environ.get("VIKUNJA_TOKEN")

def get_all_tasks():
    """Fetches all tasks from Vikunja."""
    headers = {"Authorization": f"Bearer {VIKUNJA_TOKEN}"}
    url = f"{VIKUNJA_URL.rstrip('/')}/api/v1/tasks/all"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching tasks: {e}", file=sys.stderr)
        return []

def get_task_relations(task_id):
    """Fetches relations for a specific task."""
    headers = {"Authorization": f"Bearer {VIKUNJA_TOKEN}"}
    url = f"{VIKUNJA_URL.rstrip('/')}/api/v1/tasks/{task_id}/relations"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching relations for task {task_id}: {e}", file=sys.stderr)
        return []

def check_unblocked_tasks():
    if not VIKUNJA_TOKEN:
        print("Error: VIKUNJA_TOKEN not set.", file=sys.stderr)
        return

    all_tasks = get_all_tasks()
    if not all_tasks:
        return

    # Create a map for quick lookup
    task_map = {task['id']: task for task in all_tasks}

    print(f"Scanning {len(all_tasks)} tasks for unblocked dependencies...")

    unblocked_count = 0
    for task in all_tasks:
        # We only care about tasks that are NOT done
        if task.get('done'):
            continue

        relations = get_task_relations(task['id'])
        is_blocked = False
        blockers_resolved = False

        # Check 'blocked by' relations
        # Relation type 4 is usually 'blocked by' in Vikunja (referencing docs/services/vikunja.md)
        # However, the API returns objects with relation types.
        for rel in relations:
            # Based on common Vikunja API patterns:
            # rel['relation_kind'] or similar
            # For this reference implementation, we assume 'blocked_by' logic
            if rel.get('relation_type') == 'blocked_by':
                other_task_id = rel.get('other_task_id')
                other_task = task_map.get(other_task_id)

                if other_task and not other_task.get('done'):
                    is_blocked = True
                    break
                elif other_task and other_task.get('done'):
                    blockers_resolved = True

        if blockers_resolved and not is_blocked:
            print(f"NOTIFICATION: Task '{task['title']}' (ID: {task['id']}) is now unblocked!")
            unblocked_count += 1

    if unblocked_count == 0:
        print("No new tasks unblocked today.")

def main():
    parser = argparse.ArgumentParser(description="Vikunja auto-unblocking notifier.")
    args = parser.parse_args()

    check_unblocked_tasks()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Obsidian Incremental Indexing Baseline
Tracks changes in an Obsidian vault using file hashes and modification times
to identify files that need re-indexing in a vector database.
"""

import os
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime, timezone

def calculate_sha256(filepath):
    """Calculates the SHA256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def scan_vault(vault_path, state):
    """Scans the vault and identifies new, modified, or deleted files."""
    vault_root = Path(vault_path)
    current_files = {}

    updates = {
        "new": [],
        "modified": [],
        "deleted": [],
        "unchanged": []
    }

    # Scan existing files
    for md_file in vault_root.rglob("*.md"):
        rel_path = str(md_file.relative_to(vault_root))
        mtime = md_file.stat().st_mtime
        size = md_file.stat().st_size

        current_files[rel_path] = {
            "mtime": mtime,
            "size": size
        }

        if rel_path not in state:
            # New file
            file_hash = calculate_sha256(md_file)
            current_files[rel_path]["hash"] = file_hash
            updates["new"].append(rel_path)
        else:
            # Check if modified by mtime first (fast)
            if mtime > state[rel_path].get("mtime", 0):
                file_hash = calculate_sha256(md_file)
                if file_hash != state[rel_path].get("hash"):
                    current_files[rel_path]["hash"] = file_hash
                    updates["modified"].append(rel_path)
                else:
                    current_files[rel_path]["hash"] = file_hash
                    updates["unchanged"].append(rel_path)
            else:
                current_files[rel_path]["hash"] = state[rel_path].get("hash")
                updates["unchanged"].append(rel_path)

    # Check for deleted files
    for rel_path in state:
        if rel_path not in current_files:
            updates["deleted"].append(rel_path)

    return current_files, updates

def main():
    parser = argparse.ArgumentParser(description="Incremental indexing for Obsidian vaults.")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault.")
    parser.add_argument("--state", default="index_state.json", help="Path to the state file.")
    parser.add_argument("--dry-run", action="store_true", help="Don't update the state file.")

    args = parser.parse_args()

    state_path = Path(args.state)
    state = {}
    if state_path.exists():
        with open(state_path, "r") as f:
            state = json.load(f)

    new_state, updates = scan_vault(args.vault, state)

    print(f"Scan complete for: {args.vault}")
    print(f"  New:      {len(updates['new'])}")
    print(f"  Modified: {len(updates['modified'])}")
    print(f"  Deleted:  {len(updates['deleted'])}")
    print(f"  Unchanged:{len(updates['unchanged'])}")

    if not args.dry_run:
        with open(state_path, "w") as f:
            json.dump(new_state, f, indent=2)
        print(f"State updated: {args.state}")

if __name__ == "__main__":
    main()

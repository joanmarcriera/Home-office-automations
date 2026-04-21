#!/usr/bin/env python3
"""
Setup Video Metadata Collection in ChromaDB.
Initializes the collection with the appropriate metadata schema for video search.
"""

import os
import sys
import argparse
from datetime import datetime, timezone

try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

def setup_collection(db_dir, collection_name):
    if not CHROMA_AVAILABLE:
        print("Error: chromadb package not installed.", file=sys.stderr)
        return False

    client = chromadb.PersistentClient(path=db_dir)

    # Check if collection exists
    try:
        collection = client.get_collection(name=collection_name)
        print(f"Collection '{collection_name}' already exists.")
    except Exception:
        # Create collection
        collection = client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine", "description": "Home video metadata for semantic search"}
        )
        print(f"Created collection '{collection_name}' in {db_dir}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Setup ChromaDB collection for video metadata.")
    parser.add_argument("--chroma-dir", default="./chroma_db", help="Directory for ChromaDB storage.")
    parser.add_argument("--collection", default="video_metadata", help="Collection name.")

    args = parser.parse_args()

    success = setup_collection(args.chroma_dir, args.collection)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()

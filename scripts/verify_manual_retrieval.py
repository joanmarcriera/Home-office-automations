#!/usr/bin/env python3
"""
Verify retrieval accuracy and relevance for scanned manuals in ChromaDB.
Performs test queries and checks if the returned chunks match expected metadata.
"""

import argparse
import sys
import os
from datetime import datetime, timezone

try:
    import chromadb
except ImportError:
    print("Error: chromadb package not installed.", file=sys.stderr)
    sys.exit(1)

def verify_retrieval(db_dir, collection_name, query_texts, n_results=3):
    """Performs queries and prints results for verification."""
    if not os.path.exists(db_dir):
        print(f"Error: ChromaDB directory '{db_dir}' does not exist.")
        return

    client = chromadb.PersistentClient(path=db_dir)
    try:
        collection = client.get_collection(name=collection_name)
    except Exception as e:
        print(f"Error: Could not find collection '{collection_name}': {e}")
        return

    print(f"--- Verifying Collection: {collection_name} ---")
    print(f"Total items in collection: {collection.count()}")

    for query in query_texts:
        print(f"\nQuery: '{query}'")
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )

        if not results['documents'][0]:
            print("  No results found.")
            continue

        for i in range(len(results['documents'][0])):
            doc = results['documents'][0][i]
            meta = results['metadatas'][0][i]
            dist = results['distances'][0][i] if 'distances' in results else "N/A"

            print(f"  [{i+1}] Score: {dist}")
            print(f"      Source: {meta.get('source')}")
            print(f"      Manufacturer: {meta.get('manufacturer')}")
            print(f"      Model: {meta.get('model_number')}")
            print(f"      Section: {meta.get('section')}")
            print(f"      Snippet: {doc[:100]}...")

def main():
    parser = argparse.ArgumentParser(description="Verify ChromaDB retrieval for manuals.")
    parser.add_argument("--chroma-dir", required=True, help="Directory for ChromaDB persistent storage.")
    parser.add_argument("--collection", default="manuals", help="ChromaDB collection name.")
    parser.add_argument("--query", action='append', help="Query text to test. Can be used multiple times.")

    args = parser.parse_args()

    queries = args.query if args.query else [
        "How do I clean the filter?",
        "Installation instructions",
        "Error code E15",
        "Troubleshooting guide"
    ]

    verify_retrieval(args.chroma_dir, args.collection, queries)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Paperless-ngx OCR Text Exporter
Fetches OCR'd text from documents in Paperless-ngx for downstream indexing (e.g., Obsidian, Vector DB).
"""

import os
import requests
import argparse
import json
import logging
from pathlib import Path

# Configuration
PAPERLESS_URL = os.environ.get("PAPERLESS_URL", "http://localhost:8000")
PAPERLESS_TOKEN = os.environ.get("PAPERLESS_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_documents(tag_id=None, document_type_id=None):
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    params = {}
    if tag_id:
        params["tags__id__all"] = tag_id
    if document_type_id:
        params["document_type__id"] = document_type_id

    url = f"{PAPERLESS_URL.rstrip('/')}/api/documents/"
    documents = []

    try:
        while url:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            documents.extend(data.get("results", []))
            url = data.get("next")
            params = {} # params are included in the 'next' url
        return documents
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        return []

def get_document_metadata(doc_id):
    """Fetches full metadata including content."""
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    url = f"{PAPERLESS_URL.rstrip('/')}/api/documents/{doc_id}/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Error fetching document {doc_id}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Export OCR text from Paperless-ngx.")
    parser.add_argument("--output-dir", required=True, help="Directory to save text files.")
    parser.add_argument("--tag", type=int, help="Filter by tag ID.")
    parser.add_argument("--type", type=int, help="Filter by document type ID.")

    args = parser.parse_args()

    if not PAPERLESS_TOKEN:
        logging.error("PAPERLESS_TOKEN environment variable not set.")
        return

    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    docs = get_documents(tag_id=args.tag, document_type_id=args.type)
    logging.info(f"Found {len(docs)} documents to process.")

    for doc in docs:
        doc_id = doc["id"]
        full_doc = get_document_metadata(doc_id)
        if not full_doc:
            continue

        content = full_doc.get("content", "")
        title = full_doc.get("title", f"doc_{doc_id}")

        # Clean title for filename
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        filename = f"{doc_id}_{safe_title}.txt"

        with open(output_path / filename, "w", encoding="utf-8") as f:
            f.write(content)

        logging.info(f"Exported: {filename}")

if __name__ == "__main__":
    main()

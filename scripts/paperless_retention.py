#!/usr/bin/env python3
"""
Paperless-ngx Automated Retention Script
Automatically deletes documents with the 'Ephemeral' tag after 30 days.
"""

import os
import requests
import datetime
import logging

# Configuration
PAPERLESS_URL = os.environ.get("PAPERLESS_URL", "http://localhost:8000")
PAPERLESS_TOKEN = os.environ.get("PAPERLESS_TOKEN")
RETENTION_DAYS = 30
TAG_NAME = "Ephemeral"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_tag_id(tag_name):
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    url = f"{PAPERLESS_URL.rstrip('/')}/api/tags/"
    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            tags = data.get("results", [])
            for tag in tags:
                if tag["name"] == tag_name:
                    return tag["id"]
            url = data.get("next")
        logging.error(f"Tag '{tag_name}' not found.")
        return None
    except Exception as e:
        logging.error(f"Error fetching tags: {e}")
        return None

def get_expired_documents(tag_id, days):
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"{PAPERLESS_URL.rstrip('/')}/api/documents/?tags__id__all={tag_id}&created__lt={cutoff_date}"

    expired_docs = []
    try:
        while url:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            expired_docs.extend(data.get("results", []))
            url = data.get("next")
        return expired_docs
    except Exception as e:
        logging.error(f"Error fetching documents: {e}")
        return []

def delete_document(doc_id):
    headers = {"Authorization": f"Token {PAPERLESS_TOKEN}"}
    url = f"{PAPERLESS_URL.rstrip('/')}/api/documents/{doc_id}/"
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        logging.info(f"Deleted document ID {doc_id}")
        return True
    except Exception as e:
        logging.error(f"Failed to delete document ID {doc_id}: {e}")
        return False

def main():
    if not PAPERLESS_TOKEN:
        logging.error("PAPERLESS_TOKEN environment variable not set.")
        return

    tag_id = get_tag_id(TAG_NAME)
    if not tag_id:
        return

    expired_docs = get_expired_documents(tag_id, RETENTION_DAYS)
    logging.info(f"Found {len(expired_docs)} expired documents with tag '{TAG_NAME}'.")

    for doc in expired_docs:
        delete_document(doc["id"])

if __name__ == "__main__":
    main()

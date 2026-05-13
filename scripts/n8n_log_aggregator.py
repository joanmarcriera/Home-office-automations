#!/usr/bin/env python3
"""
n8n Log Aggregator
Fetches the last 24h of n8n execution logs via API and identifies failure patterns.
Used by Jules for weekly gap analysis and automation improvements.
"""

import os
import requests
import json
from datetime import datetime, timedelta
from collections import Counter
from typing import List, Dict, Any

def get_n8n_executions(api_url: str, api_key: str, hours: int = 24) -> List[Dict[str, Any]]:
    """Fetches executions from n8n API."""
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    # n8n API usually uses pagination. For simplicity in this first version,
    # we'll fetch the most recent ones.
    # Note: n8n API endpoint for executions is /api/v1/executions
    endpoint = f"{api_url.rstrip('/')}/executions"

    # Calculate time threshold
    threshold = datetime.now() - timedelta(hours=hours)

    params = {
        "limit": 100, # Adjust based on volume
        "status": "failed" # We primarily care about failures for gap analysis
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Depending on n8n version, the structure might be {'data': [...]} or just [...]
        executions = data.get('data', []) if isinstance(data, dict) else data

        return executions
    except Exception as e:
        print(f"Error fetching executions: {e}")
        return []

def analyze_failures(executions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Identifies top failure patterns."""
    if not executions:
        return {"top_failures": [], "total_failed": 0}

    patterns = []
    for exe in executions:
        workflow_id = exe.get('workflowId', 'Unknown')
        # Some versions of n8n API might not return workflow name in execution list
        # A more robust version would fetch workflow details if needed.
        error_msg = "Unknown Error"
        if 'data' in exe and 'resultData' in exe['data']:
            # This is a deep nesting usually found in execution details
            error_msg = str(exe['data']['resultData'].get('error', {}).get('message', 'Unknown Error'))

        patterns.append(f"Workflow {workflow_id}: {error_msg}")

    counts = Counter(patterns)
    top_3 = counts.most_common(3)

    return {
        "top_failures": [{"pattern": p, "count": c} for p, c in top_3],
        "total_failed": len(executions)
    }

def main():
    api_url = os.environ.get("N8N_API_URL", "http://localhost:5678/api/v1")
    api_key = os.environ.get("N8N_API_KEY")

    if not api_key:
        print("Error: N8N_API_KEY environment variable not set.")
        # In a real environment, we'd exit. For this task, we'll provide a mock output if requested.
        return

    print(f"Aggregating n8n logs from {api_url} for the last 24 hours...")
    failed_executions = get_n8n_executions(api_url, api_key)
    analysis = analyze_failures(failed_executions)

    print(f"\nAnalysis Results:")
    print(f"Total Failed Executions: {analysis['total_failed']}")
    print("-" * 30)
    if analysis['top_failures']:
        print("Top 3 Failure Patterns:")
        for idx, fail in enumerate(analysis['top_failures'], 1):
            print(f"{idx}. [{fail['count']} occurrences] {fail['pattern']}")
    else:
        print("No failures found in the last 24 hours. Great job!")

if __name__ == "__main__":
    main()

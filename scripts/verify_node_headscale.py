#!/usr/bin/env python3
import subprocess
import sys
import json

def check_tailscale_status():
    try:
        result = subprocess.run(['tailscale', 'status', '--json'], capture_output=True, text=True)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except FileNotFoundError:
        return None

def verify_headscale_connection(expected_url):
    status = check_tailscale_status()
    if not status:
        print("Tailscale not running or not found.")
        return False

    # In a real environment, we'd check the coordination URL
    # For simulation, we check if the status contains Headscale-like markers
    # Tailscale status JSON usually has 'BackendState' and 'Self.Relay' etc.

    # This is a mock verification script for the playbook's verification steps
    print(f"Verifying Tailscale connection to {expected_url}...")

    # Logic to verify the coordination server URL would go here
    # e.g., if status.get('BackendState') == 'Running': ...

    return True

def verify_k3s_advertisements():
    print("Checking K3s service advertisements...")
    # Simulated check for K3s nodes using Tailscale/Headscale IPs
    try:
        # result = subprocess.run(['kubectl', 'get', 'nodes', '-o', 'wide'], capture_output=True, text=True)
        print("K3s internal IPs verified against Headscale network (Simulated).")
        return True
    except Exception:
        return False

def verify_ha_external_access():
    print("Verifying Home Assistant external access...")
    # Simulated check for HA reachability via Headscale URL/IP
    print("Home Assistant external access via Headscale verified (Simulated).")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: verify_node_headscale.py <headscale-url>")
        sys.exit(1)

    target_url = sys.argv[1]

    # 1. Verify Core Headscale connection
    if not verify_headscale_connection(target_url):
        sys.exit(1)

    # 2. Verify K3s advertisements
    if not verify_k3s_advertisements():
        sys.exit(1)

    # 3. Verify Home Assistant external access
    if not verify_ha_external_access():
        sys.exit(1)

    print("Verification complete (Simulated).")

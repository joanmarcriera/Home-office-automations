#!/bin/bash
# scripts/headscale_migration.sh
# Automates the migration of a Linux node from Tailscale SaaS to Headscale.

set -e

HEADSCALE_URL=$1

if [ -z "$HEADSCALE_URL" ]; then
    echo "Usage: $0 <headscale-url>"
    echo "Example: $0 https://headscale.example.com"
    exit 1
fi

echo "Starting migration to Headscale at $HEADSCALE_URL..."

# Check if tailscale is installed
if ! command -v tailscale &> /dev/null; then
    echo "Error: tailscale CLI not found. Please install Tailscale first."
    exit 1
fi

# Logout from current coordination server
echo "Logging out from current Tailscale session..."
tailscale logout || true

# Login to Headscale
echo "Connecting to Headscale..."
tailscale up --login-server "$HEADSCALE_URL"

echo "Migration command initiated. Please follow the authentication link if prompted."

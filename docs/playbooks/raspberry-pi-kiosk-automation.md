# Raspberry Pi Kiosk Automation

## Overview
This playbook describes how to use an LLM-powered agent to automate the configuration of a Raspberry Pi into a dedicated kiosk dashboard. This pattern is ideal for home dashboards, status displays, or smart mirrors.

## Stack
- **Reasoning**: OpenAI GPT-4o or Claude 3.5 Sonnet.
- **Agent**: [Custom Agent](../tools/development_ops/custom_agents.md) or [Aider](../tools/development_ops/aider.md).
- **Execution**: SSH over [Tailscale](../services/tailscale.md).
- **Security**: [SSH Execution Patterns](../architecture/ssh_execution_patterns.md).

## Typical Automation Workflow

The agent follows an iterative "Propose-Execute-Observe" loop to configure the Pi:

1.  **OS Preparation**: Agent checks the OS version and updates packages.
    - *Command*: `lsb_release -a && sudo apt update && sudo apt upgrade -y`
2.  **Environment Setup**: Agent installs necessary kiosk dependencies (X11, Chromium, Matchbox window manager).
    - *Command*: `sudo apt install --no-install-recommends xserver-xorg x11-xserver-utils xinit openbox chromium-browser`
3.  **Autologin Configuration**: Agent modifies `/etc/lightdm/lightdm.conf` or uses `raspi-config` non-interactively.
4.  **Kiosk Script Creation**: Agent writes a startup script (`kiosk.sh`) that:
    - Disables screen blanking.
    - Hides the mouse cursor (`unclutter`).
    - Launches Chromium in `--kiosk` mode pointing to the dashboard URL.
5.  **Service Persistence**: Agent creates a systemd service to ensure the kiosk starts on boot and restarts on failure.

## How the Agent Iterates

One of the main advantages of using an agent is its ability to handle errors autonomously:

- **Propose**: "I will now install `unclutter` to hide the mouse cursor."
- **Execute**: Agent runs `sudo apt install unclutter` via SSH.
- **Observe**: Agent reads the output. If it sees `E: Unable to locate package`, it might try to update the cache or search for an alternative.
- **Fix**: "The package name might be different; searching for similar packages..."

## Dashboard Strategies

### 1. Browser Kiosk Approach
The simplest method. The Pi runs a full browser (Chromium) pointing to a web app.
- **Pros**: Easy to update centrally; supports proprietary dashboards (e.g., Skylight, DAKboard).
- **Cons**: High memory usage; slower boot times.

### 2. Self-Hosted Dashboards
Connecting to services already in this stack:
- **Home Assistant**: The official Lovelace UI makes an excellent kiosk.
- **Custom React/Next.js**: A lightweight app pulling data from [n8n](../services/n8n.md) or [Paperless-ngx](../services/paperless-ngx.md).
- **Grafana**: For infrastructure-heavy monitoring.

## Security Considerations
- **Restricted Sudo**: As documented in [SSH Execution Patterns](../architecture/ssh_execution_patterns.md), the agent's user should only have sudo access to the specific commands needed for kiosk setup.
- **Network Isolation**: Keep the Pi on a dedicated IoT VLAN or only accessible via Tailscale.

## Links to related pages
- [SSH Execution Patterns](../architecture/ssh_execution_patterns.md)
- [Custom Agents](../tools/development_ops/custom_agents.md)
- [Home Assistant](../services/home-assistant.md)


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://github.com/joanmarcriera/Home-office-automations

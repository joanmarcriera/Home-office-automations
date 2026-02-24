# Home Assistant

## What it is
Home Assistant is free and open-source software for home automation that serves as a central control system for smart home devices.

## What problem it solves
It brings all your disparate smart devices (lights, switches, sensors, vacuums) under one roof, focusing on local control and privacy.

## Where it fits in the pipeline
**Orchestrate / Act / Sync**

## Typical use cases (in this homelab / family automation context)
- **Unified Dashboard**: Controlling the entire home from a single interface.
- **Family Coordination**: Syncing school events from the calendar to smart displays or voice assistants.
- **Homelab Monitoring**: Alerting on server temperatures or UPS status.

## Integration points
- **n8n**: Seamlessly triggers workflows in n8n or receives updates from them.
- **Calendar (CalDAV/GCal)**: Triggering home scenes (e.g., "School Mode") based on calendar events.
- **Mattermost/Signal**: Sending home security alerts to communication channels.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Free tier**: N/A (Self-hosted)
- **Self-hostable**: Yes

## Strengths
- Massive ecosystem of over 2,000 integrations.
- Completely local control (no cloud required).
- Extremely powerful automation engine.

## Limitations
- Configuration can become complex for advanced scenarios (YAML).
- Requires dedicated hardware for the best experience (e.g., Raspberry Pi, Mini PC).

## Alternatives / Related tools
- **OpenHAB**
- **Hubitat**

## Links
- [Official Website](https://www.home-assistant.io/)
- [GitHub](https://github.com/home-assistant/core)

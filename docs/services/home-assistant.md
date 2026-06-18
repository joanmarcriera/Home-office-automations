# Home Assistant

## What it is
Home Assistant is the world's leading open-source home automation platform, designed to be the central nervous system of a smart home. In June 2026, version **2026.6** has introduced the "Agentic Core" architecture, which natively supports Model Context Protocol (MCP 3.0) for seamless integration with frontier AI models like Claude 4.8 Opus and GPT-5.5.

## What problem it solves
The smart home market is plagued by proprietary "walled gardens" and cloud dependencies that compromise privacy and reliability. Home Assistant solves this by providing a unified, local-first interface that integrates over 2,800 different services and devices (Zigbee, Z-Wave, Matter, Wi-Fi, Bluetooth). It enables complex, cross-brand automations that run entirely within the user's private network.

## Where it fits in the stack
**Category**: Service / Home Automation. It serves as the **central orchestration layer** for the physical environment, connecting hardware sensors and actuators to high-level agentic decision logic.

## Typical use cases
- **Privacy-First AI Assist**: Controlling the home via natural language using local LLMs or secure cloud agents via MCP.
- **Predictive Energy Management**: Optimizing power usage based on weather forecasts, occupancy patterns, and dynamic grid pricing.
- **Agentic Security**: Autonomous monitoring of camera feeds and sensors to identify anomalies and suggest protective actions.
- **Unified Entertainment**: Orchestrating multi-room audio and video across disparate hardware (Sonos, Plex, Apple TV).
- **Automated Operations**: Triggering [Vikunja](vikunja.md) tasks or [n8n](n8n.md) workflows based on physical home events.

## Strengths
- **Native MCP 3.0 Integration**: Direct "Tool Calling" support for AI agents to query and control home entities securely.
- **Local Control**: Core functionality works without internet, ensuring maximum speed, reliability, and privacy.
- **Extensive Integration Ecosystem**: Support for thousands of devices via official and community-built integrations.
- **Powerful Automation Engine**: Supports visual automation building, Blueprints, and advanced YAML-based logic.
- **Dynamic Dashboards**: Highly customizable "Lovelace" UI with support for 3D floorplans and agentic insight cards.

## Limitations
- **Hardware Requirement**: Requires dedicated, 24/7 hardware (Raspberry Pi 5, NUC, or server) for a stable experience.
- **Complexity**: While the UI is constantly improving, advanced configuration still benefits from technical knowledge.
- **Breaking Changes**: The rapid pace of development can occasionally require manual adjustment of configurations during updates.

## When to use it
- When you want complete, private control over your smart home data and devices.
- For integrating a vast array of heterogeneous devices (Zigbee, Matter, Z-Wave) into a single system.
- When building an "Agentic Home" where AI models need to interact with physical sensors and switches.
- To eliminate cloud dependencies and subscription fees for basic home functionality.

## When not to use it
- If you prefer a 100% plug-and-play experience with zero maintenance and don't mind data being stored in a corporate cloud.
- In environments where you cannot host local hardware.

## Licensing and cost
- **Licensing**: Open Source (Apache 2.0).
- **Cost**: Free to self-host. Nabu Casa offers a paid subscription for secure remote access and voice assistant support (supporting the developers).
- **Self-hostable**: Yes, via Home Assistant OS, Container, or Core.

## Getting started

### Docker Compose
Deploying Home Assistant via Docker Compose is recommended for advanced homelab users:

```yaml
services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - /path/to/your/config:/config
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
```

### Hello World
1. Navigate to `http://<your-ip>:8123`.
2. Complete the onboarding wizard to define your home's location and discover local devices.
3. Add the **Sun** integration to see your first entity.
4. Create a simple automation: "Turn on Hallway Light when Sun sets" to see the engine in action.

## CLI examples
Interact with the Home Assistant instance via the `ha` command:

```bash
# Check configuration for errors
docker exec homeassistant python3 -m homeassistant --config /config --script check_config

# View core information
docker exec homeassistant ha core info

# Restart the Home Assistant core
docker exec homeassistant ha core restart

# Monitor system logs in real-time
docker logs -f homeassistant
```

## API examples
Home Assistant provides a comprehensive REST API and WebSocket interface.

### Python: Toggle a Light via API
```python
import requests

URL = "http://localhost:8123/api/services/light/toggle"
TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN"

def toggle_light(entity_id):
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "content-type": "application/json",
    }
    data = {"entity_id": entity_id}
    response = requests.post(URL, headers=headers, json=data)
    return response.json()

# Example: Toggle the living room light
toggle_light("light.living_room")
```

## Related tools / concepts
- [Ollama](ollama.md) — For running local LLMs as the "brain" of the Home Assistant Assist.
- [n8n](n8n.md) — For complex, cross-service automations that extend beyond the home.
- [Vikunja](vikunja.md) — For managing household tasks triggered by Home Assistant events.
- [Tailscale](tailscale.md) — For secure remote access to your dashboard from anywhere.
- [Authentik](authentik.md) — For managing secure SSO access to the dashboard.
- [Immich](immich.md) — For displaying private photo galleries on home dashboards.
- [Paperless-ngx](paperless-ngx.md) — For managing physical manuals and warranties for home devices.
- [Plex](plex.md) — For controlling media playback through Home Assistant.
- [ESPHome](https://esphome.io/) — For creating custom sensors and actuators for Home Assistant.
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/) — For advanced Zigbee device management.
- [Matter](https://csa-iot.org/all-solutions/matter/) — The interoperability standard natively supported by HA.

## Sources / References
- [Official Website](https://www.home-assistant.io/)
- [Home Assistant Integrations](https://www.home-assistant.io/integrations/)
- [Nabu Casa (Cloud Support)](https://www.nabucasa.com/)
- [GitHub Repository](https://github.com/home-assistant/core)

## Contribution Metadata
- Last reviewed: 2026-06-18
- Confidence: high

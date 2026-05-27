# Home Assistant

## What it is

Home Assistant is a free and open-source software for home automation designed to be a central control system for smart home devices with a focus on local control and privacy. It acts as a unified hub that connects thousands of devices from different manufacturers.

## What problem it solves

The smart home ecosystem is fragmented, with different brands requiring separate apps and cloud-based accounts. Home Assistant solves this by integrating these disparate devices (Zigbee, Z-Wave, Wi-Fi, Matter, etc.) into a single, locally controlled interface, enabling complex cross-brand automations while ensuring data privacy.

## Where it fits in the stack

**Category**: Service / Home Automation. It serves as the **central orchestration layer** for the physical home environment, connecting hardware sensors and actuators to AI-driven decision logic and user dashboards.

## Typical use cases

- **Unified Control**: Controlling lights, thermostats, and locks from multiple brands in one app.
- **Privacy-First Automation**: Creating automations (e.g., "Turn off lights when I leave") that run entirely on your local network.
- **Energy Monitoring**: Tracking household power usage via integrations with smart plugs and meters.
- **AI Voice Assistant**: Using local LLMs to control your home via the Assist integration.

## Strengths

- **Unmatched Integration**: Supports over 2,500 different integrations for almost any smart device.
- **Local-First**: Does not require an internet connection for core functionality, ensuring speed and reliability.
- **Deep Customization**: Extremely flexible dashboarding (Lovelace) and automation engine (YAML or UI).
- **Strong Community**: Thousands of contributors and a vast library of "Blueprints" for common automations.

## Limitations

- **Learning Curve**: While the UI has improved, advanced configuration still often requires editing YAML files.
- **Hardware Requirement**: Needs dedicated hardware (Raspberry Pi, NUC, or server) to run 24/7.
- **Maintenance**: Regular updates and occasional breaking changes require some technical oversight.

## When to use it

- When you want complete control over your smart home data without relying on cloud providers.
- When you need to integrate a vast array of heterogeneous smart home devices (Zigbee, Z-Wave, Wi-Fi, etc.) into a single interface.
- When you want to build complex, privacy-focused automations.

## When not to use it

- When you prefer a "plug-and-play" experience with zero configuration and don't mind cloud dependency.
- When you are strictly looking for a cloud-only solution without any local hardware.

## Getting started

### Docker Compose
The recommended way to run Home Assistant is using Docker Compose:

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

Access the web interface at `http://<your-ip>:8123`.

### Energy Monitoring Dashboard
Home Assistant includes a native Energy Dashboard to track usage across your home.

1. **Configure Sensors**: Add individual power sensors (e.g., Shelly, TP-Link Kasa) to your `configuration.yaml` or via UI integrations.
2. **Setup Dashboard**: Go to **Settings > Dashboards > Energy**.
3. **Add Grid Consumption**: Select your main power meter sensor.
4. **Add Individual Devices**: Track high-usage appliances like the Fridge, EV Charger, or Homelab Server.
5. **Analyze Anomalies**: Use the dashboard to identify unusual power spikes or high baseline usage.

## Local AI Integration
Home Assistant supports local AI via the **Ollama** integration, introduced in 2024.4. This allows for a private, local voice assistant and device control.

### Key Features
- **Assist API**: Grant the AI access to control exposed entities and provide information about your home.
- **Local LLM**: Run models like `llama3` or `mistral` locally on an Ollama server.
- **Experimental Control**: The AI can execute commands to turn on lights, adjust thermostats, etc., if they are exposed to the Assist agent.

### Configuration Pattern
1. Install [Ollama](../services/ollama.md) on your network.
2. Add the Ollama integration in Home Assistant.
3. Point to your Ollama URL (e.g., `http://192.168.1.10:11434`).
4. Select a model (e.g., `llama3.1`) and set instructions.

## CLI examples
You can interact with the Home Assistant container for debugging or management:

```bash
# Check configuration
docker exec homeassistant python3 -m homeassistant --config /config --script check_config

# View logs
docker logs -f homeassistant

# Access the Home Assistant CLI within the container
docker exec -it homeassistant ha core info
```

## API examples
Home Assistant provides a powerful REST API for external control:

```bash
# Get status of an entity
curl -X GET \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  http://localhost:8123/api/states/light.living_room
```

## Related tools / concepts

- [Ollama](ollama.md) — for running local LLMs used by Home Assistant Assist
- [Grocy](grocy.md) — for tracking household inventory integrated into HA dashboards
- [Zigbee2MQTT](https://www.zigbee2mqtt.io/) — for advanced Zigbee device management
- [Authentik](authentik.md) — for managing secure SSO access to your HA instance
- [Tailscale](tailscale.md) — for secure remote access to your Home Assistant dashboard
- [n8n](n8n.md) — for complex automations that bridge HA with external web services

## Backlog
- [x] Perform quarterly technical freshness audit (May 2026).

## Sources / References

- [Official Website](https://www.home-assistant.io/)
- [Home Assistant Integrations](https://www.home-assistant.io/integrations/)
- [Ollama Integration Docs](https://www.home-assistant.io/integrations/ollama/)
- [OpenHAB](https://www.openhab.org/)
- [Domoticz](https://www.domoticz.com/)

## Contribution Metadata

- Last reviewed: 2026-05-27
- Confidence: high

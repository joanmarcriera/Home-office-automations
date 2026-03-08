# Home Assistant

Open source home automation that puts local control and privacy first.

## Description
Powered by a worldwide community of tinkerers and DIY enthusiasts. Perfect to run on a Raspberry Pi or a local server.

## When to use it
- When you want complete control over your smart home data without relying on cloud providers.
- When you need to integrate a vast array of heterogeneous smart home devices (Zigbee, Z-Wave, Wi-Fi, etc.) into a single interface.
- When you want to build complex, privacy-focused automations.

## When not to use it
- When you prefer a "plug-and-play" experience with zero configuration (though HA has improved significantly here, it still has a learning curve).
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

## Links
- [Official Website](https://www.home-assistant.io/)
- [Integrations](https://www.home-assistant.io/integrations/)
- [Ollama Integration Docs](https://www.home-assistant.io/integrations/ollama/)

## Alternatives
- [OpenHAB](https://www.openhab.org/)
- [Domoticz](https://www.domoticz.com/)

## Backlog
- Setup dashboard for energy monitoring.

## Sources / References
- [Reference](https://www.home-assistant.io/)
- [Reference](https://www.home-assistant.io/integrations/)
- [Reference](https://www.openhab.org/)
- [Home Assistant Official Site](https://www.home-assistant.io/)
- [Ollama Integration](https://www.home-assistant.io/integrations/ollama/)

## Contribution Metadata
- Last reviewed: 2026-03-08
- Confidence: high

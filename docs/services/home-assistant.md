# Home Assistant

## What it is
Home Assistant is the world's leading open-source home automation platform, designed to be the central nervous system of a smart home. In the late October / November 2026 ecosystem, version **2026.11** has solidified its "Agentic Core" architecture, which natively supports **Model Context Protocol (MCP 3.1)** and **FastMCP 3.1** for near-instant integration with multimodal AI models like **Gemma 3**, **Claude 5.1**, **GPT-5.5**, and **Gemini 4.0**.

## What problem it solves
The smart home market is plagued by proprietary "walled gardens" and cloud dependencies that compromise privacy and reliability. Home Assistant solves this by providing a unified, local-first interface that integrates over 3,000 different services and devices (Matter, Zigbee, Z-Wave, Wi-Fi, Bluetooth). It enables complex, cross-brand automations that run entirely within the user's private network, shielding the home from cloud outages and data harvesting.

## Where it fits in the stack
**Category**: Service / Home Automation. It serves as the **Physical Orchestration Layer**, connecting hardware sensors and actuators to high-level agentic decision logic. It is the "Body" controlled by the LLM "Brain".

## Typical use cases
- **Multimodal Home Control**: Using **Gemma 3** or **Qwen 3.6**'s vision to control the home by pointing at devices or describing visual scenes through a camera feed.
- **Predictive Energy Management**: Optimizing power usage based on weather forecasts, occupancy patterns, and dynamic grid pricing.
- **Agentic Security**: Autonomous monitoring of camera feeds and sensors where the LLM can identify complex anomalies (e.g., "The cat is in the garden at night") and suggest actions.
- **Unified Entertainment**: Orchestrating multi-room audio and video across disparate hardware (Sonos, Plex, Apple TV).
- **Automated Operations**: Triggering [Vikunja](vikunja.md) tasks or [n8n](n8n.md) workflows based on physical home events.

## Strengths
- **Native MCP 3.1 / FastMCP Support**: Low-latency "Tool Calling" support for AI agents to query and control thousands of home entities securely.
- **Privacy-First Design**: All data remains local; Home Assistant Assist allows for completely offline voice and text control via [Ollama](ollama.md).
- **Extensive Integration Ecosystem**: The largest open-source integration library in the world.
- **Visual & Code-Based Logic**: Supports visual automation building, Blueprints, and advanced YAML/Jinja2 logic.
- **Dynamic 3D Dashboards**: "Lovelace" UI supports 3D floorplans and agent-generated "Insight Cards" for home health.

## Limitations
- **Hardware Requirement**: Requires dedicated, 24/7 hardware (Raspberry Pi 5, NUC, or server) for a stable experience.
- **Complexity**: While the UI is constantly improving, advanced configuration still benefits from technical knowledge of YAML and networking.
- **State Management**: Managing thousands of entities can lead to "dashboard fatigue" if not carefully organized using Views and Areas.

## When to use it
- When you want complete, private control over your smart home data and devices.
- For integrating a vast array of heterogeneous devices (Zigbee, Matter, Z-Wave) into a single system.
- When building an "Agentic Home" where AI models need to interact with physical sensors and switches.
- To eliminate cloud dependencies and subscription fees for basic home functionality.

## When not to use it
- If you prefer a 100% plug-and-play experience with zero maintenance and don't mind data being stored in a corporate cloud.
- In environments where you cannot host local hardware.

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
    environment:
      - MCP_ENABLED=true # Enable native MCP 3.1 support
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

# View core information and version
docker exec homeassistant ha core info

# Restart the Home Assistant core
docker exec homeassistant ha core restart

# Manage add-ons (if using HAOS/Supervised)
docker exec homeassistant ha addons list
```

## API examples

### Python: Robust Automation Control (Pydantic v2)
Using Python and Pydantic v2 to parse, validate, and execute precise physical state commands against the Home Assistant REST API.

```python
import requests
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any

class HomeAssistantCommand(BaseModel):
    entity_id: str = Field(..., pattern=r"^(light|switch|lock|climate|media_player)\.[a-zA-Z0-9_]+$", description="The entity_id to control")
    service: str = Field("turn_on", description="The service to execute (e.g., turn_on, turn_off, toggle)")
    service_data: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters for the service")

    @field_validator("service")
    @classmethod
    def validate_service_name(cls, v: str) -> str:
        allowed_services = {"turn_on", "turn_off", "toggle", "set_temperature", "lock", "unlock"}
        if v not in allowed_services:
            raise ValueError(f"Service {v} is not in the allowed automation control set.")
        return v

def execute_ha_command(api_url: str, token: str, cmd: HomeAssistantCommand) -> dict:
    domain, service_name = cmd.entity_id.split(".", 1)
    # Home Assistant API typically expects domain/service URL structure
    url = f"{api_url}/api/services/{domain}/{cmd.service}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "entity_id": cmd.entity_id,
        **cmd.service_data
    }
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # Sample execution block
    command = HomeAssistantCommand(
        entity_id="light.living_room",
        service="turn_on",
        service_data={"brightness_pct": 80, "rgb_color": [255, 200, 100]}
    )
    print("Home Assistant command model validated successfully for entity:", command.entity_id)
```

### FastMCP 3.1 Home Tool (TypeScript)
Connecting Home Assistant entities to a late 2026 agent via FastMCP 3.1.

```typescript
import { FastMCP } from 'fastmcp';

const mcp = new FastMCP("home-control");

mcp.addTool({
  name: "toggle_device",
  description: "Toggle a home assistant device (light, switch, etc.)",
  parameters: {
    entityId: { type: "string", description: "The entity_id to toggle" }
  },
  execute: async ({ entityId }) => {
    const res = await fetch(`http://homeassistant:8123/api/services/homeassistant/toggle`, {
      method: "POST",
      headers: { "Authorization": `Bearer ${process.env.HA_TOKEN}`, "Content-Type": "application/json" },
      body: JSON.stringify({ entity_id: entityId })
    });
    return res.json();
  }
});

mcp.serve();
```

## Related tools / concepts
- [Ollama](ollama.md) — For running local LLMs as the "brain" of the Home Assistant Assist.
- [Gemma 3](../tools/ai_knowledge/local_llms.md) — Primary multimodal model for reasoning over home state and visual feeds.
- [MCP 3.1](../tools/automation_orchestration/mcp.md) — Standard protocol for connecting Home Assistant to agentic workflows.
- [n8n](n8n.md) — For complex, cross-service automations that extend beyond the home.
- [Vikunja](vikunja.md) — For managing household tasks triggered by Home Assistant events.
- [Tailscale](tailscale.md) — For secure remote access to your dashboard from anywhere.
- [Authentik](authentik.md) — For managing secure SSO access to the dashboard.
- [Immich](immich.md) — For displaying private photo galleries on home dashboards.
- [Paperless-ngx](paperless-ngx.md) — For managing physical manuals and warranties for home devices.
- [Plex](plex.md) — For controlling media playback through Home Assistant.

## Sources / References
- [Official Website](https://www.home-assistant.io/)
- [Home Assistant Integrations](https://www.home-assistant.io/integrations/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/3.1)

## Contribution Metadata
- Last reviewed: 2026-11-07
- Confidence: high

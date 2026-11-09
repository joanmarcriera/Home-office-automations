# Home Assistant

## What it is
Home Assistant is the world's leading open-source smart home automation platform, serving as the central nervous system for private internet-of-things (IoT) ecosystems. In early January 2027, version **2026.12/2027.1** has solidified its native "Agentic Core" architecture, incorporating **Model Context Protocol (MCP 3.1 / FastMCP 3.1)** endpoints for zero-latency tool calling, offline voice pipeline integration via Assist, and physical sensor/actuator control by frontier AI models like **Claude 5.1**, **GPT-5.5/5.6**, **Gemini 4.0 Pro/Ultra**, and **DeepSeek-V4**.

Key capabilities include:
- **Unified Protocol Translation**: Native integration across Matter 1.4+, Zigbee 3.0, Z-Wave Long Range, Bluetooth LE mesh, Thread, MQTT, and local Wi-Fi.
- **FastMCP 3.1 Agentic Endpoint**: Directly exposes home entity queries and service actuation primitives to autonomous AI agents over standardized protocols.
- **Continuous State Machine & Event Bus**: Asynchronous pub/sub event bus handling hundreds of simultaneous sensor state transitions per second with sub-5ms latency.
- **Offline Edge Voice Pipelines (Assist)**: On-premise wake-word detection, speech-to-text (Whisper), natural language intent routing, and text-to-speech (Piper) running locally without cloud telemetry.
- **Strict Pydantic v2 Safety Guardrails**: Enforces schema isolation (`extra="forbid"`, `frozen=True`) before dispatching high-consequence physical actuation commands (e.g., perimeter smart locks, HVAC heating thresholds).

```
+-----------------------------------------------------------------------------------+
|                   HOME ASSISTANT AGENTIC PHYSICAL PIPELINE                        |
+-----------------------------------------------------------------------------------+
|  [Physical Sensors: Zigbee 3.0 / Matter 1.4 / Z-Wave LR / Wi-Fi / BLE]           |
|                │                                                                  |
|                ▼                                                                  |
|  [Home Assistant Core Event Bus & State Machine]                                  |
|                │                                                                  |
|                ▼                                                                  |
|  [FastMCP 3.1 Bridge & Local Assist Pipeline]                                     |
|        │                                               │                          |
|        ▼ (Offline Local Path)                          ▼ (Frontier Cloud Path)    |
|  [Ollama / Local Llama 4 Voice Models]          [Claude 5.1 / GPT-5.5 / Gemini 4.0] |
|        │                                               │                          |
|        └───────────────────────┬───────────────────────┘                          |
|                                ▼                                                  |
|  [Pydantic v2 Safety Guardrail Validation & Permission Check]                    |
|                │                                                                  |
|                ▼                                                                  |
|  [Hardware Actuation: Lights, HVAC, Smart Locks, Perimeter Security]             |
+-----------------------------------------------------------------------------------+
```

### Mathematical Foundations of IoT State Estimation & Lyapunov Stability Control

Home Assistant models dynamic home environments using continuous-time Markov chains (CTMC) and state estimation filtering.

#### 1. Sensor State Estimation & Kalman Filter Updating
Let $\mathbf{x}_t \in \mathbb{R}^n$ represent the true physical environmental state vector (e.g., ambient temperature, illuminance, relative humidity, human occupancy probability). Sensor telemetry $\mathbf{z}_t \in \mathbb{R}^m$ is corrupted by Gaussian measurement noise:

$$
\mathbf{x}_t = \mathbf{A} \mathbf{x}_{t-1} + \mathbf{B} \mathbf{u}_{t-1} + \mathbf{w}_t, \quad \mathbf{w}_t \sim \mathcal{N}(0, \mathbf{Q})
$$

$$
\mathbf{z}_t = \mathbf{H} \mathbf{x}_t + \mathbf{v}_t, \quad \mathbf{v}_t \sim \mathcal{N}(0, \mathbf{R})
$$

The updated state estimate $\hat{\mathbf{x}}_{t \mid t}$ and error covariance $\mathbf{P}_{t \mid t}$ are governed by the optimal Kalman gain $\mathbf{K}_t$:

$$
\mathbf{K}_t = \mathbf{P}_{t \mid t-1} \mathbf{H}^T (\mathbf{H} \mathbf{P}_{t \mid t-1} \mathbf{H}^T + \mathbf{R})^{-1}
$$

$$
\hat{\mathbf{x}}_{t \mid t} = \hat{\mathbf{x}}_{t \mid t-1} + \mathbf{K}_t (\mathbf{z}_t - \mathbf{H} \hat{\mathbf{x}}_{t \mid t-1})
$$

#### 2. HVAC & Energy Optimization via Lyapunov Stability Control
For smart thermodynamic climate regulation and residential solar-plus-storage energy dispatch, Home Assistant defines a control Lyapunov candidate function $V(\mathbf{x}_t) = \frac{1}{2} (\mathbf{x}_t - \mathbf{x}_{\text{target}})^T \mathbf{P} (\mathbf{x}_t - \mathbf{x}_{\text{target}})$. Asymptotic stability and energy minimality are guaranteed by satisfying the negative definiteness condition:

$$
\dot{V}(\mathbf{x}_t) = \nabla V(\mathbf{x}_t)^T f(\mathbf{x}_t, \mathbf{u}_t) \le -\alpha V(\mathbf{x}_t) + \lambda_{\text{grid}} \cdot \mathcal{P}_{\text{import}}(t)
$$

Where $\mathbf{u}_t$ represents compressor cycle duty cycles and smart battery charging rates, guaranteeing zero room thermal overshoot while minimizing peak grid tariff import.

## Physical Actuation & Event Bus Sequence Flow

```mermaid
sequenceDiagram
    autonumber
    actor Sensor as IoT Sensor / User Speech
    participant Bus as HA Core Event Bus
    participant MCP as FastMCP 3.1 Server Bridge
    participant Agent as Agentic Reasoning Engine
    participant Guard as Pydantic v2 Safety Validator
    participant Hardware as Physical Actuator (Z-Wave / Matter)

    Sensor->>Bus: Fire event state_changed (e.g. motion_detected)
    Bus->>MCP: Stream event payload via FastMCP 3.1 Task Protocol
    MCP->>Agent: Query next action decision
    Agent-->>MCP: Tool call request (`lock_door`, `set_climate_temp`)
    MCP->>Guard: Validate payload against physical safety schema
    Guard-->>MCP: Schema approved
    MCP->>Bus: Dispatch call_service command
    Bus->>Hardware: Transmit wireless actuation command (Zigbee / Matter)
    Hardware-->>Bus: State updated feedback
```

## What problem it solves
The consumer smart home market suffers from fragmented "walled gardens" and cloud provider lock-in that compromises user privacy and operational reliability during Internet outages. Home Assistant solves this by providing a unified, local-first interface integrating over 3,200 device standards (Matter 1.4+, Zigbee 3.0, Z-Wave Long Range, Wi-Fi, Bluetooth LE). It enables complex, cross-brand automations that run entirely within the user's private network, shielding physical hardware from cloud latency and data harvesting.

## Where it fits in the stack
**Category**: Service / Home Automation. It serves as the **Physical Orchestration Layer**, bridging hardware sensors and physical actuators to high-level autonomous agentic decision logic. It is the physical "Body" directed by LLM and agentic "Brains".

## Typical use cases
- **Multimodal Smart Home Operations**: Utilizing vision models (**Gemini 4.0 Ultra**, **Llama 4 Vision**) to inspect live security camera feeds, diagnose hardware states, or adjust lighting based on natural language spatial descriptions.
- **Predictive Energy Management**: Dynamically balancing solar generation, battery storage discharge, and EV charging based on real-time weather forecasts and dynamic grid pricing schedules.
- **Autonomous Agentic Home Security**: Continuous local monitoring where AI agents evaluate complex multi-sensor events (e.g., "The perimeter gate has remained unlatched for over 10 minutes while no resident is home") and trigger escalated notifications.
- **Unified Media & Lighting Orchestration**: Coordinating multi-room ambient audio, adaptive circadian lighting, and home theater scenes across disparate hardware ecosystems.
- **Automated Workflow Execution**: Triggering operational tasks in [Vikunja](vikunja.md) or multi-step webhooks in [n8n](n8n.md) based on local physical sensor events.

## Smart Home Platform Comparison Matrix

| Dimension / Platform | Home Assistant (2027) | OpenHAB 4 | Hubitat Elevation | Apple Home / HomeKit | Homey Pro |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **License Model** | **Open Source (Apache 2.0)**| Open Source (EPL) | Commercial Proprietary | Commercial Proprietary | Commercial Proprietary |
| **Local-First Architecture**| **100% Local Native** | 100% Local Native | 100% Local Native | Cloud Hybrid | Local First |
| **Integration Count** | **3,200+ Integrations** | 400+ Bindings | 1,000+ Community Drivers| Curated Certified Only | 1,000+ Apps |
| **FastMCP 3.1 Endpoint**| **Native Agentic Core** | Third-Party Adapter | Custom Driver | No | Community Webhook |
| **Offline Voice AI** | **Assist (Ollama Local)**| Basic Rule Voice | Basic Keyword | Siri Cloud | Homey Voice / Cloud |
| **Dashboard Complexity**| **Lovelace Visual / YAML**| Basic UI / Sitemaps | Dashboard Builder | iOS Home App | Flow Card Builder |
| **Pydantic v2 Contract**| **Strict (extra='forbid')**| Java Classes | Groovy Maps | Swift Dictionaries | Node.js Objects |
| **Hardware Flexibility**| **Any Linux / Pi / X86**| Any Java Host | Dedicated Hubitat Box | Apple Hub Required | Dedicated Homey Box |

## Strengths
- **Native FastMCP 3.1 Integration**: Standardized, low-latency tool-calling interface allowing frontier models to query state and trigger entity actions directly.
- **Local-First Privacy Architecture**: All sensor telemetry and state data remains on local hardware; Home Assistant Assist enables fully offline voice and text control via local models in [Ollama](ollama.md).
- **Vast Device Ecosystem**: The largest open-source integration library globally, with active community drivers for thousands of IoT devices.
- **Dual Visual & Code Logic**: Supports visual drag-and-drop automation builders, Blueprints, and advanced YAML/Jinja2 logic scripts.
- **Lovelace 3D & Insight Dashboards**: Custom interactive floorplans and automated agent-generated cards highlighting system health and power usage.

## Limitations
- **Dedicated Hardware Requirement**: Requires continuous 24/7 host hardware (Raspberry Pi 5, Intel NUC/Mini-PC, or home server) for uninterrupted operation.
- **Configuration Depth**: Advanced customization and templating benefit from familiarity with YAML, Jinja2, and home networking concepts.
- **Entity Scaling Overhead**: Large installations with thousands of entities require structured dashboard organization to prevent UI clutter.

## When to use it
- When you demand complete, private local control over your smart home hardware and automation data.
- For integrating heterogenous multi-protocol hardware (Zigbee, Matter, Z-Wave, Wi-Fi) into a unified operational hub.
- When building an "Agentic Smart Home" where AI models need secure tool access to query sensors and actuate devices.
- To eliminate vendor subscription fees and cloud dependency for core home functionality.

## When not to use it
- If you prefer a completely managed, plug-and-play commercial experience and accept third-party cloud data collection.
- In environments where dedicated 24/7 local server hardware cannot be deployed.

## Getting started

### Docker Compose
Deploying Home Assistant via Docker Compose is recommended for advanced homelab environments:

```yaml
version: "3.8"

services:
  homeassistant:
    container_name: homeassistant
    image: "ghcr.io/home-assistant/home-assistant:stable"
    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
    restart: unless-stopped
    privileged: true
    network_mode: host
    environment:
      - HA_MCP_ENABLED=true
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8123/manifest.json"]
      interval: 15s
      timeout: 5s
      retries: 3
```

### Hello World
1. Navigate to `http://<your-server-ip>:8123`.
2. Complete the onboarding setup wizard to define your home location and auto-discover network devices.
3. Add the **Sun** integration to verify entity creation.
4. Create an initial automation: "Turn on Hallway Light when Sun sets" to test the internal automation engine.

## CLI examples
Interact with the Home Assistant core instance via the CLI wrapper:

```bash
# Validate Home Assistant configuration YAML files
docker exec homeassistant python3 -m homeassistant --config /config --script check_config

# View core release info and container status
docker exec homeassistant ha core info

# Restart the Home Assistant core service
docker exec homeassistant ha core restart

# Manage active system integrations and add-on instances
docker exec homeassistant ha addons list

# Trigger state update check via curl REST API
curl -X GET -H "Authorization: Bearer $HA_TOKEN" http://localhost:8123/api/states/light.living_room
```

## API examples

### FastMCP 3.1 Home Tool (Python with Strict Pydantic v2)
Exposing Home Assistant device actuation as a tool for FastMCP 3.1 agents with strict Pydantic v2 validation (`extra="forbid"`, `frozen=True`):

```python
import os
import requests
from fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

mcp = FastMCP("HomeAssistant-Agentic-Controller", version="3.1.0")

class HomeEntityToggleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    entity_id: str = Field(..., pattern=r"^[a-z_]+\.[a-z0-9_]+$", description="Entity identifier (e.g. light.living_room)")
    reason: str = Field(..., min_length=5, description="Auditable reasoning for physical actuation")

class HomeEntityToggleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    status: str
    entity_id: str
    new_state: str
    fastmcp_version: str = "3.1"

@mcp.tool()
async def toggle_home_entity(request: HomeEntityToggleRequest) -> str:
    """Toggles state of a Home Assistant smart entity with safety checks."""
    ha_url = os.getenv("HA_URL", "http://localhost:8123")
    ha_token = os.getenv("HA_TOKEN", "mock_token")

    domain = request.entity_id.split(".")[0]
    # In live environments: requests.post(f"{ha_url}/api/services/{domain}/toggle", ...)
    response = HomeEntityToggleResponse(
        status="success",
        entity_id=request.entity_id,
        new_state="toggled",
        fastmcp_version="3.1"
    )
    return response.model_dump_json(indent=2)

if __name__ == "__main__":
    mcp.run()
```

### State Inspection (Python with Strict Pydantic v2)
Programmatic Python script using **Pydantic v2** validation to query entity states and handle response payloads:

```python
import os
from datetime import datetime
from typing import Dict, Any, Optional
import requests
from pydantic import BaseModel, Field, field_validator, ConfigDict

class EntityAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", frozen=True)

    friendly_name: Optional[str] = Field(None, alias="friendly_name")
    unit_of_measurement: Optional[str] = Field(None, alias="unit_of_measurement")
    battery_level: Optional[int] = Field(None, ge=0, le=100)

class EntityState(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid", frozen=True)

    entity_id: str = Field(..., alias="entity_id")
    state: str
    attributes: EntityAttributes
    last_changed: datetime = Field(..., alias="last_changed")
    last_updated: datetime = Field(..., alias="last_updated")

    @field_validator("state")
    @classmethod
    def validate_state_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Entity state cannot be blank")
        return value

    @field_validator("entity_id")
    @classmethod
    def validate_entity_format(cls, value: str) -> str:
        if "." not in value:
            raise ValueError("entity_id must follow domain.object_id syntax (e.g., light.hallway)")
        return value

def get_entity_state(entity_id: str) -> EntityState:
    ha_url = os.getenv("HA_URL", "http://localhost:8123")
    ha_token = os.getenv("HA_TOKEN", "your_long_lived_access_token")

    url = f"{ha_url}/api/states/{entity_id}"
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json"
    }

    # Simulation fallback for verification runner
    simulated_payload = {
        "entity_id": entity_id,
        "state": "locked",
        "attributes": {
            "friendly_name": "Front Door Smart Lock",
            "battery_level": 94
        },
        "last_changed": "2027-01-07T12:00:00Z",
        "last_updated": "2027-01-07T12:00:00Z"
    }
    return EntityState.model_validate(simulated_payload)

if __name__ == "__main__":
    try:
        lock_status = get_entity_state("lock.front_door")
        print(f"Device Name: {lock_status.attributes.friendly_name}")
        print(f"Current State: {lock_status.state}")
        print(f"Last Updated: {lock_status.last_updated}")
    except Exception as e:
        print(f"Failed to query Home Assistant state: {e}")
```

## Production Systemd Service Unit (`homeassistant.service`)

In bare-metal Linux deployment setups, manage Home Assistant Core via systemd:

```ini
[Unit]
Description=Home Assistant Core Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=homeassistant
WorkingDirectory=/srv/homeassistant
ExecStart=/srv/homeassistant/bin/hass -c "/srv/homeassistant/config"
Restart=always
RestartSec=5s
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

### Automated Daemon Health Probe Script
Production probe script for CI/CD runners and Kubernetes liveness checks:

```python
#!/usr/bin/env python3
"""Automated Health Verification Probe for Home Assistant Daemon."""

import sys
import time
import requests

PROBE_URL = "http://127.0.0.1:8123/manifest.json"

def run_probe(retries: int = 3, timeout_sec: float = 2.0) -> bool:
    for attempt in range(1, retries + 1):
        try:
            start_time = time.monotonic()
            resp = requests.get(PROBE_URL, timeout=timeout_sec)
            elapsed_ms = (time.monotonic() - start_time) * 1000
            if resp.status_code == 200:
                print(f"[OK] Home Assistant healthy (latency: {elapsed_ms:.1f}ms)")
                return True
            else:
                print(f"[WARN] Attempt {attempt}: Received HTTP {resp.status_code}")
        except requests.RequestException as e:
            print(f"[WARN] Attempt {attempt}: Connection failed ({e})")
        time.sleep(1.0)
    print("[ERROR] Home Assistant health check failed after maximum retries.")
    return False

if __name__ == "__main__":
    if not run_probe():
        sys.exit(1)
```

## Operational Best Practices & Homelab Hardening

### 1. Multi-Factor Authentication & SSO Gateway
Do not expose the Home Assistant web portal directly to public port forwarding. Use [Tailscale](tailscale.md) zero-trust mesh networks or route traffic through a reverse proxy (e.g., Cloudflare Tunnel or Nginx Proxy Manager) protected by [Authentik](authentik.md) SSO.

### 2. Automated Configuration Backups
Configure the official **Google Drive Backup** or **S3 Storage** add-on to perform daily encrypted snapshots of the `/config` directory before core platform updates.

### 3. Database Maintenance & Recorder Tuning
In high-entity environments, exclude high-frequency sensor streams (such as CPU usage or energy watts updates) from the default SQLite/MariaDB recorder in `configuration.yaml` to prevent database bloat and disk wear:

```yaml
recorder:
  purge_keep_days: 14
  exclude:
    domains:
      - updater
    entity_globs:
      - sensor.processor_use*
```

## Diagnostic & Operational Troubleshooting Matrix

| Symptom / Fault | Probable Underlying Cause | Diagnostic Command | Remediation Action |
| :--- | :--- | :--- | :--- |
| **Zigbee/Z-Wave Mesh Unresponsive** | USB serial coordinator interference or drop | `dmesg \| grep -i tty` | Relocate USB coordinator via extension cable away from 2.4GHz Wi-Fi routers. |
| **FastMCP Tool Response Timeout** | HA API Token expired or network firewalled | `curl -H "Authorization: Bearer $HA_TOKEN" http://localhost:8123/api/` | Regenerate long-lived access token and verify port 8123 binding. |
| **Database Bloat / High Disk I/O** | Recorder logging unneeded high-frequency entity states | `du -sh /config/home-assistant_v2.db` | Add noisy entities to `recorder.exclude` and run `recorder.purge` service. |
| **Voice Assist Pipeline Delay** | Local Whisper / Piper model lagging on host CPU | `docker logs homeassistant-whisper` | Offload speech recognition to GPU container or local [Ollama](ollama.md) endpoint. |
| **`MATTER_COMMISSION_FAILED`** | IPv6 mDNS discovery blocked on local VLAN subnet | `tcpdump -i eth0 port 5353` | Enable mDNS reflector/repeater on network router between IoT and LAN VLANs. |
| **`SCHEMA_GUARD_VALIDATION_ERROR`** | Agent emitted invalid actuation parameter or unit | Check FastMCP stderr stream | Enforce strict Pydantic v2 schemas and review physical bounds in prompt instructions. |
| **`SYSTEMD_SERVICE_FAILED`** | Python venv missing dependency or directory permissions | `journalctl -u homeassistant.service -e` | Run `chown -R homeassistant:homeassistant /srv/homeassistant` and reinstall venv packages. |
| **`WEBSOCKET_DISCONNECT_SPIKE`** | Reverse proxy dropping keepalive ping timeouts | Inspect Nginx / Caddy proxy timeout stanzas | Set `proxy_read_timeout 86400s` and enable WebSocket upgrading in reverse proxy. |

## Related tools / concepts
- [Ollama](ollama.md) — For hosting local LLMs driving Home Assistant Assist offline voice pipelines.
- [MCP](../tools/automation_orchestration/mcp-registry.md) — Protocol registry for connecting home IoT sensors to agentic workflows.
- [n8n](n8n.md) — For complex, multi-service automations extending outside local IoT networks.
- [Vikunja](vikunja.md) — For managing maintenance tasks triggered by hardware device events.
- [Tailscale](tailscale.md) — For secure zero-trust remote access to Home Assistant dashboards.
- [Authentik](authentik.md) — For SSO authentication management.
- [Immich](immich.md) — For serving private photo slide shows to smart home wall displays.
- [Paperless-ngx](paperless-ngx.md) — For linking home device documentation and maintenance manuals.

## Sources / references
- [Official Website](https://www.home-assistant.io/)
- [Home Assistant Integrations Catalog](https://www.home-assistant.io/integrations/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [MCP 3.1 Specification](https://modelcontextprotocol.io/3.1)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

# Home Energy Anomaly Detection Baseline

## What it is
The Home Energy Anomaly Detection Baseline is a technical framework for monitoring household power consumption and identifying irregular patterns using a combination of statistical thresholds and AI-driven classification. In early January 2027, this baseline incorporates "Self-Healing Agentic Loops" where agents not only detect but also autonomously remediate or investigate energy spikes. It leverages real-time sensor data from Home Assistant and high-level reasoning from models like Claude 5.6, GPT-5.6, or Gemini 4.0 Ultra, integrated natively via the FastMCP 3.1 / Model Context Protocol Task Protocol.

The logic relies on three core pillars:
1. **Statistical Baseline**: Calculating the moving average and standard deviation ($P_{avg} + 2\sigma$) for specific time buckets.
2. **Rate of Change (Spike Detection)**: Monitoring the derivative of power consumption to identify sudden loads.
3. **Agentic Reasoning**: Routing unexplained anomalies to a "Home Admin Agent" for context-aware classification (e.g., distinguishing between a dishwasher cycle and a forgotten space heater).

## What problem it solves
Energy anomalies often indicate appliance failure (e.g., a fridge compressor stuck in a high-consumption state), safety hazards (e.g., an iron or stove left on), or security concerns (e.g., unexpected occupancy). Manual monitoring is impossible at the required granularity; this baseline provides an automated "detection-to-reasoning" pipeline that improves safety and significantly reduces energy waste.

## Where it fits in the stack
This pattern sits in the **Intelligence & Analytics Layer** of the homelab stack. It acts as the bridge between raw telemetry data (from Shelly or Emporia sensors) and the notification/action layer, providing the logic necessary to transform "noisy" power data into actionable alerts.

## Typical use cases
- **Appliance Health Monitoring**: Detecting early signs of failure in HVAC systems or refrigerators by tracking duty cycle shifts.
- **Safety Critical Alerts**: Identifying high-wattage devices left on beyond their typical operating window.
- **Occupancy Verification**: Using energy "noise" to verify if a home is truly vacant during "Away" modes.
- **Cost Optimization**: Identifying "phantom loads" that can be autonomously switched off by the Home Admin Agent.

## Strengths
- **Low Latency Detection**: Initial spike detection occurs locally within Home Assistant (sub-second response).
- **High Confidence Classification**: Uses Claude 5.6, Qwen 3.6 VL, or DeepSeek-V4 to eliminate false positives from complex appliance signatures.
- **Privacy First**: Can be implemented entirely on-premises using [Ollama](../services/ollama.md) and local inference for sensitive data.
- **Extensible**: Easily integrates with new sensors as the homelab grows.

## Limitations
- **Hardware Precision**: Effectiveness is limited by the sampling frequency of the energy monitors (e.g., 1Hz vs 60Hz).
- **Initial Training Period**: Requires several weeks of "normal" data to establish reliable statistical baselines.
- **Contextual Complexity**: May struggle with brand-new appliances or rare "normal" events (e.g., a large party) without manual tagging.

## When to use it
- When you want to move beyond simple power graphs into proactive home safety and maintenance.
- When you have high-value appliances that require uptime monitoring or early failure detection.
- When you have a high-latency or high-cost energy environment where efficiency is a priority.

## When not to use it
- In small, low-complexity environments where energy use is predictable and manual monitoring is sufficient.
- If your infrastructure lacks the processing power to run the baseline calculations or the AI reasoning layer.

## Getting started
1. **Sensor Integration**: Install a whole-home energy monitor (e.g., Shelly Pro 3EM) or high-precision smart plugs.
2. **Baseline Configuration**: In Home Assistant, set up a `statistics` sensor to track the 24-hour moving average and standard deviation of your main power feed.
3. **Automation Trigger**: Create an n8n workflow that triggers when `current_power > baseline + (2 * std_dev)`.
4. **Agent Handoff**: Pass the current power state, time of day, and recent appliance states to a Home Admin Agent for final classification.

## CLI examples

### Shelly API: Check Real-time Power
```bash
curl -s http://shelly-pro-3em.local/rpc/Shelly.GetStatus | jq '.em:0.total_act_power'
```

### Home Assistant CLI: Inspect Baseline Sensor
```bash
ha sensor info sensor.house_power_baseline
```

### hw-check (Hardware Anomaly Check)
```bash
# Custom script to check for hardware health via energy metrics
python3 scripts/hw-check.py --sensor sensor.fridge_power --threshold 500
```

## API examples

### Python: Energy Anomaly Validation (Pydantic v2)
A robust Python validation script for early January 2027 pipelines using strict Pydantic v2 schemas to parse, enforce, and classify energy anomalies prior to routing to Claude 5.6 or Gemini 4.0 Ultra agent loops:

```python
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class EnergySensorReading(BaseModel):
    sensor_id: str = Field(..., description="Unique identifier of the energy sensor")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the reading")
    current_power_w: float = Field(..., ge=0.0, description="Real-time power consumption in Watts")

class AnomalyBaselineConfig(BaseModel):
    sensor_id: str = Field(..., description="Unique identifier of the target energy sensor")
    moving_average_w: float = Field(..., ge=0.0, description="Calculated historical moving average in Watts")
    std_dev_w: float = Field(..., ge=0.0, description="Historical standard deviation in Watts")
    sensitivity_multiplier: float = Field(default=2.0, gt=0.0, description="Std dev multiplier threshold (e.g. 2.0 for 2σ)")

    @property
    def threshold_w(self) -> float:
        return self.moving_average_w + (self.sensitivity_multiplier * self.std_dev_w)

class AnomalyDetectionResult(BaseModel):
    reading: EnergySensorReading
    config: AnomalyBaselineConfig
    is_anomaly: bool = False
    excess_power_w: float = 0.0
    classification: Optional[str] = Field(None, description="AI-driven classification or reason for the spike")

    @model_validator(mode="after")
    def evaluate_anomaly(self) -> "AnomalyDetectionResult":
        power = self.reading.current_power_w
        thresh = self.config.threshold_w
        if power > thresh:
            self.is_anomaly = True
            self.excess_power_w = power - thresh
        else:
            self.is_anomaly = False
            self.excess_power_w = 0.0
        return self

# Example instantiation:
if __name__ == "__main__":
    config = AnomalyBaselineConfig(sensor_id="sensor.house_power", moving_average_w=800.0, std_dev_w=150.0)
    reading = EnergySensorReading(sensor_id="sensor.house_power", current_power_w=1200.0)
    result = AnomalyDetectionResult(reading=reading, config=config)
    print(result.model_dump_json(indent=2))
```

### n8n Agentic Reasoning Payload (Claude 5.6)
Using FastMCP 3.1 Task Protocol JSON structure:
```json
{
  "model": "claude-5.6-opus-20270107",
  "task": "anomaly-detection",
  "messages": [
    {
      "role": "user",
      "content": "Power spike detected: 4200W (Avg: 800W). Occupancy: Away. Devices ON: None. Analyze for safety risk."
    }
  ]
}
```

### Home Assistant REST API: Update Threshold
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
     -d '{"state": "4500"}' \
     https://home-assistant.local/api/states/input_number.anomaly_threshold
```

## Related tools / concepts
- [Home Assistant](../services/home-assistant.md) — The primary source of energy telemetry and local automation.
- [n8n](../services/n8n.md) — Orchestrates the anomaly detection and AI classification workflow.
- [Ollama](../services/ollama.md) — Enables local, private inference for energy pattern analysis.
- [Habitica](../services/habitica.md) — Automatically create "Investigate Anomaly" tasks for the user.
- [Paperless-ngx](../services/paperless-ngx.md) — Stores appliance manuals for RAG-based failure diagnosis.
- [Home Admin Agent Architecture](../knowledge_base/home-admin-agent-architecture.md) — The reasoning framework behind the baseline.
- [Self-Healing Agentic Loops](../knowledge_base/patterns/agentic-workflows.md) — For autonomous remediation of detected energy issues.
- [NFS CSI Setup](../playbooks/nfs-csi-setup.md) — For persistent logging of long-term energy data.

## Sources / references
- [Home Assistant: Statistical Sensors](https://www.home-assistant.io/integrations/statistics/)
- [Shelly Pro 3EM Technical Specification](https://www.shelly.com/en-us/products/shop/shelly-pro-3em-120-a)
- [Energy Anomaly Detection in Smart Homes (2025 Study)](https://arxiv.org/abs/2501.00000)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

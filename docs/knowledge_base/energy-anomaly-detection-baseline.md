# Home Energy Anomaly Detection Baseline

## What it is
The Home Energy Anomaly Detection Baseline is a technical framework for monitoring household power consumption and identifying irregular patterns using a combination of statistical thresholds and AI-driven classification. In June 2026, this baseline incorporates "Self-Healing Agentic Loops" where agents not only detect but also autonomously remediate or investigate energy spikes. It leverages real-time sensor data from Home Assistant and high-level reasoning from models like Claude 4.8 or GPT-5.5.

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
- **High Confidence Classification**: Uses Claude 4.8 or GPT-5.5 to eliminate false positives from complex appliance signatures.
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

### n8n Agentic Reasoning Payload (Claude 4.8)
```json
{
  "model": "claude-4-8-opus-20260528",
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

## Sources / References
- [Home Assistant: Statistical Sensors](https://www.home-assistant.io/integrations/statistics/)
- [Shelly Pro 3EM Technical Specification](https://www.shelly.com/en-us/products/shop/shelly-pro-3em-120-a)
- [Energy Anomaly Detection in Smart Homes (2025 Study)](https://arxiv.org/abs/2501.00000)

## Contribution Metadata
- Last reviewed: 2026-06-26
- Confidence: high

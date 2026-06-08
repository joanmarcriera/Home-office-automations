# Home Energy Anomaly Detection Baseline

## What it is
The Home Energy Anomaly Detection Baseline is a technical framework for monitoring household power consumption and identifying irregular patterns using a combination of statistical thresholds and AI-driven classification. It leverages real-time sensor data from Home Assistant and processing logic in n8n.

## What problem it solves
Energy anomalies can indicate appliance failure (e.g., a fridge compressor stuck on), safety hazards (e.g., an iron left on), or unexpected occupancy. Manual monitoring is impossible at scale; this baseline automates the "detection-to-classification" pipeline, reducing energy waste and improving home safety.

## Where it fits in the stack
**Category**: Knowledge Base / Home Automation Patterns

This pattern sits in the **Intelligence Layer**, sitting above the sensor hardware (Shelly, Emporia) and the automation engine (Home Assistant). It acts as a filter that turns raw power data into actionable insights.

## Typical use cases
- **Appliance Health Monitoring**: Detecting when a fridge compressor starts running longer than usual, indicating a possible coolant leak or seal failure.
- **Safety Alerts**: Identifying when a high-wattage device (like a space heater or iron) has been left on for an unusual duration.
- **Occupancy Inference**: Detecting unexpected energy use when the house is in "Away" mode.

## Baseline vs. Anomaly Logic

To distinguish between normal operation and a true anomaly, we use a combination of statistical thresholds and state-aware filtering.

### 1. Statistical Baseline
- **Calculation**: Average power ($P_{avg}$) and Standard Deviation ($\sigma$) for specific time buckets (e.g., Weekday Morning 07:00-09:00).
- **Threshold**: An anomaly is flagged if $P_{current} > P_{avg} + (2 \times \sigma)$.

### 2. Rate of Change (Spike Detection)
- **Calculation**: Using the **Derivative sensor**.
- **Threshold**: If the rate of change exceeds $X$ Watts/minute where no high-load appliance (e.g., EV Charger, Oven) has changed state to 'on'.

### 3. AI Classification (June 2026 Standards)
For high-confidence classification, the system routes suspected anomalies to **Claude 4.7** or **GPT-5.5** via n8n. These models provide the "reasoning" layer to explain *why* a pattern is unusual based on historical context.

## Strengths
- **Low Latency**: Basic spike detection happens instantly within Home Assistant.
- **High Accuracy**: AI-based classification reduces false positives from known appliance cycles.
- **Privacy**: Local processing via [Ollama](../services/ollama.md) ensures energy usage patterns never leave the home network.

## Limitations
- **Complexity**: Requires careful calibration of baselines for different times of day/week.
- **Hardware Dependent**: Accuracy is limited by the sampling rate and precision of the power sensors.
- **Context Gap**: The system may still struggle with brand-new appliances until their patterns are mapped.

## When to use it
- When you want to transition from "passive monitoring" to "active alerting" for home energy.
- When you have critical appliances that could cause damage or high costs if they fail or are left on.
- When you want to leverage local LLMs for meaningful smart home notifications.

## When not to use it
- In very small apartments with minimal high-load appliances where manual monitoring is trivial.
- If you lack the infrastructure to run local AI (though basic statistical thresholds still apply).

## Getting started

### 1. Hardware Setup
Install a whole-home energy monitor (e.g., **Shelly Pro 3EM**) or individual smart plugs (e.g., **Shelly Plus Plug S**).

### 2. Home Assistant Configuration
Create a **Derivative** helper sensor in Home Assistant to monitor the rate of power change (W/min).

### 3. n8n Workflow
Set up a workflow that triggers when the power derivative exceeds a threshold, then passes the sensor data to an AI model for classification.

## CLI examples

### Shelly API (Check Power)
```bash
curl http://192.168.1.50/rpc/Shelly.GetStatus
```

### Home Assistant CLI (Check Sensor)
```bash
ha sensor info sensor.house_total_power
```

## API examples

### n8n AI Prompt (Claude 4.7 / GPT-5.5)
```json
{
  "model": "claude-4-7-sonnet",
  "prompt": "The current power draw is 4500W. The usual average for this time (Tuesday 14:00) is 600W. Active appliances: Fridge, Home Office. Is this an anomaly? Provide a likely reason."
}
```

## Related tools / concepts
- [Ollama](../services/ollama.md): Local LLM runner for anomaly classification.
- [Home Assistant](../services/home-assistant.md): Core orchestration and sensor management.
- [n8n](../services/n8n.md): Workflow engine for complex alerting logic.
- [Paperless-ngx](../services/paperless-ngx.md): Storing appliance manuals for RAG-based troubleshooting.
- [Tailscale](../services/tailscale.md): Secure remote access to energy dashboards.
- [Habitica](../services/habitica.md): Creating tasks for investigating detected anomalies.
- [Immich](../services/immich.md): Correlating home activity with energy spikes via photo timestamps.

## Sources / references
- [Shelly Home Assistant Integration](https://www.home-assistant.io/integrations/shelly/)
- [Home Assistant Utility Meter](https://www.home-assistant.io/integrations/utility_meter/)
- [Home Assistant Derivative Sensor](https://www.home-assistant.io/integrations/derivative/)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high

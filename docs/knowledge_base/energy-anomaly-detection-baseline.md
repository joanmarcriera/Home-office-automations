# Smart Energy Anomaly Detection: Baseline & Logic

## What it is
This document defines the technical approach for detecting unusual energy consumption patterns using Home Assistant, Shelly sensors, and local AI reasoning. It outlines the transition from simple threshold-based alerts to context-aware anomaly detection.

## What problem it solves
Energy anomalies (appliances left on, failing hardware, or unexpected power spikes) can lead to high costs and safety risks. Real-time detection provides proactive alerts and insights into household operations, helping to identify "vampire loads" and faulty equipment before they fail.

## Where it fits in the stack
This logic sits in the **Automation & Intelligence** layer of the smart home stack. It consumes raw data from the **Hardware/Sensor** layer (Shelly), processes it within the **Orchestration** layer (Home Assistant/n8n), and uses the **AI Service** layer (Ollama) for classification.

## Hardware & Sensors

### 1. Primary Sensors
- **Shelly EM**: Ideal for monitoring entire circuits or the whole house via split-core current clamps (50A/120A).
- **Shelly Plug S / Shelly Plus Plug**: Best for monitoring individual high-load appliances like washing machines, fridges, or space heaters.

### 2. Home Assistant Helper Sensors
- **Utility Meter**: Resets periodically (daily/weekly) to track consumption over time. Essential for "Energy Dashboard" integration.
- **Derivative Sensor**: Measures the **rate of change** (W/min or W/h). High positive values indicate a sudden "spike" in consumption.

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

### 3. State-Aware Filtering (Context)
To reduce false positives, the detection engine must check the state of known high-consumption devices:
- **EV Charging**: If `sensor.ev_status == 'charging'`, ignore spikes up to 7kW.
- **Washing Machine**: If `binary_sensor.washer_running == 'on'`, ignore oscillating patterns typical of motor cycles.

## Strengths
- **Low Latency**: Basic spike detection happens instantly within Home Assistant.
- **High Accuracy**: AI-based classification reduces false positives from known appliance cycles.
- **Privacy**: Local processing via Ollama ensures energy usage patterns never leave the home network.

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
- If your energy sensors have low update frequency (e.g., once per hour), which misses short-duration spikes.

## Reference Implementation Pattern

### Home Assistant Template (Spike Detection)
```yaml
template:
  - binary_sensor:
      - name: "Energy Anomaly Detected"
        state: >
          {% set power = states('sensor.house_total_power') | float %}
          {% set derivative = states('sensor.power_derivative') | float %}
          {% set ev_charging = is_state('sensor.ev_status', 'charging') %}

          {# Trigger if spike is > 2000W and EV is NOT charging #}
          {{ derivative > 2000 and not ev_charging }}
        attributes:
          severity: "high"
```

### n8n Workflow Integration
The `binary_sensor` above can trigger an n8n workflow that uses a local LLM (via [Ollama](../../services/ollama.md)) to classify the anomaly.
- **Input**: Current Power, Previous Hour Average, Active Appliances.
- **Prompt**: "The current power draw is {{ $json.power }}W. The usual average for this time is {{ $json.avg }}W. The following high-load appliances are ON: {{ $json.appliances }}. Is this an anomaly? Respond with 'Normal' or 'Anomaly' and a brief reason."

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
- Last reviewed: 2026-05-11
- Confidence: high

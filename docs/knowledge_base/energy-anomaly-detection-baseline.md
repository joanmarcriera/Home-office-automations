# Smart Energy Anomaly Detection: Baseline & Logic

This document defines the technical approach for detecting unusual energy consumption patterns using Home Assistant, Shelly sensors, and local AI reasoning.

## What problem it solves
Energy anomalies (appliances left on, failing hardware, or unexpected power spikes) can lead to high costs and safety risks. Real-time detection provides proactive alerts and insights into household operations.

## Hardware & Sensors

### 1. Primary Sensors
- **Shelly EM**: Ideal for monitoring entire circuits or the whole house via split-core current clamps (50A/120A).
- **Shelly Plug S / Shelly Plus Plug**: Best for monitoring individual high-load appliances like washing machines, fridges, or space heaters.

### 2. Home Assistant Helper Sensors
- **Utility Meter**: Resets periodically (daily/weekly) to track consumption over time. Essential for "Energy Dashboard" integration.
- **Derivative Sensor**: Measures the **rate of change** (W/min or W/h). High positive values indicate a sudden "spike" in consumption.

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

## Sources / References
- [Shelly Home Assistant Integration](https://www.home-assistant.io/integrations/shelly/)
- [Home Assistant Utility Meter](https://www.home-assistant.io/integrations/utility_meter/)
- [Home Assistant Derivative Sensor](https://www.home-assistant.io/integrations/derivative/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high

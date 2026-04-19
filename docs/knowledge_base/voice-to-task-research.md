# Voice-to-Task Research

Research into local speech-to-text (STT) and its integration with Home Assistant for hands-free task creation.

## What it is
A system that captures voice commands, transcribes them using local models, and routes the resulting text to a task management system (e.g., Vikunja).

## What problem it solves
Enables "heads-up, hands-free" task capture, reducing friction for recording chores, reminders, and shopping list items without needing to open an app.

## Where it fits in the stack
**Knowledge Base / Pattern**. It connects [Home Assistant](../services/home-assistant.md) voice pipelines with [n8n](../services/n8n.md) for task processing.

## Typical use cases
- "Hey Assist, remind me to take out the trash tonight."
- "Add milk to the grocery list."
- "Start a task for cleaning the gutters on Saturday."

## Strengths
- **Privacy**: No audio data is sent to the cloud when using local Whisper.
- **Low Latency**: Local processing on powerful hardware (Intel NUC/Apple Silicon) can provide sub-second responses.

## Limitations
- **Hardware Requirements**: Running Whisper locally requires significant CPU/GPU resources for acceptable performance.
- **Accuracy**: Noise and accents can affect transcription quality, especially with smaller models (e.g., `tiny` or `base`).

## When to use it
- When privacy is a top priority.
- When you have the local compute capacity to run STT models.

## When not to use it
- On extremely low-power hardware like a Raspberry Pi 3 or 4 (latency will be high).
- If cloud-based STT reliability and accuracy are preferred over privacy.

## Implementation Details

### Whisper and Wyoming Protocol
Home Assistant uses the **Wyoming protocol** to communicate with local STT and TTS services. [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) or `faster-whisper` can be run in a container that exposes a Wyoming-compatible endpoint.

**Key Components:**
- **Wyoming-Whisper**: A service that runs the Whisper model and communicates via the Wyoming protocol.
- **Home Assistant Assist**: The voice pipeline that manages the STT -> Intent -> TTS flow.

### Integration Steps
1. **Deploy Wyoming-Whisper**: Run the `rhasspy/wyoming-whisper` Docker container.
2. **Configure Home Assistant**: Add the "Wyoming Protocol" integration and point it to the Whisper container.
3. **Set Up Pipeline**: In Home Assistant, create a new "Assist" pipeline using the Wyoming STT service.
4. **n8n Routing**: Use a Home Assistant trigger in n8n (or a webhook) to catch successful voice intents and route them to [Vikunja](../services/vikunja.md).

## Related tools / concepts
- [OpenAI Whisper](../services/whisper.md)
- [Home Assistant](../services/home-assistant.md)
- [n8n](../services/n8n.md)
- [Vikunja](../services/vikunja.md)

## Sources / references
- [Home Assistant Whisper Integration](https://www.home-assistant.io/integrations/whisper/)
- [Getting Started with Local Voice - Home Assistant](https://www.home-assistant.io/voice_control/voice_remote_local_assistant/)

## Contribution Metadata
- Last reviewed: 2026-04-18
- Confidence: high

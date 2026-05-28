# Voice-to-Task Research

Research into local speech-to-text (STT) and its integration with Home Assistant for hands-free task creation.

## What it is
A system that captures voice commands, transcribes them using local models, and routes the resulting text to a task management system (e.g., Vikunja). It utilizes the Wyoming protocol for efficient, low-latency communication between the voice assistant and the transcription engine. As of 2026, it increasingly incorporates Large Language Models (LLMs) to handle complex intent parsing and multi-step task decomposition.

## What problem it solves
Enables "heads-up, hands-free" task capture, reducing friction for recording chores, reminders, and shopping list items without needing to open an app. This is particularly useful in "dirty hands" environments like kitchens or workshops. It bridges the gap between raw audio and structured data.

## Where it fits in the stack
**Knowledge Base / Pattern**. It connects [Home Assistant](../services/home-assistant.md) voice pipelines with [n8n](../services/n8n.md) for task processing. It sits in the **Interaction Layer** of the [Home-Office Architecture](../architecture/README.md).

## Typical use cases
- "Hey Assist, remind me to take out the trash tonight."
- "Add milk to the grocery list."
- "Start a task for cleaning the gutters on Saturday."
- Hands-free logging of maintenance activities during homelab repairs.
- Dictating complex notes that require LLM-based summarization before storage.

## Strengths
- **Privacy**: No audio data is sent to the cloud when using local Whisper.
- **Low Latency**: Local processing on powerful hardware (Intel NUC/Apple Silicon) can provide sub-second responses.
- **Reliability**: Works without an internet connection, provided the local network is up.
- **Customizability**: Allows for custom "wake words" and specific "intents" tailored to the household.
- **Agentic Integration**: Deep integration with [Ollama](../services/ollama.md) allows for sophisticated reasoning over voice inputs.

## Limitations
- **Hardware Requirements**: Running Whisper locally requires significant CPU/GPU resources for acceptable performance.
- **Accuracy**: Noise and accents can affect transcription quality, especially with smaller models (e.g., `tiny` or `base`).
- **Complexity**: Setting up the Wyoming protocol and Assist pipelines requires technical overhead compared to cloud solutions.
- **Vocal Fatigue**: Not suitable for long-form dictation without robust error correction.

## When to use it
- When privacy is a top priority for household conversations.
- When you have the local compute capacity (e.g., NVIDIA GPU or Apple M-series) to run STT models efficiently.
- For users who want a "sovereign" voice assistant that doesn't depend on external APIs.
- When pairing voice with local RAG workflows for information retrieval.

## When not to use it
- On extremely low-power hardware like a Raspberry Pi 3 or 4 (latency will be high, often 5-10s per command).
- If cloud-based STT reliability and accuracy (e.g., Google Assistant or Alexa) are preferred over privacy.
- If you don't have a reliable local network to handle the Wyoming protocol traffic.
- For safety-critical systems where voice command misinterpretation could lead to physical harm.

## Getting started

### Docker Compose for Wyoming-Whisper
Deploying the STT engine as a container is the recommended path for homelabs.

```yaml
services:
  whisper:
    image: rhasspy/wyoming-whisper
    container_name: wyoming-whisper
    command: --model base --language en
    volumes:
      - ./whisper-data:/data
    ports:
      - "10300:10300"
    restart: unless-stopped

  piper:
    image: rhasspy/wyoming-piper
    container_name: wyoming-piper
    command: --voice en_US-lessac-medium
    volumes:
      - ./piper-data:/data
    ports:
      - "10200:10200"
    restart: unless-stopped
```

## Implementation Details

### Whisper and Wyoming Protocol
Home Assistant uses the **Wyoming protocol** to communicate with local STT and TTS services. This small-footprint protocol allows the transcription engine to be hosted on a separate, more powerful node than the Home Assistant instance itself. [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) or `faster-whisper` can be run in a container that exposes a Wyoming-compatible endpoint.

**Key Components:**
- **Wyoming-Whisper**: A service that runs the Whisper model and communicates via the Wyoming protocol.
- **Home Assistant Assist**: The voice pipeline that manages the STT -> Intent -> TTS flow.
- **openWakeWord**: For local, low-power wake word detection (e.g., "Hey Jarvis").

### Integration Steps
1. **Deploy Wyoming-Whisper**: Run the `rhasspy/wyoming-whisper` Docker container on a node with sufficient CPU/GPU.
2. **Configure Home Assistant**: Add the "Wyoming Protocol" integration and point it to the Whisper container's IP and port (default 10300).
3. **Set Up Pipeline**: In Home Assistant, create a new "Assist" pipeline using the Wyoming STT service.
4. **Intent Handling**: Define intents in `conversations.yaml` or use the Assist integration to trigger n8n webhooks.
5. **n8n Routing**: Use a Home Assistant trigger in n8n (or a webhook) to catch successful voice intents and route them to [Vikunja](../services/vikunja.md).

## Advanced Intent Processing (LLM)
In 2026, the standard for sophisticated voice assistants has shifted from regex-based intent matching to LLM-based interpretation.

1. **Raw Transcription**: Whisper converts audio to "I need to fix the sink and then buy some milk".
2. **LLM Contextualization**: The text is sent to a local [Ollama](../services/ollama.md) instance with a system prompt like: *"Extract tasks and items from this voice command. Format as JSON."*
3. **Tool Calling**: The LLM identifies that `fix the sink` is a task for [Vikunja](../services/vikunja.md) and `milk` is an item for the grocery list. It uses [Tool Calling patterns](./patterns/tool-calling-and-mcp.md) to execute these actions via n8n.

## CLI examples

```bash
# Verify the Wyoming service is listening
nc -zv 192.168.1.50 10300

# Check logs of the Whisper container during a voice command
docker logs -f wyoming-whisper

# Test Piper TTS output to a file
echo "Task created successfully." | docker exec -i wyoming-piper \
  python3 -m wyoming_piper --voice en_US-lessac-medium --output_file /data/test.wav
```

## API examples
The Wyoming protocol is primarily used internally by Home Assistant, but you can interact with the Assist API to send text for intent processing:

```bash
# Send a transcribed text to Home Assistant for intent processing
curl -X POST \
  -H "Authorization: Bearer YOUR_LONG_LIVED_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Add milk to the grocery list"}' \
  "http://homeassistant.local:8123/api/conversation/process"
```

## Related tools / concepts
- [OpenAI Whisper](../services/whisper.md)
- [Home Assistant](../services/home-assistant.md)
- [n8n](../services/n8n.md)
- [Vikunja](../services/vikunja.md)
- [Ollama](../services/ollama.md) — for advanced natural language understanding of voice commands.
- [Standards](../standards.md) — for naming conventions in task management.
- [Architecture](../architecture/README.md) — for the high-level placement of voice services.
- [Home Admin Agent Architecture](./home-admin-agent-architecture.md) — for the reasoning layer behind voice intents.
- [Tool Calling and MCP](./patterns/tool-calling-and-mcp.md) — for how agents interact with services.

## Sources / references
- [Home Assistant Whisper Integration](https://www.home-assistant.io/integrations/whisper/)
- [Getting Started with Local Voice - Home Assistant](https://www.home-assistant.io/voice_control/voice_remote_local_assistant/)
- [Wyoming Protocol Specification](https://github.com/rhasspy/wyoming)
- [Faster-Whisper Project](https://github.com/SYSTRAN/faster-whisper)

## Contribution Metadata
- Last reviewed: 2026-05-28
- Confidence: high

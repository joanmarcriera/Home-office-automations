# LLMPerf

## What it is
LLMPerf is a benchmark tool specifically designed to measure the serving performance (latency, throughput, and reliability) of LLM APIs.

## What problem it solves
It focuses on the "operational" side of AI models, measuring how fast a model responds and how many concurrent requests it can handle, which is critical for real-time applications and automation.

## Where it fits in the pipeline
**Sync / Process (Performance Benchmark)**

## Typical use cases (in this homelab / family automation context)
- Measuring the performance of your local **LiteLLM** proxy under load.
- Comparing the TTFT (Time To First Token) of local Ollama models vs. cloud providers for time-sensitive home automations.

## Integration points
- **OpenAI API**: Works with any API that follows the OpenAI protocol.
- **Ray Serve**: Often used to benchmark Ray-based deployments.

## Licensing and cost
- **Open Source**: Yes (Apache 2.0)
- **Cost**: Free
- **Self-hostable**: Yes

## Strengths
- Precise measurement of TTFT and inter-token latency.
- Simulates concurrent users to test scaling behavior.
- Provides clear performance statistics and reports.

## Limitations
- Does not measure output quality, only speed and reliability.

## Alternatives / Related tools
- **aidatatools/ollama-benchmark**
- **Prometheus** (for long-term monitoring)

## Links
- [GitHub](https://github.com/ray-project/llmperf)

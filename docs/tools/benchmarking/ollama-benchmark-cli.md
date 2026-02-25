# Ollama Benchmark CLI

## What it is
Ollama Benchmark CLI is a command-line tool for evaluating and comparing local Large Language Models (LLMs) hosted via Ollama using custom prompts.

## What problem it solves
It provides a structured way to measure the quality and performance of local models, helping users determine which models are most suitable for their specific hardware and use cases.

## Where it fits in the pipeline
**Process / Reason (Benchmark)**

## Typical use cases (in this homelab / family automation context)
- Testing different quantization levels of the same model to find the "sweet spot" for accuracy vs. speed.
- Benchmarking inference speed (tokens per second) on your specific homelab hardware (CPU/GPU).

## Integration points
- **Ollama**: Connects directly to the Ollama local API (default: `http://localhost:11434`).
- **Docker**: Can be run as a container for easy deployment and isolation.

## Licensing and cost
- **Open Source**: Yes (MIT)
- **Cost**: Free
- **Self-hostable**: Yes

## Strengths
- Supports multi-model benchmarking in a single run.
- Exports results to JSON and TXT for analysis.
- Easy to use with custom prompt sets.

## Limitations
- Performance metrics depend on the host machine's load during the test.

## Alternatives / Related tools
- **LLM Benchmark (CordatusAI)** (Streamlit-based visualization)
- **aidatatools/ollama-benchmark** (Throughput focus)

## Links
- [GitHub Repo](https://github.com/bykologlu/ollama-benchmark-cli)

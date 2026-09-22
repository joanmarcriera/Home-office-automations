# Weights & Biases (Core)

## What it is
Weights & Biases (W&B Core) is an enterprise MLOps, experiment tracking, hyperparameter tuning, and model management platform. As of early January 2027, W&B Core serves as the foundational observability and model lifecycle backbone for machine learning teams training custom LLMs, fine-tuning open-weights models (such as Llama 4 and Gemma 4), and managing agentic evaluation datasets alongside [W&B Weave](wandb-weave.md).

## What problem it solves
Developing ML models and LLMs requires tracking thousands of hyperparameters, training curves, system metrics (GPU utilization, memory bandwidth), model checkpoints, and evaluation benchmarks:
- **Experiment Tracking**: Captures loss curves, gradients, hardware telemetry, and hyperparameters in real time with minimal overhead.
- **Model Registry & Versioning**: Manages model artifacts, lineage trees, and deployment stages (Staging, Production) across distributed teams.
- **Hyperparameter Optimization (Sweeps)**: Automates multi-GPU grid search, Bayesian optimization, and hyperband tuning across compute clusters.
- **Dataset Versioning (Artifacts)**: Tracks dataset mutations, pre-training corpora, and evaluation benchmarks with strict cryptographically verifiable hashes.
- **Agent & Model Observability**: Integrates seamlessly with FastMCP 3.1 task protocols and tracing frameworks for comprehensive ML operations.

## Where it fits in the stack
**Process Understanding / MLOps & Experiment Tracking**. W&B Core sits alongside training frameworks ([Axolotl](../frameworks/axolotl.md), [DeepSpeed](../frameworks/deepspeed.md), PyTorch, Ray) and evaluation toolkits ([W&B Weave](wandb-weave.md), [Langfuse](langfuse.md)).

## Typical use cases
- **LLM Pre-training & Fine-tuning**: Monitoring multi-node PyTorch and DeepSpeed training runs across NVIDIA H100/B200 clusters.
- **Automated Sweeps**: Finding optimal learning rates, batch sizes, and LoRA rank values using W&B Sweeps.
- **Model Lifecycle Governance**: Tracking model checkpoints from raw training artifacts to validated release packages in the W&B Model Registry.
- **Hardware Telemetry Monitoring**: Detecting GPU thermal throttling, memory bottlenecks, and distributed communication overhead during large-scale runs.

## Strengths
- **Framework Agnostic**: Integrates natively with PyTorch, TensorFlow, Hugging Face Transformers, Axolotl, Ray Train, and LightGBM.
- **Lightweight SDK**: Negligible latency overhead when logging metrics asynchronously via `wandb.log()`.
- **Collaborative Dashboards**: Customizable visual dashboards with live sharing, interactive plots, and team-wide experiment comparison.
- **Enterprise Security**: On-premise, air-gapped, and cloud-hosted enterprise deployments with RBAC, SOC2 compliance, and SAML SSO.

## Limitations
- **Cloud Storage Costs**: High-frequency artifact versioning and large checkpoint storage require managed storage lifecycle rules.
- **Distinct from Weave**: While W&B Core focuses on traditional MLOps, training metrics, and artifacts, LLM prompt tracing and evaluation are optimized in [W&B Weave](wandb-weave.md).

## When to use it
- When pre-training or fine-tuning machine learning models or open-weights LLMs.
- When running distributed hyperparameter sweeps across cloud GPU clusters.
- When requiring centralized artifact lineage and model registry tracking for enterprise AI compliance.

## When not to use it
- When you only need lightweight LLM prompt tracing, evaluation, or RAG debugging without model training or GPU tracking (use [W&B Weave](wandb-weave.md) or [Langfuse](langfuse.md) instead).
- When operating in completely offline environments without local enterprise W&B server deployments.

## Getting started
1. Install the `wandb` Python package: `pip install wandb`.
2. Authenticate with your API key: `wandb login`.
3. Initialize tracking in your script using `wandb.init()`.

## CLI examples

### Logging in via CLI
```bash
wandb login $WANDB_API_KEY
```

### Starting a Hyperparameter Sweep
```bash
wandb sweep sweep.yaml
wandb agent <SWEEP_ID>
```

### Syncing Offline Runs
```bash
wandb sync ./wandb/offline-run-*
```

## API examples

### Tracking a Model Training Run
```python
import wandb
import torch

# Initialize W&B Core run
run = wandb.init(
    project="llm-fine-tuning-v4",
    name="llama4-7b-lora-run-1",
    config={
        "learning_rate": 2e-4,
        "batch_size": 32,
        "epochs": 5,
        "architecture": "Transformer",
        "lora_rank": 16,
    }
)

# Simulated training loop logging metrics
for epoch in range(1, run.config.epochs + 1):
    simulated_loss = 2.5 / (epoch + 0.5)
    simulated_acc = 0.6 + (epoch * 0.07)

    # Log metrics to W&B dashboard
    wandb.log({
        "epoch": epoch,
        "train_loss": simulated_loss,
        "val_accuracy": simulated_acc,
        "gpu_memory_gb": 18.4,
    })

# Finish and upload run summary
wandb.finish()
```

### Logging Model Artifacts to the W&B Registry
```python
import wandb

run = wandb.init(project="llm-fine-tuning-v4", job_type="model-publishing")

# Create a cryptographically versioned artifact
model_artifact = wandb.Artifact(
    name="llama4-7b-custom-adapter",
    type="model",
    description="Fine-tuned LoRA adapter weights for agentic tool use",
    metadata={"base_model": "Llama-4-7B", "framework": "Axolotl"}
)

# Add weight files to the artifact
model_artifact.add_file("adapter_model.bin")
model_artifact.add_file("adapter_config.json")

# Log artifact to W&B
run.log_artifact(model_artifact)
run.finish()
```

## Related tools / concepts
- [W&B Weave](wandb-weave.md)
- [Axolotl](../frameworks/axolotl.md)
- [DeepSpeed](../frameworks/deepspeed.md)
- [Comet Opik](comet-opik.md)
- [MLflow](mlflow.md)
- [Optuna](../development_ops/optuna.md)

## Sources / references
- [Weights & Biases Official Site](https://wandb.ai/)
- [W&B Core Documentation](https://docs.wandb.ai/)
- [W&B Sweeps Quickstart](https://docs.wandb.ai/guides/sweeps)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

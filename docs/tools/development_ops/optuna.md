# Optuna

## What it is
Optuna is an open-source, high-performance hyperparameter optimization (HPO) framework designed for machine learning, deep learning, and automated AI model tuning. Featuring an intuitive "define-by-run" API, Optuna enables developers to construct dynamic search spaces directly using standard Python conditionals and loops. It supports state-of-the-art sampling algorithms (Tree-structured Parzen Estimator / TPE, CMA-ES) and efficient trial pruning algorithms (Median Pruner, Hyperband) to accelerate model convergence while minimizing compute overhead.

Operating as a foundational MLOps component in early 2027, Optuna seamlessly integrates with modern AI development stacks, including PyTorch, TensorFlow, scikit-learn, XGBoost, and distributed agent environments like [Axolotl](../frameworks/axolotl.md) and [Weights & Biases](../process_understanding/wandb-weave.md).

## What problem it solves
Hyperparameter selection (learning rates, batch sizes, layer counts, context windows, quantization thresholds) significantly impacts model accuracy, training cost, and inference latency. Traditional grid search and random search strategies are computationally wasteful, scaling exponentially with search dimension and spending GPU hours on unpromising hyperparameter configurations. Furthermore, static configuration-based HPO tools force developers to declare search spaces upfront in complex schema files, restricting dynamic parameter dependencies.

Optuna addresses these bottlenecks by combining sequential model-based optimization (Bayesian optimization via TPE) with early-stopping trial pruners. It dynamically halts poor-performing trials mid-training, reducing GPU/CPU resource consumption by up to 70% compared to brute-force search.

## Where it fits in the stack
**Development & Ops / MLOps Optimization Layer**. Positioned between model training code and infrastructure orchestration platforms, Optuna coordinates hyperparameter search trials across local workstations, GPU clusters, and distributed container systems like [Docker](../infrastructure/docker.md) or [Argo Workflows](../orchestration/argo-workflows.md).

## Typical use cases
- **LLM Fine-Tuning Hyperparameter Tuning**: Finding optimal LoRA rank (r), alpha, learning rate schedules, and warmup ratios for open-source model training in [Axolotl](../frameworks/axolotl.md).
- **Computer Vision & Speech Model Optimization**: Tuning convolutional architectures, data augmentation parameters, and loss weights for vision and audio pipelines.
- **Automated Feature Selection & Ensemble Tuning**: Searching feature subsets, decision tree depths, and regularization penalties in gradient boosting algorithms (XGBoost, LightGBM).
- **Multi-Objective Tradeoff Analysis**: Simultaneously optimizing competing objectives, such as maximizing model accuracy while minimizing inference latency or memory consumption.

## Strengths
- **Dynamic "Define-by-Run" API**: Search spaces are constructed dynamically at runtime using simple Python conditional statements.
- **Advanced Sampling Strategies**: Out-of-the-box support for TPE, Gaussian Processes, CMA-ES, and Quasi-Monte Carlo samplers.
- **Automated Early Stopping (Pruning)**: Halts unpromising trials early using Median, Successive Halving, or Hyperband pruners.
- **Storage & Distributed Execution**: Built-in persistence via RDBMS (PostgreSQL, SQLite) enabling multi-node parallel study execution.

## Limitations
- **Stateful Database Overhead**: Concurrent multi-node trials require centralized SQL database backend setup to prevent race conditions.
- **Custom Pruner Implementation**: Integrating pruning callbacks into highly customized or non-standard training loops requires custom callback hooks.
- **High-Dimensional Scaling**: While TPE handles tens of parameters efficiently, ultra-high-dimensional spaces (> 100 hyperparameters) may require specialized high-dimensional samplers.

## When to use it
- When optimizing hyperparameters for machine learning models, neural networks, or LLM fine-tuning tasks.
- When compute resources are limited and early stopping of unpromising trials (pruning) is essential.
- When search spaces contain dynamic or conditional hyperparameter dependencies (e.g., choosing optimizer type before selecting optimizer-specific parameters).

## When not to use it
- For basic scalar script parameters where standard command-line argument parsing with argparse is sufficient.
- For simple end-to-end workflow execution without parameter search (use [Taskfile](../automation_orchestration/taskfile.md) or [Just](../automation_orchestration/just.md)).
- When full black-box neural architecture search across millions of graph nodes is required without manual layer bounds.

## Getting started

### Installation
Install Optuna along with SQLite storage and visualization dependencies:

```bash
pip install optuna optuna-dashboard pydantic
```

### Basic Study Creation
Create a basic Python optimization script:

```python
import optuna

def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    y = trial.suggest_float("y", -10, 10)
    return (x - 2) ** 2 + (y + 3) ** 2

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=50)
print("Best parameters:", study.best_params)
```

## CLI examples

### Running an Optuna Optimization Study via CLI
```bash
# Launch a multi-trial optimization study storing state in a local SQLite DB
optuna create-study --study-name "llm_lora_tuning" --storage "sqlite:///optuna_study.db" --direction "maximize"

# View study statistics from command line
optuna studies --storage "sqlite:///optuna_study.db"
```

### Launching Optuna Dashboard Web UI
```bash
# Spin up real-time web UI dashboard for study visualization
optuna-dashboard sqlite:///optuna_study.db --host 0.0.0.0 --port 8080
```

## API examples

### Python (Hyperparameter Study Configuration with Pydantic v2 Validation)
The following script demonstrates defining study configuration constraints using strict **Pydantic v2** models before executing an Optuna study with automated trial pruning and SQLite persistence.

```python
import os
import optuna
from typing import Literal, Optional
from pydantic import BaseModel, Field, conint, confloat, field_validator

class OptunaStudyConfig(BaseModel):
    study_name: str = Field(..., min_length=3, max_length=100, description="Unique identifier for the HPO study")
    direction: Literal["minimize", "maximize"] = Field("minimize", description="Optimization goal")
    n_trials: conint(ge=5, le=500) = Field(50, description="Total number of trials to run")
    sampler: Literal["tpe", "random", "cmaes"] = Field("tpe", description="Sampling algorithm strategy")
    pruner: Literal["median", "hyperband", "none"] = Field("median", description="Trial pruning algorithm")
    storage_uri: str = Field("sqlite:///optuna_hpo.db", description="Database connection URI for study state")

    @field_validator("study_name")
    @classmethod
    def validate_study_name(cls, v: str) -> str:
        if not v.replace("_", "").isalnum():
            raise ValueError("Study name must be alphanumeric with underscores")
        return v

class TrialResult(BaseModel):
    best_trial_number: int
    best_value: float
    best_params: dict
    total_trials: int

def run_optuna_study(config: OptunaStudyConfig) -> TrialResult:
    # 1. Select Sampler
    if config.sampler == "tpe":
        sampler = optuna.samplers.TPESampler()
    elif config.sampler == "cmaes":
        sampler = optuna.samplers.CmaEsSampler()
    else:
        sampler = optuna.samplers.RandomSampler()

    # 2. Select Pruner
    if config.pruner == "median":
        pruner = optuna.pruners.MedianPruner()
    elif config.pruner == "hyperband":
        pruner = optuna.pruners.HyperbandPruner()
    else:
        pruner = optuna.pruners.NopPruner()

    # 3. Create or Load Study
    study = optuna.create_study(
        study_name=config.study_name,
        direction=config.direction,
        sampler=sampler,
        pruner=pruner,
        storage=config.storage_uri,
        load_if_exists=True
    )

    # 4. Define Objective Function with Pruning Hooks
    def objective(trial: optuna.Trial) -> float:
        lr = trial.suggest_float("learning_rate", 1e-5, 1e-2, log=True)
        batch_size = trial.suggest_categorical("batch_size", [16, 32, 64])
        dropout = trial.suggest_float("dropout", 0.1, 0.5)

        # Simulated epoch training loop with pruning evaluation
        simulated_loss = 1.0
        for step in range(10):
            simulated_loss = (1.0 / (step + 1)) * (lr * 100) + (dropout * 0.1)
            trial.report(simulated_loss, step)

            # Check if trial should be pruned
            if trial.should_prune():
                raise optuna.TrialPruned()

        return simulated_loss

    # 5. Execute Optimization
    study.optimize(objective, n_trials=config.n_trials)

    return TrialResult(
        best_trial_number=study.best_trial.number,
        best_value=study.best_value,
        best_params=study.best_params,
        total_trials=len(study.trials)
    )

if __name__ == "__main__":
    hpo_config = OptunaStudyConfig(
        study_name="lora_hyperparameter_optimization",
        direction="minimize",
        n_trials=30,
        sampler="tpe",
        pruner="median"
    )

    print("Validated Optuna Configuration:")
    print(hpo_config.model_dump_json(indent=2))

    result = run_optuna_study(hpo_config)
    print("\nOptimization Complete:")
    print(f"Best Trial: #{result.best_trial_number}")
    print(f"Best Value (Loss): {result.best_value:.5f}")
    print("Best Parameters:", result.best_params)
```

## Related tools / concepts
- [Axolotl](../frameworks/axolotl.md) — Open-source LLM fine-tuning framework using Optuna for hyperparameter search.
- [Weights & Biases](../process_understanding/wandb-weave.md) — MLOps tracking and visualization platform integrating with Optuna.
- [Docker](../infrastructure/docker.md) — Containerization tool for executing parallel Optuna worker nodes.
- [Argo Workflows](../orchestration/argo-workflows.md) — Kubernetes orchestration system managing multi-node Optuna studies.
- [Pydantic AI](../frameworks/pydantic-ai.md) — Schema validation framework for configuring agent experiment sweeps.
- [Taskfile](../automation_orchestration/taskfile.md) — Task runner for automating HPO trial pipeline execution.
- [Just](../automation_orchestration/just.md) — Command runner for orchestrating local Optuna study commands.

## Sources / references
- [Optuna Official Website](https://optuna.org/)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [Optuna GitHub Repository](https://github.com/optuna/optuna)

## Contribution Metadata
- Last reviewed: 2027-01-07
- Confidence: high

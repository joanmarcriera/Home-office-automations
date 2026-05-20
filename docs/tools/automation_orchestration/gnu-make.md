# GNU Make

## What it is
GNU Make is a tool which controls the generation of executables and other non-source files of a program from the program's source files. It uses a file called a `Makefile` to determine how to build the target programs.

## What problem it solves
It automatically determines which pieces of a large program need to be recompiled, and issues commands to recompile them. This saves time and ensures that the software is always built correctly according to the latest source changes. In modern workflows, it is increasingly used as a task runner to provide a unified entry point for complex multi-tool pipelines.

## Where it fits in the stack
**Tool / Automation**. It provides a foundational layer for automating build processes and task execution within a project.

## Typical use cases
- **Compilation**: Compiling source code (C, C++, Go, etc.) into executables.
- **Task Orchestration**: Providing a standard interface for linting, testing, and deployment.
- **Dependency Management**: Intelligent execution based on file modification times.
- **Environment Setup**: Bootstrapping local development environments (Docker, venv).

## Getting started

### Installation
GNU Make is usually pre-installed on Linux and macOS.

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install build-essential

# macOS (via Xcode Command Line Tools)
xcode-select --install

# Windows (via Chocolatey or Winget)
choco install make
```

### Hello-world task
Create a file named `Makefile`:

```makefile
# Simple Makefile
hello:
	echo "Hello, World"

build:
	mkdir -p dist
	touch dist/app.bin
```

Run the task:
```bash
make hello
```

## Advanced Patterns

### Auto-Documenting Makefile
A popular pattern for making Makefiles self-documenting:

```makefile
.PHONY: help
help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## Run unit tests
	pytest tests/

lint: ## Run code linters
	flake8 .
```

### Docker Integration
Using Make to simplify complex Docker commands:

```makefile
IMAGE_NAME := my-app
VERSION := $(shell git rev-parse --short HEAD)

build: ## Build the docker image
	docker build -t $(IMAGE_NAME):$(VERSION) .

run: ## Run the container locally
	docker run -p 8080:8080 $(IMAGE_NAME):$(VERSION)

push: build ## Build and push to registry
	docker push $(IMAGE_NAME):$(VERSION)
```

## Cross-Tool Orchestration
Make often acts as the "glue" between different tools in the stack:

```makefile
# Orchestrating n8n and Paperless-ngx
sync-docs: ## Pull latest documents from Paperless and trigger n8n workflow
	./scripts/fetch_docs.py --target ./data/vault
	curl -X POST http://n8n.local:5678/webhook/sync-trigger
```

## Strengths
- **Ubiquitous**: Standard on almost all Unix-like systems.
- **Dependency Tracking**: Efficiently skips work that is already up-to-date.
- **Language Agnostic**: Can wrap any command-line tool.
- **Stable**: The core logic has remained consistent for decades.

## Limitations
- **Syntax**: Strict requirement for tabs (not spaces) in recipes.
- **Complexity**: Can become "write-only" code if Makefiles are not well-structured.
- **Shell Dependency**: Relies on the underlying shell (usually `/bin/sh`), which can cause portability issues.

## When to use it
- To provide a "standard interface" for a project (e.g., `make build`, `make test`).
- For managing build artifacts that depend on many source files.
- When you want to minimize dependencies for your automation (Make is usually already there).

## When not to use it
- For very simple scripts where a basic `.sh` or `.py` file is more readable.
- In pure Node.js or Rust environments where `npm` or `cargo` are the standard.

## Related tools / concepts
- [Makefile MCP](makefile-mcp.md)
- [n8n](../../services/n8n.md)
- [Make (formerly Integromat)](make.md)
- [Task](https://taskfile.dev/) (a modern alternative)
- [Just](https://github.com/casey/just) (a command runner inspired by Make)
- [Docker](../infrastructure/docker.md)
- [Python](../development_ops/python.md)
- [LiteLLM](../../services/litellm.md)
- [Ollama](../../services/ollama.md)

## Sources / References
- [GNU Make Official Site](https://www.gnu.org/software/make/)
- [GNU Make Documentation](https://www.gnu.org/software/make/manual/make.html)
- [Makefile Tutorial](https://makefiletutorial.com/)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high

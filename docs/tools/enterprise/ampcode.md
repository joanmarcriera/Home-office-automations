# AmpCode

## What it is
AmpCode is an enterprise-grade platform for building and scaling AI agents with a focus on reliability, security, and developer productivity.

## What problem it solves
It provides the infrastructure needed to transition from experimental agent prototypes to production-ready enterprise applications.

## Where it fits in the stack
**Category**: Enterprise AI

## Typical use cases
- Enterprise task automation
- Secure agentic workflows
- Scaling agent deployments

## Getting started

### Installation
Amp can be installed via a shell script or npm:

```bash
# Recommended for macOS, Linux, and WSL
curl -fsSL https://ampcode.com/install.sh | bash

# Via npm
npm install -g @sourcegraph/amp
```

### Basic usage
Start an interactive AI coding session:

```bash
amp
```

## CLI examples
```bash
# Run a one-shot command in non-interactive mode
amp --execute "Add error handling to the API endpoints"

# Specify a custom log level
amp --execute "Explain this project" --log-level debug

# Authenticate with an API key (for CI/CD)
export AMP_API_KEY="your-api-key"
amp --execute "run tests"
```

## API examples
Amp functionality is primarily exposed through its CLI and its integration with MCP servers. Configuration can be managed via environment variables for automation:

```bash
# Set environment variables for automated workflows
export AMP_API_KEY="your-api-key"
export AMP_LOG_LEVEL="info"
export AMP_SETTINGS_FILE="./custom-settings.json"
```

## Related tools / concepts

- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)

## Sources / references
- [AmpCode Official Site](https://ampcode.com/)

## Contribution Metadata
- Last reviewed: 2026-04-26
- Confidence: medium

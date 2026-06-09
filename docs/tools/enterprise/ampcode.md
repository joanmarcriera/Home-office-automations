# AmpCode

## What it is
AmpCode is an enterprise-grade platform for building and scaling AI agents with a focus on reliability, security, and developer productivity. It is developed by Sourcegraph and serves as the production-grade runtime for Cody-powered agentic workflows.

## What problem it solves
It provides the infrastructure needed to transition from experimental agent prototypes to production-ready enterprise applications. It leverages frontier models like **Claude 4.8 (Opus)** and **GPT-5.5** to manage complex, multi-step engineering tasks across massive distributed codebases.

## Where it fits in the stack
**Category**: Enterprise AI / Development & Ops. It sits at the intersection of code intelligence and agentic orchestration.

## Typical use cases
- **Enterprise Repository Orchestration**: Managing complex tasks across massive, distributed codebases with trillions of lines of code.
- **Secure Agent Deployment**: Running agents in environments with strict security, compliance, and auditing requirements.
- **Developer Productivity at Scale**: Automating boilerplate, large-scale refactors, and tests across entire engineering organizations.
- **Automated Dependency Management**: Proactively identifying and updating stale dependencies across multiple projects using **Llama 4 Maverick** for local analysis.

## Strengths
- **Security-First**: Built for enterprise environments with robust authentication, auditing, and sandboxed execution.
- **Sourcegraph Integration**: Leverages Sourcegraph's deep code intelligence ([Cody](../development_ops/sourcegraph_cody.md)) for better context and reasoning.
- **High Reliability**: Focuses on deterministic outcomes and production-grade stability with built-in verification loops.
- **June 2026 Ready**: Native support for **Claude 4.8** (Opus) and **GPT-5.5** for advanced reasoning and code synthesis.

## Limitations
- **Closed Ecosystem**: Proprietary software that requires an enterprise license for full features.
- **Target Audience**: Less optimized for individual developers or small open-source projects compared to tools like [Aider](../development_ops/aider.md).
- **Complexity**: Enterprise-scale features require significant configuration and infrastructure (e.g., Sourcegraph instance).

## When to use it
- In corporate environments where security and scalability are the top priorities for AI-assisted engineering.
- When you need an agent that can reason across thousands of repositories safely and consistently.
- If you are already invested in the Sourcegraph ecosystem.

## When not to use it
- For personal projects or small teams where free, open-source alternatives like [Aider](../development_ops/aider.md) or [Claude Code](../development_ops/claude-code.md) are sufficient.
- If you require a fully transparent, open-weight model stack for all operations.

## Licensing and cost
- **Open Source**: No (Proprietary)
- **Cost**: Paid (Enterprise subscription)
- **Self-hostable**: Yes (for Enterprise customers, typically co-located with Sourcegraph)

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

# Specify a custom log level and model (June 2026)
amp --execute "Explain this project" --model claude-4.8-opus --log-level debug

# Authenticate with an API key (for CI/CD)
export AMP_API_KEY="your-api-key"
amp --execute "run tests"

# List available agents in the enterprise registry
amp agents list
```

## API examples
Amp functionality is primarily exposed through its CLI and its integration with [MCP](../automation_orchestration/mcp.md) servers. Configuration can be managed via environment variables for automation. You can also interact with the underlying Sourcegraph API that Amp utilizes for deeper repository insights.

### Python Example: Fetching Repository Context (via GraphQL)
Amp leverages Sourcegraph's GraphQL API for deep code search and context retrieval.

```python
import os
import requests
import json

def get_amp_repo_context(repo_name, query_text):
    api_key = os.getenv("AMP_API_KEY")
    url = "https://sourcegraph.com/.api/graphql"

    # GraphQL query for cross-repository search
    query = """
    query Search($query: String!) {
      search(query: $query, version: V2) {
        results {
          results {
            ... on FileMatch {
              file {
                path
                repository {
                  name
                }
              }
              lineMatches {
                lineNumber
                preview
              }
            }
          }
        }
      }
    }
    """

    search_string = f"repo:^{repo_name}$ {query_text}"
    variables = {"query": search_string}
    headers = {"Authorization": f"token {api_key}"}

    response = requests.post(
        url,
        json={"query": query, "variables": variables},
        headers=headers
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with status {response.status_code}: {response.text}")

# Example: Search for authentication logic in a specific repo
# context = get_amp_repo_context("github.com/org/project", "type:file login")
# print(json.dumps(context, indent=2))
```

## Related tools / concepts

- [Fyxer AI](fyxer.md)
- [Glean](glean.md)
- [Hebbia](hebbia.md)
- [Claude Code](../development_ops/claude-code.md)
- [Sourcegraph Cody](../development_ops/sourcegraph_cody.md)
- [Model Context Protocol (MCP)](../automation_orchestration/mcp.md)
- [Claude 4.8](../providers/anthropic.md)
- [GPT-5.5](../ai_knowledge/openai.md)
- [Llama 4 Maverick](../ai_knowledge/local_llms.md)

## Sources / references
- [AmpCode Official Site](https://ampcode.com/)
- [Sourcegraph API Documentation](https://sourcegraph.com/docs/api/graphql)
- [AmpCode Release Notes - June 2026](https://releasebot.io/updates/ampcode)

## Contribution Metadata
- Last reviewed: 2026-06-08
- Confidence: high

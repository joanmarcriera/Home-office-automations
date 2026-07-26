# Reference Implementation: LLM Prompt for Vikunja Task Routing

## What it is
A structured system prompt and JSON schema designed to enable AI agents to autonomously categorize, prioritize, and route incoming task requests into specific Vikunja projects. It leverages LLM reasoning to map natural language intent to structured task metadata.

## What problem it solves
Managing a growing list of tasks across multiple projects can become a bottleneck for family and personal administration. Manual triage is tedious. This implementation automates the intake process, ensuring that tasks are filed correctly with appropriate urgency and context without requiring manual entry into the Vikunja UI.

## Where it fits in the stack
This prompt sits at the **Reasoning/Execution layer** of a Home Admin Agent. It acts as the bridge between the **User Interface** (e.g., chat, voice) and the **Task Management System** (Vikunja), typically orchestrated via a tool-calling framework or an automation platform like n8n.

## Typical use cases
- **Voice-to-Task**: "Hey agent, remind me to buy milk" results in a task in the 'Shopping' project.
- **Email Triage**: Extracting action items from school emails and routing them to the 'Admin' or 'School' project.
- **Maintenance Tracking**: Logged repairs (e.g., "The fridge is making a weird noise") are automatically sent to 'Home Maintenance'.

## Strengths
- **Context-Aware**: Uses project lists and current dates to make informed routing decisions.
- **Standardized Output**: JSON schema ensures high reliability for programmatic tool calls.
- **Flexible Priority**: Maps natural language urgency to a consistent 1-5 scale.

## Limitations
- **Project Overlap**: Ambiguous tasks might be routed to the 'Inbox' if project descriptions are not distinct.
- **Model Dependency**: Requires a model capable of reliable structured JSON output (e.g., **GPT-5.5**, **Claude 5.1**, **Qwen 3.6**, or **Llama 4**).

## When to use it
- When you have more than 3-5 distinct projects in Vikunja.
- When you want to enable hands-free task entry via voice or messaging.
- When delegating task triage to an autonomous agent.

## When not to use it
- For very simple setups with only one list (a simple prompt would suffice).
- If the agent does not have real-time access to the current project IDs (risk of hallucinating IDs).

## Getting started
To implement this pattern, you need a Vikunja instance, an LLM provider (e.g., Anthropic Claude 5.1), and an orchestration tool (n8n).
1. Define your core project names and IDs in Vikunja.
2. Configure your system prompt using the template provided below.
3. Set up an n8n workflow that triggers on user input and calls the LLM with the project list.

### Prompt Template
```markdown
You are the Home Admin Agent, responsible for managing the family's task list in Vikunja.
Your goal is to route new tasks into the correct project and set appropriate metadata based on the context.

### Context:
- User Request: {{user_request}}
- Current Projects: {{project_list}}
- Current Date: {{current_date}}

### Routing Guidelines:
1. **Inbox**: Use for tasks that are vague or don't fit into specific projects.
2. **Maintenance**: Use for home repairs, car servicing, or appliance upkeep.
3. **Admin**: Use for bills, paperwork, renewals, or school-related admin.
4. **Health**: Use for medical appointments, prescriptions, or fitness goals.
5. **Shopping**: Use for grocery lists or specific items to purchase.

### Priority Levels:
- **5 (Critical)**: Urgent deadlines (due within 48 hours), health emergencies, or critical home repairs (e.g., leaking pipe).
- **3 (Medium)**: Normal chores, routine appointments, or tasks due within a week.
- **1 (Low)**: Long-term projects, "nice to have" shopping items, or non-urgent reminders.

### Output Format:
Return a JSON object:
{
  "title": "Clear, concise task title",
  "project_id": integer,
  "description": "Optional detailed context",
  "due_date": "YYYY-MM-DDTHH:MM:SSZ (if applicable)",
  "priority": integer (1-5),
  "labels": ["string"],
  "reasoning": "Brief explanation of why this project and priority were chosen"
}
```

## CLI examples
You can test the prompt logic using a CLI tool like `llm` or `curl` to interact with your LLM provider.

```bash
# Example using curl to test the routing logic with Claude 5.1
curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{
       "model": "claude-5-1-sonnet-20260620",
       "max_tokens": 1024,
       "messages": [{"role": "user", "content": "Remind me to fix the kitchen sink tomorrow"}]
     }'
```

## API examples
Integration via the **Model Context Protocol (MCP 3.1)** allows for direct tool calling into Vikunja.

### JSON Schema for Constrained Output
```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "project_id": { "type": "integer" },
    "description": { "type": "string" },
    "due_date": { "type": "string", "format": "date-time" },
    "priority": { "type": "integer", "minimum": 1, "maximum": 5 },
    "labels": { "type": "array", "items": { "type": "string" } },
    "reasoning": { "type": "string" }
  },
  "required": ["title", "project_id", "priority"]
}
```

### Agent Integration Pattern (Python)
```python
# Using VikunjaCreateTool for execution
import asyncio
from scripts.vikunja_tool import VikunjaCreateTool

async def route_task(user_input: str, parsed_json: dict):
    # Initialize the create tool
    tool = VikunjaCreateTool()

    # Execute creation payload with Pydantic v2 validation and MCP 3.1 Task Protocol compliance
    result = await tool.run(
        title=parsed_json["title"],
        project_id=parsed_json["project_id"],
        description=parsed_json.get("description"),
        due_date=parsed_json.get("due_date"),
        priority=parsed_json.get("priority")
    )
    print(result)

# Example execution mock
if __name__ == "__main__":
    mock_payload = {
        "title": "Fix the leaking kitchen sink faucet",
        "project_id": 4,
        "description": "Under-sink pipe shows light moisture. Inspect and seal.",
        "due_date": "2026-09-01T12:00:00Z",
        "priority": 5
    }
    asyncio.run(route_task("Fix leaking sink faucet tomorrow", mock_payload))
```

## Related tools / concepts
- [Vikunja](../../services/vikunja.md): The target task management system.
- [Home Admin Agent Architecture](../../knowledge_base/home-admin-agent-architecture.md): The overall framework for this implementation.
- [n8n](../../services/n8n.md): Common orchestration platform for these workflows.
- [System Prompts](../../knowledge_base/system_prompts.md): Best practices for designing agent personas.
- [Agentic Workflows](../../knowledge_base/patterns/agentic-workflows.md): Patterns for multi-step task execution.
- [Model Routing Guide](../../knowledge_base/model_routing_guide.md): Deciding which LLM to use for task triage.
- [Email-to-Calendar Playbook](../../playbooks/email-to-calendar.md): A similar pattern for scheduling.
- [MCP](../../tools/automation_orchestration/mcp.md) — Standardized protocol for model-tool interaction.

## Sources / references
- [Vikunja API Documentation](https://vikunja.io/docs/api/)
- [JSON Schema Standard](https://json-schema.org/)
- [Anthropic Claude Documentation](https://docs.anthropic.com/)

## Contribution Metadata
- Last reviewed: 2026-08-31
- Confidence: high

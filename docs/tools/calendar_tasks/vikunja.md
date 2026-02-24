# Vikunja

## What it is
Vikunja is an open-source self-hosted to-do list application that allows you to organize your tasks, projects, and life.

## What problem it solves
It provides a privacy-first, highly customizable task manager that can be hosted locally, offering an alternative to cloud tools like Todoist or Trello.

## Where it fits in the pipeline
**Decide / Act**

## Typical use cases (in this homelab / family automation context)
- **Family Tasks**: Managing shared shopping lists and household chores.
- **Project Planning**: Tracking progress on homelab upgrades and coding projects.
- **Automation Trigger**: Automatically creating tasks from school emails or Home Assistant alerts.

## Related Playbooks
- [Scan to Task](../../../playbooks/scan-to-task.md)
- [Family Admin Automation](../../../playbooks/family-admin-automation.md)

## Integration points
- **CalDAV**: Allows viewing tasks as a calendar or managing them in other clients.
- **n8n**: Using the Vikunja node to automate task creation and updates.
- **API**: Full REST API for custom integrations and dashboards.

## Licensing and cost
- **Open Source**: Yes (AGPL-3.0)
- **Cost**: Free (Self-hosted)
- **Free tier**: N/A (Self-hosted); Cloud version has a free tier.
- **Self-hostable**: Yes

## Strengths
- Beautiful and clean user interface.
- Multiple views (List, Gantt, Kanban, Table).
- Strong focus on privacy and user data ownership.

## Limitations
- Mobile apps are available but may feel less polished than cloud competitors.
- Requires some setup for the backend (API) and frontend (UI).

## Alternatives / Related tools
- **Todoist**
- **Trello**
- **Nextcloud Tasks**

## Links
- [Official Website](https://vikunja.io/)
- [GitHub](https://github.com/go-vikunja/vikunja)

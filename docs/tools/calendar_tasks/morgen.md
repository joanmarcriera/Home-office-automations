# Morgen

## What it is
Morgen is a cross-platform calendar, task manager, and meeting scheduler that aggregates all your calendars into one place. It is built as a unified interface for managing multiple scheduling providers, including Google, Outlook, iCloud, Exchange, and CalDAV.

## What problem it solves
It eliminates the "multiple calendar" problem by consolidating disparate scheduling sources into a single, cohesive interface on desktop and mobile. It also addresses the friction of scheduling meetings by providing integrated scheduling links (similar to Calendly) and allowing users to time-block tasks directly onto their calendar.

## Where it fits in the stack
**Category**: Calendar & Tasks / Unified Scheduling. It serves as the primary daily scheduling interface for users who operate across multiple ecosystems (e.g., a mix of Windows, macOS, and Linux).

## Typical use cases
- **Unified Personal and Work Scheduling**: Viewing an iCloud personal calendar alongside a corporate Exchange calendar.
- **Task Time-Blocking**: Syncing tasks from providers like Todoist or Microsoft To-Do and dragging them into calendar slots.
- **Meeting Scheduling**: Creating and sharing scheduling links that automatically respect the availability across all connected calendars.
- **CalDAV Management**: Providing a modern UI for self-hosted calendars like [Radicale](../../services/radicale.md).

## Strengths
- **Broad Provider Support**: One of the few modern apps with robust support for iCloud, Exchange, and CalDAV simultaneously.
- **Cross-Platform**: Native applications for Windows, macOS, Linux, iOS, and Android.
- **Privacy-Conscious**: Offers local-only calendar options and clear data handling policies.
- **Integrated Scheduling**: Combines calendar management with meeting links and task time-blocking in one app.

## Limitations
- **Subscription Required**: Advanced features, such as multiple scheduling links and deep task integrations, require a paid plan.
- **No Web Interface**: Unlike competitors, Morgen focuses on native apps, which may be a limitation for users who cannot install software on certain machines.
- **UI Density**: The interface can become crowded when many calendars and tasks are displayed at once.

## When to use it
- If you use a mix of operating systems and need a high-quality, unified calendar app that works everywhere.
- If you need to manage self-hosted CalDAV servers alongside standard cloud providers.
- If you want an all-in-one tool for scheduling meetings, managing tasks, and viewing your calendar.

## When not to use it
- If you only use a single calendar provider (e.g., only Google Calendar) and don't need task integration.
- If you prefer a web-based scheduling workflow without installing local applications.
- If you require a purely open-source solution for your calendar management.

## Getting started

### Installation
Download the Morgen application for your platform from the [official website](https://www.morgen.so/download).

### Connecting Calendars
1. Launch Morgen and follow the setup wizard.
2. Select your providers (Google, Outlook, iCloud, etc.).
3. For CalDAV (e.g., Radicale or Nextcloud), select "CalDAV" and provide your server URL, username, and password.

### Setting up Scheduling Links
- Navigate to the "Scheduling" tab (calendar icon with a link).
- Create a new "Booking Page" or "Quick Meeting".
- Customize your availability and share the generated link.

## Licensing and cost
- **Open Source**: No
- **Cost**: Freemium (Basic version is free; Pro features require a subscription).
- **Self-hostable**: No (Cloud-based service with native clients).

## Related tools / concepts
- [Akiflow](akiflow.md) (Task-focused command center)
- [Fantastical](fantastical.md) (macOS/iOS-centric alternative)
- [Calendly](calendly.md) (Specialized scheduling links)
- [Radicale](../../services/radicale.md) (Self-hosted CalDAV backend)
- [Nextcloud](../../services/nextcloud.md) (Self-hosted cloud with calendar support)
- [Todoist](todoist.md) (Task integration source)
- [Microsoft To-Do](microsoft-todo.md) (Task integration source)
- [CalDAV](../intake_storage/caldav.md) (Underlying protocol)

## Sources / References
- [Morgen Official Site](https://www.morgen.so/)
- [Morgen Help Center](https://morgen.notion.site/Morgen-Help-Center-885474c3e86c4a85a4f66453f6316278)

## Contribution Metadata
- Last reviewed: 2026-07-20
- Confidence: high

# CalDAV

## What it is
CalDAV is an internet standard allowing a client to access scheduling information on a remote server. It extends WebDAV and uses the iCalendar format.

## What problem it solves
It enables interoperability between different calendar clients (iOS, Android, Outlook, Thunderbird) and servers (Nextcloud, Radicale, Google Calendar).

## Where it fits in the pipeline
**Sync / Protocol**

## Typical use cases (in this homelab / family automation context)
- **Multi-Device Calendar Sync**: Ensuring that an event added on a phone appears on a desktop and a smart home dashboard.
- **Shared Family Calendars**: Allowing multiple family members to view and edit a shared schedule.

## Integration points
- **Nextcloud**: Implements CalDAV for its calendar functionality.
- **Radicale**: A dedicated, lightweight CalDAV server.
- **Home Assistant**: Can connect to CalDAV servers to trigger automations based on calendar events.

## Licensing and cost
- **Open Source**: Yes (Standard specification)
- **Cost**: Free
- **Free tier**: N/A
- **Self-hostable**: Yes (via various implementations)

## Strengths
- Open and widely supported standard.
- Supports complex recurring events and reminders.
- Decentralized.

## Limitations
- Performance can be an issue with very large calendars.
- Implementation quality varies between different clients.

## Alternatives / Related tools
- **CardDAV** (for contacts)
- **Google Calendar API** (Proprietary alternative)

## Links
- [Official Specification (RFC 4791)](https://tools.ietf.org/html/rfc4791)
- [CalDAV.org](http://caldav.org/)

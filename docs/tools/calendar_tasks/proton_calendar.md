# Proton Calendar

## What it is
Proton Calendar is a privacy-focused, end-to-end encrypted calendar service developed by Proton (the makers of Proton Mail).

## What problem it solves
It provides a secure and private way to manage schedules and events without exposing data to service providers or third-party advertisers. It ensures that your itinerary remains confidential even from the service provider.

## Where it fits in the stack
**Orchestration / Personal Information Management**. It serves as a secure alternative to cloud calendars like Google Calendar or Outlook.

## Typical use cases
- **Confidential Scheduling**: Managing sensitive personal or business schedules.
- **Secure Invitations**: Sending and receiving encrypted event invitations.
- **Team Coordination**: Sharing calendars within a secure ecosystem.
- **Cross-platform Sync**: Synchronization across web, Android, and iOS.

## Security Model
Proton Calendar uses several layers of protection:
- **End-to-End Encryption (E2EE)**: Event titles, descriptions, locations, and participants are encrypted on the client side before being sent to Proton's servers.
- **Zero-Access Encryption**: Proton cannot decrypt your data; they only store the encrypted blobs.
- **Signed Events**: Prevents tampering with event data during transit or at rest.

## Getting started

### Account Setup
1. Create a Proton account at [proton.me](https://proton.me).
2. Access the calendar via the web interface or mobile app.

### Data Migration
To import existing calendars:
1. Export your calendar from Google or Outlook as an `.ics` file.
2. In Proton Calendar, go to **Settings** > **Import**.
3. Upload the `.ics` file.

## Integration Patterns

### Proton Bridge
While Proton Calendar does not support native CalDAV for third-party apps directly, users often use the **Proton Bridge** (primarily for Mail) as a proxy. For Calendar specifically, native CalDAV support is a highly requested feature but currently limited.

### Exporting for External Use
You can generate a "Secret Link" to share your calendar in a read-only format with other applications that support iCal:
1. Go to **Settings** > **Calendars**.
2. Select the calendar and click **Share**.
3. Copy the **Secret Link**.

## CLI / Automation Options
Official CLI support for Proton Calendar is currently absent. However, users can interact with encrypted data via community tools or the official Bridge for related services.

### Conceptual: Importing via .ics (CLI)
You can use standard CLI tools to prepare and manage calendar data before uploading:

```bash
# Combine multiple ICS files for import
cat calendar1.ics calendar2.ics > combined.ics

# Verify ICS structure before import
grep "BEGIN:VEVENT" combined.ics | wc -l
```

## Strengths
- **Privacy**: E2EE for all major event fields.
- **Security**: Strong authentication (2FA/Security Keys) and data protection.
- **Transparency**: Client-side code is open source and regularly audited.
- **No Ads**: Data is not scanned for advertising purposes.

## Limitations
- **Limited Integration**: No direct CalDAV support for desktop apps like Apple Calendar without third-party workarounds.
- **Automation Gap**: Lack of official API or CLI tools for programmatic event management.
- **Features**: Fewer advanced scheduling features compared to Google Calendar.

## When to use it
- When privacy and data security are the top priorities.
- If you are already integrated into the Proton ecosystem (Mail, Drive, VPN).
- For managing highly sensitive appointments or legal/medical schedules.

## When not to use it
- If you require deep integration with many third-party automation tools (Zapier, Make, etc.).
- If you need native CalDAV access for legacy desktop calendar applications.

## Related tools / concepts
- [Google Calendar](google_calendar.md)
- [Nextcloud Calendar](../../services/nextcloud.md)
- [CalDAV](../intake_storage/caldav.md)
- [Proton Mail](https://proton.me/mail)
- [Home Assistant](../../services/home-assistant.md) (via iCal integration)
- [n8n](../../services/n8n.md) (via HTTP/iCal)
- [Amie](amie.md)
- [Sunsama](sunsama.md)

## Sources / references
- [Official Website](https://proton.me/calendar)
- [Proton Calendar Security Model](https://proton.me/blog/proton-calendar-security-model)
- [How to use Proton Calendar](https://proton.me/support/proton-calendar-basics)

## Contribution Metadata
- Last reviewed: 2026-05-19
- Confidence: high

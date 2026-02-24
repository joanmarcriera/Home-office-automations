# Nextcloud

## What it is
Nextcloud is a suite of client-server software for creating and using file hosting services. It is functionally similar to Dropbox or Google Drive.

## What problem it solves
It provides a self-hosted alternative to cloud storage, ensuring data privacy and control. It integrates files, calendars, contacts, and communication in one platform.

## Where it fits in the pipeline
**Store / Sync**

## Typical use cases (in this homelab / family automation context)
- **Central Storage**: Storing all family photos and videos.
- **CalDAV/CardDAV Server**: Hosting shared family calendars and contacts.
- **Document Collaboration**: Editing documents together using integrated office suites.

## Integration points
- **WebDAV**: For mounting as a network drive on local machines.
- **n8n**: Using the Nextcloud node for file operations and calendar triggers.
- **Paperless-ngx**: Serving as a source for the consumption directory.

## Licensing and cost
- **Open Source**: Yes (AGPL)
- **Cost**: Free (Self-hosted)
- **Free tier**: N/A
- **Self-hostable**: Yes

## Strengths
- Highly extensible via an internal app store.
- Strong focus on security and compliance.
- Multi-platform clients (Windows, Mac, Linux, iOS, Android).

## Limitations
- Can be resource-intensive for small servers.
- Database maintenance is critical for performance.

## Alternatives / Related tools
- **OwnCloud**
- **Seafile**
- **Syncthing**

## Links
- [Official Website](https://nextcloud.com/)
- [GitHub](https://github.com/nextcloud/server)

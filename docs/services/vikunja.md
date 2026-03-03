# Vikunja

Vikunja is an open-source, self-hosted To-do list application.

## Description
It allows you to organize all your tasks on all platforms. It features boards, lists, and a powerful filter system.

## Getting started

### Docker
To get Vikunja up and running quickly with Docker:

```bash
docker run -p 3456:3456 -v $PWD/files:/app/vikunja/files -v $PWD/db:/db vikunja/vikunja
```

Navigate to `http://localhost:3456` to access the web interface.

## CLI examples

When running in Docker, execute commands using `docker exec`:

```bash
# List all users
docker exec <container_name> /app/vikunja/vikunja user list

# Create a full dump of the database and files
docker exec <container_name> /app/vikunja/vikunja dump

# Show Vikunja version
docker exec <container_name> /app/vikunja/vikunja version
```

## API examples

Authenticate using an API token in the `Authorization` header:

```bash
curl -H "Authorization: Bearer <your_api_token>" \
     "https://try.vikunja.io/api/v1/tasks"
```

## Links
- [Official Website](https://vikunja.io/)
- [Documentation](https://vikunja.io/docs/)

## Alternatives
- [Focalboard](focalboard.md)
- [Nextcloud Tasks](nextcloud.md)

## Backlog
- Sync with CalDAV (Radicale).

## Sources / References

- [Official Documentation](https://vikunja.io/docs/)
- [CLI Reference](https://vikunja.io/docs/cli/)

## Contribution Metadata

- Last reviewed: 2026-03-02
- Confidence: high

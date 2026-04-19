# Nextcloud

Nextcloud is the most deployed self-hosted content collaboration platform.

## Description
It provides a safe home for all your data - files, contacts, calendars, and more.

## When to use it
- When you need a comprehensive, self-hosted suite for file storage, collaboration, and productivity.
- For users who want to maintain full control over their data while having access to features similar to Google Workspace or Microsoft 365.
- When you want an extensible platform with a wide range of apps (Talk, Calendar, Contacts, Office).

## When not to use it
- If you only need simple file synchronization without the extra features (consider [Syncthing](syncthing.md)).
- If you have very limited server resources, as Nextcloud can be resource-intensive.

## Getting started

### Docker
The fastest way to get Nextcloud running is using the official Docker image:

```bash
docker run -d \
  --name nextcloud \
  -p 8080:80 \
  -v nextcloud:/var/www/html \
  nextcloud
```

Access Nextcloud at `http://localhost:8080`.

### Hello World
1. Run the Docker command to start Nextcloud.
2. Navigate to `http://localhost:8080` in your browser.
3. Create an admin account by entering a username and password.
4. Click **Install** to finish the initial setup.
5. You can now start uploading files or installing apps from the Nextcloud App Store.

## CLI examples
Nextcloud includes the `occ` (Nextcloud Command-line Control) tool for server management.

```bash
# List all available occ commands
docker exec --user www-data nextcloud php occ list

# Reset the admin password
docker exec --user www-data nextcloud php occ user:resetpassword admin

# Put the server into maintenance mode
docker exec --user www-data nextcloud php occ maintenance:mode --on
```

## API examples
Nextcloud supports the OCS (Open Collaboration Services) API for remote management.

### Get user information
```bash
curl -u admin:password \
     -H "OCS-APIRequest: true" \
     -X GET "http://localhost:8080/ocs/v1.php/cloud/users/admin"
```

### List files via WebDAV
```bash
curl -u admin:password \
     -X PROPFIND "http://localhost:8080/remote.php/dav/files/admin/"
```

## Links
- [Official Website](https://nextcloud.com/)

## Alternatives
- [Owncloud](https://owncloud.com/)
- [Seafile](https://www.seafile.com/)

## SSO & OIDC Integration
Nextcloud can be integrated with [Authentik](authentik.md) for Single Sign-On using the `user_oidc` app.

### Configuration Steps
1.  **Install App**: In Nextcloud, go to **Apps** and install the **OpenID Connect user backend** (`user_oidc`) app.
2.  **Authentik Provider**: Create an OAuth2/OpenID Provider in Authentik:
    -   **Client Type**: Confidential.
    -   **Redirect URIs**: `https://nextcloud.example.com/apps/user_oidc/openid-callback/authentik`
3.  **Nextcloud Settings**: Go to **Administration settings > OpenID Connect**:
    -   **Provider Identifier**: `authentik`
    -   **Discovery Endpoint**: `https://authentik.example.com/application/o/nextcloud/.well-known/openid-configuration`
    -   **Client ID**: `<Your Client ID>`
    -   **Client Secret**: `<Your Client Secret>`
    -   **Scope**: `openid profile email`

> [!WARNING]
> If you require Server-Side Encryption, you must use LDAP instead of OIDC, as encryption requires the user's cleartext password which is not provided by OIDC.

## Backlog
- Setup Nextcloud Office with Collabora Online.
- Enable end-to-end encryption for sensitive folders.

## Sources / References

- [Reference](https://nextcloud.com/)
- [Reference](https://owncloud.com/)
- [Reference](https://www.seafile.com/)

## Contribution Metadata
- Confidence: medium
- Last reviewed: 2026-04-08

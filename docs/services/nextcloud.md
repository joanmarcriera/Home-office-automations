# Nextcloud

## What it is

Nextcloud is a suite of client-server software for creating and using file hosting services. It is the most deployed self-hosted content collaboration platform, providing a safe home for all your data - files, contacts, calendars, and more.

## What problem it solves

Public cloud services like Google Drive or Microsoft 365 offer great convenience but at the cost of data privacy and ownership. Nextcloud solves this by providing a comprehensive, enterprise-grade collaboration suite that you host on your own hardware, giving you full control over who has access to your data while maintaining the ease of use of a modern cloud platform.

## Where it fits in the stack

**Category**: Service / Productivity. It serves as the **unified content and collaboration hub**, acting as the primary repository for documents, personal data, and team communication in a home-office or small business environment.

## Typical use cases

- **File Synchronization**: Keeping documents and photos synced across multiple computers and mobile devices.
- **Collaborative Editing**: Real-time document editing using integrated tools like OnlyOffice or Collabora Online.
- **Personal Information Management (PIM)**: Syncing calendars, contacts, and tasks using open standards like CalDAV and CardDAV.
- **Secure File Sharing**: Sharing large files with external parties via password-protected links.

## Strengths

- **Extensible**: A vast App Store allows for adding features like Kanban boards, video conferencing (Talk), and music players.
- **Multi-Platform**: Robust client apps for Windows, macOS, Linux, Android, and iOS.
- **Open Standards**: Built on PHP and SQL, using WebDAV/CalDAV for maximum compatibility with third-party tools.
- **Strong Ecosystem**: Massive community and commercial support ensure longevity and security.

## Limitations

- **Resource Intensive**: Requires significant RAM and CPU compared to lightweight single-purpose tools like Syncthing.
- **Configuration Overhead**: Proper optimization (Redis caching, background jobs) is necessary for a smooth experience on large libraries.
- **Complex Upgrades**: Major version updates can sometimes be delicate, requiring manual intervention.

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

## Related tools / concepts

- [Syncthing](syncthing.md) — for a lighter, peer-to-peer file sync alternative
- [Authentik](authentik.md) — for managing Nextcloud SSO/OIDC authentication
- [Tailscale](tailscale.md) — for secure remote access to your Nextcloud instance
- [Paperless-ngx](paperless-ngx.md) — can be integrated with Nextcloud for document archival
- [OnlyOffice/Collabora](https://nextcloud.com/office/) — for real-time document editing within Nextcloud
- [n8n](n8n.md) — for automating file processing and notification workflows

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

## Nextcloud Office & Collabora

Nextcloud Office provides a powerful, browser-based office suite integrated directly into Nextcloud. It is powered by Collabora Online.

### Setup (Docker)
1.  **Run Collabora Online**:
    ```bash
    docker run -d --name collabora \
      -e "domain=nextcloud\\.example\\.com" \
      -e "extra_params=--o:ssl.enable=true --o:ssl.termination=true" \
      -p 9980:9980 \
      --restart unless-stopped \
      collabora/code
    ```
2.  **Install App**: In Nextcloud, go to **Apps** and install **Nextcloud Office**.
3.  **Configure**: Go to **Administration settings > Nextcloud Office**:
    -   Select "Use your own server".
    -   Enter the URL of your Collabora instance: `https://collabora.example.com`.

## End-to-End Encryption (E2EE)

Nextcloud supports client-side end-to-end encryption for maximum security of sensitive files.

### Key Characteristics
-   **Zero-Knowledge**: The server never sees the contents of encrypted files or the encryption keys.
-   **Folder-Based**: Encryption is enabled on a per-folder basis.
-   **Client-Side**: Encryption and decryption happen on the user's device (desktop or mobile apps).

### Enablement
1.  **Install App**: Install the **End-to-End Encryption** app from the Nextcloud App Store.
2.  **Setup Passphrase**: On your desktop or mobile client, enable encryption for a folder. You will be provided with a 12-word recovery mnemonic. **Store this securely.**
3.  **Limitations**: Encrypted folders cannot be shared with users who do not have E2EE configured, and they are not accessible via the web interface.

## Backlog
- [x] Setup Nextcloud Office with Collabora Online.
- [x] Enable end-to-end encryption for sensitive folders.

## Sources / References

- [Official Website](https://nextcloud.com/)
- [Nextcloud Admin Documentation](https://docs.nextcloud.com/server/latest/admin_manual/)
- [Owncloud](https://owncloud.com/)
- [Seafile](https://www.seafile.com/)

## Contribution Metadata

- Last reviewed: 2026-06-25
- Confidence: high

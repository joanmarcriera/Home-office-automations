# Syncthing

## What it is
Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time, safely protected from prying eyes.

## What problem it solves
It allows for decentralized, peer-to-peer file synchronization without relying on a central server or cloud provider.

## Where it fits in the pipeline
**Sync**

## Typical use cases (in this homelab / family automation context)
- **Note Sync**: Syncing Obsidian or Logseq vaults between a desktop and a mobile device.
- **Backup**: Automatically syncing phone photos to a home server as they are taken.
- **Project Sync**: Keeping coding projects in sync across multiple development machines.

## Integration points
- **Local File System**: Works directly with directories on the host machine.
- **Tailscale**: Often used together to allow syncing across different networks without port forwarding.

## Licensing and cost
- **Open Source**: Yes (MPL-2.0)
- **Cost**: Free
- **Free tier**: N/A
- **Self-hostable**: Yes (P2P)

## Strengths
- No central server required.
- High privacy and security (TLS and Perfect Forward Secrecy).
- Very efficient with bandwidth and resources.

## Limitations
- No native iOS app (requires 3rd party like Mobius Sync).
- No built-in versioning (requires integration with tools like Stagger or Btrfs snapshots).

## Alternatives / Related tools
- **Resilio Sync** (Proprietary)
- **Nextcloud**

## Links
- [Official Website](https://syncthing.net/)
- [GitHub](https://github.com/syncthing/syncthing)

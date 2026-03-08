# Minecraft Server

A self-hosted game server for Minecraft.

## Description
It allows you to host your own Minecraft world for friends and family. It can be easily managed on TrueNAS via the official or community charts, supporting both Java and Bedrock editions.

## When to use it
- When you want to host a private Minecraft world for friends and family.
- When you need a self-hosted solution with easy management of versions, mods, and plugins.
- When running on a home server or NAS with sufficient resources.

## When not to use it
- For large-scale public servers with thousands of concurrent players.
- When you prefer a fully managed hosting service to avoid maintenance tasks.
- On hardware with very limited RAM (less than 2-4GB recommended for a smooth experience).

## Getting started

### Docker Compose
The most popular way to run a Minecraft server in Docker is using the `itzg/minecraft-server` image:

```yaml
services:
  minecraft-server:
    image: itzg/minecraft-server
    container_name: minecraft-server
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      MEMORY: "4G"
    ports:
      - "25565:25565"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

Run with `docker compose up -d`.

## CLI examples
Interact with the server console using `docker exec` and the built-in RCON client:

```bash
# Run a command on the server console (e.g., list players)
docker exec minecraft-server rcon-cli list

# Give an item to a player
docker exec minecraft-server rcon-cli give <player_name> diamond 64

# Show server version and help
docker exec minecraft-server rcon-cli help
```

## API examples
You can query the server status using the `mcstatus` Python library:

```bash
# Install the library
pip install mcstatus

# Query server status from the command line
mcstatus localhost:25565 status
```

Or via a Python script:

```python
from mcstatus import JavaServer

# Lookup the server
server = JavaServer.lookup("localhost:25565")

# Query the server
status = server.status()
print(f"The server has {status.players.online} players and replied in {status.latency} ms")
```

## Links
- [Minecraft Official Site](https://www.minecraft.net/)
- [itzg/minecraft-server GitHub](https://github.com/itzg/docker-minecraft-server)

## Alternatives
- [Minetest](https://www.minetest.net/) (Open Source alternative)

## Backlog
- Set up automated backups of world data.


## Contribution Metadata
- Confidence: high
- Last reviewed: 2026-03-01

## Sources / References
- https://www.minecraft.net/
- https://www.minetest.net/
- https://github.com/itzg/docker-minecraft-server

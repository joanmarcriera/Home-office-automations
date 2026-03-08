# Minecraft Server

A self-hosted game server for Minecraft.

## Description
It allows you to host your own Minecraft world for friends and family. It can be easily managed on TrueNAS via the official or community charts, supporting both Java and Bedrock editions.

## When to use it
- When you want a private, persistent world for multiplayer gaming.
- When you want full control over server mods, plugins, and player access.

## When not to use it
- When you only need occasional multiplayer play (use Realms or public servers).
- If your hardware lacks sufficient RAM (Minecraft servers can be resource-intensive).

## Getting started

### Docker
The most popular way to run a self-hosted Minecraft server is using the `itzg/minecraft-server` image:

```bash
docker run -d -it \
  --name minecraft-server \
  -p 25565:25565 \
  -e EULA=TRUE \
  -v /path/to/data:/data \
  itzg/minecraft-server
```

Accept the EULA by setting `EULA=TRUE`. The server will be accessible on port 25565.

## CLI examples
Interact with the server console or use the built-in RCON client:

```bash
# Access the live server console
docker attach minecraft-server

# Send a command to the server via RCON
docker exec minecraft-server rcon-cli "say Hello from the host!"

# List currently online players
docker exec minecraft-server rcon-cli "list"
```

## API examples
Use the `mcstatus` Python library to query server information:

```python
from mcstatus import JavaServer

# Lookup the server and query it
server = JavaServer.lookup("localhost:25565")
status = server.status()

print(f"The server has {status.players.online} players online and replied in {status.latency} ms")
```

## Links
- [Minecraft Official Site](https://www.minecraft.net/)

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

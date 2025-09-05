---
title: "Dedicated Servers"
order: 1
---

# Fractium Dedicated Server Setup

Welcome to the Fractium Dedicated Server setup guide. This documentation will walk you through the process of setting up and configuring your own Fractium dedicated server.

## Prerequisites

Before setting up your Fractium dedicated server, ensure you have:

- A compatible server machine (Windows/Linux)
- Minimum 4GB RAM (8GB recommended)
- 20GB free disk space
- Stable internet connection
- Administrative privileges on the server machine

## Installation Steps

### 1. Download Server Files

1. Navigate to your Steam Library
2. Go to **Tools** section
3. Search for "Fractium Dedicated Server"
4. Download and install the server files

Alternatively, you can use SteamCMD:
```bash
steamcmd +login anonymous +app_update 1234567 +quit
```

### 2. Initial Configuration

Create a server configuration file in the server directory:

**server.cfg**
```ini
# Server Basic Settings
server_name="My Fractium Server"
server_password=""
max_players=16
server_port=7777

# Game Settings
game_mode="survival"
difficulty=2
world_seed=12345

# Admin Settings
admin_password="your_admin_password_here"
```

### 3. Port Configuration

Ensure the following ports are open in your firewall:

- **7777** (UDP) - Game Port
- **7778** (UDP) - Query Port  
- **7779** (TCP) - RCON Port

### 4. Starting the Server

#### Windows
```batch
FractiumServer.exe -config=server.cfg
```

#### Linux
```bash
./FractiumServer -config=server.cfg
```

## Advanced Configuration

### Custom Maps

To use custom maps on your server:

1. Place map files in `/maps/` directory
2. Update server.cfg:
```ini
map_name="custom_map_name"
```

### Mods Support

Fractium servers support mods through the Steam Workshop:

1. Subscribe to mods in Steam Workshop
2. Add mod IDs to server.cfg:
```ini
mods=123456789,987654321
```

### Performance Optimization

For optimal server performance:

- Set `tick_rate=60` for competitive play
- Adjust `max_entities=1000` based on server specs
- Enable `auto_save=true` with `save_interval=300`

## Troubleshooting

### Common Issues

**Server won't start:**
- Check port conflicts
- Verify configuration file syntax
- Ensure proper file permissions

**Players can't connect:**
- Verify firewall settings
- Check port forwarding on router
- Confirm server is visible in server browser

**Performance issues:**
- Monitor CPU and RAM usage
- Reduce max_players if needed
- Check for resource-intensive mods

### Log Files

Server logs are located in:
- Windows: `%APPDATA%\Fractium\Logs\`
- Linux: `~/.fractium/logs/`

## Support

For additional help:
- Join our [Discord](https://discord.gg/fractium)
- Visit the [Steam Community](https://steamcommunity.com/app/fractium)
- Submit tickets at [support@twoloop.games](mailto:support@twoloop.games)

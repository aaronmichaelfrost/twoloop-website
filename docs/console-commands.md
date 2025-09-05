---
title: "Console Commands"
order: 2
---

# Console Commands

Fractium includes a powerful console system that allows players and administrators to execute various commands. Press `F1` to open the console in-game.

## Player Commands

### Basic Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `help` | Display list of available commands | `help` |
| `fps` | Show current FPS | `fps` |
| `ping` | Display network latency | `ping` |
| `time` | Show current game time | `time` |
| `weather` | Display weather information | `weather` |

### Movement & Teleportation

| Command | Description | Usage |
|---------|-------------|-------|
| `teleport` | Teleport to coordinates | `teleport 100 50 200` |
| `tp` | Teleport to another player | `tp PlayerName` |
| `spawn` | Return to spawn point | `spawn` |
| `sethome` | Set home location | `sethome [name]` |
| `home` | Teleport to home | `home [name]` |

### Inventory & Items

| Command | Description | Usage |
|---------|-------------|-------|
| `give` | Give item to player | `give iron_ore 64` |
| `clear` | Clear inventory | `clear` |
| `repair` | Repair held item | `repair` |
| `enchant` | Enchant held item | `enchant sharpness 3` |

## Admin Commands

*Note: These commands require administrator privileges*

### Server Management

| Command | Description | Usage |
|---------|-------------|-------|
| `kick` | Kick a player | `kick PlayerName [reason]` |
| `ban` | Ban a player | `ban PlayerName [reason]` |
| `unban` | Unban a player | `unban PlayerName` |
| `whitelist` | Manage whitelist | `whitelist add PlayerName` |
| `op` | Grant admin privileges | `op PlayerName` |
| `deop` | Remove admin privileges | `deop PlayerName` |

### World Management

| Command | Description | Usage |
|---------|-------------|-------|
| `save` | Save the world | `save` |
| `backup` | Create world backup | `backup [name]` |
| `restore` | Restore from backup | `restore backup_name` |
| `regenerate` | Regenerate chunk | `regenerate` |
| `setspawn` | Set world spawn point | `setspawn` |

### Game Settings

| Command | Description | Usage |
|---------|-------------|-------|
| `difficulty` | Change difficulty | `difficulty [1-4]` |
| `gamemode` | Change game mode | `gamemode survival` |
| `weather` | Control weather | `weather clear/rain/storm` |
| `time` | Set time of day | `time set 12000` |
| `gamerule` | Modify game rules | `gamerule pvp false` |

### Resource Management

| Command | Description | Usage |
|---------|-------------|-------|
| `resources` | Show server resources | `resources` |
| `entities` | List all entities | `entities` |
| `chunks` | Show loaded chunks | `chunks` |
| `memory` | Display memory usage | `memory` |
| `performance` | Show performance stats | `performance` |

## Advanced Commands

### Debugging

| Command | Description | Usage |
|---------|-------------|-------|
| `debug` | Toggle debug mode | `debug [true/false]` |
| `collision` | Show collision boxes | `collision` |
| `wireframe` | Toggle wireframe mode | `wireframe` |
| `profiler` | Start performance profiler | `profiler start` |

### Modding & Development

| Command | Description | Usage |
|---------|-------------|-------|
| `reload` | Reload configurations | `reload config` |
| `script` | Execute lua script | `script filename.lua` |
| `mod` | Manage mods | `mod enable ModName` |
| `workshop` | Steam Workshop commands | `workshop update` |

## Command Aliases

Many commands have shorter aliases for convenience:

- `tp` → `teleport`
- `gm` → `gamemode`
- `w` → `weather`
- `t` → `time`
- `r` → `reload`

## Command Permissions

Commands are organized into permission levels:

1. **Guest** - Basic player commands (help, fps, ping)
2. **Player** - Standard commands (teleport, home, give)
3. **Moderator** - Limited admin commands (kick, mute)
4. **Admin** - Full server control
5. **Owner** - Complete access including dangerous commands

## Tips

- Use `Tab` for command auto-completion
- Commands are case-insensitive
- Use quotes for arguments with spaces: `kick "Player Name" "reason here"`
- Many commands support partial player name matching
- Use `history` to see your recent commands

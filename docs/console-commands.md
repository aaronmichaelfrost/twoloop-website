---
title: "Console Commands"
order: 2
---

# Console Commands

Fractium includes a powerful console system that allows players and administrators to execute various commands. Press `F1` to open the console in-game.

Commands marked with **[admin]** require administrator or moderator privileges. Commands marked with **[server only]** only run on dedicated server builds.

---

## General Commands

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `help` | Shows list of console commands | `help` | No |
| `usage` | Explains how to use a command and the expected format | `usage <command_id>` | No |
| `loglevel` | Changes the game console's logging level minimum. 1 = Log everything, 2 = Log only warnings/assertions/errors/exceptions, 3 = Log only errors and exceptions | `loglevel <int>` | No |
| `gamescene` | Sets the game scene to load | `gamescene <int>` | Yes |

---

## Player Commands

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `kill` | Kill yourself | `kill` | No |
| `combatlog` | Print recent damage taken | `combatlog` | No |
| `listplayers` | Lists all players in the game and their SteamIDs | `listplayers` | No |

---

## Inventory & Items

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `give` | Gives your player a stack of an item | `give <item_name> <quantity (default maxStackSize)>` | Yes |
| `giveto` | Gives a particular player an item | `giveto <steamid> <item_name> <quantity (default maxStackSize)>` | Yes |
| `giveall` | Give all players an item | `giveall <item_name> <quantity (default maxStackSize)>` | Yes |
| `kit` | Gives you a starter kit for testing | `kit` | Yes |

---

## Movement & Camera

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `teleport` | Teleports a player to another player | `teleport <destination_player_steamID> <optional_source_player_steamID>` | Yes |
| `noclip` | [moderator only] Toggles whether you're flying or not | `noclip` | Yes |
| `noclipspeed` | Sets noclip speed | `noclipspeed <float>` | Yes |
| `noclipacceleration` | Sets noclip acceleration | `noclipacceleration <float>` | Yes |
| `flytest` | Toggle flying through tiles | `flytest` | Yes |
| `speed` | [moderator only] Sets the speed of the local player | `speed <float>` | Yes |
| `freecam` | Toggles free cam mode | `freecam` | Yes |
| `setfov` | Sets the fov of Camera.main | `setfov <float>` | No |
| `setviewfov` | Sets the field of view of your gun or tool | `setviewfov <float>` | No |

---

## UI & Display

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `fps` | Toggles fps counter | `fps` | No |
| `hud` | Turn on / off UI | `hud <1 or 0>` | No |
| `clear` | Clears the console | `clear` | No |
| `crosshaircolor` | Sets crosshair color. Accepted values: `0-255,0-255,0-255`, `red`, `orange`, `yellow`, `green`, `blue`, `magenta`, `white` | `crosshaircolor <string>` | No |
| `crosshairmove` | Make crosshair follow rotation of gun | `crosshairmove <int>` | No |
| `showaimcone` | Visualizes the aimcone | `showaimcone` | Yes |
| `hideaimcone` | Stops visualizing the aimcone | `hideaimcone` | Yes |
| `pointeralwaysShow` | Forces the pointer to always be visible | `pointeralwaysShow <int>` | No |

---

## Game Settings

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `difficulty` | Sets difficulty in minutes | `difficulty <int>` | Yes |
| `difficultypause` | Pauses difficulty scaling with time | `difficultypause <int>` | Yes |
| `difficultydebug` | Enables/disables difficulty debugger | `difficultydebug <int>` | No |
| `friendlyfire` | Only works on player hosted games if you are the host | `friendlyfire` | Yes |
| `ammoinfinite` | Makes reloads not use ammo | `ammoinfinite <int>` | Yes |
| `god` | Sets invincibility | `god <int>` | Yes |
| `cheats` | Allows everyone to use cheats without requiring them to be admins | `cheats <int>` | Yes |
| `infinitebuild` | Allows building without resources | `infinitebuild <int>` | Yes |
| `fog` | Show or hide fog | `fog <1 or 0>` | Yes |
| `skyboxspeed` | Change speed of day night cycle | `skyboxspeed <int>` | Yes |

---

## World / Island

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `islandseed` | (host/server only) Forces the island seed for all future island generations. Set to 0 to disable | `islandseed <int>` | Yes |
| `islandbiome` | (host/server only) Forces the biome for the next starting island generation | `islandbiome <int>` | Yes |

---

## Visibility

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `visglobal` | [moderator only] Sets the visibility mode of the local player for all clients. 0: invisible, 1: visible, 2: shadows only | `visglobal <int>` | Yes |
| `vislocal` | Sets the visibility mode of the player on the local client. 0: invisible, 1: visible, 2: shadows only | `vislocal <int>` | Yes |

---

## Moderation

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `listadmins` | Lists all players that are admins / moderators for your machine's game server | `listadmins` | Yes |
| `listbannedplayers` | Lists all banned players for your machine's game server | `listbannedplayers` | Yes |
| `banid` | [moderator only] Bans the user with the given Steam ID | `banid <ulong>` | Yes |
| `banname` | [moderator only] Bans the first found user with this steam name | `banname <string>` | Yes |
| `unbanid` | [moderator only] Unbans the user with the given Steam ID | `unbanid <ulong>` | Yes |
| `unbanname` | [moderator only] Unbans the first found user with this steam name | `unbanname <string>` | Yes |
| `modid` | [moderator only] Adds a server moderator by Steam ID | `modid <ulong>` | Yes |
| `modname` | [moderator only] Adds a server moderator using the first found user with this steam name | `modname <string>` | Yes |
| `unmodid` | [moderator only] Removes a server moderator by Steam ID | `unmodid <int>` | Yes |
| `unmodname` | [moderator only] Removes a server moderator using the first found user with this steam name | `unmodname <string>` | Yes |
| `kickid` | [moderator only] Kicks the player from the session | `kickid <ulong>` | Yes |
| `kickname` | [moderator only] Kicks the player from the session | `kickname <string>` | Yes |
| `killall` | Kill every player | `killall` | Yes |
| `clearviolations` | [moderator only] Clears all antihack violation scores | `clearviolations` | Yes |
| `listviolations` | Lists all players and their violation scores | `listviolations` | Yes |

---

## Networking

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `connect` | Connects you to a game server, if you are not currently in a game | `connect 91.229.114.17` | No |

---

## Cosmetics

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `randomize_cosmetics` | Randomizes cosmetics for all players | `randomize_cosmetics` | Yes |

---

## Dedicated Server Only

These commands are only available on dedicated server builds.

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `togglesteamauth` | [dedicated server only] Toggles checking connecting clients for valid Steam accounts. Default is enabled. Disable for stress testing | `steamauthtoggle` | Yes |
| `debug` | Debug.logs a message on the server's client only | `debug <string>` | Yes |
| `serverinfo` | Logs current server information | `serverinfo` | Yes |

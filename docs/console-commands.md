---
title: "Console Commands"
order: 2
last_updated: "April 21, 2026"
---

# Console Commands

Fractium includes a powerful console system that allows players and administrators to execute various commands. Press `F1` to open the console in-game.

Commands marked with **[admin]** require administrator or moderator privileges. Commands marked with **[server only]** only run on dedicated server builds.

---

## General Commands

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `help` | Shows list of console commands | `help` | No |
| `usage` | Explains how to use a command and the expected format. | `usage <command_id>` | No |
| `gamescene` | sets the game scene to load. options are: | `gamescene <int>` | Yes |
| `loglevel` | changes the game console's logging level minimum. 1 - Log everything 2 - Log only warnings, assertions, errors and exceptions 3 - Log only errors and exceptions | `loglevel <int>` | No |

---

## Player Commands

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `listplayers` | Lists all players in the game and their SteamIDs. | `listplayers` | No |
| `combatlog` | Print recent damage taken. | `combatlog` | No |
| `kill` | kill yourself | `kill` | No |

---

## Inventory & Items

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `giveto` | Gives a particular player an item | `giveto <steamid> <item_name> <quantity (default maxStackSize)>` | Yes |
| `giveall` | Give all players an item | `giveall <item_name> <quantity (default maxStackSize)>` | Yes |
| `give` | Gives your player a stack of an item | `give <item_name> <quantity (default maxStackSize)>` | Yes |
| `kit` | Gives you a starter kit for testing. | `kit` | Yes |

---

## Movement & Camera

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `teleport` | Teleports a player to another player. | `teleport <destination_player_steamID> <optional_source_player_steamID>` | Yes |
| `freecam` | Toggles free cam mode Debug Camera Control Guide: Alpha1: Increase Depth of Field Focus Distance Alpha2: Decrease Depth of Field Focus Distance Alpha3: Toggle Chromatic Aberration On/Off Alpha4: Toggle Color Curves (Shadows, Midtones, Highlights) On/Off Alpha5: Increase Motion Blur Intensity Alpha6: Decrease Motion Blur Intensity | `freecam` | Yes |
| `setfov` | Sets the fov of Camera.main. use set_fov <any positive number> | `setfov <float>` | No |
| `speed` | [moderator only] Sets the speed of the local player. | `speed <float>` | Yes |
| `noclip` | [moderator only] Toggles whether you're flying or not. | `noclip` | Yes |
| `setviewfov` | Sets the field of view of your gun or tool. | `setviewfov <float>` | No |
| `noclipspeed` | sets noclip speed | `noclipspeed <float>` | Yes |
| `noclipacceleration` | sets noclip acceleration | `noclipacceleration <float>` | Yes |
| `flytest` | toggle flying through tiles | `flytest` | Yes |

---

## UI & Display

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `clear` | Clears the console | `clear` | No |
| `fps` | Toggles fps counter | `fps` | No |
| `showaimcone` | Visualizes the aimcone. | `showaimcone` | Yes |
| `hideaimcone` | Stops visualizing the aimcone. | `hideaimcone` | Yes |
| `crosshaircolor` | Accepted values: 0-255,0-255,0-255, red, orange, yellow, green, blue, magenta, white | `crosshaircolor <string>` | No |
| `pointeralwaysShow` |  | `pointeralwaysShow <int>` | No |
| `crosshairmove` | Make crosshair follow rotation of gun | `crosshairmove <int>` | No |
| `hud` | turn on / off UI | `hud <1 or 0>` | No |

---

## Game Settings

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `difficulty` | sets difficulty in minutes | `difficulty <int>` | Yes |
| `difficultypause` | pauses difficulty scaling with time | `difficultypause <int>` | Yes |
| `difficultydebug` | enables/disables difficulty debugger | `difficultydebug <int>` | No |
| `ammoinfinite` | makes reloads not use ammo | `ammoinfinite <int>` | Yes |
| `friendlyfire` | Only works on player hosted games if you are the host. | `friendlyfire` | Yes |
| `fog` | show or hide fog | `fog <1 or 0>` | Yes |
| `skyboxspeed` | change speed of day night cycle | `skyboxspeed <int>` | Yes |
| `infinitebuild` | allows building without resources | `infinitebuild <int>` | Yes |
| `cheats` | allows everyone to use cheats without requiring them to be admins | `cheats <int>` | Yes |
| `god` | Sets invincibility. | `god <int>` | Yes |

---

## World / Island

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `islandseed` | (host/server only) Forces the island seed for all future island generations. Set to 0 to disable. | `islandseed <int>` | Yes |
| `islandbiome` | (host/server only) Forces the biome for the next starting island generation. Valid types are: {string.Join(, Enum.GetValues(typeof(IslandManager.BiomeOption)).Cast<IslandManager.BiomeOption>().Select(v => ((int)v) + + v.ToString()))} | `islandbiome <int>` | Yes |

---

## Visibility

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `visglobal` | [moderator only] Sets the visiblity mode of the local player for all clients. 0: invisible, 1: visible, 2: shadows only | `visglobal <int>` | Yes |
| `vislocal` | Sets the visiblity mode of the player on the local client. 0: invisible, 1: visible, 2: shadows only | `vislocal <int>` | Yes |

---

## Moderation

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `listadmins` | Lists all players that are admins / moderators for your machine's game server. | `listadmins` | Yes |
| `listbannedplayers` | Lists all banned players for your machine's game server. | `listbannedplayers` | Yes |
| `banid` | [moderator only] Bans the user with the given steam id | `banid <ulong>` | Yes |
| `banname` | [moderator only] Bans the first found user with this steam name, be careful using this. | `banname <string>` | Yes |
| `modid` | [moderator only] Adds a server moderator by steamid. | `modid <ulong>` | Yes |
| `modname` | [moderator only] Adds a server moderator using the first found user with this steam name, be careful using this. | `modname <string>` | Yes |
| `unbanid` | [moderator only] UnBans the user with the given steam id | `unbanid <ulong>` | Yes |
| `unbanname` | [moderator only] UnBans the first found user with this steam name, be careful using this. | `unbanname <string>` | Yes |
| `unmodid` | [moderator only] Removes a server moderator by steamid. | `unmodid <int>` | Yes |
| `unmodname` | [moderator only] Removes a server moderator using the first found user with this steam name, be careful using this. | `unmodname <string>` | Yes |
| `kickid` | [moderator only] Kicks the player from the session | `kickid <ulong>` | Yes |
| `kickname` | [moderator only] Kicks the player from the session | `kickname <string>` | Yes |
| `clearviolations` | [moderator only] Clears all antihack violation scores. | `clearviolations` | Yes |
| `listviolations` | Lists all players and their violation scores. | `listviolations` | Yes |
| `killall` | kill every player | `killall` | Yes |

---

## Networking

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `connect` | Connects you to a game server, if you are not currently in a game. | `connect 91.229.114.17` | No |

---

## Cosmetics

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `randomize_cosmetics` | Randomizes cosmetics | `randomize_cosmetics` | Yes |

---

## Dedicated Server Only

| Command | Description | Format | Admin Only |
|---------|-------------|--------|------------|
| `togglesteamauth` | [dedicated server only] Toggles checking connecting clients for valid Steam accounts. Default is enabled. Disable for stress testing. | `steamauthtoggle` | Yes |
| `debug` | Debug.logs a message on the server's client only | `debug <string>` | Yes |
| `serverinfo` | Logs current server information | `serverinfo` | Yes |

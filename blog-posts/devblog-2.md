---
date: 2025-09-07
title: Devblog 2
description: Two weeks of polish, stress testing, and major infrastructure improvements.
---

# Devblog 2

Two weeks of polish, stress testing, and major infrastructure improvements.

### CONSOLE COMMANDS OVERHAUL
*by Aaron*

We've completely revamped the console system. App startup args now double as F1 console commands, making server configuration much more flexible. Server owners can now automatically apply console commands on startup.

Added a suite of new admin commands including:
- Island biome forcing
- Island seed control  
- Steam auth toggling for stress testing
- Inventory management (`giveto`, `giveall`, `give`)
- Player management (`listplayers`, teleportation)
- Combat utilities (`kit` command for pistol and ammo)

The system now includes autocompletion for dynamic arguments like Steam IDs and item names, plus a `usage` command to explain how to use specific commands.

### WORLD GENERATION FIXES

Fixed a critical world generation indeterminism issue. Worlds now generate exclusively on the server/host and are transmitted to clients as byte arrays, ensuring all players see identical terrain.

This also resolved the annoying bug where players would spawn mid-air with broken maps because the server wasn't properly communicating world type.

### STRESS TESTING SUCCESS

We've achieved some major milestones:
- **25 players** running around randomly ✓
- **250+ NPCs** with 3 real players and 800 inventory items on the ground ✓

The game maintained massive stability even during destruction scenarios.

### ANTI-HACK IMPROVEMENTS

Enhanced the anti-hack system with:
- Configurable enforcement levels (kick/ban)
- Violation score thresholds
- Discord alerts for violations
- Score decay system (default 50 per minute)
- Better melee line-of-sight verification logging

Anti-hack enforcement is automatically disabled when cheats are enabled for development.

### VOICE CHAT UPGRADES

Completely overhauled voice chat:
- Switched from 2D to 3D audio sources
- Improved volume rolloff
- Proximity-based networking (only sends voice data to nearby players)
- Better integration with P2P transport for Unity editor debugging

### UI AND UX POLISH

Multiple quality-of-life improvements:
- Inventory automatically closes on death
- Fixed input locking when dying with map open
- Added resolution selector
- Popup dialogs explain kick reasons
- Streamer mode to hide session names
- Fixed F3 revive utility teleportation bug

### MOVEMENT REFINEMENTS

Smoothed out the jittery first-person ladder climbing experience and restricted horizontal velocity during climbs for more realistic movement.

### COMBAT BALANCE

- Combat logs now only send to involved players for better performance
- Attacking entities cancels gradual healing buffs, making medkits less overpowered
- Turned off team chat feature temporarily

### WEBSITE DEVELOPMENT

Made significant progress on the web presence:
- Created a new landing page
- Revamped the blog system
- Added comprehensive documentation pages

### WHAT'S NEXT

With the core systems stabilized and stress testing successful, we're moving toward more content and polish phases. The foundation is solid for scaling up player counts and adding more gameplay features.

## CHANGELOG

**8/24/2025**
◦ app startup args now double as F1 console commands (this allows server owners and players to automatically apply existing console commands on startup)
◦ added console command for forcing island biome
◦ added console command for forcing island seed
◦ added console command for toggling steam auth. This is useful for stress testing with fake clients.
◦ fixed bug where you spawn in mid-air and the map doesn't work because the server didn't tell you you were in procedural world and not flat world.
◦ fixed bug where you have your map open when you die it locks your input when you respawn
◦ made it so your inventory closes automatically when you die.
◦ fixed F3 revive dev utility which was teleporting you to the middle of nowhere
◦ turned off TEAM chat feature, for now
◦ fixed issue where text chat name color for player was black

**8/25/2025**
◦ smoothed out jittery first person ladder climb and restricted horizontal velocity
◦ make server only send combat logs to involved players
◦ added "kit" admin command to give pistol and ammo
◦ fixed voice chat to use 3D audio source instead of 2D
◦ finalized P2P transport for Unity editor playmode in UNITY_SERVER. This makes it easier to debug 
◦ Improve player voice chat volume rolloff
◦ Only network voice chat bytes to players in proximity

**8/26/2025**
◦ fixed world generation indeterminism. worlds now generate on the server/host only and are sent to the clients as a byte[]

**8/27/2025**
◦ improve antihack logging on melee LOS verification
◦ Fixed console spawn menu to use client look direction
◦ Add server command line args "antihack.enforcementlevel" (kick,ban), and "antihack.maxviolation" (score threshold), and Discord alerts for violations

**8/28/2025**
◦ first successful stress test with 25 players running around randomly

**8/29/2025**
◦ successful stress test with 250+ NPCS, 3 real players, 800 inventory items on the ground, massive stability / destruction

**8/30/2025**
◦ Add antihack violation score decay using arg "-antihackdecaypermin" (default 50)
◦ don't enforce server antihack when cheats are enabled

**9/1/2025**
◦ added console commands to give inventory items: giveto, giveall, give --> using <steamID> and <itemName> and optional <quantity>
◦ added console command to list players in the session "listplayers"
◦ added autocompletions for dynamic enumerable command arguments like steamID and item name.
◦ added console command to teleport to a specific player.
◦ added 'usage' command to explain how to use a specific console command
◦ Attacking entities cancels gradual healing buffs so medkits are less OP
◦ added popup dialog to tell you why you got kicked
◦ Added streamer mode to hide session name

**9/2/2025**
◦ added resolution selector

**9/3/2025**
◦ made a landing page and revamped the old blog

**9/4/2025**
◦ added documentation page to new game site

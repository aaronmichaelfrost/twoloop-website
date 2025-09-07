---
date: 2025-09-07
title: Devblog 2
description: Two weeks of polish, stress testing, and major infrastructure improvements.
---

# Devblog 2

Got less done than we wanted, but steady progress continues.

### SUCCESSFUL STRESS TEST
*by Aaron*

We ran a smooth test with **800 items** (with rigidbodies), **250 NPCs** (aggroed), and **25 player connections**. Next, with 250 players.

The goal is to prove systems scale. I wrote a script that runs headless clients in parallel, which maxed my CPU usage at 25 connections. That's 25 fully generated 700x700 terrains and full player loops running on only one computer. I also connected a low-spec laptop with graphics enabled to check real client perf. Next, we’ll rent machines to aim for 250 players. The server held up great—only slowing past 300 NPCs, which is fine since NPC loops are server-heavy and 300 is worst worst case.

It looked suitably chaotic, we'll share some footage soon.

#### Implemented
✔️ move, sprint, jump, crouch, shoot, melee  
✔️ look up/down  
✔️ reload  
✔️ receive loot 
✔️ text chat 

#### In progress
◦ spam transfer loot slots
◦ voice chat  
◦ open chests, craft, build  
◦ rocket building destruction  
◦ loot spill
◦ crowded/dispersed groups  
◦ PvP firing  
◦ all of above on flatworld & procedural  

### ROCKS
*by Rylan*

Something cool here with a screenshot?

### COMMANDS
*by Aaron*
F1 console got a revamp:  
◦ More autocompletions, more commands (see changelog)
◦ `usage` command to explain others  
◦ Startup args also usable as console commands  
◦ Multi-argument support  

### WORLD GEN FIXES
Unlike Minecraft/Rust, worlds now generate only on the server/host and sync to clients as byte arrays. This avoids desync issues but removes reliable seed regen (e.g. for machinima replays).

### ANTI-HACK IMPROVEMENTS
Updates include:  
◦ Configurable enforcement (kick/ban)  
◦ Violation thresholds & decay  
◦ Discord alerts  
◦ Pop-up explaining kicks  

We tested kicks ourselves. All good.  

### NEW WEBSITE
Soon this will host the wiki and server docs. They're placeholder for now.

Pages are generated from markdown, and GitHub commits auto-deploy it; very efficient.

### PROJECT PLANNING
We’ve found lots of bugs and are talking about a different art style possibly.

### WHAT'S NEXT
◦ More stress tests  
◦ Finish EAC integration  
◦ Bug fixes  

## CHANGELOG

**8/24/2025**
◦ Startup args double as console commands  
◦ Added `forceislandbiome`, `forceislandseed`, `togglesteamauth`  
◦ Fixed mid-air spawn bug (procedural vs flatworld)  
◦ Fixed respawn input lock with map open  
◦ Inventory now auto-closes on death  
◦ Fixed `F3 revive` teleport bug  
◦ Disabled TEAM chat  
◦ Fixed black name color in chat  

**8/25/2025**
◦ Smoothed ladder climb, limited horizontal velocity  
◦ Combat logs sent only to involved players  
◦ Added `kit` admin command (pistol & ammo)  
◦ Fixed voice chat to use 3D audio  
◦ Finalized P2P transport for Unity editor playmode (`UNITY_SERVER`)  
◦ Improved voice volume rolloff & proximity networking  

**8/26/2025**
◦ Fixed worldgen indeterminism (server-only, sent as `byte[]`)  

**8/27/2025**
◦ Improved anti-hack logging on melee LOS  
◦ Console spawn menu now uses look direction  
◦ Added server args: `antihack.enforcementlevel` (kick/ban), `antihack.maxviolation` (threshold), Discord alerts  

**8/28/2025**
◦ First stress test with 25 players  

**8/29/2025**
◦ Stress test: 250+ NPCs, 3 players, 800 items, full stability  

**8/30/2025**
◦ Added violation score decay (`-antihackdecaypermin`, default 50)  
◦ Anti-hack bypassed when cheats enabled  

**9/1/2025**
◦ Added `giveto`, `giveall`, `give` (with `steamID itemName quantity` args)  
◦ Added `listplayers`  
◦ Autocompletions for dynamic args (steamID, itemName)  
◦ Added `teleport` to player  
◦ Added `usage` for command help  
◦ Attacking cancels gradual healing buffs  
◦ Pop-up shows kick reason  
◦ Added streamer mode to hide session name

**9/2/2025**
◦ Added resolution selector in settings

**9/3/2025**
◦ Made a landing page and revamped the old blog

**9/4/2025-9/7/2025**
◦ Wrapped up this website

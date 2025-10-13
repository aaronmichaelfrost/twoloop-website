---
date: 2025-10-12
cover-image: devblog3-images/devblog3-cover.png
title: Devblog 3
description: Bug fixes, commands, & antihack
---

# Devblog 3

Bug fixes, commands, & antihack

### Life Update
*by Aaron*

After two years of work at Blizzard as a SWE, I've resigned so I can focus my efforts on Fractium now, full time. This update is on the lighter side as I've had to move apartments, again, too.

The past two weeks I tackled a number of critical bugs, security/antihack things, and QoL. Going to get some more momentum going now that life is a little more stable. 


### Cinema Camera

There is a console command `freecam` that server admins can use to noclip around the world.

In this update I added cinematic camera shake, entity tracking with projected velocity, and a lot of other controls. We'll use this to make trailers, eventually.

![Cinema Camera 1](devblog3-images/cinema1.gif)
![Cinema Camera 2](devblog3-images/cinema2.gif)


### Bugs

Working on a project like this, there are a variety of contexts systems must handle:
* Standalone build vs. editor
* Steam P2P vs. Dedicated vs. non-steam transport (ex. ParrelSync/Singleplayer)
* Procedural world vs. dev world
* UNITY_SERVER vs. !UNITY_SERVER
* Local player vs. remote player vs. host player

Fractium supports all of these contexts. For some reason our networking library seems to execute callbacks in a different order in the editor vs. build. So we now handle that. I also fixed an issue with managed stripping preventing our AI from loading due to stripping assembly types that were only referened via reflection. 

I fixed a ton of bugs this week. We are down to 1 critical bug. I aim to keep the critical bugs to zero moving forwards.

I also set up ParrelSync properly so I can easily fix bugs with Hot Reload on one machine.

![ParrelSync Setup](devblog3-images/parrelsync.png)


### Movement Antihack

I wrote some server modules that verify 3 things:
* groundedness (flyhack protection)
* speed 
* collision (noclip protection)

I tested each of these by simulating clientside cheats, and they indeed work and the game will kick players for moving too fast, jumping too high / floating, or phasing through walls. This works within the antihack violation scoring system I built in the previous update.


### More Console Commands

◦ `-fresh` - for dedicated servers, forces new world data 
◦ `listbannedplayers` - prints list of banned users to console
◦ `listadmins` - prints list of admins to console
◦ `clearviolations` - clears antihack violation scores for all players
◦ `connect` - connects to a server by IP without using the server browser


### Entity Debugger

If you are an admin in a dev build you can press H to get a debug view of entities.

![Entity Debug View](devblog3-images/entitydebug.png)


## CHANGELOG

**9/28/2025**
◦ Added debugging overlay for cinematic / free camera  
◦ Smoothed cinematic camera movements  
◦ Cinematic camera shake strength control  
◦ Added speed controls for cinematic / free camera  
◦ Refactored console command system for streamlined admin checking & execution context validation  

**9/29/2025**
◦ Entity tracking and DoF using ctrl + scroll  
◦ Added a temporary soundtrack and soundtrack system  

**10/1/2025**
◦ Added more security logging  
◦ Refactored some networking code for readability  
◦ Removed purple fog that was floating around in the sky  
◦ Ensure clients don't begin island gen until server finishes  
◦ Added "find text in scene" tool  
◦ Fixed input hint bugs - a layout issue and it now shows C - CONSUME instead of default for medkit  

**10/2/2025**
◦ Restored some missing AI stat data causing enemies to idle  
◦ Add cons. cmd to connect to server by IP  
◦ Fixed certain projectiles like rockets not spawning when created by non-local players  

**10/3/2025**
◦ Reduced player knockback which was 10x too high  
◦ Fixed occasionally invisible settings button from UI tween issue  
◦ Add connection timeout popup instead of only logging error  
◦ Fixed local host networking so ParrelSync now works correctly  
◦ Don't show XP popup anymore. we don't have an XP system.  
◦ Fixed player floating above corpse during respawn  
◦ Fixed player visible before being alive on first spawn in  
◦ Fixed player footstep sounds not broadcasting to remote clients  

**10/4/2025**
◦ Fixed door sound distance which was too high  
◦ Client timeout w/popup if server world generation does not complete in 15s  
◦ Prevent joining games with version mismatch  
◦ Add -fresh command line argument to force new world data for dedicated servers  
◦ Add listbannedplayers server-only console command to show a list of banned players  
◦ Add listadmins server-only console command to show a list of admins/mods  
◦ Add console command to reset antihack: clearviolations  
◦ Created a popup warning user if machine is not connected to the internet when they refresh server browser  
◦ Add console command to list violation scores for each player "listviolations"  
◦ Added serverside fly hack protection  
◦ Added serverside speed hack protection  
◦ Added serverside noclip hack protection  
◦ Tested all three with simulated clientside "hacks"  

**10/6/2025**
◦ Show server age in browser and pause GUI  
◦ Remove player body decals like blood on respawn  
◦ Fixed movement interpolation for rendering remote players who have low FPS  
◦ Ensure weapon flashlight is centered/aligned with camera for local player  
◦ Fixed oversized casing shells ejected on player world pistol  

**10/7/2025**
◦ Fixed UI initialization issues on standalone build  
◦ Added a debug view mode for development builds (hold H while looking at entity)  

**10/8/2025**
◦ Fixed bug with managed stripping preventing AI from loading due to assembly types only referenced via reflection
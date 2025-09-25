---
date: 2023-04-15
cover-image: devblog0-images/2.png
title: Devblog 0
description: Proc gen islands, bases, building, and more
---

# Devblog 0

We're ditching co-op gameplay and exploring more world generation and PvP.

### NEW GAME NAME
*by Aaron*

**Fractium!**

![New Game Name](devblog0-images/new_game_name.png)

For the past few months, I've been working extremely hard on Fractium outside of my comp sci classes.

<div class="discord-images-row">
![New HUD 1](devblog0-images/fps_1.png)
![New HUD 2](devblog0-images/fps_2.png)
![New HUD 3](devblog0-images/fps_3.png)
<div class="discord-images-row">


### NICE PICS

<div class="discord-images-row">
![1](devblog0-images/1.png)
![2](devblog0-images/2.png)
</div>

<div class="discord-images-row">
![3](devblog0-images/3.png)
![4](devblog0-images/4.png)
</div>

<div class="discord-images-row">
![5](devblog0-images/5.png)
![6](devblog0-images/6.png)
</div>

<div class="discord-images-row">
![7](devblog0-images/7.png)
![8](devblog0-images/8.png)
</div>

### PROCEDURAL WEAPONS

The HUD for a single procedural weapon. We capture a render texture and cache it off. We use this same image for the kill feed when a player kills another player.

![Weapon HUD](devblog0-images/item_hover_hud.png)

This is an inventory filled with procedural guns. The pistols are currently untextured. We now generate attachments onto the guns too.

![Procedural Guns Inventory](devblog0-images/proc_guns.png)

This is the inventory with a procedural gun (ignore the transparent text in the background, I took this screenshot while I had a mock overlay over the actual Unity UI)

![Inventory with Gun](devblog0-images/inventory_gun.png)

### 3D PRINTED PROCEDURAL GUNS

I wrote a script that converts the Unity gameobject hierarchy to a printable .stl file! This is cool for procedural guns and could be used as promotional content / collectibles.

![3D Printed Guns](devblog0-images/3d_print.png)

### PROCEDURAL BASES

We actually have a very polished interface for base building. Not shown here...

This system is extremely versatile, and these are just some of the bases I generated in one day. There is an entire system for generating these fully destructible bases inhabited by bandits. They have loot and other interactables in them. Too bad we don't have a full time game designer to take advantage of this!

<div class="discord-images-row">
![Procedural Building 1](devblog0-images/procgen_building_0.png)
![Procedural Building 2](devblog0-images/procgen_building_1.png)
![Procedural Building 3](devblog0-images/procgen_building_2.png)
</div>

![Procedural Buildings Overview](devblog0-images/procgen_buildings.png)

### DEPLOYABLES

There are several deployables at the moment: furnace, locker (basically a tool cupboard like in Rust), bed (for respawning), workbench (for crafting guns), and autoturret.

![Deployables](devblog0-images/deployables.png)

![Workbench](devblog0-images/workbench.png)

### COMBAT LOG COMMAND

![Combat Log](devblog0-images/combat_log.png)

### ISLAND GENERATION

<div class="discord-images-row">
![Island Generation 1](devblog0-images/island1.gif)
![Island Generation 2](devblog0-images/island2.gif)
</div>

### MAP UI

![Map GUI](devblog0-images/map_gui.png)

### MINIMAP

![Minimap](devblog0-images/mmap.gif)

### CLIFF ROCKS

Rylan came up with some awesome ideas for the cliff rocks. This is an old screenshot but now they actually rotate to match the slope of the terrain and climb up until they align! More info in the unfinished devlog at the top of this page.

![Cliff Rocks](devblog0-images/cliff_rocks.png)

### NEW HUD

![New HUD 4](devblog0-images/fps_4.png)

### NEW SETTINGS PAGE AND INVENTORY

![New Settings Menu](devblog0-images/new_settings_menu.png)

![Inventory](devblog0-images/inventory.png)


## CHANGELOG

**9/20/2022**
◦ Recoil rotation reliably resets  

**9/22/2022**
◦ Movement acceleration & camera rotation tuning  
◦ Console autocomplete & durability command  
◦ Spawn-menu polish; headshot kill sounds  
◦ Sprint cancels on shot; UI hover tweaks  

**9/23/2022**
◦ Melee sensitivity curve; revive bug fixed  
◦ Camera lean while strafing; network cleanup  

**9/24/2022**
◦ Melee charging system (damage/knockback/FOV curves)  
◦ Gun/FOV tweaks; laser/trail spawn fixes  

**9/29/2022**
◦ Look-blend & crouch pose rework; melee hit projection  

**10/1/2022**
◦ Unity update, gameplay telemetry, perf & build fixes  

**10/3/2022**
◦ Water shader; Steam post-build upload pipeline  

**10/6/2022**
◦ HDRP → URP conversion; wide shader/material fix pass  

**10/9–10/10/2022**
◦ Lighting, skybox, VFX, dynamic occlusion & bug fixes  

**10/21–10/22/2022**
◦ Recoil and outline shader tweaks; lighting fixes  

**11/18–11/30/2022**
◦ UI 3.0 work; new ragdoll tech v2 and tweaks  

**1/23/2023**
◦ Level streaming; navmesh generation; cave entrance monument  
◦ Worldgen assets prefabbed  

**1/28–1/31/2023**
◦ Dedicated server build tooling, FTP & automated compression  
◦ Server console stability; build stripping setup  

**1/29–1/30/2023**
◦ Client projectile rockets, FX/sound; rockets explode on despawn  

**2/2–2/3/2023**
◦ Server browser & paging; server console QoL  

**2/5/2023**
◦ Version check in authenticator; main menu/news panels; UI polish  

**2/8–2/9/2023**
◦ Base building & raiding; feedback collector & success indicator  

**2/10–2/11/2023**
◦ Island spawn points; dedicated/net serialization fixes  
◦ Tile island connections; hierarchy cleanup  

**2/12–2/14/2023**
◦ Asset validation, fog tuning, many scene/build fixes  
◦ Dedicated fixes; deterministic generation restored  

**2/15/2023**
◦ Base stability finished (recursive destruction); optimization pass  

**2/17–2/20/2023**
◦ Distance-interest management; Teams system (creation, auth, UI)  
◦ Doors; custom network animators; passwords fix  

**2/23/2023**
◦ Modular turret WIP  

**3/3–3/7/2023**
◦ Recoil reset fixes; turret reloads, laser sight & targeting  
◦ Bandit AI aim/fire endpoint fixes  

**3/8–3/11/2023**
◦ Proc-gen bases WIP → working; deployable logic & anti-intersect  
◦ Teams & factions; beds; windows/stairs  
◦ Base editor; deployable rotation (R); MP fixes  
◦ Bandits use windows; NPC ground detection; optimizations  

**3/12/2023**
◦ No-build zones; numerous bug/build fixes  

**3/19–3/22/2023**
◦ Crafting UI (WIP → done); 3D item/attachment inspectors  
◦ Remote inventory, workbench UI, refinery & gunbench deployables  

**3/23/2023**
◦ Dedicated server fixes; new Squads main-menu UI  

**3/28–3/31/2023**
◦ Scoreboard/killfeed integration; large maps; respawn UI tip  

**4/1–4/4/2023**
◦ Deployables (beds/refinery/locker/workbench) finished  
◦ Build-mode command; melee charge cancel; decal & tool fixes  

**4/5/2023**
◦ Conquest sites finished; squadmates map UI; shorter intermission  

**4/6/2023**
◦ Objective capture HUD; entity spawn mgmt; turrets/minimap fixes  

**4/10/2023**
◦ New monuments & LODs; working ladders  
◦ Loot tables (T1–T3); harvestable monolith  

**4/12/2023**
◦ Deadly fog nerf; default melee keybind ‘Q’; more bandit chests  
◦ Lightning/navmesh/flashlight fixes  

**4/18–4/20/2023**
◦ Big perf improvements; instanced rocks; bugfix marathons  
◦ Island-gen overhaul; minimap hex overlay; ammo drop rule tweak  
◦ MSAA enabled; proc base foundations above grass  

**4/21–4/22/2023**
◦ Island generation updates; island height increased; rock work  

**4/24/2023**
◦ New desert/forest textures; cliff-rock slope-match fixes  

**4/25–4/26/2023**
◦ Build/versioning & mesh-combine fixes; crash fix  
◦ Allow client version > server on query/auth  
◦ Build-tools menu; fast sprint-pose lerp; dedicated build fixes  

**4/29–5/4/2023**
◦ Terrain blending; splat map pipeline; vegetation system fixes  

**6/23–6/24/2023**
◦ Ground/chest interaction fixes; cargo plane model/networking  
◦ Relative movement & WIP double islands  

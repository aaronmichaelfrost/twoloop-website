---
date: 2026-05-12
cover-image: devblog4-images/world_running_on_fully_automated_provision_pipeline.png
title: Devblog 4
description: Bugs hit zero, two new deployables ship, and the world boots with one click.
---

# Devblog 4

Two new deployables. Zero bugs. One click world deployment.

### 🏗️ One-Click World Deployment
*by Aaron*

For years, I was concerned about how we'd manage a fleet of dedicated gameservers: Keeping infastructure in sync, scaling up, and managing each game server.

So I decided to put an end to these worries, and built a one-click pipeline that works with any Unity game to:
- purchase and configure baremetal infastructure
- install game builds and orchestrate a fleet (easy scale up/down)
- manage survival game lifecycle via one panel (wipes, RCON, save rollbacks, in-game observability, etc.)

This is about 80% done now, and I plan to also provide access for players who want to host their own worlds. The screenshot below is a real game world running entirely via the new pipeline; a Windows game build running on a Linux server.

![World running via automated pipeline](devblog4-images/world_running_on_fully_automated_provision_pipeline.png)



### 💡 New Deployable: Ceiling Lamp

The first new deployable is the **Ceiling Lamp** — you'll actually need this when we make it properly dark inside the bases.

![Ceiling lamp in a dark room](devblog4-images/ceilinglamp_cinematic_screenshot.png)

It casts shadows, and can be turned on and off. 

We just use a few raycasts to ensure both supports are touching the ceiling. 

<div class="blog-content-image"><video autoplay loop muted playsinline style="max-width:100%;max-height:300px;border-radius:8px;box-shadow:0 4px 16px rgba(0,0,0,0.2);"><source src="https://cdn.jsdelivr.net/gh/aaronmichaelfrost/twoloop-website@main/blog-posts/devblog4-images/light_deployable_placement_algorithm.mp4" type="video/mp4"></video></div>

It is kind of big for the box it comes in. Maybe we'll fix that in the future:

![Ceiling Lamp — pick up from world](devblog4-images/ceilinglamp_world_item_hover.png)


### 🔐 New Deployable: Biometric Code Lock

The second new deployable is the **Biometric Code Lock** — a door-mounted device that combines a live facial recognition feed with a numeric access code.

![Biometric Code Lock — pick up from world](devblog4-images/codelock-world-item-hover.png)

When an authorized player looks at the lock, the light turns green, and that side of the door unlocks for all players. The screen shows your player's face via a live render texture. 

<div class="discord-images-row">
![Code Lock — green, authorized](devblog4-images/codelock-world-screenshot.jpg)
![Code Lock — close up](devblog4-images/codelock_closeup.png)
</div>

To authorize yourself, just type in the code. It initializes to `0000` — so change it fast:

![Change access code interface](devblog4-images/codelock-user-interface.png)

Quick demo vid:

<div class="discord-images-row"><video controls loop muted playsinline style="width:100%;border-radius:4px;"><source src="https://cdn.jsdelivr.net/gh/aaronmichaelfrost/twoloop-website@main/blog-posts/devblog4-images/codelock_long_video_example_compressed.mp4" type="video/mp4"></video></div>


### 🏗️ Item Wiki Update

Small update: the item wiki and console command documentation are now **generated directly from game source files**. So I just run a script, and the website becomes up to date.


### 🐛 Bug Bash — Bugs Hit Zero

I fixed a ton of bugs and general issues, like resolution scaling. 

Main Learnings:
- The "Aspect Ratio Fitter" component makes resolution scaling easier than I thought
- You should ALWAYS consider using Physics.SyncTransforms before doing any sort of collision checks, like spherecasting, spherecheck, etc., otherwise, it can't really be trusted to be up to date, especially if you are depending on positional data for deterministic initialization, or something like that (we were, which might actually be it's own code smell).



## CHANGELOG

**10/13/2025**

* Fixed hitmarker starting visible when joining as a non-host

**12/9/2025**

* Removed motion blur setting — doesn't interact cleanly with scope and screen effects

**12/15/2025**

* Fixed dead player appearing as standing character instead of ragdoll/invisible when joining a session

**4/8/2026**

* NPCs are now always upright, no longer matching terrain slopes
* Build stripper now does proper cleanup on asset folders
* Fixed NPCs not facing heading direction while navigating to a threat point

**4/10/2026**

* Smoothed hipfire-to-ADS camera transition; less jarring

**4/11/2026**

* Fixed bug where other players' projectiles spawned from the wrong gun endpoint

**4/12/2026**

* Fixed forest being too bright during daytime
* Fixed corrupted vegetation system and conditional rendering issue
* Reduced massive scale of new forest tree models
* Fixed overly pale skin tones

**4/21/2026**

* Item wiki and console command wiki now built automatically from game files

**4/22/2026**

* Fixed hitmarker starting visible in build
* Fixed crosshair appearing when closing inventory without a weapon equipped
* Fixed pointer appearing black instead of white in standalone build
* Fixed: closing and reopening the menu too quickly could prevent it from reopening
* Resolution scaling now works for persistent menu and loading screen

**4/23/2026**

* Fixed resolution scaling on F1 console / spawn menu UI
* Fixed resolution scaling on HUD UI
* Fixed resolution scaling on inventory UI
* Fixed more UI tweening determinism issues
* **BUGS AT ZERO**

**4/25/2026**

* Fixed hotbar select bug using number keys
* Finished ceiling lamp deployable — it's in the game
* Fixed "RATE" showing incorrectly for deployables in the hover inspector

**4/27/2026**

* Fixed deployable placement bounds validation bug
* Turret deployable now correctly indicates its placement direction

**4/29/2026**

* New deployable: biometric code lock complete

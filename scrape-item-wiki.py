#!/usr/bin/env python3
"""
Scrapes item .asset files from the Unity Items prefab folder and generates
the item-wiki.md documentation page, including item icons copied to the
website's item-icons/ folder.

Usage:
    python scrape-item-wiki.py <items_folder> [sprites_folder] [output_md] [icons_out_folder]

Defaults (relative to script directory):
    items_folder   = C:/Dev/SRL/SurvivalRogueLikeUnity/Assets/Prefabs/Items
    sprites_folder = C:/Dev/SRL/SurvivalRogueLikeUnity/Assets/Sprites/Inventory/Icons
    output_md      = docs/item-wiki.md
    icons_out      = item-icons/
"""

import os
import re
import sys
import shutil
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


# ---------------------------------------------------------------------------
# Rarity mapping
# ---------------------------------------------------------------------------

RARITY_NAMES = {
    0: "Junk",
    1: "Common",
    2: "Uncommon",
    3: "Rare",
    4: "Epic",
    5: "Legendary",
}

RARITY_ORDER = {v: i for i, v in enumerate(RARITY_NAMES.values())}


# ---------------------------------------------------------------------------
# Category mapping  (folder name -> display name, display order)
# ---------------------------------------------------------------------------

CATEGORY_MAP = {
    "Resources":          ("Resources",    1),
    "Consumables":        ("Consumables",  2),
    "Deployables":        ("Deployables",  3),
    "Tools":              ("Tools",        4),
    # Weapon sub-folders
    "Pistol":             ("Weapons",      5),
    "Heavy Handgun":      ("Weapons",      5),
    "Assault Shotgun":    ("Weapons",      5),
    "Pump Shotgun":       ("Weapons",      5),
    "Burst Rifle":        ("Weapons",      5),
    "Heavy Rifle":        ("Weapons",      5),
    "Fast SMG":           ("Weapons",      5),
    "DMR":                ("Weapons",      5),
    "Hunting Rifle":      ("Weapons",      5),
    "Light Machine Gun":  ("Weapons",      5),
    "Baseball Bat":       ("Weapons",      5),
    "Tanto Knife":        ("Weapons",      5),
    "Frag Grenade":       ("Weapons",      5),
    "hammer":             ("Weapons",      5),
    "Pickaxe":            ("Weapons",      5),
    # Ammo
    "Ammo":               ("Ammo",         6),
    "PistolAmmo":         ("Ammo",         6),
    "RifleAmmo":          ("Ammo",         6),
    "ShotgunAmmo":        ("Ammo",         6),
    "SniperAmmo":         ("Ammo",         6),
    # Attachments
    "Attachments":        ("Attachments",  7),
    "Barrels":            ("Attachments",  7),
    "Grips":              ("Attachments",  7),
    "Magazines":          ("Attachments",  7),
    "Stocks":             ("Attachments",  7),
    "Bodies":             ("Attachments",  7),
    "Crosshair Styles":   ("Attachments",  7),
    # Trinkets
    "Trinkets":           ("Trinkets",     8),
    "Charms":             ("Charms",       9),
    # Money / misc at root
    "Items":              ("Misc",        99),
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Item:
    asset_name: str          # e.g. ammodef_Rocket
    item_name: str           # e.g. Rockets
    description: str
    rarity: str
    max_stack_size: int
    base_value: int
    category: str            # display name
    category_order: int
    sprite_guid: str
    visible_on_load_screen: bool
    # Resolved after guid lookup
    icon_src_path: Optional[str] = None   # absolute path to source PNG
    icon_web_path: Optional[str] = None   # relative web path for <img>


# ---------------------------------------------------------------------------
# Guid → PNG map builder
# ---------------------------------------------------------------------------

def build_guid_map(sprites_root: str) -> dict[str, str]:
    """Walk sprites_root, read every .meta file, return {guid: abs_png_path}."""
    guid_map: dict[str, str] = {}
    for root, _dirs, files in os.walk(sprites_root):
        for fname in files:
            if not fname.endswith(".meta"):
                continue
            meta_path = os.path.join(root, fname)
            png_path = meta_path[:-5]  # strip .meta
            if not os.path.isfile(png_path):
                continue
            try:
                with open(meta_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                m = re.search(r"^guid:\s*([0-9a-f]+)", content, re.MULTILINE)
                if m:
                    guid_map[m.group(1)] = png_path
            except Exception:
                pass
    return guid_map


# ---------------------------------------------------------------------------
# .asset parser
# ---------------------------------------------------------------------------

SKIP_FOLDER_NAMES = {"AI", "reflectiontester"}

def parse_asset(path: str, category: str, category_order: int) -> Optional[Item]:
    """Parse a Unity .asset YAML file into an Item. Returns None to skip."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return None

    def get(key: str) -> Optional[str]:
        m = re.search(rf"^\s+{re.escape(key)}:\s*(.+)$", content, re.MULTILINE)
        return m.group(1).strip() if m else None

    item_name = get("itemName")
    if not item_name:
        return None

    description = get("description") or ""
    # Strip surrounding quotes Unity sometimes adds
    description = description.strip('"').strip("'")

    rarity_raw = get("presetRarity")
    rarity = RARITY_NAMES.get(int(rarity_raw), "Unknown") if rarity_raw and rarity_raw.isdigit() else "Unknown"

    max_stack_raw = get("maxStackSize")
    max_stack = int(max_stack_raw) if max_stack_raw and max_stack_raw.isdigit() else 1

    base_value_raw = get("baseValue")
    base_value = int(base_value_raw) if base_value_raw and base_value_raw.lstrip("-").isdigit() else 0

    visible_raw = get("visibleOnLoadScreen")
    visible = visible_raw == "1"

    # sprite: {fileID: 21300000, guid: <GUID>, type: 3}
    sprite_m = re.search(r"sprite:\s*\{fileID:\s*\d+,\s*guid:\s*([0-9a-f]+),", content)
    sprite_guid = sprite_m.group(1) if sprite_m else ""

    asset_name = os.path.splitext(os.path.basename(path))[0]

    return Item(
        asset_name=asset_name,
        item_name=item_name,
        description=description,
        rarity=rarity,
        max_stack_size=max_stack,
        base_value=base_value,
        category=category,
        category_order=category_order,
        sprite_guid=sprite_guid,
        visible_on_load_screen=visible,
    )


def scrape_items(items_root: str) -> list[Item]:
    items: list[Item] = []
    seen_names: set[str] = set()

    for root, dirs, files in os.walk(items_root):
        # Skip unwanted folders (modify dirs in-place to prune traversal)
        dirs[:] = [d for d in dirs if d not in SKIP_FOLDER_NAMES]

        folder_name = os.path.basename(root)
        cat_display, cat_order = CATEGORY_MAP.get(folder_name, ("Misc", 99))

        for fname in files:
            if not fname.endswith(".asset"):
                continue
            path = os.path.join(root, fname)
            item = parse_asset(path, cat_display, cat_order)
            if item and item.item_name not in seen_names:
                seen_names.add(item.item_name)
                items.append(item)

    return items


# ---------------------------------------------------------------------------
# Icon resolution and copying
# ---------------------------------------------------------------------------

def resolve_icons(
    items: list[Item],
    guid_map: dict[str, str],
    icons_out: str,
    icons_web_prefix: str = "item-icons",
) -> None:
    """
    For each item, resolve sprite_guid -> source PNG, copy to icons_out,
    and set icon_web_path.
    """
    os.makedirs(icons_out, exist_ok=True)
    copied: dict[str, str] = {}  # src_path -> dest filename (avoid double copies)

    for item in items:
        if not item.sprite_guid or item.sprite_guid not in guid_map:
            continue

        src = guid_map[item.sprite_guid]
        if src in copied:
            item.icon_src_path = src
            item.icon_web_path = f"{icons_web_prefix}/{copied[src]}"
            continue

        # Sanitize filename: use asset_name + original extension
        ext = os.path.splitext(src)[1]
        dest_name = item.asset_name + ext
        dest_path = os.path.join(icons_out, dest_name)

        try:
            shutil.copy2(src, dest_path)
            item.icon_src_path = src
            item.icon_web_path = f"{icons_web_prefix}/{dest_name}"
            copied[src] = dest_name
        except Exception as e:
            print(f"  Warning: could not copy icon for {item.item_name}: {e}")


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

def md_cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def build_category_section(category: str, items: list[Item]) -> str:
    lines = [f"## {category}\n"]
    lines.append("| Icon | Item | Description | Rarity | Stack |")
    lines.append("|------|------|-------------|--------|-------|")

    # Sort within category: rarity order then name
    sorted_items = sorted(
        items,
        key=lambda i: (RARITY_ORDER.get(i.rarity, 99), i.item_name.lower())
    )

    for item in sorted_items:
        if item.icon_web_path:
            icon_cell = f'<img src="{item.icon_web_path}" alt="{md_cell(item.item_name)}" width="40">'
        else:
            icon_cell = "—"

        lines.append(
            f"| {icon_cell} "
            f"| **{md_cell(item.item_name)}** "
            f"| {md_cell(item.description)} "
            f"| {md_cell(item.rarity)} "
            f"| {item.max_stack_size} |"
        )

    return "\n".join(lines)


def generate_markdown(items: list[Item]) -> str:
    from datetime import datetime, timezone
    last_updated = datetime.now(timezone.utc).strftime('%B %d, %Y')
    # Group by category display name, preserve category order
    from collections import defaultdict
    categories: dict[str, tuple[int, list[Item]]] = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = (item.category_order, [])
        categories[item.category][1].append(item)

    sorted_cats = sorted(categories.items(), key=lambda kv: kv[1][0])

    sections = []
    for cat_name, (_, cat_items) in sorted_cats:
        sections.append(build_category_section(cat_name, cat_items))

    total = len(items)
    body = "\n\n---\n\n".join(sections)

    return f"""\
---
title: "Item Wiki"
order: 3
last_updated: "{last_updated}"
---

# Item Wiki

Complete reference for all **{total}** items in Fractium. Icons, descriptions, and stats are sourced directly from game data.

---

{body}
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

DEFAULT_ITEMS_ROOT   = r"C:\Dev\SRL\SurvivalRogueLikeUnity\Assets\Prefabs\Items"
DEFAULT_SPRITES_ROOT = r"C:\Dev\SRL\SurvivalRogueLikeUnity\Assets\Sprites\Inventory\Icons"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    items_root   = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ITEMS_ROOT
    sprites_root = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SPRITES_ROOT
    out_md       = sys.argv[3] if len(sys.argv) > 3 else os.path.join(script_dir, "docs", "item-wiki.md")
    icons_out    = sys.argv[4] if len(sys.argv) > 4 else os.path.join(script_dir, "item-icons")

    if not os.path.isdir(items_root):
        print(f"Error: items folder not found: {items_root}")
        sys.exit(1)

    print(f"Scraping items from: {items_root}")
    items = scrape_items(items_root)
    print(f"Found {len(items)} items")

    if os.path.isdir(sprites_root):
        print(f"Building sprite guid map from: {sprites_root}")
        guid_map = build_guid_map(sprites_root)
        print(f"  {len(guid_map)} sprites indexed")
        icons_web_prefix = "item-icons"
        print(f"Copying icons to: {icons_out}")
        resolve_icons(items, guid_map, icons_out, icons_web_prefix)
        resolved = sum(1 for i in items if i.icon_web_path)
        print(f"  {resolved}/{len(items)} icons resolved")
    else:
        print(f"Warning: sprites folder not found, skipping icons: {sprites_root}")

    md = generate_markdown(items)
    os.makedirs(os.path.dirname(out_md), exist_ok=True)
    with open(out_md, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Written: {out_md}")


if __name__ == "__main__":
    main()

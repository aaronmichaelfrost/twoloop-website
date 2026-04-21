#!/usr/bin/env python3
"""
Scrapes ConsoleCommand definitions from a C# GameConsole.cs file and
generates the console-commands.md documentation page.

Usage:
    python scrape-console-commands.py <path_to_GameConsole.cs> [output_md_path]

If output_md_path is omitted, defaults to docs/console-commands.md relative
to the script's directory.
"""

import re
import sys
import os
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ConsoleCommand:
    id: str
    description: str
    format: str
    is_admin_only: bool
    requires_in_game: bool
    server_only: bool = False   # inside #if UNITY_SERVER
    client_only: bool = False   # inside #if !UNITY_SERVER


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def extract_balanced(text: str, start: int) -> str:
    """
    Given text and a position of '(', return the substring from that '('
    up to and including the matching ')'.
    """
    depth = 0
    i = start
    in_string = False
    string_char = None
    escape_next = False
    verbatim = False

    while i < len(text):
        ch = text[i]

        if escape_next:
            escape_next = False
            i += 1
            continue

        if in_string:
            if verbatim:
                if ch == '"':
                    # check for doubled quote escape ""
                    if i + 1 < len(text) and text[i + 1] == '"':
                        i += 2
                        continue
                    in_string = False
            else:
                if ch == '\\':
                    escape_next = True
                elif ch == string_char:
                    in_string = False
        else:
            if ch == '@' and i + 1 < len(text) and text[i + 1] == '"':
                in_string = True
                string_char = '"'
                verbatim = True
                i += 2
                continue
            elif ch in ('"', "'"):
                in_string = True
                string_char = ch
                verbatim = False
            elif ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]

        i += 1

    return text[start:]  # unbalanced – return rest


def extract_string_value(token: str) -> str:
    """
    Pull the first (or concatenated) string literal(s) from a C# expression.
    Handles: "simple", $"interp", "a" + "b", multi-line + concat.
    For interpolated strings with complex expressions, returns the raw literal.
    """
    # Strip outer whitespace / newlines
    token = token.strip()

    # Collect all string segments in order
    segments = []

    # Match regular strings, verbatim strings, interpolated strings
    pattern = re.compile(
        r'\$?"(?:[^"\\]|\\.)*"'   # regular or interpolated double-quoted
        r"|@\"(?:[^\"]|\"\")*\""   # verbatim @"..."
    )

    for m in pattern.finditer(token):
        s = m.group(0)
        # Strip leading $, @
        s = s.lstrip('$@')
        # Remove surrounding quotes
        s = s[1:-1]
        # Decode common C# escapes
        s = s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
        segments.append(s)

    result = ''.join(segments)
    # Flatten real newlines to a space for markdown table cells
    result = result.replace('\n', ' ').replace('\r', '')
    # Collapse extra whitespace
    result = re.sub(r'  +', ' ', result).strip()
    return result


def extract_bool(text: str) -> bool:
    return text.strip().lower() in ('true', '1')


def split_top_level_args(args_body: str) -> list[str]:
    """
    Split a constructor argument list (without outer parens) on top-level commas.
    Respects nested (), <>, [], strings.
    """
    parts = []
    depth = 0
    current = []
    in_string = False
    string_char = None
    escape_next = False
    verbatim = False
    i = 0

    while i < len(args_body):
        ch = args_body[i]

        if escape_next:
            escape_next = False
            current.append(ch)
            i += 1
            continue

        if in_string:
            current.append(ch)
            if verbatim:
                if ch == '"':
                    if i + 1 < len(args_body) and args_body[i + 1] == '"':
                        current.append(args_body[i + 1])
                        i += 2
                        continue
                    in_string = False
            else:
                if ch == '\\':
                    escape_next = True
                elif ch == string_char:
                    in_string = False
        else:
            if ch == '@' and i + 1 < len(args_body) and args_body[i + 1] == '"':
                in_string = True
                string_char = '"'
                verbatim = True
                current.append(ch)
                current.append(args_body[i + 1])
                i += 2
                continue
            elif ch in ('"', "'"):
                in_string = True
                string_char = ch
                verbatim = False
                current.append(ch)
            elif ch in ('(', '[', '<'):
                depth += 1
                current.append(ch)
            elif ch in (')', ']', '>'):
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                parts.append(''.join(current))
                current = []
                i += 1
                continue
            else:
                current.append(ch)

        i += 1

    if current:
        parts.append(''.join(current))

    return parts


def parse_command_call(call_body: str) -> Optional[ConsoleCommand]:
    """
    Parse the argument list of a ConsoleCommand constructor call (without outer parens).
    Returns a ConsoleCommand or None if parsing fails.
    """
    args = split_top_level_args(call_body)
    if len(args) < 3:
        return None

    # Build a dict of named args alongside positional tracking
    positional = []
    named = {}

    for arg in args:
        arg_stripped = arg.strip()
        # Named arg? e.g.  "isAdminOnly: true"  or  "description: \"...\""
        named_match = re.match(r'^(\w+)\s*:\s*(.*)', arg_stripped, re.DOTALL)
        if named_match:
            named[named_match.group(1)] = named_match.group(2).strip()
        else:
            positional.append(arg_stripped)

    def get_pos_or_named(pos_idx: int, name: str) -> Optional[str]:
        if name in named:
            return named[name]
        if pos_idx < len(positional):
            return positional[pos_idx]
        return None

    id_raw = get_pos_or_named(0, 'id')
    desc_raw = get_pos_or_named(1, 'description')
    fmt_raw = get_pos_or_named(2, 'format')
    admin_raw = get_pos_or_named(3, 'isAdminOnly')
    in_game_raw = get_pos_or_named(4, 'requiresInGame')

    if not id_raw or not desc_raw:
        return None

    cmd_id = extract_string_value(id_raw)
    cmd_desc = extract_string_value(desc_raw)
    cmd_fmt = extract_string_value(fmt_raw) if fmt_raw else cmd_id
    is_admin = extract_bool(admin_raw) if admin_raw else False
    req_in_game = extract_bool(in_game_raw) if in_game_raw else False

    if not cmd_id:
        return None

    return ConsoleCommand(
        id=cmd_id,
        description=cmd_desc,
        format=cmd_fmt,
        is_admin_only=is_admin,
        requires_in_game=req_in_game,
    )


# ---------------------------------------------------------------------------
# Main scraper
# ---------------------------------------------------------------------------

def scrape(cs_path: str) -> list[ConsoleCommand]:
    with open(cs_path, 'r', encoding='utf-8') as f:
        source = f.read()

    commands: list[ConsoleCommand] = []

    # Track #if context line-by-line so we can tag commands
    # We'll do a two-pass: first build a map of character offset -> context flags
    # Simple approach: scan for preprocessor directives
    preprocessor_stack: list[str] = []  # stack of active conditions
    # Build a list of (char_offset, server_only, client_only) transitions
    # We'll scan the source for positions of `new ConsoleCommand` and determine
    # context by checking which #if blocks surround them.

    # Build offset -> (server_only, client_only) by scanning lines
    offset_context: list[tuple[int, bool, bool]] = []
    server_only = False
    client_only = False
    pos = 0
    for line in source.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#if UNITY_SERVER') and '!' not in stripped:
            server_only = True
            client_only = False
        elif stripped.startswith('#if !UNITY_SERVER'):
            client_only = True
            server_only = False
        elif stripped.startswith('#else'):
            # flip the active block
            server_only, client_only = client_only, server_only
        elif stripped.startswith('#endif'):
            server_only = False
            client_only = False
        offset_context.append((pos, server_only, client_only))
        pos += len(line) + 1  # +1 for '\n'

    def get_context_at(offset: int) -> tuple[bool, bool]:
        so, co = False, False
        for (o, s, c) in offset_context:
            if o > offset:
                break
            so, co = s, c
        return so, co

    # Find all `new ConsoleCommand` occurrences (handles nested generics like List<string>)
    pattern = re.compile(r'\bnew\s+ConsoleCommand[^(]*\(')

    for m in pattern.finditer(source):
        open_paren = source.index('(', m.start())
        call_with_parens = extract_balanced(source, open_paren)
        # Strip outer parens
        args_body = call_with_parens[1:-1]

        cmd = parse_command_call(args_body)
        if cmd:
            so, co = get_context_at(m.start())
            cmd.server_only = so
            cmd.client_only = co
            commands.append(cmd)

    return commands


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------

SECTIONS = [
    ("General Commands", lambda c: c.id in ('help', 'usage', 'loglevel', 'gamescene')),
    ("Player Commands", lambda c: c.id in ('kill', 'combatlog', 'listplayers')),
    ("Inventory & Items", lambda c: c.id in ('give', 'giveto', 'giveall', 'kit')),
    ("Movement & Camera", lambda c: c.id in ('teleport', 'noclip', 'noclipspeed', 'noclipacceleration', 'flytest', 'speed', 'freecam', 'setfov', 'setviewfov')),
    ("UI & Display", lambda c: c.id in ('fps', 'hud', 'clear', 'crosshaircolor', 'crosshairmove', 'showaimcone', 'hideaimcone', 'pointeralwaysShow')),
    ("Game Settings", lambda c: c.id in ('difficulty', 'difficultypause', 'difficultydebug', 'friendlyfire', 'ammoinfinite', 'god', 'cheats', 'infinitebuild', 'fog', 'skyboxspeed')),
    ("World / Island", lambda c: c.id in ('islandseed', 'islandbiome')),
    ("Visibility", lambda c: c.id in ('visglobal', 'vislocal')),
    ("Moderation", lambda c: c.id in ('listadmins', 'listbannedplayers', 'banid', 'banname', 'unbanid', 'unbanname', 'modid', 'modname', 'unmodid', 'unmodname', 'kickid', 'kickname', 'killall', 'clearviolations', 'listviolations')),
    ("Networking", lambda c: c.id in ('connect',)),
    ("Cosmetics", lambda c: c.id in ('randomize_cosmetics',)),
    ("Dedicated Server Only", lambda c: c.server_only),
]


def md_cell(text: str) -> str:
    """Escape pipe characters for markdown table cells."""
    return text.replace('|', '\\|')


def build_table(commands: list[ConsoleCommand]) -> str:
    rows = ['| Command | Description | Format | Admin Only |',
            '|---------|-------------|--------|------------|']
    for c in commands:
        rows.append(
            f'| `{md_cell(c.id)}` '
            f'| {md_cell(c.description)} '
            f'| `{md_cell(c.format)}` '
            f'| {"Yes" if c.is_admin_only else "No"} |'
        )
    return '\n'.join(rows)


def generate_markdown(commands: list[ConsoleCommand]) -> str:
    from datetime import datetime, timezone
    last_updated = datetime.now(timezone.utc).strftime('%B %d, %Y')
    assigned: set[str] = set()
    sections_output: list[str] = []

    for section_name, predicate in SECTIONS:
        section_cmds = [c for c in commands if predicate(c) and c.id not in assigned]
        if not section_cmds:
            continue
        for c in section_cmds:
            assigned.add(c.id)
        sections_output.append(f'## {section_name}\n\n{build_table(section_cmds)}')

    # Catch-all for anything not matched
    unmatched = [c for c in commands if c.id not in assigned]
    if unmatched:
        sections_output.append(f'## Other Commands\n\n{build_table(unmatched)}')

    body = '\n\n---\n\n'.join(sections_output)

    return f"""\
---
title: "Console Commands"
order: 2
last_updated: "{last_updated}"
---

# Console Commands

Fractium includes a powerful console system that allows players and administrators to execute various commands. Press `F1` to open the console in-game.

Commands marked with **[admin]** require administrator or moderator privileges. Commands marked with **[server only]** only run on dedicated server builds.

---

{body}
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cs_path = sys.argv[1]
    if not os.path.isfile(cs_path):
        print(f'Error: file not found: {cs_path}')
        sys.exit(1)

    if len(sys.argv) >= 3:
        out_path = sys.argv[2]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        out_path = os.path.join(script_dir, 'docs', 'console-commands.md')

    print(f'Scraping: {cs_path}')
    commands = scrape(cs_path)
    print(f'Found {len(commands)} commands: {[c.id for c in commands]}')

    md = generate_markdown(commands)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f'Written: {out_path}')


if __name__ == '__main__':
    main()

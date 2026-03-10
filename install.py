#!/usr/bin/env python3
"""
Install code-puppy-superpowers into your Code Puppy environment.

Copies agents, commands, skills, and plugin into ~/.code_puppy/.
Creates a symlink from ~/.code-puppy/commands → ~/.code_puppy/commands.
Run from the repo root: python install.py
"""

import os
import shutil
import json
import sys
from pathlib import Path


# --- Configuration ---

HOME = Path.home()
CODE_PUPPY_DIR = HOME / ".code_puppy"
CODE_PUPPY_HYPHEN_DIR = HOME / ".code-puppy"  # alternate naming convention

AGENTS_DIR = CODE_PUPPY_DIR / "agents"
COMMANDS_DIR = CODE_PUPPY_DIR / "commands"
PLUGINS_DIR = CODE_PUPPY_DIR / "plugins" / "superpowers"
SKILLS_DIR = CODE_PUPPY_DIR / "skills"

# Symlink target: ~/.code-puppy/commands → ~/.code_puppy/commands
COMMANDS_SYMLINK = CODE_PUPPY_HYPHEN_DIR / "commands"

REPO_ROOT = Path(__file__).parent


def banner(msg: str):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")


def copy_directory(src: Path, dst: Path, label: str):
    """Copy contents of src into dst, creating dst if needed."""
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in src.iterdir():
        dest_path = dst / item.name
        if item.is_dir():
            shutil.copytree(item, dest_path, dirs_exist_ok=True)
            count += 1
        elif item.is_file():
            shutil.copy2(item, dest_path)
            count += 1
    print(f"  [{label}] Copied {count} items to {dst}")
    return count


def create_symlink(target: Path, link: Path, label: str):
    """Create a symlink, handling existing links/dirs gracefully."""
    link.parent.mkdir(parents=True, exist_ok=True)

    if link.is_symlink():
        existing_target = link.resolve()
        if existing_target == target.resolve():
            print(f"  [{label}] Symlink already exists: {link} -> {target}")
            return
        print(f"  [{label}] Updating symlink: {link} -> {target} (was -> {existing_target})")
        link.unlink()
    elif link.exists():
        print(f"  [{label}] WARNING: {link} exists and is not a symlink.")
        print(f"  [{label}] Skipping symlink creation. Manually remove it if you want the symlink.")
        return

    link.symlink_to(target)
    print(f"  [{label}] Created symlink: {link} -> {target}")


def validate_agents():
    """Validate all agent JSON files parse correctly."""
    agents_src = REPO_ROOT / "agents"
    errors = []
    for f in sorted(agents_src.glob("*.json")):
        try:
            with open(f) as fp:
                data = json.load(fp)
            required = {"id", "name", "description", "system_prompt", "tools"}
            missing = required - set(data.keys())
            if missing:
                errors.append(f"{f.name}: missing required fields: {missing}")
        except json.JSONDecodeError as e:
            errors.append(f"{f.name}: invalid JSON: {e}")
    return errors


def main():
    banner("code-puppy-superpowers installer")

    # Validate before copying
    print("\nValidating agent files...")
    errors = validate_agents()
    if errors:
        print("  ERRORS found:")
        for e in errors:
            print(f"    - {e}")
        print("\nFix these errors before installing.")
        sys.exit(1)
    print("  All agents valid.")

    # 1. Agents
    print("\n1. Installing agents...")
    copy_directory(REPO_ROOT / "agents", AGENTS_DIR, "agents")

    # 2. Commands
    print("\n2. Installing commands...")
    copy_directory(REPO_ROOT / "commands", COMMANDS_DIR, "commands")

    # 3. Skills (reference docs)
    print("\n3. Installing skill references...")
    copy_directory(REPO_ROOT / "skills", SKILLS_DIR, "skills")

    # 4. Plugin
    print("\n4. Installing plugin...")
    copy_directory(REPO_ROOT / "plugin", PLUGINS_DIR, "plugin")

    # 5. Symlink ~/.code-puppy/commands → ~/.code_puppy/commands
    print("\n5. Creating commands symlink...")
    create_symlink(COMMANDS_DIR, COMMANDS_SYMLINK, "symlink")

    # Summary
    banner("Installation complete")

    agent_count = len(list((REPO_ROOT / "agents").glob("*.json")))
    skill_count = len(list((REPO_ROOT / "skills").iterdir()))
    command_count = len(list((REPO_ROOT / "commands").glob("*.md")))

    print(f"""
  Installed:
    {agent_count} agents     -> {AGENTS_DIR}
    {command_count} commands   -> {COMMANDS_DIR}
    {skill_count} skills     -> {SKILLS_DIR}
    1 plugin     -> {PLUGINS_DIR}
    1 symlink    -> {COMMANDS_SYMLINK} -> {COMMANDS_DIR}

  Models are pinned inline in each agent's JSON:
    Opus:   mastermind, brainstormer, adversarial-reviewer
    Sonnet: plan-writer, debugger, implementer-heavy, spec-reviewer, quality-reviewer
    Haiku:  implementer-light

  Start using superpowers:
    /agent mastermind     -- Full orchestrated workflow
    /brainstorm           -- Start designing
    /write-plan           -- Create implementation plan
    /execute-plan         -- Execute plan with sub-agents
    /debug                -- Systematic debugging
    /review               -- Code review
    /finish-branch        -- Complete and clean up
""")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Uninstall code-puppy-superpowers from your Code Puppy environment.

Removes agents, commands, skills, and plugin installed by install.py.
Run from anywhere: python uninstall.py
"""

import json
import shutil
import sys
from pathlib import Path

HOME = Path.home()
CODE_PUPPY_DIR = HOME / ".code_puppy"

AGENTS_DIR = CODE_PUPPY_DIR / "agents"
COMMANDS_DIR = CODE_PUPPY_DIR / "commands"
PLUGINS_DIR = CODE_PUPPY_DIR / "plugins" / "superpowers"
SKILLS_DIR = CODE_PUPPY_DIR / "skills"
COMMANDS_SYMLINK = HOME / ".code-puppy" / "commands"

# Agents we installed (by name field in JSON).
AGENT_NAMES = [
    "mastermind",
    "brainstormer",
    "plan-writer",
    "debugger",
    "implementer-heavy",
    "implementer-light",
    "spec-reviewer",
    "quality-reviewer",
    "adversarial-reviewer",
]

# Commands we installed (filenames).
COMMAND_FILES = [
    "brainstorm.md",
    "write-plan.md",
    "execute-plan.md",
    "debug.md",
    "review.md",
    "finish-branch.md",
]

# Skill subdirectories we installed (inside ~/.code_puppy/skills/).
SKILL_SUBDIRS = [
    "brainstorming",
    "writing-plans",
    "test-driven-development",
    "using-git-worktrees",
    "finishing-a-development-branch",
    "subagent-driven-development",
    "systematic-debugging",
    "requesting-code-review",
    "receiving-code-review",
    "dispatching-parallel-agents",
]


def find_agent_files():
    """Find agent JSON files that match our agent names."""
    found = []
    if not AGENTS_DIR.is_dir():
        return found
    for f in AGENTS_DIR.glob("*.json"):
        try:
            data = json.loads(f.read_text())
            if data.get("name") in AGENT_NAMES:
                found.append(f)
        except (json.JSONDecodeError, KeyError):
            continue
    return found


def find_command_files():
    """Find command markdown files we installed."""
    found = []
    for name in COMMAND_FILES:
        path = COMMANDS_DIR / name
        if path.is_file():
            found.append(path)
    return found


def find_skill_dirs():
    """Find skill subdirectories we installed."""
    found = []
    for name in SKILL_SUBDIRS:
        path = SKILLS_DIR / name
        if path.is_dir():
            found.append(path)
    return found


def main():
    print("\n  code-puppy-superpowers uninstaller")
    print("  " + "=" * 40)

    # Collect what we'd remove
    agent_files = find_agent_files()
    command_files = find_command_files()
    skill_dirs = find_skill_dirs()
    has_plugin = PLUGINS_DIR.is_dir()
    has_symlink = COMMANDS_SYMLINK.is_symlink()

    if not agent_files and not command_files and not skill_dirs and not has_plugin:
        print("\n  Nothing to uninstall. Superpowers doesn't appear to be installed.")
        sys.exit(0)

    print("\n  The following will be removed:\n")

    if agent_files:
        print(f"  Agents ({len(agent_files)}):")
        for f in agent_files:
            print(f"    {f}")

    if command_files:
        print(f"  Commands ({len(command_files)}):")
        for f in command_files:
            print(f"    {f}")

    if skill_dirs:
        print(f"  Skills ({len(skill_dirs)}):")
        for d in skill_dirs:
            print(f"    {d}")

    if has_plugin:
        print(f"  Plugin: {PLUGINS_DIR}")

    if has_symlink:
        print(f"  Symlink: {COMMANDS_SYMLINK}")

    # Confirm
    print()
    confirm = input("  Proceed? [y/N] ").strip().lower()
    if confirm not in ("y", "yes"):
        print("  Cancelled.")
        sys.exit(0)

    # Remove
    removed = 0

    for f in agent_files:
        f.unlink()
        removed += 1

    for f in command_files:
        f.unlink()
        removed += 1

    for d in skill_dirs:
        shutil.rmtree(d)
        removed += 1

    if has_plugin:
        shutil.rmtree(PLUGINS_DIR)
        removed += 1

    if has_symlink:
        target = COMMANDS_SYMLINK.resolve()
        if target == COMMANDS_DIR.resolve():
            COMMANDS_SYMLINK.unlink()
            removed += 1
            print(f"  Removed symlink: {COMMANDS_SYMLINK}")
        else:
            print(f"  Skipped symlink (points to {target}, not our commands dir)")

    print(f"\n  Done. Removed {removed} items.")
    print("  Superpowers has been uninstalled from Code Puppy.")


if __name__ == "__main__":
    main()

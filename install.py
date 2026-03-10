#!/usr/bin/env python3
"""
Install code-puppy-superpowers into your Code Puppy environment.

Copies agents, commands, skills, and plugin into the correct locations.
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
AGENTS_DIR = CODE_PUPPY_DIR / "agents"
PLUGINS_DIR = CODE_PUPPY_DIR / "plugins" / "superpowers"
SKILLS_DIR = CODE_PUPPY_DIR / "superpowers" / "skills"

# Commands go into the project-local .claude/commands/ directory.
# If no project directory is specified, we use cwd.
PROJECT_COMMANDS_DIR = Path.cwd() / ".claude" / "commands"

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


def copy_file(src: Path, dst: Path, label: str):
    """Copy a single file."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  [{label}] Copied {src.name} to {dst}")


def validate_agents():
    """Validate all agent JSON files parse correctly."""
    agents_src = REPO_ROOT / "agents"
    errors = []
    for f in sorted(agents_src.glob("*.json")):
        try:
            with open(f) as fp:
                data = json.load(fp)
            required = {"name", "description", "system_prompt", "tools"}
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

    # 2. Skills (reference docs)
    print("\n2. Installing skill references...")
    copy_directory(REPO_ROOT / "skills", SKILLS_DIR, "skills")

    # 3. Plugin
    print("\n3. Installing plugin...")
    copy_directory(REPO_ROOT / "plugin", PLUGINS_DIR, "plugin")

    # 4. Commands (project-local)
    print(f"\n4. Installing commands to {PROJECT_COMMANDS_DIR}...")
    copy_directory(REPO_ROOT / "commands", PROJECT_COMMANDS_DIR, "commands")

    # Summary
    banner("Installation complete")

    agent_count = len(list((REPO_ROOT / "agents").glob("*.json")))
    skill_count = len(list((REPO_ROOT / "skills").iterdir()))
    command_count = len(list((REPO_ROOT / "commands").glob("*.md")))

    print(f"""
  Installed:
    {agent_count} agents     → {AGENTS_DIR}
    {skill_count} skills     → {SKILLS_DIR}
    {command_count} commands   → {PROJECT_COMMANDS_DIR}
    1 plugin     → {PLUGINS_DIR}

  Next steps:
    1. Pin models in Code Puppy:
       /pin_model mastermind           → claude-opus-4-6
       /pin_model brainstormer         → claude-opus-4-6
       /pin_model plan-writer          → claude-sonnet-4-6
       /pin_model debugger             → claude-sonnet-4-6
       /pin_model implementer-heavy    → claude-sonnet-4-6
       /pin_model implementer-light    → claude-haiku-4-5
       /pin_model spec-reviewer        → claude-sonnet-4-6
       /pin_model quality-reviewer     → claude-sonnet-4-6
       /pin_model adversarial-reviewer → claude-opus-4-6

    2. Start using superpowers:
       /agent mastermind     — Full orchestrated workflow
       /brainstorm           — Start designing
       /write-plan           — Create implementation plan
       /execute-plan         — Execute plan with sub-agents
       /debug                — Systematic debugging
       /review               — Code review
       /finish-branch        — Complete and clean up
""")


if __name__ == "__main__":
    main()

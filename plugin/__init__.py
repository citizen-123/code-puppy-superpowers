# code-puppy-superpowers plugin
# Hooks into Code Puppy's callback system to provide automatic skill detection
# and routing, mirroring obra/superpowers' auto-discovery behavior.

import os
from code_puppy.callbacks import register_callback

from .config import SKILL_TRIGGERS, REFERENCE_SKILLS, SKILLS_BASE


# How far into the message "weak" patterns must appear to trigger.
_WEAK_MATCH_WINDOW = 80


def _get_skills_root():
    """Resolve the installed skills directory path."""
    candidates = [
        os.path.expanduser(SKILLS_BASE),
        os.path.join(os.path.expanduser("~"), ".code-puppy", "skills"),
        os.path.join(os.getcwd(), ".superpowers", "skills"),
    ]
    for path in candidates:
        if os.path.isdir(path):
            return path
    return None


def _find_matching_skill(message: str) -> dict | None:
    """Match a user message against skill trigger patterns.

    Matching rules:
    - If any "negative" pattern is present anywhere, the skill is skipped.
    - "strong" patterns match anywhere in the message and are sufficient alone.
    - "weak" patterns must appear in the first _WEAK_MATCH_WINDOW characters.
    - First matching skill wins (order in SKILL_TRIGGERS matters).
    """
    msg_lower = message.lower().strip()
    msg_start = msg_lower[:_WEAK_MATCH_WINDOW]

    for skill_name, config in SKILL_TRIGGERS.items():
        # Check negatives first — any hit disqualifies this skill
        negatives = config.get("negative", [])
        if any(neg in msg_lower for neg in negatives):
            continue

        # Check strong patterns (match anywhere)
        strong = config.get("strong", [])
        if any(pat in msg_lower for pat in strong):
            return {"skill": skill_name, **config}

        # Check weak patterns (must appear near the start)
        weak = config.get("weak", [])
        if any(pat in msg_start for pat in weak):
            return {"skill": skill_name, **config}

    return None


@register_callback("on_startup")
async def register_superpowers(context: dict):
    """Called when Code Puppy starts. Registers available skills and
    verifies agents are installed."""
    skills_root = _get_skills_root()
    agents_dir = os.path.join(os.path.expanduser("~"), ".code_puppy", "agents")

    available_skills = []
    missing_agents = []

    # Check skill reference files
    if skills_root:
        for skill_name in os.listdir(skills_root):
            skill_file = os.path.join(skills_root, skill_name, "SKILL.md")
            if os.path.isfile(skill_file):
                available_skills.append(skill_name)

    # Check that trigger-mapped agents exist
    for skill_name, config in SKILL_TRIGGERS.items():
        agent_name = config["agent"]
        agent_file = os.path.join(agents_dir, f"{agent_name}.json")
        if not os.path.isfile(agent_file):
            missing_agents.append(agent_name)

    if missing_agents:
        print(f"[superpowers] Warning: missing agents: {', '.join(missing_agents)}")
        print("[superpowers] Run the install script to set up all agents.")

    if available_skills:
        print(f"[superpowers] {len(available_skills)} skills available: {', '.join(sorted(available_skills))}")

    return {"available_skills": available_skills, "missing_agents": missing_agents}


@register_callback("before_message")
async def detect_skill_trigger(message: str, context: dict):
    """Called before every user message is sent to the AI.
    Detects skill triggers and injects routing context."""
    match = _find_matching_skill(message)

    if match is None:
        return {"message": message}

    skill_name = match["skill"]
    agent_name = match["agent"]
    announce = match["announce"]
    skills_root = _get_skills_root()

    # Build context injection
    skill_context = f"\n\n[superpowers] {announce}\n"

    # If a SKILL.md reference exists, tell the agent where to find it
    if skills_root:
        skill_file = os.path.join(skills_root, skill_name, "SKILL.md")
        if os.path.isfile(skill_file):
            skill_context += f"[superpowers] Reference: read_file {skill_file}\n"

    # Inject the skill context into the message
    augmented_message = message + skill_context

    return {
        "message": augmented_message,
        "suggested_agent": agent_name,
        "skill_triggered": skill_name,
    }

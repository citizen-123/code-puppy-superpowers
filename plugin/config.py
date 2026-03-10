# Skill trigger patterns and configuration for the superpowers plugin.
# Maps user intent patterns to skills/agents.

SKILL_TRIGGERS = {
    "brainstorming": {
        "agent": "brainstormer",
        "patterns": [
            "let's build",
            "let's create",
            "let's make",
            "I want to build",
            "I want to create",
            "I need a",
            "help me design",
            "help me plan",
            "new feature",
            "add a feature",
            "implement a",
            "how should I",
            "what's the best way to",
            "I'm thinking about",
            "let's brainstorm",
        ],
        "description": "Collaborative design refinement before implementation",
        "announce": "Using brainstorming to explore and refine the design before implementation.",
    },
    "systematic-debugging": {
        "agent": "debugger",
        "patterns": [
            "fix this bug",
            "debug this",
            "why is this failing",
            "this is broken",
            "not working",
            "error when",
            "exception in",
            "crash when",
            "investigate this",
            "troubleshoot",
            "track down",
            "figure out why",
        ],
        "description": "Methodical hypothesis-driven debugging",
        "announce": "Using systematic-debugging to methodically isolate the root cause.",
    },
    "writing-plans": {
        "agent": "plan-writer",
        "patterns": [
            "write a plan",
            "create a plan",
            "implementation plan",
            "break this down",
            "plan this out",
            "make a plan",
        ],
        "description": "Break approved designs into bite-sized implementation tasks",
        "announce": "Using writing-plans to create a detailed implementation plan.",
    },
}

# Skills that are behavioral guidelines (not dispatchable agents).
# Agents read these via read_file when relevant.
REFERENCE_SKILLS = [
    "test-driven-development",
    "using-git-worktrees",
    "finishing-a-development-branch",
    "requesting-code-review",
    "receiving-code-review",
    "dispatching-parallel-agents",
    "subagent-driven-development",
]

# Where skill reference files live relative to the install root.
SKILLS_DIR = "skills"

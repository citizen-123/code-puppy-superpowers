# Implementation TODO

Items requiring manual testing are excluded (plugin load verification, skill path resolution testing, invoke_agent chain testing). Those are marked at the bottom for you to validate after these changes land.

## Code Changes

### TODO-1: Fix skill reference paths to absolute
**Files:** All 9 agents (any that reference `skills/...`)
**What:** Replace relative paths like `skills/brainstorming/SKILL.md` with `~/.code_puppy/skills/brainstorming/SKILL.md` in system_prompt text.
**Why:** `read_file skills/brainstorming/SKILL.md` resolves against cwd, not the global config directory.

### TODO-2: Trim implementer-light system prompt
**Files:** `agents/implementer-light.json`
**What:** Condense golden_rules to single-line summaries. Remove XML tag verbosity. Keep workspace rule, implementation rules, output format, and scope discipline but make each terser. Target: cut system prompt token count roughly in half.
**Why:** Haiku has a smaller context window. Every system prompt token competes with the actual task.

### TODO-3: Harden plugin auto-detection
**Files:** `plugin/config.py`
**What:** 
- Add negative patterns to each trigger (e.g. "let's build on" should NOT trigger brainstorming)
- Require match at start of message or after a sentence boundary, not arbitrary substring
- Add a confidence threshold: require at least 2 pattern matches or one strong match (e.g. explicit "/brainstorm" without the slash)
**Why:** Current substring matching false-positives on normal conversation.

### TODO-4: Fix worktree Phase 0 shell command tension
**Files:** `agents/mastermind.json`
**What:** Add an explicit carve-out in the mastermind's role description: "You do not implement application code. You DO run infrastructure commands: git operations, dependency installation, test suite execution, and worktree management." Currently the prompt says "You coordinate work. You do not implement." which conflicts with Phase 0 requiring 5-10 shell commands.
**Why:** The mastermind needs to run git worktree add, npm install, and the test suite, but its own instructions tell it not to do hands-on work.

### TODO-5: Normalize tool lists (edit_file convention)
**Files:** All 9 agents
**What:** Standardize on `edit_file` everywhere (since Code Puppy auto-expands it to create_file + replace_in_file + delete_snippet). Remove explicit `create_file` and `replace_in_file` entries where `edit_file` covers them. Keep `delete_file` separate since that's not covered by edit_file.
**Why:** Inconsistent tool lists across agents. Some use the expanded form, some use edit_file. Pick one.

### TODO-6: Add AGENT.md / CLAUDE.md reading to mastermind Phase 1
**Files:** `agents/mastermind.json`
**What:** In Phase 1 (Decomposition), before producing the plan, add a step: "Read AGENT.md and/or CLAUDE.md in the project root if they exist. Extract coding conventions, style guides, and project-specific rules. Include these as global constraints in the implementation plan so all sub-agents follow them."
**Why:** Superpowers reads these for project conventions. Our port ignores them.

### TODO-7: Add plan-writer awareness and missing-plan detection to mastermind
**Files:** `agents/mastermind.json`
**What:** 
- Add `writing-plans` to the skills_awareness block
- Add `plan-writer` to the available_agents block
- Add a guard at the start of Phase 2: "If no implementation plan exists in docs/plans/, do not proceed. Tell the user to run /write-plan or invoke the plan-writer agent first."
**Why:** If someone goes straight to /execute-plan without a plan file, the mastermind should catch this rather than failing mid-dispatch.

### TODO-8: Add uninstall script
**Files:** New file `uninstall.py`
**What:** Script that:
- Reads the agent names from agents/*.json and removes matching files from ~/.code_puppy/agents/
- Removes ~/.code_puppy/commands/{brainstorm,write-plan,execute-plan,debug,review,finish-branch}.md
- Removes ~/.code_puppy/skills/ (the skills we installed)
- Removes ~/.code_puppy/plugins/superpowers/
- Removes the symlink ~/.code-puppy/commands if it points to ~/.code_puppy/commands
- Confirms before deleting, lists what will be removed
**Why:** Clean uninstall without manual file hunting.

### TODO-9: Update README
**Files:** `README.md`
**What:**
- Remove the manual /pin_model section from the install.py output section (already done but verify)
- Add uninstall instructions pointing to uninstall.py
- Note that models are pinned inline in agent JSON
- Document the AGENT.md/CLAUDE.md integration
- Update the Superpowers → Code Puppy translation table if any mappings changed

### TODO-10: Update install.py summary
**Files:** `install.py`
**What:** Update the post-install summary to reflect all changes (no pin_model, mention AGENT.md support, mention uninstall.py).

---

## Execution Order

Dependency chain means some items should go before others:

1. **TODO-5** (normalize tool lists) — touches all agents, do first to avoid merge conflicts
2. **TODO-1** (fix skill paths) — touches all agents, batch with TODO-5
3. **TODO-4** (fix mastermind role carve-out) — mastermind-only
4. **TODO-6** (add AGENT.md reading) — mastermind-only, do with TODO-4
5. **TODO-7** (add plan-writer awareness) — mastermind-only, do with TODO-4 and TODO-6
6. **TODO-2** (trim implementer-light) — single file, independent
7. **TODO-3** (harden plugin) — single file, independent
8. **TODO-8** (uninstall script) — new file, independent
9. **TODO-9** (README) — do last, after all agent changes are final
10. **TODO-10** (install.py) — do with README

---

## Requires Your Manual Testing (after the above lands)

- **Plugin load test:** Does Code Puppy find and execute ~/.code_puppy/plugins/superpowers/__init__.py on startup?
- **Skill path test:** Switch to brainstormer, ask it to read its skill file. Does `read_file ~/.code_puppy/skills/brainstorming/SKILL.md` resolve?
- **invoke_agent chain test:** Use mastermind on a small task. Does the dispatch → review → revision loop actually work? Does the sub-agent response come back as parseable text?
- **Command discovery test:** Do /brainstorm, /write-plan etc. appear in Code Puppy after install?

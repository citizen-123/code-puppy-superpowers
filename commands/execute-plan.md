# Execute Plan

Execute the most recent implementation plan using sub-agents and two-stage review.

1. Read the plan from docs/plans/.
2. Set up a git worktree for isolated development.
3. For each task: dispatch an implementer agent, then run spec-reviewer (compliance), then quality-reviewer (code quality). Loop revisions until approved.
4. After all tasks pass, run adversarial-reviewer on the full implementation.
5. Finish the branch — merge, PR, keep, or discard.

This command works best with the mastermind agent: /agent mastermind

For the full methodology, read ~/.code_puppy/skills/subagent-driven-development/SKILL.md

# Subagent-Driven Development

Execute implementation plans by dispatching a fresh sub-agent per task with two-stage review after each.

## When This Triggers

When an approved implementation plan exists and the user invokes `/execute-plan` or the mastermind agent. This is the core execution pattern the mastermind follows.

## The Pattern

For each task in the plan:

1. **Dispatch implementer** — Fresh agent gets the full task text, context, and worktree path. Agent implements, tests, commits, and self-reviews.
2. **Spec compliance review** — Separate reviewer agent checks: everything in the spec is present, nothing extra was added.
3. **Code quality review** — Separate reviewer agent checks: quality, naming, tests, DRY, architecture fit.
4. **Revision loop** — If either review fails, the implementer fixes and the reviewer re-reviews. Repeat until approved or escalate after 3 cycles.
5. **Mark complete** — Move to the next task.

After all tasks:
- Dispatch a final adversarial reviewer on the full implementation.
- Use finishing-a-development-branch to complete.

## Key Principles

- **Fresh context per task:** Each sub-agent gets a clean context window. No pollution from previous tasks.
- **Controller provides full text:** The orchestrator reads the plan once, extracts all tasks, and provides complete task text to each sub-agent. Sub-agents never read the plan file themselves.
- **Spec before quality:** Always run spec compliance review first. No point evaluating code quality on incomplete work.
- **Answer questions before proceeding:** If a sub-agent asks a question, answer it before letting them implement.

## Red Flags

- Skipping either review stage.
- Proceeding with unfixed review issues.
- Dispatching multiple implementers in parallel on the same files (conflicts).
- Letting the implementer's self-review replace actual review (both are needed).
- Starting quality review before spec compliance passes.

## Code Puppy Mapping

| Superpowers Concept | Code Puppy Equivalent |
|---|---|
| Implementer subagent | `invoke_agent` → `implementer-heavy` or `implementer-light` |
| Spec reviewer subagent | `invoke_agent` → `spec-reviewer` |
| Code quality reviewer subagent | `invoke_agent` → `quality-reviewer` |
| Final reviewer | `invoke_agent` → `adversarial-reviewer` |
| TodoWrite | Plan file in `docs/plans/` + mastermind state tracking |

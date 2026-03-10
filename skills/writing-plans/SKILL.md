# Writing Plans

Convert approved design documents into granular, executable implementation plans.

## When This Triggers

After a design document has been approved via the brainstorming process. The design doc should exist in `docs/plans/`.

## Process

1. **Read the design** — Understand full scope. Check existing code, patterns, test framework.
2. **Decompose into tasks** — Each task is 2-5 minutes of focused work. Each specifies exact file paths, implementation details, test cases, and verification steps.
3. **Order and group** — Satisfy dependencies. Group parallelizable tasks. Tag each task with agent tier (heavy vs. light).
4. **Write the plan** — Save to `docs/plans/YYYY-MM-DD-<feature-name>.md`. Commit.
5. **Hand off** — Direct user to `/execute-plan` or the mastermind agent.

## Task Quality Rules

- Self-contained: an agent with zero project context can complete a task given only its text.
- Every task includes tests. No exceptions.
- Tests come BEFORE implementation in the task description (TDD order).
- File paths are exact, not approximate.
- No vague instructions ("refactor as needed", "clean up if necessary"). Be specific or omit.
- If a task can't be described precisely in a paragraph, split it further.

## Plan Template

```markdown
# [Feature Name] Implementation Plan
> Execute with /execute-plan or invoke the mastermind agent.

## Summary
[One paragraph: what this builds and why]

## Tasks

### Task 1: [Title]
**Agent:** implementer-heavy | implementer-light
**Dependencies:** none | Task N
**Files:** path/to/file.py
**Tests:** [Specific test cases with expected assertions]
**Implement:** [Precise description of what to build]
**Verify:** [How to confirm completion]
```

## Transitions

- **Previous:** brainstormer agent or `/brainstorm` command
- **Next:** mastermind agent or `/execute-plan` command

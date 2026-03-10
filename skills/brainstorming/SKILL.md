# Brainstorming

Collaborative design refinement through structured dialogue. Runs before any code gets written.

## When This Triggers

Any request to build, create, or add something. Every project goes through this process — a config change gets a short pass, a new system gets a thorough one. None get zero.

## Process

1. **Explore context** — Read project files, docs, recent commits. Understand what exists.
2. **Ask questions** — One at a time. Prefer multiple-choice. Focus on purpose, constraints, success criteria.
3. **Propose 2-3 approaches** — With trade-offs and a recommendation. Wait for the user to choose.
4. **Present design in sections** — Scale detail to complexity. Get approval after each section.
5. **Write design doc** — Save to `docs/plans/YYYY-MM-DD-<topic>-design.md`. Commit.
6. **Transition** — Hand off to plan-writer. Do NOT start implementation.

## Rules

- One question at a time. Do not overwhelm.
- YAGNI ruthlessly. Cut unnecessary features from every design.
- Always propose alternatives before settling.
- The design document must be understandable by someone with no project context.
- Do NOT invoke implementation agents. The only next step is writing-plans.

## Output

Design document committed to `docs/plans/` with architecture, components, data flow, error handling, and testing strategy sections.

## Transitions

- **Next:** plan-writer agent or `/write-plan` command
- **Triggered by:** `/brainstorm` command or automatic detection of build/create intent

# Receiving Code Review

How implementer agents handle review feedback.

## When You Receive Review Findings

1. Read every finding carefully.
2. Fix exactly what's listed. Nothing more, nothing less.
3. Re-run all tests after changes.
4. Update your self-assessment.

## Rules

- Do not refactor adjacent code while fixing review findings.
- Do not add features while fixing review findings.
- If a finding conflicts with the original spec, flag the conflict rather than guessing which is correct.
- If a finding is unclear, ask for clarification rather than interpreting loosely.
- After fixes, the reviewer will re-review. Expect this — it's the process working correctly.

## Responding to Severity Levels

- **CRITICAL / HIGH:** Must fix before the deliverable can be approved.
- **MEDIUM:** Fix if straightforward. If it requires significant rework, note it and let the orchestrator decide.
- **LOW:** Acknowledge. Fix only if trivial.

## Anti-Patterns

- Arguing with review findings instead of fixing them.
- Making unrelated "improvements" alongside fixes (scope creep).
- Marking a finding as fixed without actually verifying the fix works.
- Weakening a test to make a finding go away.

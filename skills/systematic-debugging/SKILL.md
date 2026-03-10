# Systematic Debugging

Hypothesis-driven debugging methodology. Evidence first, changes second.

## When This Triggers

Any bug report, test failure, unexpected behavior, or "this is broken" message.

## Process

1. **Reproduce** — Get exact steps. Run the failing case. Record the error.
2. **Gather evidence** — Read the code path. Check git history. Check test coverage. Grep for TODOs/FIXMEs.
3. **Form hypotheses** — 2-4 ranked hypotheses with supporting evidence and a test to confirm/eliminate each.
4. **Test hypotheses** — Most likely first. One at a time. Record results. Eliminate or confirm.
5. **Fix with TDD** — Write failing test capturing the bug. Write minimal fix. Verify no regressions.
6. **Verify** — Re-run original reproduction steps. Run full test suite.

## Rules

- Never change code based on a hunch. Evidence first.
- Never make multiple changes at once. One hypothesis, one test, one result.
- Never remove a failing test to make the suite pass.
- If a fix introduces new failures, the fix is wrong. Revert.
- Commit messages explain the root cause, not just the symptom.

## Evidence Gathering Commands

```bash
git log --oneline -20 -- <file>        # Recent changes to affected file
git diff HEAD~5 -- <file>              # What changed recently
grep -rn "TODO\|FIXME\|HACK" <dir>    # Known issues in area
```

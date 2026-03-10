# Debug

Begin systematic, hypothesis-driven debugging.

1. Reproduce the bug — get exact steps, expected vs. actual behavior.
2. Gather evidence — read the code path, check git history, grep for TODOs/FIXMEs.
3. Form 2-4 ranked hypotheses with supporting evidence.
4. Test hypotheses one at a time. Most likely first.
5. Once root cause is confirmed: write a failing test, write the minimal fix, verify no regressions.
6. Commit with a message that explains the root cause.

For the full methodology, read ~/.code_puppy/skills/systematic-debugging/SKILL.md

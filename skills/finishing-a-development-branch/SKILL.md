# Finishing a Development Branch

Complete a development branch after all implementation tasks pass review.

## When This Triggers

After all subtasks are approved and integration review passes. The mastermind handles this in Phase 4.

## Process

1. **Verify tests pass** — Run the full suite in the worktree. All tests must pass.
2. **Present options to the user:**
   - **Merge:** Merge the branch into main/master and push.
   - **PR:** Create a pull request for human review.
   - **Keep:** Leave the branch for further work.
   - **Discard:** Delete the branch and all changes.
3. **Execute the chosen option.**
4. **Clean up worktree:** `git worktree remove <path>`

## Rules

- Never merge with failing tests.
- Never auto-merge without user confirmation.
- Always offer all four options — let the user decide.
- Clean up the worktree regardless of which option is chosen (except "Keep").

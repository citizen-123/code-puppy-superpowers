# Using Git Worktrees

Create isolated workspaces for development tasks without switching branches in the main checkout.

## When This Triggers

Before any implementation work begins. The mastermind agent handles worktree creation in Phase 0 — sub-agents receive the worktree path and work inside it.

## Setup Process

1. **Find or create worktree directory:**
   - Check for existing `.worktrees/` or `worktrees/` in the project root (`.worktrees/` wins if both exist).
   - Check `CLAUDE.md` or `AGENT.md` for a preference.
   - If nothing found, ask the user: project-local (`.worktrees/`) or sibling directory (`../<project>-worktrees/`).

2. **Verify gitignore coverage:**
   ```bash
   git check-ignore <worktree_dir>
   ```
   If not ignored, add it to `.gitignore` before proceeding.

3. **Create worktree with descriptive branch:**
   - Naming: `<project>-<purpose>` or `<feature-description>`
   - Examples: `myapp-add-auth-middleware`, `api-refactor-pagination`
   ```bash
   git worktree add <dir>/<branch-name> -b <branch-name>
   ```

4. **Install dependencies:**
   - Detect from project files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`).
   - Run the appropriate install command.

5. **Baseline tests:**
   - Run the test suite. All tests must pass before work begins.
   - Record count: `N tests, 0 failures`.

## Organization Rules

- **Consistent naming:** `<project>-<purpose>` for directories and branches.
- **Dedicated parent directory:** Worktrees live as siblings to the main project or in a dedicated subdirectory. Never nested arbitrarily inside the main worktree.
- **One worktree per task:** Each task gets its own isolated workspace.

## Cleanup

After work is complete (via finishing-a-development-branch):
```bash
git worktree remove <worktree_path>
```

## Common Problems

- Worktree contents pollute `git status` → Always verify gitignore before creating.
- Dependencies not installed → Always run project setup after creating worktree.
- Tests fail on baseline → Report to user before proceeding. Do not ignore.

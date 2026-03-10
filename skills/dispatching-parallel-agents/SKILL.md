# Dispatching Parallel Agents

Run independent sub-agents concurrently for throughput.

## When to Parallelize

Tasks can run in parallel when they have:
- No shared file modifications (different files or different directories)
- No sequential dependencies (Task B doesn't need Task A's output)
- No shared state (no database migrations that affect each other)

## When NOT to Parallelize

- Tasks modify the same files → sequential only
- Task B reads output of Task A → sequential, pass output as context
- Tasks share database state or config → sequential unless isolation is guaranteed
- More than 3 parallel agents → diminishing returns, increased conflict risk

## How the Mastermind Handles This

The mastermind's implementation plan groups tasks into `parallel_group` sets:

```
execution_order:
  - parallel_group: 1
    subtask_ids: [subtask-01, subtask-02]    # independent, run together
  - parallel_group: 2
    subtask_ids: [subtask-03]                # depends on group 1
```

Each sub-agent in a parallel group receives the same worktree path but works on different files. The mastermind waits for all agents in a group to complete before dispatching the next group.

## Conflict Prevention

- Verify file-level independence before dispatching in parallel.
- If two tasks touch the same file, move one to the next sequential group.
- Each parallel agent commits its own changes. The orchestrator resolves any merge issues before proceeding.

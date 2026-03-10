# Requesting Code Review

How the orchestrator structures and dispatches code reviews.

## Two-Stage Review

Every deliverable goes through two independent reviews in sequence:

### Stage 1: Spec Compliance (spec-reviewer agent)

Checks exactly two things:
- **MISSING:** Is anything in the spec absent from the deliverable?
- **EXTRA:** Is anything in the deliverable not requested by the spec?

Both are failures. The reviewer does not evaluate quality — only compliance.

### Stage 2: Code Quality (quality-reviewer agent)

Evaluates against six dimensions:
1. Test quality — meaningful tests, behavior-focused, good failure messages
2. Code clarity — naming, readability, cognitive complexity
3. Error handling — failure modes at boundaries, informative errors
4. DRY / reuse — no duplication, use existing utilities
5. Architecture fit — follows project patterns, consistent abstraction level
6. Documentation — public APIs documented, non-obvious decisions commented

Findings are severity-ranked: CRITICAL, HIGH, MEDIUM, LOW.

## Review Flow

1. Dispatch spec-reviewer with the subtask spec and deliverable.
2. If NON_COMPLIANT: route back to implementer with specific findings. Re-review after fix.
3. If COMPLIANT: dispatch quality-reviewer.
4. If CRITICAL or HIGH findings: route back to implementer. Re-review after fix.
5. MEDIUM and LOW: note but do not block.
6. Max 3 revision cycles before escalating to the user.

## Rules

- Spec compliance ALWAYS comes before quality review.
- Each review stage is a separate agent invocation (fresh context).
- Reviewers do not suggest improvements outside their lane.
- Every finding needs a specific, actionable recommendation.

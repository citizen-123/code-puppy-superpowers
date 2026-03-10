# Test-Driven Development

Strict RED-GREEN-REFACTOR cycle for all implementation work.

## The Cycle

1. **RED** — Write a failing test that captures the requirement. Run it. Watch it fail. If it passes, your test is wrong.
2. **GREEN** — Write the minimum code to make the test pass. Nothing more.
3. **REFACTOR** — Clean up while keeping tests green. Extract functions, rename variables, remove duplication.
4. **COMMIT** — After each green phase.

## Rules

- If you write implementation code before its corresponding test, delete the code and start over.
- Each acceptance criterion gets at least one test.
- Tests assert behavior, not implementation details.
- Test failure messages should be descriptive enough to diagnose the problem without reading the test code.
- Edge cases get tests: empty inputs, boundaries, error paths.
- Never delete or weaken a test to make the suite pass.

## Running Tests

- Run the full suite after every GREEN phase.
- If a refactor breaks a test, the refactor is wrong — revert it.
- Report test count and pass/fail status in every deliverable.

## Anti-Patterns

- Writing tests after implementation (not TDD).
- Tests that test the framework, not your code.
- Tests that pass regardless of implementation (tautological).
- Mocking everything — mock at boundaries, test real logic.
- Skipping the RED step (how do you know the test catches anything?).

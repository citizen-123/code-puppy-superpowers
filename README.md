# Mastermind Agent Constellation

Multi-agent orchestration system for Code Puppy. The Mastermind decomposes tasks, dispatches specialized sub-agents, and drives iterative review until quality gates pass.

## Architecture

```mermaid
graph TD
    M["<b>MASTERMIND</b><br/><i>Opus</i><br/>Orchestrator"]

    subgraph impl ["Implementation Tier"]
        IH["<b>implementer-heavy</b><br/><i>Sonnet</i><br/>Complex tasks · TDD · Worktrees"]
        IL["<b>implementer-light</b><br/><i>Haiku</i><br/>Mechanical tasks · Fast & cheap"]
    end

    subgraph rev ["Review Tier"]
        SR["<b>spec-reviewer</b><br/><i>Sonnet</i><br/>Spec compliance"]
        QR["<b>quality-reviewer</b><br/><i>Sonnet</i><br/>Code quality"]
        AR["<b>adversarial-reviewer</b><br/><i>Opus</i><br/>Break everything"]
    end

    M -- "invoke_agents" --> IH
    M -- "invoke_agents" --> IL
    M -- "invoke_agents" --> SR
    M -- "invoke_agents" --> QR
    M -- "invoke_agents" --> AR

    IH -. "deliverable" .-> SR
    IL -. "deliverable" .-> SR
    SR -. "if compliant" .-> QR
    QR -. "all subtasks approved" .-> AR

    style M fill:#6e44ff,stroke:#4a2db5,color:#fff
    style IH fill:#3b82f6,stroke:#2563eb,color:#fff
    style IL fill:#22c55e,stroke:#16a34a,color:#fff
    style SR fill:#f59e0b,stroke:#d97706,color:#fff
    style QR fill:#f59e0b,stroke:#d97706,color:#fff
    style AR fill:#ef4444,stroke:#dc2626,color:#fff
    style impl fill:#f0f4ff,stroke:#93c5fd
    style rev fill:#fef9ee,stroke:#fcd34d
```

## Workflow

```mermaid
flowchart TD
    START(["User provides task"]) --> PLAN
    PLAN["<b>Phase 1: Decomposition</b><br/>Mastermind produces plan"] --> APPROVE{User approves?}
    APPROVE -- "No" --> PLAN
    APPROVE -- "Yes" --> DISPATCH

    subgraph phase2 ["Phase 2: Implementation Loop"]
        DISPATCH["Dispatch implementer<br/><i>heavy or light</i>"] --> IMPL["Agent implements subtask"]
        IMPL --> SPEC{"spec-reviewer<br/>COMPLIANT?"}
        SPEC -- "No" --> REVISE_SPEC["Implementer fixes<br/>spec gaps"]
        REVISE_SPEC --> SPEC
        SPEC -- "Yes" --> QUAL{"quality-reviewer<br/>CRITICAL/HIGH?"}
        QUAL -- "Yes" --> REVISE_QUAL["Implementer fixes<br/>quality issues"]
        REVISE_QUAL --> QUAL
        QUAL -- "No" --> DONE_SUB["Subtask approved"]
    end

    DONE_SUB --> MORE{More subtasks?}
    MORE -- "Yes" --> DISPATCH
    MORE -- "No" --> INTEGRATION

    subgraph phase3 ["Phase 3: Integration Review"]
        INTEGRATION["<b>adversarial-reviewer</b><br/>attacks full implementation"] --> PASS{CRITICAL/HIGH<br/>findings?}
        PASS -- "Yes" --> FIX["Route to implementer<br/>for remediation"]
        FIX --> INTEGRATION
        PASS -- "No" --> DELIVER
    end

    DELIVER(["Deliver final output"])

    style START fill:#6e44ff,stroke:#4a2db5,color:#fff
    style DELIVER fill:#22c55e,stroke:#16a34a,color:#fff
    style phase2 fill:#f0f4ff,stroke:#93c5fd
    style phase3 fill:#fef2f2,stroke:#fca5a5
```

## Agents

| Agent | Model | Role |
|---|---|---|
| `mastermind` | Opus | Decomposes tasks, dispatches agents, reviews, synthesizes |
| `implementer-heavy` | Sonnet | Complex implementation: multi-file, architecture, TDD |
| `implementer-light` | Haiku | Mechanical tasks: config, boilerplate, simple edits |
| `spec-reviewer` | Sonnet | Binary spec compliance: COMPLIANT / NON_COMPLIANT |
| `quality-reviewer` | Sonnet | Code quality with severity-ranked findings |
| `adversarial-reviewer` | Opus | Tries to break everything. The paranoid one. |

## Setup

### 1. Copy agents into place

```bash
cp agents/*.json ~/.code_puppy/agents/
```

### 2. Pin models

In Code Puppy, use `/pin_model` to assign each agent its model:

```
/pin_model mastermind           → claude-opus-4-6
/pin_model implementer-heavy    → claude-sonnet-4-6
/pin_model implementer-light    → claude-haiku-4-5
/pin_model spec-reviewer        → claude-sonnet-4-6
/pin_model quality-reviewer     → claude-sonnet-4-6
/pin_model adversarial-reviewer → claude-opus-4-6
```

### 3. Switch to mastermind

```
/agent mastermind
```

### 4. Activate skills

The agents reference these skills — install them if you haven't:

```bash
# obra/superpowers (TDD, worktrees, SDD, finishing branches)
# Install via your preferred method — plugin marketplace or manual

# NeoLabHQ/context-engineering-kit (DDD, SADD)
/plugin install ddd@NeoLabHQ/context-engineering-kit
/plugin install sadd@NeoLabHQ/context-engineering-kit
```

## Workflow

**Phase 1 — Decomposition**: Mastermind analyzes your task, produces an implementation plan with subtasks, agent assignments, dependencies, and execution order. Presents for approval.

**Phase 2 — Implementation**: For each subtask, Mastermind dispatches the assigned implementer, then runs spec-reviewer → quality-reviewer in sequence. Revisions loop up to 3 times before escalating.

**Phase 3 — Integration Review**: After all subtasks pass, adversarial-reviewer attacks the full implementation. CRITICAL/HIGH findings trigger targeted fixes and re-review.

## Agent Selection Heuristic

The Mastermind picks agents based on subtask characteristics:

**implementer-heavy** (Sonnet) when:
- Multi-file changes
- New modules, classes, or architectural components
- Algorithmic complexity or nuanced logic
- Integration work across subsystems
- Decisions requiring judgment

**implementer-light** (Haiku) when:
- Single-file edits with clear instructions
- Config/env changes
- Boilerplate generation
- Renaming/moving
- Documentation updates
- Mechanical refactors (pattern already established)

## Cost Optimization Notes

- Haiku is ~60x cheaper than Opus per token. Route aggressively to `implementer-light` for mechanical work.
- Spec-reviewer and quality-reviewer on Sonnet are a deliberate tradeoff: they need enough capability to catch real issues but run on every subtask, so cost matters.
- Adversarial-reviewer on Opus is justified: it runs once at integration time and needs deep reasoning to find subtle bugs.
- If revision loops are firing frequently on Haiku tasks, the subtask scoping is probably too loose. Tighten the spec rather than upgrading the model.

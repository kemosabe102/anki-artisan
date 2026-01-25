---
name: test-driven-development
description: >
  Use this skill when implementing components using RED-GREEN-REFACTOR cycle.
  Provides 5-phase workflow, Definition of Done checklists, and quality gates.
  Trigger keywords: TDD, test-driven development, red-green-refactor, RED phase,
  GREEN phase, REFACTOR phase, write failing test, make test pass, test cycle.
---

# Test-Driven Development Skill

Build components incrementally using the RED-GREEN-REFACTOR cycle with atomic commits and quality gates.

## Reference Documentation

- **Phase 1: RED** -> [reference/phase-1-red.md](reference/phase-1-red.md)
- **Phase 2: GREEN** -> [reference/phase-2-green.md](reference/phase-2-green.md)
- **Phase 3: REFACTOR** -> [reference/phase-3-refactor.md](reference/phase-3-refactor.md)
- **Phase 4: Self-Review** -> [reference/phase-4-self-review.md](reference/phase-4-self-review.md)
- **Phase 5: Commit** -> [reference/phase-5-commit.md](reference/phase-5-commit.md)
- **Anti-Patterns** -> [reference/anti-patterns.md](reference/anti-patterns.md)

**Templates**:
- **Workflow Status Tracker** -> [templates/workflow-status.md](templates/workflow-status.md)

---

## Quick Reference: TDD Phases

| Phase | Duration | Output | Success Criteria |
|-------|----------|--------|------------------|
| **1: RED** | 5-15 min | Failing test | Test fails for right reason |
| **2: GREEN** | 10-30 min | Implementation | All tests pass |
| **3: REFACTOR** | 10-20 min | Clean code | Tests pass, code readable |
| **4: REVIEW** | 5-10 min | Verified component | No debug code, >80% coverage |
| **5: COMMIT** | 3-5 min | Atomic commit | Clear message, pushed |

---

## RED-GREEN-REFACTOR Flow

```
┌─────────────────────────────────────────────────────┐
│                   PER COMPONENT                     │
│  ┌─────┐    ┌───────┐    ┌──────────┐              │
│  │ RED │───>│ GREEN │───>│ REFACTOR │              │
│  └─────┘    └───────┘    └──────────┘              │
│     ^                          │                    │
│     │    More tests needed?    │                    │
│     └──────────YES─────────────┘                    │
│                                │                    │
│                               NO                    │
│                                v                    │
│                     ┌────────────────┐              │
│                     │  SELF-REVIEW   │              │
│                     └────────────────┘              │
│                                │                    │
│                                v                    │
│                     ┌────────────────┐              │
│                     │    COMMIT      │              │
│                     └────────────────┘              │
│                                │                    │
└────────────────────────────────┼────────────────────┘
                                 │
            More components?     │
            YES ─────────────────┘ (back to RED)
            NO  ─────────────────> Done
```

---

## Anti-Patterns Summary

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Writing all tests first | Batch coding, hard to debug | One test at a time: RED->GREEN->REFACTOR |
| Skipping REFACTOR | Code debt accumulates | REFACTOR is mandatory, not optional |
| Big tests (multiple behaviors) | Unclear failures | One test = one behavior |

See [reference/anti-patterns.md](reference/anti-patterns.md) for full list.

---

## Key Philosophy

- **Small components**: One component per cycle (40-90 min)
- **Test-first**: Write failing test before any implementation
- **Atomic commits**: One logical change per commit
- **Quality gates**: Definition of Done checklists at each phase
- **Continuous verification**: All tests pass after every change
- **No untested components**: If it's not tested, it doesn't exist

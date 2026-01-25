---
name: python-implementation
description: >
  Use this skill when implementing Python code with TDD-first methodology.
  Provides enforcement gates for quality assurance, defensive programming
  patterns, and test-first workflow guidance. Trigger keywords: implement,
  TDD, test-first, python, enforcement gates, defensive programming,
  mutable defaults, red-green-refactor.
---

# Python Implementation Skill

You are a senior software engineer implementing single, focused Python tasks with TDD-first methodology and strict quality gates.

## Core Philosophy

**Tests define the implementation contract.** Simple tests lead to well-designed code.

```
Task received -> Pre-flight checks -> Find/create tests -> Implement -> Self-review -> Report
```

## Reference Documentation

**Detailed Guides** (read when relevant):
- **TDD Workflow** -> [reference/tdd-workflow.md](reference/tdd-workflow.md)
- **Enforcement Gates** -> [reference/enforcement-gates.md](reference/enforcement-gates.md)
- **Defensive Programming** -> [reference/defensive-programming.md](reference/defensive-programming.md)

**Utility Scripts**:
- **TDD Compliance Validator** -> `scripts/validate_tdd_compliance.py <impl_file>`
  - Validates test coverage of public interfaces
  - Checks defensive programming patterns
  - Returns JSON compliance report

**Project Standards** (if available):
- `docs/04-guides/code-review/coding-guidelines.md`
- `docs/00-project/COMPONENT_ALMANAC.md`

---

## Quick Reference: 5 Enforcement Gates

| Gate | HALT Condition | Priority |
|------|----------------|----------|
| Ambiguity Detection | Clarity score <= 2 | 1 (highest) |
| Scope Boundary | File not in declared_scope | 2 |
| COMPONENT_ALMANAC | Creating component without check | 3 |
| TDD-First | No tests before implementation | 4 |
| Defensive Programming | Mutable defaults, bare exceptions | 5 |

---

## Implementation Flow

### Pre-Flight (MANDATORY)
1. Read `docs/04-guides/code-review/coding-guidelines.md`
2. Read `docs/00-project/COMPONENT_ALMANAC.md`
3. Search for existing tests: `Grep("test.*<module_name>", path="tests/")`

### TDD Cycle
1. **RED**: Write failing test first
2. **GREEN**: Implement minimal code to pass
3. **REFACTOR**: Clean up with test safety net

### Self-Review Checklist
- [ ] Correctness: Verified by tests
- [ ] Security: All 7 patterns addressed
- [ ] Defensive: DP-02, DP-03, DP-10 verified
- [ ] Linter: Clean output from ruff

---

## Anti-Patterns (NEVER DO)

- Implement without reading tests first
- Add features beyond task scope
- Use mutable default arguments (`def foo(items=[])`)
- Swallow exceptions with empty `except: pass`
- Process collections without empty check

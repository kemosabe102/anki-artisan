# Python Code Reviewer Documentation

This directory contains detailed documentation for the python-code-reviewer agent.

## Contents

| File | Purpose |
|------|---------|
| `workflow-phases.md` | Detailed OODA loop phases with timing and sub-steps |
| `review-dimensions.md` | Review dimension guide references and validation approach |

## External References (Shared - Do Not Duplicate)

The following documentation lives in the project's shared `docs/` directory and is used by multiple agents:

### Primary Code Review Guides
- `docs/04-guides/code-review/python-code-review-checklist.md` - Primary checklist (MANDATORY every review)
- `docs/04-guides/code-review/coding-guidelines.md` - PEP 8, naming, structure

### Dimension-Specific Guides
- `docs/04-guides/code-review/python-security-patterns.md` - OWASP Top 10, LLM Top 10
- `docs/04-guides/code-review/python-testing-standards.md` - AAA pattern, coverage
- `docs/04-guides/code-review/python-type-safety.md` - Type hints, generics
- `docs/04-guides/code-review/python-performance-patterns.md` - Async, caching, N+1
- `docs/04-guides/code-review/python-exception-handling.md` - Error propagation
- `docs/04-guides/code-review/code-testability.md` - DI patterns, seams
- `docs/04-guides/code-review/oop-design-patterns-code-review.md` - SOLID principles
- `docs/04-guides/code-review/dependency-injection-and-modular-design-principles.md` - Architecture

### Base Pattern
- `.claude/docs/01-guides/agents/base-agent-pattern.md` - Inherited agent patterns

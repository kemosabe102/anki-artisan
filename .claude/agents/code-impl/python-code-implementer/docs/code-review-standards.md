# Code Review Standards for Self-Review

Apply these standards during self-review to prevent common issues flagged by python-code-reviewer.

---

## Security Pre-Flight

- **Path validation**: Use `pathlib.Path.resolve()` + `.relative_to()` for boundary checks
- **Subprocess**: NEVER `shell=True`, use list args (`["cmd", "arg"]`)
- **Regex**: Avoid nested quantifiers (`(a+)+`), use atomic groups for backtracking prevention
- **User input**: Whitelist validation over blacklist (e.g., `str.isalnum()` before file paths)

Reference: `docs/04-guides/code-review/python-security-patterns.md`

---

## Exception Handling

- Order exceptions specific → generic (`FileNotFoundError` before `OSError`)
- ALWAYS catch `PermissionError`, `FileNotFoundError`, `IsADirectoryError` for file ops
- Use context managers (`with` statements) for resource cleanup

Reference: `docs/04-guides/code-review/python-exception-handling.md`

---

## Type Hints (MANDATORY)

- ALL public functions require parameter and return type hints
- Use Pydantic models for complex returns (>3 values or nested structures)
- Run `mypy` before implementation completion

Reference: `docs/04-guides/code-review/python-type-safety.md`

---

## Testing Standards (TDD-First)

> **Note**: TDD protocol and schema requirements defined in main agent > Enforcement Gates > TDD-First Gate.

- **Tests define the implementation contract** - understand or create tests FIRST
- Write tests BEFORE implementation code (TDD workflow is MANDATORY)
- Security tests required for validation code
- AAA pattern (Arrange-Act-Assert), meaningful assertion messages
- Simple tests lead to well-designed, testable code
- ≥80% coverage target for `packages/**`

Reference: `docs/04-guides/code-review/python-testing-standards.md`

---

## Performance Patterns

- Compile regex at module level (`PATTERN = re.compile(r"...")`)
- Use generators over `list()` for large datasets
- Context managers for file operations (automatic resource cleanup)

Reference: `docs/04-guides/code-review/python-performance-patterns.md`

---

## Object-Oriented Design

- Apply SOLID principles
- Use design patterns appropriately (Factory, Strategy, Observer)
- Favor composition over inheritance
- Avoid anti-patterns (God Object, Anemic Domain Model)

Reference: `docs/04-guides/code-review/oop-design-patterns-code-review.md`

---

## Self-Review Checklist

Before returning results, validate:

| Category | Check |
|----------|-------|
| **Correctness** | Does code meet task acceptance criteria? Tests pass? |
| **Readability** | Meaningful names, docstrings for non-trivial logic? |
| **Maintainability** | No duplication, small cohesive functions, single responsibility? |
| **Security** | Path validation, subprocess safety, regex safety, input whitelisting? |
| **Performance** | Compiled regex, generators, context managers? |
| **Standards** | Linters clean, mypy passes, ≥80% coverage? |
| **Surface area** | Minimal API changes, no unnecessary public exposure? |

---

## Implementation Rules (Hard Guardrails)

- **No over-engineering**: Avoid unnecessary patterns or new dependencies
- **Small, readable changes**: Meaningful names, small functions, clear control flow
- **Error handling**: Explicit failure modes, no blanket catch unless policy allows
- **Dependency hygiene**: Do not add libs unless justified and allowed
- **Touch only scoped files**: No drive-by refactors
- **Prevent duplication**: Build on existing components

---

## Minimal Implementation Heuristics

- Prefer composition over inheritance; pure functions where possible
- Avoid feature flags/config unless explicitly required
- Avoid premature caching or async unless required by acceptance criteria
- Choose the clearest data structure (dict > custom class unless justified)

# Review Dimensions Reference

Quick reference for which external guide to consult based on change type.

## Primary References (Active Documentation)

| Dimension | Guide | Key Focus |
|-----------|-------|-----------|
| **Code Quality** | `docs/04-guides/code-review/coding-guidelines.md` | PEP 8, naming, structure, clarity |
| **Type Safety** | `docs/04-guides/code-review/python-type-safety.md` | Type hints, generic types, Protocol usage |
| **Testing** | `docs/04-guides/code-review/python-testing-standards.md` | Coverage, AAA pattern, fixture scoping |
| **Security** | `docs/04-guides/code-review/python-security-patterns.md` | OWASP Top 10, LLM Top 10, input validation |
| **Performance** | `docs/04-guides/code-review/python-performance-patterns.md` | Async/await, caching, N+1 queries |
| **Exception Handling** | `docs/04-guides/code-review/python-exception-handling.md` | Error propagation, context preservation |
| **Testability** | `docs/04-guides/code-review/code-testability.md` | DI patterns, seams, test isolation |
| **Design Patterns** | `docs/04-guides/code-review/oop-design-patterns-code-review.md` | SOLID principles, pattern usage |
| **Architecture** | `docs/04-guides/code-review/dependency-injection-and-modular-design-principles.md` | Layering, coupling |

## Validation Approach

1. **Identify Dimensions**: From git diff, determine which dimensions apply
   - Security changes → consult `python-security-patterns.md`
   - Test changes → consult `python-testing-standards.md`
   - API changes → consult `coding-guidelines.md` + security

2. **Context7 Validation**: Verify findings against official library documentation (when confidence <0.9)

3. **Cross-Reference**: Use dimension-specific guides above for detailed patterns

4. **Apply Finding Gates**: Ensure high-signal feedback

## Verification Pattern Examples

### Async not awaited
```python
Wrong: r = startAsyncOp()  # used immediately
Correct: r = await startAsyncOp()
Verification: rg -n "startAsyncOp\s*\(" | grep -v 'await'
```

### Nullable safety
```python
Wrong: return input.value  # no nullability contract
Correct: Use Optional type hints, explicit unwraps, or idiomatic guards
Verification: Context7-guided static rule + minimal harness passing None
```

### Missing error handling
```python
Wrong: response = client.get(url)  # unhandled exceptions
Correct: try/except with specific exception types
Verification: rg "\.get\(" | grep -v "try:"
```

## Research Tool Selection

| Scenario | Confidence | Tool Selection |
|----------|------------|----------------|
| Finding validation | Any | **Context7 FIRST** |
| High-quality docs | ≥0.9 | Context7 ONLY (STOP) |
| Medium confidence | 0.75-0.89 | Context7 + validation |
| Low confidence | <0.75 | **Perplexity escalation** |
| Context7 FAILURE | Any | **Perplexity** (fallback) |

Target 4:1 Context7:Perplexity ratio (cost-optimized).

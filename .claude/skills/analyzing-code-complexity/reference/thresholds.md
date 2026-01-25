# Complexity Thresholds Reference

Industry-standard thresholds for code complexity metrics.

---

## Cyclomatic Complexity

Measures the number of linearly independent paths through code.

| Value | Risk Level | Action |
|-------|------------|--------|
| 1-5 | Low | Maintainable, no action needed |
| 6-10 | Moderate | Monitor, consider simplification |
| 11-20 | High | Refactor recommended |
| 21-50 | Very High | Refactor required |
| >50 | Untestable | Immediate refactoring critical |

**Calculation**: Count decision points (if, else, elif, switch, case, while, for, foreach, catch, and, or) + 1

---

## Function Length

Lines of code per function/method.

| Lines | Risk Level | Action |
|-------|------------|--------|
| 1-15 | Ideal | SIG low-risk benchmark |
| 16-30 | Good | Maintainable |
| 31-50 | Acceptable | Monitor growth |
| 51-100 | High | Refactor into smaller functions |
| >100 | Critical | Immediate split required |

**Best Practice**: Functions should do one thing well (Single Responsibility)

---

## Nesting Depth

Maximum indentation levels within a function.

| Depth | Risk Level | Action |
|-------|------------|--------|
| 0-2 | Ideal | Easy to read and test |
| 3 | Acceptable | Threshold for most standards |
| 4 | Code Smell | Extract nested logic |
| >4 | Critical | Refactor immediately |

**Detection**: Count indentation levels (typically 4 spaces = 1 level)

---

## Parameter Count

Number of parameters per function.

| Count | Risk Level | Action |
|-------|------------|--------|
| 0-3 | Ideal | SIG low-risk benchmark |
| 4-5 | Acceptable | Consider parameter object |
| 6-7 | High | Use parameter object or builder |
| >7 | Critical | Refactor required |

---

## SIG Maintainability Model

Software Improvement Group benchmarks for low-risk code:

| Metric | Low-Risk Threshold | Measurement |
|--------|-------------------|-------------|
| Unit Complexity | <15 | Cyclomatic complexity per unit |
| Unit Size | <15 LOC | Lines per unit |
| Unit Interfacing | <4 params | Parameters per unit |
| Module Coupling | <10 imports | Dependencies per module |

---

## Language-Specific Adjustments

### Python
- Use 4 spaces per indentation level for nesting calculation
- Include comprehensions in complexity count
- Count `try/except/finally` blocks

### JavaScript/TypeScript
- Count arrow functions as units
- Include callback chains in nesting depth
- Count ternary operators in complexity

### Go
- Include `defer` statements in complexity
- Count goroutine spawns as decision points

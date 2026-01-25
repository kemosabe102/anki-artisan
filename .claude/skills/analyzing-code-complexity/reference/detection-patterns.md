# Detection Patterns Reference

Grep and analysis patterns for measuring code complexity metrics.

---

## Cyclomatic Complexity Detection

### Decision Point Pattern (Python)

```bash
# Count decision points in Python files
grep -rn '\b(if|elif|else|while|for|except|and|or|with)\b' <scope> --include="*.py" | wc -l
```

### Decision Point Pattern (JavaScript/TypeScript)

```bash
# Count decision points in JS/TS files
grep -rn '\b(if|else|switch|case|while|for|catch|&&|\|\||\?)\b' <scope> --include="*.{js,ts,jsx,tsx}" | wc -l
```

### Decision Point Pattern (Go)

```bash
# Count decision points in Go files
grep -rn '\b(if|else|switch|case|for|select|defer)\b' <scope> --include="*.go" | wc -l
```

**Formula**: Complexity = Decision Points + 1

---

## Function Length Detection

### Python Function Boundaries

```bash
# Find function definitions with line numbers
grep -n '^\s*def \|^\s*async def ' <file>
```

### JavaScript/TypeScript Function Boundaries

```bash
# Find function definitions
grep -n 'function \|^\s*\w\+\s*=\s*(' <file>
grep -n '=>' <file>  # Arrow functions
```

### Calculate LOC Between Functions

```python
# Pseudocode for LOC calculation
for each function_start_line:
    next_function_line = find_next_function_or_eof()
    loc = next_function_line - function_start_line
    if loc > 50:
        flag_for_refactoring(function_name, loc)
```

---

## Nesting Depth Detection

### Indentation-Based Pattern

```bash
# Lines with >3 levels of nesting (4 spaces per level = 12+ spaces)
grep -E '^\s{12,}' <file> | wc -l

# Lines with >4 levels (16+ spaces)
grep -E '^\s{16,}' <file> | wc -l
```

### Tab-Based Indentation

```bash
# Lines with >3 tabs
grep -E '^\t{4,}' <file> | wc -l
```

### Mixed Indentation Detection

```bash
# Detect inconsistent indentation (potential issues)
grep -E '^(\t+ +| +\t)' <file>
```

---

## Parameter Count Detection

### Python Parameters

```bash
# Functions with many parameters
grep -E 'def \w+\([^)]{50,}\)' <file>
```

### Accurate Parameter Counting

```python
# Pseudocode for parameter counting
import ast

for func in ast.walk(tree):
    if isinstance(func, ast.FunctionDef):
        param_count = len(func.args.args) + len(func.args.kwonlyargs)
        if param_count > 4:
            flag_excessive_parameters(func.name, param_count)
```

---

## Composite Complexity Score

```bash
# Run all metrics in parallel for a directory
grep -rn '\b(if|elif|else|while|for|except|and|or)\b' <scope> --include="*.py" > /tmp/decisions.txt &
grep -rn '^\s*def ' <scope> --include="*.py" > /tmp/functions.txt &
grep -rE '^\s{12,}' <scope> --include="*.py" > /tmp/nesting.txt &
wait
```

---

## Output Format

Detection results should be structured as:

```json
{
  "file": "<path>",
  "line": 0,
  "metric": "complexity|length|nesting|params",
  "value": 0,
  "context": "<surrounding code snippet>"
}
```

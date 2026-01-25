# Code Duplication Analysis Reference

Methods for detecting and quantifying code duplication as technical debt.

---

## Threshold

| Duplication % | Risk Level | Action |
|---------------|------------|--------|
| 0-3% | Acceptable | Normal code reuse |
| 3-5% | Monitor | Review for extraction opportunities |
| 5-10% | Technical Debt | Plan refactoring |
| >10% | Critical | Immediate refactoring required |

**Industry Standard**: >5% duplication = technical debt flag

---

## Detection Types

### 1. Exact Duplicates (Type 1)

Identical code fragments (ignoring whitespace and comments).

```bash
# Find exact duplicate lines (simplified)
sort <file> | uniq -d | wc -l

# Find duplicate lines with context
sort <file> | uniq -c | sort -rn | head -20
```

### 2. Renamed Duplicates (Type 2)

Identical structure with different identifiers.

```bash
# Normalize identifiers and compare
sed 's/\b[a-z_][a-z0-9_]*\b/VAR/gi' <file> | sort | uniq -d
```

### 3. Structural Duplicates (Type 3)

Similar structure with some modifications.

```bash
# Function signature similarity
grep -E '(def|function|func) \w+\(' <file> | sort | uniq -cd

# Find similar function signatures
grep -hE '^\s*(def|async def) \w+\(' packages/**/*.py | \
  sed 's/def \w\+/def FUNC/' | sort | uniq -c | sort -rn
```

---

## Duplication Calculation

```
Duplication % = (Duplicated Lines / Total Lines) * 100
```

### Calculation Steps

1. **Extract Code Blocks**: Identify logical blocks (functions, classes)
2. **Normalize**: Remove whitespace, comments, standardize formatting
3. **Hash Comparison**: Generate hashes for blocks of N lines (typically 6+)
4. **Match Detection**: Find blocks with identical hashes
5. **Percentage Calculation**: Sum duplicated lines / total lines

---

## Common Duplication Patterns

### Copy-Paste Code

```python
# Indicator: Similar function bodies
def process_user(user):
    validate(user)
    transform(user)
    save(user)

def process_order(order):  # Near-duplicate
    validate(order)
    transform(order)
    save(order)
```

**Refactoring**: Extract generic `process_entity()` function

### Repeated Validation

```python
# Indicator: Same validation logic in multiple places
if not data:
    raise ValueError("Data required")
if not isinstance(data, dict):
    raise TypeError("Dict expected")
```

**Refactoring**: Create validation decorator or utility

### Boilerplate Patterns

```python
# Indicator: Repeated setup/teardown code
try:
    conn = get_connection()
    # ... different operations ...
finally:
    conn.close()
```

**Refactoring**: Use context managers

---

## Detection Commands

### Quick Duplicate Scan

```bash
# Find files with high internal duplication
for f in packages/**/*.py; do
  total=$(wc -l < "$f")
  unique=$(sort "$f" | uniq | wc -l)
  dup_pct=$((100 - (unique * 100 / total)))
  if [ $dup_pct -gt 5 ]; then
    echo "$f: ${dup_pct}% duplication"
  fi
done
```

### Cross-File Duplication

```bash
# Find lines duplicated across files
sort packages/**/*.py | uniq -d > /tmp/dup_lines.txt
grep -rFf /tmp/dup_lines.txt packages/ --include="*.py" | \
  cut -d: -f1 | sort | uniq -c | sort -rn
```

---

## Output Format

```json
{
  "duplication_pct": 0.0,
  "duplicated_lines": 0,
  "total_lines": 0,
  "clusters": [
    {
      "hash": "<block-hash>",
      "occurrences": [
        {"file": "<path>", "start_line": 0, "end_line": 0}
      ],
      "lines": 0
    }
  ]
}
```

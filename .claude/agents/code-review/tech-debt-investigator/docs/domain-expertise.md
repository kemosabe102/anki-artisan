# Domain Expertise: Metric Collection Patterns

Detailed metric collection patterns, thresholds, and quantitative analysis methods.

---

## Complexity Metrics (Code Quality Category)

### Cyclomatic Complexity Detection
```bash
# Count decision points
grep -rn '\b(if|else|elif|switch|case|while|for|foreach|catch|and|or)\b' <scope> | wc -l

# Function length (lines per function)
grep -n 'def \|function \|func ' <file>  # Count LOC between definitions

# Nesting depth (>3 levels = code smell)
grep -E '^\s{12,}' <file> | wc -l  # Lines with >3 levels (4 spaces per level)
```

**Thresholds**:
- Cyclomatic complexity >10 = high risk
- Function >50 lines = needs refactoring
- Nesting >3 levels = code smell

---

## Duplication Metrics (Code Quality Category)

```bash
# Exact duplicate blocks (simplified)
sort <file> | uniq -d | wc -l

# Structural similarity (function signatures)
grep -E '(def|function|func) \w+\(' <file> | sort | uniq -cd
```

**Threshold**: >5% duplication = technical debt

---

## Coverage Metrics (Testing Category)

```bash
# Test/implementation ratio
test_funcs=$(grep -rn 'def test_\|it(\|describe(' tests/ | wc -l)
impl_funcs=$(grep -rn 'def \|function ' packages/ | wc -l)
coverage_pct=$((test_funcs * 100 / impl_funcs))

# Untested modules
comm -23 <(ls packages/**/*.py | sed 's|packages/||') <(ls tests/**/*.py | sed 's|test_||;s|tests/||')
```

**Threshold**: <80% coverage = technical debt

---

## Dependency Metrics (Infrastructure Category)

```bash
# Outdated dependencies
grep -E '==' requirements.txt  # Compare against latest versions

# Deprecated APIs
grep -rn 'apiVersion: apps/v1beta1' k8s/  # Flag deprecated API versions
```

---

## Documentation Metrics

```bash
# Docstring coverage
funcs_total=$(grep -rn 'def \|function ' packages/ | wc -l)
funcs_documented=$(grep -B1 'def \|function ' packages/ | grep -E '"""|\'\'\'' | wc -l)
docstring_coverage_pct=$((funcs_documented * 100 / funcs_total))

# Missing README files
find . -type d -maxdepth 2 ! -path '*/.git/*' ! -path '*/node_modules/*' -exec test ! -e {}/README.md \; -print
```

---

## Git-Based Historical Metrics

### Code Churn (Hotspot Detection)
```bash
# High-churn files in 3-month window
git log --since="3 months ago" --name-only --format="" | sort | uniq -c | sort -rn | head -20
```

### Ownership Dispersion
```bash
# Contributors per file (low ownership = higher defect risk)
git shortlog -sn --since="6 months ago" -- <file>
```

### Recurrent Churn
```bash
# Files changed month-over-month
for month in {0..2}; do
  git log --since="$month months ago" --until="$((month+1)) months ago" --name-only --format="" | sort -u
done | sort | uniq -c | awk '$1 >= 3'
```

### Defect Density
```bash
# Correlate with bug IDs
git log --grep="BUG-\|fixes #" --since="6 months ago"
```

---

## Architectural Coupling

```bash
# Import dependency analysis
grep -rn '^import \|^from .* import' packages/ | cut -d: -f2 | sort | uniq -c

# Circular dependency detection requires graph traversal logic
```

---

## Parallel Execution Guidelines

**Parallelize**:
- Multiple file reads across independent modules
- Grep for different debt categories (complexity + duplication + coverage)
- Independent git log operations (churn + ownership)

**Serialize**:
- Sequential OODA phases (output feeds next step)
- Connection graph building (needs full context)
- Priority ranking (comparative analysis)
- Composite debt_score (requires all category scores)

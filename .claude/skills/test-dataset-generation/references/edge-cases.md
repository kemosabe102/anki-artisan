# Edge Cases Reference

Seven required edge case types for test dataset diversity.

---

## Required Edge Cases (7/7 Coverage)

### 1. mixed_change_types

**Definition**: Single commit with multiple Conventional Commit types

**Examples**:
- `feat(api): add endpoint + fix(auth): resolve token bug`
- `refactor(db): optimize + docs: update API docs`

**Identification**:
```bash
git log --oneline -150 | grep -E "(feat|fix).*\+(fix|docs|test)"
```

**Ground Truth**: Separate by change type prefix, create distinct groups

---

### 2. test_only_changes

**Definition**: Commit modifying exclusively test files

**Examples**:
- `test: add missing unit tests`
- `test: improve coverage for auth module`

**Identification**:
```bash
git log --name-only -150 | awk '/^commit/,/^$/ {if (/^tests\//) print}'
```

**Ground Truth**: Group by test module or feature under test

---

### 3. large_repository_50_files

**Definition**: Commit changing 50+ files

**Examples**:
- Version bumps
- Mass refactoring
- Code formatting

**Identification**:
```bash
git log --stat -150 | awk '/files changed/ && $1 >= 50 {print}'
```

**Ground Truth**: Detect bulk operations, create umbrella group or directory-based subgroups

---

### 4. low_confidence_ambiguous

**Definition**: Scenarios with confidence < 0.70, multiple valid interpretations

**Examples**:
- Unrelated files in single commit
- Cross-cutting concerns
- Experimental code

**Identification**:
```bash
git log --name-only -150 | awk '/^commit/,/^$/ {if (/\.py$|\.md$|\.yaml$/) print}'
```

**Ground Truth**: Generate multiple groupings, flag with lowest confidence

---

### 5. renamed_deleted_files

**Definition**: Commits with rename (R) or delete (D) operations

**Examples**:
- `refactor: rename auth.py -> authentication.py`
- `chore: remove deprecated endpoints`

**Identification**:
```bash
git log --diff-filter=R --diff-filter=D --name-status -150
```

**Ground Truth**: Track renames through identity, group deletions by purpose

---

### 6. ungrouped_files

**Definition**: Files that don't fit into logical groups (singletons)

**Examples**:
- `.gitignore` changes
- Isolated typo fixes
- Standalone utility scripts

**Identification**:
```bash
git log --stat -150 | awk '/1 file changed|2 files changed/ {print}'
```

**Ground Truth**: Allow singletons when grouping confidence < 0.70

---

### 7. dependency_ordering

**Definition**: Files with strict dependency relationships

**Examples**:
- Database migrations (001_create.sql -> 002_add.sql)
- Module initialization (__init__.py)
- Build system changes

**Identification**:
```bash
git log --name-only -150 | grep -E "(migrations/|__init__\.py)"
```

**Ground Truth**: Build dependency graph, perform topological sort

---

## Validation Checklist

```python
edge_cases_required = [
    "mixed_change_types",
    "test_only_changes",
    "large_repository_50_files",
    "low_confidence_ambiguous",
    "renamed_deleted_files",
    "ungrouped_files",
    "dependency_ordering"
]

def validate_coverage(scenarios):
    covered = set()
    for s in scenarios:
        covered.update(s.edge_case_tags)
    
    missing = set(edge_cases_required) - covered
    return {
        "covered": list(covered),
        "missing": list(missing),
        "ratio": len(covered) / 7,
        "passed": len(missing) == 0
    }
```

---

## Requirements

- 7/7 edge cases covered (100%)
- At least 1 scenario per edge case
- Mined from real git history (not synthetic)
- Ground truth confidence >= 0.70 or flagged low_confidence

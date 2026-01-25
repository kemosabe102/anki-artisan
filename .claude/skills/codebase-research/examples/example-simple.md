# Example: Simple Codebase Research

**Scenario**: "Find where ConfigLoader is used in the codebase"

---

## Request Analysis

- **Type**: Needle query (specific identifier)
- **Scope**: Single symbol lookup
- **Expected Tools**: Grep → Read

---

## Execution

### Step 1: Find all occurrences

```
Tool: Grep
Pattern: "ConfigLoader"
Output Mode: files_with_matches
```

**Result**:
```
packages/core/config/loader.py       # Definition
packages/core/config/__init__.py     # Export
packages/core/app.py                 # Usage
tests/unit/config/test_loader.py     # Tests
```

### Step 2: Read definition (understand what it does)

```
Tool: Read
File: packages/core/config/loader.py
Limit: 100 (class definition + key methods)
```

**Result**: Class with `load()`, `validate()`, `merge()` methods

### Step 3: Read primary usage (understand how it's used)

```
Tool: Read
File: packages/core/app.py
Offset: [line where ConfigLoader appears]
Limit: 30 (surrounding context)
```

---

## Findings Output

```markdown
## ConfigLoader Usage Analysis

**Definition**: `packages/core/config/loader.py:15`
- Class: `ConfigLoader`
- Methods: `load()`, `validate()`, `merge()`
- Purpose: Load and validate YAML/JSON configuration files

**Usages** (3 locations):
1. `packages/core/app.py:42` - Application startup
2. `packages/core/config/__init__.py:5` - Public export
3. `tests/unit/config/test_loader.py` - Unit tests (12 test cases)

**Confidence**: 0.95 (all usages found via direct symbol search)
```

---

## Tool Calls Summary

| Tool | Calls | Purpose |
|------|-------|---------|
| Grep | 1 | Find all occurrences |
| Read | 2 | Definition + primary usage |
| **Total** | **3** | |

**Time**: ~5 seconds

# Defensive Programming Reference

## Quick Reference Principles

| Principle | Definition | When to Apply |
|-----------|------------|---------------|
| **Anticipate Failures** | Assume errors will occur | External input, API calls, storage reads |
| **Fail Gracefully** | Catch specific exceptions | Error handling, resource cleanup |
| **Validate All Inputs** | Check type, range, format | Public APIs, external data |
| **Least Privilege** | Minimum access required | API design, DB access, file ops |
| **Default to Safe/Deny** | Deny unless granted | Security decisions, initialization |

---

## DP-02: Mutable Defaults Anti-Pattern (CRITICAL)

### The Problem

In Python, mutable default values are evaluated once when the function is defined:

```python
def add_item(item, collection=[]):  # WRONG
    collection.append(item)
    return collection

result1 = add_item("apple")   # ["apple"]
result2 = add_item("banana")  # ["apple", "banana"] - UNEXPECTED!
```

### The Solution: None Sentinel

```python
def add_item(item, collection=None):
    if collection is None:
        collection = []
    collection.append(item)
    return collection

result1 = add_item("apple")   # ["apple"]
result2 = add_item("banana")  # ["banana"] - Correct!
```


### Detection Patterns

**Red flags (mutable defaults):**
```python
def func(data=[]):           # List default
def func(config={}):         # Dict default
def func(items=set()):       # Set default
def func(obj=SomeClass()):   # Object default
```

**Safe defaults:**
```python
def func(data=None):         # None
def func(config="default"):  # String (immutable)
def func(items=()):          # Tuple (immutable)
def func(enabled=True):      # Boolean
def func(count=0):           # Number
```

---

## DP-03: Exception Handling

### Bad Pattern
```python
try:
    risky_operation()
except Exception:  # Too broad
    pass  # Silent failure - NEVER DO THIS
```

### Good Pattern
```python
try:
    risky_operation()
except ValueError as e:
    logger.warning(f"Invalid value: {e}")
    return default_value
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    raise  # Re-raise for caller to handle
```

### Rules
- Catch specific exceptions only
- Never use bare `except:` or `except Exception:`
- Log or handle errors (no silent `pass`)
- Include context in error messages

---

## DP-10: Input Validation at Entry Points

### Public Functions MUST Validate

```python
def process_user_data(user_id: int, data: dict) -> Result:
    # Validate at entry point
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError(f"user_id must be positive int, got {user_id}")
    if not isinstance(data, dict):
        raise TypeError(f"data must be dict, got {type(data)}")
    if "required_field" not in data:
        raise ValueError("data missing required_field")
    
    # Now safe to proceed
    return _internal_process(user_id, data)
```

### Internal Functions May Skip
```python
def _internal_process(user_id: int, data: dict) -> Result:
    # Skip validation - caller already validated
    # Document as "N/A: internal function" in evidence
    ...
```

---

## Complete Checklist

| ID | Check | Evidence Required |
|----|-------|-------------------|
| DP-01 | Inputs validated: type, range, format | Line numbers |
| DP-02 | No mutable defaults: None sentinel used | Grep result empty |
| DP-03 | Specific exceptions: no bare except | Exception types listed |
| DP-04 | Error context: logs include diagnostics | Logger calls shown |
| DP-05 | Graceful degradation: recovery logic | Try/except documented |
| DP-06 | Safe defaults: deny-by-default | Default values favor security |
| DP-07 | Resource cleanup: context managers | `with` statements used |
| DP-08 | API design: invalid states unrepresentable | Required params in __init__ |
| DP-09 | Explicit over implicit | Validation raises, not corrects |
| DP-10 | Fail fast: validation at entry points | Validation before logic |
| DP-11 | No silent failures: errors surfaced | No empty except:pass |
| DP-12 | Type hints: present for public APIs | -> ReturnType on all |

---

## Security Pre-Flight (MANDATORY for ACT phase)

| Pattern | Verification | Evidence |
|---------|--------------|----------|
| Path Validation | `pathlib.Path.resolve()` + `.relative_to()` | Lines OR "N/A: no user paths" |
| Subprocess Safety | NO `shell=True`; use list args | Lines OR "N/A: no subprocess" |
| Regex Safety | No nested quantifiers; compile at module level | Lines OR "N/A: no regex" |
| Input Validation | Whitelist before file paths, SQL params | Lines OR "N/A: no external input" |
| Secret Handling | No hardcoded credentials | "Verified: no secrets" |
| Mutable Defaults | No `[]`, `{}`, `set()` defaults | Grep result OR "N/A" |
| Empty Collections | Check `.empty` or `len()` before aggregation | Lines OR "N/A" |

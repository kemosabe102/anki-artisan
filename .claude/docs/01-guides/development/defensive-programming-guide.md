---
title: "Defensive Programming Guide"
date: 2025-12-03
status: ACTIVE
tags: [python, defensive-programming, code-quality, mutable-defaults]
canonical_for: [mutable-defaults-antipattern, defensive-programming-checklist]
audience: [development, code-quality]
---

# Defensive Programming Guide

> Reference for defensive programming practices. Load before implementation tasks.

## Quick Reference

| Principle | Definition | When to Apply |
|-----------|------------|---------------|
| **Anticipate Failures** | Assume errors will occur; never trust external input | External input, API calls, storage reads |
| **Fail Gracefully** | Catch specific exceptions, provide context-rich errors | Error handling, resource cleanup, user-facing ops |
| **Validate All Inputs** | Check type, range, format, state before processing | Public APIs, external data, form submissions |
| **Least Privilege** | Minimum access required; immutable when possible | API design, DB access, file ops, state management |
| **Default to Safe/Deny** | Deny unless granted; fail closed not open | Security decisions, initialization, permissions |

---

## Mutable Defaults Anti-Pattern (CANONICAL)

**This section is the canonical reference for Python mutable default arguments.**

### Problem

In Python, mutable default values are evaluated once when the function is defined, not each time the function is called.

**What happens:**

```python
def add_item(item, collection=[]):  # WRONG
    collection.append(item)
    return collection

# First call
result1 = add_item("apple")
print(result1)  # ["apple"]

# Second call - UNEXPECTED!
result2 = add_item("banana")
print(result2)  # ["apple", "banana"] - same list!
```

The default list is created once and reused for all function calls. Any mutations affect all future calls.

### Solution 1: Use None as Sentinel (Recommended)

```python
def add_item(item, collection=None):
    if collection is None:
        collection = []
    collection.append(item)
    return collection

# Now each call gets a fresh list
result1 = add_item("apple")
print(result1)  # ["apple"]

result2 = add_item("banana")
print(result2)  # ["banana"]
```

**Why this works**: None is immutable. Inside the function, a new list is created if None is passed.

### Solution 2: Use Type-Specific Factories

```python
def process_data(data, config=None, cache=None):
    if config is None:
        config = {}
    if cache is None:
        cache = []

    # Process with fresh defaults
    return {"data": data, "config": config, "cache": cache}
```

**When to use**: When you have multiple mutable parameters.

### Solution 3: Use Factory Functions

```python
def add_items(items, collection_factory=None):
    if collection_factory is None:
        collection_factory = list  # Use list constructor as factory

    collection = collection_factory()
    for item in items:
        collection.append(item)
    return collection

# Caller can provide custom factory
custom_result = add_items(["a", "b"], collection_factory=lambda: ["default"])
```

**When to use**: When maximum flexibility is needed; less common.

### Solution 4: Use Type Hints + Documentation

```python
from typing import Optional, List

def add_item(item: str, collection: Optional[List[str]] = None) -> List[str]:
    """
    Add item to collection.

    Args:
        item: Item to add
        collection: Optional list. If None, new list created. NEVER mutate default.

    Returns:
        Updated collection (note: may be same object if passed in)
    """
    if collection is None:
        collection = []
    collection.append(item)
    return collection
```

**When to use**: Always. Type hints + clear documentation prevent misuse.

### Detection: What to Look For

**Red flags (mutable default problem):**

```python
def func(data=[]):           # List default
def func(config={}):         # Dict default
def func(items=set()):       # Set default
def func(obj=SomeClass()):   # Object default
```

**Safe defaults:**

```python
def func(data=None):         # None
def func(config="default"):  # String
def func(items=()):          # Tuple (immutable)
def func(enabled=True):      # Boolean
def func(count=0):           # Number
```

---

## Defensive Programming Checklist

| ID | Check | Evidence Required |
|----|-------|-------------------|
| DP-01 | Inputs validated: type, range, format | Line numbers where validation occurs |
| DP-02 | No mutable defaults: None sentinel used | Grep for `=[]`, `={}`, `=set()` returns empty |
| DP-03 | Specific exceptions: no bare `except Exception` | Exception types match failure modes |
| DP-04 | Error context: logs include diagnostic info | Logger calls with `extra={}` or f-string context |
| DP-05 | Graceful degradation: recoverable vs fatal clear | Try/except with recovery logic documented |
| DP-06 | Safe defaults: deny-by-default config | Default values favor security over convenience |
| DP-07 | Resource cleanup: context managers used | `with` statements for files, connections, locks |
| DP-08 | API design: invalid states unrepresentable | Required params in `__init__`, no None-able required fields |
| DP-09 | Explicit over implicit: no silent assumptions | Validation raises, not silently corrects |
| DP-10 | Fail fast: validation at entry points | Validation before business logic |
| DP-11 | No silent failures: errors logged/surfaced | No empty `except: pass` blocks |
| DP-12 | Type hints: present for public APIs | `-> ReturnType` on all public functions |

---

## Cross-References (Authoritative Sources)

For detailed patterns on these topics, consult the canonical documents:

| Topic | Canonical Doc | Key Sections |
|-------|---------------|--------------|
| Exception Handling | `docs/04-guides/code-review/python-exception-handling.md` | Patterns 1-5, Error Categories, Resource Management |
| Input Validation | `docs/04-guides/code-review/python-security-patterns.md` | InputValidator class, Path validation |
| Path Traversal | `docs/04-guides/code-review/python-security-patterns.md` | Section 1: Defense-in-depth validation |
| SQL Injection | `docs/04-guides/code-review/python-security-patterns.md` | Parameterized queries pattern |
| Error Logging | `docs/04-guides/code-review/python-exception-handling.md` | Logging standards, what to log/not log |

**Load Order for Implementation Tasks:**
1. This guide (quick reference, mutable defaults)
2. `python-exception-handling.md` (if error handling needed)
3. `python-security-patterns.md` (if security-sensitive input)

# Common Issues Reference

Quick reference for frequently encountered Python anti-patterns and their fixes.

## Table of Contents

1. [Mutable Default Arguments](#mutable-default-arguments)
2. [Identity vs Equality](#identity-vs-equality)
3. [Assertion Misuse](#assertion-misuse)
4. [Bare Exception Handler](#bare-exception-handler)
5. [Exception Ordering](#exception-ordering)
6. [Missing Type Hints](#missing-type-hints)
7. [Deprecated Patterns](#deprecated-patterns)
8. [Global Mutable State](#global-mutable-state)

---

## Mutable Default Arguments

**Problem:** Default list/dict mutates across function calls

```python
# ❌ BAD - Default list persists and grows
def append_to(item, target=[]):
    target.append(item)
    return target

append_to(1)  # 
append_to(2)  # [1, 2] - Unexpected!

# ✅ GOOD - Use None sentinel pattern
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

**Why:** Default arguments are evaluated once at function definition, not each call. Mutable defaults (list, dict, set) retain modifications.

---

## Identity vs Equality

**Problem:** Using `is` for value comparison instead of `==`

```python
# ❌ BAD - Unreliable due to Python's integer caching
if x is 256:    # May work (cached range -5 to 256)
    pass
if x is 257:    # Will fail unpredictably
    pass
if name is "admin":  # String interning is implementation-dependent
    pass

# ✅ GOOD - Use == for value comparison
if x == 256:
    pass
if name == "admin":
    pass

# ✅ CORRECT use of 'is' - only for singletons
if value is None:
    pass
if flag is True:
    pass
if result is NotImplemented:
    pass
```

**Why:** `is` checks object identity (same memory address), not value equality. Only use `is` for `None`, `True`, `False`, and sentinel objects.

---

## Assertion Misuse

**Problem:** Using `assert` for runtime validation in production

```python
# ❌ BAD - Assertions disabled with python -O
def process_payment(amount):
    assert amount > 0, "Amount must be positive"  # SKIPPED IN PRODUCTION!
    charge_card(amount)

def validate_user(user_id):
    assert isinstance(user_id, int)  # SKIPPED!
    return get_user(user_id)

# ✅ GOOD - Explicit validation with exceptions
def process_payment(amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    charge_card(amount)

def validate_user(user_id):
    if not isinstance(user_id, int):
        raise TypeError(f"user_id must be int, got {type(user_id)}")
    return get_user(user_id)
```

**Why:** Python's `-O` flag disables all assertions. Critical checks must use explicit `if/raise`.

---

## Bare Exception Handler

**Problem:** Catching all exceptions silently hides bugs

```python
# ❌ BAD - Catches everything including KeyboardInterrupt, SystemExit
try:
    risky_operation()
except:
    pass  # Silent failure - impossible to debug

# ❌ ALSO BAD - Too broad, masks different errors
try:
    data = fetch_and_parse()
except Exception:
    return None  # Was it network error? Parse error? Bug?

# ✅ GOOD - Catch specific exceptions
try:
    data = fetch_and_parse()
except requests.RequestException as e:
    logger.warning(f"Network error: {e}")
    return None
except json.JSONDecodeError as e:
    logger.error(f"Parse error: {e}")
    raise
except Exception as e:
    logger.exception("Unexpected error")
    raise  # Re-raise unexpected errors
```

**Why:** Broad exception handling masks bugs, makes debugging impossible, and can catch system signals.

---

## Exception Ordering

**Problem:** Parent exceptions caught before specific children

```python
# ❌ BAD - ValueError never reached (RuntimeError is parent)
try:
    operation()
except RuntimeError:
    handle_runtime()
except ValueError:  # Never reached if ValueError is a subclass!
    handle_value()

# ❌ BAD - Specific exception shadowed
try:
    operation()
except Exception:
    handle_all()
except FileNotFoundError:  # Never reached!
    handle_missing_file()

# ✅ GOOD - Most specific first
try:
    operation()
except FileNotFoundError:
    handle_missing_file()
except PermissionError:
    handle_permission()
except OSError:
    handle_os_error()
except Exception:
    handle_unexpected()
```

**Why:** Python matches exceptions in order. Parent classes catch their children first.

---

## Missing Type Hints

**Problem:** Functions without type annotations

```python
# ❌ BAD - No type information
def process_items(items, limit):
    return items[:limit]

def get_user(user_id):
    return db.query(User).get(user_id)

# ✅ GOOD - Complete type annotations
def process_items(items: list[str], limit: int) -> list[str]:
    return items[:limit]

def get_user(user_id: int) -> User | None:
    return db.query(User).get(user_id)

# ✅ GOOD - Complex types with TypeVar
from typing import TypeVar, Sequence

T = TypeVar("T")

def first_or_none(items: Sequence[T]) -> T | None:
    return items[0] if items else None
```

**Why:** Type hints enable static analysis, IDE support, and serve as documentation.

---

## Deprecated Patterns

### Python 3.10+ Deprecations

```python
# ❌ BAD - Old typing imports (deprecated 3.9+)
from typing import List, Dict, Optional, Union

def process(items: List[str]) -> Dict[str, int]:
    pass

# ✅ GOOD - Use built-in generics
def process(items: list[str]) -> dict[str, int]:
    pass

# ❌ BAD - Union type syntax
def get_value() -> Union[str, None]:
    pass

# ✅ GOOD - Pipe syntax (3.10+)
def get_value() -> str | None:
    pass
```

### Removed Modules (Python 3.12+)

```python
# ❌ BAD - Removed in Python 3.12+
import imp          # Use importlib
import distutils    # Use setuptools
import cgi          # Use urllib.parse, html
import audioop      # Removed
import telnetlib    # Use third-party library
```

### Collections ABC

```python
# ❌ BAD - Deprecated since 3.3
from collections import Mapping, Sequence

# ✅ GOOD
from collections.abc import Mapping, Sequence
```

---

## Global Mutable State

**Problem:** Functions that depend on or modify global state

```python
# ❌ BAD - Hidden dependency on global
config = {}

def process_data(data):
    if config.get("debug"):  # Hidden dependency
        print(data)
    return transform(data, config["settings"])  # May fail if not set

# ✅ GOOD - Explicit dependencies
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    debug: bool = False
    settings: dict = None

def process_data(data: dict, config: Config) -> dict:
    if config.debug:
        print(data)
    return transform(data, config.settings)
```

**Why:** Global state creates hidden coupling, makes testing difficult, and causes unpredictable behavior.

---

## Quick Reference Table

| Issue | Detection | Fix |
|-------|-----------|-----|
| Mutable default | `def f(x=[])` | Use `None` sentinel |
| Identity check | `x is 100` | Use `==` for values |
| Assert for validation | `assert x > 0` | Use `if/raise` |
| Bare except | `except:` or `except Exception` | Catch specific types |
| Wrong exception order | Parent before child | Most specific first |
| Missing type hints | No `: type` annotations | Add full annotations |
| Old typing imports | `from typing import List` | Use `list[...]` |
| Deprecated modules | `import imp` | Use modern alternatives |
| Global mutable state | Module-level `config = {}` | Inject dependencies |

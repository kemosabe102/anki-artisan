# Mock Decision Tree Reference

## When to Mock

```
Should I mock this dependency?
         │
         ▼
┌─────────────────────────────────┐
│ Is it EXTERNAL?                 │
│ (API, DB, filesystem, network)  │
└─────────────────────────────────┘
         │
    ┌────┴────┐
    │YES      │NO
    ▼         ▼
  MOCK    ┌──────────────────────────┐
          │ Is it SLOW (>100ms)?     │
          └──────────────────────────┘
                    │
               ┌────┴────┐
               │YES      │NO
               ▼         ▼
             MOCK    ┌──────────────────────────┐
                     │ Is it NON-DETERMINISTIC? │
                     │ (time, random, UUID)     │
                     └──────────────────────────┘
                              │
                         ┌────┴────┐
                         │YES      │NO
                         ▼         ▼
                       MOCK    ┌──────────────────────────┐
                               │ Is it the CODE UNDER TEST?│
                               └──────────────────────────┘
                                        │
                                   ┌────┴────┐
                                   │YES      │NO
                                   ▼         ▼
                              DON'T MOCK   USE REAL
```

---

## Mock Types

| Type | Use Case | Example |
|------|----------|---------|
| `Mock()` | Generic mock object | `mock = Mock()` |
| `MagicMock()` | Mock with magic methods | `mock = MagicMock()` |
| `patch()` | Replace module attribute | `@patch('module.func')` |
| `patch.object()` | Replace object attribute | `@patch.object(obj, 'method')` |

---

## Basic Mocking Patterns

### Return Value
```python
mock_db = Mock()
mock_db.get_user.return_value = User(id=1, name="test")

result = mock_db.get_user(1)
assert result.name == "test"
```

### Side Effect (Exception)
```python
mock_api = Mock()
mock_api.fetch.side_effect = ConnectionError("timeout")

with pytest.raises(ConnectionError):
    mock_api.fetch()
```

### Side Effect (Multiple Returns)
```python
mock_counter = Mock()
mock_counter.next.side_effect = [1, 2, 3]

assert mock_counter.next() == 1
assert mock_counter.next() == 2
assert mock_counter.next() == 3
```

---

## Patch Decorator

```python
from unittest.mock import patch

@patch('mymodule.external_api.fetch_data')
def test_service_handles_api_response(mock_fetch):
    mock_fetch.return_value = {"status": "ok"}
    
    service = MyService()
    result = service.process()
    
    assert result == "processed"
    mock_fetch.assert_called_once()
```

---

## Verifying Mock Calls

```python
mock_db = Mock()
service = UserService(db=mock_db)
service.get_user(123)

# Verify call happened
mock_db.get_user.assert_called()
mock_db.get_user.assert_called_once()
mock_db.get_user.assert_called_with(123)
mock_db.get_user.assert_called_once_with(123)

# Check call count
assert mock_db.get_user.call_count == 1

# Check all calls
mock_db.get_user.assert_has_calls([call(123), call(456)])
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Mocking the code under test | Not testing real behavior | Mock dependencies only |
| Over-mocking | Tests pass but code is broken | Use integration tests |
| Mocking implementation details | Brittle tests | Mock at boundaries |
| Not verifying mock calls | Tests don't prove behavior | Add assertions |

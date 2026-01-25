# Test Independence Validation Reference

## Why Test Independence Matters

Independent tests:
- Can run in any order
- Can run in parallel
- Give reliable results
- Are easier to debug

Dependent tests:
- Fail randomly based on order
- Can't parallelize safely
- Hide real bugs
- Waste debugging time

---

## Independence Validation Protocol

### Step 1: Run Test in Isolation

```bash
# Run single test
uv run pytest tests/unit/test_auth.py::test_login_success -v
```

Record result: PASS or FAIL

### Step 2: Run in Full Suite

```bash
# Run full test file
uv run pytest tests/unit/test_auth.py -v
```

Record result: PASS or FAIL

### Step 3: Compare Results

| Isolated | Suite | Conclusion |
|----------|-------|------------|
| PASS | PASS | ✅ Independent |
| FAIL | FAIL | ✅ Independent (but broken) |
| PASS | FAIL | ⚠️ Order-dependent |
| FAIL | PASS | ⚠️ Relies on other test's side effect |

---

## Common Independence Issues

### Shared State
```python
# BAD: Tests share mutable state
_cache = {}

def test_add_to_cache():
    _cache["key"] = "value"
    assert _cache["key"] == "value"

def test_cache_empty():
    assert len(_cache) == 0  # FAILS if test_add runs first
```

**Fix**: Reset state in fixture or each test.

### Database State
```python
# BAD: Tests rely on database state
def test_create_user():
    create_user("test@example.com")
    
def test_user_exists():
    user = get_user("test@example.com")  # FAILS in isolation
    assert user is not None
```

**Fix**: Each test creates its own data.

### File System State
```python
# BAD: Tests share files
def test_write_file():
    Path("output.txt").write_text("data")
    
def test_read_file():
    content = Path("output.txt").read_text()  # FAILS in isolation
    assert content == "data"
```

**Fix**: Use temp directories, clean up in fixtures.

---

## Randomized Order Testing

Verify independence by running tests in random order:

```bash
# Install pytest-random-order
uv pip install pytest-random-order

# Run with random order
uv run pytest --random-order

# Run with specific seed (reproducible)
uv run pytest --random-order-seed=12345
```

If tests pass in default order but fail randomly, you have order dependencies.

---

## Independence Checklist

- [ ] Test passes when run alone
- [ ] Test passes when run in full suite
- [ ] Test passes with `--random-order`
- [ ] Test doesn't modify global state
- [ ] Test doesn't rely on other tests' side effects
- [ ] Test cleans up its own resources

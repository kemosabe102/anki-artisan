# Fixture Design Reference

## Scope Selection Matrix

| Scope | Lifetime | Use When |
|-------|----------|----------|
| `function` | Each test | Fresh state needed per test |
| `class` | All tests in class | Expensive setup, read-only sharing |
| `module` | All tests in file | One-time file-level setup |
| `session` | Entire test run | Global setup (DB schema, etc.) |

**Default**: Use `function` scope unless you have a specific reason not to.

---

## Basic Fixture Pattern

```python
import pytest

@pytest.fixture
def user():
    """Create a test user."""
    return User(id=1, name="test_user", role="member")

@pytest.fixture
def admin_user():
    """Create an admin user."""
    return User(id=2, name="admin", role="admin")

def test_user_can_read(user):
    assert user.can_perform("read") is True

def test_admin_can_delete(admin_user):
    assert admin_user.can_perform("delete") is True
```

---

## Fixture with Cleanup

```python
@pytest.fixture
def temp_file():
    """Create and clean up a temporary file."""
    # Setup
    path = Path("/tmp/test_file.txt")
    path.write_text("test content")
    
    yield path  # Provide to test
    
    # Teardown (always runs)
    if path.exists():
        path.unlink()
```

---

## Parameterized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def database(request):
    """Test against multiple database backends."""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.close()

def test_query_works(database):
    # Runs 3 times, once per database type
    result = database.query("SELECT 1")
    assert result is not None
```

---

## Fixture Dependencies

```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture
def user_repository(db_connection):
    # Depends on db_connection fixture
    return UserRepository(db_connection)

@pytest.fixture
def user_service(user_repository):
    # Depends on user_repository fixture
    return UserService(user_repository)
```

---

## conftest.py Organization

```
tests/
├── conftest.py           # Shared fixtures for all tests
├── unit/
│   ├── conftest.py       # Unit test specific fixtures
│   └── test_auth.py
└── integration/
    ├── conftest.py       # Integration test fixtures
    └── test_api.py
```

Fixtures in parent conftest.py are available to all child directories.

---

## Best Practices

| Practice | Reason |
|----------|--------|
| Use smallest scope possible | Prevents test pollution |
| Always clean up resources | Prevents resource leaks |
| Name fixtures clearly | Self-documenting tests |
| Avoid fixture side effects | Predictable behavior |
| Prefer composition | Build complex from simple |

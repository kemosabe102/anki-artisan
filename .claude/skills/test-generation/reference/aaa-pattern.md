# AAA Pattern Reference

## Structure

```python
def test_<method>_<condition>_<expected_outcome>():
    """Verify <what> when <condition>."""
    
    # Arrange - Set up test data and dependencies
    # All setup code goes here
    
    # Act - Execute the code under test
    # Single action being tested
    
    # Assert - Verify the outcome
    # Check results match expectations
```

---

## Arrange Phase

Set up everything needed for the test:
- Create test data
- Configure mocks
- Set up fixtures
- Initialize dependencies

```python
# Arrange
user = User(name="test_user", role="admin")
mock_db = Mock()
mock_db.get_user.return_value = user
service = UserService(db=mock_db)
```

**Rule**: Keep arrange focused - if setup is complex, use fixtures.

---

## Act Phase

Execute the code under test:
- Single function/method call
- Clear, focused action
- Capture result if needed

```python
# Act
result = service.authorize(user_id=123, action="delete")
```

**Rule**: One action per test. Multiple actions = multiple tests.

---

## Assert Phase

Verify the outcome:
- Check return values
- Verify mock calls
- Assert state changes

```python
# Assert
assert result.allowed is True
assert result.reason == "admin_role"
mock_db.get_user.assert_called_once_with(123)
```

**Rule**: One logical assertion. Multiple related checks are OK.

---

## Complete Example

```python
def test_authorize_admin_user_for_delete_returns_allowed():
    """Verify admin users can perform delete actions."""
    
    # Arrange
    admin_user = User(id=123, name="admin", role="admin")
    mock_repository = Mock()
    mock_repository.get_user.return_value = admin_user
    auth_service = AuthorizationService(user_repo=mock_repository)
    
    # Act
    result = auth_service.authorize(user_id=123, action="delete")
    
    # Assert
    assert result.allowed is True
    assert result.reason == "admin_role_permits_delete"
    mock_repository.get_user.assert_called_once_with(123)
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Multiple acts | Testing too much | Split into separate tests |
| Assert in arrange | Confusing flow | Move to assert phase |
| No clear separation | Hard to read | Add comment markers |
| Complex assertions | Hard to debug | One logical check |

# Phase 2A: RED - Write Failing Test

**Goal:** Define expected behavior through a failing test.

---

## Activities

1. **Write ONE test** for the next small piece of functionality
   - Test name should express the behavior clearly
   - Example: `test_password_hash_returns_different_value_than_input`
   - NOT: `test_password_hash`

2. **Test structure (language-agnostic template):**
   ```
   Test Name: Clearly describes expected behavior
   Setup: Create test inputs/mocks
   Action: Call the function/method you're testing
   Assert: Verify the result matches expectation
   ```

3. **Consider scope:**
   - One test = one specific behavior
   - Test happy path OR edge case, not both
   - Example: One test for "valid input", separate test for "empty input"


4. **Run the test:**
   ```bash
   npm test       # JavaScript
   pytest -v      # Python
   go test        # Go
   cargo test     # Rust
   ```
   - Test MUST FAIL
   - Failure message should be clear (not "undefined is not a function")

---

## Definition of Done (Move to GREEN when)

- [ ] Test file created or updated with new test
- [ ] Test name clearly describes expected behavior
- [ ] Test covers ONE specific behavior
- [ ] Test FAILS when you run it (shows test is working)
- [ ] Failure message is informative (e.g., "Expected 'password123' to not equal 'password123'")
- [ ] You understand exactly what code will make this test pass
- [ ] No test is skipped (no `@Skip`, `xit`, `.skip`, etc.)

---

## Time Investment

5-15 minutes per test (mostly thinking, not typing)

---

## Related Skills to Invoke

- **debugging-methodology** (if test fails for syntax reasons instead of logic)
- **code-review-standards** (if team has specific test naming conventions)

# Phase 2B: GREEN - Make Test Pass

**Goal:** Write minimal code to make the failing test pass.

---

## Activities

1. **Write the simplest code possible** that makes the test pass
   - Focus ONLY on the specific behavior tested
   - Avoid premature optimization
   - Resist adding "nice-to-have" features not covered by tests
   - Ugly/simple is better than elegant/over-engineered

2. **Example (Python):**
   ```python
   # RED test written:
   def test_password_hash_differs_from_input():
       result = hash_password("password123")
       assert result != "password123"
   
   # GREEN implementation (minimal):
   import hashlib
   
   def hash_password(password):
       return hashlib.sha256(password.encode()).hexdigest()
   ```


3. **Run ALL tests (not just the new one):**
   ```bash
   npm test  # Ensure no regressions
   ```

4. **If test still fails:**
   - Debug: Does the function exist? Does it take the right parameters?
   - Check test assertion logic (is it actually testable?)
   - Don't skip; fix it before moving to REFACTOR

---

## Definition of Done (Move to REFACTOR when)

- [ ] The test you wrote in RED now PASSES
- [ ] ALL previous tests still PASS (no regressions)
- [ ] Code implements the specific behavior, nothing more
- [ ] No unused variables or dead code
- [ ] No hardcoded test data
- [ ] Function/method signature is reasonable (not accepting test-specific parameters)
- [ ] You resisted the urge to add "extra" features

---

## Time Investment

10-30 minutes per test (coding + debugging if needed)

---

## Related Skills to Invoke

- **debugging-methodology** (if test fails unexpectedly)

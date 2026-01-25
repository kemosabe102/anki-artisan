# Phase 2C: REFACTOR - Improve Code Quality

**Goal:** Clean up code while maintaining all passing tests.

---

## Activities

1. **Review the code you just wrote:**
   - Is there duplicated logic with other functions?
   - Are variable names clear?
   - Are there obvious code smells?

2. **Common refactoring patterns:**
   - Extract magic strings/numbers to named constants
   - Extract complex logic to helper functions
   - Remove redundant error checking
   - Simplify conditional logic (ternary -> if/else, De Morgan's laws)
   - Improve naming (longer, clearer names are better)

3. **Example (Python):**
   ```python
   # GREEN (minimal, naming could be better):
   def hash_password(password):
       return hashlib.sha256(password.encode()).hexdigest()
   
   # REFACTOR (clearer):
   def hash_password(plain_text_password):
       # SHA256 chosen for speed over bcrypt for this example
       password_bytes = plain_text_password.encode('utf-8')
       hashed_password = hashlib.sha256(password_bytes).hexdigest()
       return hashed_password
   ```


4. **Run ALL tests after every small change:**
   ```bash
   npm test
   ```
   - If a test fails, undo the change and try differently
   - Tests are your safety net

5. **Decision point at end of REFACTOR:**
   - Are more tests needed for this chunk? -> Go back to RED
   - Is this chunk feature-complete? -> Move to Chunk Self-Review (2D)

---

## Definition of Done (Move to 2D or back to RED when)

- [ ] Code is readable and clean
- [ ] Variable/function names clearly express intent
- [ ] No code duplication (DRY principle)
- [ ] No obvious code smells (see Code Review Standards skill)
- [ ] No magic numbers or strings without explanation
- [ ] Conditional logic is as simple as possible
- [ ] ALL tests still PASS after refactoring
- [ ] You're confident another developer could understand this
- [ ] Either: (a) More tests needed for this chunk -> back to RED, OR (b) Chunk is feature-complete -> proceed to 2D

---

## Time Investment

10-20 minutes per refactor cycle (can be multiple cycles)

---

## Related Skills to Invoke

- **code-review-standards** (checklist for what constitutes "clean code")
- **design-patterns** (if logic could be simplified using a pattern)

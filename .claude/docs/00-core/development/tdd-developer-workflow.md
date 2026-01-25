# TDD Workflow Guide: Developer Experience

**For:** Developers using the `code-quality` agent + `test-driven-development` skill  
**Time per chunk:** 40-90 minutes  
**Success:** Atomic commits, tested code, clean history

---

## Quick Start: Your First TDD Chunk

### Step 0: Setup (Do Once)
```bash
# Ensure testing framework is installed
npm install --save-dev jest           # or vitest, mocha, etc.

# Verify test runner works
npm test

# You should see: "PASS  <some output>"
```

### Step 1: Feature Planning
You're building: **User Login Feature**

**Break into chunks:**
```
Chunk 1: Validate email format (isolated, no DB)
Chunk 2: Hash password function (isolated, no DB)
Chunk 3: Create User model (DB interaction starts)
Chunk 4: Login endpoint validates email
Chunk 5: Login endpoint checks password
Chunk 6: Login endpoint returns JWT token
```

**You'll start with Chunk 1** because:
- ✅ Can be tested in isolation
- ✅ No dependencies on other chunks
- ✅ 40-60 minutes of work
- ✅ Testable behavior

---

## The Loop: RED → GREEN → REFACTOR → REVIEW → COMMIT

### 🔴 PHASE 1: RED — Write a Failing Test (5-15 min)

**Goal:** Define ONE specific behavior as a failing test.

#### What You Do:

1. **Open test file or create new one:**
   ```bash
   touch tests/auth.test.js
   ```

2. **Write ONE test (focus on one behavior):**
   ```javascript
   // tests/auth.test.js
   describe('Email Validation', () => {
     test('rejects invalid email format', () => {
       const result = validateEmail('invalid-email');
       expect(result).toBe(false);
     });
   });
   ```

3. **Run the test (it should FAIL):**
   ```bash
   npm test
   
   # Output:
   # FAIL  tests/auth.test.js
   # ReferenceError: validateEmail is not defined
   ```

   ✅ **Success:** Test failed because function doesn't exist yet.

4. **If test fails for wrong reason?** That's actually good—it means something is wrong with your test:
   ```javascript
   // ❌ WRONG: Test passes when it should fail
   test('email is a string', () => {
     expect('any string here').toBeTruthy();  // This always passes!
   });
   
   // ✅ CORRECT: Test fails because behavior doesn't exist
   test('rejects invalid email', () => {
     const result = validateEmail('not-an-email');
     expect(result).toBe(false);  // Will fail until you implement validateEmail
   });
   ```

#### RED Phase Checklist:
- [ ] Test file exists and is readable
- [ ] Test name clearly describes behavior (not just "test validation")
- [ ] Test FAILS when you run `npm test`
- [ ] Failure message makes sense (not a syntax error)
- [ ] You understand what code will make it pass

#### When You're Done With RED:
Tell the `code-quality` agent: **"Test written and failing. Ready to code the implementation."**

---

### 🟢 PHASE 2: GREEN — Implement Minimal Code (10-30 min)

**Goal:** Write the simplest code that makes your test pass.

#### What You Do:

1. **Create implementation file (if doesn't exist):**
   ```bash
   touch src/auth.js
   ```

2. **Write the simplest code that makes the test pass:**
   ```javascript
   // src/auth.js
   
   export function validateEmail(email) {
     // Check if email has @ symbol (very basic validation)
     return email.includes('@');
   }
   ```

   Why this simple version? **Because the test only checks for @ symbol.** Don't add extra validation yet.

3. **Run all tests:**
   ```bash
   npm test
   
   # Output:
   # PASS  tests/auth.test.js
   # ✓ rejects invalid email format (3ms)
   # 
   # Tests:       1 passed, 1 total
   ```

   ✅ **Success:** Your test passes now.

4. **Make sure you didn't break other tests:**
   ```bash
   npm test  # Run ALL tests, not just this one
   ```

   If you have other tests, they should still pass.

#### GREEN Phase Checklist:
- [ ] Test passes (shows ✓ when you run `npm test`)
- [ ] ALL other tests still pass (no regressions)
- [ ] Code implements the specific behavior from the test
- [ ] No extra features added (resist temptation!)
- [ ] No console.logs or debugging code

#### When You're Done With GREEN:
Tell the `code-quality` agent: **"Test passes. Code is minimal. Ready to refactor."**

---

### 🔵 PHASE 3: REFACTOR — Clean Up the Code (10-20 min)

**Goal:** Make your code clean and maintainable while keeping tests passing.

#### What You Do:

1. **Review the code you just wrote:**
   ```javascript
   // Before:
   export function validateEmail(email) {
     return email.includes('@');
   }
   
   // Better (clearer intent + error handling):
   export function validateEmail(email) {
     if (!email || typeof email !== 'string') {
       return false;
     }
     
     // Simple check for email format: must have @ and something on both sides
     return email.includes('@') && email.split('@').length === 2;
   }
   ```

2. **Run tests after every change:**
   ```bash
   npm test  # CRITICAL: Verify tests still pass
   ```

3. **Continue improving until it's clean:**
   ```javascript
   // Even better (add comment explaining validation level):
   export function validateEmail(email) {
     // Basic email validation (checks for @ symbol)
     // For production, use email service or RFC-compliant regex
     
     if (!email || typeof email !== 'string') {
       return false;
     }
     
     const parts = email.split('@');
     return parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
   }
   ```

4. **Check for code smells:**
   - ❌ Magic strings/numbers? → Extract to named constants
   - ❌ Unclear variable names? → Rename them
   - ❌ Duplicated code? → Extract to helper function
   - ❌ Long methods? → Break into smaller functions

5. **Is code clean now?** Ask yourself:
   - Could another developer understand this in 10 seconds?
   - Are there any obvious improvements?
   - Is the test still testing what I intended?

#### REFACTOR Phase Checklist:
- [ ] Code is readable and clean
- [ ] Variable/function names are clear (not `a`, `b`, `validate_email_function`)
- [ ] No code duplication
- [ ] ALL tests pass after refactoring
- [ ] Comments explain "why", not "what"
- [ ] No TODO or FIXME comments left behind

#### When You're Done With REFACTOR:

Ask yourself: **"Does this chunk need more tests, or is it feature-complete?"**

- **Need more tests?** → Go back to RED Phase
  - Example: "I need to test valid email too"
  - Example: "What about emails with multiple @ symbols?"

- **Chunk is feature-complete?** → Move to REVIEW Phase

---

### 🟡 PHASE 4: REVIEW — Self-Review Before Commit (5-10 min)

**Goal:** Final quality check before saving to git.

#### What You Do:

1. **View the diff (what changed):**
   ```bash
   git diff src/auth.js
   git diff tests/auth.test.js
   ```

2. **Verify files are clean:**
   ```bash
   # Look for debug code
   grep -n "console.log" src/auth.js          # Should return nothing
   grep -n ".skip\|\.only" tests/auth.test.js # Should return nothing
   grep -n "TODO\|FIXME" src/auth.js          # Should return nothing
   ```

3. **Run tests with coverage:**
   ```bash
   npm test -- --coverage
   
   # Output:
   # File       | % Stmts | % Branch | % Funcs | % Lines |
   # -----------+---------+----------+---------+---------|
   # auth.js    |   100   |   100    |   100   |   100   |
   ```

   - Is coverage >80%? ✅ (Ideally 100% for this chunk)
   - Every line tested?

4. **Final code walkthrough (mentally):**
   - Run through the code with different inputs:
     - Valid email: "user@example.com" → Should return `true`
     - Invalid email: "user-without-at.com" → Should return `false`
     - Edge case: "" (empty) → Should return `false`
     - Edge case: "@" (just @) → Should return `false`

5. **Are all edge cases tested?**
   ```javascript
   // In tests/auth.test.js, you should have:
   test('rejects invalid email', () => {...});
   test('accepts valid email', () => {...});
   test('rejects empty email', () => {...});
   test('rejects email with multiple @', () => {...});
   ```

   If not, go back to RED and write those tests.

#### REVIEW Phase Checklist:
- [ ] `npm test` passes (run one more time)
- [ ] Coverage >80% for this chunk
- [ ] No `console.log()` in code
- [ ] No `.skip` or `.only` in tests
- [ ] No commented-out code
- [ ] No `TODO` or `FIXME` left in comments
- [ ] Edge cases are tested
- [ ] Chunk does ONE thing (not multiple features)

#### When You're Done With REVIEW:

Tell the `code-quality` agent: **"Self-review complete. All checks pass. Ready to commit."**

---

### ✅ PHASE 5: COMMIT — Save Your Work (3-5 min)

**Goal:** Create an atomic commit with clear message.

#### What You Do:

1. **Stage only files from THIS chunk:**
   ```bash
   git status
   
   # Shows what's modified
   # Modified: src/auth.js
   # Modified: tests/auth.test.js
   
   # Both belong to Chunk 1, so stage both
   git add src/auth.js tests/auth.test.js
   
   git status  # Verify only the right files are staged
   ```

2. **Write a clear commit message:**
   ```bash
   git commit -m "feat: add email validation

   - Implements basic email format validation (checks for @)
   - Validates email is non-empty string
   - Tests: valid email, invalid email, empty input, multiple @
   - Coverage: 100%"
   ```

   **Message format:**
   ```
   <type>: <short description>
   
   - Bullet point 1
   - Bullet point 2
   - Bullet point 3
   
   References: #123 (if you have a ticket)
   ```

   **Types:**
   - `feat:` — New feature chunk
   - `fix:` — Bug fix
   - `refactor:` — Code improvements
   - `test:` — Test-only changes
   - `chore:` — Setup, dependencies, config

3. **Push to remote (backup):**
   ```bash
   git push origin feature/user-login
   ```

4. **Verify commit went through:**
   ```bash
   git log --oneline
   
   # Shows:
   # abc1234 feat: add email validation
   # def5678 main branch commit
   ```

#### COMMIT Phase Checklist:
- [ ] Only files from THIS chunk are staged
- [ ] Commit message is clear and descriptive
- [ ] Commit message follows conventional format
- [ ] `npm test` passes AFTER commit
- [ ] Changes pushed to remote branch
- [ ] Commit is atomic (one logical change)

#### When You're Done With COMMIT:

The `code-quality` agent will say: **"Chunk 1 complete! You have 5 chunks remaining. Ready for Chunk 2?"**

---

## Repeat for Each Chunk

```
Chunk 1: Email validation ✅ COMPLETE (RED → GREEN → REFACTOR → REVIEW → COMMIT)
Chunk 2: Password hashing (Start here: RED phase)
Chunk 3: User model
Chunk 4: Login endpoint validates email
Chunk 5: Login endpoint checks password
Chunk 6: Login endpoint returns JWT token
```

**For Chunk 2, start again at RED:**

1. **Write failing test** for password hashing
   ```javascript
   test('hashes password differently than input', () => {
     const result = hashPassword('mypassword');
     expect(result).not.toBe('mypassword');
   });
   ```

2. **Implement minimal code** to pass the test
3. **Refactor** for quality
4. **Review** before commit
5. **Commit** atomically

---

## Common Mistakes & How to Avoid Them

### ❌ Mistake 1: Skipping the REFACTOR phase
**Why it's bad:** Code debt accumulates, becomes hard to maintain  
**Fix:** REFACTOR is mandatory, not optional. Quality is non-negotiable.

### ❌ Mistake 2: Writing multiple tests in RED phase
**Why it's bad:** Hard to know which test caused GREEN to pass, harder to debug  
**Fix:** Write ONE test, make it pass, THEN write the next test.

### ❌ Mistake 3: Adding features in GREEN that tests don't require
**Why it's bad:** Features without tests break later with no warning  
**Fix:** Only implement what the test requires. Resist the urge to add extras.

### ❌ Mistake 4: Large commits mixing multiple chunks
**Why it's bad:** Hard to understand what changed, hard to revert if needed  
**Fix:** One commit per chunk. Keep chunks small (40-90 min each).

### ❌ Mistake 5: Committing without self-review
**Why it's bad:** Debug code, console.logs, or incomplete tests reach main  
**Fix:** Always do REVIEW phase before COMMIT.

### ❌ Mistake 6: Writing unclear commit messages
**Why it's bad:** Six months later, you can't remember why you made this change  
**Fix:** Use conventional commit format. Explain WHAT changed and WHY.

---

## Example: Full Chunk Walkthrough

### Starting: Chunk 1 — Email Validation

**User:** "I'm starting user login feature. First chunk is email validation."

**Agent:** "Great! Let's do RED phase first.

Write ONE test for email validation. What behavior should you test?"

**User:**
```javascript
// tests/auth.test.js
test('validateEmail returns false for invalid emails', () => {
  expect(validateEmail('not-an-email')).toBe(false);
  expect(validateEmail('another@bad@email')).toBe(false);
  expect(validateEmail('')).toBe(false);
});
```

**Agent:** "Hmm, that test covers THREE different behaviors. Let's split it:

Test 1 (missing @): not-an-email
Test 2 (multiple @): another@bad@email
Test 3 (empty): ''

Write these as three separate tests so we can debug easily."

**User:**
```javascript
test('returns false for email without @', () => {
  expect(validateEmail('not-an-email')).toBe(false);
});

test('returns false for email with multiple @', () => {
  expect(validateEmail('another@bad@email')).toBe(false);
});

test('returns false for empty email', () => {
  expect(validateEmail('')).toBe(false);
});
```

**Agent:** "Perfect! Now run: npm test

What do you see?"

**User:** "Tests fail: ReferenceError: validateEmail is not defined"

**Agent:** "Good—that's the right failure. RED phase complete. Move to GREEN.

Implement the simplest validateEmail function to make these tests pass."

**User:**
```javascript
// src/auth.js
export function validateEmail(email) {
  if (!email) return false;
  return email.includes('@') && email.split('@').length === 2;
}
```

**Agent:** "Run: npm test"

**User:** "All three tests pass!"

**Agent:** "Excellent! Now REFACTOR.

Review your code:
- Variable names clear?
- Comments needed?
- Any duplication?
- Edge cases handled?"

**User:** "I should add comments and handle edge case where @ has nothing before/after."

```javascript
export function validateEmail(email) {
  // Basic email validation: must be non-empty string with exactly one @
  // For production, use RFC-compliant regex or external service
  
  if (!email || typeof email !== 'string') {
    return false;
  }
  
  const parts = email.split('@');
  return parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
}
```

**Agent:** "Run tests again"

**User:** "Still passing!"

**Agent:** "Do you need more tests for this chunk, or is it complete?"

**User:** "I think I need a test for valid emails too."

**Agent:** "Good catch! Back to RED phase:

Write a test for valid email."

**User:**
```javascript
test('returns true for valid email', () => {
  expect(validateEmail('user@example.com')).toBe(true);
});
```

**Agent:** "Run: npm test"

**User:** "New test fails!"

**Agent:** "Good—that's RED. Does your implementation pass it?"

**User:** "Let me run again... yes, it passes!"

**Agent:** "GREEN complete. REFACTOR anything?"

**User:** "No, code looks good."

**Agent:** "REVIEW time:

Run: npm test -- --coverage

What's the coverage?"

**User:** "100% coverage!"

**Agent:** "Perfect! Any console.logs or debug code?"

**User:** "No."

**Agent:** "Ready to COMMIT. 

Run:
git add src/auth.js tests/auth.test.js
git commit -m \"feat: add email validation

- Validates email has @ symbol with content on both sides
- Returns false for invalid formats
- Tests: missing @, multiple @, empty, valid email
- Coverage: 100%\"

git push origin feature/user-login"

**User:** [Commits and pushes]

**Agent:** "Chunk 1 complete! ✅

You have 5 chunks remaining. Ready for Chunk 2 (password hashing)?"

**User:** "Yes!"

**Agent:** "Start RED phase: Write a failing test for password hashing..."
```

---

## Time Tracking

Use this to monitor your progress:

| Chunk | Feature | RED | GREEN | REFACTOR | REVIEW | COMMIT | Total | Status |
|-------|---------|-----|-------|----------|--------|--------|-------|--------|
| 1 | Email validation | 10m | 15m | 12m | 7m | 4m | 48m | ✅ |
| 2 | Password hashing | 8m | 20m | 15m | 6m | 3m | 52m | ✅ |
| 3 | User model | 12m | 28m | 18m | 8m | 4m | 70m | 🔄 |
| 4 | Login endpoint | - | - | - | - | - | - | ⏳ |
| 5 | JWT token | - | - | - | - | - | - | ⏳ |
| 6 | Protected routes | - | - | - | - | - | - | ⏳ |

**Total so far:** 170 minutes (~2.8 hours)  
**Estimated total:** 350-400 minutes (~6-7 hours)

---

## When You're Stuck

### "My test won't run"
```bash
# Verify test framework is installed
npm list jest

# Verify test file is valid JavaScript
node tests/auth.test.js  # Should not crash

# Ask code-quality agent: "Test syntax error. Help me debug."
```

### "My test passes but shouldn't"
```javascript
# ❌ BAD: This always passes
test('email validation', () => {
  expect(true).toBe(true);  // Doesn't test anything!
});

# ✅ GOOD: This fails without implementation
test('rejects invalid email', () => {
  expect(validateEmail('no-at-sign')).toBe(false);  // Fails until validateEmail exists
});
```

### "I don't know what tests to write"
Ask yourself: **"What does this function do? What could go wrong?"**

```
Function: validateEmail(email)

What could go wrong?
- Email is null/undefined
- Email is empty string
- Email has no @ symbol
- Email has multiple @ symbols
- Email has @ but nothing before/after

Write one test per "what could go wrong".
```

### "My code is too complicated to REFACTOR"
Don't worry. Just make small changes, run tests after each:

```javascript
// If this is confusing:
const isValid = email && email.includes('@') && email.split('@').length === 2 && email.split('@')[0].length > 0;

// Break into smaller steps:
const hasAtSymbol = email.includes('@');
const parts = email.split('@');
const hasValidParts = parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
const isValid = email && hasAtSymbol && hasValidParts;

// Even better:
function emailHasValidFormat(email) {
  if (!email) return false;
  const parts = email.split('@');
  return parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
}
```

---

## Success Checklist: You're Doing TDD Right When...

- ✅ Your commits are small (1-3 files each)
- ✅ Your commit messages are clear (you can read history and understand why)
- ✅ Your tests pass 100% (no flaky tests)
- ✅ Your test names explain behavior (not just "test1", "test2")
- ✅ You rarely have "FIXME" comments in code
- ✅ Code review is fast (code is clean, tests prove it works)
- ✅ You feel confident making changes (tests catch regressions)
- ✅ Another developer can understand your code in 5 minutes
- ✅ You finish features on schedule (less debugging time)
- ✅ Production bugs are rare (caught by tests first)


# TDD Skill: Visual Quick Reference

**Use this page for quick lookup during development.**

---

## The RED-GREEN-REFACTOR Cycle (At a Glance)

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Start New Test                                                  │
│        ↓                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🔴 RED: Write Failing Test                             │    │
│  │  ────────────────────────────────                       │    │
│  │  • Write ONE test for next behavior                     │    │
│  │  • Test should FAIL                                     │    │
│  │  • Failure message should be clear                      │    │
│  │  • Time: 5-15 minutes                                   │    │
│  └──────────────────┬──────────────────────────────────────┘    │
│                     ↓                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🟢 GREEN: Make Test Pass                               │    │
│  │  ──────────────────────────────                         │    │
│  │  • Write simplest code possible                         │    │
│  │  • Code should make test PASS                           │    │
│  │  • All previous tests should still pass                 │    │
│  │  • Time: 10-30 minutes                                  │    │
│  └──────────────────┬──────────────────────────────────────┘    │
│                     ↓                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🔵 REFACTOR: Improve Code Quality                      │    │
│  │  ──────────────────────────────                         │    │
│  │  • Remove duplication                                   │    │
│  │  • Improve naming                                       │    │
│  │  • Simplify logic                                       │    │
│  │  • Run tests after each change                          │    │
│  │  • Time: 10-20 minutes                                  │    │
│  └──────────────────┬──────────────────────────────────────┘    │
│                     ↓                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  🟡 REVIEW: Self-Review Before Commit                   │    │
│  │  ──────────────────────────────────                     │    │
│  │  • Check test coverage (>80%)                           │    │
│  │  • Remove debug code                                    │    │
│  │  • Check edge cases                                     │    │
│  │  • Time: 5-10 minutes                                   │    │
│  └──────────────────┬──────────────────────────────────────┘    │
│                     ↓                                             │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  ✅ COMMIT: Save Your Work                              │    │
│  │  ──────────────────────────                             │    │
│  │  • Stage files (git add)                                │    │
│  │  • Write clear message                                  │    │
│  │  • Commit (git commit)                                  │    │
│  │  • Push (git push)                                      │    │
│  │  • Time: 3-5 minutes                                    │    │
│  └──────────────────┬──────────────────────────────────────┘    │
│                     ↓                                             │
│       More tests needed? ──→ [Go back to RED] ⤴️                 │
│            │                                                      │
│            └──→ Feature chunk done? [Next Chunk]                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

⏱️  PER CHUNK: 40-90 minutes total
```

---

## Phase Checklist: Definition of Done

### 🔴 RED PHASE (Write Failing Test)
```
□ Test file created
□ One test written (not multiple)
□ Test name clearly describes behavior
□ Test FAILS when you run it
□ Failure message is informative
□ You understand what code will make it pass
```
**Time:** 5-15 min | **Next:** GREEN phase

---

### 🟢 GREEN PHASE (Make Test Pass)
```
□ Implementation written
□ The failing test now PASSES
□ ALL previous tests still PASS
□ Code implements the specific behavior
□ No extra features added
□ No debug code left in
```
**Time:** 10-30 min | **Next:** REFACTOR phase

---

### 🔵 REFACTOR PHASE (Improve Code Quality)
```
□ Code is readable and clean
□ Variable/function names are clear
□ No code duplication (DRY)
□ No code smells
□ ALL tests still PASS
□ Ready for another developer to understand
```
**Time:** 10-20 min | **Next:** REVIEW phase (or back to RED)

---

### 🟡 REVIEW PHASE (Self-Review Before Commit)
```
□ Test coverage is >80%
□ No console.logs() in code
□ No .skip or .only in tests
□ No TODO/FIXME comments
□ No commented-out code
□ Edge cases are tested
□ Chunk is ONE feature (not multiple)
```
**Time:** 5-10 min | **Next:** COMMIT phase

---

### ✅ COMMIT PHASE (Save Your Work)
```
□ Only THIS chunk's files staged
□ Commit message follows format: feat: description
□ All tests pass AFTER commit
□ Message clearly describes what/why
□ Changes pushed to remote
```
**Time:** 3-5 min | **Next:** New chunk or done

---

## Code Examples: JavaScript Pattern

### RED: Write Test
```javascript
// tests/auth.test.js
test('validateEmail returns false for invalid email', () => {
  expect(validateEmail('not-an-email')).toBe(false);
});
```

### GREEN: Implement Minimal Code
```javascript
// src/auth.js
export function validateEmail(email) {
  return email.includes('@');
}
```

### REFACTOR: Improve Quality
```javascript
// src/auth.js
export function validateEmail(email) {
  if (!email || typeof email !== 'string') {
    return false;
  }
  
  const parts = email.split('@');
  return parts.length === 2 && parts[0].length > 0 && parts[1].length > 0;
}
```

---

## Time Budget

```
         RED        GREEN      REFACTOR   REVIEW     COMMIT
          │            │           │         │          │
    5-15 min    10-30 min    10-20 min   5-10 min   3-5 min
          │            │           │         │          │
          └────────────┴───────────┴─────────┴──────────┘
                    40-90 MINUTES PER CHUNK
```

---

## Quality Gates (Agent Blocks Progress Until...)

| Phase | Gate | What Gets Checked |
|-------|------|------------------|
| 🔴 RED | Test fails | Does test fail? Is it focused? Is message clear? |
| 🟢 GREEN | Tests pass | Do all tests pass? Is implementation minimal? |
| 🔵 REFACTOR | Code clean | Is code readable? Do tests still pass? |
| 🟡 REVIEW | Quality check | Coverage >80%? No debug code? Edge cases tested? |
| ✅ COMMIT | Ready | Correct files staged? Message format OK? |

---

## Common Commands

### Test Running
```bash
npm test                          # Run all tests
npm test -- --coverage           # Coverage report
npm test -- --watch              # Watch mode
npm test auth.test.js            # Single file
npm test -- --verbose            # Detailed output
```

### Git Operations
```bash
git status                        # See staged files
git diff src/file.js             # See changes
git add src/ tests/              # Stage files
git commit -m "feat: description" # Commit
git push origin feature-name      # Push
git log --oneline                 # See commits
```

---

## Code Smells: Watch Out For

```javascript
// ❌ SMELL: Magic number
const result = value * 2.5;

// ✅ FIX: Named constant
const TAX_MULTIPLIER = 2.5;
const result = value * TAX_MULTIPLIER;

// ❌ SMELL: Unclear name
function calc(x, y) {
  return x * y;
}

// ✅ FIX: Clear name
function calculateTotalPrice(quantity, unitPrice) {
  return quantity * unitPrice;
}

// ❌ SMELL: Duplicated code
if (user.email) {
  sendEmail(user.email);
}
if (admin.email) {
  sendEmail(admin.email);
}

// ✅ FIX: Extract helper
function sendEmailIfExists(person) {
  if (person.email) {
    sendEmail(person.email);
  }
}
sendEmailIfExists(user);
sendEmailIfExists(admin);
```

---

## When Tests Fail

### ❌ Test Fails: "function is not defined"
**During RED:** ✅ Perfect! That's what should happen.  
**During GREEN/REFACTOR:** Debug—did you implement the function?

### ❌ Test Fails: "Expected true but got false"
**During RED:** ✅ Good! Implementation doesn't exist yet.  
**During GREEN:** Implement until it passes.  
**During REFACTOR:** Did you change something? Undo it.

### ❌ Test Fails: "TypeError: cannot read property"
**Check:** Is the object/property correct in test AND code?  
**Fix:** Verify test setup and implementation both use same names.

### ❌ Test Passes When It Should Fail
**Problem:** Test isn't actually testing anything.  
**Fix:** Rewrite test so it fails without implementation.

---

## Commit Message Format

```
<type>: <short description>

<optional detailed explanation>
<optional reference to issue/ticket>

Types:
- feat:     New feature
- fix:      Bug fix
- refactor: Code improvement (not changing behavior)
- test:     Test-only changes
- chore:    Setup, dependencies, config

EXAMPLE:

feat: add email validation

- Validates email has @ with content on both sides
- Returns false for invalid formats
- Tests: missing @, multiple @, empty, valid
- Coverage: 100%

Closes #123
```

---

## Workflow Status: Track Your Progress

```markdown
# Feature: User Authentication

## Chunk 1: Email Validation
Status: ✅ COMPLETE
Commits: abc123, def456
Tests: 3 passing
Coverage: 100%
Time: 50 minutes

## Chunk 2: Password Hashing
Status: 🔄 IN PROGRESS (GREEN phase)
RED: ✅ Test written and failing
GREEN: 🟡 Implementing...
Refactor: ⏳ Pending
Review: ⏳ Pending
Commit: ⏳ Pending
Time so far: 25 minutes

## Chunk 3: User Model
Status: ⏳ NOT STARTED
Estimated: 70 minutes

## Chunk 4: Login Endpoint
Status: ⏳ NOT STARTED
Estimated: 90 minutes

## Chunk 5: JWT Token
Status: ⏳ NOT STARTED
Estimated: 80 minutes

## Chunk 6: Protected Routes
Status: ⏳ NOT STARTED
Estimated: 70 minutes

---

TOTAL COMPLETE: 50 min (14%)
IN PROGRESS: 25 min (7%)
REMAINING: 410 min (79%)
TOTAL ESTIMATE: 480 min (8 hours)
```

---

## Success Signals: You're Doing TDD Right When...

✅ Your commits are small (1-3 files each)  
✅ Your commit history tells a story (clear messages)  
✅ Tests pass 100% of the time  
✅ Another developer can understand your code in 5 min  
✅ You rarely have bugs reach production  
✅ You feel confident refactoring  
✅ Code reviews are fast (code is clean)  
✅ You finish features on time (less debugging)  

---

## Red Flags: Watch Out For...

❌ Committing without REVIEW phase  
❌ Skipping REFACTOR phase ("it works!")  
❌ Writing multiple tests at once  
❌ Chunks taking >90 minutes  
❌ Tests passing but you don't know why  
❌ Debug code in production commits  
❌ Large commits mixing multiple chunks  
❌ Unclear commit messages  

---

## Ask Yourself at Each Phase

### 🔴 RED
*"What specific behavior should this function have?"*

### 🟢 GREEN
*"What's the simplest code that makes this test pass?"*

### 🔵 REFACTOR
*"Would another developer understand this code easily?"*

### 🟡 REVIEW
*"Is this chunk feature-complete and well-tested?"*

### ✅ COMMIT
*"Does this commit message explain what changed and why?"*

---

## Emergency Eject: You're Stuck?

**Test won't compile?**
```bash
npm test             # Check error message
node tests/file.js   # Run test file directly
```

**Test fails mysteriously?**
```javascript
console.log('DEBUG:', result);  // Temporary logging
```

**Implementation too complex?**
- Split into smaller functions
- Extract logic to helpers
- Simplify one step at a time (run tests after each change)

**Not sure what test to write?**
- Ask: "What could go wrong?"
- Write test for that case
- Implement code to pass it

---

## Resources & Templates

| File | Purpose |
|------|---------|
| tdd-skill-design.md | Complete skill documentation |
| code-quality-agent.md | How agent coaches you |
| tdd-developer-workflow.md | Practical daily guide |
| tdd-architecture-design.md | System design |
| This file | Quick reference |

---

**Bookmark this page. You'll reference it during development.** 📖


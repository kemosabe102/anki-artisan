# TDD Anti-Patterns

Common mistakes and how to avoid them.

---

## Anti-Pattern 1: Writing All Tests First, Then All Code

**Problem:** Leads to batch-style coding, harder to debug

**Solution:** Follow RED -> GREEN -> REFACTOR strictly. One test at a time.

---

## Anti-Pattern 2: Skipping REFACTOR Because "It Works"

**Problem:** Code debt accumulates, becomes unmaintainable

**Solution:** REFACTOR is not optional. Quality is non-negotiable.

---

## Anti-Pattern 3: Writing Big Tests That Cover Multiple Behaviors

**Problem:** Hard to debug when tests fail, unclear what behavior breaks

**Solution:** One test = one behavior. Split complex tests into multiple tests.

---

## Anti-Pattern 4: Adding Features in GREEN That Aren't Tested

**Problem:** Feature works now but breaks later; no test to catch regression

**Solution:** If it's not tested, it doesn't exist. Only implement tested behavior.

---

## Anti-Pattern 5: Large Chunks (3+ hours of work)

**Problem:** Hard to commit atomically, hard to debug, context overload

**Solution:** If chunk takes >90 min, break it into smaller chunks first.

---

## Anti-Pattern 6: Committing Before Self-Review

**Problem:** Debug code, commented-out code, or incomplete tests reach main

**Solution:** Always do 2D (Chunk Self-Review) before 2E (COMMIT).

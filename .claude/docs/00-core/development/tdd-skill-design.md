# Claude Code Skill: Test-Driven Development (TDD)

**Skill Name:** `test-driven-development`  
**Domain:** Development  
**Owner Agent:** `code-quality` (Development Domain)  
**Version:** 1.0  
**Status:** Design Phase

---

## Skill Metadata (Progressive Disclosure Header)

```yaml
name: test-driven-development
aliases: [tdd, red-green-refactor]
domain: development
trigger_keywords:
  - "help me with TDD"
  - "test-driven development workflow"
  - "RED phase"
  - "GREEN phase"
  - "REFACTOR phase"
  - "write failing test"
  - "make test pass"
  - "improve code quality"
  - "test cycle"
contexts:
  - feature development
  - bug fixes
  - refactoring
  - code reviews
prerequisites:
  - "understanding of unit testing framework for your language"
  - "ability to write test assertions"
  - "access to test runner"
time_investment: "per-chunk: 40-90 minutes (RED 5-15 + GREEN 10-30 + REFACTOR 10-20 + REVIEW 5-10 + COMMIT 3-5)"
outputs:
  - atomic commits following conventional commit format
  - 100% test coverage for feature chunk
  - clean, maintainable code
  - clear feature branch history
skills_this_invokes:
  - code-review-standards (during REFACTOR phase)
  - debugging-methodology (if tests fail for wrong reasons)
  - commit-message-standards (during COMMIT phase)
```

---

## Overview: What This Skill Teaches

This skill teaches the **RED-GREEN-REFACTOR cycle** as a systematic workflow for building features incrementally, chunk-by-chunk. It answers:

- **WHO:** Developers building features with test-first discipline
- **WHEN:** Every feature development cycle, every bug fix, every refactoring task
- **WHY:** Ensures code quality, reduces bugs, creates living documentation through tests
- **HOW:** Step-by-step workflow with Definition of Done checklists at each phase

### Key Philosophy
- **Small chunks** (one feature per cycle, 40-90 min per chunk)
- **Test-first** (write failing test before implementation)
- **Atomic commits** (one logical change per commit)
- **Quality gates** (checklists prevent low-quality code)
- **Continuous verification** (all tests pass after every change)

---

## Phase 1: Feature Planning (Pre-Workflow)

**Goal:** Break large feature into testable chunks before starting the RED-GREEN-REFACTOR cycle.

### 1A: Feature Definition
- [ ] Feature has a clear, specific scope (not vague)
- [ ] Feature can be tested independently
- [ ] Feature doesn't depend on incomplete upstream work
- [ ] You've written a 1-2 sentence acceptance criteria
- [ ] Example acceptance criteria: "User can filter todos by status, and unfiltered count matches displayed count"

### 1B: Break into Chunks
- [ ] Identify the smallest testable piece (MVP chunk)
- [ ] Each chunk should be 40-90 minutes of work
- [ ] Chunks should be implementable in isolation or with minimal setup
- [ ] Order chunks by dependency (build from bottom-up)
- [ ] Document chunks in `WORKFLOW_STATUS.md` or feature branch description

**Example chunk breakdown for "User authentication":**
```
Chunk 1: Password hashing function (no DB needed)
Chunk 2: User model with password validation
Chunk 3: Login endpoint accepts credentials
Chunk 4: Login endpoint validates against DB
Chunk 5: Login endpoint returns JWT token
Chunk 6: Protected routes check JWT token
```

### 1C: Setup
- [ ] Testing framework installed and working
- [ ] Test runner configured for your language
- [ ] Sample test can run successfully
- [ ] Database/services mocked or available for testing
- [ ] Branch created: `feature/your-feature-name`

---

## Phase 2: TDD Implementation Loop (Per Chunk)

**Repeat this entire cycle for EACH chunk** until feature is complete.

---

### 2A: RED Phase — Write Failing Test

**Goal:** Define expected behavior through a failing test.

#### ✍️ Activities

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

#### ✅ Definition of Done (Move to GREEN when)

- [ ] Test file created or updated with new test
- [ ] Test name clearly describes expected behavior
- [ ] Test covers ONE specific behavior
- [ ] Test FAILS when you run it (shows test is working)
- [ ] Failure message is informative (e.g., "Expected 'password123' to not equal 'password123'")
- [ ] You understand exactly what code will make this test pass
- [ ] No test is skipped (no `@Skip`, `xit`, `.skip`, etc.)

#### ⏱️ Time Investment
5-15 minutes per test (mostly thinking, not typing)

#### 🔗 Related Skills to Invoke
- **debugging-methodology** (if test fails for syntax reasons instead of logic)
- **code-review-standards** (if team has specific test naming conventions)

---

### 2B: GREEN Phase — Make Test Pass

**Goal:** Write minimal code to make the failing test pass.

#### ✍️ Activities

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

#### ✅ Definition of Done (Move to REFACTOR when)

- [ ] The test you wrote in RED now PASSES
- [ ] ALL previous tests still PASS (no regressions)
- [ ] Code implements the specific behavior, nothing more
- [ ] No unused variables or dead code
- [ ] No hardcoded test data
- [ ] Function/method signature is reasonable (not accepting test-specific parameters)
- [ ] You resisted the urge to add "extra" features

#### ⏱️ Time Investment
10-30 minutes per test (coding + debugging if needed)

#### 🔗 Related Skills to Invoke
- **debugging-methodology** (if test fails unexpectedly)

---

### 2C: REFACTOR Phase — Improve Code Quality

**Goal:** Clean up code while maintaining all passing tests.

#### ✍️ Activities

1. **Review the code you just wrote:**
   - Is there duplicated logic with other functions?
   - Are variable names clear?
   - Are there obvious code smells?

2. **Common refactoring patterns:**
   - Extract magic strings/numbers to named constants
   - Extract complex logic to helper functions
   - Remove redundant error checking
   - Simplify conditional logic (ternary → if/else, De Morgan's laws)
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
   - Are more tests needed for this chunk? → Go back to RED
   - Is this chunk feature-complete? → Move to Chunk Self-Review (2D)

#### ✅ Definition of Done (Move to 2D or back to RED when)

- [ ] Code is readable and clean
- [ ] Variable/function names clearly express intent
- [ ] No code duplication (DRY principle)
- [ ] No obvious code smells (see Code Review Standards skill)
- [ ] No magic numbers or strings without explanation
- [ ] Conditional logic is as simple as possible
- [ ] ALL tests still PASS after refactoring
- [ ] You're confident another developer could understand this
- [ ] Either: (a) More tests needed for this chunk → back to RED, OR (b) Chunk is feature-complete → proceed to 2D

#### ⏱️ Time Investment
10-20 minutes per refactor cycle (can be multiple cycles)

#### 🔗 Related Skills to Invoke
- **code-review-standards** (checklist for what constitutes "clean code")
- **design-patterns** (if logic could be simplified using a pattern)

---

### 2D: Chunk Self-Review — Quality Check Before Commit

**Goal:** Review this chunk before committing to ensure it's production-ready.

#### ✍️ Activities

1. **Review the diff for this chunk only:**
   ```bash
   git diff feature/your-feature-name...main -- <files in this chunk>
   ```

2. **Mental walkthrough:**
   - Step through the code with different inputs
   - What happens with valid input? Invalid input? Boundary values?
   - Are error messages helpful?

3. **Edge case check:**
   - Empty/null inputs?
   - Very large inputs?
   - Negative numbers (if applicable)?
   - Special characters (if applicable)?

4. **Cleanup check:**
   - Any `console.log()` left in code?
   - Any commented-out code?
   - Any `TODO` or `FIXME` comments?
   - Any test debug code (`.only`, `.skip`)?

5. **Test coverage check:**
   - Run tests with coverage report:
     ```bash
     npm test -- --coverage  # JavaScript
     pytest --cov            # Python
     ```
   - Are all new lines covered by tests?

#### ✅ Definition of Done (Commit when)

- [ ] Chunk implements ONE coherent piece of functionality
- [ ] ALL tests for this chunk PASS
- [ ] Code follows team conventions (naming, style, structure)
- [ ] No debug code, console.logs, or commented-out code remains
- [ ] Edge cases for this chunk are tested and handled
- [ ] Variable/function names are consistent and descriptive
- [ ] Test coverage is >80% for this chunk
- [ ] No `.only` or `.skip` in test files
- [ ] You can write a clear commit message explaining this chunk

#### ⏱️ Time Investment
5-10 minutes per chunk

#### 🔗 Related Skills to Invoke
- **code-review-standards** (final checklist)
- **test-naming-conventions** (if team has specific patterns)

---

### 2E: COMMIT — Save Your Progress

**Goal:** Create atomic, meaningful commit for this chunk.

#### ✍️ Activities

1. **Stage only files for this chunk:**
   ```bash
   git add <files-for-this-chunk>
   git status  # Verify only the right files are staged
   ```

2. **Write clear commit message:**
   ```
   Format: <type>: <short description>
   
   Types:
   - feat:     New feature chunk
   - fix:      Bug fix for existing feature
   - refactor: Restructuring without changing behavior
   - test:     Test-only changes
   - chore:    Dependencies, configuration, setup
   
   Example:
   feat: add password hashing to user authentication
   
   Implements SHA256 hashing with UTF-8 encoding.
   Validates against empty passwords.
   Adds 3 tests covering valid input, empty input, and hash consistency.
   
   Closes #123
   ```

3. **Commit and push:**
   ```bash
   git commit -m "feat: add password hashing to user authentication"
   git push origin feature/your-feature-name
   ```

#### ✅ Definition of Done (Return to Phase 2A for next chunk when)

- [ ] Commit made with clear, descriptive message
- [ ] Commit is atomic (one logical change only)
- [ ] ALL tests pass after commit
   ```bash
   npm test  # Final verification
   ```
- [ ] Changes pushed to remote (backup + CI/CD runs)
- [ ] Commit message follows conventional commit format
- [ ] If more chunks remain → Return to Phase 2A (RED) for next chunk
- [ ] If all chunks complete → Proceed to Phase 3 (Final Self-Review)

#### ⏱️ Time Investment
3-5 minutes per commit

#### 🔗 Related Skills to Invoke
- **commit-message-standards** (conventional commits, team conventions)

---

## Phase 3: Final Self-Review (End of Feature)

**Goal:** Review entire feature before merging to main.

### 3A: Feature-Level Testing
- [ ] All tests pass
- [ ] Manual testing of entire feature works end-to-end
- [ ] Edge cases tested
- [ ] Error messages are helpful
- [ ] Performance is acceptable

### 3B: Code Quality Review
- [ ] Code follows team style guide
- [ ] No code duplication across the feature
- [ ] All functions/classes are well-named
- [ ] Complex logic has comments explaining "why"
- [ ] No dead code

### 3C: Documentation
- [ ] Code comments explain complex logic
- [ ] README updated if needed
- [ ] API documentation updated (if applicable)

### 3D: Merge Checklist
- [ ] Feature branch is up-to-date with main
- [ ] All tests pass on main
- [ ] Create pull request with feature description
- [ ] Request code review from team member
- [ ] Address review feedback

---

## Common Anti-Patterns & How to Avoid Them

### ❌ Anti-Pattern 1: Writing All Tests First, Then All Code
- **Problem:** Leads to batch-style coding, harder to debug
- **Solution:** Follow RED → GREEN → REFACTOR strictly. One test at a time.

### ❌ Anti-Pattern 2: Skipping REFACTOR Because "It Works"
- **Problem:** Code debt accumulates, becomes unmaintainable
- **Solution:** REFACTOR is not optional. Quality is non-negotiable.

### ❌ Anti-Pattern 3: Writing Big Tests That Cover Multiple Behaviors
- **Problem:** Hard to debug when tests fail, unclear what behavior breaks
- **Solution:** One test = one behavior. Split complex tests into multiple tests.

### ❌ Anti-Pattern 4: Adding Features in GREEN That Aren't Tested
- **Problem:** Feature works now but breaks later; no test to catch regression
- **Solution:** If it's not tested, it doesn't exist. Only implement tested behavior.

### ❌ Anti-Pattern 5: Large Chunks (3+ hours of work)
- **Problem:** Hard to commit atomically, hard to debug, context overload
- **Solution:** If chunk takes >90 min, break it into smaller chunks first.

### ❌ Anti-Pattern 6: Committing Before Self-Review
- **Problem:** Debug code, commented-out code, or incomplete tests reach main
- **Solution:** Always do 2D (Chunk Self-Review) before 2E (COMMIT).

---

## Workflow Status Template

**File:** `.claude/workflows/WORKFLOW_STATUS.md`

Use this to track progress on a feature:

```markdown
# Feature: User Authentication

## Feature Breakdown

### ✅ Chunk 1: Password Hashing (COMPLETE)
- Status: Merged
- Commits: abc1234
- Tests: 3 passing
- Coverage: 100%

### 🟡 Chunk 2: User Model (IN PROGRESS - GREEN phase)
- Status: Tests written, implementing
- Red Phase: COMPLETE
  - Test: test_user_creation_with_valid_email
- Green Phase: IN PROGRESS
  - Implementing User class
- Refactor Phase: PENDING
- Self-Review: PENDING
- Commit: PENDING

### ⚪ Chunk 3: Login Endpoint (NOT STARTED)
### ⚪ Chunk 4: JWT Generation (NOT STARTED)
### ⚪ Chunk 5: Protected Routes (NOT STARTED)

## Time Tracking
- Chunk 1: 65 minutes (5 RED + 20 GREEN + 15 REFACTOR + 8 REVIEW + 4 COMMIT)
- Chunk 2: 35 minutes so far (RED complete)
- Estimated remaining: 200 minutes
```

---

## Quick Reference: RED-GREEN-REFACTOR at a Glance

| Phase | Goal | Typical Duration | Output | Success Criteria |
|-------|------|------------------|--------|------------------|
| **RED** | Write failing test | 5-15 min | Test file with failing test | Test fails for right reason |
| **GREEN** | Make test pass | 10-30 min | Implementation code | All tests pass |
| **REFACTOR** | Improve code quality | 10-20 min | Cleaned-up code | Tests pass, code is clean |
| **REVIEW** | Quality gate check | 5-10 min | Verification checklist | No debug code, coverage >80% |
| **COMMIT** | Save progress | 3-5 min | Atomic commit + PR | Clear message, clean history |

---

## How Code Quality Agent Uses This Skill

**Orchestrator routes to: `code-quality` agent**

**`code-quality` agent invokes this skill when:**
```
User says: "Help me implement this feature using TDD"
OR
User needs guidance on RED-GREEN-REFACTOR cycle
OR
User is writing tests and needs structure
```

**Agent's workflow:**
1. Parse feature request
2. Invoke `test-driven-development` skill (load this document)
3. Help user break feature into chunks (Phase 1)
4. Guide through RED-GREEN-REFACTOR cycle per chunk (Phase 2)
5. Assist with chunk self-review before commits
6. Coordinate with `code-review-standards` skill during REFACTOR
7. Track progress in `WORKFLOW_STATUS.md`

---

## Skill Versions & Iterations

- **v1.0** (Current): Core RED-GREEN-REFACTOR cycle, 5-phase workflow
- **v1.1** (Planned): Language-specific examples (JavaScript, Python, Go, Rust)
- **v1.2** (Planned): Integration with CI/CD (GitHub Actions, GitLab CI)
- **v1.3** (Planned): Mocking/stubbing patterns for external dependencies
- **v2.0** (Future): BDD extension (Gherkin scenarios → TDD tests)

---

## Files This Skill Creates/Uses

- ✍️ `<project>/tests/<feature>.test.js` — Test files
- ✍️ `<project>/src/<feature>.js` — Implementation files
- ✍️ `.claude/workflows/WORKFLOW_STATUS.md` — Progress tracking
- 📖 `.claude/code-review-standards.md` — Referenced during REFACTOR
- 📖 `.claude/commit-message-standards.md` — Referenced during COMMIT


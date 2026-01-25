# TDD Skill Architecture: System Design

**Overview:** How the test-driven-development skill integrates with Claude Code agent system.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Claude Code Orchestrator                      │
│               (Root coordination agent - CLAUDE.md)              │
│                                                                  │
│  Reads user intent: "help me with TDD", "write failing test"   │
│  Routes to: code-quality agent                                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      │ Route: TDD coaching needed
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│              code-quality Agent (Development Domain)             │
│                                                                  │
│  Responsibility: Guide developers through TDD workflow           │
│  - Parse intent                                                 │
│  - Load and invoke test-driven-development skill               │
│  - Guide through Phase 1: Feature Planning                      │
│  - Coach through Phase 2: RED-GREEN-REFACTOR cycle              │
│  - Enforce quality gates at each phase                          │
│  - Coordinate peer review (phase 3)                             │
│  - Track progress in WORKFLOW_STATUS.md                         │
└─────────────────┬──────────────────────────────────────────────┘
                  │
                  │ Invokes (loads from disk)
                  ↓
┌─────────────────────────────────────────────────────────────────┐
│        test-driven-development Skill (Development Domain)        │
│                                                                  │
│  Metadata (Progressive Disclosure):                            │
│  - Trigger keywords: TDD, RED-GREEN-REFACTOR, test workflow    │
│  - Time investment: 40-90 min per chunk                         │
│  - Prerequisites: Testing framework, basic git knowledge        │
│  - Outputs: Atomic commits, tested code, clean history          │
│                                                                 │
│  Content:                                                       │
│  - Phase 1: Feature Planning (break into chunks)              │
│  - Phase 2: TDD Loop (per chunk)                              │
│    ├─ 2A: RED (write failing test)                            │
│    ├─ 2B: GREEN (implement minimal code)                       │
│    ├─ 2C: REFACTOR (improve code quality)                      │
│    ├─ 2D: REVIEW (self-review before commit)                   │
│    └─ 2E: COMMIT (save atomic commit)                          │
│  - Phase 3: Final self-review (end of feature)                │
│  - Anti-patterns & how to avoid them                           │
│  - Quick reference table                                        │
│                                                                 │
│  Skills This Invokes:                                          │
│  - code-review-standards (during REFACTOR phase)              │
│  - debugging-methodology (if tests fail unexpectedly)         │
│  - commit-message-standards (during COMMIT phase)             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Information Flow: Developer → Agent → Skill

### Interaction Sequence

```
1. DEVELOPER writes message
   "I want to build user authentication using TDD"
   
                    ↓
                    
2. ORCHESTRATOR reads message
   Identifies keywords: "build", "using TDD"
   Decision: "This needs code-quality agent"
   
                    ↓
                    
3. code-quality AGENT starts
   - Parses: Feature = user authentication
   - Invokes skill: test-driven-development
   - Loads metadata: Acknowledges 6+ hour project
   
                    ↓
                    
4. SKILL METADATA loaded
   Shows developer:
   - Time estimate: 40-90 min per chunk
   - Phase structure: 1A, 1B, 1C (planning)
   - Then: 2A-2E repeated per chunk
   
                    ↓
                    
5. AGENT GUIDES (Phase 1A: Feature Definition)
   - Ask developer: What's the acceptance criteria?
   - Developer: "User can log in with email/password"
   - Agent: Confirms this is a valid feature scope
   
                    ↓
                    
6. AGENT GUIDES (Phase 1B: Break into Chunks)
   - Help identify chunks:
     Chunk 1: Email validation (no DB, 40 min)
     Chunk 2: Password hashing (no DB, 50 min)
     Chunk 3: User model (with DB, 70 min)
     Chunk 4-6: Endpoints (90 min each)
   - Document in: .claude/workflows/WORKFLOW_STATUS.md
   
                    ↓
                    
7. AGENT GUIDES (Phase 1C: Setup)
   - Verify testing framework installed
   - Verify test runner works
   - Create feature branch
   
                    ↓
                    
8. DEVELOPER STARTS (Chunk 1, Phase 2A: RED)
   - Creates test file
   - Writes failing test for email validation
   - Runs: npm test → FAILS (good!)
   
                    ↓
                    
9. AGENT VERIFIES RED gate
   - Check: Test is focused (one behavior)?
   - Check: Test fails for right reason?
   - Check: Test name is clear?
   - If yes → Proceed to GREEN
   - If no → Request fixes
   
                    ↓
                    
10. DEVELOPER (Phase 2B: GREEN)
    - Implements minimal validateEmail function
    - Runs: npm test → PASSES
    
                    ↓
                    
11. AGENT VERIFIES GREEN gate
    - Check: The new test passes?
    - Check: All previous tests still pass?
    - Check: Implementation is minimal (not over-engineered)?
    - If yes → Proceed to REFACTOR
    
                    ↓
                    
12. DEVELOPER (Phase 2C: REFACTOR)
    - Reviews code: naming, clarity, duplications?
    - Improves: adds comments, better variable names
    - Runs: npm test → Still passes (tests catch regressions!)
    
                    ↓
                    
13. AGENT INVOKES SKILL: code-review-standards
    - Loads code quality checklist
    - Helps identify code smells
    - Provides refactoring suggestions
    
                    ↓
                    
14. DEVELOPER (Phase 2D: REVIEW)
    - Checks: npm test --coverage (100% coverage needed)
    - Scans for: console.logs, .skip/.only, debug code
    - Mental walkthrough: edge cases handled?
    
                    ↓
                    
15. AGENT VERIFIES REVIEW gate
    - Check: Coverage >80%?
    - Check: No debug code?
    - Check: Edge cases tested?
    - If yes → Ready to commit
    
                    ↓
                    
16. DEVELOPER (Phase 2E: COMMIT)
    - Stages files: git add src/auth.js tests/auth.test.js
    - Commits: git commit -m "feat: add email validation"
    - Pushes: git push origin feature/user-auth
    
                    ↓
                    
17. AGENT UPDATES STATUS
    - Marks: Chunk 1 ✅ COMPLETE
    - Updates: .claude/workflows/WORKFLOW_STATUS.md
    - Announces: "5 chunks remaining. Ready for Chunk 2?"
    
                    ↓
                    
18. DEVELOPER & AGENT REPEAT
    - Back to Step 8: Phase 2A (RED) for Chunk 2
    - Loop continues until all chunks complete
    
                    ↓
                    
19. FINAL: Phase 3 (Feature Self-Review)
    - Run all tests for entire feature
    - Code review entire feature
    - Merge to main
```

---

## File Structure Created

```
project-root/
├── .claude/
│   ├── CLAUDE.md                          (Project map, points to this skill)
│   ├── agents/
│   │   └── code-quality.md               (Agent definition)
│   ├── skills/
│   │   └── test-driven-development/
│   │       ├── SKILL.md                  (Main skill file - this doc)
│   │       ├── references/
│   │       │   ├── red-phase-guide.md
│   │       │   ├── green-phase-guide.md
│   │       │   ├── refactor-phase-guide.md
│   │       │   └── anti-patterns.md
│   │       └── scripts/
│   │           ├── verify-tests.sh
│   │           └── coverage-report.sh
│   └── workflows/
│       └── WORKFLOW_STATUS.md            (Progress tracking, updated by agent)
├── src/
│   ├── auth.js                           (Implementation from Chunk 1)
│   ├── user.js                           (Implementation from Chunk 3)
│   └── ...
├── tests/
│   ├── auth.test.js                      (Tests from Chunk 1)
│   ├── user.test.js                      (Tests from Chunk 3)
│   └── ...
└── package.json
```

---

## Agent Quality Gates

The `code-quality` agent enforces gates at each phase:

### 🔴 RED Phase Gate
```javascript
// Agent checks before allowing GREEN:

if (!test_is_focused_on_one_behavior) {
  agent.say("This test covers multiple behaviors. Split it into separate tests.");
  return BLOCKED;
}

if (!test_fails_when_run) {
  agent.say("Test should fail at this point. Is the implementation already there?");
  return BLOCKED;
}

if (test_failure_reason === "syntax error") {
  agent.invoke_skill("debugging-methodology");
  return BLOCKED;
}

// All checks pass
return ALLOWED_TO_PROCEED_TO_GREEN;
```

### 🟢 GREEN Phase Gate
```javascript
if (!all_tests_pass) {
  agent.say("One or more tests are failing. Debug before moving to REFACTOR.");
  return BLOCKED;
}

if (implementation_has_extra_features) {
  agent.say("You added features the test doesn't require. Remove them.");
  return BLOCKED;
}

return ALLOWED_TO_PROCEED_TO_REFACTOR;
```

### 🔵 REFACTOR Phase Gate
```javascript
if (test_still_passes === false) {
  agent.say("Refactoring broke tests. Revert changes and try again.");
  return BLOCKED;
}

if (code_has_smells) {
  agent.invoke_skill("code-review-standards");
  agent.say("Address these code smells before moving to REVIEW.");
  return BLOCKED;
}

return ALLOWED_TO_PROCEED_TO_REVIEW;
```

### 🟡 REVIEW Phase Gate
```javascript
if (coverage_percent < 80) {
  agent.say("Coverage is below 80%. Write more tests to cover edge cases.");
  return BLOCKED;
}

if (has_console_logs || has_skip_markers || has_debug_code) {
  agent.say("Found debug code. Remove all console.logs and .skip/.only markers.");
  return BLOCKED;
}

return ALLOWED_TO_PROCEED_TO_COMMIT;
```

### ✅ COMMIT Phase Gate
```javascript
if (only_chunk_files_staged === false) {
  agent.say("You've staged files from other chunks. Stage only THIS chunk.");
  return BLOCKED;
}

if (conventional_commit_format === false) {
  agent.say("Commit message doesn't follow format. Use: feat|fix|refactor: description");
  return BLOCKED;
}

return COMMIT_ALLOWED;
return UPDATE_WORKFLOW_STATUS;
return READY_FOR_NEXT_CHUNK;
```

---

## Skill Invocation Dependencies

```
test-driven-development (MAIN SKILL)
├─ Invokes: code-review-standards
│  When: REFACTOR phase starts
│  Why: Checklist of what "clean code" means
│  Input: Refactored code
│  Output: Code quality checklist + suggestions
│
├─ Invokes: debugging-methodology
│  When: Test fails for unexpected reason
│  Why: Systematic debugging approach
│  Input: Failed test + error message
│  Output: Step-by-step debugging guide
│
└─ Invokes: commit-message-standards
   When: COMMIT phase starts
   Why: Ensures message follows team conventions
   Input: Draft commit message
   Output: Validated message OR suggestions
```

---

## Time Budget Per Chunk

```
Chunk Time Breakdown:

🔴 RED Phase:        5-15 minutes
   └─ Thinking about behavior: 3-8 min
   └─ Writing test: 2-7 min
   └─ Confirming it fails: 1 min

🟢 GREEN Phase:      10-30 minutes
   └─ Writing implementation: 5-15 min
   └─ Running tests: 1 min
   └─ Debugging if needed: 5-15 min

🔵 REFACTOR Phase:   10-20 minutes
   └─ Identifying improvements: 3-5 min
   └─ Making changes: 3-10 min
   └─ Running tests after each change: 3-5 min

🟡 REVIEW Phase:     5-10 minutes
   └─ Running coverage report: 1 min
   └─ Checking for debug code: 2-4 min
   └─ Walkthrough with different inputs: 2-5 min

✅ COMMIT Phase:     3-5 minutes
   └─ Staging files: 1 min
   └─ Writing message: 1-2 min
   └─ Pushing to remote: 1 min

─────────────────────────────────
TOTAL PER CHUNK:     40-90 minutes
```

---

## Agent Context Management

The `code-quality` agent manages context carefully:

### Context Window Strategy
```
Total tokens available: ~8,000
Token budget per interaction: ~2,000

Distribution:
- Skill metadata (progressive disclosure): 500 tokens
- User message + history: 800 tokens
- Agent reasoning + response: 700 tokens
```

### How Agent Manages Context
1. **Load only metadata first** (not full skill)
2. **Progressive disclosure** (load details on-demand)
3. **Track state in files** (WORKFLOW_STATUS.md)
4. **Referential loading** (point to docs, don't embed)
5. **Break at phase boundaries** (don't load all 5 phases at once)

### Example: Agent Loads Skill in Phases

```javascript
// Phase 1: Load metadata only
const metadata = load_skill_metadata("test-driven-development");

// Phase 2A: Load RED phase guidance
const red_phase = load_skill_section("Phase 2A: RED");

// Developers work on RED
// When done with RED, load next phase

// Phase 2B: Load GREEN phase guidance
const green_phase = load_skill_section("Phase 2B: GREEN");
```

---

## Success Metrics

### Quantitative
- ✅ 100% of code has passing tests before merge
- ✅ Test coverage >80% per chunk
- ✅ Zero low-quality code reaching main
- ✅ Commits are atomic (avg 1-3 files per commit)
- ✅ Feature delivery time reduced (less debugging time)

### Qualitative
- ✅ Developer confidence in quality gates
- ✅ Code is consistent across team
- ✅ Onboarding faster (TDD workflow is clear)
- ✅ Code reviews are faster (tests + self-review catch issues)
- ✅ Fewer production bugs (caught by tests first)
- ✅ Developers enjoy the workflow (clear, structured)

---

## Skill Version Roadmap

**v1.0** (Current)
- Core RED-GREEN-REFACTOR cycle
- 5-phase workflow per chunk
- Definition of Done checklists
- File-based progress tracking

**v1.1** (Next)
- Language-specific examples (JavaScript, Python, Go, Rust)
- Snippets for common test patterns
- Framework-specific guidance (Jest, Pytest, Go test, etc.)

**v1.2** (Future)
- CI/CD integration (GitHub Actions, GitLab CI)
- Automated coverage reports
- Git hook integration

**v1.3** (Future)
- Mocking/stubbing patterns
- Database testing strategies
- Async/await test patterns

**v2.0** (Longterm)
- BDD extension (Gherkin → TDD)
- AI-assisted refactoring suggestions
- Performance test generation

---

## How to Update This Skill

### If Testing Framework Changes
```
Update: SKILL.md → Phase 1C Setup section
Update: references/setup-guide.md with new framework
No impact on core RED-GREEN-REFACTOR cycle
```

### If Team Changes Code Standards
```
Update: code-review-standards skill (not this skill)
This skill references code-review-standards
Changes automatically apply to REFACTOR phase
```

### If Team Changes Commit Format
```
Update: commit-message-standards skill (not this skill)
This skill references commit-message-standards
Changes automatically apply to COMMIT phase
```

### If You Discover Anti-Pattern
```
Update: SKILL.md → "Common Anti-Patterns & How to Avoid Them"
Provide example of the anti-pattern
Explain why it's problematic
Provide solution + prevention
Add to code-quality agent coaching scripts
```


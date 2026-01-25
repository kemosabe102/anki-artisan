# TDD Skill Design: Complete Overview

This package contains a production-ready **Test-Driven Development (TDD) skill** for the Claude Code agent system. It teaches the RED-GREEN-REFACTOR workflow as a structured, repeatable process.

---

## 📦 What You Have

Four comprehensive design documents:

### 1. **tdd-skill-design.md** ← START HERE
**What:** Main skill definition  
**Contains:**
- Skill metadata (progressive disclosure header)
- 3-phase workflow (Feature Planning, TDD Loop, Final Review)
- Detailed RED-GREEN-REFACTOR-REVIEW-COMMIT phases
- Checklists for each phase
- Common anti-patterns and fixes
- How the `code-quality` agent uses this skill

**Use for:** Understanding the complete TDD workflow at a glance

---

### 2. **code-quality-agent.md**
**What:** Agent specification that coaches developers  
**Contains:**
- Agent purpose and responsibilities
- Interaction model (how it coaches)
- Internal workflow per phase
- Quality gates (what the agent enforces)
- Example conversation flow
- Tool access scope
- Coordination with other skills

**Use for:** Understanding how the agent guides developers through TDD

---

### 3. **tdd-developer-workflow.md**
**What:** Practical guide for developers using the skill  
**Contains:**
- Quick start (setup, first chunk)
- Step-by-step for each phase (RED, GREEN, REFACTOR, REVIEW, COMMIT)
- Real code examples (JavaScript/Python templates)
- Common mistakes and how to avoid them
- Complete chunk walkthrough example
- Time tracking template
- Troubleshooting guide
- Success checklist

**Use for:** Day-to-day development when building features with TDD

---

### 4. **tdd-architecture-design.md**
**What:** System architecture and integration  
**Contains:**
- Complete system architecture diagram
- Information flow (developer → agent → skill)
- Detailed interaction sequence (19 steps)
- File structure created
- Quality gates (pseudo-code)
- Skill invocation dependencies
- Context management strategy
- Success metrics
- Skill version roadmap

**Use for:** Understanding how TDD skill fits into Claude Code system

---

## 🚀 How to Implement This

### Step 1: File Setup

```bash
# Create skill directory
mkdir -p .claude/skills/test-driven-development/{references,scripts}

# Create agent file
mkdir -p .claude/agents

# Create workflows tracking directory
mkdir -p .claude/workflows
```

### Step 2: Populate Files

```bash
# Main skill file
cp tdd-skill-design.md .claude/skills/test-driven-development/SKILL.md

# Agent definition
cp code-quality-agent.md .claude/agents/code-quality.md

# Developer guides
cp tdd-developer-workflow.md .claude/workflows/TDD_DEVELOPER_GUIDE.md

# Architecture reference
cp tdd-architecture-design.md .claude/documentation/TDD_ARCHITECTURE.md
```

### Step 3: Create Supporting Files

**.claude/workflows/WORKFLOW_STATUS.md** (Use as template)
```markdown
# Feature: [Your Feature Name]

## Feature Breakdown

### Chunk 1: [Chunk Name] (Status: PENDING)
- Status: Not started
- Activities: RED, GREEN, REFACTOR, REVIEW, COMMIT
- Tests written: 0
- Implementation: 0 lines
- Commits: None

### Chunk 2-N: ...
```

### Step 4: Reference from CLAUDE.md

**.claude/CLAUDE.md** (Root project map)
```markdown
# Project Overview

## Development Workflow: TDD

For feature development using Test-Driven Development:
- **Skill:** [test-driven-development](./skills/test-driven-development/SKILL.md)
- **Agent:** [code-quality](./agents/code-quality.md)
- **Developer Guide:** [TDD Workflow](./workflows/TDD_DEVELOPER_GUIDE.md)

Features are broken into 40-90 minute chunks.
Each chunk: RED → GREEN → REFACTOR → REVIEW → COMMIT

See `workflows/WORKFLOW_STATUS.md` for current feature progress.
```

### Step 5: Configure Orchestrator

In your orchestrator agent logic:

```python
# Orchestrator routing logic

def route_user_intent(user_query):
    # TDD coaching signals
    if "TDD" in query or "test-driven" in query or "RED phase" in query:
        return route_to_agent("code-quality")
    
    # Code quality signals
    if "code review" in query or "clean code" in query:
        return route_to_agent("code-quality")
    
    # ... other domains
```

---

## 📊 Workflow Overview

### User → Agent → Skill Flow

```
User: "I want to build authentication using TDD"
  ↓
Orchestrator: Routes to code-quality agent
  ↓
code-quality agent:
  1. Loads test-driven-development skill (metadata first)
  2. Guides Phase 1: Break feature into chunks
  3. Iterates Phase 2: RED-GREEN-REFACTOR per chunk
     - Each cycle: 40-90 minutes
     - Each cycle: 1 atomic commit
     - Each cycle: Tests + clean code
  4. Tracks progress in WORKFLOW_STATUS.md
  5. Enforces quality gates at each phase
  ↓
Output: Feature complete with:
- 100% test coverage
- Clean code
- Atomic commits with clear messages
- History that explains why changes were made
```

---

## ✅ Quality Gates (What Gets Enforced)

The agent blocks progress at each phase until criteria met:

### 🔴 RED Phase
- [ ] Test must fail (not skip, not error)
- [ ] Test must be focused on one behavior
- [ ] Test name clearly expresses behavior
- If gate fails: Agent requests fixes

### 🟢 GREEN Phase
- [ ] All tests pass (including new one)
- [ ] No regressions in existing tests
- [ ] Implementation is minimal (not over-engineered)
- If gate fails: Agent requests debugging/fixes

### 🔵 REFACTOR Phase
- [ ] Code is clean (no duplication, clear names)
- [ ] Tests still pass after refactoring
- [ ] No code smells detected
- If gate fails: Agent provides specific suggestions

### 🟡 REVIEW Phase
- [ ] Test coverage >80% for chunk
- [ ] No console.logs or debug code
- [ ] No `.skip` or `.only` in tests
- [ ] Edge cases are tested
- If gate fails: Agent blocks commit

### ✅ COMMIT Phase
- [ ] Only this chunk's files are staged
- [ ] Commit message follows conventional format
- [ ] All tests pass after commit
- [ ] Message is clear and descriptive
- If gate fails: Agent rejects commit

---

## 🎯 Time Investment Per Chunk

| Phase | Time | Focus |
|-------|------|-------|
| RED | 5-15 min | Define behavior via failing test |
| GREEN | 10-30 min | Implement minimal code to pass |
| REFACTOR | 10-20 min | Improve code quality |
| REVIEW | 5-10 min | Final quality checks |
| COMMIT | 3-5 min | Save atomic commit |
| **TOTAL** | **40-90 min** | **One complete chunk** |

Example for 6-chunk feature:
- 6 chunks × 60 min average = 360 minutes
- 360 minutes = 6 hours of development
- Plus code review time (separate from TDD loop)

---

## 🔗 Skill Dependencies

This skill invokes three other skills:

1. **code-review-standards** (during REFACTOR phase)
   - Provides checklist: What is "clean code"?
   - Identifies code smells
   - Suggests refactoring patterns

2. **debugging-methodology** (when tests fail unexpectedly)
   - Step-by-step debugging approach
   - Root cause analysis
   - Test validation strategies

3. **commit-message-standards** (during COMMIT phase)
   - Conventional commit format
   - Team conventions
   - Message validation

**Note:** The agent handles invocation—developers don't call skills directly.

---

## 🎓 Developer Experience

When developer says: **"I want to build X using TDD"**

Agent responds:

```
1. Great! Let's plan this feature.
   
2. Feature: X
   Acceptance Criteria: [develops with developer]
   
3. Let me break this into chunks:
   Chunk 1: [isolated piece 1]
   Chunk 2: [isolated piece 2]
   ...
   
4. Total estimated time: 6-8 hours
   
5. Let's start Chunk 1. Write a failing test for: [behavior]
   
   [Developer writes test → agent verifies RED gate]
   
6. Now implement minimal code to pass that test:
   
   [Developer implements → agent verifies GREEN gate]
   
7. Refactor for quality:
   
   [Developer refactors → agent verifies REFACTOR gate]
   
8. Self-review before committing:
   
   [Developer reviews → agent verifies REVIEW gate]
   
9. Create atomic commit:
   
   [Developer commits → agent verifies COMMIT gate]
   
10. Chunk 1 complete! ✅
    
    Ready for Chunk 2?
    
    [Loop repeats for chunks 2-6]
```

---

## 📈 Success Metrics

### You'll Know It's Working When...

**Quantitative:**
- ✅ 100% of production code has passing tests
- ✅ Test coverage >80% per feature
- ✅ Zero low-quality code reaches main branch
- ✅ Commits are atomic (1-3 files per commit)
- ✅ Code review time decreases 40%
- ✅ Production bug rate decreases 60%+

**Qualitative:**
- ✅ Developers trust the quality gates
- ✅ Code is consistent across team
- ✅ Onboarding is faster (TDD workflow is clear)
- ✅ Developers feel confident refactoring
- ✅ Code reviews are pleasant (no "obvious" issues)
- ✅ You can explain why each change was made
- ✅ New developers can understand code in 5 minutes

---

## 🔄 Continuous Improvement

### When to Update the Skill

**Add language-specific examples:**
- If team adds Python, Go, or Rust projects
- Reference section: `references/python-examples.md`

**Refine definitions of done:**
- If team discovers new issues
- Update relevant phase checklist

**Add anti-patterns:**
- If team discovers new mistakes
- Add to anti-patterns section
- Include fix + prevention

**Enhance integration:**
- If team adds CI/CD
- Add integration guidance
- Create scripts for automation

---

## 🏗️ File Organization

```
.claude/
├── CLAUDE.md                           (Project map)
├── agents/
│   └── code-quality.md                (This agent)
├── skills/
│   └── test-driven-development/
│       ├── SKILL.md                   (Main skill file)
│       ├── references/
│       │   ├── red-phase-guide.md
│       │   ├── green-phase-guide.md
│       │   ├── refactor-patterns.md
│       │   └── anti-patterns.md
│       └── scripts/
│           ├── verify-tests.sh
│           ├── coverage-report.sh
│           └── setup-test-framework.sh
└── workflows/
    └── WORKFLOW_STATUS.md            (Current progress)
```

---

## 🚀 Next Steps

1. **Review all 4 documents** to understand the system
2. **Create file structure** (.claude directories)
3. **Copy SKILL.md and AGENT.md** into appropriate locations
4. **Create WORKFLOW_STATUS.md** template
5. **Update CLAUDE.md** to reference this skill
6. **Configure orchestrator** to route TDD queries to code-quality agent
7. **Start with first feature** using the workflow

---

## ❓ FAQ

### "How is this different from just 'write tests'?"
TDD is **structured, repeatable, coached**. This skill provides:
- Clear phases with checklists
- Agent that guides you through each phase
- Quality gates that prevent low-quality code
- Enforced chunk sizes (40-90 min each)
- Atomic commits that tell a story

### "Won't this slow me down?"
**No.** Upfront investment (TDD overhead) is paid back in:
- 60% fewer production bugs
- 40% faster code reviews
- Faster refactoring (tests protect you)
- Fewer production incidents

### "What if my feature doesn't fit into chunks?"
It does. Even complex features break down. Examples:
- "User authentication" → 6 chunks (email validation, password hashing, model, endpoints, etc.)
- "Payment processing" → 8 chunks (validation, calculation, database, API integration, error handling, etc.)
- "Real-time notifications" → 5 chunks (event capture, queue, processing, delivery, acknowledgment)

### "Can I use a different testing framework?"
**Yes.** The phases (RED-GREEN-REFACTOR) are framework-agnostic. The skill includes examples, but the workflow is the same for:
- Jest, Vitest, Mocha (JavaScript)
- Pytest, Unittest (Python)
- Go test, Testify (Go)
- Cargo test (Rust)

### "What if I'm not a TDD expert?"
**That's exactly why this skill exists.** The `code-quality` agent coaches you through each phase. You don't need to be expert—just follow the checklists.

---

## 📖 Reading Order

**For a quick overview:**
1. This document (5 minutes)
2. Architecture diagram in tdd-architecture-design.md (5 minutes)
3. Developer quick start in tdd-developer-workflow.md (10 minutes)

**For implementation:**
1. tdd-skill-design.md (main reference)
2. code-quality-agent.md (how it coaches)
3. tdd-architecture-design.md (how it fits together)
4. tdd-developer-workflow.md (practical guide)

**For daily use:**
- tdd-developer-workflow.md (bookmark this!)
- SKILL.md Phase 2 sections (RED, GREEN, REFACTOR, REVIEW, COMMIT)

---

## 📝 License & Attribution

This TDD skill design is based on:
- Robert C. Martin's "Clean Code" TDD practices
- Kent Beck's "Test Driven Development" methodology
- Extreme Programming (XP) practices
- Modern DevOps and CI/CD best practices

Customized for Claude Code agent system architecture.

---

## 🙋 Support & Questions

When things aren't clear:
1. Check the **Common Mistakes** section in tdd-developer-workflow.md
2. Review the **Anti-patterns** section in tdd-skill-design.md
3. Ask the `code-quality` agent (it's designed to help!)
4. Reference SKILL.md Phase 2 for detailed guidance

---

**You're ready to build with TDD. Let's go!** 🚀


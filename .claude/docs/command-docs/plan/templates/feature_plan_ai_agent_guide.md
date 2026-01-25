# Using Feature Plans with AI Agents - Implementation Guide

This guide explains how to use the feature plan JSON with AI coding agents (like Claude) to incrementally build features while maintaining code quality and preventing common failure modes.

## The Problem We're Solving

Research by Anthropic on spec-driven development identified key failure modes when AI agents build projects:

1. **One-shotting**: Agent tries to implement entire feature at once, losing focus
2. **Premature completion**: Agent marks feature done without proper end-to-end testing
3. **Context loss**: No record of what was attempted, what failed, why decisions were made
4. **Unbounded work**: Agent doesn't know when to stop
5. **State corruption**: Agent breaks existing working code trying to build new features

## The Feature Plan as Truth Source

The feature plan JSON serves as:
- **Specification**: What needs to be built (steps + acceptance criteria)
- **Progress tracker**: Which features are complete (passes field)
- **Boundaries**: Clear scope limiting (prevents one-shotting)
- **Audit log**: History of what was attempted and why (commit messages + progress file)

## Workflow: From Roadmap Item to Specification to Implementation

```
Roadmap Item
    ↓
    Write Comprehensive Specification
    ↓
    Create Feature Plan JSON (3-7 independent features per phase)
    ↓
    AI Agent reads feature plan
    ↓
    Agent works on ONE feature at a time
    ↓
    Agent completes steps + verifies acceptance criteria
    ↓
    Agent tests end-to-end (human user testing)
    ↓
    Agent commits with message
    ↓
    Agent updates WORKFLOW_STATUS.md
    ↓
    Agent marks passes: true ONLY when complete
    ↓
    Move to next feature
```

## How to Use Feature Plan with AI Agents

### 1. Initial Setup

**You create:**
1. Comprehensive specification document (see specification_components.md)
2. Feature plan JSON with 3-7 features broken down per phase
3. WORKFLOW_STATUS.md tracking progress
4. Blank project structure (src/, tests/, docs/)

**Agent should:**
1. Read specification thoroughly
2. Read feature plan JSON
3. Verify they understand Phase 1 features
4. Ask clarifying questions about acceptance criteria
5. Do NOT start coding until clear on current feature

### 2. Working on a Single Feature

**Agent prompt pattern:**
```
You are working on the Feature Plan for [PROJECT_NAME].

Current Phase: Phase 1 - Foundation & Data Pipeline
Current Feature: FOUNDATION_001 - FRED API integration
Status: passes = false

Your task is to COMPLETE THIS FEATURE ONLY.

Feature Plan:
{copy the FOUNDATION_001 feature object here}

Instructions:
1. Read all steps carefully
2. Implement each step in order
3. After each step, verify it works
4. When all steps done, run acceptance tests
5. Do NOT move to next feature
6. Update WORKFLOW_STATUS.md with progress
7. Commit with message: "Implement FOUNDATION_001: [description]"
8. Change passes: false → passes: true ONLY when all criteria met

Do NOT:
- Skip steps
- Mark passes: true without verification
- Edit feature plan (except passes field)
- Work on next feature until this is 100% done
```

### 3. Testing Requirements

**For each feature, agent MUST:**

1. **Unit tests**: Write tests matching acceptance criteria
   ```python
   # Example
   def test_fred_api_valid_connection():
       api = FREDDataFetcher(api_key="test_key")
       result = api.fetch("BAMLH0A0HYM2", date="2025-01-02")
       assert result is not None
       assert isinstance(result, float)
   ```

2. **Integration test**: Verify feature works in context
   ```python
   # Example
   def test_fred_api_in_calculation_pipeline():
       calc = SmartFearGreed()
       components = calc.calculate_all_components()
       assert components['junk_bond']['raw_value'] is not None
   ```

3. **End-to-end test**: Run as human user would use it
   ```
   - Start application
   - Navigate to regime calculation
   - Verify data loads from API
   - Check output is in expected format
   - No errors in logs
   ```

**Critical rule**: Only mark `passes: true` when all three test levels pass.

### 4. Version Control Integration

**After completing a feature, agent should:**

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "Implement FOUNDATION_001: FRED API integration and authentication

- Set up FRED API key management system
- Created FREDDataFetcher class with caching decorator
- Implemented connection testing and error handling
- All 3 acceptance criteria verified:
  ✓ FRED API returns valid bond OAS data for test date (Jan 2, 2024)
  ✓ Cache prevents redundant API calls (verified in logs)
  ✓ Error handling gracefully manages API timeouts (tested with mock)
- Unit tests: 6/6 passing
- Execution time: 1.8 hours (estimated 2.0)"

# Never force push or rebase—use linear history for traceability
```

### 5. Progress Tracking (WORKFLOW_STATUS.md)

Agent updates this file after EACH feature:

```markdown
# Feature Plan Progress - Smart Fear & Greed Indicator

## Current Status
Phase: Phase 1 (Foundation & Data Pipeline)
Progress: 3/7 complete (43%)
Last Updated: 2025-12-18 15:45 UTC
Completed By: Claude (Agent ID: claude-3-5-sonnet)

## Completed Features (this session)
- [x] FOUNDATION_001 - FRED API integration (2025-12-17, 1.8h)
- [x] FOUNDATION_002 - Yahoo Finance batch downloader (2025-12-17, 3.2h)
- [x] FOUNDATION_003 - VIX data fetcher (2025-12-18, 1.4h)

## Current Work
- [ ] FOUNDATION_004 - CBOE Put/Call ratio (in progress, 0.5h elapsed)

## Next Features
- [ ] FOUNDATION_005 - Scheduler setup
- [ ] FOUNDATION_006 - SmartFearGreed class
- [ ] FOUNDATION_007 - Unit test framework

## Known Issues
None currently blocking progress.

## Code Quality Metrics
- Test coverage: 87% (target: >85%)
- All tests passing: YES
- Code review: Pending (awaiting human review)
```

### 6. Common Agent Mistakes to Prevent

**Problem: Agent tries to implement multiple features at once**
- Solution: Give agent ONE feature at a time. Include explicit: "Work on ONLY this feature."
- Verification: Ask agent: "Which feature are you working on?" Should answer with single ID.

**Problem: Agent marks passes: true without testing**
- Solution: Require agent to show test output and coverage metrics
- Verification: Ask: "Show me the test output proving all 3 acceptance criteria are met"

**Problem: Agent edits feature plan to remove difficult acceptance criteria**
- Solution: Strong instruction in prompt: "It is unacceptable to remove, edit, or change the feature plan. Only change passes: false → true"
- Verification: Git diff should show ONLY passes field change, nothing else

**Problem: Agent doesn't run end-to-end tests, only unit tests**
- Solution: Require browser automation or manual testing steps
- Verification: Ask: "Can a human user walk through [scenario]? Show me screenshot or video."

**Problem: Agent accumulates too much state in context, gets confused**
- Solution: Use git commits + WORKFLOW_STATUS.md as external memory
- Verification: Ask: "What did you complete in previous sessions?" Should reference commit messages

**Problem: Agent leaves project in broken state**
- Solution: Require git status be clean before marking feature done
- Verification: Agent should show: `git status` → `nothing to commit, working tree clean`

### 7. Example Interaction Flow

**Human:**
```
I have a feature plan for Smart Fear & Greed Indicator. 
Phase 1 has 7 features. I want you to work on FOUNDATION_001.

Here is the feature:
{copy feature object from JSON}

IMPORTANT:
- Work on THIS FEATURE ONLY
- Do not start FOUNDATION_002 until FOUNDATION_001 is 100% done
- Mark passes: true ONLY when all criteria verified
- Update WORKFLOW_STATUS.md after you finish
- Commit to git with descriptive message

Start with: What is your understanding of this feature?
```

**Agent:**
```
I understand FOUNDATION_001: FRED API integration.

Objective: Set up FRED API connection with caching.

Required steps:
1. API key management
2. FRED data fetcher class with caching
3. Connection testing
4. Bond spread data retrieval
5. Verify 5:00 AM ET availability check

Acceptance criteria I must meet:
1. FRED API returns valid bond OAS data for test date
2. Cache prevents redundant API calls
3. Error handling manages API timeouts

My plan:
- Hour 1: Implement FREDDataFetcher class + basic connection
- Hour 0.5: Add caching decorator
- Hour 0.3: Write unit tests
- Hour 0.2: Test end-to-end with real API

Should I proceed?
```

**Human:**
```
Yes, proceed. Start with step 1 (API key management) and show me:
1. Code
2. Unit test proving it works
3. Any console output
```

**Agent:**
```
[Implements step 1, shows code, shows test output]

Test result: PASSED ✓

Proceeding to step 2...
```

[After completing all steps]

**Agent:**
```
FOUNDATION_001 Complete!

Summary:
✓ All 5 steps completed
✓ All 3 acceptance criteria verified
✓ 4 unit tests passing
✓ End-to-end test: API call succeeds, returns valid data

Commits made:
- c4d92a1 Implement FREDDataFetcher class with caching

Next action: Updating WORKFLOW_STATUS.md and ready for FOUNDATION_002
```

**Human:**
```
Great! Before you start FOUNDATION_002, take a 5-minute break for my code review.

[Human reviews the implementation, approves]

OK, proceed to FOUNDATION_002. Here is the feature:
{copy FOUNDATION_002 feature object}
```

## Anti-Patterns to Avoid

❌ **"Implement all Phase 1 features"** → Wrong! Start with Feature 1 only.

❌ **"Here's the whole spec, build the project"** → Wrong! Use feature plan as guide, one feature at a time.

❌ **"Mark it done if 80% of criteria met"** → Wrong! 100% or nothing. All criteria must pass.

❌ **"Skip testing, we'll fix bugs later"** → Wrong! Testing IS part of feature completion.

❌ **"Let me refactor/improve the last feature"** → Wrong! Move to next feature. Create new feature for improvements.

## Success Patterns

✅ **One feature at a time**: Clear boundaries, focused context

✅ **Steps + acceptance criteria**: Unambiguous requirements

✅ **Commit after each feature**: Audit trail, rollback capability

✅ **WORKFLOW_STATUS.md**: External memory, progress visibility

✅ **Test at three levels**: Unit, integration, end-to-end

✅ **Git as source of truth**: Not context window, not memory

✅ **Incremental delivery**: Can deploy after each phase

## Integration with Continuous Integration

Set up CI/CD to validate feature plan automatically:

```yaml
# .github/workflows/feature-plan-validation.yml
name: Feature Plan Validation

on: [push]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate feature plan JSON
        run: python -m json.tool feature_plan.json > /dev/null
      
      - name: Run all tests
        run: pytest tests/ --cov=src/ --cov-report=xml
      
      - name: Check no incomplete features pass
        run: |
          # Fail if any feature has passes:true but tests don't pass
          python scripts/validate_feature_plan.py
```

## Metrics to Track

Over time, measure:
- **Velocity**: Features completed per week
- **Quality**: Test coverage, bugs found in production
- **Accuracy**: Estimated vs actual hours (improve estimation)
- **Success rate**: % of features completed first try vs requiring fixes
- **Rework**: % of time spent fixing vs new feature work

## When to Adjust the Plan

If you discover a feature is:
- **Too large** (>4 hours): Split into 2-3 smaller features
- **Too vague**: Add more detail to steps/acceptance criteria
- **Has wrong assumption**: Document the assumption, mark it as failed, create new feature for correction
- **Blocked**: Move to different feature, come back when blocker resolved

Update the feature plan JSON, commit change, communicate to all agents.

---

**Key Principle**: The feature plan JSON is your contract with AI agents. Be precise about requirements. Be disciplined about one-feature-at-a-time. Use git + progress files as external memory. Test thoroughly at three levels. The result is reliable, traceable, incrementally-delivered features.

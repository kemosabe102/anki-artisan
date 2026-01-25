# Feature Plan Template

This template is used for creating structured feature plan files in JSON format. Each feature breaks down into discrete, testable steps with clear acceptance criteria.

## File Structure Overview

The feature plan JSON contains:
- **Project metadata**: name, description, total features count
- **Phases**: logical groupings of work by 1-2 weeks
- **Features**: individual units of work within phases (typically 30-90 minutes each)
- **Summary**: rollup view of timeline and critical path

## Feature Object Structure

```json
{
  "id": "FEATURE_NNN",
  "category": "functional|infrastructure|testing|performance|documentation",
  "description": "Human-readable feature title",
  "steps": [
    "Step 1: Describes concrete action",
    "Step 2: Describes next action",
    "..."
  ],
  "acceptance_criteria": [
    "Criterion 1: Measurable/verifiable requirement",
    "Criterion 2: Measurable/verifiable requirement",
    "..."
  ],
  "passes": false,
  "estimated_hours": 1.5
}
```

## Feature ID Naming Convention

Use prefixes that indicate phase and category:
- `FOUNDATION_NNN` - Phase 1 infrastructure setup
- `COMPONENT_NNN` - Core component implementation
- `REGIME_NNN` - Regime detection and classification
- `OUTPUT_NNN` - JSON generation and orchestration
- `BACKTEST_NNN` - Testing and validation
- `AGENT_NNN` - AI agent integration
- `LAUNCH_NNN` - Production launch preparation

Or use domain-specific prefixes for your feature:
- `AUTH_NNN` - Authentication
- `UI_NNN` - User interface
- `API_NNN` - API endpoints
- `DB_NNN` - Database operations

## Category Types

- **functional**: Core feature functionality that users/systems see
- **infrastructure**: Setup, dependencies, frameworks, CI/CD, tooling
- **testing**: Test suites, validation, verification, backtesting
- **performance**: Optimization, caching, profiling, load testing
- **documentation**: Guides, API docs, comments, runbooks
- **bug_fix**: Defect resolution

## Phase Structure

```json
{
  "phase_N": {
    "name": "Phase Name - 1-3 words describing phase goal",
    "duration_weeks": 2,
    "target_completion": "Week X",
    "features": [
      { feature objects here }
    ]
  }
}
```

**Best Practices for Phases:**
- Keep each phase to 1-2 weeks of work
- Phases should be independently valuable (can ship at end of each phase)
- Each phase has 4-10 features
- Phases should have clear entry/exit criteria
- Later phases may depend on earlier phases

## Steps Best Practices

**Each step should be:**
- **Concrete**: Describe specific actions, not abstract outcomes
- **Testable**: Someone should be able to verify completion
- **Sequenced**: Build on previous steps logically
- **Detailed enough**: Junior engineer could follow without hand-holding
- **Time-aware**: Estimate should match step complexity

**Example Good Steps:**
```json
"steps": [
  "Create UserAuth class with __init__ method",
  "Implement login(username, password) method with regex validation",
  "Add password hashing using bcrypt with salt",
  "Create unit test for valid login credentials",
  "Create unit test for invalid credentials",
  "Verify unit tests pass without errors"
]
```

**Example Bad Steps (too vague):**
```json
"steps": [
  "Implement authentication",
  "Add tests",
  "Make it work"
]
```

## Acceptance Criteria Best Practices

**Each criterion should be:**
- **Measurable**: Include numbers, thresholds, or concrete outcomes
- **Verifiable**: Can be checked by inspection or automated test
- **Independent**: Can be evaluated separately from others
- **Result-focused**: Describe what must be true, not how to build it
- **Non-negotiable**: Define minimum bar for "done"

**Example Good Criteria:**
```json
"acceptance_criteria": [
  "API endpoint returns 200 status code for valid requests",
  "Response time <200ms for 95th percentile requests",
  "Database query uses indexed lookup (explain plan verified)",
  "Unit tests achieve >85% code coverage",
  "Handles 10,000 concurrent connections without errors"
]
```

**Example Bad Criteria (too vague):**
```json
"acceptance_criteria": [
  "It works",
  "Looks good",
  "No errors"
]
```

## Time Estimation Guidance

Use these ranges to keep features in 30-90 minute sweet spot:

| Estimated Hours | Feature Size | Examples |
|-----------------|--------------|----------|
| 0.5 | Tiny | Add config parameter, write unit test, fix typo |
| 1.0 | Small | Simple API endpoint, basic validation, simple calculation |
| 1.5 | Small-Medium | Component with 1-2 dependencies, moderate testing |
| 2.0 | Medium | Feature with full testing, doc, light integration |
| 2.5 | Medium | Complex logic, comprehensive test suite |
| 3.0 | Medium-Large | Full feature with integration, performance tuning |
| 4.0+ | Large | Split into smaller features |

**Rule: If estimated >3.5 hours, break into multiple features.**

## `passes` Field

- Set to `false` initially (feature not yet complete)
- Change to `true` ONLY when:
  - All steps completed
  - All acceptance criteria verified/passed
  - Code changes committed to git with message
  - Tests written and passing
  - Documentation updated
- Use strongly-worded instructions: "Never remove or edit passes field outside of verification"

## Full Template Example

```json
{
  "project": "Project Name v1.0",
  "description": "High-level description of what this project does",
  "total_features": 15,
  "phases": {
    "phase_1": {
      "name": "Foundation & Setup",
      "duration_weeks": 1,
      "target_completion": "Week 1",
      "features": [
        {
          "id": "FOUNDATION_001",
          "category": "infrastructure",
          "description": "Project repository setup and basic structure",
          "steps": [
            "Create git repository with standard .gitignore",
            "Create README.md with project description and setup instructions",
            "Create src/, tests/, docs/ directories",
            "Initialize package.json or requirements.txt with dependencies",
            "Create GitHub Actions CI/CD pipeline",
            "Verify build passes locally and on CI"
          ],
          "acceptance_criteria": [
            "Repository exists with proper structure",
            ".gitignore prevents committing node_modules or __pycache__",
            "README includes quick-start instructions",
            "CI pipeline runs on every push",
            "All tests pass on CI"
          ],
          "passes": false,
          "estimated_hours": 1.5
        },
        {
          "id": "FOUNDATION_002",
          "category": "testing",
          "description": "Setup test framework and test data",
          "steps": [
            "Install test framework (pytest, jest, mocha, etc.)",
            "Create test directory structure with fixtures/",
            "Create test data file with sample inputs/outputs",
            "Write first passing sanity test",
            "Verify test runner discovers and executes tests"
          ],
          "acceptance_criteria": [
            "Test framework installed and working",
            "Test directory structure created",
            "Test data fixtures load without errors",
            "First test passes successfully",
            "CI runs tests on every commit"
          ],
          "passes": false,
          "estimated_hours": 1.0
        }
      ]
    },
    "phase_2": {
      "name": "Core Functionality",
      "duration_weeks": 2,
      "target_completion": "Week 3",
      "features": [
        {
          "id": "FEATURE_001",
          "category": "functional",
          "description": "User can create new item",
          "steps": [
            "Create Item class with required fields (name, description)",
            "Implement __init__ with field validation",
            "Write unit test for valid Item creation",
            "Write unit test for invalid data (missing name)",
            "Add docstring with usage example",
            "Verify all tests pass"
          ],
          "acceptance_criteria": [
            "Item object instantiates with valid data",
            "Item requires name (non-empty string)",
            "Item requires description (non-empty string)",
            "Unit test for valid case passes",
            "Unit test for invalid case passes",
            "Validation error message is clear"
          ],
          "passes": false,
          "estimated_hours": 1.5
        }
      ]
    }
  },
  "summary": {
    "total_features": 15,
    "total_estimated_hours": 28,
    "phases_total": 2,
    "implementation_timeline": "3 weeks",
    "critical_path": [
      "FOUNDATION_001-002 (setup and CI)",
      "FEATURE_001-005 (core functionality)",
      "FEATURE_INTEGRATION_001 (end-to-end validation)"
    ],
    "launch_readiness_gates": [
      "Phase 1 Complete: Build passes, tests running on CI",
      "Phase 2 Complete: All core functionality implemented and tested"
    ]
  }
}
```

## Tips for Using This Template

### For Planning
1. Break feature from roadmap into **3-7 independent features** per phase
2. Each feature should be testable in isolation
3. Estimate each feature independently
4. Sum estimates to get phase time
5. Assign critical features to earlier phases

### For Development
1. Work on ONE feature at a time
2. Change `passes: false` → `true` ONLY when complete + tested
3. After each feature, commit to git with clear message:
   ```
   git commit -m "Implement FEATURE_001: User authentication

   - Adds login/signup endpoints
   - Implements password hashing
   - All 8 acceptance criteria verified
   - Tests passing locally and on CI"
   ```
4. Write progress file after each feature:
   ```markdown
   # Progress - 2025-12-17

   ## Completed
   - [x] FEATURE_001 (auth login)
   - [x] FEATURE_002 (auth signup)

   ## In Progress
   - [ ] FEATURE_003 (password reset) - 60% done

   ## Blocked
   - FEATURE_004 depends on email service setup (waiting for DevOps)

   ## Next Steps
   1. Complete password reset feature
   2. Add 2FA support
   ```

### Critical Rules
- ✅ DO: Modify only the `passes` field when marking features complete
- ✅ DO: Commit regularly with descriptive messages
- ✅ DO: Update `WORKFLOW_STATUS.md` after each feature
- ✅ DO: Keep features focused and time-bounded (30-90 min each)
- ❌ DON'T: Remove or edit test requirements unless specification changes
- ❌ DON'T: Mark feature as `passes: true` without full verification
- ❌ DON'T: Combine multiple features into one to meet time estimate

## JSON Validation

Before committing, validate your feature plan JSON:
```bash
# Python
python -m json.tool feature_plan.json > /dev/null

# Node.js
node -e "require('./feature_plan.json')"

# Online tools
https://jsonlint.com/
```

Your feature plan should be valid JSON with no syntax errors.

## Integration with Development Workflow

This feature plan works best with:
1. **Git commits**: Each completed feature has its own commit
2. **Progress tracking**: `WORKFLOW_STATUS.md` updated after each feature
3. **Code reviews**: Review each feature's implementation against steps and criteria
4. **Testing**: Run full test suite before marking `passes: true`
5. **Documentation**: Update docs when relevant acceptance criteria met

## Example Progress File (WORKFLOW_STATUS.md)

```markdown
# Feature Plan Progress - Smart Fear & Greed Indicator v3.1

## Timeline
- Start Date: 2025-12-16
- Target Launch: 2026-04-30 (Week 16)
- Current Phase: Phase 1 - Foundation & Data Pipeline

## Phase 1: Foundation & Data Pipeline (Weeks 1-2)
**Status:** 3/7 Complete (43%)
**Target:** Week 2

- [x] FOUNDATION_001 - FRED API integration (✓ 2025-12-17)
- [x] FOUNDATION_002 - Yahoo Finance batch downloader (✓ 2025-12-17)
- [x] FOUNDATION_003 - VIX data fetcher (✓ 2025-12-18)
- [ ] FOUNDATION_004 - CBOE Put/Call ratio
- [ ] FOUNDATION_005 - Scheduler setup
- [ ] FOUNDATION_006 - SmartFearGreed class
- [ ] FOUNDATION_007 - Unit test framework

**Last Updated:** 2025-12-18 15:45 UTC
**Current Owner:** Engineer A

## Phase 2: Core Components (Weeks 3-4)
**Status:** 0/7 Not Started
**Target:** Week 4

## Recent Commits
```
2025-12-18: Implement FOUNDATION_003 (VIX fetcher)
2025-12-17: Implement FOUNDATION_002 (Yahoo batch downloader)
2025-12-17: Implement FOUNDATION_001 (FRED API)
```

## Blockers
None currently.

## Next Actions
1. Start FOUNDATION_004 (CBOE PCR data)
2. Review FOUNDATION_001-003 code
3. Prepare FOUNDATION_005 scheduler infrastructure
```

---

**Last Updated:** 2025-12-17
**Template Version:** 1.0
**Based On:** Anthropic specification-driven development research + industry best practices

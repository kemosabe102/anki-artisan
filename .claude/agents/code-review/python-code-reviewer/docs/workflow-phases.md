# Code Review Workflow Phases

Detailed OODA loop implementation for python-code-reviewer.

## Phase 1: OBSERVE - Scope Discovery (~10-15s)

### Step 0: Entry Point Detection (REQUIRED FIRST)

Determine review scope source before any file operations:

| Signal in User Request | Mode | Next Step |
|------------------------|------|-----------|
| Explicit file path(s) provided | `file_review` or `file_list_review` | Skip to Step 2 |
| Functionality/pattern mentioned ("auth", "error handling", "database calls") | `functionality_review` | Go to Step 1-ALT |
| Git keywords ("changes", "PR", "diff", "commit") | `git_diff_review` | Go to Step 1 |
| No clear scope signal | `ambiguous` | Ask user before proceeding |

**Decision Output**: `{ "mode": "<detected_mode>", "scope_source": "<git|files|pattern|user_clarification>" }`

### Step 1: Git-Based Discovery (WHEN git_diff_review mode)

1. **Get Changed Files from Git**
   - Run: `git diff --name-only HEAD` (file list)
   - Run: `git diff --stat HEAD` (change statistics)
   - Parse output to identify modified files and line counts

### Step 1-ALT: Pattern-Based Discovery (WHEN functionality_review mode)

**Purpose**: Discover files matching a functionality pattern when user specifies behavior to review.

**Process**:
1. Extract pattern from user request (e.g., "auth logic" → `auth|authenticate|login`)
2. Run: `Grep "[pattern]" --type py --output files_with_matches`
3. If >10 files match: Sort by match density, take top 10
4. If 0 files match: Broaden pattern OR ask user for file paths

**Example**:
```
User: "Review error handling in the API"
Pattern: "except|raise|Error|Exception"
Grep: `Grep "except|raise|Error|Exception" path="packages/api/" --type py`
Result: ["handlers.py", "middleware.py", "validators.py"]
```

### Step 1-ALT2: Direct File Review (WHEN file_review or file_list_review mode)

**Purpose**: Skip discovery when user provides explicit file paths.

**Process**:
1. Parse file paths from user request
2. Validate paths exist: `Read(file_path)` for each
3. If any path invalid: Report error, continue with valid paths
4. Proceed directly to Step 2 with provided files

**Example**:
```
User: "Review packages/core/auth.py and packages/core/session.py"
Files: ["packages/core/auth.py", "packages/core/session.py"]
→ Skip git diff, proceed to priority calculation
```

### Step 2: Calculate Review Priority On-Demand

**Applies to all modes after file discovery**:
- HIGH: Python files (`.py`) with substantive changes (>10 lines) or high match density
- MEDIUM: Test files, Python files with minor changes
- LOW: Documentation, configuration, non-code files
- Sort by lines changed (descending) or match density within each priority group

### Step 3: Load Review Guidelines and Project Context

- Read `docs/04-guides/code-review/python-code-review-checklist.md` (MANDATORY)
- Extract principle-driven review criteria for this review type

**Project Context Loading** (MANDATORY for technology-related reviews):
- IF review involves database/persistence code:
  - Read `docs/00-project/SPEC.md` Section 7 (Architecture - PostgreSQL mandated)
- IF review involves framework/library choices:
  - Read `docs/00-project/SPEC.md` Section 9 (Technology Stack)
- IF review may recommend new components:
  - Read `docs/00-project/COMPONENT_ALMANAC.md` to check for existing solutions

**Technology Recommendation Gate**:
- Any finding recommending technology changes MUST cite SPEC.md alignment
- Recommendations conflicting with SPEC.md are INVALID and must not be reported

### Step 4: Scope Confirmation Gate (Conditional)

**Trigger** (ANY condition):
- `functionality_review` discovers >5 files
- `git_diff_review` or `file_list_review` with >10 files
- Estimated review time >10 minutes

**Process**:
1. Compile scope summary with blast radius preview
2. Present to user for confirmation
3. Wait for approval or scope adjustment

**Prompt**:
```
Review scope: [N] files, ~[X] minutes

Blast radius breakdown:
- CRITICAL: [files]
- HIGH: [files]
- MEDIUM/LOW: [files]

Proceed? Reply:
- "yes" → Start review
- "focus on [files]" → Narrow scope
- "expand [pattern]" → Widen scope
```

**Skip Condition**: File count ≤5 AND mode is `file_review`/`file_list_review` (user provided explicit small scope)

---

## Phase 1.5: BLAST RADIUS ANALYSIS (~15-20s)

**Purpose**: Calculate downstream impact of each file to adjust review depth. High-impact files warrant deeper analysis.

### Why Blast Radius Matters
- `packages/core/auth.py` with 15 importers → bug affects 15+ files
- `tests/conftest.py` with 0 importers → bug affects only tests
- Reviewing both at same depth wastes time on low-impact code

### Step 1: Calculate Afferent Coupling

For each file in review scope, count how many other files import it:

```bash
# For file: packages/core/auth.py
# Module name: packages.core.auth

Grep "from packages\.core\.auth import|from packages\.core import.*auth|import packages\.core\.auth" --type py --output count
```

**Shortcut for speed**: If file count >10, only calculate for files with >100 lines (likely core modules).

### Step 2: Assess Business Criticality

Add +3 to blast radius score if file path contains:
- `auth`, `security`, `permission` (security-critical)
- `payment`, `billing`, `transaction` (financial-critical)
- `user`, `account`, `profile` (user-data-critical)
- `api/`, `handlers/`, `routes/` (user-facing)

### Step 3: Classify Files

| Afferent Count + Criticality Bonus | Classification | Review Mode |
|------------------------------------|----------------|-------------|
| 10+ | CRITICAL | `full_depth` - all findings, no limits |
| 5-9 | HIGH | `standard` - rate limits apply |
| 2-4 | MEDIUM | `focused` - Major and Critical only |
| 0-1 | LOW | `scan` - Critical only |

### Step 4: Output Blast Radius Map

```json
{
  "blast_radius_analysis": {
    "critical_files": [
      {"path": "packages/core/auth.py", "afferent": 12, "review_mode": "full_depth"}
    ],
    "high_files": [
      {"path": "packages/api/handlers.py", "afferent": 7, "review_mode": "standard"}
    ],
    "medium_files": [
      {"path": "packages/utils/helpers.py", "afferent": 3, "review_mode": "focused"}
    ],
    "low_files": [
      {"path": "tests/conftest.py", "afferent": 0, "review_mode": "scan"}
    ]
  }
}
```

### Step 5: Adjust Rate Limits by Review Mode

| Review Mode | Critical | Major | Minor | Nit |
|-------------|----------|-------|-------|-----|
| `full_depth` | unlimited | unlimited | 10 | 5 |
| `standard` | 3 | 5 | 5 | 2 |
| `focused` | 3 | 5 | 0 | 0 |
| `scan` | 3 | 0 | 0 | 0 |

### Performance Note
- Skip blast radius for single-file reviews (entry mode `file_review`)
- For `functionality_review` with <5 files, use quick heuristic (path-based criticality only)
- Full afferent calculation only for `git_diff_review` or `file_list_review` with 5+ files

---

## Phase 1.5A: PROJECT CONTEXT SYNC (~5s)

**Purpose**: Load project-specific context to calibrate review expectations.

### Step 1: Load Project Maturity Indicators

**Read** (graceful degradation if missing):
1. `docs/00-project/SPEC.md` - Extract:
   - `project_stage`: mvp | alpha | beta | ga
   - `type_safety_target`: percentage if stated
2. `docs/00-project/COMPONENT_ALMANAC.md` - Component count (codebase maturity indicator)

### Step 2: Infer Context When Missing

If SPEC.md unavailable, quick inference:
```bash
# Type hint adoption (sampling top 20 files)
Grep "def .*\) ->" --type py --output count  # typed
Grep "def .*\):" --type py --output count    # total
# Ratio: High (>0.8), Medium (0.5-0.8), Low (<0.5)
```

### Step 3: Output

```json
{
  "project_context": {
    "stage": "alpha",
    "type_safety_adoption": "medium",
    "context_source": "explicit" | "inferred" | "default"
  }
}
```

### Graceful Degradation
- ALL sources unavailable → `context_source: "default"`, standard thresholds
- Log: "Project context unavailable, using defaults"
- Do NOT halt review

---

## Phase 2: ORIENT - Context Research (~15-20s)

**Inputs**: Files from Phase 1 + Blast Radius classifications from Phase 1.5
**Purpose**: Research library patterns for each file, weighted by blast radius.

**Priority Order**: Review CRITICAL blast radius files first, then HIGH, then MEDIUM, then LOW.

### Sub-Phase 1: Extract Keywords (~5s)
1. Identify libraries/frameworks used (fastapi, pydantic, sqlalchemy, langchain, pytest)
2. Extract patterns (async/await, ORM queries, validation, testing)
3. Note architectural approaches (Clean Architecture, DI, repositories)
4. Prioritize top 3-5 libraries/patterns for validation

### Sub-Phase 2: Research Official Documentation (~10s)
1. For each library: `resolve-library-id` (e.g., "fastapi" → "/fastapi/fastapi")
2. `get-library-docs` with specific topics from discovered patterns
   - Example: `get-library-docs("/fastapi/fastapi", topic="async dependency injection")`
   - Example: `get-library-docs("/pydantic/pydantic", topic="Field validation patterns")`
3. Fallback: IF Context7 unavailable after 3 retries → WebSearch "[library] best practices [year]"

### Sub-Phase 3: Standards Conflict Detection (~5s)
1. Compare Context7 docs vs project guidelines
2. IF conflict detected → HALT with "Standards Conflict Note"
3. Document conflicting recommendations with sources
4. Escalate to orchestrator for resolution

---

## Phase 3: DECIDE - Finding Gate Application (~20-30s)

### Step 1: Apply Finding Gate (≥1 required to proceed)
1. **Invariant Violation**: Does code violate documented contract or type constraint?
2. **Intent vs Behavior Conflict**: Does implementation contradict stated purpose?
3. **Concrete Failure Path**: Can you trace specific conditions leading to failure?
4. **Unsafe Pattern Present**: Does code match known anti-pattern with anchored evidence?

### Step 2: Active Codebase Research (3-attempt limit)
```
attempt_1_broad:
  - Grep with general keyword across codebase
  - Example: "Grep 'async def' ." → Find all async functions

attempt_2_focused:
  - Glob pattern matching + targeted Grep in relevant directories
  - Example: "Glob 'packages/core/*/validation.py' + Grep 'validate'"

attempt_3_specific:
  - Read specific files identified in previous attempts
  - Example: "Read packages/core/auth/validation.py"

if_unresolved_after_3:
  - Flag as "Missing Context" with confidence <0.70
  - Move to Open Questions section (not a finding)
```

### Step 3: Context7 Validation (when confidence <0.9)
1. Validate against official library docs
2. Confidence calibration:
   - High (≥0.90): Official docs explicitly state anti-pattern
   - Medium (≥0.80): Docs imply issue through best practices
   - Low (<0.70): Docs ambiguous → Move to Open Questions
3. IF confidence <0.75 → Escalate to Perplexity for synthesis

### Step 4: Prioritization Matrix Routing
```
VALUE (What's the impact?):
  - Correctness/safety/security: High
  - User harm potential: High
  - Maintainability improvement: Medium
  - Performance gain (evidenced): Medium-High

COMPLEXITY (How hard to fix?):
  - Effort/time to fix: Low/Medium/High
  - Risk of introducing new bugs: Low/Medium/High

RISK (What could go wrong?):
  - Likelihood × Blast radius

ROUTING:
  - Should-Do: High value, low-med complexity, or low effort/high value
  - Optional/Later: Lower value, higher complexity, or exploration needed
```

### Step 5: Generate Verification Commands (≤2 per finding)
- Prefer deterministic checks: rg/grep pattern, linter command, tiny shell script
- Prefer high-level Make wrappers aggregating related checks
- Target fast execution (<5s per command)

---

## Phase 4: ACT - Output Generation (~10-15s)

### Output Order (STRUCTURE MATTERS)

1. **Open Questions & Missing Context** (Top Priority)
   - Bulleted questions with file:line + missing symbols/files/config keys
   - Only items unresolved after 3-attempt codebase research

2. **Summary Verdict** (OK / Changes Requested)
   - One concise paragraph based on git-driven analysis

3. **Review Scope**
   - Files reviewed from git diff
   - Change statistics and implementation context
   - Surfaces affected (APIs, data shapes, concurrency, external I/O)

4. **Should-Do Changes** (Matrix-Justified)
   - **Critical (≤3)**: Conf ≥0.90, deterministic verification
   - **Major (≤5)**: Conf ≥0.80, search + small harness when feasible
   - **Minor (≤5)**: Low-effort/high-value items

5. **Optional / Later** (Matrix-Justified)
   - **Nits (≤2, Optional)**: Only if value > 0, low priority
   - Lower-value/higher-complexity items with rationale

6. **Tests & Coverage** - Missing tests tied to changed behavior

7. **Security Notes** - Input/secret/logging risks with anchors

8. **Performance Notes** - Only if evidenced by change set

9. **Context7 Research Summary** - Libraries researched, validation results

### Per-Finding Format
```
* **File:line** | **Severity:** X | **Confidence:** 0.xx
  * **Problem:** ...
  * **Why (Principle):** ... [Reference guide section]
  * **Missing Context:** "None" or specifics
  * **Verification — Wrong vs Correct (≤2, best first):**
    * *Wrong signature(s):* ...
    * *Correct signature(s):* ...
    * *Quick check:* ...
  * **Fix (Minimal, in-scope):** ... (LAST BULLET)
```

---

## Timing Summary

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| OBSERVE | ~10-15s | Entry point detection, scope discovery (git/files/grep), priority calculation, load checklist |
| BLAST RADIUS | ~15-20s | Afferent coupling calculation, business criticality assessment, file classification |
| ORIENT | ~15-20s | Extract keywords, Context7 research, conflict detection |
| DECIDE | ~20-30s | Finding gates, codebase research, validation, matrix routing |
| ACT | ~10-15s | Structured output generation |
| **Total** | ~70-100s | Comprehensive code review with blast radius prioritization |

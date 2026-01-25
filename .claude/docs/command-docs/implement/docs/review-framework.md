# Multi-Agent Review Checkpoint Framework

Detailed documentation for the multi-agent review system used at implementation checkpoints.

---

## Purpose

When the orchestrator encounters a review checkpoint, it analyzes what was actually built and selects appropriate review agents using confidence-based multi-agent selection.

---

## Context Available at Review Time

- Actual files changed (not just planned files)
- Actual complexity observed during implementation
- Actual security concerns surfaced
- Actual test coverage achieved
- Actual integration points created

---

## Review Agent Selection

### Core Review Perspectives (ALWAYS - 75% collective weight)

| Agent | Weight | Focus |
|-------|--------|-------|
| code-quality | 25% | Patterns, conventions, maintainability, readability |
| architectureer | 25% | Integration quality, scalability, reliability, operational concerns |
| tech-debt-investigator | 25% | Code reuse opportunities, cleanup validation, duplication detection |

### Dynamic Review Perspectives (0-2 based on confidence >0.8 - 25% split)

| Agent | When to Include |
|-------|-----------------|
| feature-analyzer | Multiple components interact, cross-cutting concerns, system-wide integration |
| code-quality | Test-heavy implementation, complex validation scenarios, QA depth critical |
| sast-scanner | External-facing, auth/authz, sensitive data, regulatory concerns |

---

## Confidence Calculation for Dynamic Selection

```
For each potential dynamic reviewer:

confidence = (domain_fit × 0.6) + (unique_value_add × 0.3) + (efficiency × 0.1)

Include reviewer if confidence > 0.8
```

**Dimension Definitions**:

| Dimension | Question | Scoring |
|-----------|----------|---------|
| Domain fit | Does actual implementation fall in reviewer's specialty? | 0.0-1.0 |
| Unique value | Will this reviewer catch issues others won't? | 0.0-1.0 |
| Efficiency | Is additional review time justified by risk/complexity? | 0.0-1.0 |

### Worked Examples: Dynamic Agent Selection

**Example 1: Authentication Module → INCLUDE sast-scanner**

```
Component: auth.py, login_handler.py (JWT, password hashing, sessions)

sast-scanner calculation:
  domain_fit    = 0.95  (security specialty, auth is high-risk)
  unique_value  = 0.90  (catches injection/bypass others miss)
  efficiency    = 0.70  (90s scan justified by risk)
  
  confidence = (0.95×0.6) + (0.90×0.3) + (0.70×0.1) = 0.84 → INCLUDE
```

**Example 2: Validation Pipeline → INCLUDE code-quality**

```
Component: validators.py, schema_checks.py (47 rules, edge cases)

code-quality calculation:
  domain_fit    = 0.85  (validation requires thorough testing)
  unique_value  = 0.80  (catches runtime failures)
  efficiency    = 0.85  (fast tests, high confidence)
  
  confidence = (0.85×0.6) + (0.80×0.3) + (0.85×0.1) = 0.835 → INCLUDE
```

**Example 3: Simple CRUD → EXCLUDE feature-analyzer**

```
Component: preferences.py (single-table CRUD, no dependencies)

feature-analyzer calculation:
  domain_fit    = 0.40  (no multi-component interaction)
  unique_value  = 0.30  (core reviewers handle CRUD fine)
  efficiency    = 0.50  (adds time without value)
  
  confidence = (0.40×0.6) + (0.30×0.3) + (0.50×0.1) = 0.38 → EXCLUDE
```

### Scoring Guide

| Dimension | 0.9-1.0 | 0.7-0.89 | 0.5-0.69 | <0.5 |
|-----------|---------|----------|----------|------|
| domain_fit | Core specialty match | Strong relevance | Moderate relevance | Weak/no relevance |
| unique_value | Catches critical issues others miss | Adds valuable perspective | Some overlap with core | Fully redundant |
| efficiency | Fast, high confidence | Reasonable time/value | Marginal value for time | Not worth time cost |

**Decision Rule**: Include dynamic agent if confidence > 0.8; maximum 2 dynamic agents per review.

---

## Review Execution Pattern

### 1. Analyze Actual Implementation

```
# What was actually built (not planned)
files_modified = git_diff(review_group.task_range)
actual_complexity = analyze_complexity(files_modified)
security_concerns = detect_security_patterns(files_modified)
integration_points = identify_integrations(files_modified)
```

### 2. Select Review Agents

```
# Always 3 core agents
core_agents = [code-quality, architectureer, tech-debt-investigator]

# Calculate confidence for dynamic agents
dynamic_candidates = [feature-analyzer, code-quality, sast-scanner]
dynamic_agents = [a for a in dynamic_candidates if confidence(a) > 0.8]

# Cap at 2 dynamic agents
selected_dynamic = dynamic_agents[:2]
```

### 3. Launch Multi-Agent Review (Parallel)

```
# Single message with multiple Task calls
Task(code-quality, "Review {files}...")
Task(architectureer, "Review {files}...")
Task(tech-debt-investigator, "Review {files}...")
Task(selected_dynamic[0], "Review {files}...") if selected_dynamic
Task(selected_dynamic[1], "Review {files}...") if len(selected_dynamic) > 1
```

### 4. Synthesize Findings

```
# Weighted scoring
core_weight = 0.75 / 3  # 0.25 each
dynamic_weight = 0.25 / len(selected_dynamic) if selected_dynamic else 0

# Combine all findings
all_findings = combine_agent_findings(agent_outputs, weights)

# Calculate overall confidence
review_confidence = weighted_average(agent_confidences)
```

---

## Issue Categorization

### Critical Issues (MUST resolve before unblocking)

- Security vulnerabilities (auth bypass, injection, data exposure)
- Broken functionality (core features don't work, integration failures)
- Test failures (unit tests fail, integration broken, validation gaps)
- Data integrity problems (corruption risks, consistency violations)

### High-Priority Improvements (SHOULD address if time permits)

- Pattern violations (inconsistent with codebase patterns)
- Missing edge case handling (works for happy path only)
- Sub-optimal architecture (will cause maintenance burden)
- Incomplete error handling (some paths unhandled)

### Future Improvements (CAN defer to backlog)

- Performance optimizations (works but could be faster)
- Additional test coverage (basic exists, more would be better)
- Code cleanup opportunities (tech debt, refactoring candidates)
- Documentation enhancements (code works, docs could be clearer)

---

## Review Retry Loop

When critical issues are found, the orchestrator enters a focused resolution cycle.

### Iteration Flow

```
FOR iteration IN 1..3:
    1. Analyze issue types from review findings
    2. Determine fix agents by issue type
    3. Apply fixes (with iteration history context)
    4. Re-review with SAME multi-agent selection
    5. IF no critical issues → APPROVE
    6. IF still critical → Check for oscillation → Next iteration
    
IF OSCILLATION_DETECTED:
    → ESCALATE immediately as ARCHITECTURAL_CONFLICT

IF iteration == 3 AND still critical:
    → ESCALATE (block dependents, report to user)
```

---

## Iteration History (Anti-Oscillation)

**Purpose**: Prevent fix agents from repeating failed approaches or creating oscillating fixes.

### State Tracking

Each review group maintains iteration history:

```json
{
  "review_group": "RG003",
  "iteration_history": [
    {
      "iteration": 1,
      "issues_found": ["SQL injection in query_user()"],
      "issues_hash": "a1b2c3",
      "fix_attempted": "Applied parameterized queries",
      "outcome": "PARTIAL - new issue introduced",
      "new_issues": ["ORM pattern violated"]
    },
    {
      "iteration": 2,
      "issues_found": ["ORM pattern violated"],
      "issues_hash": "d4e5f6",
      "fix_attempted": "Reverted to ORM abstraction",
      "outcome": "PARTIAL - reintroduced original issue",
      "new_issues": ["SQL injection in query_user()"]
    }
  ]
}
```

### Oscillation Detection Algorithm

```
# Hash critical issues at each iteration (normalize: sort, lowercase, strip whitespace)
issue_hash(issues) = hash(sorted([normalize(i) for i in issues]))

# Detection rule
IF iteration >= 3:
    IF issue_hash(iteration_N) == issue_hash(iteration_N-2):
        → OSCILLATION_DETECTED
        → Escalate immediately with "ARCHITECTURAL_CONFLICT"
        → Do NOT exhaust remaining retries

# Similarity threshold for near-oscillation warning
IF jaccard_similarity(issues_N, issues_N-2) > 0.7:
    → NEAR_OSCILLATION_WARNING
    → Add constraint: "Avoid incremental changes; consider architectural solution"
```

### Oscillation Outcomes

| Detection | Action | Rationale |
|-----------|--------|-----------|
| OSCILLATION_DETECTED | Escalate as ARCHITECTURAL_CONFLICT | Mutually exclusive solutions indicate design issue |
| NEAR_OSCILLATION_WARNING | Add architectural constraint to fix prompt | Guide fix agent toward non-oscillating solution |
| NO_OSCILLATION | Continue normal iteration | Fixes are progressing |

### Fix Agent Prompt Enhancement

When delegating to fix agent on iteration 2+, include iteration history:

```
Previous fixes attempted:
- Iteration 1: {fix_attempted} → {outcome}
  Issues found: {issues_found}
  New issues introduced: {new_issues}
- Iteration 2: {fix_attempted} → {outcome}
  Issues found: {issues_found}
  New issues introduced: {new_issues}

CONSTRAINTS:
- Do NOT reintroduce patterns that were previously removed
- Do NOT revert changes from iteration {N-1} unless explicitly required
- If issue appears architectural (mutually exclusive solutions), return fix_status: "ARCHITECTURAL_CONFLICT"
- Consider: Are these issues fundamentally incompatible? If yes, escalate rather than oscillate
```

### Issue Type → Fix Agent

| Issue Type | Fix Approach | Agent |
|------------|--------------|-------|
| Test failures | Investigation, root cause | debugger |
| Pattern violations | Apply correct patterns | development |
| Security vulnerabilities | Security-focused fixes | development |
| Performance issues | Optimization | development |
| Integration breakage | System analysis | debugger |

### Re-Review Philosophy

**Key Principle**: Re-review uses the SAME multi-agent selection.

- Component hasn't changed type just because issues were found
- Same expert perspectives still needed
- Fresh look at whether critical issues resolved

---

## Success Criteria

A review checkpoint is APPROVED when:

1. All critical issues resolved
2. High-priority improvements addressed OR documented for follow-up
3. Future improvements captured in tech debt backlog
4. Review confidence meets threshold (weighted average of agent confidences)

---

## Escalation After 3 Iterations

If critical issues remain:

1. **Block dependent tasks** (preserve quality gates)
2. **Report critical issues** with full context:
   - What was tried
   - What failed
   - Why unresolved
3. **Document improvements** (don't lose this information)
4. **Provide guidance** for manual intervention

---

## Performance Characteristics

| Operation | Duration |
|-----------|----------|
| Initial review (3-5 agents parallel) | 1.5-2.5 min |
| Fix application per iteration | 1-3 min |
| Re-review per iteration | 1.5-2.5 min |
| Total for 3 iterations | 6-15 min |

---

## Integration with Task Validation

Review checkpoints use the same framework as `/tasks` Step 6 validation:

| Aspect | Task Validation | Review Checkpoint |
|--------|-----------------|-------------------|
| Input | Task descriptions | Actual code changes |
| Core agents | planning, architectureer, tech-debt | code-quality, architectureer, tech-debt |
| Success criteria | Planning completeness | Implementation quality |
| Blocking criteria | Planning gaps | Critical issues only |

Both apply: multiple expert perspectives, confidence-based dynamic selection, weighted synthesis, clear success criteria.

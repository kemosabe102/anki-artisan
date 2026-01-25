# Architecture Reviewer Delegation Examples

## Example 1: MVP Architecture Review

**Orchestrator Invocation**:
```markdown
Task(architecture-reviewer,
  "Review technical architecture for market-data-ingestion.
   Stage: MVP (score ≥3.5 required)
   SPEC: docs/01-planning/specifications/market-data-ingestion/SPEC.md
   Plans: docs/01-planning/specifications/market-data-ingestion/PLAN.md
   framework_visibility: explicit")
```

**Expected Execution** (~6 min):
1. Input Analysis (30s): Stage=MVP, FR_IDs: FR-001→FR-008
2. Mandatory Research (90s): 3 critical concepts via Context7
3. Traceability (60s): FR_ID mapping 8/8 = 100%
4. Quality Matrix (120s): Arch 4.0, Impl 3.5, Prod 3.0 → Overall 3.6 PASS
5. Report (60s): TECH-REV-20251121-A3F9G2, 2 P2 enhancements

---

## Example 2: Beta Review with Perplexity Research

**Orchestrator Invocation**:
```markdown
Task(architecture-reviewer,
  "Validate authentication-system architecture for Beta stage.
   Stage: Beta (score ≥3.8 required)
   SPEC: docs/01-planning/specifications/auth-system/SPEC.md
   Plans: docs/01-planning/specifications/auth-system/PLAN.md
   framework_visibility: silent")
```


**Research Phase** (240s):
- Context7: JWT library best practices (jose vs python-jwt)
- Perplexity: "OAuth2 vs JWT trade-offs for microservices"
- Perplexity: "Rate limiting strategies for auth endpoints"

**Output**: Overall 4.1/5.0 PASS Beta, 1 P1 blocker (FR-018 missing)

---

## Example 3: Stage Gate Validation Only

**Orchestrator Invocation**:
```markdown
Task(architecture-reviewer,
  "Quick stage gate check - does event-analytics meet GA requirements?
   Stage: GA (score ≥4.2 required)
   Plans: docs/01-planning/specifications/event-analytics/PLAN.md")
```

**Expected Output**: FAIL - Score 3.9 < 4.2, missing 99.9% availability design

---

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `plans` | Yes | Path(s) to PLAN.md files |
| `spec` | Recommended | Path to SPEC.md for traceability |
| `stage` | Yes | MVP, Alpha, Beta, or GA |
| `framework_visibility` | No | `explicit` (default) or `silent` |

---

## Output Schema Reference

**Technical Review Report** (`TECH-REV-*`):
- `overall_score`: 0.0-5.0
- `rubric`: 8 criteria with scores and evidence
- `traceability`: coverage_pct, missing_links
- `anti_patterns`: detected issues
- `recommendations`: top 5 actions

**Technical Edit Plan** (`TECH-EDIT-*`):
- `patches`: unified diff format
- `replacements`: pattern → replacement
- `unresolved_items`: needs human decision
- `priority`: P1/P2/P3

# Tech-Debt-Investigator: Orchestrator Integration Guide

> How to effectively invoke and integrate tech-debt-investigator in multi-agent workflows.

---

## When to Invoke

| Invoke After | Invoke Before |
|--------------|---------------|
| Security review (SAST scan) | Sprint planning |
| Architecture review | Team capacity allocation |
| Linting / formatting | Release decisions |
| Code review (python-code-reviewer) | Quality gate decisions |

**Typical Pipeline Position**:
```
security-review → architecture-review → python-code-reviewer → tech-debt-investigator → sprint-planning
```

---

## What to Provide in business_context

| Field | Type | Effect on Analysis |
|-------|------|-------------------|
| `critical_modules` | `string[]` | 1.5x impact multiplier for findings in these paths |
| `usage_frequency` | `Record<string, "high"\|"medium"\|"low">` | +2/+1/+0 impact adjustment |
| `team_ownership` | `Record<string, string>` | Ownership dispersion flagging |
| `incident_files` | `string[]` | Auto-P0 priority, incident correlation |

**Example Input**:
```json
{
  "business_context": {
    "critical_modules": ["packages/core/auth.py", "packages/core/payments.py"],
    "usage_frequency": {
      "packages/api/": "high",
      "packages/utils/": "low"
    },
    "team_ownership": {
      "packages/core/": "platform-team",
      "packages/api/": "api-team"
    },
    "incident_files": ["packages/core/session.py"]
  }
}
```

---

## How to Interpret Hotspot Scores

| Score | Severity | Action |
|-------|----------|--------|
| >7.0 | **Urgent** | Block sprint start if not addressed |
| 5.0-7.0 | High | Address in current sprint if capacity |
| 3.0-5.0 | Medium | Plan for next sprint |
| <3.0 | Low | Monitor, address opportunistically |

---

## Merging with Other Reviewers

| If Other Reviewer Says... | Adjust tech-debt-investigator Output |
|---------------------------|--------------------------------------|
| Security review flags file X vulnerable | +2 to impact_score for X |
| Architecture review rejects design in module Y | Defer remediation recommendations for Y |
| Performance test shows slowdown in Z | Increase hotspot urgency for Z |
| Code reviewer flags maintainability issue | Correlate with duplication/complexity scores |

---

## Iteration Pattern

**For trend analysis (iterative mode)**:
1. First run: No baseline → establishes baseline
2. Subsequent runs: Pass previous `debt_score` as baseline
3. Agent calculates deltas and flags regressions

**Feedback Loop**:
```
Sprint N complete → Run tech-debt-investigator → Compare to Sprint N-1 baseline
  ↓
Regression detected? → Investigate recent commits → Adjust Sprint N+1 priorities
```

---

## Delegation Example

```markdown
Task(tech-debt-investigator,
  "Analyze technical debt in packages/core/.
   business_context: {
     critical_modules: ['packages/core/auth.py'],
     incident_files: ['packages/core/session.py']
   }
   baseline: { debt_score: 72, tdr_ratio: 0.08 }
   Output: Full analysis with trend comparison.
   BOUNDARIES: Read-only analysis, no code modifications.")
```

---

## Related Documentation

- [Phase 2: ORIENT](../phases/phase-2-orient.md) - Business context integration details
- [Phase 3: DECIDE](../phases/phase-3-decide.md) - Conflict resolution logic
- [Phase 4: ACT](../phases/phase-4-act.md) - Trend confidence thresholds
- [Frameworks](frameworks.md) - SQALE/SIG methodology reference

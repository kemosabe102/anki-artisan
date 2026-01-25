# Delegation Examples for Doc Librarian

**Purpose**: How orchestrator invokes this agent

---

## Pre-PR Health Check

```markdown
Objective: Check documentation health before PR merge
Output Format: JSON health report with score and violations
Tool Guidance: Use Tier 1 (read-only) for pre-commit checks
Boundaries: Focus on critical violations only (broken links, major misplacements)
```

**Expected Output**:
```json
{
  "status": "SUCCESS",
  "agent": "doc-librarian",
  "summary": "Health score: 92/100. 3 broken links, 2 naming violations.",
  "confidence": 0.95,
  "agent_specific_output": {
    "health_report": {
      "health_score": 92,
      "coverage_percentage": 98,
      "link_health": { "total_links": 250, "broken_links": 3 },
      "organization_compliance": { "total_files": 145, "misplaced_files": 2 },
      "naming_compliance": { "total_files": 145, "violations": 2 }
    },
    "recommendations": [
      { "priority": "high", "category": "links", "action": "Fix 3 broken internal links", "estimated_effort": "15min" }
    ]
  }
}
```

---

## Fix Broken Links

```markdown
Objective: Fix all broken internal links in docs/
Output Format: JSON with fixes applied and verification status
Tool Guidance: Use Tier 2 (automated fixes with verification)
Boundaries: Internal links only, no external URL fixes
```

---

## Organization Audit

```markdown
Objective: Audit docs/ organization against DOCS-MANAGEMENT.md
Output Format: JSON with violations and move recommendations
Tool Guidance: Use Tier 1 (read-only analysis)
Boundaries: Generate plan only, do not move files
```

---

## Git Command Integration

Pattern for `/git doc-check`:

1. Orchestrator delegates: "Check health of modified docs files"
2. If `health_score < 90`: Report violations to user
3. If critical violations: Block commit with fix recommendations
4. If warnings only: Proceed with commit, log recommendations

---

## Multi-Agent Workflow

**Upstream Dependencies**:
- `git-github` → Provides modified file list for incremental checks
- `/spec command` → Triggers link validation after spec generation

**Downstream Integration**:
- `claude-code` → Receives `.claude/docs/` organization recommendations
- `git-github` → Receives file modification list for commit

---

## Sample FAILURE Response

```json
{
  "status": "FAILURE",
  "agent": "doc-librarian",
  "summary": "Link fix failed: 5 of 10 links corrected, 5 require manual intervention.",
  "confidence": 0.8,
  "failure_details": {
    "failure_type": "partial_completion",
    "reasons": [
      "Cannot determine correct path for 3 orphaned files",
      "2 files exceed Edit tool size limit"
    ],
    "partial_results": {
      "fixes_applied": 5,
      "fixes_failed": 5
    },
    "recovery_suggestions": [
      { "approach": "Manual review for orphaned files", "requires_coordination": false }
    ],
    "next_steps": "escalate_to_orchestrator"
  }
}
```

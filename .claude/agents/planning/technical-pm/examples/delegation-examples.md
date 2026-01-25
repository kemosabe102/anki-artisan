# Delegation Examples

How the orchestrator delegates to technical-pm with proper context.

---

## Example 1: Full Business Review

**User Request**: "Review the data pipeline spec for business alignment"

**Orchestrator Delegation**:
```
Task(technical-pm,
  "Review docs/01-planning/specifications/012-data-pipeline/SPEC.md for business alignment.
   Analyze all plan files in the specification directory.
   Produce Business Review Report with alignment scores, NFR assessment, and traceability analysis.
   Generate Business Edit Plan for enhancement agents.")
```

**Expected Behavior**:
1. Glob `docs/01-planning/specifications/012-data-pipeline/**/*.md`
2. Read SPEC.md, PLAN.md, and all component plans
3. Calculate business_goals_alignment_score
4. Assess NFR coverage across 4 categories
5. Map FR-IDs and calculate traceability %
6. Census placeholders by priority
7. Generate schema-compliant report

---

## Example 2: Focused NFR Assessment

**User Request**: "Check if the auth system spec has adequate security requirements"

**Orchestrator Delegation**:
```
Task(technical-pm,
  "Perform NFR-focused review of docs/01-planning/specifications/008-auth-system/SPEC.md.
   Priority: security requirements coverage.
   Assess authentication, authorization, and data protection specifications.
   Flag gaps and recommend enhancements.")
```

**Expected Behavior**:
1. Focus on NFR assessment dimension
2. Deep-dive security requirements (auth, authz, data protection)
3. Cross-reference with compliance requirements
4. Score coverage as low/medium/high
5. Generate targeted recommendations

---

## Example 3: Pre-Implementation Validation

**User Request**: "Is the payment integration plan ready for architecture review?"

**Orchestrator Delegation**:
```
Task(technical-pm,
  "Validate business readiness of docs/01-planning/specifications/015-payment-integration/.
   Check: business context completeness, requirements traceability, placeholder resolution.
   Determine if ready for handoff to architecture-review agent.
   Include handoff_package assessment in output.")
```

**Expected Behavior**:
1. Full review with handoff focus
2. Assess architecture_handoff_ready criteria
3. Verify business_context_preserved
4. Check investigation_agenda_complete
5. Return handoff_notes with blockers (if any)

---

## Example 4: Budget Compliance Check

**User Request**: "Will this feature stay within our $100/month budget?"

**Orchestrator Delegation**:
```
Task(technical-pm,
  "Review docs/01-planning/specifications/020-monitoring-system/SPEC.md for cost compliance.
   Validate against $100/month operational budget constraint.
   Apply cost-analysis-framework.md methodology.
   Identify cost optimization opportunities.")
```

**Expected Behavior**:
1. Extract all cost estimates from plans
2. Sum projected monthly operational costs
3. Compare against $100/month constraint
4. Identify >$50/month items requiring ROI justification
5. Recommend free tier maximization opportunities

---

## Input Schema Reference

**Required Fields**:
```json
{
  "input": {
    "context": "Primary instruction - what to review and focus areas",
    "execution_timestamp": "2024-01-15T10:30:00Z",
    "existing_plans": ["path/to/PLAN.md", "path/to/component-plan.md"],
    "operation_type": "plan_file_enhancement|business_analysis|nfr_analysis|investigation_guidance"
  }
}
```

**Optional Context**:
```json
{
  "business_context": {
    "business_goals": ["Goal 1", "Goal 2"],
    "user_value_proposition": "Core value statement",
    "success_metrics": ["Metric 1", "Metric 2"],
    "constraints": ["$100/month budget", "MVP scope"]
  },
  "requirements": {
    "nfr_analysis_required": true,
    "business_context_preservation": true,
    "investigation_agenda_needed": false,
    "architecture_handoff_required": true
  }
}
```

---

## Anti-Patterns (What NOT to Delegate)

**Wrong**: "Update the SPEC.md with better business context"
- technical-pm does NOT modify files

**Wrong**: "Design the architecture for this feature"
- Use architecture-review instead

**Wrong**: "Implement the payment integration"
- Use python-code-implementer instead

**Wrong**: "Fix the code quality issues"
- Use python-code-reviewer or debugger instead

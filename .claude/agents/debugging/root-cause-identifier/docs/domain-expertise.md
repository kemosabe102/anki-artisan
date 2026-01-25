# Domain Expertise: Root Cause Analysis Methodology

Detailed workflow phases, framework applications, and validation protocols for root-cause-identifier.

---

## Analyze Root Cause Workflow

### Phase 1: Analysis

- Parse problem statement for observable symptoms
- Identify the specific failure point or issue
- Extract timeline if available (when did this start, what changed)
- Catalog available evidence (logs, code, patterns, metrics)
- Assess evidence quality (strong/moderate/weak)

### Phase 2: Research

- Read relevant code files mentioned in problem context
- Grep for error patterns, similar issues, related failures
- Identify affected components and their dependencies
- Look for recent changes that correlate with problem timeline
- Search for previous occurrences of similar symptoms

### Phase 3: 5 Whys Execution

**Level-by-Level Drilling:**

```
Level 1: Why did [symptom] occur?
  → Answer with evidence
  → Confidence score based on evidence strength

Level 2: Why did [Level 1 answer] happen?
  → Answer with evidence
  → Confidence score

Level 3: Why did [Level 2 answer] happen?
  → Answer with evidence
  → Confidence score

Level 4: Why did [Level 3 answer] happen?
  → Answer with evidence
  → Confidence score

Level 5: Why did [Level 4 answer] happen?
  → This is typically the root cause
  → Validate: Is it actionable? Is it non-circular?
```


**Early Termination (fewer than 5 levels):**
- Stop if root cause is clearly actionable before level 5
- Document why drilling stopped early
- Minimum 3 levels required for valid analysis

**Branching (multiple answers at one level):**
- If multiple valid answers exist, follow the most evidenced path
- Document alternatives as "alternative_root_causes_considered"
- May need to analyze multiple branches for complex issues

### Phase 4: Root Cause Validation

**Actionable Check:**
- Can this root cause be directly addressed?
- Is there a clear owner/team who can fix this?
- Are resources available to address it?

**Circular Check:**
- Trace forward: If we fix the root cause, trace through the chain
- Does fixing the root cause prevent all intermediate causes?
- Does the chain NOT loop back to the original symptom?

**Category Assignment:**
- process: Workflow, procedure, or policy issue
- technical: Code, infrastructure, or system issue
- human: Training, communication, or expertise issue
- external: Third-party, vendor, or external dependency issue
- design: Architecture or design decision issue
- resource: Capacity, staffing, or budget issue

### Phase 5: SCAMPER Recommendations

**Apply each lens systematically:**

1. **Substitute**: What components, processes, or tools could be replaced?
2. **Combine**: What steps or systems could be merged?
3. **Adapt**: What solutions from elsewhere could be applied?
4. **Modify**: What could be scaled, changed in frequency, or adjusted?
5. **Put to other use**: What existing tools/patterns could help?
6. **Eliminate**: What unnecessary complexity could be removed?
7. **Reverse/Rearrange**: What order or flow could be changed?

**Selection criteria for final 2-5 recommendations:**
- Directly addresses root cause
- Prevents recurrence (not just symptom treatment)
- Feasible with available resources
- Impact justifies effort


### Phase 6: Validation & Reflection

- Verify 5 Whys chain is complete with evidence at each level
- Confirm root cause passes actionable and circular checks
- Validate 2-5 recommendations generated
- Each recommendation has effort/impact estimates
- Check confidence scores are justified by evidence quality

---

## Evidence Types and Quality

| Type | Strong Evidence | Weak Evidence |
|------|-----------------|---------------|
| log | Exact error message with timestamp | General log mentioning area |
| code | Specific line causing issue | File in affected area |
| pattern | Reproducible failure pattern | Single occurrence |
| testimony | Multiple consistent accounts | Single unclear report |
| metric | Clear correlation in data | Suggestive but not conclusive |
| documentation | Explicit design decision | Implied from context |

**Evidence Quality Scoring:**
- **Strong**: 2+ types of evidence, high correlation, reproducible
- **Moderate**: 1-2 types, reasonable correlation, partially reproducible
- **Weak**: Inference-based, circumstantial, not reproducible

---

## Common Root Cause Categories

### Process Issues
- Missing validation steps
- Unclear handoff procedures
- Inadequate review processes
- Poor change management

### Technical Issues
- Race conditions
- Resource exhaustion
- Configuration drift
- Missing error handling

### Human Issues
- Knowledge gaps
- Communication failures
- Cognitive overload
- Unclear responsibilities

### External Issues
- Third-party API changes
- Dependency vulnerabilities
- Network instability
- Vendor limitations

---

## Validation Protocol

| Check | Requirement |
|-------|-------------|
| Schema Compliance | All outputs validate against root-cause-identifier.schema.json |
| 5 Whys Depth | Minimum 3 levels, typically 5 levels with evidence |
| Root Cause Quality | Actionable AND non-circular |
| Recommendations | 2-5 SCAMPER-derived with effort/impact estimates |
| Confidence Justified | Score reflects evidence quality |

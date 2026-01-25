# Plan Enhancer Workflow Phases

Detailed 4-phase OODA workflow for business context enhancement.

## Phase 1: OBSERVE - Pre-Processing (~10-15s)

**Steps**:
1. Validate inputs: Use Read tool to verify both plan and SPEC files exist
2. Read COMPONENT_ALMANAC.md to identify existing components for reuse
3. Read SPEC content: Extract business goals, user needs, functional requirements, success metrics
4. Read existing plan: Scan entire plan file structure
5. Generate enhancement checklist:
   - Identify ALL placeholders: `[.*]`, `[Component.*]`, `[Business.*]`, `[Success.*]`, `[Value.*]`
   - Create explicit checklist of every business section needing content
   - Map placeholders to specific component details from plan_metadata
   - Record baseline count of placeholders to replace
6. Identify code reuse opportunities using `code-reuse-framework.md`

## Phase 2: ORIENT - Framework Integration (~15-20s)

**Steps**:
7. Extract business context: Parse SPEC for strategic value, business goals, success criteria
8. Apply framework integration:

**Cost-Conscious Planning** (`cost-analysis-framework.md`):
- Include business justification for costs >$50/month with ROI timeline
- Map business value to cost optimization strategies
- Align business goals with $100/month budget constraints

**Risk-Aware Context** (`risk-assessment-matrix.md`):
- Include business risk mitigation in success criteria using P×I×E framework
- Map business goals to risk management strategies with quantified scores

**Quality-Driven Enhancement** (`quality-scoring-algorithms.md`):
- Apply pain point alignment scoring to validate business goal effectiveness
- Ensure business success criteria are measurable using quality algorithms

9. Process checklist items systematically

## Phase 3: DECIDE - Content Replacement Strategy (~5-10s)

### Placeholder Patterns to Replace

| Pattern | Replace With |
|---------|--------------|
| `[Component1]`, `[Component2]` | Actual component names from plan_metadata.name |
| `[Business Goal 1]`, `[Business Goal 2]` | Specific goals from SPEC.md |
| `[Success Metric 1]`, `[Success Metric 2]` | Specific success criteria from SPEC.md |
| `[Value Proposition 1]` | Specific user value statements + reuse benefits |
| `[FR-XXX]`, `[Requirement 1]` | Actual FR-IDs and descriptions |
| `[X Sprint Points]` | Actual sprint points from component_details |

### Content Replacement Rules
1. Never leave generic placeholders—all business content must be specific
2. Use SPEC.md as source of truth—all business content derives from specification
3. Maintain component specificity—use exact component names from spec-reviewer output
4. Preserve FR-ID traceability—map to actual functional requirement identifiers
5. Create measurable metrics—success criteria must be specific and measurable
6. Technical placeholders preserved—leave architecture/implementation sections as-is

## Phase 4: ACT - Systematic Population (~20-30s)

**Steps**:
10. Replace placeholders with specific content (see patterns above)
11. Map requirements: Create complete traceability between FRs and business value
12. Populate code reuse business value:
    - Add "Technical Debt Reduction Value" to success metrics when replacing code
    - Include "Existing Component Reuse" in user value propositions
    - Document "Maintenance Burden Reduction" from code consolidation
13. Populate business sections using Desktop Commander (`mcp__desktop-commander__edit_block`)
14. Generate preliminary cleanup task list for components being replaced
15. Self-validate completion:
    - Re-scan plan file for remaining business section placeholders
    - Verify all component names are actual names, not generic placeholders
    - Confirm all requirements mapped to specific FR-IDs
    - Validate business metrics are measurable and specific
16. Generate completion evidence

**Expected Duration**: 50-75 seconds for comprehensive plan enhancement with validation

## Progressive Disclosure Application

### Before (Placeholder)
```markdown
## Business Goals
[Business Goals Placeholder]
```

### After (Progressive Disclosure)
```markdown
## Business Goals (Essential - Always Visible)

**Primary Objective**: Reduce customer onboarding time by 40% (from 10 days to 6 days)

**Success Metrics**:
- Customer satisfaction score >4.5/5.0 (current: 3.8/5.0)
- Onboarding completion rate >85% (current: 68%)
- Support ticket reduction: 30% fewer onboarding-related tickets

**Value Proposition**:
- Cost savings: $500K annually (reduced support overhead)
- Revenue impact: 15% increase in customer activation rate

**Detailed Analysis**: See `docs/05-reference/[feature]-business-case.md`
```

## Validation Checklist

### SUCCESS Criteria
- [ ] Plan file successfully read and enhancement checklist generated
- [ ] SPEC.md content successfully extracted with specific business details
- [ ] ALL business section placeholders identified and replaced with actual content
- [ ] NO business placeholders remaining (validated count = 0)
- [ ] Requirements mapped to specific FR-IDs with business value
- [ ] Component names are actual names, not generic placeholders
- [ ] Business metrics are specific and measurable from SPEC.md
- [ ] Technical sections preserved as placeholders for architecture-enhancer
- [ ] Progressive disclosure applied (essential visible, details externalized if >500 lines)

### FAILURE Criteria
- Plan file not found or not readable
- SPEC.md file missing or cannot be parsed
- Enhancement checklist generation fails
- File modification operations fail
- Business section placeholders remain after processing
- Self-validation detects remaining business placeholders

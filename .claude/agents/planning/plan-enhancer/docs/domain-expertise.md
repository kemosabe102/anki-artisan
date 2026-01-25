# Domain Expertise: Plan Enhancement

Detailed methodology for extracting business context from SPEC.md to populate PLAN.md business sections.

---

## Purpose and Scope

### What Plan Enhancement Does
- Extracts business context, goals, and metrics from SPEC.md
- Populates business placeholders in existing PLAN.md files
- Maps functional requirements (FR-IDs) to business value
- Identifies component reuse opportunities from COMPONENT_ALMANAC.md
- Ensures traceability between specifications and implementation plans

### What Plan Enhancement Does NOT Do
- Create new files (enhancement-only)
- Modify technical/architecture sections (architecture-enhancer domain)
- Generate specifications (/spec command domain)
- Make technology decisions (technical placeholders preserved)

---

## Business Placeholder Patterns

### Common Placeholders to Identify and Replace

| Pattern | Source | Replace With |
|---------|--------|--------------|
| `[Business Goal 1]` | SPEC.md Goals section | Specific goal statement with measurable outcome |
| `[Component Name]` | COMPONENT_ALMANAC.md | Actual component name with business purpose |
| `[TODO: Business Context]` | SPEC.md Business Context | Strategic alignment and value proposition |
| `[Success Metric N]` | SPEC.md Success Criteria | Specific KPI with target value |
| `[FR-XXX Description]` | SPEC.md Requirements | Full requirement text with business rationale |
| `[ROI Statement]` | SPEC.md Business Case | Quantified return with timeline |
| `[Stakeholder Value]` | SPEC.md Stakeholders | Concrete benefits per stakeholder group |
| `[Risk-XXX]` | SPEC.md Risk Matrix | Risk description with business impact |

### Content Replacement Rules

1. **SPEC.md is Source of Truth**: All business content must trace to SPEC.md
2. **No Fabrication**: Never invent metrics, goals, or values not in source
3. **Specific Over Generic**: Replace `[Goal 1]` with actual goal text
4. **Measurable Metrics**: Success criteria must have quantifiable targets
5. **Technical Preservation**: Never modify `[Architecture:*]` or `[Technology:*]` placeholders

---

## SPEC.md to PLAN.md Mapping Techniques

### Section Mapping Matrix

| SPEC.md Section | Maps To PLAN.md Section | Extraction Focus |
|-----------------|-------------------------|------------------|
| Business Context | Business Context & Strategic Alignment | Problem statement, market need |
| Goals & Objectives | Success Criteria, Component Goals | Measurable outcomes |
| Functional Requirements | Requirements Traceability | FR-ID to component mapping |
| Non-Functional Requirements | Quality Attributes | Performance, security targets |
| Success Criteria | Validation Metrics | KPIs with thresholds |
| Stakeholders | Stakeholder Value Matrix | Benefits per role |
| Risk Assessment | Risk Mitigation Summary | Business impact focus |
| Cost Analysis | Budget & Resource Allocation | Investment justification |

### FR-ID Mapping Process

1. **Extract FR-IDs**: Scan SPEC.md for `FR-XXX` patterns
2. **Group by Component**: Map requirements to planned components
3. **Business Value Annotation**: Add business rationale per FR
4. **Priority Alignment**: Ensure priority matches business impact

**Example Mapping**:
```markdown
| FR-ID | Requirement | Component | Business Value |
|-------|-------------|-----------|----------------|
| FR-001 | User authentication | auth-service | Secure access, compliance |
| FR-002 | Data export | reports-module | Stakeholder reporting needs |
```

### Business Context Extraction Patterns

**From SPEC.md Problem Statement**:
- Pain points → Plan's "Why" section
- Current state → Baseline metrics
- Desired state → Success criteria targets

**From SPEC.md Goals**:
- Primary goal → Plan's strategic objective
- Secondary goals → Component-level objectives
- Constraints → Plan's scope boundaries

---

## Component Reuse Analysis Approach

### COMPONENT_ALMANAC.md Integration

1. **Load Almanac First**: Before populating component sections
2. **Match by Capability**: Compare planned features to existing components
3. **Reuse Classification**:
   - **Direct Reuse**: Component meets requirements as-is
   - **Extend**: Component needs enhancement (prefer over create)
   - **Replace**: Component fundamentally incompatible (justify thoroughly)
   - **Create New**: No existing component matches (last resort)

### Business Value of Reuse

| Reuse Type | Development Savings | Risk Reduction | Business Value Statement |
|------------|---------------------|----------------|--------------------------|
| Direct Reuse | 80-100% | High | "Leverages proven {component}, reducing time-to-market by X weeks" |
| Extend | 40-60% | Medium | "Builds on {component} foundation, adding {capability} with Y% effort savings" |
| Replace | 0% | Low | "New implementation required due to {incompatibility}, enables {business benefit}" |
| Create New | 0% | Variable | "Novel capability addresses {unmet need}, no existing solution" |

### Reuse Decision Framework

```
IF component exists in Almanac matching >70% requirements THEN
  → Prefer Direct Reuse or Extend
  → Document business justification in plan
ELSE IF component exists with 40-70% match THEN
  → Evaluate Extend vs Create trade-offs
  → Include effort comparison in plan
ELSE
  → Create New with full business justification
  → Flag for future Almanac addition
```

---

## Quality Metrics for Plan Enhancement

### Placeholder Elimination Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Business Placeholder Count | 0 | `Grep('[Business|Goal|TODO.*context]')` after enhancement |
| FR-ID Coverage | 100% | All SPEC FR-IDs appear in plan with business mapping |
| Metric Specificity | 100% | No generic "improve X" without quantified target |
| Source Traceability | 100% | Every business claim cites SPEC.md section |

### Confidence Scoring

| Confidence Level | Score Range | Action |
|------------------|-------------|--------|
| High | 0.85-1.0 | Populate directly, cite source |
| Medium | 0.7-0.84 | Populate with "[REVIEW]" flag |
| Low | <0.7 | Mark "[UNVERIFIED]", request clarification |
| Missing | N/A | Return FAILURE, identify SPEC.md gap |

### Self-Validation Checklist

Before reporting success:
- [ ] Zero business placeholders remain (`Grep` verification)
- [ ] All FR-IDs from SPEC.md mapped to components
- [ ] Success metrics have quantified targets
- [ ] Business context traces to SPEC.md (citations present)
- [ ] Component reuse opportunities documented
- [ ] No technical sections modified (architecture-enhancer domain)

---

## Common Pitfalls and Prevention

### Pitfall 1: Generic Placeholder Replacement
**Problem**: Replacing `[Goal 1]` with `[Primary Business Goal]`
**Prevention**: Extract exact goal text from SPEC.md, include measurable outcome
**Example Fix**: `[Goal 1]` → "Reduce manual data entry by 60% within 6 months"

### Pitfall 2: Fabricated Metrics
**Problem**: Inventing success criteria not in SPEC.md
**Prevention**: Only use metrics explicitly stated in SPEC.md; mark gaps as "[SPEC GAP: metric needed]"
**Recovery**: Return partial success, flag missing metrics for /spec command

### Pitfall 3: Technical Section Modification
**Problem**: Populating `[Architecture: TBD]` with technical decisions
**Prevention**: Only touch business placeholders; leave technical for architecture-enhancer
**Detection**: Pre-scan for technical patterns, exclude from work list

### Pitfall 4: Missing FR-ID Traceability
**Problem**: Components listed without FR-ID mapping
**Prevention**: Extract ALL FR-IDs from SPEC.md first, ensure each maps to component
**Validation**: Count FR-IDs in SPEC vs plan; must match

### Pitfall 5: Ignoring COMPONENT_ALMANAC.md
**Problem**: Proposing new components when reusable ones exist
**Prevention**: Always load Almanac in ORIENT phase before populating components
**Business Impact**: Missing reuse = inflated cost estimates, credibility loss

### Pitfall 6: Incomplete Confidence Reporting
**Problem**: Claiming 100% success without validation evidence
**Prevention**: Generate JSON evidence with before/after counts, confidence scores
**Output Format**:
```json
{
  "status": "SUCCESS",
  "placeholders_before": 15,
  "placeholders_after": 0,
  "fr_coverage": "100%",
  "confidence": 0.92,
  "sources_cited": ["SPEC.md:L45-67", "SPEC.md:L120-135"]
}
```

---

## Operation Phases (Detailed)

### Phase 1: Context Loading (OBSERVE)
1. `Read(plan_path)` - Verify file exists, load structure
2. `Grep('\\[.*\\]', plan_path)` - Identify ALL placeholders
3. `Read('docs/00-project/SPEC.md')` - Load business context source
4. `Read('docs/00-project/COMPONENT_ALMANAC.md')` - Load reuse opportunities
5. Record baseline placeholder count

### Phase 2: Mapping Analysis (ORIENT)
1. Classify placeholders: business vs technical
2. Map business placeholders to SPEC.md sections
3. Identify reuse opportunities from Almanac
4. Flag gaps: placeholders without SPEC.md source
5. Calculate initial confidence score

### Phase 3: Enhancement Strategy (DECIDE)
1. Prioritize: goals > metrics > FR-mappings > context
2. Determine replacement order (dependencies first)
3. Plan chunk sizes for edit_block calls (<=30 lines)
4. Flag ambiguous items for user clarification if confidence < 0.7

### Phase 4: Systematic Population (ACT)
1. Replace placeholders using `mcp__desktop-commander__edit_block()`
2. Process in priority order, one section at a time
3. Preserve technical placeholders unchanged
4. Add source citations for traceability

### Phase 5: Validation
1. `Grep('\\[Business|Component|TODO\\]', plan_path)` - Must return 0
2. Verify FR-ID coverage matches SPEC.md
3. Confirm technical sections unchanged
4. Generate completion evidence (JSON)
5. Report confidence score with source citations

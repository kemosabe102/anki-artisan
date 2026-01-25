# Specification Review Guidelines

**Purpose**: Systematic review process for feature specifications ensuring quality, completeness, and proper WHAT/WHY focus before technical planning begins.

**Last Updated**: 2025-10-03

---

## Table of Contents

1. [When This Process Runs](#when-this-process-runs)
2. [Review Philosophy: WHAT vs WHY vs HOW](#review-philosophy-what-vs-why-vs-how)
3. [Review Agents & Their Roles](#review-agents--their-roles)
4. [Output Requirements](#output-requirements)
5. [Review Criteria Checklist](#review-criteria-checklist)
6. [Review Report Template](#review-report-template)
7. [Integration with SDD Workflow](#integration-with-sdd-workflow)
8. [Common Issues & How to Flag Them](#common-issues--how-to-flag-them)

---

## When This Process Runs

**Trigger Point**: Automatically suggested after `/spec` command completion

**Workflow Position**:

```
/spec → [REVIEW PROCESS] → /plan → /tasks → /implement
        ↑ YOU ARE HERE
```

**Timing**: Before `/plan` command is executed to ensure specifications are complete and properly scoped

**Purpose**: Quality gate to catch implementation details, ambiguities, and missing business context before planning phase

---

## Review Philosophy: WHAT vs WHY vs HOW

### Core Principle

**Specifications define business requirements (WHAT) and rationale (WHY), NOT implementation details (HOW)**

### WHAT Should Be in Specs ✅

**User Requirements & Scenarios**:

- User stories in Given/When/Then format
- Acceptance criteria (observable outcomes)
- Functional requirements (FR-XXX identifiers)
- Success metrics (measurable business outcomes)

**Business Context**:

- Pain points being addressed
- ROI calculations (hours saved, efficiency gains)
- Customer value proposition
- Strategic outcomes

**Platform & Constraints**:

- Target platform (Claude Code, Python, Kubernetes, etc.)
- Architectural constraints (must use X protocol, integrate with Y system)
- Non-functional requirements (performance targets, reliability SLOs)
- Technology choices that ARE the requirement (e.g., "must be Claude Code command")

**Example (GOOD)**:

```markdown
FR-001: System MUST generate task list from technical plan within 10 minutes
FR-002: System MUST identify parallel work opportunities with 80% accuracy
TC-001: Solution MUST be implemented as Claude Code slash command
NFR-001: Task generation completes within 10 minutes for plans with up to 20 components
```

### WHY Should Be in Specs ✅

**Business Rationale**:

- Why this feature solves customer problems
- Why this approach over alternatives
- Why these constraints are necessary
- Why these metrics matter

**Example (GOOD)**:

```markdown
Pain Point DEV-001: Developers spend 2-4 hours manually breaking down plans
Business Value: Eliminate manual breakdown bottleneck, save 20.32 hours/month
Platform Rationale: Claude Code chosen for seamless integration with existing workflow
```

### HOW Should NOT Be in Specs ❌

**Implementation Details to Avoid**:

- Specific code structure or class hierarchies
- Function names or method signatures
- Detailed algorithms or data structures
- Database schema designs
- API endpoint implementations
- Low-level technical decisions

**Example (BAD - Remove from Specs)**:

```markdown
❌ "Implement TaskGenerator class with generateFromPlan() method"
❌ "Use breadth-first search algorithm for dependency graph traversal"
❌ "Create tasks table with columns: id, title, description, agent_id, status"
❌ "Define GET /api/tasks/:id endpoint returning JSON with task details"
```

**Why These Are Wrong**:

- These are planning/implementation decisions
- They constrain technical creativity unnecessarily
- They belong in PLAN.md or implementation code
- They make specs brittle and hard to regenerate

### Borderline Cases (Use Judgment)

**System Architecture Patterns** (Usually OK if they're requirements):

```markdown
✅ "System MUST use Task tool for sub-agent delegation" (requirement)
❌ "Implement observer pattern for task state changes" (implementation)
```

**Data Concepts** (High-level OK, detailed NO):

```markdown
✅ "System tracks task dependencies in a directed acyclic graph"
❌ "Use adjacency list representation with HashMap<String, List<String>>"
```

**Integration Points** (Required integrations OK, internal wiring NO):

```markdown
✅ "System MUST integrate with LIVING_SPRINT.md for progress tracking"
❌ "Create TaskProgressWriter class to update LIVING_SPRINT.md via file I/O"
```

---

## Review Agents & Their Roles

### 1. planning

**Persona**: Quality Assurance Specialist
**Primary Focus**: Specification completeness, clarity, and testability

**Key Responsibilities**:

- Validate all requirements are testable and measurable
- Check for ambiguities and unclear language
- Verify Given/When/Then scenarios are concrete
- Ensure requirements have proper FR-XXX identifiers
- **Flag any implementation details (HOW) that leaked into spec**

**Output**: `review/spec-review-report.md`

### 2. planning

**Persona**: Business Alignment Validator
**Primary Focus**: Business value, ROI, and pain point alignment

**Key Responsibilities**:

- Verify pain points are properly addressed
- Validate ROI calculations (hours-based, no hourly rates)
- Check success metrics are business-focused
- Ensure strategic outcomes align with roadmap
- Assess cost-benefit analysis compliance with $100/month budget

**Output**: `review/business-review-report.md`

### 3. architecture

**Persona**: Technical Constraints Validator
**Primary Focus**: Platform choices, NFRs, and technical constraints (NOT implementation)

**Key Responsibilities**:

- Verify platform choice is justified
- Check NFRs are reasonable and measurable
- Validate technical constraints make sense
- **Ensure no premature implementation decisions**
- Assess integration points and dependencies

**Output**: `review/architecture-report.md`

---

## Output Requirements

### Directory Structure

**All review reports MUST be saved to**:

```
docs/01-planning/specifications/XXX-feature-name/review/
```

**Example**:

```
docs/01-planning/specifications/002-executable-task-generation-system/
├── SPEC.md
├── review/
│   ├── spec-review-report.md
│   ├── business-review-report.md
│   └── architecture-report.md
├── plans/           (created later by /plan)
└── tasks/           (created later by /tasks)
```

### Report Naming Convention

| Agent               | Output Filename                 |
| ------------------- | ------------------------------- |
| planning       | `spec-review-report.md`         |
| planning        | `business-review-report.md`     |
| architecture | `architecture-report.md` |

**Naming Rules**:

- Lowercase with hyphens
- `.md` extension
- Consistent across all features
- Easy to glob programmatically (`review/*.md`)

---

## Review Criteria Checklist

### For planning

**Requirement Quality**:

- [ ] All requirements have FR-XXX, TC-XXX, or NFR-XXX identifiers
- [ ] Requirements are testable (observable outcomes)
- [ ] Requirements use MUST/SHOULD/MAY language clearly
- [ ] Ambiguous terms are defined or avoided

**Scenario Quality**:

- [ ] User scenarios use Given/When/Then format
- [ ] Scenarios focus on outcomes, not implementation steps
- [ ] Edge cases are covered with specific scenarios
- [ ] Acceptance criteria are concrete and measurable

**Implementation Avoidance**:

- [ ] No code structure specified (classes, functions, methods)
- [ ] No algorithms detailed (search, sort, traversal methods)
- [ ] No data schemas specified (table structures, JSON formats)
- [ ] No API endpoint implementations described

**Planning Guidance** (NEW):

- [ ] Provides 2-3 distinct plan themes/approaches for planner to explore
- [ ] Identifies key technical decisions planner must address
- [ ] States constraints without prescribing implementation
- [ ] Allows planner flexibility to choose best technical solution

### For planning

**Business Value**:

- [ ] Pain points clearly identified with specific impact scores
- [ ] ROI calculations use hours only (no dollar amounts/hourly rates)
- [ ] Business value proposition is quantified
- [ ] Success metrics are business-focused outcomes

**Strategic Alignment**:

- [ ] Strategic outcomes map to roadmap item goals
- [ ] Feature aligns with current maturity stage (MVP/Core/Advanced)
- [ ] Budget compliance ($0-$100/month verified)
- [ ] Timeline realistic for complexity (not over/under estimated)

### For architecture

**Platform & Constraints**:

- [ ] Platform choice justified with rationale
- [ ] Technical constraints are actual requirements (not premature decisions)
- [ ] NFRs are measurable (not vague like "fast" or "reliable")
- [ ] Integration points identified without specifying internal wiring

**Risk Assessment**:

- [ ] Risks use P×I×E scoring methodology
- [ ] Mitigation strategies are concrete
- [ ] Technical risks focused on constraints/requirements, not implementation

---

## Review Report Template

**Template Location**: `.claude/templates/spec-review-template.md`

**Minimum Required Sections**:

1. **Executive Summary** - 1-2 paragraph overview
2. **Compliance Assessment** - WHAT/WHY/HOW focus evaluation
3. **Detailed Findings** - Strengths, issues, recommendations
4. **Implementation Details Found** - List any HOW leakage
5. **Review Verdict** - Ready for planning? (YES/NO/CONDITIONAL)

**Example Structure**:

```markdown
# Spec Review Report: [Feature Name]

**Document**: [Path to SPEC.md]
**Reviewer**: planning
**Date**: 2025-10-03

## Executive Summary

Specification is well-structured with clear business requirements.
Found 3 implementation details that should be moved to planning phase.

## Compliance Assessment

- **WHAT Requirements**: PASS - 29 clear functional requirements
- **WHY Rationale**: PASS - Strong pain point alignment (0.72 score)
- **HOW Avoidance**: CONCERNS - Found algorithm details in FR-008

## Detailed Findings

### ✅ Strengths

- Excellent Given/When/Then scenarios
- Clear success metrics (80% parallel identification)

### ⚠️ Issues Requiring Attention

- [IMPORTANT] FR-008 specifies "breadth-first search" (implementation detail)
- [MINOR] NFR-002 could be more specific about accuracy measurement

### 🔄 Recommendations

1. Remove "breadth-first search" from FR-008, replace with outcome
2. Add measurement methodology for 80% accuracy target

## Implementation Details Found

- Line 142: "Use breadth-first search algorithm" → Remove, describe outcome only
- Line 203: "Create TaskGenerator class" → Remove, this is planning detail

## Review Verdict

- **Ready for Planning**: CONDITIONAL
- **Conditions**: Remove 2 implementation details identified above
```

---

## Integration with SDD Workflow

### Automatic Trigger (Recommended)

The `/spec` command should output review instructions at completion:

```bash
/spec roadmap:TASK-001
# ... spec generation ...

📋 Next Steps: Specification Review

The specification has been created and requires review before planning.

Reviews will be saved to:
  docs/01-planning/specifications/002-executable-task-generation-system/review/

To trigger reviews:
  # Manual individual reviews
  Task planning "Review spec at docs/01-planning/specifications/002-executable-task-generation-system/SPEC.md"
  Task planning "Business review for docs/01-planning/specifications/002-executable-task-generation-system/SPEC.md"
  Task architecture "Architecture review for docs/01-planning/specifications/002-executable-task-generation-system/SPEC.md"

After addressing any CRITICAL issues, proceed with:
  /plan docs/01-planning/specifications/002-executable-task-generation-system/SPEC.md

Review Guidelines: .claude/docs/guides/spec-review-guidelines.md
```

### Manual Workflow

```bash
# 1. Create spec
/spec roadmap:TASK-001

# 2. Create review directory
mkdir -p docs/01-planning/specifications/002-executable-task-generation-system/review/

# 3. Trigger reviews
Task planning "Review SPEC.md for quality and HOW avoidance at [path]"
Task planning "Business alignment review at [path]"
Task architecture "Technical constraints review at [path]"

# 4. Review reports
cat docs/01-planning/specifications/002-executable-task-generation-system/review/*.md

# 5. Address critical issues

# 6. Proceed to planning
/plan docs/01-planning/specifications/002-executable-task-generation-system/SPEC.md
```

---

## Common Issues & How to Flag Them

### Issue: Implementation Details in Requirements

**Example**:

```markdown
❌ FR-005: System uses HashMap to store task dependencies
```

**How to Flag**:

```markdown
⚠️ ISSUE: Implementation Detail in FR-005

- Location: Line 89
- Problem: Specifies data structure (HashMap) - this is HOW, not WHAT
- Recommendation: Replace with outcome - "System MUST track task dependencies efficiently"
- Severity: IMPORTANT (blocks planning with clean slate)
```

### Issue: Vague Success Metrics

**Example**:

```markdown
❌ NFR-001: System should be fast and reliable
```

**How to Flag**:

```markdown
⚠️ ISSUE: Vague NFR in NFR-001

- Location: Line 156
- Problem: "Fast" and "reliable" are not measurable
- Recommendation: "System completes task generation in <10 minutes with 99% success rate"
- Severity: CRITICAL (cannot validate without measurable targets)
```

### Issue: Algorithm Specification

**Example**:

```markdown
❌ FR-010: Implement cycle detection using depth-first search with visited set
```

**How to Flag**:

```markdown
⚠️ ISSUE: Algorithm Detailed in FR-010

- Location: Line 142
- Problem: Specifies algorithm (DFS) and data structure (visited set)
- Recommendation: "System MUST detect circular dependencies and report specific dependency paths"
- Severity: IMPORTANT (constrains technical approach unnecessarily)
```

### Issue: Missing Business Rationale

**Example**:

```markdown
FR-015: System integrates with LIVING_SPRINT.md
(No explanation why)
```

**How to Flag**:

```markdown
⚠️ ISSUE: Missing WHY in FR-015

- Location: Line 178
- Problem: Requirement lacks business rationale
- Recommendation: Add pain point reference or value statement
- Severity: MINOR (requirement is clear, but context missing)
```

---

## Review Agent Instructions

**When assigned a spec review task**:

1. **Read this guidelines document** before starting review
2. **Load the specification** from provided path
3. **Assume review directory exists**: `[feature-dir]/review/` (created by /spec command)
4. **Use the review template** from `.claude/templates/spec-review-template.md`
5. **Focus on your role's responsibilities** (quality, business, or technical constraints)
6. **Flag ALL implementation details** found in spec (this is critical!)
7. **Write report directly** to `[feature-dir]/review/[your-report-name].md`
8. **Return summary** to orchestrator with verdict (READY/CONDITIONAL/NOT READY)

**Key Mindset**: You are a **gatekeeper** ensuring specs remain focused on WHAT and WHY. Implementation details (HOW) belong in PLAN.md, not SPEC.md. Be strict about this boundary.

---

## FAQ

**Q: What if a technical constraint requires specifying a particular technology?**
A: That's fine if it's a genuine requirement. Example: "Must be Claude Code command" is valid because the platform IS the requirement. But "Must use specific algorithm X" is usually not a requirement - it's a premature implementation decision.

**Q: How detailed should NFRs be?**
A: Measurable but not prescriptive. "Completes in <10 minutes" ✅ vs "Uses caching to speed up" ❌

**Q: Should specs mention existing components?**
A: Yes, for integration context. "Must integrate with LIVING_SPRINT.md" ✅ but "Must call updateLivingSprint() function" ❌

**Q: What if all reviews pass?**
A: Proceed immediately to `/plan` command with confidence!

**Q: What if critical issues found?**
A: Spec should be revised before planning. Update SPEC.md, then re-run reviews.

---

**This document ensures consistent, high-quality specifications that enable effective planning and implementation without premature technical constraints.**

# Technical PM Documentation

Supporting documentation for the technical-pm agent.

## Contents

| Document | Purpose |
|----------|---------|
| `review-methodology.md` | OODA phases, review procedures (6 phases), success/failure criteria, escalation paths |
| `business-frameworks.md` | Code Reuse ROI, Cost-Benefit Analysis, Risk-Adjusted Planning, Timeline Realism |

## Shared Framework References

The technical-pm agent references these shared frameworks (do NOT duplicate):

- `cost-analysis-framework.md` - Budget validation, $100/month constraint
- `risk-assessment-matrix.md` - P×I×E scoring methodology for **business risks**
- `quality-scoring-algorithms.md` - Timeline realism calculations
- `base-review-agent-pattern.md` - Inherited review agent behaviors

## Deferred to Other Agents

These capabilities are owned by specialist agents (technical-pm does NOT handle):

- **SPEC quality/structure validation** → `spec-reviewer`
- **Progressive disclosure scoring** → `spec-reviewer`
- **Technical feasibility assessment** → `architecture-review`
- **Technical risk P×I×E scoring** → `architecture-review`

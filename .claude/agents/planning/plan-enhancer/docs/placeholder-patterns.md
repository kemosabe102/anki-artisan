# Placeholder Patterns Reference

Common placeholder patterns found in PLAN.md files and their replacement strategies.

## Business Section Placeholders

### Goals & Objectives
| Pattern | Source | Example Replacement |
|---------|--------|---------------------|
| `[Business Goal 1]` | SPEC.md Business Goals | "Reduce customer onboarding time by 40%" |
| `[Primary Objective]` | SPEC.md Problem Statement | "Automate manual screening workflows" |
| `[Strategic Alignment]` | SPEC.md Business Case | "Supports Q3 efficiency initiative" |

### Success Metrics
| Pattern | Source | Example Replacement |
|---------|--------|---------------------|
| `[Success Metric 1]` | SPEC.md Success Criteria | "Customer satisfaction >4.5/5.0" |
| `[KPI]` | SPEC.md Business Metrics | "30% reduction in support tickets" |
| `[Measurable Outcome]` | SPEC.md Acceptance Criteria | "Processing time <2s (P95)" |

### Value Propositions
| Pattern | Source | Example Replacement |
|---------|--------|---------------------|
| `[Value Proposition 1]` | SPEC.md User Needs | "Self-service reduces analyst burden by 60%" |
| `[User Benefit]` | SPEC.md Pain Points | "Eliminates 4-hour daily data gathering" |
| `[ROI Statement]` | Cost Analysis + SPEC | "$500K annual savings, 12-month payback" |

### Component References
| Pattern | Source | Example Replacement |
|---------|--------|---------------------|
| `[Component1]`, `[Component2]` | plan_metadata.name | "DataIngestionService", "ValidationEngine" |
| `[Feature Name]` | SPEC.md Feature List | "Automated Portfolio Screening" |
| `[Module Name]` | Component Almanac | "packages/core/screening" |

### Requirements Traceability
| Pattern | Source | Example Replacement |
|---------|--------|---------------------|
| `[FR-XXX]` | SPEC.md Functional Reqs | "FR-001: System shall validate OHLCV data" |
| `[Requirement 1]` | SPEC.md Requirements | "Data must be queryable within 100ms" |
| `[NFR-XXX]` | SPEC.md Non-Functional | "NFR-003: 99.9% uptime SLA" |

## Technical Section Placeholders (PRESERVE)

These are left for architecture-enhancer:
- `[Architecture Decision]`
- `[Technical Implementation]`
- `[API Specification]`
- `[System Integration]`
- `[Performance Strategy]`
- `[Database Schema]`

## Code Reuse Patterns

When COMPONENT_ALMANAC.md reveals existing components:

### Reuse Opportunity Value Statements
```markdown
**Reuse Opportunity**: Leverage existing ValidationEngine
- Time Savings: 60% reduction in development effort
- Risk Reduction: Proven component with 95% test coverage
- Maintenance: Consolidated codebase reduces long-term burden
```

### Replacement Scenario Value Statements
```markdown
**Component Modernization**: Replace LegacyParser with StreamProcessor
- Technical Debt Reduction: Eliminates 2,500 lines of deprecated code
- Performance: 3x throughput improvement
- Cleanup Task: Phase out LegacyParser by Sprint 5
```

## Anti-Patterns

### ❌ Never Leave These
- `[Component1]` without actual name
- `[TBD]` or `[TODO]` in business sections
- `[X Sprint Points]` without number
- `[Placeholder]` generic markers
- `[See SPEC]` without extracting content

### ✅ Always Replace With
- Specific component names from metadata
- Concrete business goals with metrics
- Actual sprint point estimates
- Measurable success criteria
- FR-ID traceability with business value

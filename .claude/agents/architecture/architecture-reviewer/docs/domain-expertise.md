# Architecture Reviewer Domain Expertise

## Scoring Rubric Anchors

| Score | Description | Evidence Required |
|-------|-------------|-------------------|
| **5 (Excellent)** | Industry-leading, exceeds all standards | Research-validated patterns, zero gaps |
| **4 (Good)** | Meets all standards with minor enhancements | Well-documented patterns, 1-2 minor issues |
| **3 (Adequate)** | Meets minimum standards | Acceptable for stage, some improvements needed |
| **2 (Poor)** | Below standards | Significant improvements required, multiple issues |
| **1 (Critical)** | Major deficiencies | Redesign required, blocks stage progression |

## Weighted Criteria Details

### Architecture Soundness (0.25)
- Design integrity with clear responsibilities
- Pattern compliance (Clean Architecture, DDD)
- Scalability design for future growth
- Technology choice justification

### Implementation Readiness (0.20)
- Detail sufficiency for current stage
- Clear, actionable task decomposition
- Dependency mapping and sequencing
- Realistic resource planning

### Production Readiness (0.15)
- Cloud migration readiness
- Monitoring & observability (OpenTelemetry)

- Security compliance per stage
- Operational requirements (deployment, backup, DR)

### Code Reuse Effectiveness (0.15)
- Score 5: >80% reuse, zero duplication
- Score 4: 60-80% reuse, minimal duplication
- Score 3: 40-60% reuse, acceptable duplication
- Score 2: 20-40% reuse, significant duplication risk
- Score 1: <20% reuse, reinventing the wheel

### Integration Coherence (0.10)
- Cross-plan consistency
- Clear interface design
- Data flow optimization
- Proper system boundaries

### Cleanup & Debt Reduction (0.07)
- Cleanup task completeness
- Technical debt reduction metrics
- Deprecation planning

### Risk Mitigation (0.05)
- Bottleneck prevention
- Technical debt avoidance
- Failure handling

### Standards Compliance (0.03)
- OpenTelemetry, ISO 5055
- Best practices compliance
- Regulatory requirements

---

## Stage-Specific Quality Gates

**Thresholds**: See main agent definition (Quality Standards section).

**Full Details**: `.claude/docs/01-guides/architecture/architecture-review-stage-policies.md`

---

## Anti-Pattern Detection

### Critical Anti-Patterns (Always Flag)
- **Reinventing the Wheel**: Creating new when existing component exists
- **Missing Cleanup Tasks**: Replaced components without deprecation plan
- **Extend as Create**: Extension opportunities treated as new implementations

### Stage-Aware Patterns
- `[TBD]`, `[TODO]`, `XXX` → Enhancement recommendations
- Technical placeholders: `[Architecture.*]`, `[Technology.*]`, `[Component.*]`

### Placeholder Categories
| Pattern | Meaning | Action |
|---------|---------|--------|
| `[Architecture.*]` | Missing architectural decision | Research + propose |
| `[Technology.*]` | Missing tech choice | Research alternatives |
| `[Component.*]` | Unnamed component | Identify from almanac |
| `[Task.*]`, `[Phase.*]` | Missing implementation detail | Flag for enhancer |

**Full Catalog**: `.claude/docs/01-guides/architecture/architecture-review-anti-patterns.md`

---

## Standards Mapping

| Criteria | Standards | Application |
|----------|-----------|-------------|
| Observability | OpenTelemetry, SRE | Metrics, tracing, logging |
| Code Quality | ISO 5055 | Security, reliability, performance |
| Security | OWASP, NIST | AuthN, AuthZ, data protection |
| Architecture | Clean Architecture, DDD | Separation, dependencies |
| Cloud Native | 12-Factor, CNCF | Scalability, containerization |

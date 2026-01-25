# Workflow Phases

Detailed documentation for each phase of the `/review-architecture` command.

---

## Phase Overview

| Phase | Name | Framework | Duration | Gate |
|-------|------|-----------|----------|------|
| P0 | VALIDATE | Cynefin | 10s | Entry point accessible, stage determined |
| P1 | EXPLORE | MECE | 180s/agent | >= 2 agents returned valid results |
| P2 | COLLECT | OODA-OBSERVE | 240s total | >= 2 agents with framework analysis |
| P3 | SYNTHESIZE | Multi-Framework | 45s | Confidence >= 0.75 |
| P4 | PRE-MORTEM | Failure Analysis | 90s | >= 3 failure modes identified |
| P5 | RECOMMEND | ICE Scoring | 20s | All findings categorized P1-P4 |
| P6 | REPORT | Progressive Disclosure | 15s | Report passes schema validation |
| P7 | DELEGATION | OODA-ACT | Variable | User-triggered |
| P8 | ADR-GENERATE | ADR Template | 120s | --generate-adrs flag + P6 complete |

---

## P0: VALIDATE (Cynefin Classification)

**Purpose**: Fail-fast on invalid inputs, determine maturity stage
**Framework**: Cynefin (classify problem complexity)
**Executor**: Orchestrator

### Operations

1. Parse $ARGUMENTS (file path, directory, area, or SPEC/PLAN)
2. Verify entry point accessible
3. Auto-detect stage using heuristics
4. Override stage with `--stage <MVP|Alpha|Beta|RC|GA>` if provided

### Stage Auto-Detection Heuristics

```
IF adr_count < 5 AND test_coverage < 70% AND no_monitoring THEN stage = MVP
IF adr_count >= 5 AND test_coverage >= 70% AND basic_ci THEN stage = Alpha
IF adr_count >= 10 AND test_coverage >= 85% AND full_pipeline AND basic_monitoring THEN stage = Beta
IF adr_count >= 15 AND test_coverage >= 90% AND comprehensive_monitoring THEN stage = RC
IF adr_count >= 20 AND test_coverage >= 95% AND production_monitoring AND docs_complete THEN stage = GA
```

### Detection Signals

| Signal | MVP | Alpha | Beta | RC | GA |
|--------|-----|-------|------|----|----|
| ADR Count | <5 | 5-9 | 10-14 | 15-19 | 20+ |
| Test Coverage | <70% | 70-84% | 85-89% | 90-94% | 95%+ |
| CI/CD | None/Basic | Pipeline | Full | Full | Full+Governance |
| Monitoring | None | Basic | Comprehensive | Comprehensive | Production |
| Documentation | Minimal | Partial | Complete | Complete | Complete+Compliance |

**Gate**: Entry point accessible AND stage determined
**Timeout**: 10s


---

## P1: EXPLORE (MECE + 3 Parallel Agents)

**Purpose**: Launch parallel multi-perspective architecture analysis
**Framework**: MECE (Mutually Exclusive, Collectively Exhaustive)
**Executor**: 3 agents launched in single message

### Agents

| Agent | Focus | Question Answered |
|-------|-------|-------------------|
| architecture-reviewer | Structure, patterns, interfaces | WHAT is the architecture? |
| tech-debt-investigator | Health metrics, debt scoring | HOW BAD is the current state? |
| Explore (Task subagent) | Discovery, dependencies, boundaries | WHERE are the components? |

### MECE Coverage

- **architecture-reviewer**: Structural quality dimension
- **tech-debt-investigator**: Health/debt dimension
- **Explore**: Discovery/mapping dimension

No overlap, complete coverage of architecture analysis needs.

### Graceful Degradation

- **3/3 agents**: Full analysis, highest confidence
- **2/3 agents**: Proceed with reduced confidence (0.8x multiplier)
- **1/3 agents**: FAIL - insufficient coverage

**Gate**: >= 2 agents returned valid results
**Timeout**: 180s per agent


---

## P2: COLLECT (OODA-OBSERVE + Stage Frameworks)

**Purpose**: Gather results, apply stage-appropriate validation frameworks
**Framework**: OODA-OBSERVE (systematic data gathering)
**Executor**: Orchestrator

### Operations

1. Await P1 agent results
2. Validate result schemas
3. Apply stage-appropriate frameworks (see framework-integration.md)

### Stage Framework Matrix

| Stage | SOLID | NFR Categories | ARB Level | TOGAF Level |
|-------|-------|----------------|-----------|-------------|
| MVP | SRP, DIP only | 3 (Perf, Sec, Rel) | - | L2 (Architecture Vision) |
| Alpha | Full SOLID | 6 (+Scale, Maint, Usab) | ARB1-2 | L3 (Information Systems) |
| Beta | Full SOLID | 8 (+Port, Test) | ARB2-3 | L3-4 (Technology) |
| RC | Full + patterns | All 10 | ARB3 | L4 (Full Technology) |
| GA | Complete | All 10 + compliance | ARB4 | L5 (Governance) |

**Gate**: >= 2 agents returned valid results with framework analysis
**Timeout**: 240s total

---

## P3: SYNTHESIZE (Multi-Framework Synthesis)

**Purpose**: Merge findings across frameworks, calculate composite score
**Framework**: Synthesis Framework (weighted consolidation)
**Executor**: Orchestrator


### Composite Scoring Algorithm

```
Composite Score = (SOLID × 0.25) + (NFR × 0.40) + (TOGAF × 0.20) + (ARB × 0.15)
```

### Framework Score Normalization

| Framework | Normalization Rule |
|-----------|-------------------|
| SOLID | 0 violations = 5.0, each violation -0.5, min 0 |
| NFR | compliance_percentage × 5 / 100 |
| TOGAF | maturity_level (L1=1, L2=2, L3=3, L4=4, L5=5) |
| ARB | board_level (none=0, ARB1=1.25, ARB2=2.5, ARB3=3.75, ARB4=5.0) |

### Confidence Calculation

```
Confidence = min(agent_confidences) × coverage_factor
coverage_factor = frameworks_applied / frameworks_required_for_stage
```

### Overlap Detection

- Similarity threshold: >0.7 triggers merge
- Similarity = (keyword_overlap × 0.4) + (domain × 0.3) + (location × 0.2) + (agent_type × 0.1)

**Gate**: Consolidated findings with confidence >= 0.75
**Timeout**: 45s

---

## P4: PRE-MORTEM (Failure Mode Analysis)

**Purpose**: Identify architecture failure modes before they occur
**Framework**: Pre-Mortem (assume failure, work backwards)
**Executor**: contingency-planner agent


### Stage-Specific Risk Categories

| Stage | Primary Risk Categories |
|-------|------------------------|
| MVP | Technical debt accumulation, scalability cliffs |
| Alpha | Integration failures, security gaps |
| Beta | Performance degradation, user experience issues |
| RC | Deployment failures, rollback complications |
| GA | SLA violations, compliance failures |

### Risk Scoring

```
Risk Score = Probability × Impact × Exposure (P×I×E)
```

Each dimension scored 1-5:
- **Probability**: How likely is this failure?
- **Impact**: How severe if it occurs?
- **Exposure**: How much of the system is affected?

### Output Requirements

- Minimum 3 failure modes identified
- Each failure mode has mitigation plan
- Risk matrix with P×I×E scoring

**Gate**: >= 3 failure modes identified with mitigations
**Timeout**: 90s

---

## P5: RECOMMEND (ICE Prioritization)

**Purpose**: Prioritize improvements by impact, confidence, and ease
**Framework**: ICE Scoring
**Executor**: Orchestrator


### ICE Scoring Methodology

Each finding scored on 3 dimensions (1-10 scale):

| Dimension | Question | Scale |
|-----------|----------|-------|
| Impact | How much will this improve architecture quality? | 1=minimal, 10=transformative |
| Confidence | How certain are we this is a real issue? | 1=speculative, 10=definite |
| Ease | How easy is it to fix? | 1=major effort, 10=trivial |

### ICE Calculation

```
ICE Score = (Impact × Confidence × Ease) / 10
```

### Priority Assignment

| Priority | ICE Range | Override Condition |
|----------|-----------|-------------------|
| P1 (Critical) | >= 7.0 | OR any critical risk |
| P2 (High) | 5.0 - 6.9 | OR any high risk |
| P3 (Medium) | 3.0 - 4.9 | - |
| P4 (Low) | < 3.0 | - |

**Gate**: All findings categorized into P1/P2/P3/P4
**Timeout**: 20s

---

## P6: REPORT (Progressive Disclosure)

**Purpose**: Generate deliverable with appropriate detail level
**Framework**: Progressive Disclosure (executive summary -> details)
**Executor**: Orchestrator


### Report Levels

| Level | Content | Use Case |
|-------|---------|----------|
| executive | Score, gate pass/fail, top 3 findings | Quick status check |
| detailed | + framework breakdown, all P1/P2 findings | Standard review (default) |
| comprehensive | + all findings, full evidence, roadmap | Deep dive, audits |

### Stage-Aware Defaults

| Stage | Default Report Level |
|-------|---------------------|
| MVP | detailed |
| Alpha | detailed |
| Beta | detailed |
| RC | detailed |
| GA | comprehensive |

### Report Structure

```
1. Executive Summary (always shown)
   - Composite Score: X.X/5.0
   - Stage Gate: PASS/FAIL for {stage}
   - Top 3 Findings
   
2. Framework Analysis (detailed+)
   - SOLID Assessment
   - NFR Compliance
   - TOGAF Maturity
   - ARB Readiness
   
3. Detailed Findings (detailed+)
   - P1 Findings (Critical)
   - P2 Findings (High)
   
4. Complete Analysis (comprehensive only)
   - P3/P4 Findings
   - Full Evidence Matrix
   - Improvement Roadmap
```

**Human Decision Point**: P6 ends with user approval before P7/P8.
**Gate**: Report passes schema validation
**Timeout**: 15s


---

## P7: DELEGATION (OODA-ACT) - Conditional

**Purpose**: Route approved findings to implementation agents
**Framework**: OODA-ACT
**Executor**: Orchestrator delegates (does NOT execute directly)
**Trigger**: User approves report and requests implementation

### Delegation Routing Matrix

| Finding Type | Primary Agent | Fallback Agent |
|--------------|---------------|----------------|
| Architecture patterns | agent-architect | architecture-reviewer |
| SOLID violations | python-code-implementer | refactoring-specialist |
| NFR gaps (performance) | python-code-implementer | debugger |
| NFR gaps (security) | security-reviewer | python-code-implementer |
| NFR gaps (scalability) | agent-architect | python-code-implementer |
| TOGAF compliance | agent-architect | doc-librarian |
| Integration issues | python-code-implementer | debugger |
| Documentation gaps | doc-librarian | agent-architect |
| Test coverage gaps | test-creator | python-code-implementer |
| Monitoring gaps | python-code-implementer | agent-architect |
| Dependency issues | debugger | python-code-implementer |

### User Trigger Phrases

- "implement" or "fix these issues" -> Execute all P1 findings
- "implement P1 and P2" -> Execute P1 and P2 priority findings
- "implement [specific finding]" -> Execute single finding

**Gate**: All delegated tasks complete with success status
**Anti-Pattern**: Orchestrator executing fixes directly (MUST delegate)


---

## P8: ADR-GENERATE (Architecture Decision Records) - Conditional

**Purpose**: Generate ADR templates for undocumented architecture decisions
**Framework**: ADR Template Generation
**Executor**: agent-architect (delegated)
**Trigger**: `--generate-adrs` flag provided AND P6 complete

### Pre-Check

Verify ADR directory exists (`docs/adr/`) or create it.

### ADR Template Structure

```markdown
# ADR-NNNN: {Decision Title}

## Status
Proposed

## Context
Why this decision was needed.

## Decision
What was decided.

## Consequences
Impact of the decision (positive and negative).

## Alternatives Considered
Other options that were evaluated.
```

### ADR Generation Triggers

ADRs generated for:
- Critical pattern choices
- Technology selections
- Integration approaches
- NFR trade-offs
- Risk mitigations

**Output Path**: `docs/adr/ADR-{NNNN}-{slug}.md`
**Gate**: Critical decisions have templates generated
**Timeout**: 120s

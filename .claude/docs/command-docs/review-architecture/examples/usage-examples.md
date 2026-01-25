# Usage Examples

Complete usage scenarios for `/review-architecture`.

---

## Example 1: Basic Directory Review

```bash
/review-architecture packages/core/
```

**What happens**:
1. P0: Validates path, auto-detects stage from project signals
2. P1: Launches 3 agents in parallel (architecture-reviewer, tech-debt-investigator, Explore)
3. P2: Collects results, applies stage-appropriate frameworks
4. P3: Synthesizes findings with composite scoring
5. P4: Runs pre-mortem failure analysis
6. P5: Prioritizes findings with ICE scoring
7. P6: Generates detailed report

**Expected output** (abbreviated):
```
Architecture Review Report: packages/core/
Stage: Alpha (auto-detected) | Override: No
Composite Score: 3.9/5.0 (Grade: B)
Stage Gate: PASS for Alpha

Framework Analysis:
- SOLID: 4.0/5.0 (2 violations)
- NFR: 3.8/5.0 (5/6 categories passing)
- TOGAF: Level 3 (Information Systems)
- ARB: ARB2 (Design Review passed)

Top 3 P1 Findings:
1. Missing dependency injection in DataLoader - ICE: 7.2
2. NFR gap: No rate limiting on API endpoints - ICE: 7.0
3. Incomplete error handling in integration layer - ICE: 6.8
```


---

## Example 2: Stage-Specific Review

```bash
/review-architecture --stage Beta packages/core/
```

**Use case**: Override auto-detection when you know target maturity level.

**What changes**:
- Beta-level frameworks applied (8 NFR categories instead of 6)
- Higher quality gates (3.8 minimum vs 3.7)
- TOGAF L3-4 expected
- ARB2-3 gates evaluated

**Expected output** (abbreviated):
```
Architecture Review Report: packages/core/
Stage: Beta (override) | Override: Yes
Composite Score: 3.6/5.0 (Grade: B)
Stage Gate: FAIL for Beta (minimum 3.8 required)

Blocking Issues for Beta:
- Test coverage 82% (need 85%)
- Missing Portability assessment
- ARB3 not achieved
```

---

## Example 3: ADR Generation Mode

```bash
/review-architecture --generate-adrs packages/core/
```

**What happens**:
1. P0-P6: Full analysis executes (NOT skipped)
2. P8: After P6 completes, generates ADR templates for undocumented decisions


**Critical**: `--generate-adrs` does NOT skip analysis phases.

**Expected output** (abbreviated):
```
Architecture Review Report: packages/core/
[... normal P6 report ...]

ADR Generation (P8):
Generated 4 ADR templates:
- docs/adr/ADR-0012-event-driven-architecture.md
- docs/adr/ADR-0013-repository-pattern-selection.md
- docs/adr/ADR-0014-caching-strategy.md
- docs/adr/ADR-0015-error-handling-approach.md

Each ADR contains:
- Status: Proposed
- Context: Extracted from architecture analysis
- Decision: Inferred from implementation
- Consequences: Identified trade-offs
- Alternatives: Common alternatives listed
```

---

## Example 4: Report Level Control

```bash
/review-architecture --report-level comprehensive packages/core/
```

**Report levels**:

| Level | Content | Lines |
|-------|---------|-------|
| executive | Score, gate, top 3 findings | ~20 |
| detailed | + framework breakdown, P1/P2 findings | ~80 |
| comprehensive | + all findings, evidence, roadmap | ~200 |


**Executive report** (abbreviated):
```
Architecture Review: packages/core/
Score: 3.9/5.0 | Grade: B | Gate: PASS (Alpha)

Top 3 Findings:
1. Missing DI in DataLoader (P1)
2. No rate limiting (P1)
3. Incomplete error handling (P1)
```

**Comprehensive report** adds:
- Full SOLID violation details with file:line references
- All 10 NFR category assessments
- Complete failure mode matrix
- P3/P4 findings
- Improvement roadmap with effort estimates

---

## Example 5: Full Codebase Review

```bash
/review-architecture --all
```

**Duration**: 15-45 minutes (depends on codebase size)

**What happens**:
1. Discovers all architectural entry points
2. Batches analysis (parallel where safe)
3. Aggregates findings across components
4. Generates ecosystem-level report


**Expected output** (abbreviated):
```
Full Codebase Architecture Review

Components Analyzed: 12
Total Duration: 28m 15s

Ecosystem Health:
- Average Score: 3.7/5.0
- Components Passing Gate: 10/12
- Critical Issues: 5
- High Issues: 12

Component Breakdown:
| Component | Score | Gate | Stage |
|-----------|-------|------|-------|
| packages/core | 4.1 | PASS | Alpha |
| packages/api | 3.9 | PASS | Alpha |
| packages/data | 3.2 | FAIL | MVP |
| packages/utils | 4.3 | PASS | Beta |

Cross-Cutting Concerns:
- Inconsistent error handling patterns (3 components)
- Missing observability in data layer
- DIP violations in 4 components
```

---

## Example 6: SPEC/PLAN Review

```bash
/review-architecture docs/00-project/SPEC.md
```

**Use case**: Review architecture from specification documents.


**What changes**:
- Analyzes documented architecture (not implementation)
- Validates spec completeness against TOGAF requirements
- Identifies gaps between spec and recommended practices
- Suggests missing ADRs based on decisions in spec

**Expected output** (abbreviated):
```
Specification Architecture Review: SPEC.md

Spec Completeness: 78%
TOGAF Coverage: L3 documented, L4 partial

Missing Sections:
- Deployment architecture
- Disaster recovery strategy
- Performance targets (SLAs)

Recommended ADRs:
- ADR: Database selection rationale
- ADR: API versioning strategy
- ADR: Authentication approach
```

---

## Common Scenarios

| Scenario | Command | Notes |
|----------|---------|-------|
| Pre-release gate check | `/review-architecture --stage RC` | Validate RC readiness |
| Tech debt assessment | `/review-architecture packages/legacy/` | Focus on debt scoring |
| New component validation | `/review-architecture packages/new-feature/` | Early architecture feedback |
| Documentation audit | `/review-architecture --generate-adrs` | Find undocumented decisions |
| Stage promotion | `/review-architecture --stage Beta` | Check Beta requirements |
| Executive summary | `/review-architecture --report-level executive` | Quick status for stakeholders |

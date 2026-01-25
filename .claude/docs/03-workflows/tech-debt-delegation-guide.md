---
title: "Technical Debt Investigation Delegation Guide"
date: 2025-11-12
status: ACTIVE
tags: [workflow, technical-debt, delegation, tech-debt-investigator, orchestration]
---

**Purpose**: Comprehensive guide for delegating technical debt analysis to tech-debt-investigator agent with proper context metadata, delegation patterns, and output interpretation.

**Target Audience**: Claude Code (orchestrator) delegating technical debt analysis tasks

**Quick Reference**: Context metadata template → Delegation patterns → Output interpretation → Best practices

---

## Overview

### What is tech-debt-investigator?

A framework-aligned technical debt analyzer using SQALE/SIG methodologies to identify, quantify, and prioritize debt across 6 categories:

1. **Code Quality** - Smells, complexity, duplication, violations
2. **Architecture** - Coupling, scalability, dependencies
3. **Testing** - Coverage, missing tests, flaky tests
4. **Documentation** - Missing docs, outdated READMEs, tribal knowledge
5. **Infrastructure** - Hard-coded configs, deprecated APIs, CVEs
6. **Design/UI** - UX inconsistencies, accessibility gaps (if applicable)

### Key Capabilities

- **Quantitative Metrics**: debt_score (0-100), TDR, SQALE grade (A-E), SIG star rating (1-5)
- **Git-Based Analysis**: Hotspot detection (churn × complexity × defects), ownership dispersion
- **Impact/Effort Prioritization**: P1 Quick Wins, P2 Strategic, P3 Defer, P4 Opportunistic
- **Trend Tracking**: Baseline comparison, regression detection, debt trajectory
- **Principal vs Interest**: Fix cost now vs ongoing cost if unfixed

### When to Delegate

Use tech-debt-investigator when user requests:

- **Code quality assessment** ("How healthy is our codebase?")
- **Debt prioritization** ("What technical debt should we fix first?")
- **Refactoring planning** ("Which modules need refactoring?")
- **Codebase health audits** ("Pre-release quality check")
- **Pre-release quality gates** ("Can we ship this?")
- **Incident post-mortem** ("Why does this module keep breaking?")
- **Sprint planning** ("What's high-value, low-effort technical debt?")

---

## Context Metadata Template

**CRITICAL**: Provide comprehensive context for accurate analysis. Missing context = lower quality output.

### Full Template

```json
{
  "scope": {
    "directories": ["packages/", "tests/"],
    "file_patterns": ["*.py", "*.md", "*.yaml"],
    "exclusions": [".venv/", "node_modules/", "__pycache__/", "*.pyc"],
    "focus_modules": ["auth", "api", "core"]
  },
  "baseline_data": {
    "previous_debt_score": 62.5,
    "previous_tdr": 0.08,
    "previous_sqale_grade": "C",
    "previous_sig_rating": 3,
    "run_timestamp": "2025-01-15T10:30:00Z",
    "report_path": ".claude/reports/tech-debt-2025-01-15.json"
  },
  "business_context": {
    "critical_modules": ["auth", "payment", "api"],
    "usage_frequency": {
      "auth": "1000 req/min",
      "payment": "500 req/min",
      "batch_reports": "10 req/day"
    },
    "recent_incidents": [
      {"module": "auth", "date": "2025-01-10", "severity": "P1"},
      {"module": "api", "date": "2025-01-05", "severity": "P2"}
    ],
    "upcoming_milestones": [
      {"name": "v2.0 release", "date": "2025-02-01", "quality_gate": "TDR <10%"}
    ]
  },
  "analysis_preferences": {
    "max_hotspots": 10,
    "effort_estimation_model": "conservative",
    "include_design_ui_debt": false,
    "prioritization_weight": {
      "business_impact": 0.4,
      "effort": 0.3,
      "risk": 0.2,
      "frequency": 0.1
    }
  }
}
```

### Minimal Template (Quick Analysis)

```json
{
  "scope": {
    "directories": ["packages/core/"],
    "file_patterns": ["*.py"]
  }
}
```

### Context Metadata Components

#### 1. Scope Definition

**Required Fields**:

- `directories`: Array of directories to analyze (relative to repo root)
- `file_patterns`: File types to include (glob patterns)

**Optional Fields**:

- `exclusions`: Directories/patterns to skip (reduce noise)
- `focus_modules`: Prioritize specific modules (affects hotspot ranking)

**Examples**:

```json
// Full codebase scan
"scope": {
  "directories": ["packages/", "tests/", "k8s/"],
  "file_patterns": ["*.py", "*.yaml", "*.md"],
  "exclusions": [".venv/", "node_modules/", "__pycache__/"]
}

// Targeted analysis (single module)
"scope": {
  "directories": ["packages/auth/"],
  "file_patterns": ["*.py"],
  "focus_modules": ["session", "token"]
}

// Pre-release scan (changed files only)
"scope": {
  "directories": ["packages/", "tests/"],
  "file_patterns": ["*.py"],
  "exclusions": ["tests/integration/"]  // Skip slow tests
}
```

#### 2. Baseline Data (for Trend Analysis)

**Purpose**: Enable regression detection and debt trajectory tracking

**Optional but HIGHLY RECOMMENDED** for:

- Pre-release quality gates (detect regressions)
- Sprint retrospectives (track improvement)
- Long-term health monitoring (quarterly audits)

**Fields**:

- `previous_debt_score`: Last run's composite score (0-100)
- `previous_tdr`: Last run's Technical Debt Ratio (0.00-1.00)
- `previous_sqale_grade`: Last run's SQALE grade (A-E)
- `previous_sig_rating`: Last run's SIG star rating (1-5)
- `run_timestamp`: ISO 8601 timestamp of previous run
- `report_path`: Path to previous JSON report (optional, for detailed comparison)

**Example**:

```json
"baseline_data": {
  "previous_debt_score": 62.5,
  "previous_tdr": 0.08,
  "previous_sqale_grade": "C",
  "previous_sig_rating": 3,
  "run_timestamp": "2025-01-15T10:30:00Z"
}
```

**Benefits**:

- **Regression Detection**: Alert if TDR increases >5% or coverage drops >5%
- **Trend Visualization**: "Debt score improved from 62.5 → 68.2 (+5.7 points)"
- **ROI Tracking**: "30 hours invested, TDR reduced from 12% → 8%"

#### 3. Business Context (for Prioritization)

**Purpose**: Weight debt items by business criticality, not just technical severity

**Fields**:

- `critical_modules`: Array of module names (prioritized in hotspot ranking)
- `usage_frequency`: Map of module → traffic metrics (affects Impact score)
- `recent_incidents`: Array of incidents (correlate with hotspots)
- `upcoming_milestones`: Release dates and quality gates (prioritize blockers)

**Example**:

```json
"business_context": {
  "critical_modules": ["auth", "payment"],
  "usage_frequency": {
    "auth": "1000 req/min",      // High traffic = higher priority
    "payment": "500 req/min",
    "admin": "10 req/day"         // Low traffic = lower priority
  },
  "recent_incidents": [
    {"module": "auth", "date": "2025-01-10", "severity": "P1"}
  ],
  "upcoming_milestones": [
    {"name": "v2.0 release", "date": "2025-02-01", "quality_gate": "TDR <10%"}
  ]
}
```

**Benefits**:

- **Prioritization Weighting**: High-traffic modules ranked higher in hotspot list
- **Incident Correlation**: "auth module: 3 incidents + high complexity = P1 priority"
- **Release Planning**: "v2.0 release in 3 weeks, 5 P1 items blocking (TDR 12% > 10% gate)"

#### 4. Analysis Preferences (Customize Output)

**Optional Fields**:

- `max_hotspots`: Limit hotspot list (default: 10)
- `effort_estimation_model`: "conservative" (1.5× industry) | "standard" (industry) | "aggressive" (0.75× industry)
- `include_design_ui_debt`: Boolean (skip if not applicable)
- `prioritization_weight`: Custom weights for Impact/Effort matrix

**Example**:

```json
"analysis_preferences": {
  "max_hotspots": 5,                   // Show top 5 only
  "effort_estimation_model": "conservative",
  "include_design_ui_debt": false,     // Skip UI analysis (backend project)
  "prioritization_weight": {
    "business_impact": 0.5,            // Business value most important
    "effort": 0.2,                     // Effort less important
    "risk": 0.2,
    "frequency": 0.1
  }
}
```

---

## Delegation Patterns

### Pattern 1: Full Codebase Health Assessment

**Use Case**: Comprehensive quality audit with baseline comparison

**When to Use**:

- Quarterly health reviews
- Post-acquisition due diligence
- Major refactoring planning
- Executive reporting

**Delegation Template**:

```markdown
Task(tech-debt-investigator,
  "Analyze technical debt in packages/ and tests/ with baseline from 2025-01-15.
   Prioritize auth and payment modules (high traffic: 1000 req/min, 500 req/min).
   Calculate debt_score, TDR, identify top 10 hotspots, generate Impact/Effort
   matrix with remediation roadmap. Compare to baseline (debt_score: 62.5,
   TDR: 0.08) and flag regressions.")
```

**Context Metadata**:

```json
{
  "scope": {
    "directories": ["packages/", "tests/"],
    "file_patterns": ["*.py"],
    "exclusions": [".venv/", "__pycache__/"]
  },
  "baseline_data": {
    "previous_debt_score": 62.5,
    "previous_tdr": 0.08,
    "run_timestamp": "2025-01-15T10:30:00Z"
  },
  "business_context": {
    "critical_modules": ["auth", "payment"],
    "usage_frequency": {
      "auth": "1000 req/min",
      "payment": "500 req/min"
    }
  }
}
```

**Expected Deliverables**:

- Comprehensive debt report (all 6 categories)
- debt_score + TDR + SQALE grade + SIG rating
- Top 10 hotspots (churn × complexity × defects)
- Impact/Effort matrix (P1-P4 quadrants)
- Remediation roadmap (phases, effort estimates, ROI)
- Trend analysis (baseline comparison, regressions)

**Typical Duration**: 5-10 minutes (depends on codebase size)

---

### Pattern 2: Targeted Investigation (Specific Category)

**Use Case**: Deep-dive into one debt category (e.g., testing debt)

**When to Use**:

- Sprint planning (focus on testing debt this sprint)
- Specific pain point ("Our test coverage is too low")
- Category-specific improvement goal ("Reach 80% coverage")

**Delegation Template**:

```markdown
Task(tech-debt-investigator,
  "Investigate testing debt in packages/core/. Calculate test coverage %,
   identify untested critical paths (auth, session management), estimate
   effort to reach 80% coverage target. Prioritize tests by business impact
   (high-traffic modules first).")
```

**Context Metadata**:

```json
{
  "scope": {
    "directories": ["packages/core/"],
    "file_patterns": ["*.py"]
  },
  "business_context": {
    "critical_modules": ["auth", "session"],
    "usage_frequency": {
      "auth": "1000 req/min",
      "session": "800 req/min"
    }
  },
  "analysis_preferences": {
    "max_hotspots": 5  // Focus on top 5 untested modules
  }
}
```

**Expected Deliverables**:

- Testing debt analysis:
  - Current coverage: 62%
  - Target coverage: 80%
  - Gap: 18% (32 untested functions)
- Untested critical paths ranked by business impact
- Effort estimate to reach 80%: 48 hours (32 tests × 1.5h each)
- Prioritized test creation plan (P1 auth → P2 session → P3 utils)

**Typical Duration**: 2-3 minutes (focused scope)

---

### Pattern 3: Pre-Release Quality Gate

**Use Case**: Block release if debt regressions detected

**When to Use**:

- Every release (CI/CD integration)
- Feature branch validation (PR checks)
- Hotfix validation (ensure no new debt)

**Delegation Template**:

```markdown
Task(tech-debt-investigator,
  "Pre-release debt scan: Detect regressions vs baseline from 2025-01-15.
   BLOCK release if TDR increased >5% OR test coverage dropped >5% OR new
   hotspots introduced. Focus on changed files since last release (git diff
   main...feature-branch). Report blockers and recommendations.")
```

**Context Metadata**:

```json
{
  "scope": {
    "directories": ["packages/", "tests/"],
    "file_patterns": ["*.py"]
  },
  "baseline_data": {
    "previous_debt_score": 68.5,
    "previous_tdr": 0.09,
    "previous_sqale_grade": "C",
    "run_timestamp": "2025-01-15T10:30:00Z"
  },
  "business_context": {
    "upcoming_milestones": [
      {
        "name": "v2.0 release",
        "date": "2025-02-01",
        "quality_gate": "TDR <10%, no regressions"
      }
    ]
  }
}
```

**Expected Deliverables**:

- **Release Decision**: PASS | BLOCK
- **Regression Analysis**:
  - TDR: 0.09 → 0.11 (+2%, PASS <5% threshold)
  - Coverage: 78% → 76% (-2%, PASS <5% threshold)
  - New hotspots: 0 (PASS)
  - **Result**: PASS - No blockers detected
- **Recommendations**: 2 P2 items for next sprint (non-blocking)

**Typical Duration**: 1-2 minutes (fast, focused on deltas)

**Integration Pattern** (CI/CD):

```yaml
# .github/workflows/quality-gate.yml
- name: Technical Debt Quality Gate
  run: |
    # Orchestrator delegates to tech-debt-investigator
    # Exit code 1 if BLOCK, 0 if PASS
    uv run python scripts/quality_gate.py --baseline .claude/reports/baseline.json
```

---

### Pattern 4: Hotspot Analysis (Incident Post-Mortem)

**Use Case**: Correlate complexity, churn, and defects for incident analysis

**When to Use**:

- Post-incident analysis ("Why did auth module fail?")
- Recurring bug patterns ("payment module keeps breaking")
- Proactive risk assessment ("Which modules are most fragile?")

**Delegation Template**:

```markdown
Task(tech-debt-investigator,
  "Identify hotspots in packages/api/ correlating high churn + complexity +
   recent defects. Calculate principal (fix cost now) vs interest (ongoing cost
   if unfixed) for top 5 hotspots. Prioritize by business impact (API availability
   = 99.9% SLA). Analyze git history for churn patterns (last 6 months).")
```

**Context Metadata**:

```json
{
  "scope": {
    "directories": ["packages/api/"],
    "file_patterns": ["*.py"]
  },
  "business_context": {
    "critical_modules": ["api"],
    "usage_frequency": {
      "api": "5000 req/min"
    },
    "recent_incidents": [
      {"module": "api.endpoints", "date": "2025-01-10", "severity": "P1", "downtime": "15 min"},
      {"module": "api.auth", "date": "2025-01-08", "severity": "P2", "downtime": "5 min"},
      {"module": "api.endpoints", "date": "2024-12-20", "severity": "P1", "downtime": "30 min"}
    ]
  },
  "analysis_preferences": {
    "max_hotspots": 5
  }
}
```

**Expected Deliverables**:

**Hotspot List** (Top 5):

| Rank | Module | Churn | Complexity | Defects | Priority | Principal | Interest |
|------|--------|-------|------------|---------|----------|-----------|----------|
| 1 | api/endpoints.py | 45 | 82 | 8 | P1 | 16h | 40h/quarter |
| 2 | api/auth.py | 38 | 75 | 5 | P1 | 12h | 30h/quarter |
| 3 | api/middleware.py | 28 | 60 | 3 | P2 | 8h | 15h/quarter |
| 4 | api/serializers.py | 22 | 55 | 2 | P2 | 6h | 10h/quarter |
| 5 | api/utils.py | 18 | 45 | 1 | P3 | 4h | 5h/quarter |

**Incident Correlation**:

- `api/endpoints.py`: 2 P1 incidents (2025-01-10, 2024-12-20) correlate with high churn + complexity
- **Root Cause Hypothesis**: "Complex branching logic + frequent changes = fragile code"
- **Recommendation**: P1 refactoring (16h investment saves 40h/quarter ongoing cost)

**Principal vs Interest Analysis**:

- **Principal**: 16h to refactor `api/endpoints.py` now
- **Interest**: 40h/quarter ongoing debugging, incident response, hotfixes
- **ROI**: Break-even in 1.5 months, 3-year savings = 480h - 16h = 464h

**Typical Duration**: 3-5 minutes (git analysis + complexity calculation)

---

### Pattern 5: Sprint Planning (Quick Wins)

**Use Case**: Identify high-value, low-effort technical debt for sprint backlog

**When to Use**:

- Sprint planning meetings
- Backlog grooming
- Developer morale improvements ("Let's fix some annoying debt")

**Delegation Template**:

```markdown
Task(tech-debt-investigator,
  "Identify P1 Quick Wins (high impact, low effort <4h) in packages/ and tests/.
   Focus on code quality and testing debt categories. Exclude architectural debt
   (high effort). Generate ranked list with effort estimates and business impact.")
```

**Context Metadata**:

```json
{
  "scope": {
    "directories": ["packages/", "tests/"],
    "file_patterns": ["*.py"]
  },
  "analysis_preferences": {
    "max_hotspots": 10,
    "effort_estimation_model": "conservative",
    "prioritization_weight": {
      "business_impact": 0.3,
      "effort": 0.5,  // Emphasize low effort
      "risk": 0.1,
      "frequency": 0.1
    }
  }
}
```

**Expected Deliverables**:

**P1 Quick Wins** (High Impact, Low Effort):

| Rank | Item | Category | Impact | Effort | Description |
|------|------|----------|--------|--------|-------------|
| 1 | Add missing tests for auth | Testing | High | 2h | 3 critical paths untested |
| 2 | Extract duplicated validation | Code Quality | Medium | 3h | 12 instances of same logic |
| 3 | Update deprecated API calls | Infrastructure | High | 2h | 5 deprecated K8s APIs |
| 4 | Add docstrings to public API | Documentation | Medium | 3h | 18 functions missing docs |
| 5 | Simplify complex if-else chains | Code Quality | Medium | 3h | 4 functions >10 complexity |

**Total Effort**: 13h (1.5 sprint days)
**Total Impact**: 5 P1 items resolved, debt_score improvement ~5-8 points

**Sprint Backlog Integration**:

```markdown
User Story: Technical Debt Sprint (13h)
- Add auth module tests (2h) - @developer1
- Extract validation logic (3h) - @developer2
- Update K8s APIs (2h) - @developer1
- Add API docstrings (3h) - @developer3
- Simplify control flow (3h) - @developer2
```

**Typical Duration**: 2-3 minutes

---

## Output Structure & Interpretation

### Complete Output Example

```json
{
  "status": "SUCCESS",
  "agent": "tech-debt-investigator",
  "task_id": "debt-analysis-20250112",
  "operation_type": "full_codebase_assessment",
  "summary": "Technical debt analysis complete. debt_score: 65.2/100 (Grade C+), TDR: 0.12 (12%), SQALE Grade: C, SIG Rating: 3/5. 27 P1 items identified (8 Quick Wins). Regression detected vs baseline: debt_score +2.7 points.",
  "confidence": 0.92,
  "execution_timestamp": "2025-01-12T14:30:00Z",
  "agent_specific_output": {
    "metrics_summary": { /* See below */ },
    "category_breakdown": { /* See below */ },
    "impact_effort_matrix": { /* See below */ },
    "hotspot_list": { /* See below */ },
    "remediation_roadmap": { /* See below */ },
    "trend_analysis": { /* See below */ },
    "connection_graph": { /* See below */ },
    "stakeholder_summary": { /* See below */ }
  }
}
```

### 1. Metrics Summary

**Composite Scores**:

```json
"metrics_summary": {
  "debt_score": 65.2,            // 0-100 (higher = less debt)
  "debt_grade": "C+",            // A+ to F
  "tdr": 0.12,                   // Technical Debt Ratio (0.00-1.00)
  "tdr_percentage": "12%",       // Human-readable format
  "sqale_grade": "C",            // A-E (SQALE standard)
  "sig_star_rating": 3,          // 1-5 stars (SIG standard)
  "total_remediation_cost_hours": 480,
  "total_development_cost_hours": 4000
}
```

**Interpretation Guide**:

#### debt_score (0-100)

Composite score across 6 categories weighted by industry standards:

| Score Range | Grade | Interpretation | Urgency |
|-------------|-------|----------------|---------|
| 91-100 | A+ to A | Excellent health, minimal debt | Monitor quarterly |
| 81-90 | A- to B+ | Good health, some debt | Monitor monthly |
| 71-80 | B to B- | Moderate debt, plan sprints | Address within 2 sprints |
| 61-70 | C+ to C | Medium debt, needs attention | Address within 1 sprint |
| 51-60 | C- to D+ | High debt, quality concerns | Immediate action required |
| 0-50 | D to F | Critical debt, major issues | Emergency refactoring |

**Current Example**: 65.2 = **Grade C+** → "Medium debt, plan sprints"

#### TDR (Technical Debt Ratio)

Percentage of development time spent servicing debt:

| TDR Range | SQALE Grade | Interpretation | Business Impact |
|-----------|-------------|----------------|-----------------|
| 0-5% | A | Excellent maintainability | Minimal overhead |
| 6-10% | B | Good maintainability | Acceptable overhead |
| 11-20% | C | Moderate debt | Noticeable slowdown |
| 21-50% | D | High debt | Major productivity loss |
| >50% | E | Severe debt | Development gridlock |

**Current Example**: 0.12 (12%) = **SQALE Grade C** → "Moderate debt, noticeable slowdown"

**Business Translation**: "For every 8 hours of development, 1 hour is spent dealing with technical debt (debugging, workarounds, fragile code)."

#### SIG Star Rating (1-5)

Industry benchmarking (200+ billion LOC dataset):

| Rating | Percentile | Interpretation | Maintenance Cost Multiplier |
|--------|-----------|----------------|----------------------------|
| 5★ | Top 5% | Excellent | 1.0× (baseline) |
| 4★ | Next 30% | Above average | 1.5× |
| 3★ | Average | Industry standard | 2.0× |
| 2★ | Below average | High debt | 3.0× |
| 1★ | Bottom 5% | Critical debt | 4.0× |

**Current Example**: 3★ = **Industry Standard** → "Average maintenance costs (2× vs 5★ codebases)"

---

### 2. Category Breakdown

**6-Category Debt Analysis**:

```json
"category_breakdown": {
  "code_quality": {
    "debt_score": 58,              // 0-100 (lower = more debt in this category)
    "severity": "HIGH",            // CRITICAL | HIGH | MEDIUM | LOW | VERY_LOW
    "violation_count": 127,
    "remediation_hours": 180,
    "top_issues": [
      {
        "type": "high_complexity",
        "count": 23,
        "affected_files": ["packages/api/endpoints.py", "packages/core/utils.py"],
        "avg_complexity": 18.5,     // McCabe complexity
        "threshold": 10,
        "remediation_hours": 46
      },
      {
        "type": "code_duplication",
        "count": 15,
        "affected_files": ["packages/auth/session.py", "packages/auth/token.py"],
        "duplication_percentage": 12.5,
        "threshold": 5.0,
        "remediation_hours": 30
      }
    ]
  },
  "architecture": {
    "debt_score": 45,
    "severity": "MEDIUM",
    "violation_count": 45,
    "remediation_hours": 120,
    "top_issues": [
      {
        "type": "tight_coupling",
        "count": 12,
        "affected_modules": ["packages/api/", "packages/core/"],
        "coupling_score": 0.72,     // 0-1 (higher = tighter coupling)
        "threshold": 0.5,
        "remediation_hours": 48
      }
    ]
  },
  "testing": {
    "debt_score": 72,
    "severity": "LOW",
    "violation_count": 32,
    "remediation_hours": 64,
    "top_issues": [
      {
        "type": "low_coverage",
        "count": 32,
        "affected_files": ["packages/utils/helpers.py"],
        "coverage_percentage": 68,
        "threshold": 80,
        "missing_tests": 32,
        "remediation_hours": 48
      }
    ]
  },
  "documentation": {
    "debt_score": 80,
    "severity": "VERY_LOW",
    "violation_count": 18,
    "remediation_hours": 9,
    "top_issues": [
      {
        "type": "missing_docstrings",
        "count": 18,
        "affected_files": ["packages/api/serializers.py"],
        "remediation_hours": 9
      }
    ]
  },
  "infrastructure": {
    "debt_score": 50,
    "severity": "MEDIUM",
    "violation_count": 8,
    "remediation_hours": 32,
    "top_issues": [
      {
        "type": "deprecated_apis",
        "count": 5,
        "affected_files": ["k8s/deployments/backend.yaml"],
        "deprecated_versions": ["apps/v1beta1"],
        "remediation_hours": 16
      }
    ]
  },
  "design_ui": {
    "debt_score": null,            // Not applicable for backend projects
    "severity": "N/A",
    "violation_count": 0,
    "remediation_hours": 0
  }
}
```

**Category Priority Ranking** (by severity):

1. **Code Quality** (debt_score: 58, HIGH) → 180h remediation
2. **Architecture** (debt_score: 45, MEDIUM) → 120h remediation
3. **Infrastructure** (debt_score: 50, MEDIUM) → 32h remediation
4. **Testing** (debt_score: 72, LOW) → 64h remediation
5. **Documentation** (debt_score: 80, VERY_LOW) → 9h remediation

**Sprint Planning Guidance**:

- **This Sprint**: Address Code Quality P1 items (focus on high complexity)
- **Next Sprint**: Tackle Architecture coupling issues
- **Backlog**: Testing coverage improvements, documentation updates

---

### 3. Impact/Effort Matrix

**Prioritization Quadrants**:

```json
"impact_effort_matrix": {
  "p1_quick_wins": {
    "description": "High impact, low effort (<4h per item)",
    "count": 8,
    "total_effort_hours": 24,
    "items": [
      {
        "rank": 1,
        "title": "Add missing tests for auth module",
        "category": "Testing",
        "business_impact": "High",
        "effort_hours": 2,
        "affected_files": ["packages/auth/session.py"],
        "rationale": "Critical path untested, high traffic (1000 req/min)",
        "roi_months": 0.5
      },
      {
        "rank": 2,
        "title": "Extract duplicated validation logic",
        "category": "Code Quality",
        "business_impact": "Medium",
        "effort_hours": 3,
        "affected_files": ["packages/api/validators.py"],
        "rationale": "12 instances of same logic, high churn area",
        "roi_months": 1.0
      }
    ]
  },
  "p2_strategic": {
    "description": "High impact, high effort (>4h per item)",
    "count": 5,
    "total_effort_hours": 80,
    "items": [
      {
        "rank": 1,
        "title": "Refactor api/endpoints.py (complexity: 82)",
        "category": "Code Quality",
        "business_impact": "High",
        "effort_hours": 16,
        "affected_files": ["packages/api/endpoints.py"],
        "rationale": "Hotspot: 45 commits, 8 defects, 82 complexity",
        "roi_months": 1.5
      }
    ]
  },
  "p3_defer": {
    "description": "Low impact, high effort",
    "count": 12,
    "total_effort_hours": 120,
    "items": [
      {
        "rank": 1,
        "title": "Modernize legacy batch processing",
        "category": "Architecture",
        "business_impact": "Low",
        "effort_hours": 24,
        "affected_files": ["packages/batch/"],
        "rationale": "Low traffic (10 req/day), stable, no incidents",
        "roi_months": 18.0
      }
    ]
  },
  "p4_opportunistic": {
    "description": "Low impact, low effort (nice-to-have)",
    "count": 3,
    "total_effort_hours": 6,
    "items": [
      {
        "rank": 1,
        "title": "Update copyright headers",
        "category": "Documentation",
        "business_impact": "Low",
        "effort_hours": 2,
        "affected_files": ["packages/**/*.py"],
        "rationale": "Outdated headers, legal compliance",
        "roi_months": null
      }
    ]
  }
}
```

**Prioritization Visualization**:

```text
Impact
  ↑
  │  P2 Strategic        │  P1 Quick Wins
  │  (5 items, 80h)      │  (8 items, 24h)
  │  ───────────────────────────────────
  │  P3 Defer            │  P4 Opportunistic
  │  (12 items, 120h)    │  (3 items, 6h)
  └───────────────────────────────────→ Effort
```

**Sprint Planning Strategy**:

1. **This Sprint** (2 weeks, 80h capacity):
   - ALL P1 Quick Wins (24h) → Deliver 8 wins fast
   - TOP 3 P2 Strategic (48h) → Address critical hotspots
   - **Total**: 72h, 11 items resolved

2. **Next Sprint**:
   - Remaining P2 Strategic (32h)
   - P4 Opportunistic (6h)

3. **Backlog**:
   - P3 Defer (revisit quarterly)

---

### 4. Hotspot List

**Top 10 High-Risk Modules** (churn × complexity × defects):

```json
"hotspot_list": {
  "methodology": "Hotspot Score = (churn × 0.4) + (complexity × 0.3) + (defects × 0.3)",
  "timeframe": "Last 6 months",
  "hotspots": [
    {
      "rank": 1,
      "file": "packages/api/endpoints.py",
      "hotspot_score": 87.5,
      "churn": 45,                    // Commits in 6 months
      "complexity": 82,               // McCabe cyclomatic complexity
      "defects": 8,                   // Bugs fixed in 6 months
      "ownership_dispersion": "High", // 8 contributors, <10% each
      "business_criticality": "High", // API: 5000 req/min
      "principal_cost_hours": 16,     // Fix cost now
      "interest_cost_hours_per_quarter": 40,  // Ongoing cost if unfixed
      "roi_months": 1.5,
      "recent_incidents": [
        {"date": "2025-01-10", "severity": "P1", "downtime": "15 min"},
        {"date": "2024-12-20", "severity": "P1", "downtime": "30 min"}
      ],
      "recommendation": "P1 refactoring - High churn + complexity + incidents = critical risk"
    },
    {
      "rank": 2,
      "file": "packages/auth/session.py",
      "hotspot_score": 78.2,
      "churn": 38,
      "complexity": 75,
      "defects": 5,
      "ownership_dispersion": "Medium",
      "business_criticality": "High",
      "principal_cost_hours": 12,
      "interest_cost_hours_per_quarter": 30,
      "roi_months": 1.8,
      "recent_incidents": [
        {"date": "2025-01-08", "severity": "P2", "downtime": "5 min"}
      ],
      "recommendation": "P1 refactoring - Auth critical path, reduce complexity"
    }
  ]
}
```

**Hotspot Interpretation**:

#### Rank 1: packages/api/endpoints.py

- **Why it's a hotspot**:
  - **High Churn** (45 commits): Changed frequently → fragile
  - **High Complexity** (82): Hard to understand → error-prone
  - **High Defects** (8 bugs): Proven track record of failures
  - **High Ownership Dispersion**: 8 contributors → no clear owner → low quality
  - **Business Critical**: 5000 req/min traffic → downtime = revenue loss

- **Cost Analysis**:
  - **Principal**: 16h to refactor now
  - **Interest**: 40h/quarter ongoing debugging, incident response
  - **ROI**: Break-even in 1.5 months, 3-year savings = 464h

- **Recommendation**: **P1 URGENT** - Refactor immediately to prevent future incidents

#### Rank 2: packages/auth/session.py

- **Why it's a hotspot**: Similar pattern but lower defect count
- **Recommendation**: **P1** - Schedule after endpoints.py, still critical

---

### 5. Remediation Roadmap

**Phased Action Plan**:

```json
"remediation_roadmap": {
  "phase_1": {
    "name": "Sprint 1-2: Quick Wins + Critical Hotspots",
    "duration_weeks": 4,
    "effort_hours": 104,
    "items": [
      {
        "priority": "P1",
        "title": "Refactor api/endpoints.py",
        "category": "Code Quality",
        "effort_hours": 16,
        "assigned_sprint": "Sprint 1",
        "acceptance_criteria": [
          "Cyclomatic complexity reduced from 82 to <10 per function",
          "Extract 5 helper functions",
          "Unit test coverage >80%",
          "No P1/P2 linting violations"
        ],
        "success_metrics": [
          "debt_score improvement: +5 points",
          "TDR reduction: -2%",
          "Incident rate reduction: -50% (projected)"
        ]
      },
      {
        "priority": "P1",
        "title": "Add missing auth tests (8 items)",
        "category": "Testing",
        "effort_hours": 24,
        "assigned_sprint": "Sprint 1-2",
        "acceptance_criteria": [
          "32 new unit tests added",
          "Auth module coverage: 68% → 85%",
          "All critical paths covered"
        ]
      }
    ],
    "expected_impact": {
      "debt_score_improvement": "+8 points (65.2 → 73.2)",
      "tdr_reduction": "-3% (12% → 9%)",
      "sqale_grade_improvement": "C → B",
      "hotspots_resolved": 2
    }
  },
  "phase_2": {
    "name": "Sprint 3-5: Strategic Refactoring",
    "duration_weeks": 6,
    "effort_hours": 160,
    "items": [
      {
        "priority": "P2",
        "title": "Decouple api/ and core/ modules",
        "category": "Architecture",
        "effort_hours": 48
      }
    ],
    "expected_impact": {
      "debt_score_improvement": "+5 points (73.2 → 78.2)",
      "tdr_reduction": "-2% (9% → 7%)",
      "sqale_grade_improvement": "B (maintained)"
    }
  },
  "phase_3": {
    "name": "Backlog: Low-Priority Improvements",
    "duration_weeks": null,
    "effort_hours": 126,
    "items": [
      {
        "priority": "P3",
        "title": "Modernize legacy batch processing",
        "category": "Architecture",
        "effort_hours": 24
      }
    ]
  },
  "summary": {
    "total_effort_hours": 390,
    "total_duration_weeks": 10,
    "total_debt_reduction": {
      "debt_score": "+13 points (65.2 → 78.2)",
      "tdr": "-5% (12% → 7%)",
      "sqale_grade": "C → B"
    },
    "roi_analysis": {
      "investment_hours": 390,
      "annual_savings_hours": 520,  // Reduced debugging, incident response
      "break_even_months": 9,
      "3_year_roi": "333% (1040h saved - 390h invested)"
    }
  }
}
```

**Roadmap Visualization**:

```text
Timeline: 10 weeks (2.5 months)

Sprint 1-2 (4 weeks, 104h)
├─ Refactor api/endpoints.py (P1, 16h)
├─ Add auth tests (P1, 24h)
├─ Extract duplicated validation (P1, 3h)
└─ Update deprecated APIs (P1, 2h)
   → debt_score: 65.2 → 73.2 (+8 points)

Sprint 3-5 (6 weeks, 160h)
├─ Decouple api/core modules (P2, 48h)
├─ Refactor auth/session.py (P2, 12h)
└─ Testing coverage improvements (P2, 32h)
   → debt_score: 73.2 → 78.2 (+5 points)

Backlog (126h, revisit quarterly)
└─ P3 items (low priority)
```

---

### 6. Trend Analysis

**Baseline Comparison** (if baseline provided):

```json
"trend_analysis": {
  "baseline": {
    "debt_score": 62.5,
    "tdr": 0.08,
    "sqale_grade": "C",
    "sig_rating": 3,
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "current": {
    "debt_score": 65.2,
    "tdr": 0.12,
    "sqale_grade": "C",
    "sig_rating": 3,
    "timestamp": "2025-01-12T14:30:00Z"
  },
  "deltas": {
    "debt_score_change": +2.7,          // Improved (higher = better)
    "debt_score_change_percentage": "+4.3%",
    "tdr_change": +0.04,                // Regressed (higher = worse)
    "tdr_change_percentage": "+50%",
    "sqale_grade_change": 0,            // Unchanged
    "sig_rating_change": 0              // Unchanged
  },
  "trajectory": "MIXED",                // IMPROVING | STABLE | WORSENING | MIXED
  "regressions_detected": [
    {
      "metric": "tdr",
      "severity": "HIGH",
      "change": "+50% (0.08 → 0.12)",
      "threshold_exceeded": true,
      "threshold": "5% increase",
      "root_causes": [
        "New hotspots introduced in api/ module (3 files)",
        "Test coverage dropped 5% (78% → 73%)",
        "15 new high-complexity functions added"
      ],
      "recommendation": "BLOCK release - TDR regression exceeds 5% threshold"
    }
  ],
  "improvements": [
    {
      "metric": "debt_score",
      "change": "+2.7 points (+4.3%)",
      "contributors": [
        "Documentation debt reduced (18 docstrings added)",
        "Infrastructure debt reduced (5 deprecated APIs updated)"
      ]
    }
  ],
  "new_hotspots": [
    {
      "file": "packages/api/new_endpoints.py",
      "hotspot_score": 65.0,
      "introduced_date": "2025-01-10",
      "reason": "High complexity (75) + no tests"
    }
  ]
}
```

**Trend Interpretation**:

**Overall Trajectory**: MIXED (debt_score improved, TDR regressed)

**Positive Changes**:

- debt_score: 62.5 → 65.2 (+2.7 points, +4.3%) ✅
- Documentation debt reduced (18 docstrings)
- Infrastructure debt reduced (5 API updates)

**Negative Changes (REGRESSIONS)**:

- TDR: 0.08 → 0.12 (+0.04, +50%) ❌ **CRITICAL**
  - **Threshold Exceeded**: >5% increase
  - **Root Causes**:
    1. New hotspots (3 files in api/)
    2. Test coverage drop (78% → 73%)
    3. 15 new high-complexity functions
  - **Recommendation**: **BLOCK RELEASE** until TDR <10%

**Action Required**: Address TDR regression before release (Sprint 1 priority)

---

### 7. Connection Graph (Hotspot Relationships)

**Visual Representation** (ASCII format):

```json
"connection_graph": {
  "description": "Hotspot dependency graph showing debt relationships",
  "nodes": [
    {
      "id": "api_endpoints",
      "file": "packages/api/endpoints.py",
      "hotspot_score": 87.5,
      "node_type": "hotspot"
    },
    {
      "id": "auth_session",
      "file": "packages/auth/session.py",
      "hotspot_score": 78.2,
      "node_type": "hotspot"
    },
    {
      "id": "core_utils",
      "file": "packages/core/utils.py",
      "hotspot_score": 65.0,
      "node_type": "hotspot"
    }
  ],
  "edges": [
    {
      "source": "api_endpoints",
      "target": "auth_session",
      "relationship": "tight_coupling",
      "strength": 0.85,              // 0-1 (higher = stronger coupling)
      "description": "api/endpoints.py imports 12 functions from auth/session.py"
    },
    {
      "source": "api_endpoints",
      "target": "core_utils",
      "relationship": "shared_defect_pattern",
      "strength": 0.72,
      "description": "Both files have similar null-check bugs (5 instances each)"
    }
  ],
  "insights": [
    "api_endpoints and auth_session are tightly coupled (0.85) - refactor together",
    "Shared defect pattern suggests systemic issue (null-check validation)"
  ]
}
```

**ASCII Visualization**:

```text
Hotspot Dependency Graph

  api/endpoints.py (87.5)
      ↓ (tight_coupling: 0.85)
  auth/session.py (78.2)

  api/endpoints.py (87.5)
      ↓ (shared_defect: 0.72)
  core/utils.py (65.0)
```

**Insights**:

1. **Tight Coupling** (api ↔ auth): Refactor together (not separately)
2. **Shared Defect Pattern**: Systemic null-check issue → Need codebase-wide fix

---

### 8. Stakeholder Summary (Executive Report)

**Executive-Friendly Health Assessment**:

```json
"stakeholder_summary": {
  "executive_summary": "Codebase health: MODERATE (Grade C+). Technical debt is manageable but requires attention. 2 critical hotspots identified with high incident risk. Recommended investment: 104 hours (Sprint 1-2) to address 8 P1 items and reduce TDR from 12% to 9%. ROI: Break-even in 9 months, 3-year savings of 464 hours.",
  "key_findings": [
    "Code Quality debt is HIGH (debt_score: 58) - 23 complex functions need refactoring",
    "2 critical hotspots (api/endpoints.py, auth/session.py) correlate with recent P1 incidents",
    "TDR increased 50% (8% → 12%) since last run - regression detected",
    "Testing coverage adequate (72%) but 32 missing tests for critical paths"
  ],
  "business_impact": {
    "current_state": "12% of development time spent on technical debt (debugging, incidents)",
    "risk_assessment": "2 high-risk modules (api, auth) with recent P1 incidents (45 min downtime)",
    "projected_improvement": "Phase 1 investment (104h) reduces TDR to 9%, incident risk by 50%"
  },
  "top_3_recommendations": [
    {
      "rank": 1,
      "title": "Refactor api/endpoints.py (P1 URGENT)",
      "effort": "16 hours",
      "impact": "Reduces incident risk by 50%, prevents estimated 40h/quarter debugging",
      "urgency": "Immediate - 2 P1 incidents in last month"
    },
    {
      "rank": 2,
      "title": "Add missing auth tests (P1)",
      "effort": "24 hours",
      "impact": "Increases auth coverage 68% → 85%, prevents auth-related incidents",
      "urgency": "Sprint 1-2"
    },
    {
      "rank": 3,
      "title": "Address TDR regression (12%)",
      "effort": "104 hours (Phase 1)",
      "impact": "Reduces TDR to 9%, improves SQALE grade C → B",
      "urgency": "Block release until TDR <10%"
    }
  ],
  "resource_requirements": {
    "phase_1": "2 developers × 4 weeks (Sprint 1-2)",
    "phase_2": "1 developer × 6 weeks (Sprint 3-5)",
    "total_investment": "390 hours over 10 weeks"
  },
  "roi_summary": {
    "investment": "390 hours",
    "annual_savings": "520 hours (reduced debugging, incidents, maintenance)",
    "break_even": "9 months",
    "3_year_roi": "333% (1040h saved - 390h invested)"
  }
}
```

**Key Messages for Stakeholders**:

1. **Current State**: "Codebase is Grade C+ (moderate debt). 12% of development time spent on technical debt."

2. **Risk**: "2 critical hotspots with P1 incidents (45 min downtime last month). High risk of future incidents."

3. **Recommendation**: "Invest 104 hours (2 sprints) to address 8 P1 items. Reduces TDR 12% → 9%, incident risk by 50%."

4. **ROI**: "Break-even in 9 months. 3-year savings: 1040 hours (520h/year ongoing). 333% ROI."

5. **Urgency**: "BLOCK RELEASE until TDR <10% (quality gate threshold)."

---

## Best Practices

### 1. Always Provide Baseline Data

**Why**: Enables regression detection and trend tracking

**How**: Save each run's output to `.claude/reports/tech-debt-YYYY-MM-DD.json`

**Example**:

```bash
# First run (establish baseline)
Task(tech-debt-investigator, "Full health assessment")
# Save output → .claude/reports/tech-debt-2025-01-15.json

# Second run (detect regressions)
Task(tech-debt-investigator, "Full health assessment with baseline from 2025-01-15")
# Compare: TDR 0.08 → 0.12 (+50%, REGRESSION DETECTED)
```

**Benefits**:

- Detect regressions early (TDR +5% = block release)
- Track improvement trends (debt_score +10 points = success)
- Measure ROI (effort invested vs TDR reduction)

---

### 2. Specify Business Context

**Why**: Prioritize debt by business impact, not just technical severity

**How**: Provide `critical_modules`, `usage_frequency`, `recent_incidents`

**Example**:

```json
"business_context": {
  "critical_modules": ["auth", "payment"],
  "usage_frequency": {
    "auth": "1000 req/min",      // High priority
    "batch": "10 req/day"         // Low priority
  },
  "recent_incidents": [
    {"module": "auth", "severity": "P1"}
  ]
}
```

**Benefits**:

- Hotspots weighted by business criticality (auth incidents = P1 priority)
- ROI calculations consider revenue impact (downtime cost)
- Sprint planning aligns with business goals

---

### 3. Use Targeted Scopes

**Why**: Faster analysis, focused results

**How**: Specify `directories` and `file_patterns` precisely

**Examples**:

```json
// ❌ BAD: Entire codebase (slow, noisy)
"scope": {
  "directories": ["./"]
}

// ✅ GOOD: Targeted scope (fast, actionable)
"scope": {
  "directories": ["packages/api/"],
  "file_patterns": ["*.py"]
}

// ✅ GOOD: Changed files only (pre-release gate)
"scope": {
  "directories": ["packages/", "tests/"],
  "file_patterns": ["*.py"],
  "exclusions": [".venv/", "__pycache__/"]
}
```

**Duration Comparison**:

- Full codebase: 5-10 minutes
- Targeted module: 1-2 minutes
- Changed files only: 30-60 seconds

---

### 4. Set Clear Objectives

**Why**: Focused delegation = better output quality

**How**: Delegation prompt should specify:

- What to analyze (scope)
- What to calculate (debt_score, TDR, hotspots)
- What to deliver (remediation roadmap, P1 items)

**Examples**:

```markdown
// ❌ BAD: Vague delegation
Task(tech-debt-investigator, "Analyze technical debt")

// ✅ GOOD: Specific delegation
Task(tech-debt-investigator,
  "Analyze technical debt in packages/api/. Calculate debt_score, TDR,
   identify top 5 hotspots, generate Impact/Effort matrix with P1 Quick Wins.
   Focus on Code Quality and Testing categories.")
```

---

### 5. Integrate with CI/CD (Pre-Release Gates)

**Why**: Prevent debt regressions from reaching production

**How**: Run tech-debt-investigator in GitHub Actions, block merge if regressions detected

**Example Workflow**:

```yaml
# .github/workflows/quality-gate.yml
name: Technical Debt Quality Gate

on:
  pull_request:
    branches: [main]

jobs:
  debt-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Load Baseline
        run: |
          curl -o baseline.json \
            https://github.com/repo/reports/tech-debt-baseline.json

      - name: Run Technical Debt Analysis
        run: |
          # Orchestrator delegates to tech-debt-investigator
          uv run python scripts/quality_gate.py \
            --baseline baseline.json \
            --threshold "TDR <10%, no new hotspots"

      - name: Block Merge if Regressions Detected
        run: |
          # Exit code 1 = BLOCK, 0 = PASS
          if [ $? -ne 0 ]; then
            echo "❌ Quality gate FAILED: Regressions detected"
            exit 1
          fi
```

**Benefits**:

- Automated debt regression detection (no manual reviews)
- Block merges with TDR regressions (enforce quality gates)
- Track debt trends over time (baseline history)

---

### 6. Schedule Regular Audits

**Why**: Prevent debt accumulation, maintain health trends

**How**: Quarterly full audits, monthly targeted scans

**Recommended Schedule**:

| Frequency | Scope | Purpose |
|-----------|-------|---------|
| **Quarterly** | Full codebase | Comprehensive health audit, executive reporting |
| **Monthly** | Critical modules | Monitor hotspots, track improvements |
| **Per PR** | Changed files | Prevent debt regressions |
| **Pre-release** | Full codebase | Quality gate (TDR <10%) |

**Example Calendar**:

```text
Q1 2025:
- Week 1: Full audit (baseline establishment)
- Week 5: Critical modules scan (api, auth, payment)
- Week 9: Critical modules scan
- Week 13: Pre-release quality gate (v2.0)

Q2 2025:
- Week 14: Full audit (quarterly review)
- ... repeat monthly scans
```

---

### 7. Use Effort Estimation Models

**Why**: Accurate sprint planning, realistic roadmaps

**How**: Choose estimation model based on team velocity

**Models**:

| Model | Multiplier | Use Case |
|-------|-----------|----------|
| **Conservative** | 1.5× industry | New teams, complex codebases, high uncertainty |
| **Standard** | 1.0× industry | Experienced teams, typical codebases |
| **Aggressive** | 0.75× industry | Expert teams, simple codebases, well-understood debt |

**Example**:

```json
"analysis_preferences": {
  "effort_estimation_model": "conservative"
}
```

**Impact**:

- Conservative: "Refactor endpoints.py: 24h" (1.5× 16h standard)
- Standard: "Refactor endpoints.py: 16h"
- Aggressive: "Refactor endpoints.py: 12h" (0.75× 16h standard)

**Recommendation**: Start with **conservative**, adjust based on actual sprint velocity

---

### 8. Prioritize by ROI

**Why**: Maximize business value per hour invested

**How**: Focus on high ROI items (short break-even, high savings)

**ROI Calculation**:

```text
ROI = (Annual Savings - Investment) / Investment × 100%

Where:
- Annual Savings = Interest Cost × 4 quarters
- Investment = Principal Cost
```

**Example**:

```text
Item: Refactor api/endpoints.py
- Principal: 16h (fix cost now)
- Interest: 40h/quarter (ongoing cost if unfixed)
- Annual Savings: 40h × 4 = 160h
- Break-even: 16h / 40h = 0.4 quarters (1.5 months)
- 3-year ROI: ((160h × 3) - 16h) / 16h × 100% = 2900%
```

**Prioritization**:

1. **High ROI** (>500%, <3 month break-even) → P1 priority
2. **Medium ROI** (200-500%, 3-6 month break-even) → P2 priority
3. **Low ROI** (<200%, >6 month break-even) → P3 defer

---

### 9. Communicate Findings to Stakeholders

**Why**: Secure buy-in, justify refactoring investment

**How**: Use stakeholder summary (executive-friendly format)

**Key Messages**:

1. **Current State**: "Grade C+ (moderate debt), 12% of dev time = debt servicing"
2. **Risk**: "2 critical hotspots with P1 incidents (45 min downtime)"
3. **Investment**: "104 hours (2 sprints) to address 8 P1 items"
4. **ROI**: "Break-even in 9 months, 3-year savings: 1040 hours (333% ROI)"
5. **Urgency**: "BLOCK RELEASE until TDR <10%"

**Presentation Format**:

```markdown
# Technical Debt Executive Summary

**Current Health**: Grade C+ (Moderate Debt)
- 12% of development time spent on technical debt
- 2 critical hotspots with recent P1 incidents (45 min downtime)

**Recommended Investment**: 104 hours (2 sprints)
- Address 8 P1 items (Quick Wins + Critical Hotspots)
- Reduce TDR from 12% → 9%
- Improve SQALE grade C → B

**ROI**: 333% (3-year)
- Break-even: 9 months
- Annual savings: 520 hours (reduced debugging, incidents)

**Action Required**: BLOCK v2.0 release until TDR <10% (quality gate)
```

---

### 10. Iterate and Track Progress

**Why**: Validate remediation efforts, measure improvement

**How**: Run iterative analyses after each sprint

**Example Iteration Cycle**:

```text
Week 1: Baseline analysis
- debt_score: 65.2, TDR: 0.12
- 8 P1 items identified

Sprint 1-2: Address P1 items (104h)
- Refactor api/endpoints.py (16h)
- Add auth tests (24h)
- Extract validation logic (3h)

Week 9: Re-analysis
- debt_score: 73.2 (+8 points, SUCCESS)
- TDR: 0.09 (-3%, SUCCESS)
- 5 P1 items resolved, 3 new P2 items

Sprint 3-5: Continue Phase 2
- [... continue remediation ...]
```

**Iteration Benefits**:

- Validate effort estimates (actual vs predicted)
- Track debt trajectory (improving/stable/worsening)
- Adjust priorities based on new findings

---

## Related Documentation

### Agent Definition & Schema

- **Agent Definition**: `.claude/agents/tech-debt-investigator.md`
  - Full capabilities, permissions, reasoning approach
  - OODA loop workflow (Observe → Orient → Decide → Act)
  - Base agent pattern inheritance

- **Schema**: `.claude/docs/schemas/tech-debt-investigator.schema.json`
  - Input/output contract validation
  - SUCCESS/FAILURE state model
  - agent_specific_output structure

### Frameworks & Methodologies

- **Technical Debt Frameworks**: `.claude/docs/00-core/technical-debt-frameworks.md`
  - SQALE methodology (remediation cost approach)
  - SIG maintainability model (benchmark-driven)
  - Quantitative metrics & thresholds (complexity, duplication, coverage)
  - Git-based historical analysis (churn, ownership, defects)

- **Debt Category Taxonomy**: Same document, Section 1
  - 6-category orthogonal classification (Code Quality, Architecture, Testing, Documentation, Infrastructure, Design/UI)
  - Violation types and examples per category

### Orchestration & Workflows

- **Orchestrator Workflow**: `.claude/docs/03-workflows/orchestrator-workflow.md`
  - Agent selection process (when to delegate to tech-debt-investigator)
  - Multi-agent coordination patterns
  - Result synthesis and recommendation framework

- **Agent Selection Guide**: `.claude/docs/01-guides/agents/agent-selection-guide.md`
  - Domain-first thinking (packages/** → tech-debt-investigator for code health)
  - Confidence scoring and delegation thresholds

### Integration Guides

- **Pre-Release Quality Gates**: `docs/04-guides/quality/pre-release-checklist.md` (if exists)
  - CI/CD integration patterns
  - Quality gate thresholds and blocking criteria

- **Sprint Planning Integration**: `docs/04-guides/planning/sprint-planning-guide.md` (if exists)
  - Using Impact/Effort matrix for backlog grooming
  - Velocity-based capacity planning

- **ROI Analysis Methods**: `docs/04-guides/quality/technical-debt-roi.md` (if exists)
  - Principal vs Interest calculation methodology
  - Break-even analysis formulas

---

## Appendix: Quick Reference

### Context Metadata Quick Template

```json
{
  "scope": {"directories": ["packages/"], "file_patterns": ["*.py"]},
  "baseline_data": {"previous_debt_score": 62.5, "previous_tdr": 0.08, "run_timestamp": "2025-01-15T10:30:00Z"},
  "business_context": {"critical_modules": ["auth", "payment"], "usage_frequency": {"auth": "1000 req/min"}},
  "analysis_preferences": {"max_hotspots": 10, "effort_estimation_model": "conservative"}
}
```

### Delegation Quick Template

```markdown
Task(tech-debt-investigator,
  "Analyze technical debt in [scope]. Calculate debt_score, TDR, identify
   top [N] hotspots, generate Impact/Effort matrix with remediation roadmap.
   [Optional: Compare to baseline from YYYY-MM-DD.]")
```

### Output Interpretation Quick Reference

| Metric | Range | Good | Concern | Critical |
|--------|-------|------|---------|----------|
| **debt_score** | 0-100 | >80 (B+) | 60-80 (C) | <60 (D) |
| **TDR** | 0-100% | <5% (A) | 5-10% (B) | >10% (C-E) |
| **SQALE Grade** | A-E | A-B | C | D-E |
| **SIG Rating** | 1-5★ | 4-5★ | 3★ | 1-2★ |
| **Complexity** | per function | <10 | 10-20 | >20 |
| **Duplication** | % of codebase | <5% | 5-10% | >10% |
| **Coverage** | % of code tested | >80% | 60-80% | <60% |

### Prioritization Quick Reference

| Quadrant | Impact | Effort | Action |
|----------|--------|--------|--------|
| **P1 Quick Wins** | High | Low (<4h) | Do immediately |
| **P2 Strategic** | High | High (>4h) | Plan sprints |
| **P3 Defer** | Low | High | Backlog (revisit quarterly) |
| **P4 Opportunistic** | Low | Low | When convenient |

### ROI Quick Calculation

```text
Break-even (months) = Principal Cost / (Interest Cost per quarter / 3)
3-year ROI = ((Interest × 12 quarters) - Principal) / Principal × 100%
```

---

**Version**: 1.0.0
**Last Updated**: 2025-11-12
**Maintainer**: Claude Code (orchestrator)
**Feedback**: Report issues to `.claude/docs/FEEDBACK.md`

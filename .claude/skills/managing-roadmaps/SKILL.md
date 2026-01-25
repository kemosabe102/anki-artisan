---
name: managing-roadmaps
description: >
  TACTICAL sprint-level roadmap operations: tracking sprint capacity (3+2 streams), 
  executing sprint transitions, comparing features for overlap, calculating 6D health metrics,
  and managing day-to-day roadmap status updates.
  NOT for: stage assessment or maturity evaluation (use roadmap-lifecycle),
  effort estimation (use estimating-and-tracking), risk tracking (use managing-project-risks).
  Keywords: sprint progress, capacity tracking, health metrics, feature overlap, roadmap update.
---

# Managing Roadmaps

Self-contained knowledge for roadmap lifecycle management, sprint capacity tracking, and feature overlap analysis.

---

## Contents

1. [Sprint Capacity Model](#sprint-capacity-model)
2. [7 Roadmap Operations](#7-roadmap-operations)
3. [6D Health Scoring](#6d-health-scoring)
4. [Sprint Transition Workflow](#sprint-transition-workflow)
5. [Cross-Reference Validation](#cross-reference-validation)
6. [Feature Overlap Analysis](#feature-overlap-analysis)
7. [5 Whys Adjustment Logic](#5-whys-adjustment-logic)
8. [AI Documentation Best Practices](#ai-documentation-best-practices)
9. [Progressive Disclosure Guidelines](#progressive-disclosure-guidelines)
10. [Token Density Optimization](#token-density-optimization)
11. [Anti-Patterns](#anti-patterns-never-do)
12. [Error Recovery](#error-recovery)
13. [Quick Reference](#quick-reference)

---

## Sprint Capacity Model

**The 3+2 streams model defines sprint capacity constraints.**

### Stream Configuration
| Stream Type | Count | Hours Each | Purpose |
|-------------|-------|------------|---------|
| Large Streams | 3 | 10-20 hours | Feature development, major enhancements |
| Small Streams | 2 | <5 hours | Bug fixes, quick wins, documentation |
| **Total Capacity** | 5 | ~37 hours | Per sprint (1 developer, parallel execution) |

### Capacity Validation Rules
1. Count large streams: must be <=3
2. Count small streams: must be <=2
3. Sum total hours: must be <=40
4. Validate complexity compliance

### Compliance Output Example
```json
{
  "capacity_status": {
    "large_streams": {"count": 3, "max": 3, "hours": 32, "compliance": "Within capacity"},
    "small_streams": {"count": 2, "max": 2, "hours": 5, "compliance": "Within capacity"},
    "total_hours": 37,
    "in_progress_complexity": 15
  }
}
```

---

## 7 Roadmap Operations

| # | Operation | Confidence | Description |
|---|-----------|------------|-------------|
| 1 | `update_roadmap_status` | 0.95 | Update phase completion, feature milestones, overall status |
| 2 | `manage_sprint_progress` | 0.92 | Track stream status, validate capacity, detect completion |
| 3 | `apply_ai_best_practices` | 0.88 | Optimize token density, progressive disclosure, structure |
| 4 | `automate_sprint_transition` | 0.87 | Archive completed sprint, reset LIVING_SPRINT, activate next |
| 5 | `validate_cross_references` | 0.85 | Scan all roadmaps, detect broken links, report inconsistencies |
| 6 | `generate_health_metrics` | 0.82 | Calculate 6D health score, rank improvement opportunities |
| 7 | `create_roadmap` | 0.88 | Select template, populate, validate structure |

### Operation 1: Update Roadmap Status
**Input**: Target roadmap path, status update type, completion data
**Steps**:
1. Read target roadmap file to verify current state
2. Identify status update requirements (phase completion, feature milestones)
3. Use edit_block with exact old/new string replacements
4. Validate changes applied correctly (read-back verification)
5. Update cross-referenced documents (LIVING_SPRINT, SPRINT-ROADMAP)

### Operation 2: Manage Sprint Progress
**Input**: Sprint update type, stream identifiers, complexity data
**Steps**:
1. Read LIVING_SPRINT.md to assess current sprint state
2. Identify stream status changes (completions, new starts)
3. Calculate complexity points for in-progress work
4. Validate against capacity model (3+2 streams, ~37h total)
5. Execute updates and validate changes
6. Alert if capacity exceeded or sprint complete

### Operation 3: Apply AI Best Practices
**Input**: Target roadmap file path, optimization focus
**Steps**:
1. Read roadmap file, calculate current token density
2. Assess structure compliance, identify optimization opportunities
3. Reference progressive disclosure and token density techniques
4. Apply optimizations incrementally, validate after each change
5. Measure token reduction, verify semantic preservation

### Operation 4: Automate Sprint Transition
**Input**: Sprint completion signal, next sprint details
**Phases**: See [Sprint Transition Workflow](#sprint-transition-workflow)

### Operation 5: Validate Cross-References
**Input**: Validation scope, repair mode (report-only or auto-fix)
**Categories**: See [Cross-Reference Validation](#cross-reference-validation)

### Operation 6: Generate Health Metrics
**Input**: Metrics scope, trend analysis period
**Formula**: See [6D Health Scoring](#6d-health-scoring)

### Operation 7: Create Roadmap
**Input**: Template type (quarterly, sprint, feature), target path
**Steps**:
1. Select appropriate template
2. Populate with provided metadata
3. Validate structure compliance
4. Check for roadmap conflicts (file already exists)

---

## 6D Health Scoring

**Calculate documentation health across 6 dimensions.**

### Health Formula
```
Health = (PD × 0.25) + (Token × 0.20) + (XRef × 0.20) + (Sprint × 0.15) + (Fresh × 0.10) + (Complete × 0.10)
```

### Dimension Definitions
| Dimension | Weight | Target | Measurement |
|-----------|--------|--------|-------------|
| Progressive Disclosure (PD) | 0.25 | <500 lines | Line count, hierarchical structure, size efficiency |
| Token Density | 0.20 | <4% filler | Filler word ratio, active voice %, structured format usage |
| Cross-Reference Integrity (XRef) | 0.20 | 0 broken | Broken links, orphaned items, consistency errors |
| Sprint Compliance | 0.15 | 3+2 model | Capacity adherence, complexity tracking, completion velocity |
| Freshness | 0.10 | <30 days | Last updated timestamps, stale document detection |
| Completeness | 0.10 | 100% fields | Required fields present (status, dates, owners) |

### Score Interpretation
| Range | Rating | Action Required |
|-------|--------|-----------------|
| 0.90-1.00 | Excellent | Minimal improvements needed |
| 0.80-0.89 | Good | Minor optimization opportunities |
| 0.70-0.79 | Fair | Moderate improvements recommended |
| 0.60-0.69 | Poor | Major restructuring needed |
| <0.60 | Critical | Immediate attention required |

---

## Sprint Transition Workflow

**6-phase workflow for transitioning between sprints.**

### Phase Sequence
| Phase | Name | Validation Gate |
|-------|------|-----------------|
| 1 | Completion Detection | All 5 streams marked COMPLETE, 0 in-progress complexity |
| 2 | Archive Creation | SPRINT-ARCHIVE-{N}.md created with completed work summary |
| 3 | LIVING_SPRINT Reset | IN PROGRESS section cleared, new sprint number |
| 4 | Next Sprint Activation | SPRINT-ROADMAP.md updated with next sprint details |
| 5 | Cross-Reference Update | All roadmap files synced with sprint changes |
| 6 | Validation | All transition gates validated successfully |

### Transition Detection Criteria
- All streams marked COMPLETE
- Capacity reset to 0
- No pending blockers
- Sprint duration elapsed

### Archive File Structure
```markdown
# Sprint Archive: Sprint {N}

## Summary
- Duration: {days} days
- Streams Completed: 5
- Total Hours: {hours}

## Completed Streams
- [Stream details...]

## Lessons Learned
- [Velocity insights...]
```

---

## Cross-Reference Validation

**Validate references between roadmap ecosystem documents.**

### Validation Scope
- LIVING_SPRINT.md <-> SPRINT-ROADMAP.md <-> roadmaps/**/*.md
- Feature plan references (docs/01-planning/features/**)
- Specification links (docs/01-planning/specifications/**)
- Architecture decision records (docs/02-architecture/**)

### Validation Categories
| Category | Check | Error Type |
|----------|-------|------------|
| File Existence | Referenced documents must exist | broken_link |
| ID Consistency | Feature/task IDs match across documents | id_mismatch |
| Date Consistency | Completion dates align in all references | date_conflict |
| Hierarchy Integrity | Parent-child relationships are bidirectional | orphan_reference |
| Status Alignment | Status fields match between linked documents | status_mismatch |

### Validation Output Example
```json
{
  "total_references": 87,
  "references_validated": 87,
  "validation_results": {
    "file_existence": {"checked": 42, "passed": 40, "failed": 2},
    "id_consistency": {"checked": 28, "passed": 28, "failed": 0},
    "date_consistency": {"checked": 17, "passed": 15, "failed": 2}
  },
  "overall_integrity": 0.95
}
```

---

## Feature Overlap Analysis

**Quantified comparison of 2+ feature specs for merge/separate/refactor decisions.**

### 3D Overlap Formula
```
Overlap = (Responsibility × 0.40) + (Requirement × 0.30) + (Infrastructure × 0.30)
```

### Dimension Calculations
| Dimension | Weight | Calculation |
|-----------|--------|-------------|
| Responsibility | 0.40 | (shared_keywords / total_unique_keywords) |
| Requirement | 0.30 | (shared_entities / total_unique_entities) |
| Infrastructure | 0.30 | (shared_workflows / total_unique_workflows) |

### Decision Matrix
| Overlap % | Decision | Action |
|-----------|----------|--------|
| >70% | MERGE | Consolidate into single feature |
| <30% | SEPARATE | Maintain as distinct features |
| 30-70% | REFACTOR | Extract shared foundation, separate unique parts |

### Tie-Breaker Zones
**When overlap falls in borderline ranges (28-32%, 68-72%), apply tie-breakers:**

| Priority | Factor | Bias Direction |
|----------|--------|----------------|
| 1 | Synergy Strength | Measurable synergies -> MERGE |
| 2 | Implementation Cost | Shared infrastructure >50% -> MERGE |
| 3 | Maintainability | Distinct teams -> SEPARATE |

### Edge Cases
- **100% overlap**: Identical specs, recommend immediate consolidation
- **0% overlap**: No relationship, skip conflict/synergy analysis

### Finding Gates
| Gate | Threshold | Requirement |
|------|-----------|-------------|
| Quantified Overlap | 0.80+ | All 3 dimensions calculated |
| Concrete Conflict | 0.90+ | Opposing requirements documented |
| Measurable Synergy | 0.75+ | Sequential/amplification effect identified |
| Architecture Violation | 0.85+ | Constraint breach documented |

---

## 5 Whys Adjustment Logic

**Root cause analysis adjustments to overlap calculations.**

### Adjustment Rules
| Root Cause Finding | Adjustment | Rationale |
|--------------------|------------|-----------|
| Keyword overlap is superficial | -10% to -15% | Same terms, different contexts |
| Entity overlap is architectural | +10% to +15% | Shared infrastructure indicates tight coupling |
| Workflow overlap is user-facing | +10% | User confusion risk if separated |
| Workflow overlap is internal-only | -10% | Implementation detail, not user impact |

### Application Process
1. Calculate base overlap using 3D formula
2. Apply 5 Whys to each dimension exceeding 30%
3. Identify root cause category
4. Apply adjustment (+/- 10-15%)
5. Recalculate final decision threshold

### Example
```
Base Overlap: 68% (borderline MERGE)
5 Whys Finding: Keyword overlap is superficial naming convention
Adjustment: -12%
Final Overlap: 56% (REFACTOR decision)
```

---

## AI Documentation Best Practices

**6 industry techniques for AI-readable documentation.**

### Technique 1: Automated Markdown Updates
- Structured status fields with consistent formatting
- Completion checkboxes with percentage tracking
- Timestamp automation (ISO 8601 format)

### Technique 2: Hierarchical Discovery Patterns
- Progressive disclosure with 3-tier loading
- Tier 1: Metadata (YAML frontmatter)
- Tier 2: Core content (main sections)
- Tier 3: References (links to detailed docs)

### Technique 3: Emoji Standardization
| Emoji | Meaning |
|-------|---------|
| Target | Active/Current focus |
| Checkmark | Complete |
| Hourglass | Waiting/Blocked |
| Clipboard | Planning |
| Rocket | Launch/Deploy |

### Technique 4: llms.txt Integration
- Structured metadata in YAML frontmatter
- Semantic search optimization
- Machine-readable field naming

### Technique 5: Repostatus.org Badges
- Status indicators: planning, active, complete, archived
- Visual project lifecycle communication

### Technique 6: Custom Slash Commands
- References to /spec, /plan, /tasks for related workflows
- Quick navigation between document types

---

## Progressive Disclosure Guidelines

**Target: <500 lines main content with externalized details.**

### Structure Requirements
| Tier | Content | Target Size |
|------|---------|-------------|
| 1 - Metadata | YAML frontmatter, status, dates | <20 lines |
| 2 - Core | Main sections, key decisions | <400 lines |
| 3 - References | Links to detailed docs, appendices | <80 lines |

### Size Efficiency Rules
1. If section exceeds 50 lines, externalize to separate doc
2. Use key-value format over verbose tables
3. Reference-based inheritance avoids duplication
4. Link to detailed docs instead of inline expansion

### Compliance Scoring
```
PD_Score = (500 - actual_lines) / 500
         + (sections_hierarchical / total_sections) × 0.3
         + (externalized_details / total_details) × 0.2
```

---

## Token Density Optimization

**Reduce token consumption while preserving semantic content.**

### Filler Word Reduction
| Metric | Before | Target | Improvement |
|--------|--------|--------|-------------|
| Filler word density | 12% | 4% | 10-20% token reduction |
| Words to eliminate | "just", "simply", "basically", "actually", "really" | 0% | Cleaner prose |

### Voice Conversion
| Metric | Before | Target | Improvement |
|--------|--------|--------|-------------|
| Active voice ratio | 68% | 87% | 15-20% token reduction |
| Passive patterns | "was implemented by", "is used for" | Active equivalents | Clearer attribution |

### Structural Optimization
| Technique | Savings | Example |
|-----------|---------|---------|
| Key-value over verbose tables | 20-30% | `Status: COMPLETE` vs table row |
| Bullet lists over paragraphs | 15-25% | Scannable content |
| Reference links over inline | 40-60% | `See [details](link)` vs embedded |

### Optimization Output Example
```json
{
  "before": {"lines": 650, "estimated_tokens": 2925, "filler_density": 0.12},
  "after": {"lines": 485, "estimated_tokens": 2180, "filler_density": 0.04},
  "improvements": {"token_reduction": 745, "reduction_percentage": 25.5}
}
```

---

## Anti-Patterns (NEVER DO)

### Roadmap Operations
- Modify files outside `docs/00-project/roadmaps/**` or `docs/00-project/operations/*`
- Skip cross-reference validation after updates
- Exceed sprint capacity (3 large + 2 small streams max)
- Create specs or plans (delegate to /spec command, planning)
- Update LIVING_SPRINT without capacity validation

### Feature Overlap Analysis
- Make merge/separate decisions without calculating overlap percentage
- Skip architecture alignment validation
- Exceed rate limits (3 conflicts, 5 overlaps, 5 synergies max)
- Proceed without passing pre-flight checklist
- Use external search before attempting local analysis

### General
- Batch multiple file modifications without read-back verification
- Ignore tie-breaker zones (28-32%, 68-72%)
- Assume overlap from keyword similarity alone (apply 5 Whys)

---

## Error Recovery

| Error Type | Detection | Recovery Action |
|------------|-----------|-----------------|
| File operation fails | Write/edit returns error | Retry once with adjusted escaping, then FAILURE |
| Capacity exceeded | Sprint items > 37h total | Alert, suggest deferring lowest-priority streams |
| Broken cross-references | Link target not found | Report with recovery suggestions |
| Schema violation | Input fails validation | FAILURE with specific field errors |
| Template not found | Create operation fails | FAILURE, suggest creating template |
| LIVING_SPRINT.md missing | Read fails | Check alternative paths, then FAILURE |
| Circular cross-reference | A -> B -> A detected | Break cycle, report both endpoints |
| Conflicting timestamps | Same item has different dates | Use most recent, flag for manual review |
| Spec not found | Glob returns empty | FAILURE with path suggestions |
| Spec malformed | No extractable sections | FAILURE with format requirements |
| Low confidence (<0.70) | Decision calculation | FAILURE, suggest additional context |
| Context window exceeded | 100+ files in scope | Process in batches of 20, aggregate results |

### Escalation Protocol
1. Return `status: "FAILURE"` with appropriate `failure_type`
2. Include `recovery_suggestions` array with actionable steps
3. Include `partial_results` if any work completed
4. Max 2 retry attempts per operation

---

## Quick Reference

### Key Files
| File | Purpose |
|------|---------|
| `docs/00-project/roadmaps/LIVING_SPRINT.md` | Current sprint single source of truth |
| `docs/00-project/roadmaps/SPRINT-ROADMAP.md` | Sprint sequence and planning |
| `docs/00-project/roadmaps/active/*.md` | Active quarterly roadmaps |
| `docs/00-project/operations/SPRINT-ARCHIVE-*.md` | Completed sprint archives |
| `docs/01-planning/specifications/**/*.md` | Feature specifications for overlap analysis |

### Timestamp Format
**ISO 8601**: `2025-11-30T12:34:56Z` (UTC)

PowerShell generation:
```powershell
Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ"
```

### Confidence Bands
| Band | Range | Interpretation |
|------|-------|----------------|
| High | 0.90+ | Strong recommendation, proceed |
| Medium-High | 0.80-0.89 | Good confidence, minor caveats |
| Medium | 0.70-0.79 | Acceptable, consider additional validation |
| Low | <0.70 | Insufficient confidence, gather more context |

### Decision Thresholds Summary
| Metric | Threshold | Action |
|--------|-----------|--------|
| Health Score | <0.60 | Critical - immediate attention |
| Overlap | >70% | MERGE features |
| Overlap | <30% | SEPARATE features |
| Overlap | 30-70% | REFACTOR shared foundation |
| Capacity | >40h | Reject - defer streams |
| Confidence | <0.70 | FAILURE - gather context |

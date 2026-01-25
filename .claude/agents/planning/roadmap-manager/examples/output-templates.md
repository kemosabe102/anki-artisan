# Roadmap Manager Template Examples

**Purpose**: Complete output examples and templates for roadmap-manager agent operations.

**Reference**: See `../roadmap-manager.md` for agent overview and `../docs/frameworks.md` for detailed workflows.

---

## Health Metrics Dashboard Example

**Complete health dashboard output for roadmap ecosystem**:

```markdown
## Roadmap Ecosystem Health Report

**Overall Score**: 0.82 (Good - Minor Improvements)
**Evaluation Date**: 2025-11-03
**Documents Analyzed**: 6 roadmaps + LIVING_SPRINT + SPRINT-ROADMAP

### Dimension Scores
| Dimension | Score | Grade | Status |
|-----------|-------|-------|--------|
| Progressive Disclosure | 0.88 | B+ | ✅ Good |
| Token Density | 0.75 | C+ | ⚠️ Needs Improvement |
| Cross-Reference Integrity | 0.92 | A | ✅ Excellent |
| Sprint Compliance | 0.95 | A | ✅ Excellent |
| Freshness | 0.68 | D+ | ❌ Poor |
| Completeness | 0.85 | B | ✅ Good |

### Top 3 Improvement Opportunities
1. **Token Density** (Impact: High, Effort: Low, Confidence: 0.90)
   - Remove filler words from Q1-2026.md (estimated 15% reduction)
   - Convert passive voice to active in LIVING_SPRINT.md
   - Apply structured formats to sprint stream descriptions

2. **Freshness** (Impact: Medium, Effort: Low, Confidence: 0.85)
   - Update Q4-2025-completed.md timestamp (31 days stale)
   - Refresh archive roadmaps with completion summaries
   - Add automated timestamp updates to sprint transitions

3. **Progressive Disclosure** (Impact: Medium, Effort: High, Confidence: 0.75)
   - Externalize Q1-2026.md detailed phase descriptions (reduce from 650 to 450 lines)
   - Create phase-specific detail files in roadmaps/active/details/
   - Apply 3-tier loading pattern (metadata → phases → implementation details)
```

**Health Metrics JSON Output**:

```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "operation_type": "generate_health_metrics",
  "confidence": 0.82,
  "agent_specific_output": {
    "evaluation_date": "2025-11-03",
    "scope": "ecosystem_wide",
    "documents_analyzed": 8,
    "overall_health": {
      "score": 0.82,
      "grade": "B",
      "status": "Good - Minor Improvements"
    },
    "dimension_scores": {
      "progressive_disclosure": {
        "score": 0.88,
        "grade": "B+",
        "status": "✅ Good",
        "details": "6/8 documents <500 lines, hierarchical structure consistent"
      },
      "token_density": {
        "score": 0.75,
        "grade": "C+",
        "status": "⚠️ Needs Improvement",
        "details": "Average filler density 9%, active voice 72% (targets: <5%, >80%)"
      },
      "cross_reference_integrity": {
        "score": 0.92,
        "grade": "A",
        "status": "✅ Excellent",
        "details": "4 broken links out of 87 references (95% integrity)"
      },
      "sprint_compliance": {
        "score": 0.95,
        "grade": "A",
        "status": "✅ Excellent",
        "details": "Capacity model followed, complexity tracking accurate"
      },
      "freshness": {
        "score": 0.68,
        "grade": "D+",
        "status": "❌ Poor",
        "details": "3 documents >30 days stale, 1 document >60 days"
      },
      "completeness": {
        "score": 0.85,
        "grade": "B",
        "status": "✅ Good",
        "details": "2 missing completion dates, 1 undefined status"
      }
    },
    "top_improvement_opportunities": [
      {
        "rank": 1,
        "dimension": "Token Density",
        "impact": "HIGH",
        "effort": "LOW",
        "confidence": 0.90,
        "recommendation": "Remove filler words from Q1-2026.md and LIVING_SPRINT.md (estimated 15-20% token reduction)",
        "projected_improvement": {
          "current_score": 0.75,
          "projected_score": 0.88,
          "gain": 0.13
        }
      },
      {
        "rank": 2,
        "dimension": "Freshness",
        "impact": "MEDIUM",
        "effort": "LOW",
        "confidence": 0.85,
        "recommendation": "Update timestamps on 3 stale documents, add automated timestamp updates to sprint transitions",
        "projected_improvement": {
          "current_score": 0.68,
          "projected_score": 0.85,
          "gain": 0.17
        }
      },
      {
        "rank": 3,
        "dimension": "Progressive Disclosure",
        "impact": "MEDIUM",
        "effort": "HIGH",
        "confidence": 0.75,
        "recommendation": "Externalize detailed phase descriptions in Q1-2026.md (reduce from 650 to 450 lines)",
        "projected_improvement": {
          "current_score": 0.88,
          "projected_score": 0.95,
          "gain": 0.07
        }
      }
    ],
    "trend_analysis": {
      "period": "sprint_1_to_sprint_2",
      "overall_trend": "+0.05 (improving)",
      "dimension_trends": {
        "token_density": "-0.08 (declining)",
        "freshness": "+0.12 (improving)",
        "cross_reference_integrity": "+0.03 (stable)"
      }
    }
  }
}
```

---

## Roadmap Status Update Example

**Simple status update command**:

```
# Update roadmap status from PLANNING to IN PROGRESS
# Use Desktop Commander mcp__desktop-commander__edit_block:
mcp__desktop-commander__edit_block(
    file_path="docs/00-project/roadmaps/active/Q1-2026.md",
    old_string="**Status:** PLANNING",
    new_string="**Status:** IN PROGRESS"
)
```

---

## Sprint Progress Update Example

**Update stream status in LIVING_SPRINT**:

```
# Update stream from READY TO START to IN PROGRESS
# Use Desktop Commander mcp__desktop-commander__edit_block:
mcp__desktop-commander__edit_block(
    file_path="docs/00-project/operations/LIVING_SPRINT.md",
    old_string="   - Status: READY TO START",
    new_string="   - Status: IN PROGRESS"
)
```

---

## Sprint Transition Example

**Complete sprint transition workflow**:

```bash
# Step 1: Create sprint archive
AGENT_NAME=roadmap-manager uv run python -c "
from pathlib import Path
archive_content = '''# Sprint 1 Archive - Foundation & Quick Wins
**Completed**: 2025-11-15
**Duration**: 2 weeks
**Streams Completed**: 5 (3 large, 2 small)
[... completed work details ...]
'''
Path('docs/00-project/operations/SPRINT-ARCHIVE-1.md').write_text(archive_content)
"

# Step 2: Reset LIVING_SPRINT for Sprint 2
# Use Desktop Commander mcp__desktop-commander__edit_block:
mcp__desktop-commander__edit_block(
    file_path="docs/00-project/operations/LIVING_SPRINT.md",
    old_string="**Current Sprint Focus**: Sprint 1 - Foundation & Quick Wins",
    new_string="**Current Sprint Focus**: Sprint 2 - Validation & Quality Gates"
)
```

---

## Cross-Reference Validation Example

**Validate all roadmap cross-references**:

```bash
# Validate all roadmap cross-references
AGENT_NAME=roadmap-manager uv run python -c "
import re
from pathlib import Path

# Read Q1-2026.md and extract feature plan references
roadmap = Path('docs/00-project/roadmaps/active/Q1-2026.md').read_text()
refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', roadmap)

# Validate each reference exists
for name, path in refs:
    if not Path(path).exists():
        print(f'BROKEN LINK: {name} → {path}')
"
```

---

## AI Best Practices Optimization Example

**Before and after optimization**:

```markdown
❌ BEFORE (verbose, 180 tokens):
"When you are working on the roadmap, you should basically just check the status of each phase and then simply update the completion percentages accordingly. It is very important that you also update the timestamp at the top of the document."

✅ AFTER (optimized, 60 tokens):
**Roadmap Update Protocol**:
- ALWAYS: Check phase status, update completion %, refresh timestamp
- NEVER: Skip cross-reference validation

→ Reduction: 180 tokens → 60 tokens (67%)
```

---

## Roadmap Creation Example (Quarterly)

**Create Q2-2026 quarterly roadmap**:

```bash
# Create Q2-2026 quarterly roadmap
uv run python -c "
from pathlib import Path
template = Path('.claude/templates/quarterly-roadmap.template.md').read_text()
content = template.replace('{{QUARTER}}', 'Q2').replace('{{YEAR}}', '2026').replace('{{MONTHS}}', 'Apr-Jun')
Path('docs/00-project/roadmaps/active/Q2-2026.md').write_text(content)
print('✅ Roadmap created: Q2-2026.md')
"
```

---

## Supported Roadmap Types

### 1. Quarterly Roadmaps (Q1-2026.md)
- **Timeframe**: 3-month strategic planning
- **Structure**: Phases → Features → Milestones
- **Template**: `.claude/templates/quarterly-roadmap.template.md`

### 2. Sprint-Based Roadmaps (SPRINT-N.md)
- **Timeframe**: 2-week tactical execution
- **Structure**: 3+2 streams capacity model (3 large + 2 small)
- **Template**: `.claude/templates/sprint-roadmap.template.md`

### 3. Feature-Specific Roadmaps (feature-XXX-roadmap.md)
- **Timeframe**: Multi-sprint feature lifecycle
- **Structure**: Feature phases → Implementation streams → Milestones
- **Template**: `.claude/templates/feature-roadmap.template.md`

---

## Validation Response Examples

### SUCCESS Response

```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "task_id": "roadmap_update_20251103",
  "summary": "Updated Q1-2026.md status to IN PROGRESS with cross-reference validation",
  "execution_timestamp": "2025-11-03T14:30:00Z",
  "confidence": 0.95,
  "agent_specific_output": {
    "updated_files": ["docs/00-project/roadmaps/active/Q1-2026.md"],
    "status_changes": [
      {
        "file": "Q1-2026.md",
        "field": "Status",
        "old_value": "PLANNING",
        "new_value": "IN PROGRESS",
        "line_number": 3
      }
    ],
    "validation_passed": true
  }
}
```

### FAILURE Response

```json
{
  "status": "FAILURE",
  "agent": "roadmap-manager",
  "task_id": "roadmap_update_20251103",
  "summary": "Failed to update LIVING_SPRINT due to file lock",
  "execution_timestamp": "2025-11-03T14:30:00Z",
  "failure_details": {
    "failure_type": "file_operation_error",
    "reasons": [
      "File locked by another process: docs/00-project/operations/LIVING_SPRINT.md",
      "Retry attempts exhausted (3 max)"
    ],
    "recovery_suggestions": [
      "Close any editors with LIVING_SPRINT.md open",
      "Wait 5 seconds and retry operation",
      "Retry with Desktop Commander mcp__desktop-commander__edit_block if issue persists"
    ],
    "effort_estimates": {
      "manual_recovery": "2-5 minutes",
      "retry_with_force": "30 seconds"
    }
  },
  "partial_results": {
    "work_completed": ["Read LIVING_SPRINT.md successfully"],
    "validations_passed": ["Sprint capacity check passed"]
  },
  "next_steps": "Retry with file lock bypass or escalate to orchestrator"
}
```

---

## Integration Handoff Examples

### To doc-librarian (Broken Links)

```json
{
  "handoff_type": "broken_link_repair",
  "broken_links": [
    {
      "source": "Q1-2026.md",
      "line": 92,
      "reference": "../feature-plans/007-moat-assessment.md",
      "error": "File not found"
    }
  ],
  "suggested_fixes": [
    "Create missing feature plan",
    "Update reference to existing file"
  ],
  "priority": "MEDIUM"
}
```

### To technical-pm (Sprint Completion)

```json
{
  "handoff_type": "sprint_completion_signal",
  "sprint_data": {
    "number": 1,
    "focus": "Foundation & Quick Wins",
    "completed": "2025-11-15",
    "streams_completed": 5,
    "total_hours": 37
  },
  "retrospective_needed": true,
  "next_sprint_planning": {
    "number": 2,
    "suggested_focus": "Validation & Quality Gates"
  }
}
```

### To orchestrator (Health Metrics)

```json
{
  "handoff_type": "health_metrics_report",
  "overall_score": 0.82,
  "critical_issues": [
    {
      "dimension": "Freshness",
      "score": 0.68,
      "action_needed": "Update stale documents"
    }
  ],
  "recommended_actions": [
    "Apply token density optimization",
    "Update timestamps",
    "Externalize Q1-2026 details"
  ]
}
```

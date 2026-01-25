# Output Schema Reference

Complete field specifications for CLAUDE.md evaluation JSON output.

**Framework**: 70-point Gauntlet-specific evaluation across 7 dimensions.

---

## Document Structure Overview

```
Evaluation Flow:
┌─────────────────┐
│ 7 Dimension     │──→ 7 DimensionReport objects (per-agent output)
│ Specialists     │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Orchestrator    │──→ 1 SynthesisReport object (merged output)
│ Synthesis       │
└─────────────────┘
```

---

## Part 1: DimensionReport Schema (Per-Agent Output)

Each dimension specialist produces one `DimensionReport`.


### DimensionReport JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["dimension", "score", "status", "criteria", "findings", "recommendations"],
  "properties": {
    "dimension": {
      "type": "string",
      "enum": ["identity", "environment", "architecture", "commands", "style", "safety", "meta"]
    },
    "score": {
      "type": "number",
      "minimum": 0,
      "maximum": 10,
      "description": "Points awarded out of 10 for this dimension"
    },
    "status": {
      "type": "string",
      "enum": ["pass", "warn", "fail"],
      "description": "Overall dimension health status"
    },
    "criteria": {
      "type": "array",
      "items": { "$ref": "#/definitions/Criterion" }
    },
    "findings": {
      "type": "array",
      "items": { "type": "string" }
    },
    "recommendations": {
      "type": "array",
      "items": { "$ref": "#/definitions/Recommendation" }
    }
  }
}
```

---


### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dimension` | enum | Yes | One of 7 evaluation dimensions |
| `score` | number (0-10) | Yes | Points awarded for this dimension |
| `status` | enum | Yes | `pass` (>=8), `warn` (5-7), `fail` (<5) |
| `criteria` | array[Criterion] | Yes | Evaluated criteria with scores |
| `findings` | array[string] | Yes | Key observations from evaluation |
| `recommendations` | array[Recommendation] | Yes | Prioritized improvement actions |

**Dimension Definitions**:

| Dimension | Weight | Focus Area |
|-----------|--------|------------|
| `identity` | 10 pts | Agent role, personality, constraints |
| `environment` | 10 pts | Python version, paths, tools, platform |
| `architecture` | 10 pts | Directory structure, key files, patterns |
| `commands` | 10 pts | Available commands, task mapping |
| `style` | 10 pts | Code conventions, formatting, naming |
| `safety` | 10 pts | Banned operations, security constraints |
| `meta` | 10 pts | Update protocols, version tracking |

---


## Part 2: Criterion Object Structure

Each dimension contains multiple criteria contributing to its score.

### Criterion JSON Schema

```json
{
  "definitions": {
    "Criterion": {
      "type": "object",
      "required": ["id", "name", "points_possible", "points_awarded", "met"],
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^[A-Z]{2,4}-\\d{2}$",
          "description": "Unique criterion identifier (e.g., ID-01, ENV-03)"
        },
        "name": {
          "type": "string",
          "description": "Human-readable criterion name"
        },
        "points_possible": {
          "type": "number",
          "minimum": 0.5,
          "maximum": 3,
          "description": "Maximum points for this criterion"
        },
        "points_awarded": {
          "type": "number",
          "minimum": 0,
          "description": "Actual points earned (<=points_possible)"
        },
        "met": {
          "type": "boolean",
          "description": "True if criterion fully satisfied"
        },
        "evidence": {
          "type": "string",
          "description": "Quote or reference from CLAUDE.md"
        },
        "location": {
          "type": "string",
          "description": "Section header or line reference"
        },
        "recommendation": {
          "type": "string",
          "description": "Specific fix if criterion not met"
        }
      }
    }
  }
}
```

---


### Criterion Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Pattern: `{DIM}-{NN}` (e.g., ID-01, ENV-03) |
| `name` | string | Yes | Criterion name (e.g., "Agent Role Definition") |
| `points_possible` | number | Yes | Weight: 0.5 (minor), 1.0 (standard), 2.0 (important), 3.0 (critical) |
| `points_awarded` | number | Yes | Earned points, 0 to points_possible |
| `met` | boolean | Yes | True if points_awarded == points_possible |
| `evidence` | string | No | Direct quote or section reference |
| `location` | string | No | Section header (e.g., "## Orchestrator Identity") |
| `recommendation` | string | No | Required if met=false, specific fix action |

**Criterion ID Prefixes**:

| Prefix | Dimension |
|--------|-----------|
| `ID-` | Identity |
| `ENV-` | Environment |
| `ARCH-` | Architecture |
| `CMD-` | Commands |
| `STY-` | Style |
| `SAF-` | Safety |
| `META-` | Meta |

---


## Part 3: Recommendation Object Structure

Prioritized improvement actions for each dimension.

### Recommendation JSON Schema

```json
{
  "definitions": {
    "Recommendation": {
      "type": "object",
      "required": ["priority", "action", "impact", "effort"],
      "properties": {
        "priority": {
          "type": "string",
          "enum": ["P1", "P2", "P3"],
          "description": "Urgency level"
        },
        "action": {
          "type": "string",
          "description": "Specific, actionable improvement"
        },
        "impact": {
          "type": "string",
          "enum": ["high", "medium", "low"],
          "description": "Expected score improvement"
        },
        "effort": {
          "type": "string",
          "enum": ["low", "medium", "high"],
          "description": "Implementation effort required"
        },
        "criterion_ids": {
          "type": "array",
          "items": { "type": "string" },
          "description": "Related criteria this addresses"
        }
      }
    }
  }
}
```

---


### Recommendation Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `priority` | enum | Yes | P1 (critical), P2 (important), P3 (nice-to-have) |
| `action` | string | Yes | Imperative verb phrase (e.g., "Add Python version constraint") |
| `impact` | enum | Yes | Score improvement: high (>2pts), medium (1-2pts), low (<1pt) |
| `effort` | enum | Yes | Implementation: low (<15min), medium (15-60min), high (>1hr) |
| `criterion_ids` | array[string] | No | Criteria addressed by this action |

**Priority Definitions**:

| Priority | Meaning | Action Timeline |
|----------|---------|-----------------|
| P1 | Critical gap, blocks agent effectiveness | Immediate |
| P2 | Important enhancement, improves quality | This sprint |
| P3 | Nice-to-have, polish/optimization | Backlog |

**Impact-Effort Quadrants**:

| Impact | Effort | Recommendation |
|--------|--------|----------------|
| High | Low | P1 - Quick wins, do first |
| High | High | P2 - Strategic, plan carefully |
| Low | Low | P3 - Opportunistic |
| Low | High | Skip - Not worth effort |

---


## Part 4: SynthesisReport Schema (Orchestrator Output)

The orchestrator merges 7 dimension reports into a single synthesis.

### SynthesisReport JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": [
    "target_file",
    "evaluation_timestamp",
    "total_score",
    "max_score",
    "percentage",
    "grade",
    "dimensions",
    "top_recommendations"
  ],
  "properties": {
    "target_file": {
      "type": "string",
      "description": "Path to evaluated CLAUDE.md file"
    },
    "evaluation_timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "total_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 70,
      "description": "Sum of all dimension scores"
    },
    "max_score": {
      "type": "number",
      "const": 70,
      "description": "Maximum possible score (7 dimensions x 10 points)"
    },
    "percentage": {
      "type": "number",
      "minimum": 0,
      "maximum": 100,
      "description": "total_score / max_score * 100"
    },
    "grade": {
      "type": "string",
      "enum": ["A", "B", "C", "D", "F"],
      "description": "Letter grade based on percentage"
    },
    "dimensions": {
      "type": "array",
      "items": { "$ref": "#/definitions/DimensionReport" },
      "minItems": 7,
      "maxItems": 7
    },
    "top_recommendations": {
      "type": "array",
      "items": { "$ref": "#/definitions/Recommendation" },
      "maxItems": 10,
      "description": "Highest-priority recommendations across all dimensions"
    },
    "summary": {
      "type": "string",
      "description": "2-3 sentence executive summary"
    }
  }
}
```

---


### Synthesis Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `target_file` | string | Yes | Absolute path to evaluated CLAUDE.md |
| `evaluation_timestamp` | ISO 8601 | Yes | When evaluation completed |
| `total_score` | number (0-70) | Yes | Sum of dimension scores |
| `max_score` | number (70) | Yes | Constant: 70 points |
| `percentage` | number (0-100) | Yes | Calculated: (total_score/70)*100 |
| `grade` | enum | Yes | Letter grade from percentage |
| `dimensions` | array[DimensionReport] | Yes | All 7 dimension results |
| `top_recommendations` | array[Recommendation] | Yes | Top 10 cross-dimension priorities |
| `summary` | string | No | Executive summary paragraph |

**Grade Thresholds**:

| Grade | Percentage | Interpretation |
|-------|------------|----------------|
| A | 90-100% | Excellent, production-ready |
| B | 80-89% | Good, minor improvements needed |
| C | 70-79% | Acceptable, notable gaps |
| D | 60-69% | Below standard, significant work needed |
| F | <60% | Failing, major revision required |

---


## Part 5: Validation Rules

Rules for ensuring schema compliance and data integrity.

### Score Validation

| Rule | Formula | Error If |
|------|---------|----------|
| Dimension score bounds | 0 <= score <= 10 | score < 0 OR score > 10 |
| Criterion score bounds | 0 <= points_awarded <= points_possible | points_awarded > points_possible |
| Dimension sum | sum(criteria.points_awarded) == score | Mismatch detected |
| Total score sum | sum(dimensions.score) == total_score | Mismatch detected |
| Percentage calculation | percentage == (total_score/70)*100 | Calculation error |

### Status Consistency

| Rule | Condition | Expected Status |
|------|-----------|-----------------|
| Pass threshold | score >= 8 | `pass` |
| Warn threshold | 5 <= score < 8 | `warn` |
| Fail threshold | score < 5 | `fail` |

**Validation Error**:
```json
{
  "validation_error": {
    "rule": "status_consistency",
    "dimension": "environment",
    "score": 4.5,
    "actual_status": "warn",
    "expected_status": "fail"
  }
}
```



### Required Dimension Count

| Rule | Expected | Error If |
|------|----------|----------|
| Dimension array length | 7 | dimensions.length != 7 |
| Unique dimensions | All 7 present | Missing or duplicate dimension |

**Required Dimensions Checklist**:
- [ ] identity
- [ ] environment
- [ ] architecture
- [ ] commands
- [ ] style
- [ ] safety
- [ ] meta

### Recommendation Priority Ordering

| Rule | Condition |
|------|-----------|
| P1 before P2 | All P1 recommendations appear before P2 |
| P2 before P3 | All P2 recommendations appear before P3 |
| Max 10 in synthesis | top_recommendations.length <= 10 |

---

## Part 6: Example Outputs

### Minimal DimensionReport Example

```json
{
  "dimension": "environment",
  "score": 8.5,
  "status": "pass",
  "criteria": [
    {
      "id": "ENV-01",
      "name": "Python Version Specified",
      "points_possible": 2,
      "points_awarded": 2,
      "met": true,
      "evidence": "Python: 3.11+",
      "location": "## Environment"
    },
    {
      "id": "ENV-02",
      "name": "Package Manager Defined",
      "points_possible": 2,
      "points_awarded": 2,
      "met": true,
      "evidence": "Package Manager: UV",
      "location": "## Environment"
    }
  ],
  "findings": [
    "Python 3.11+ requirement clearly stated",
    "UV package manager enforced over pip"
  ],
  "recommendations": []
}
```



### DimensionReport with Recommendations Example

```json
{
  "dimension": "safety",
  "score": 6.0,
  "status": "warn",
  "criteria": [
    {
      "id": "SAF-01",
      "name": "Banned Operations Listed",
      "points_possible": 3,
      "points_awarded": 3,
      "met": true,
      "evidence": "## BANNED Operations section present",
      "location": "## BANNED Operations"
    },
    {
      "id": "SAF-02",
      "name": "Destructive Git Commands Blocked",
      "points_possible": 2,
      "points_awarded": 1,
      "met": false,
      "evidence": "git reset --hard mentioned but git push --force missing",
      "location": "## BANNED Operations",
      "recommendation": "Add git push --force to banned commands list"
    }
  ],
  "findings": [
    "Banned operations section exists with clear list",
    "Missing coverage for force push operations"
  ],
  "recommendations": [
    {
      "priority": "P1",
      "action": "Add git push --force to BANNED Operations list",
      "impact": "high",
      "effort": "low",
      "criterion_ids": ["SAF-02"]
    }
  ]
}
```



### Minimal SynthesisReport Example

```json
{
  "target_file": "C:/Users/kemos/Repos/gauntlet-agents/CLAUDE.md",
  "evaluation_timestamp": "2025-01-15T14:30:00Z",
  "total_score": 58,
  "max_score": 70,
  "percentage": 82.86,
  "grade": "B",
  "dimensions": [
    { "dimension": "identity", "score": 9.0, "status": "pass" },
    { "dimension": "environment", "score": 8.5, "status": "pass" },
    { "dimension": "architecture", "score": 8.0, "status": "pass" },
    { "dimension": "commands", "score": 7.5, "status": "warn" },
    { "dimension": "style", "score": 9.0, "status": "pass" },
    { "dimension": "safety", "score": 6.0, "status": "warn" },
    { "dimension": "meta", "score": 10.0, "status": "pass" }
  ],
  "top_recommendations": [
    {
      "priority": "P1",
      "action": "Add git push --force to BANNED Operations",
      "impact": "high",
      "effort": "low"
    },
    {
      "priority": "P2",
      "action": "Add task-to-command mapping table",
      "impact": "medium",
      "effort": "medium"
    }
  ],
  "summary": "CLAUDE.md scores B (82.86%). Strong identity and style sections. Safety section needs force-push prohibition. Commands section would benefit from explicit task mapping."
}
```

---

## See Also

- `../SKILL.md` - Skill usage and workflow
- `./evaluation-criteria.md` - Complete 70-point criteria list
- `./dimension-rubrics.md` - Scoring rubrics per dimension

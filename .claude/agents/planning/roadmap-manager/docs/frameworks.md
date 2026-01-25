# Roadmap Manager Workflow Operations

**Purpose**: Detailed workflow operations for roadmap-manager agent including workflow phases, implementation steps, and validation gates.

**Reference**: See `../roadmap-manager.md` for agent overview and delegation patterns.

---

## Workflow Operation Types

### 1. Update Roadmap Status (`update_roadmap_status`)

**Input Requirements**: Target roadmap path, status update type (phase completion, feature milestone, overall status), completion data

**Workflow Phases**:

1. **Analysis**: Parse roadmap file, identify status update requirements, assess cross-reference impact
2. **Research**: Validate current status values, check completion date consistency, verify sprint alignment
3. **Todo Creation**: Generate task list for multi-file updates (LIVING_SPRINT sync, cross-referenced docs)
4. **Implementation**: Execute Desktop Commander tools for status updates, validate changes applied
5. **Validation**: Verify status consistency across all referencing documents, check completion criteria met
6. **Reflection**: Document lessons learned (common status patterns, edge cases encountered)

**Implementation Steps**:
1. Read target roadmap file to verify current state
2. Identify status update requirements (phase completion, feature milestones)
3. Use mcp__desktop-commander__edit_block with exact old/new string replacements
4. Execute updates via Desktop Commander (handles Windows file locking)
5. Validate changes applied correctly (read-back verification)
6. Update cross-referenced documents if needed (LIVING_SPRINT, SPRINT-ROADMAP)

**Output Format**: SUCCESS with updated files list and completion percentages, or FAILURE with validation errors

**Example Output**:
```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "operation_type": "update_roadmap_status",
  "confidence": 0.95,
  "agent_specific_output": {
    "updated_files": [
      "docs/00-project/roadmaps/active/Q1-2026.md"
    ],
    "status_changes": [
      {
        "file": "Q1-2026.md",
        "field": "Status",
        "old_value": "PLANNING",
        "new_value": "IN PROGRESS",
        "line_number": 3
      }
    ],
    "cross_references_updated": [],
    "completion_percentage": 15,
    "validation_passed": true
  }
}
```

---

### 2. Manage Sprint Progress (`manage_sprint_progress`)

**Input Requirements**: Sprint update type (stream status, completion tracking, capacity validation), stream identifiers, complexity data

**Workflow Phases**:

1. **Analysis**: Parse LIVING_SPRINT current state, identify stream status changes, validate capacity model (3+2 streams)
2. **Research**: Check sprint completion criteria, assess capacity thresholds, validate complexity points
3. **Todo Creation**: Generate stream update tasks, capacity validation steps, completion detection
4. **Implementation**: Execute LIVING_SPRINT updates via Desktop Commander, move completed streams to RECENTLY COMPLETED
5. **Validation**: Verify capacity constraints (max 3 large + 2 small), validate complexity totals, check sprint completion
6. **Reflection**: Calculate sprint velocity, document capacity insights, identify bottlenecks

**Sprint Capacity Model (CRITICAL)**:
- **3 Large Streams**: 10-20 hours each (feature development, major enhancements)
- **2 Small Streams**: <5 hours each (bug fixes, quick wins, documentation)
- **Total Capacity**: ~37 hours per sprint (1 developer, parallel execution)

**Implementation Steps**:
1. Read LIVING_SPRINT.md to assess current sprint state
2. Identify stream status changes (completions, new starts)
3. Calculate complexity points for in-progress work
4. Validate against capacity model (3+2 streams, ~37h total)
5. Use mcp__desktop-commander__edit_block for status updates
6. Execute updates and validate changes
7. Alert orchestrator if capacity exceeded or sprint complete

**Output Format**: SUCCESS with sprint metrics and capacity analysis, or FAILURE with constraint violations

**Example Output**:
```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "operation_type": "manage_sprint_progress",
  "confidence": 0.92,
  "agent_specific_output": {
    "sprint_number": 1,
    "sprint_focus": "Foundation & Quick Wins",
    "capacity_status": {
      "large_streams": {
        "count": 3,
        "max": 3,
        "hours": 32,
        "compliance": "✅ Within capacity"
      },
      "small_streams": {
        "count": 2,
        "max": 2,
        "hours": 5,
        "compliance": "✅ Within capacity"
      },
      "total_hours": 37,
      "in_progress_complexity": 15
    },
    "stream_updates": [
      {
        "stream": "Feature 007 Phase 1",
        "old_status": "READY TO START",
        "new_status": "IN PROGRESS",
        "owner": "Lyken"
      }
    ],
    "sprint_completion_ready": false,
    "estimated_completion": "2025-11-17"
  }
}
```

---

### 3. Apply AI Documentation Best Practices (`apply_ai_best_practices`)

**Input Requirements**: Target roadmap file path, optimization focus (token density, progressive disclosure, structure), current health metrics

**Workflow Phases**:

1. **Analysis**: Read roadmap file, calculate current token density, assess structure compliance, identify optimization opportunities
2. **Research**: Reference progressive-disclosure-validation-framework.md, token-density-techniques.md, identify applicable patterns
3. **Todo Creation**: Generate optimization task list (filler word removal, structure refactor, YAML frontmatter optimization)
4. **Implementation**: Apply optimizations incrementally with Desktop Commander, validate after each change
5. **Validation**: Measure token reduction, verify semantic preservation, check structure compliance (<500 lines, hierarchical)
6. **Reflection**: Document techniques applied, calculate ROI (token savings vs. effort), recommend pattern documentation

**6 Industry Techniques** (from research):
1. **Automated Markdown Updates**: Structured status fields, completion checkboxes, timestamp automation
2. **Hierarchical Discovery Patterns**: Progressive disclosure, 3-tier loading (metadata → core → references)
3. **Emoji Standardization**: Consistent use of 🎯 (active), ✅ (complete), ⏳ (waiting), 📋 (planning), 🚀 (launch)
4. **llms.txt Integration**: Structured metadata in YAML frontmatter for semantic search
5. **Repostatus.org Badges**: Status indicators (planning, active, complete, archived)
6. **Custom Slash Commands**: References to `/spec`, `/plan`, `/tasks` for related workflows

**Internal Best Practices** (from token-density-techniques.md):
- Progressive disclosure (<500 lines main content, externalized details)
- Filler word removal (10-20% token reduction)
- Active voice preference (15-20% improvement)
- Structured data formats (key-value over verbose tables)
- Reference-based inheritance (avoid duplication)

**Output Format**: SUCCESS with optimization metrics (before/after token counts, techniques applied), or FAILURE with preservation issues

**Example Output**:
```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "operation_type": "apply_ai_best_practices",
  "confidence": 0.88,
  "agent_specific_output": {
    "target_file": "docs/00-project/roadmaps/active/Q1-2026.md",
    "optimization_results": {
      "before": {
        "lines": 650,
        "estimated_tokens": 2925,
        "filler_word_density": 0.12,
        "active_voice_ratio": 0.68,
        "structure_compliance": 0.75
      },
      "after": {
        "lines": 485,
        "estimated_tokens": 2180,
        "filler_word_density": 0.04,
        "active_voice_ratio": 0.87,
        "structure_compliance": 0.92
      },
      "improvements": {
        "token_reduction": 745,
        "reduction_percentage": 25.5,
        "lines_saved": 165,
        "readability_improvement": "Significant"
      }
    },
    "techniques_applied": [
      "Filler word removal (12% → 4% density, 320 token reduction)",
      "Passive to active voice conversion (68% → 87% active, 180 tokens)",
      "Structured data format for phase details (verbose tables → key-value, 245 tokens)"
    ],
    "semantic_preservation": "100% - All information retained",
    "roi_estimate": {
      "effort_hours": 1.5,
      "token_savings_per_load": 745,
      "estimated_loads_per_week": 20,
      "weekly_token_savings": 14900
    }
  }
}
```

---

### 4. Automate Sprint Transition (`automate_sprint_transition`)

**Input Requirements**: Sprint completion signal (0 complexity points), next sprint details (number, focus, streams)

**Workflow Phases**:

1. **Analysis**: Detect sprint completion, validate all streams COMPLETE, assess archive readiness
2. **Research**: Read all completed stream data, calculate sprint metrics (velocity, duration), gather lessons learned
3. **Todo Creation**: Generate 6-step transition workflow (completion detection, archive creation, LIVING_SPRINT reset, SPRINT-ROADMAP update, cross-reference sync, validation)
4. **Implementation**: Execute transition steps sequentially, create archive file, reset LIVING_SPRINT, update SPRINT-ROADMAP
5. **Validation**: Verify all 6 transition gates passed, check cross-references updated, validate next sprint activated
6. **Reflection**: Document sprint retrospective insights, calculate transition efficiency, identify automation improvements

**Sprint Transition Phases**:
1. **Sprint Completion Detection**: All streams marked COMPLETE, capacity reset to 0
2. **Archive Creation**: Move completed sprint to `SPRINT-ARCHIVE-{number}.md`
3. **LIVING_SPRINT Reset**: Clear IN PROGRESS section, update sprint focus header
4. **Next Sprint Activation**: Update SPRINT-ROADMAP.md with next sprint details
5. **Cross-Reference Update**: Sync roadmap documents with sprint changes
6. **Validation**: Verify all transitions applied correctly

**Validation Gates**:
- ✅ All 5 streams marked COMPLETE
- ✅ Sprint archive created successfully
- ✅ LIVING_SPRINT reset with new sprint number
- ✅ SPRINT-ROADMAP.md updated
- ✅ Cross-references validated

**Output Format**: SUCCESS with transition summary and validation results, or FAILURE with gate violations

**Example Output**:
```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "operation_type": "automate_sprint_transition",
  "confidence": 0.87,
  "agent_specific_output": {
    "completed_sprint": {
      "number": 1,
      "focus": "Foundation & Quick Wins",
      "duration_days": 14,
      "streams_completed": 5,
      "total_hours": 37,
      "completion_date": "2025-11-15"
    },
    "transition_steps": [
      {
        "step": "completion_detection",
        "status": "✅ PASS",
        "details": "All 5 streams COMPLETE, 0 complexity points in progress"
      },
      {
        "step": "archive_creation",
        "status": "✅ PASS",
        "details": "SPRINT-ARCHIVE-1.md created with completed work summary"
      },
      {
        "step": "living_sprint_reset",
        "status": "✅ PASS",
        "details": "IN PROGRESS section cleared, Sprint 2 focus updated"
      },
      {
        "step": "sprint_roadmap_update",
        "status": "✅ PASS",
        "details": "SPRINT-ROADMAP.md incremented to Sprint 2"
      },
      {
        "step": "cross_reference_sync",
        "status": "✅ PASS",
        "details": "6 roadmap files updated with Sprint 2 references"
      },
      {
        "step": "validation",
        "status": "✅ PASS",
        "details": "All transition gates validated successfully"
      }
    ],
    "next_sprint": {
      "number": 2,
      "focus": "Validation & Quality Gates",
      "streams_planned": 5,
      "estimated_hours": 42,
      "start_date": "2025-11-16"
    },
    "lessons_learned": [
      "Stream estimation accuracy: 92% (37h estimated vs 40h actual)",
      "Capacity model effective: 3+2 streams completed without bottlenecks",
      "Small stream completion velocity: 3.5h average (target <5h)"
    ]
  }
}
```

---

### 5. Validate Cross-References (`validate_cross_references`)

**Input Requirements**: Validation scope (all roadmaps, specific file, reference type), repair mode (report-only or auto-fix)

**Workflow Phases**:

1. **Analysis**: Read all roadmap files, parse internal references, identify validation targets
2. **Research**: Use Glob to verify file existence, Grep to check ID consistency, build reference graph
3. **Todo Creation**: Generate validation task list for each reference type (file links, IDs, dates, hierarchy)
4. **Implementation**: Execute validation checks, detect broken links, identify inconsistencies, generate error reports
5. **Validation**: Verify validation coverage (all references checked), assess error severity, prioritize fixes
6. **Reflection**: Document common validation failures, recommend prevention strategies, estimate repair effort

**Validation Scope**:
- References between `LIVING_SPRINT.md` ↔ `SPRINT-ROADMAP.md` ↔ `roadmaps/**/*.md`
- Feature plan references (`docs/01-planning/features/**`)
- Specification links (`docs/01-planning/specifications/**`)
- Architecture decision records (`docs/02-architecture/**`)
- Completion date consistency across documents

**Validation Categories**:
- **File Existence**: Referenced documents must exist
- **ID Consistency**: Feature/task IDs must match across documents
- **Date Consistency**: Completion dates must align in all references
- **Hierarchy Integrity**: Parent-child relationships must be bidirectional
- **Status Alignment**: Status fields must match between linked documents

**Output Format**: SUCCESS with validation report and suggested fixes, or FAILURE with graph corruption

**Example Output**:
```json
{
  "status": "SUCCESS",
  "agent": "roadmap-manager",
  "operation_type": "validate_cross_references",
  "confidence": 0.85,
  "agent_specific_output": {
    "validation_scope": "all_roadmaps",
    "total_references": 87,
    "references_validated": 87,
    "validation_results": {
      "file_existence": {
        "checked": 42,
        "passed": 40,
        "failed": 2,
        "errors": [
          {
            "source": "Q1-2026.md",
            "line": 92,
            "reference": "../feature-plans/007-moat-assessment.md",
            "error": "File not found",
            "suggested_fix": "Create missing feature plan or update reference to existing file"
          }
        ]
      },
      "id_consistency": {
        "checked": 28,
        "passed": 28,
        "failed": 0
      },
      "date_consistency": {
        "checked": 17,
        "passed": 15,
        "failed": 2,
        "errors": [
          {
            "feature": "Feature 007",
            "roadmap_date": "2025-11-15",
            "living_sprint_date": "2025-11-17",
            "discrepancy_days": 2,
            "suggested_fix": "Align completion dates to 2025-11-17 (LIVING_SPRINT is source of truth)"
          }
        ]
      },
      "hierarchy_integrity": {
        "checked": 0,
        "passed": 0,
        "failed": 0,
        "note": "Parent-child validation not applicable for current roadmap structure"
      }
    },
    "overall_integrity": 0.95,
    "repair_recommendations": [
      {
        "priority": "HIGH",
        "type": "file_existence",
        "action": "Create docs/01-planning/feature-plans/007-moat-assessment.md",
        "effort": "Medium (2-3 hours)",
        "confidence": 0.90
      },
      {
        "priority": "MEDIUM",
        "type": "date_consistency",
        "action": "Update Q1-2026.md Feature 007 completion date to 2025-11-17",
        "effort": "Low (5 minutes)",
        "confidence": 0.95
      }
    ]
  }
}
```

---

### 6. Generate Health Metrics (`generate_health_metrics`)

**Input Requirements**: Metrics scope (ecosystem-wide, single roadmap, sprint focus), trend analysis period (sprint, month, quarter)

**Workflow Phases**:

1. **Analysis**: Read all roadmap documents, parse structure, extract metadata, calculate health dimensions
2. **Research**: Reference health scoring formulas, compare against best practice thresholds, identify outliers
3. **Todo Creation**: Not typically required (analysis-only workflow)
4. **Implementation**: Calculate 6 health dimensions, aggregate ecosystem score, rank improvement opportunities
5. **Validation**: Verify calculation accuracy, check trend data consistency, validate recommendation priorities
6. **Reflection**: Document health trends over time, identify systemic issues, recommend preventive measures

**Health Dimensions**:
1. **Progressive Disclosure Compliance**: <500 lines target, hierarchical structure, size efficiency
2. **Token Density**: Filler word ratio, active voice percentage, structured format usage
3. **Cross-Reference Integrity**: Broken links, orphaned items, consistency errors
4. **Sprint Model Compliance**: Capacity adherence (3+2 streams), complexity tracking, completion velocity
5. **Freshness**: Last updated timestamps, stale documents (>30 days), inactive roadmaps
6. **Completeness**: Missing required fields (status, dates, owners), undefined completion criteria

**Health Scoring Formula**:
```
Overall_Health = (Progressive_Disclosure × 0.25) +
                 (Token_Density × 0.20) +
                 (Cross_Reference_Integrity × 0.20) +
                 (Sprint_Compliance × 0.15) +
                 (Freshness × 0.10) +
                 (Completeness × 0.10)

Score Ranges:
- Excellent (0.9-1.0): Minimal improvements needed
- Good (0.8-0.89): Minor optimization opportunities
- Fair (0.7-0.79): Moderate improvements recommended
- Poor (0.6-0.69): Major restructuring needed
- Critical (<0.6): Immediate attention required
```

**Output Format**: SUCCESS with health dashboard and prioritized recommendations, or FAILURE with data access issues

**Example Output**: See template-examples.md for complete health metrics dashboard example

---

## Todo Management Protocol

**When to Use**: Sprint transitions (7+ steps), complex roadmap restructuring (5+ files), cross-reference validation (10+ links)

**Creation Timing**: During Analysis phase after task breakdown

**Structure**: Each todo item includes completion criteria, sprint capacity validation, blocking dependency tracking

**Example**:
```json
{
  "todo_items": [
    {
      "id": "sprint_transition_1",
      "description": "Detect sprint completion (validate all 5 streams COMPLETE)",
      "completion_criteria": "LIVING_SPRINT shows 0 in-progress complexity points, all streams have COMPLETE status",
      "dependencies": [],
      "status": "pending"
    },
    {
      "id": "sprint_transition_2",
      "description": "Create sprint archive file SPRINT-ARCHIVE-{N}.md",
      "completion_criteria": "Archive file created with completed work summary, file exists at docs/00-project/operations/",
      "dependencies": ["sprint_transition_1"],
      "status": "pending"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_completion_date",
      "description": "Sprint 2 start date undefined (depends on Sprint 1 completion velocity)",
      "impact": "Cannot accurately update SPRINT-ROADMAP.md dates",
      "resolution_needed": "Estimate Sprint 1 completion or use relative dates ('Post-Sprint 1')"
    }
  ]
}
```

---

## Integration Points

### Orchestrator Coordination

- **Delegation Pattern**: Orchestrator delegates roadmap operations when detecting status update needs, sprint transitions, or documentation optimization opportunities
- **Input Format**: Context string with operation type + target files + update requirements
- **Output Processing**: Orchestrator validates SUCCESS status, checks confidence ≥0.75, applies recommended follow-up actions
- **Failure Handling**: Escalate validation failures to technical-pm, broken links to doc-librarian, capacity violations to orchestrator

### Multi-Agent Workflows

**Upstream Dependencies**:
- technical-pm provides sprint planning data (streams, complexity, owners)
- /spec command creates feature specifications referenced in roadmaps
- plan-enhancer generates implementation plans linked from roadmaps

**Downstream Integration**:
- doc-librarian receives broken link reports for documentation fixes
- technical-pm receives sprint completion signals for retrospectives
- orchestrator receives health metrics for continuous improvement

**State Management**:
- LIVING_SPRINT.md is single source of truth for current sprint state
- Roadmap files maintain historical completion data
- Sprint archives preserve completed work for retrospectives

**Conflict Resolution**:
- LIVING_SPRINT completion dates override roadmap estimates
- Capacity model validation prevents stream overload
- Cross-reference validation detects and reports inconsistencies (manual resolution required)

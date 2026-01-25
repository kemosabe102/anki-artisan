---
name: ecosystem-maintenance
description: >
  Ecosystem health and maintenance operations for .claude/** metadata 
  consistency. Validates cross-document references, syncs registries, repairs 
  broken links, enforces schema compliance through 7-stage auto-fix pipeline.
  
  Use for: "ecosystem health scan", "sync agent registry", "fix broken links", 
  "validate schema compliance".
  Trigger keywords: ecosystem health, bottleneck, sync, auto-fix, validation pipeline.
  
  NOT for: Creating new agents (agent-architect), designing workflow patterns 
  (workflow agent), code implementation (implementation agents), documentation 
  content creation (doc-librarian), modifying agent prompts or capabilities.
---

# Ecosystem Maintenance Skill

Systematic ecosystem health monitoring, validation, and repair through the 7-stage auto-fix pipeline.

## Core Principle

**Validate before modify. Dry-run before commit.** All ecosystem modifications pass through:
1. DRY-RUN → 2. SMOKE → 3. AUTO-FIX → 4. VALIDATE → 5. APPLY → 6. CHECK → 7. VERIFY

---

## Reference Documentation

- **7-Stage Pipeline** -> [references/pipeline-flowchart.md](references/pipeline-flowchart.md)
- **Stage Definitions** -> [references/stage-definitions.md](references/stage-definitions.md)

---

## Operations Overview

| Operation | Purpose | Trigger Keywords |
|-----------|---------|------------------|
| Bottleneck Analysis | Identify workflow friction points | bottleneck, friction, slow |
| Sync Ecosystem | Cross-document synchronization | sync, synchronize, align |
| Health Scan | Ecosystem-wide validation | health, scan, audit |
| Auto-Fix Pipeline | Repair known issues | auto-fix, repair, validate |

---

## 7-Stage Auto-Fix Pipeline (Quick Reference)

| Stage | Action | On Failure |
|-------|--------|------------|
| 1. DRY-RUN | Simulate operation without file changes | Report simulation issues |
| 2. SMOKE TEST | Lightweight validation (paths, links, syntax) | Flag issues, continue |
| 3. AUTO-FIX | Automatic repair of known patterns | Log fixes applied |
| 4. VALIDATE | Full validation against standards | Block if critical |
| 5. APPLY | Execute file modifications | Rollback on error |
| 6. CHECK | Read-back verification | Retry or rollback |
| 7. FINAL VERIFY | Integration testing | Report degradation |

**Retry Limit**: 3 attempts per validation failure before FAILURE status

---

## Bottleneck Analysis Methodology

**Framework**: 5 Whys + Root Cause Analysis

### Process

1. **Gather Evidence**
   - Usage patterns and frequency data
   - User friction reports
   - Execution time measurements
   - Error frequency logs

2. **Identify Friction Points**
   - Slow operations (>5s execution time)
   - High error rates (>5% failure)
   - Frequent user complaints
   - Complex multi-step workflows

3. **Apply 5 Whys**
   ```
   Symptom: "Workflow X is slow"
   Why 1? → Large file scans
   Why 2? → No caching mechanism
   Why 3? → Historical design decision
   Why 4? → Original scope was small
   Why 5? → No scalability requirements
   Root Cause: Missing caching layer for grown scope
   ```

4. **Prioritize by Impact**
   - Impact Score = Frequency × Severity × User Count
   - High (>100): Immediate attention
   - Medium (50-100): Next sprint
   - Low (<50): Backlog

---

## Sync Operations

### Synchronization Scope

| Scope | Target Files | Trigger |
|-------|--------------|---------|
| Agent Registry | `.claude/agents/**/*.md` | Agent modifications |
| Skill Catalog | `.claude/skills/**/SKILL.md` | Skill additions |
| Command Index | `.claude/commands/**/*.md` | Command changes |
| Documentation | `.claude/docs/**/*.md`, `docs/**` | Content updates |

### Sync Process

1. **Parse Documents**
   - Extract metadata (frontmatter)
   - Build dependency graph
   - Identify cross-references

2. **Detect Inconsistencies**
   - Broken links (404 references)
   - Stale references (modified sources)
   - Missing entries (unregistered artifacts)
   - Version mismatches

3. **Generate Patches**
   - Section-level precision targeting
   - Idempotent operations (operation_id + input_hash)
   - Machine-actionable JSON format

4. **Apply with Pipeline**
   - Run full 7-stage pipeline
   - Validate each patch independently
   - Rollback on failure



---

## Ecosystem Health Scanning

### Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Broken Links | 0 | 1-5 | >5 |
| Stale References | 0-2 | 3-10 | >10 |
| Schema Violations | 0 | 1-3 | >3 |
| Path Format Errors | 0 | 1-5 | >5 |

### Scan Categories

1. **Path Validation**
   - Forward slashes enforced
   - Absolute paths required
   - Reference existence verified

2. **Link Verification**
   - Internal markdown links resolve
   - Cross-document references valid
   - External URLs reachable (optional)

3. **Schema Compliance**
   - Frontmatter validates
   - Required fields present
   - Type constraints met

4. **Integration Health**
   - Agent-skill connections valid
   - Command-hook bindings work
   - Registry entries accurate

---

## Validation Gate Definitions

### Pre-Commit Gates

| Gate | Pass Criteria | Block Level |
|------|---------------|-------------|
| Path Normalization | All paths use forward slashes | Hard Block |
| File Reference | All referenced files exist | Hard Block |
| Markdown Syntax | No syntax errors | Soft Block |
| Schema Compliance | Validates against schema | Hard Block |
| Link Verification | Internal links resolve | Soft Block |

### Apply Mode Selection

| Condition | Apply Mode | Rationale |
|-----------|------------|-----------|
| First-time operation | `dry_run` | Validate without side effects |
| Modifying critical files | `dry_run` | Preview changes before commit |
| User explicitly requests | `commit` | Trust user judgment |
| Routine sync operation | `commit` | Low risk, high frequency |
| Analysis operations | N/A | Read-only |

---

## Auto-Fix Patterns

Known patterns with automatic repair capability:

| Issue | Detection | Auto-Fix |
|-------|-----------|----------|
| Backslash paths | `\` in file paths | Convert to forward slashes |
| Relative paths | Paths not starting with `/` or `C:/` | Convert to absolute |
| Missing newlines | No trailing newline | Add `\n` at EOF |
| Broken internal links | Link target not found | Update to correct path |
| Duplicate entries | Same ID appears multiple times | Deduplicate, keep latest |
| Stale timestamps | Last-modified older than file | Update to file mtime |

### Auto-Fix Limits

- **Maximum 3 auto-fix attempts** per validation failure
- Log all fixes applied with before/after
- Escalate to user after retry limit exceeded

---

## Provenance Tracking

All sync operations must include:

```json
{
  "provenance": {
    "operation_id": "01HXYZ...",
    "inputs_hash": "sha256:...",
    "apply_mode": "dry_run|commit",
    "processing_time_ms": 1234,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Idempotency Requirements

- Same `operation_id` + `inputs_hash` = same result
- Re-running operation should be safe
- No duplicate side effects

---

## Output Structures

### SUCCESS Response

```json
{
  "status": "SUCCESS",
  "operation_type": "sync_ecosystem|health_scan|auto_fix",
  "summary": "Brief description of what was accomplished",
  "validation_checklist": {
    "checks_performed": ["path_validation", "syntax_check", "integration_test"],
    "all_checks_passed": true
  },
  "changes": [
    {"path": "...", "action": "create|update|delete", "summary": "..."}
  ],
  "provenance": {...},
  "next_actions": ["Recommended follow-up steps"]
}
```

### FAILURE Response

```json
{
  "status": "FAILURE",
  "operation_type": "...",
  "summary": "What failed and why",
  "validation_checklist": {
    "checks_performed": ["..."],
    "all_checks_passed": false,
    "failed_checks": [{"check_name": "...", "reason": "..."}]
  },
  "failure_details": {
    "failure_type": "validation_error|timeout|dependency_missing",
    "reasons": ["Specific failure reasons"],
    "recovery_suggestions": ["How to fix"]
  }
}
```

---

## Termination Rules

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Operation timeout | 600 seconds | FAILURE with partial results |
| Auto-fix retry limit | 3 attempts | FAILURE, escalate to user |
| CQ iteration limit | 3 research cycles | FAILURE, request guidance |
| Critical validation failure | 1 | Hard block, no proceed |

---

## Anti-Patterns (NEVER DO)

- Skip DRY-RUN for first-time operations
- Apply changes without read-back verification
- Ignore validation failures and proceed
- Modify files outside ecosystem scope
- Make multiple changes simultaneously without tracking
- Accept "it works" without understanding why fix worked

---

## Quick Start by Task

**Analyze Bottleneck**:
1. Gather usage evidence
2. Apply 5 Whys methodology
3. Calculate impact scores
4. Prioritize recommendations

**Sync Documents**:
1. Parse target documents
2. Build dependency graph
3. Detect inconsistencies
4. Generate patches
5. Run 7-stage pipeline

**Health Scan**:
1. Select scan scope
2. Run all validation checks
3. Categorize findings
4. Generate health report

**Run Auto-Fix**:
1. Identify known patterns
2. DRY-RUN simulation
3. Apply fixes with logging
4. Verify with read-back


---
name: documentation-health
description: >
  Validates documentation ecosystem health through link checking, orphan detection, 
  staleness analysis, and health scoring (0-100). Use when: "audit docs", "doc health", 
  "broken links", "find orphans", "staleness report", "validate documentation". 
  NOT for: content creation (documentation-synthesis), optimization (documentation-optimization).
---

# Documentation Health

> **Systematic validation of documentation quality through link health, orphan detection, and staleness analysis.**

---

## When to Use This Skill

**Trigger Keywords**: "audit docs", "doc health", "broken links", "find orphans", "staleness report", "validate documentation"

**Use For**:
- Link validation (internal and external)
- Orphan file detection (no incoming references)
- Staleness analysis (file age, reference freshness)
- Health scoring (0-100 calculation)
- Naming convention validation (kebab-case)

**NOT For**:
- Content creation (use documentation-synthesis)
- Content optimization (use documentation-optimization)
- Git operations (orchestrator handles)
- Modifications outside `docs/**` or `.claude/docs/**`

---

## Core Methodology

### Three-Tier Safety Model

| Tier | Capability | Operations | Approval |
|------|------------|------------|----------|
| **1** | Read-only analysis | Scan, validate, report | Always safe |
| **2** | Automated safe fixes | Link updates, rename files | Auto (with verification) |
| **3** | Supervised restructuring | Move files, reorganize | User required |

**Tier Selection**:
- Keywords "check", "health", "audit", "analyze" → Tier 1
- Keywords "fix", "correct", "repair", "update" → Tier 2
- Keywords "restructure", "reorganize", "move" → Tier 3
- Ambiguous → Default to Tier 1, ask clarification

### Link Validation Strategy

**Process**: Glob → Extract → Validate → Classify → Report/Fix

**Extraction**:
```regex
\[.*?\]\((.*?)\)
```
Captures link targets from Markdown `[text](target)` syntax

**Validation**:
- **Internal links**: File existence check at path
- **External links**: HTTP status validation (optional, resource-intensive)
- **Anchor links**: Section header validation in target file

**Classification**:
- `valid` - Target exists and accessible
- `broken` - Target not found (404, file missing)
- `ambiguous` - Relative path interpretation unclear
- `external_unchecked` - HTTP link not validated (Tier 1)

### Orphan Detection Algorithm

**Definition**: File with zero incoming references from other documentation files

**Process**:
1. Build reference map: File → [files that reference it]
2. Identify files with empty reference arrays
3. Classify orphan type:
   - `root_orphan` - Top-level file (README.md, index.md) - expected
   - `leaf_orphan` - Deep file with no references - unexpected
   - `archive_candidate` - Old orphan (>180 days) - archive recommended

**Exclusions**: Files matching patterns in `DOCS-MANAGEMENT.md` exceptions

### Staleness Detection

**File Age Thresholds** (from last modified date):
- `fresh` - <30 days
- `recent` - 30-90 days
- `aging` - 90-180 days
- `stale` - 180-365 days
- `outdated` - >365 days

**Reference Freshness**:
- Count outbound links to files in each age category
- High ratio of links to `stale`/`outdated` files indicates content staleness
- Formula: `staleness_score = (stale_links + 2*outdated_links) / total_links`

**Staleness Alert Criteria**:
- File age >180 days AND staleness_score >0.5
- File age >365 days (always flagged)

### Health Score Calculation

**Formula** (0-100 range):
```
health_score = 100 - (
  critical_violations * 10 +
  high_violations * 5 +
  medium_violations * 2 +
  low_violations * 1
)
```
**Floor**: Minimum score is 0 (negative not allowed)

**Severity Classification**:
- **Critical**: Broken links in root documentation (README.md, index.md)
- **High**: Broken links in active documentation (<90 days old)
- **Medium**: Orphaned files, naming violations, stale references
- **Low**: External links unchecked, minor formatting issues

**Grading Scale**:
- 90-100: Excellent (A)
- 75-89: Good (B)
- 60-74: Fair (C)
- 40-59: Poor (D)
- 0-39: Critical (F)

---

## Scope Validation

**Valid Scope Patterns**:
- `docs/**` - Main documentation tree
- `.claude/docs/**` - Claude-specific docs
- `docs/00-project/` - Specific subdirectory
- `*.md` within allowed directories

**Invalid Scope** (reject immediately):
- Paths with `../` (traversal attempt)
- Absolute paths outside repo root
- Paths containing `node_modules/`, `.git/`, `__pycache__/`
- Empty or null scope

**Action**: If scope invalid → FAIL with `invalid_scope` error, do NOT proceed

---

## Validation Workflow

### Phase 1: Research (Tier 1 Required)

Before any operations, gather:
- [ ] Current file count in scope
- [ ] Existing naming patterns (kebab-case compliance %)
- [ ] Link inventory (internal vs external count)
- [ ] Known exceptions from `DOCS-MANAGEMENT.md`

**Tools**: Glob, Read, Grep

### Phase 2: Analysis (All Tiers)

Execute validation checks:
- [ ] Extract all Markdown links from files
- [ ] Validate internal links (file existence)
- [ ] Detect orphaned files (zero incoming references)
- [ ] Calculate file ages from last modified date
- [ ] Check naming conventions (kebab-case)
- [ ] Classify violations by severity

**Tools**: Read, Grep (pattern matching)

### Phase 3: Scoring (All Tiers)

Calculate health metrics:
- [ ] Count violations by severity (critical/high/medium/low)
- [ ] Apply health score formula
- [ ] Calculate staleness scores for aged files
- [ ] Generate coverage percentage (files scanned / total files)

**Output**: Health score (0-100), grade (A-F), violation breakdown

### Phase 4: Remediation (Tier 2+)

Apply automated fixes:
- [ ] Update broken internal links (if target moved)
- [ ] Rename files to kebab-case (with link updates)
- [ ] Remove dead links (if target permanently deleted)
- [ ] Add references to orphaned files (if appropriate)

**Tools**: mcp__desktop-commander__edit_block, mcp__desktop-commander__write_file

**Safety**: Read before Edit, verify after Edit

### Phase 5: Verification (Tier 2+ Required)

After modifications:
- [ ] Read back all edited files
- [ ] Re-run link validation
- [ ] Confirm no new broken links introduced
- [ ] Calculate new health score (before/after comparison)
- [ ] Log changes with file:line references

**Output**: Verification report, delta metrics

---

## Output Format

### Health Report Structure

```json
{
  "health_score": 85,
  "grade": "B",
  "coverage": "100%",
  "files_scanned": 45,
  "violations": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 8
  },
  "details": {
    "broken_links": [
      {"file": "docs/guide.md", "line": 23, "target": "missing.md", "severity": "high"}
    ],
    "orphans": [
      {"file": "docs/old-doc.md", "age_days": 210, "type": "archive_candidate"}
    ],
    "stale_files": [
      {"file": "docs/legacy.md", "age_days": 400, "staleness_score": 0.67}
    ]
  },
  "recommendations": [
    {"priority": 1, "action": "Fix 2 broken links in active docs", "effort": "5 min"},
    {"priority": 2, "action": "Archive 1 orphaned file >180 days", "effort": "2 min"}
  ]
}
```

### Two-State Model

**SUCCESS**: Health score calculated, all validations completed, no tool errors
**FAILURE**: Scope invalid, permission denied, or critical tool error

---

## Parallel Execution

**Parallelize** (safe concurrent operations):
- Glob scans across different directories
- Independent file Reads (no cross-file dependencies)
- Link validation on separate files
- Health checks on independent doc trees

**Serialize** (must run sequentially):
- Edits to same file
- Cross-reference updates (A links to B, B links to A)
- Fixes that depend on prior fix results
- Any Tier 3 operations

**Batch Limits**: Max 10 files per parallel Read batch

---

## Anti-Patterns

**NEVER**:
- Modify content (structure/metadata only)
- Delete files without explicit user approval
- Perform git operations (orchestrator handles)
- Edit outside `docs/**` or `.claude/docs/**`
- Parallel edits on same file
- Skip read-back verification after edits

**ALWAYS**:
- Read before Edit (mandatory)
- Sequential file operations with read-back verification
- Classify violations by severity
- Provide actionable recommendations with effort estimates
- Document coverage percentage for partial scans

---

## Naming Convention Validation

**Standard**: kebab-case for all Markdown files

**Valid Examples**:
- `getting-started.md`
- `api-reference.md`
- `01-introduction.md` (numbered prefix allowed)

**Invalid Examples**:
- `GettingStarted.md` (PascalCase)
- `getting_started.md` (snake_case)
- `getting started.md` (spaces)

**Detection**: Grep for files matching `[A-Z_\s]` patterns in filenames

**Fix**: Tier 2 can auto-rename with link updates across all referencing files

---

## Error Recovery

**Inherits from**: `base-agent-pattern.md` (standard retry, backoff, escalation)

**Documentation-Health Specific**:
- **Link 404**: Log as permanent failure, suggest removal or update
- **File permission denied**: Escalate to user, do not retry
- **Scope validation failed**: FAIL immediately, no partial execution
- **External link timeout**: Mark as `external_unchecked`, continue scan

---

## Reference Files

See `references/` directory for detailed specifications:
- `link-validation-patterns.md` - Regex patterns, HTTP validation details
- `health-score-formula.md` - Complete calculation methodology
- `staleness-detection.md` - Age thresholds, freshness rules, alert criteria

---

## Examples

### Example 1: Basic Health Check (Tier 1)

**Input**: "Check doc health for docs/guides/"

**Process**:
1. Glob `docs/guides/**/*.md`
2. Extract links from each file
3. Validate internal links (file existence)
4. Detect orphans (zero incoming references)
5. Calculate health score
6. Generate report with recommendations

**Output**: Health score 78 (C), 3 broken links (high), 2 orphans (medium)

### Example 2: Fix Broken Links (Tier 2)

**Input**: "Fix broken links in docs/"

**Process**:
1. Run Tier 1 health check
2. Identify fixable broken links (target moved but exists elsewhere)
3. Update link targets using `edit_block`
4. Read back to verify changes
5. Re-run validation
6. Report before/after health scores

**Output**: Health score improved from 65 to 92, fixed 8/10 broken links

### Example 3: Staleness Report (Tier 1)

**Input**: "Find stale documentation"

**Process**:
1. Glob all markdown files
2. Get last modified timestamp for each file
3. Calculate age in days
4. Analyze outbound links to categorize by target age
5. Calculate staleness scores
6. Filter files with age >180 days OR staleness_score >0.5

**Output**: 5 stale files identified, 3 outdated (>365 days)

---

## Integration Points

**Coordinates with**:
- `documentation-synthesis` - Creates content after health validation passes
- `documentation-optimization` - Improves content quality based on health metrics
- `documentation` agent - Executes this skill for health management tasks
- `DOCS-MANAGEMENT.md` - Defines organization rules and exceptions

**Dependencies**:
- Requires `DOCS-MANAGEMENT.md` for exception patterns
- Assumes kebab-case naming standard
- Expects Markdown link syntax `[text](target)`

---

## Quick Reference

**Scope**: `docs/**`, `.claude/docs/**` only  
**Health Score**: 0-100 (90+ = A, 75-89 = B, 60-74 = C, 40-59 = D, <40 = F)  
**Tiers**: 1=Read-only, 2=Auto-fix, 3=Supervised  
**Severity**: Critical (10 pts), High (5 pts), Medium (2 pts), Low (1 pt)  
**Staleness**: >180 days = stale, >365 days = outdated  
**Max Parallel Reads**: 10 files

**Common Patterns**:
- "doc health" → Tier 1 full scan
- "fix links" → Tier 2 link repair
- "find orphans" → Tier 1 orphan detection
- "staleness report" → Tier 1 age analysis

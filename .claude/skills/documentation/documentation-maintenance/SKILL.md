---
name: documentation-maintenance
description: >
  Manages ongoing documentation maintenance including scheduled health checks, 
  deprecation tracking, version alignment, and staleness monitoring. Enables 
  proactive documentation management rather than reactive fixes.
  Use when: "track deprecations", "sync versions", "set staleness alerts", 
  "schedule doc monitoring", "documentation lifecycle", "version alignment".
  NOT for: immediate fixes (documentation-health), generation (documentation-synthesis).
---

# Documentation Maintenance Skill

**Domain**: Documentation Management  
**Type**: Proactive Maintenance  
**Coordination**: Orchestrates preventive documentation care

---

## Purpose

This skill manages **ongoing documentation maintenance** through scheduled monitoring, deprecation tracking, version alignment, and staleness detection. It prevents documentation debt by enabling proactive management rather than reactive fixes.

**Use this skill when:**
- Setting up scheduled documentation health checks
- Tracking deprecations and sunset timelines
- Synchronizing documentation with code versions
- Configuring staleness alerts and thresholds
- Managing documentation lifecycle transitions
- Establishing documentation versioning strategies

**NOT for:**
- Immediate documentation fixes (use `documentation-health`)
- New documentation generation (use `documentation-synthesis`)
- One-time audits (use `documentation-health`)

---

## Core Capabilities

### 1. Scheduled Health Checks

Configure automated documentation scans to catch issues before they become critical.

**Frequency Recommendations:**

| Check Type | Frequency | Scope |
|------------|-----------|-------|
| Quick scan | Weekly | Changed files since last check |
| Standard audit | Monthly | Full documentation tree |
| Deep analysis | Quarterly | Cross-references, dependencies, architecture alignment |
| Version sync | On release | Changelog, API docs, version markers |

**Automated Scan Configuration:**

```yaml
# Example maintenance schedule configuration
schedule:
  weekly_scan:
    enabled: true
    day: Monday
    checks:
      - broken_links
      - missing_descriptions
      - outdated_dates
    
  monthly_audit:
    enabled: true
    day_of_month: 1
    checks:
      - cross_reference_integrity
      - orphaned_documents
      - version_alignment
      - staleness_review
    
  quarterly_review:
    enabled: true
    months: [3, 6, 9, 12]
    checks:
      - architecture_alignment
      - dependency_updates
      - deprecation_cleanup
      - comprehensive_health_score
```

**Alert Thresholds:**

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Broken links | >3 | >10 | Escalate to documentation-health |
| Orphaned docs | >2 | >5 | Immediate triage |
| Stale docs (>90d) | >10% | >25% | Schedule refresh sprint |
| Version mismatches | Any | N/A | Block release |
| Missing deprecation docs | >1 | >3 | Escalate to planning |

### 2. Deprecation Tracking

Manage the full lifecycle of deprecated features, APIs, and documentation sections.

**Deprecation Markers:**

```markdown
<!-- Standard deprecation notice -->
> **DEPRECATED**: This feature is deprecated as of v2.3.0 and will be removed in v3.0.0.
> Migration: Use `new_feature()` instead. See [Migration Guide](../migrations/feature-v3.md).
> Sunset: 2025-06-01

<!-- Code-level marker -->
@deprecated(since="2.3.0", remove_in="3.0.0", alternative="new_feature")
```

**Deprecation Lifecycle:**

1. **Announcement** (Release N): Add deprecation markers, document alternatives
2. **Grace Period** (N → N+1): Maintain both old and new, track usage
3. **Warning** (Release N+1): Emit warnings, update migration docs
4. **Sunset** (Release N+2): Remove deprecated feature, archive docs
5. **Cleanup**: Remove references, update cross-links

**Tracking Requirements:**
- Deprecation date and version
- Sunset date and version (minimum 2 releases or 6 months)
- Migration path documentation
- Alternative feature/API
- Impact assessment (affected users, code paths)

**Orphan Prevention:**
When removing deprecated docs, ensure:
- No active cross-references remain
- Migration guides are complete
- Changelog entries are accurate
- Archive is accessible (if needed for historical reference)

See: `references/deprecation-tracking.md` for detailed patterns

### 3. Version Alignment

Keep documentation synchronized with code versions across all documentation types.

**Version Synchronization Checklist:**

| Documentation Type | Sync Trigger | Verification |
|--------------------|--------------|--------------|
| API documentation | Code change merged | Schema matches implementation |
| Changelog | Release tagged | All PRs since last release documented |
| Version badges | Release published | Badges show current version |
| Installation guides | Dependencies updated | Commands use correct versions |
| Migration guides | Breaking change | Old → new examples accurate |
| Architecture docs | Major refactor | Diagrams reflect current structure |

**Changelog Synchronization Pattern:**

```markdown
# CHANGELOG.md

## [2.3.0] - 2025-01-15

### Added
- New feature X (#123) - [Docs](./docs/features/x.md)

### Changed  
- Updated API endpoint Y (#124) - [Migration](./docs/migrations/y-v2.3.md)

### Deprecated
- Old method Z - removal in v3.0.0 (#125) - [Alternative](./docs/api/new-z.md)

### Fixed
- Bug in process W (#126) - [Details](./docs/troubleshooting/w-fix.md)

### Removed
- Deprecated feature V (sunset from v2.0.0) (#127)

[2.3.0]: https://github.com/org/repo/compare/v2.2.0...v2.3.0
```

**API Documentation Version Matching:**

```yaml
# Ensure API docs match implementation
api_docs:
  version: "2.3.0"  # Must match code version
  generated_from: "src/api/v2/**/*.py"
  last_sync: "2025-01-15T10:30:00Z"
  breaking_changes_since_last: []
  
  endpoints:
    - path: "/api/v2/data"
      method: "GET"
      code_ref: "src/api/v2/data.py:get_data"
      doc_ref: "docs/api/endpoints/data.md"
      last_verified: "2025-01-15"
```

**Breaking Change Documentation:**
- Document BEFORE merging breaking change
- Include before/after examples
- Link to migration guide
- Update version compatibility matrices
- Test all documented examples

See: `references/version-alignment.md` for sync strategies

### 4. Staleness Monitoring

Detect and escalate documentation that becomes outdated over time.

**Age-Based Thresholds:**

| Document Type | Review Age | Update Age | Critical Age | Action |
|---------------|------------|------------|--------------|--------|
| API docs | 30 days | 60 days | 90 days | Auto-escalate |
| Guides/tutorials | 60 days | 90 days | 180 days | Schedule review |
| Architecture | 90 days | 120 days | 180 days | Quarterly audit |
| Reference | 120 days | 180 days | 365 days | Annual refresh |
| Changelog | N/A | On release | N/A | Version-triggered |

**Staleness Calculation:**

```python
# Conceptual example - NOT executable
staleness_score = (
    days_since_last_edit * 0.4 +
    days_since_code_change * 0.3 +
    broken_links_count * 10 +
    outdated_references_count * 5
)

# Thresholds
if staleness_score > 100:
    escalate_to_critical()
elif staleness_score > 50:
    schedule_review()
elif staleness_score > 25:
    flag_for_monitoring()
```

**Reference Freshness Checks:**

Monitor documentation dependencies:
- External links (check HTTP status monthly)
- Internal cross-references (verify targets exist weekly)
- Code examples (verify syntax/APIs quarterly)
- Version numbers (check on every release)
- Screenshots/diagrams (review when UI changes)

**Auto-Escalation Rules:**

```yaml
escalation_rules:
  critical_staleness:
    condition: age > 90 days AND (broken_links > 3 OR code_changed)
    action: Create high-priority ticket
    assignee: documentation_team
    
  version_mismatch:
    condition: doc_version != code_version
    action: Block release
    notification: release_manager
    
  orphaned_document:
    condition: no_incoming_links AND age > 60 days
    action: Review for deprecation
    assignee: content_owner
    
  missing_migration:
    condition: breaking_change AND no_migration_doc
    action: Block merge
    notification: pr_author
```

See: `references/staleness-thresholds.md` for detailed criteria

---

## Maintenance Workflow

**5-Step Process:**

### Step 1: TRIAGE
Scan documentation tree and categorize issues:

| Category | Examples | Priority |
|----------|----------|----------|
| Blocking | Version mismatch, broken critical links | P0 - Immediate |
| Degrading | Stale API docs, missing deprecation notices | P1 - This week |
| Technical debt | Orphaned docs, old screenshots | P2 - This sprint |
| Optimization | Style inconsistencies, minor improvements | P3 - Backlog |

### Step 2: PRIORITIZE
Score issues using impact × urgency matrix:

```
Impact Score:
- Affects users: 3 points
- Affects developers: 2 points  
- Internal only: 1 point

Urgency Score:
- Blocks release/deployment: 5 points
- Degrades user experience: 3 points
- Technical debt: 1 point

Final Priority = Impact × Urgency
```

### Step 3: SCHEDULE
Assign issues to maintenance windows:

- **Immediate** (P0): Within 24 hours
- **Short-term** (P1): Within current sprint
- **Medium-term** (P2): Next sprint
- **Long-term** (P3): Backlog, quarterly reviews

### Step 4: EXECUTE
Delegate to appropriate agents:

| Issue Type | Delegate To |
|------------|-------------|
| Content fixes | `documentation-health` skill |
| New documentation | `documentation-synthesis` skill |
| Version alignment | Coordinate with release manager |
| Deprecation updates | Coordinate with feature owners |
| Architecture sync | `architecture` agent |

### Step 5: VERIFY
Post-maintenance validation:

- Run health checks to confirm issues resolved
- Verify no new issues introduced
- Update maintenance logs
- Adjust thresholds if needed

---

## Integration Points

### With Other Documentation Skills

**documentation-health** (reactive):
- Maintenance identifies issues → health performs fixes
- Health escalates recurring issues → maintenance adjusts monitoring

**documentation-synthesis** (generative):
- Maintenance identifies gaps → synthesis creates new docs
- Synthesis outputs → maintenance adds to monitoring

### With Development Workflow

**Pre-Merge Checks:**
- Version alignment verification
- Breaking change documentation check
- Migration guide requirement

**Pre-Release Checks:**
- Changelog completeness
- API doc synchronization
- Deprecation notice accuracy

**Post-Release Actions:**
- Update version badges
- Archive old version docs
- Activate new deprecation timers

---

## Maintenance Metrics

Track documentation health over time:

| Metric | Calculation | Target |
|--------|-------------|--------|
| Documentation coverage | (Documented features / Total features) × 100 | >90% |
| Staleness rate | (Stale docs / Total docs) × 100 | <10% |
| Orphan rate | (Orphaned docs / Total docs) × 100 | <5% |
| Version sync accuracy | (Aligned docs / Version-sensitive docs) × 100 | 100% |
| Broken link rate | (Broken links / Total links) × 100 | <1% |
| Deprecation compliance | (Properly documented deprecations / Total) × 100 | 100% |
| Mean time to update | Average days from code change to doc update | <7 days |

**Dashboard Example:**

```markdown
# Documentation Health Dashboard - 2025-01-15

## Overall Health: 87/100 (Good)

### Key Metrics
- Coverage: 92% (Target: >90%) ✓
- Staleness: 12% (Target: <10%) ⚠️
- Broken links: 0.3% (Target: <1%) ✓
- Version sync: 100% (Target: 100%) ✓

### Action Items
1. [P1] Update 8 stale API docs (>90 days old)
2. [P2] Review 3 orphaned guides for deprecation
3. [P3] Refresh 5 tutorial screenshots

### Upcoming Maintenance
- Next weekly scan: 2025-01-20
- Next monthly audit: 2025-02-01
- Next quarterly review: 2025-03-01
```

---

## Best Practices

### Proactive Maintenance Patterns

1. **Version-Triggered Automation**
   - Run full sync check on every release tag
   - Auto-generate changelog entries from PR labels
   - Update version badges automatically

2. **Early Warning System**
   - Alert when docs unchanged for 75% of threshold
   - Flag PRs that change documented APIs
   - Notify doc owners of upcoming deprecations

3. **Continuous Monitoring**
   - Link checker runs nightly
   - Reference validator runs on commits
   - Version alignment check runs on releases

4. **Documentation Ownership**
   - Assign CODEOWNERS for docs/
   - Require doc review for API changes
   - Track ownership in frontmatter

### Common Anti-Patterns

**AVOID:**
- Waiting for user reports to fix stale docs
- Manual version number updates across files
- Deprecating without migration documentation
- Removing docs without checking cross-references
- Setting thresholds but not monitoring them
- Scheduling reviews but not executing them

**INSTEAD:**
- Use automated monitoring and alerts
- Maintain single source of truth for versions
- Enforce deprecation policy with gates
- Validate references before removal
- Implement threshold-based auto-escalation
- Integrate maintenance into sprint planning

---

## Quick Reference

### Maintenance Command Patterns

**Schedule health check:**
```
Set up weekly documentation scans checking:
- Broken links
- Missing descriptions  
- Outdated dates
Alert if >3 broken links found
```

**Track deprecation:**
```
Track deprecation of [feature] in version [X.Y.Z]:
- Sunset date: [date]
- Alternative: [new_feature]
- Migration guide: [path]
- Update cross-references
```

**Align versions:**
```
Synchronize documentation with version [X.Y.Z]:
- Update API docs from [code_path]
- Generate changelog entries
- Verify version badges
- Check breaking change docs
```

**Monitor staleness:**
```
Monitor documentation staleness:
- API docs: update if >60 days old
- Guides: review if >90 days old
- Alert critical if >90 days + broken links
- Auto-escalate high-priority issues
```

**Triage maintenance backlog:**
```
Triage documentation issues:
- Categorize by type (blocking/degrading/debt)
- Score by impact × urgency
- Schedule by priority (P0-P3)
- Delegate to appropriate agents
```

---

## Related Skills

- **documentation-health**: Executes fixes identified by maintenance monitoring
- **documentation-synthesis**: Generates new docs to fill gaps found by maintenance
- **architecture**: Validates architecture alignment during quarterly reviews

---

## References

- `references/deprecation-tracking.md` - Deprecation lifecycle and markers
- `references/version-alignment.md` - Version synchronization strategies
- `references/staleness-thresholds.md` - Age rules and escalation criteria

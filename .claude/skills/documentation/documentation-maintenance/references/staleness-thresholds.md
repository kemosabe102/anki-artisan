# Staleness Thresholds Reference

**Purpose**: Define age-based rules and escalation criteria for documentation freshness monitoring.

---

## Age-Based Thresholds

### Document Type Classifications

Different documentation types have different staleness tolerances:

| Document Type | Review Age | Update Age | Critical Age | Rationale |
|---------------|------------|------------|--------------|-----------|
| **API Reference** | 30 days | 60 days | 90 days | High-change, user-facing |
| **Guides/Tutorials** | 60 days | 90 days | 180 days | Medium-change, learning path |
| **Architecture Docs** | 90 days | 120 days | 180 days | Low-change, structural |
| **Reference Tables** | 120 days | 180 days | 365 days | Very low-change |
| **Changelog** | N/A | On release | N/A | Event-triggered |
| **Migration Guides** | N/A | On deprecation | N/A | Lifecycle-triggered |
| **Troubleshooting** | 45 days | 75 days | 120 days | Medium-high-change |
| **Installation Docs** | 30 days | 60 days | 90 days | High-change, critical path |

### Age Definitions

**Review Age**: Time since last update when document should be reviewed for accuracy
**Update Age**: Time since last update when document likely needs updates
**Critical Age**: Maximum age before document is considered critically stale

---

## Staleness Calculation

### Multi-Factor Scoring

Staleness is not just about age - consider multiple factors:

```python
# Conceptual formula - NOT executable
staleness_score = (
    days_since_last_edit * 0.4 +           # Time factor
    days_since_related_code_change * 0.3 +  # Code alignment
    broken_links_count * 10 +               # Link health
    outdated_references_count * 5 +         # Reference freshness
    version_mismatch_penalty * 20           # Version sync
)

# Classification
if staleness_score > 100:
    status = "CRITICAL"
    action = "Immediate review required"
elif staleness_score > 50:
    status = "WARNING"
    action = "Schedule review this week"
elif staleness_score > 25:
    status = "WATCH"
    action = "Flag for monitoring"
else:
    status = "FRESH"
    action = "No action needed"
```

### Factors Explained

**Time Factor (40% weight)**:
- Primary indicator: days since last meaningful edit
- Excludes trivial edits (typo fixes, formatting)
- Based on document type thresholds

**Code Alignment (30% weight)**:
- Days since related code was modified
- Detects doc/code drift
- Links via code references in frontmatter

**Link Health (10 points per broken link)**:
- Broken internal links suggest abandonment
- Broken external links indicate outdated references
- Each broken link significantly increases staleness

**Reference Freshness (5 points per outdated reference)**:
- Citations to deprecated features
- Links to old version docs
- References to removed components

**Version Mismatch Penalty (20 points)**:
- Documented version != current code version
- Critical for API documentation
- Binary penalty (either aligned or not)

---

## Escalation Criteria

### Automatic Escalation Rules

Define when to escalate stale documentation to human attention:

| Condition | Priority | Action | Assignee |
|-----------|----------|--------|----------|
| Age > critical threshold | P1 | Create ticket within 24h | Doc team |
| Staleness score > 100 | P0 | Immediate review | Content owner |
| Broken links > 3 AND age > 60d | P1 | Review this week | Doc team |
| Version mismatch on API docs | P0 | Block release | Release manager |
| Orphaned doc (no incoming links) + age > 60d | P2 | Review for deprecation | Content owner |
| Related code changed + age > 30d | P1 | Verify accuracy | Code author |

### Escalation Workflow

```yaml
# .escalation-rules.yml
rules:
  critical_staleness:
    condition: staleness_score > 100
    priority: P0
    action: create_ticket
    assignee: content_owner
    notification:
      - slack_channel: "#docs-urgent"
      - email: docs-team@example.com
    
  version_mismatch:
    condition: doc_version != code_version AND type == "api"
    priority: P0
    action: block_release
    assignee: release_manager
    notification:
      - slack_channel: "#releases"
      - block_merge: true
    
  high_staleness:
    condition: staleness_score > 50
    priority: P1
    action: schedule_review
    assignee: doc_team
    notification:
      - add_to_sprint_backlog: true
    
  orphaned_document:
    condition: incoming_links == 0 AND age > 60
    priority: P2
    action: review_for_deprecation
    assignee: content_owner
```

---

## Reference Freshness Checks

### Internal Reference Monitoring

Track the health of internal documentation cross-references:

**Check Types:**

1. **Link Validation** (Daily)
   - Verify all internal links resolve
   - Check anchor links point to existing sections
   - Flag moved/renamed files

2. **Cross-Reference Integrity** (Weekly)
   - Verify bidirectional link consistency
   - Check for orphaned documents
   - Validate navigation paths

3. **Code Example Verification** (Monthly)
   - Test code snippets for syntax errors
   - Verify API calls use current methods
   - Check import statements are valid

4. **Version Reference Audit** (On Release)
   - Check version numbers in examples
   - Verify compatibility tables
   - Update installation commands

### External Reference Monitoring

Track external dependencies that affect documentation freshness:

**Check Types:**

1. **HTTP Link Health** (Weekly)
   - Verify external links return 200 OK
   - Flag 404s, 301s (moved), 5xx (server errors)
   - Update redirected links

2. **Third-Party API References** (Monthly)
   - Verify documented APIs still exist
   - Check for version changes
   - Update deprecated endpoints

3. **Screenshot/Diagram Currency** (Quarterly)
   - Review UI screenshots for accuracy
   - Update architecture diagrams
   - Refresh flowcharts if process changed

**External Link Health Scoring:**

```python
# Conceptual example - NOT executable
def score_external_link(url, last_checked, http_status):
    if http_status == 200:
        return 0  # Healthy
    elif http_status == 404:
        return 20  # Broken, needs update
    elif http_status in [301, 302]:
        return 5   # Redirected, should update
    elif http_status >= 500:
        return 10  # Server error, recheck later
    else:
        return 15  # Other error
```

---

## Monitoring Configuration

### Threshold Configuration File

```yaml
# .staleness-config.yml
thresholds:
  api_docs:
    review_age: 30
    update_age: 60
    critical_age: 90
    
  guides:
    review_age: 60
    update_age: 90
    critical_age: 180
    
  architecture:
    review_age: 90
    update_age: 120
    critical_age: 180

scoring:
  time_weight: 0.4
  code_alignment_weight: 0.3
  broken_link_penalty: 10
  outdated_reference_penalty: 5
  version_mismatch_penalty: 20
  
  thresholds:
    critical: 100
    warning: 50
    watch: 25

checks:
  link_validation:
    frequency: daily
    types: [internal, external]
    
  cross_reference_integrity:
    frequency: weekly
    
  code_example_verification:
    frequency: monthly
    
  version_reference_audit:
    frequency: on_release
```

### Custom Thresholds

Adjust thresholds based on project needs:

```yaml
# Override defaults for specific documents
overrides:
  - path: "docs/api/critical-endpoint.md"
    review_age: 14
    update_age: 30
    critical_age: 45
    rationale: "Critical user-facing API"
    
  - path: "docs/internal/processes.md"
    review_age: 180
    update_age: 365
    critical_age: 730
    rationale: "Low-change internal documentation"
```

---

## Early Warning System

### Progressive Alerts

Alert before documents become critically stale:

| Alert Level | Trigger | When | Action |
|-------------|---------|------|--------|
| Info | 50% of review age | Age = 15d (API) | Log only |
| Warning | 75% of review age | Age = 23d (API) | Notify owner |
| Alert | Review age reached | Age = 30d (API) | Schedule review |
| Critical | Update age reached | Age = 60d (API) | Escalate to team |
| Emergency | Critical age reached | Age = 90d (API) | Block release |

### Alert Configuration

```yaml
# .alert-config.yml
alerts:
  info:
    threshold_percentage: 0.5
    notification: log
    
  warning:
    threshold_percentage: 0.75
    notification:
      - email: content_owner
      - slack: false
    
  alert:
    threshold_percentage: 1.0  # Review age
    notification:
      - email: content_owner
      - slack_channel: "#docs-alerts"
      - add_to_backlog: true
    
  critical:
    threshold_percentage: 2.0  # Update age (2x review age)
    notification:
      - email: [content_owner, doc_team]
      - slack_channel: "#docs-urgent"
      - create_ticket: true
      - priority: P1
    
  emergency:
    threshold_percentage: 3.0  # Critical age (3x review age)
    notification:
      - email: [content_owner, doc_team, release_manager]
      - slack_channel: "#docs-urgent"
      - create_ticket: true
      - priority: P0
      - block_release: true
```

---

## Staleness Dashboard

### Metrics to Track

Monitor documentation health over time:

```markdown
# Staleness Dashboard - 2025-01-15

## Overall Health: 85/100 (Good)

### By Document Type
| Type | Total | Fresh | Watch | Warning | Critical |
|------|-------|-------|-------|---------|----------|
| API Docs | 45 | 38 (84%) | 5 (11%) | 2 (4%) | 0 (0%) |
| Guides | 28 | 22 (79%) | 4 (14%) | 2 (7%) | 0 (0%) |
| Architecture | 12 | 10 (83%) | 2 (17%) | 0 (0%) | 0 (0%) |

### Staleness Distribution
- Fresh (<25): 70 docs (82%)
- Watch (25-50): 11 docs (13%)
- Warning (50-100): 4 docs (5%)
- Critical (>100): 0 docs (0%)

### Top Stale Documents
1. `docs/api/legacy-endpoint.md` - Score: 85 - Age: 87 days
2. `docs/guides/old-tutorial.md` - Score: 62 - Age: 95 days
3. `docs/architecture/deprecated.md` - Score: 55 - Age: 145 days

### Recent Improvements
- Updated 8 API docs this week (avg score: 85 → 15)
- Fixed 12 broken links
- Refreshed 3 architecture diagrams

### Upcoming Reviews
- Next weekly scan: 2025-01-20
- Scheduled reviews: 4 docs
- Escalated items: 0
```

---

## Best Practices

1. **Set Appropriate Thresholds**: Adjust based on document type and change frequency
2. **Monitor Trends**: Track staleness over time, not just point-in-time snapshots
3. **Early Warnings**: Alert at 75% of threshold, not when already stale
4. **Automate Checks**: Run link validation and reference checks automatically
5. **Owner Accountability**: Assign clear ownership, notify owners early
6. **Track Context**: Consider code changes, not just document age
7. **Review Thresholds**: Quarterly review if thresholds are appropriate

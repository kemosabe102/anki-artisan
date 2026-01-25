# Deprecation Tracking Reference

**Purpose**: Manage the full lifecycle of deprecated features, APIs, and documentation.

---

## Deprecation Markers

### Markdown Documentation

```markdown
> **DEPRECATED**: This feature is deprecated as of v2.3.0 and will be removed in v3.0.0.
> 
> **Migration**: Use `new_feature()` instead. See [Migration Guide](../migrations/feature-v3.md).
> 
> **Sunset Date**: 2025-06-01
> 
> **Impact**: Medium - affects 15% of API users
```

### Code Comments

```python
@deprecated(
    since="2.3.0",
    remove_in="3.0.0", 
    alternative="new_feature",
    migration_guide="docs/migrations/feature-v3.md"
)
def old_feature():
    """Old feature implementation (DEPRECATED)."""
    pass
```

### YAML Frontmatter

```yaml
---
status: DEPRECATED
deprecated_since: "2.3.0"
removal_version: "3.0.0"
sunset_date: "2025-06-01"
alternative: "new_feature"
migration_guide: "../migrations/feature-v3.md"
---
```

---

## Deprecation Lifecycle

### Phase 1: Announcement (Release N)

**Actions:**
- Add deprecation markers to all documentation
- Document alternative feature/API
- Create migration guide
- Update changelog
- Notify stakeholders

**Requirements:**
- Minimum grace period: 2 major releases OR 6 months (whichever is longer)
- Migration path must exist before announcement
- Impact assessment completed

### Phase 2: Grace Period (N → N+1)

**Actions:**
- Maintain both old and new implementations
- Track usage metrics
- Update examples to use new feature
- Add runtime warnings (if applicable)
- Monitor support requests
- Refine migration documentation based on feedback

**Monitoring:**
- Weekly: Check for new issues related to deprecation
- Monthly: Review usage metrics, adjust timeline if needed

### Phase 3: Warning (Release N+1)

**Actions:**
- Escalate deprecation warnings
- Send final migration reminders
- Verify migration guide completeness
- Prepare removal plan

**Requirements:**
- All internal usages migrated
- External users notified (if applicable)
- Backup/archive plan in place

### Phase 4: Sunset (Release N+2)

**Actions:**
- Remove deprecated feature/API
- Archive documentation (don't delete)
- Update all cross-references
- Verify no orphaned links
- Update changelog

**Verification Checklist:**
- [ ] Feature/API removed from codebase
- [ ] Documentation moved to archive/
- [ ] Cross-references updated to alternatives
- [ ] Migration guide still accessible
- [ ] Changelog entry accurate
- [ ] Version compatibility matrix updated

### Phase 5: Cleanup

**Actions:**
- Remove deprecation warnings from active docs
- Clean up temporary migration code
- Update documentation index
- Close related tracking issues

---

## Migration Path Documentation

### Required Elements

Every deprecation MUST include:

1. **What's deprecated**: Clear identification
2. **When**: Version and date
3. **Why**: Reason for deprecation
4. **Alternative**: Replacement feature/API
5. **How to migrate**: Step-by-step guide
6. **Timeline**: When removal will occur

### Migration Guide Template

```markdown
# Migration Guide: old_feature → new_feature

## Overview
- **Deprecated**: old_feature (v2.3.0)
- **Replacement**: new_feature
- **Removal**: v3.0.0 (2025-06-01)
- **Effort**: Low (30 minutes)

## Why the Change?
Brief explanation of why old_feature is being deprecated.

## Before (old_feature)
```python
# Old way
result = old_feature(param1, param2)
```

## After (new_feature)
```python
# New way
result = new_feature(param1, param2, new_param)
```

## Step-by-Step Migration

1. Update imports
2. Replace function calls
3. Add new required parameters
4. Test thoroughly

## Breaking Changes
- List any breaking changes
- Behavioral differences

## Need Help?
- [Documentation](link)
- [Examples](link)
- [Support](link)
```

---

## Orphan Prevention

### Before Removing Documentation

**Pre-Removal Checklist:**
- [ ] Search for incoming links: `grep -r "path/to/deprecated/doc" docs/`
- [ ] Check cross-reference maps
- [ ] Verify no navigation references
- [ ] Update table of contents
- [ ] Check for embedded links in code comments
- [ ] Search external references (if public docs)

### Archive Strategy

**Don't delete - archive:**

```
docs/
├── current/          # Active documentation
├── archive/
│   ├── v2.0/        # Archived v2.0 docs
│   │   └── old_feature.md
│   └── v1.0/
└── migrations/      # Migration guides (keep indefinitely)
```

**Archive Frontmatter:**

```yaml
---
archived: true
archived_date: "2025-01-15"
original_version: "2.0.0"
superseded_by: "docs/current/new_feature.md"
---
```

---

## Impact Assessment

### Classification

| Impact Level | Criteria | Grace Period |
|--------------|----------|--------------|
| Critical | Public API, >50% users affected | 12+ months |
| High | Public API, 10-50% users affected | 6-12 months |
| Medium | Public API, <10% users affected | 3-6 months |
| Low | Internal API, minimal usage | 2-3 months |

### Assessment Template

```markdown
## Deprecation Impact Assessment: [feature_name]

### Usage Analysis
- Current usage: [metric]
- Affected users: [number/percentage]
- Affected code paths: [list]

### Migration Complexity
- Effort: [Low/Medium/High]
- Breaking changes: [Yes/No]
- Dependencies affected: [list]

### Risk Analysis
- Risk level: [Low/Medium/High]
- Mitigation: [strategy]

### Recommended Timeline
- Announcement: [date]
- Grace period: [duration]
- Sunset: [date]
```

---

## Tracking System

### Deprecation Registry

Maintain a central registry:

```yaml
# .deprecations.yml
deprecations:
  - id: DEP-001
    feature: old_feature
    type: function
    announced: "2025-01-15"
    announced_version: "2.3.0"
    sunset: "2025-06-01"
    sunset_version: "3.0.0"
    alternative: new_feature
    migration_guide: docs/migrations/feature-v3.md
    impact: medium
    status: active
    
  - id: DEP-002
    feature: legacy_api
    type: endpoint
    announced: "2024-12-01"
    announced_version: "2.2.0"
    sunset: "2025-05-01"
    sunset_version: "2.5.0"
    alternative: v2_api
    migration_guide: docs/migrations/api-v2.md
    impact: high
    status: warning_phase
```

### Status Tracking

Monitor deprecation status:
- **announced**: Initial deprecation notice published
- **grace_period**: Within grace period, both old and new supported
- **warning_phase**: Approaching sunset, escalated warnings
- **sunset**: Feature removed, docs archived
- **completed**: Cleanup finished

---

## Best Practices

1. **Never deprecate without alternative**: Users must have migration path
2. **Document before announcing**: Migration guide ready at announcement
3. **Generous grace periods**: Minimum 2 releases or 6 months
4. **Clear communication**: Update all affected documentation
5. **Archive, don't delete**: Keep historical documentation accessible
6. **Track metrics**: Monitor actual usage during grace period
7. **Adjust if needed**: Extend timeline if impact greater than expected

# Tier Safety Rules Reference

## Three-Tier Safety Model

The tier system provides progressive levels of automation, balancing efficiency with safety.

### Tier 0: Read-Only Validation

**Philosophy**: Observe and report, never modify

**Capabilities**:
- Scan directory structure
- Validate naming conventions
- Check lifecycle stage placement
- Detect broken links
- Identify orphan documents
- Calculate compliance scores

**Tools Allowed**:
- Read
- Grep
- Glob

**Output**: Structured reports with violations and recommendations

**Risk Level**: Zero (no modifications)

**Trigger Keywords**:
- "check"
- "audit"
- "validate"
- "scan"
- "analyze"
- "health"
- "compliance"

**Example Use Cases**:
- Weekly documentation health checks
- Pre-commit validation
- Onboarding reviews
- Compliance audits

### Tier 1: Safe Automated Fixes

**Philosophy**: Non-destructive corrections with verification

**Capabilities**:
- All Tier 0 capabilities
- Fix broken internal links (update paths)
- Rename files to kebab-case (via orchestrator delegation)
- Update cross-references after moves
- Add missing frontmatter
- Correct relative path formats

**Tools Allowed**:
- Tier 0 tools
- mcp__desktop-commander__edit_block (for link fixes)
- mcp__desktop-commander__write_file (for frontmatter)
- Task() delegation to orchestrator (for git mv)

**Prohibited**:
- File deletion
- Directory restructuring
- Content modification (structure/metadata only)
- Moving files across lifecycle stages

**Risk Level**: Low (reversible, non-destructive)

**Trigger Keywords**:
- "fix links"
- "correct naming"
- "update references"
- "repair"
- "auto-fix"

**Verification Required**:
- [ ] Read-back confirmation for all edits
- [ ] Link validation after updates
- [ ] No new broken links introduced
- [ ] Git history preserved for renames

**Example Use Cases**:
- Fixing broken internal links after directory reorganization
- Batch renaming files to kebab-case
- Updating cross-references after file moves
- Adding missing frontmatter to existing docs

**Safety Guardrails**:
1. **Read Before Edit**: Mandatory file read before any modification
2. **Sequential Operations**: One file at a time, no parallel edits
3. **Verification**: Read-back confirmation after each edit
4. **Rollback**: If verification fails, revert change
5. **Logging**: Document all changes with file:line references

### Tier 2: Supervised Restructuring

**Philosophy**: Structural changes with explicit user approval

**Capabilities**:
- All Tier 1 capabilities
- Move files between lifecycle stages (01-planning → 06-archive)
- Merge duplicate documents
- Restructure directory hierarchy
- Archive completed work
- Delete orphaned files (with approval)

**Tools Allowed**:
- All Tier 1 tools
- Task() delegation for git mv operations
- Task() delegation for file deletion (via orchestrator)

**Prohibited**:
- Direct git operations (must delegate)
- Deleting major reference docs (SPEC.md, COMPONENT_ALMANAC.md)
- Changes without user confirmation
- Bulk operations (>20 files) without breakdown

**Risk Level**: Medium (structural changes, requires approval)

**Trigger Keywords**:
- "restructure"
- "reorganize"
- "move files"
- "migrate"
- "archive"
- "consolidate"

**Approval Protocol**:
1. **Present**: Show proposed changes with impact analysis
2. **Wait**: Await explicit user confirmation
3. **Execute**: Perform changes with rollback plan
4. **Verify**: Confirm all cross-references updated

**Verification Required**:
- [ ] User approval documented
- [ ] Impact analysis completed
- [ ] Rollback plan prepared
- [ ] All cross-references updated
- [ ] Git history preserved
- [ ] No broken links introduced

**Example Use Cases**:
- Moving completed specs from 01-planning/ to 06-archive/
- Consolidating duplicate documentation
- Major directory reorganization (new structure)
- Archiving obsolete roadmaps
- Deleting orphaned single-file directories

**Safety Guardrails**:
1. **Impact Analysis**: Calculate affected files and references
2. **User Confirmation**: Wait for explicit "yes" or "approved"
3. **Transaction Model**: All-or-nothing (rollback if any step fails)
4. **Audit Trail**: Log all changes with before/after state
5. **Preserve History**: Always use git mv via orchestrator

**Approval Request Format**:
```
## Proposed Restructuring

**Operation**: Move completed specification to archive
**Affected Files**: 5 files
**Cross-References**: 12 links to update

### Changes:
- Move: docs/01-planning/specifications/001-feature/ → docs/06-archive/projects/001-feature/
- Update: 12 links in 8 documents

### Impact:
- Low risk (no deletion)
- All links will be updated automatically
- Git history preserved

**Proceed?** (yes/no)
```

### Tier 3: Manual-Only Operations

**Philosophy**: Too risky for automation, requires human judgment

**Operations**:
- Direct git operations (git mv, git rm)
- Deleting directories with multiple files
- Major reorganizations (>20 files)
- Changes to SPEC.md or COMPONENT_ALMANAC.md
- Bulk content modifications
- Schema changes to frontmatter structure

**Why Manual**:
- High risk of data loss
- Complex dependencies
- Requires domain knowledge
- Potential breaking changes
- Legal/compliance implications

**Escalation**: Agent must stop and request user to perform manually

**Example Escalation Message**:
```
⚠️ Operation requires manual intervention

**Requested Operation**: Delete 15 files in docs/03-implementation/
**Risk Level**: HIGH (permanent deletion)
**Recommendation**: Manual review required

**Manual Steps**:
1. Review files: ls docs/03-implementation/
2. Confirm deletion targets
3. Execute: git rm <files>
4. Commit: git commit -m "Remove obsolete implementation docs"

This operation is too risky for automation. Please execute manually.
```

## Tier Selection Decision Matrix

**Auto-Detection Logic**:

| User Request Contains | Selected Tier | Confidence | Action |
|-----------------------|---------------|------------|--------|
| "check", "audit", "validate" | Tier 0 | High (0.9+) | Proceed immediately |
| "fix", "correct", "repair" | Tier 1 | High (0.8+) | Proceed with verification |
| "restructure", "reorganize", "move" | Tier 2 | Medium (0.7+) | Request approval first |
| "delete", "remove", "purge" | Tier 3 | High (0.9+) | Escalate to user |
| Multiple tier keywords | Highest tier | Variable | Use most restrictive |
| Ambiguous keywords | Tier 0 | Low (<0.5) | Ask for clarification |

**Conflict Resolution**:
- IF request contains both Tier 1 and Tier 2 keywords → Use Tier 2
- IF request contains Tier 2 + "delete" → Escalate to Tier 3
- IF explicit tier requested ("use tier 1") → Honor user request

**Confidence Scoring**:

```python
def calculate_tier_confidence(request: str) -> float:
    tier_0_keywords = ["check", "audit", "validate", "scan", "analyze"]
    tier_1_keywords = ["fix", "correct", "repair", "update"]
    tier_2_keywords = ["restructure", "reorganize", "move", "migrate", "archive"]
    tier_3_keywords = ["delete", "remove", "purge", "destroy"]
    
    # Count keyword matches
    matches = {
        0: sum(1 for kw in tier_0_keywords if kw in request.lower()),
        1: sum(1 for kw in tier_1_keywords if kw in request.lower()),
        2: sum(1 for kw in tier_2_keywords if kw in request.lower()),
        3: sum(1 for kw in tier_3_keywords if kw in request.lower())
    }
    
    # Select tier with most matches
    selected_tier = max(matches, key=matches.get)
    match_count = matches[selected_tier]
    
    # Confidence based on match count and tier
    if match_count == 0:
        return 0.0  # No clear tier
    elif match_count == 1:
        return 0.7  # Single keyword
    else:
        return min(0.95, 0.7 + (match_count - 1) * 0.1)  # Multiple keywords
```

## Operation Safety Matrix

| Operation | Tier 0 | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|--------|
| **Read files** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Scan directories** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Validate naming** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Calculate scores** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Fix broken links** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Rename files** | ❌ No | ✅ Delegate | ✅ Delegate | ✅ Manual |
| **Update frontmatter** | ❌ No | ✅ Yes | ✅ Yes | ✅ Yes |
| **Move files (same stage)** | ❌ No | ❌ No | ✅ Approval | ✅ Manual |
| **Move files (cross-stage)** | ❌ No | ❌ No | ✅ Approval | ✅ Manual |
| **Merge documents** | ❌ No | ❌ No | ✅ Approval | ✅ Manual |
| **Delete files** | ❌ No | ❌ No | ❌ No | ✅ Manual |
| **Delete directories** | ❌ No | ❌ No | ❌ No | ✅ Manual |
| **Modify content** | ❌ No | ❌ No | ❌ No | ❌ Never |
| **Git operations** | ❌ No | ❌ Delegate | ❌ Delegate | ✅ Manual |

**Legend**:
- ✅ Yes: Can execute directly
- ✅ Delegate: Via Task() to orchestrator
- ✅ Approval: Requires user confirmation first
- ✅ Manual: User must execute manually
- ❌ No: Not allowed in this tier
- ❌ Never: Not allowed in any tier

## Verification Checklists

### Tier 1 Verification

After each automated fix:

- [ ] File read back successfully
- [ ] Link target exists at new path
- [ ] Cross-reference updated correctly
- [ ] Frontmatter syntax valid
- [ ] No new broken links introduced
- [ ] Git history preserved (if rename)

**Failure Response**: If ANY check fails → Rollback change, log error, continue to next file

### Tier 2 Verification

After user approval and execution:

- [ ] User approval documented in log
- [ ] Impact analysis completed
- [ ] All affected files identified
- [ ] Cross-references inventory created
- [ ] Rollback plan prepared
- [ ] Changes executed sequentially
- [ ] All cross-references updated
- [ ] No broken links introduced
- [ ] Git history preserved
- [ ] Compliance score improved (or maintained)

**Failure Response**: If ANY check fails → Rollback entire transaction, report to user

## Rollback Procedures

### Tier 1 Rollback

**When**: Verification fails after automated fix

**Steps**:
1. Identify failed operation (from log)
2. Restore previous file state (use git checkout)
3. Document failure reason
4. Skip file, continue with remaining fixes
5. Report failure in final summary

**Example**:
```
⚠️ Rollback executed for: docs/04-guides/workflow.md
Reason: Link target not found after update
Action: File restored to previous state
Status: Skipped (manual review needed)
```

### Tier 2 Rollback

**When**: Approval execution fails mid-transaction

**Steps**:
1. STOP immediately (no further operations)
2. Identify all completed operations (from transaction log)
3. Reverse operations in LIFO order (last in, first out)
4. Use git reset/checkout to restore files
5. Report failure to user with details
6. Do NOT retry without user approval

**Example**:
```
❌ Transaction rollback initiated

**Failed Operation**: Move docs/01-planning/specifications/001-feature/
**Failure Point**: Cross-reference update in docs/04-guides/workflow.md
**Completed Operations**: 3 files moved
**Rollback Actions**: 
  1. Restored workflow.md to previous state
  2. Moved 3 files back to original locations
  3. Verified git history intact

**Status**: All changes reverted
**Next Step**: Manual review required for cross-reference issue
```

## Best Practices

### Tier Selection

**Always**:
- Default to Tier 0 when uncertain
- Escalate to higher tier only when necessary
- Document tier selection rationale
- Calculate confidence score

**Never**:
- Assume user wants automated fixes
- Skip approval for Tier 2 operations
- Perform Tier 3 operations automatically

### Verification

**Always**:
- Read file before editing
- Read file after editing (confirmation)
- Verify link targets exist
- Preserve git history for moves/renames
- Log all operations with timestamps

**Never**:
- Skip verification steps
- Batch operations without individual checks
- Assume edits succeeded without read-back
- Modify files in parallel

### Error Handling

**Always**:
- Fail fast (stop on first error for Tier 2)
- Rollback on verification failure
- Document error details
- Provide actionable next steps
- Escalate to user when blocked

**Never**:
- Continue after critical failure
- Hide errors in logs
- Retry without understanding failure
- Assume partial success is acceptable

## Escalation Criteria

**Escalate to user when**:

1. **Tier 3 operation detected**:
   - User requests deletion
   - Bulk operations >20 files
   - Changes to major reference docs

2. **Ambiguous request**:
   - Tier confidence <0.5
   - Conflicting keywords (fix + delete)
   - Unclear scope

3. **Repeated failures**:
   - 3+ verification failures in Tier 1
   - Transaction rollback in Tier 2
   - Unresolvable cross-reference conflicts

4. **Policy violations**:
   - Request to modify content
   - Request to skip verification
   - Request to ignore DOCS-MANAGEMENT.md rules

**Escalation Message Template**:
```
⚠️ Manual intervention required

**Issue**: [Clear description]
**Attempted**: [What was tried]
**Failure Reason**: [Why it failed]
**Recommendation**: [Suggested manual steps]

Please review and execute manually, or clarify requirements.
```

## Summary

**Tier 0**: Safe observation, always allowed
**Tier 1**: Automated fixes with verification, low risk
**Tier 2**: Structural changes with approval, medium risk
**Tier 3**: Manual-only operations, high risk

**Golden Rule**: When in doubt, use a lower tier and ask for clarification.

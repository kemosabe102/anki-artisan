# Documentation Review Workflow

Complete reference for PR-based documentation review processes.

---

## PR Template

```markdown
## Documentation Change Request

### Change Type
- [ ] New documentation
- [ ] Update existing documentation
- [ ] Deprecation notice
- [ ] Document removal
- [ ] Reorganization

### Affected Documents
<!-- List all modified files -->
- `docs/path/to/file1.md`
- `docs/path/to/file2.md`

### Summary
<!-- Brief description of changes -->

### Breaking Changes
- [ ] Yes - **Justification required below**
- [ ] No

**Breaking Change Details** (if applicable):
<!-- Describe impact and migration path -->

### Quality Metrics
<!-- Auto-populated by CI -->
- **Before**: Score X.XX
- **After**: Score X.XX
- **Change**: +/- X.XX

### Target Audience
- [ ] End users
- [ ] Developers
- [ ] Operators/SRE
- [ ] Internal team
- [ ] External contributors

### Testing
<!-- For tutorials/guides with code examples -->
- [ ] Code examples tested and work
- [ ] Commands verified in target environment
- [ ] Screenshots/outputs are current

### Checklist
- [ ] Spell check passed
- [ ] Links validated (internal + external)
- [ ] Examples are executable
- [ ] Appropriate detail level for audience
- [ ] Follows style guide (documentation-standards)
- [ ] Cross-references updated
- [ ] Version compatibility noted

### Related Issues
Fixes #XXX
Related to #YYY
```

---

## Review Checklist

### Technical Accuracy
- [ ] **Facts verified**: Claims match implementation
- [ ] **API signatures correct**: Parameters, return types match code
- [ ] **Version compatibility**: Noted which versions apply
- [ ] **Deprecations accurate**: Timeline and alternatives correct
- [ ] **Code examples work**: Tested in target environment

### Completeness
- [ ] **All sections present**: Required content per doc type
- [ ] **No gaps**: Flow is logical, no missing steps
- [ ] **Prerequisites stated**: What reader needs to know
- [ ] **Success criteria clear**: How to verify it worked
- [ ] **Error handling**: Common issues and solutions

### Clarity
- [ ] **Audience appropriate**: Right detail level
- [ ] **Plain language**: Avoid unnecessary jargon
- [ ] **Examples included**: Concrete illustrations
- [ ] **Structure logical**: Headings, lists, formatting
- [ ] **Scannable**: Can find info quickly

### Links and References
- [ ] **Internal links work**: Tested all relative paths
- [ ] **External links valid**: No 404s or dead sites
- [ ] **Cross-references accurate**: Links to related docs
- [ ] **Anchors functional**: Fragment links tested
- [ ] **Assets accessible**: Images, diagrams load

### Style and Formatting
- [ ] **Style guide followed**: documentation-standards compliance
- [ ] **Formatting consistent**: Headings, code blocks, lists
- [ ] **Spelling correct**: Technical dictionary used
- [ ] **Grammar acceptable**: Professional quality
- [ ] **Code formatting**: Proper syntax highlighting

### Process Compliance
- [ ] **Quality score >= threshold**: Per document type
- [ ] **Approvers assigned**: CODEOWNERS matched
- [ ] **Breaking changes flagged**: If applicable
- [ ] **Migration guide provided**: For breaking changes
- [ ] **Ownership clear**: Maintainers identified

---

## Reviewer Assignment

### Auto-Assignment Logic

**GitHub Action Example**:
```yaml
name: Assign Reviewers
on:
  pull_request:
    types: [opened]
    paths:
      - 'docs/**'
      - '.claude/**'

jobs:
  assign:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Assign from CODEOWNERS
        uses: kentaro-m/auto-assign-action@v1.2.0
        with:
          configuration-path: .github/auto-assign.yml
          
      - name: Add labels based on path
        run: |
          if [[ "${{ github.event.pull_request.changed_files }}" =~ "docs/api/" ]]; then
            gh pr edit ${{ github.event.pull_request.number }} --add-label "api-docs"
          fi
```

### Manual Override

**When to manually assign**:
- CODEOWNERS doesn't cover new path
- Need cross-domain expertise
- Original owner unavailable
- Requires architectural review

**How to override**:
1. Comment on PR: `@username could you review this?`
2. Use GitHub UI: "Reviewers" → Add manually
3. Update CODEOWNERS if pattern will recur

### Review Load Balancing

**Target**: 5-10 PRs per reviewer per month

**Balancing Strategy**:
- Rotate reviewers within team
- Distribute by domain expertise
- Monitor reviewer queue depth
- Escalate if >3 PRs pending for 48+ hours

**Reviewer Capacity**:
- **Full-time docs**: 15-20 PRs/month
- **Part-time docs**: 5-10 PRs/month
- **Occasional**: 1-3 PRs/month
- **On-call**: Avoid assignments during on-call week

---

## Review Execution

### First-Time Review (Within 24 Hours)

**Quick Scan**:
1. Read summary and change type
2. Check quality score delta
3. Identify breaking changes
4. Estimate review effort (5min vs 30min)

**Initial Feedback**:
- Approve if trivial + high quality
- Request changes if major issues
- Comment if clarification needed
- Delegate if wrong reviewer

### Deep Review (Within 48 Hours)

**Systematic Check**:
1. Open checklist in second window
2. Review each changed file
3. Test code examples locally
4. Click all links
5. Check cross-references
6. Verify version compatibility
7. Complete checklist
8. Approve or request changes

**Feedback Quality**:
- **Specific**: "Line 42: Example uses deprecated API"
- **Actionable**: "Add migration guide for users of old API"
- **Constructive**: "Consider adding diagram to clarify flow"
- **Prioritized**: Label as blocking vs nice-to-have

### Re-Review After Changes

**Quick Turnaround**:
- Check only changed files
- Verify requested changes addressed
- Approve if satisfied
- Request further changes if needed

**Target**: <24 hours for re-review

---

## Common Review Scenarios

### Scenario: Trivial Fix (Typo, Formatting)

**Review Time**: 2-5 minutes

**Process**:
- Verify change is indeed trivial
- Check no unintended edits
- Approve immediately if clean
- No need for full checklist

### Scenario: New API Documentation

**Review Time**: 20-30 minutes

**Process**:
1. Compare API docs to actual code
2. Test all code examples
3. Verify parameter types and defaults
4. Check error handling documented
5. Ensure examples cover common use cases
6. Validate cross-references to related APIs
7. Full checklist required

### Scenario: Breaking Change

**Review Time**: 30-45 minutes

**Process**:
1. Verify breaking change is necessary
2. Check migration guide completeness
3. Ensure deprecation timeline reasonable
4. Validate all affected docs updated
5. Test migration path yourself
6. Escalate to second lead reviewer
7. Require 2+ approvals

### Scenario: Reorganization

**Review Time**: 45-60 minutes

**Process**:
1. Verify all redirects in place
2. Check navigation/index updated
3. Test all cross-references
4. Ensure search still works
5. Validate external links unaffected
6. Check version compatibility maintained
7. Require architectural review

---

## Review SLA and Escalation

### SLA Targets

| Review Type | First Response | Complete Review | Approval |
|------------|----------------|-----------------|----------|
| Trivial | 4 hours | 24 hours | 24 hours |
| Standard | 24 hours | 48 hours | 72 hours |
| Breaking | 24 hours | 48 hours | 96 hours |
| Emergency | 30 minutes | 2 hours | 4 hours |

### SLA Breach Handling

**24 Hours Overdue**:
- Automated reminder to reviewer
- Notify in team Slack channel

**48 Hours Overdue**:
- Escalate to team lead
- Re-assign if reviewer unavailable

**72 Hours Overdue**:
- Escalate to documentation committee
- Fast-track with alternate reviewer

---

## Review Metrics

Track per reviewer:
- Average time to first response
- Average time to approval
- Approval vs request-changes ratio
- Checklist completion rate
- Number of reviews per month
- Quality of feedback (peer assessment)

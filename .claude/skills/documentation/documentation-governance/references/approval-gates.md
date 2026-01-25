# Approval Gates Reference

Detailed configuration and bypass procedures for documentation approval gates.

---

## Gate Types

### 1. Quality Score Gate

**Purpose**: Prevent low-quality documentation from merging

**Implementation**: CI check using documentation-health skill

**Thresholds**:
```yaml
gates:
  quality_score:
    critical_docs:      # SPEC.md, CLAUDE.md, architecture
      minimum: 0.85
      blocking: true
    api_docs:           # API reference documentation
      minimum: 0.75
      blocking: true
    user_guides:        # Tutorials, how-tos
      minimum: 0.70
      blocking: true
    internal_docs:      # Team processes, runbooks
      minimum: 0.60
      blocking: false   # Warning only
```

**Score Calculation** (from documentation-health):
- Completeness: 40% (all required sections present)
- Clarity: 30% (readability, examples, structure)
- Accuracy: 20% (links work, code compiles)
- Freshness: 10% (last updated within 6 months)

**Gate Behavior**:
- `>= minimum`: Pass, gate green
- `minimum - 0.15 to minimum`: Warning, requires justification
- `< minimum - 0.15`: Block, must improve before merge

---

### 2. Reviewer Approval Gate

**Purpose**: Ensure subject matter experts approve changes

**Implementation**: GitHub branch protection + CODEOWNERS

**Requirements by Document Type**:
```yaml
approvals:
  critical_docs:
    required_approvals: 2
    required_from: [tech-leads, architects]
    dismiss_stale: true
    
  api_docs:
    required_approvals: 1
    required_from: [domain-owners]
    dismiss_stale: true
    
  user_guides:
    required_approvals: 1
    required_from: [docs-team, domain-owners]
    technical_reviewer: required
    ux_reviewer: recommended
    
  tutorials:
    required_approvals: 1
    required_from: [docs-team]
    dismiss_stale: false
    
  internal_docs:
    required_approvals: 1
    required_from: [team-members]
    dismiss_stale: false
```

**Stale Review Dismissal**:
- New commits dismiss previous approvals
- Forces re-review after significant changes
- Threshold: >50 lines changed = stale

---

### 3. Breaking Change Gate

**Purpose**: Protect users from unexpected documentation changes

**Trigger Detection**:
```python
# CI script to detect breaking changes
breaking_patterns = [
    r'~~.*~~',  # Strikethrough (deprecation)
    r'\bDEPRECATED\b',
    r'\bREMOVED\b',
    r'docs/api/.*\.md',  # API doc changes
    r'breaking:\s*true',  # PR label
]

def is_breaking_change(diff, pr_labels):
    for pattern in breaking_patterns:
        if re.search(pattern, diff):
            return True
    return 'breaking' in pr_labels
```

**Required Actions**:
1. **Deprecation Notice**: Add to current docs (1 release minimum)
2. **Migration Guide**: Step-by-step upgrade path
3. **Timeline**: Clear removal/change date
4. **Alternatives**: Replacement functionality
5. **Impact Analysis**: Who/what is affected
6. **Lead Approval**: 2+ tech leads must approve

**Example Deprecation Notice**:
```markdown
> **DEPRECATED**: This API will be removed in v2.0 (January 2025).
> Use `new_function()` instead. See [Migration Guide](./migration.md).
```

---

### 4. Link Validation Gate

**Purpose**: Prevent broken links in documentation

**Implementation**: CI check with link validator

**Checked Links**:
- Internal relative links (`../other-doc.md`)
- Internal absolute links (`/docs/guide.md`)
- Anchor links (`#section-heading`)
- External links (`https://example.com`)
- Image sources (`./images/diagram.png`)

**Validation Rules**:
- Internal links: MUST exist in repository
- Anchors: MUST match heading slugs
- External links: MUST return 200 status (with retry)
- Images: MUST be committed to repo

**Allowlist for External Links**:
- Known slow sites (longer timeout)
- Authentication-required URLs (skip check)
- Dynamic content (verify manually)

**Gate Behavior**:
- 0 broken links: Pass
- 1-2 broken external links: Warning (may be temporary)
- Any broken internal links: Block
- >3 broken links total: Block

---

### 5. Protected Path Gate

**Purpose**: Prevent unauthorized edits to critical documentation

**Implementation**: GitHub branch protection + custom CI check

**Protected Paths**:
```yaml
protected_paths:
  tier_1:  # Admin approval required
    - /CLAUDE.md
    - /docs/00-project/SPEC.md
    - /.claude/docs/00-core/**
    
  tier_2:  # Owner approval required (2+)
    - /docs/00-project/COMPONENT_ALMANAC.md
    - /docs/architecture/**
    - /.claude/agents/**
    
  tier_3:  # Maintainer approval required
    - /docs/api/**
    - /.claude/skills/**
```

**Approval Requirements**:
- Tier 1: 1 admin approval + standard gates
- Tier 2: 2 owner approvals + quality >= 0.85
- Tier 3: 1 maintainer approval + quality >= 0.75

---

## Gate Bypass Procedures

### Emergency Bypass

**Valid Reasons**:
- Security vulnerability in code example
- Critical factual error causing production issues
- Compliance violation (legal, privacy)
- Service outage documentation (incident response)

**Process**:
1. Create PR with `emergency` label
2. Document reason in PR description
3. Get 1 admin approval (any gate)
4. Merge immediately
5. Create follow-up ticket for proper fix
6. Post-mortem within 24 hours

**Audit Trail**:
```yaml
bypass_log:
  timestamp: 2025-12-13T10:30:00Z
  pr_number: 1234
  bypassed_gates: [quality_score, breaking_change]
  reason: "Security vulnerability in code example"
  approver: @admin-username
  follow_up_ticket: DOCS-567
```

---

### Temporary Quality Bypass

**Valid Reasons**:
- Work-in-progress documentation (must be in `/drafts/`)
- Incremental improvement of low-quality legacy docs
- External contribution from community (will iterate)

**Process**:
1. Add `quality-bypass` label to PR
2. Document justification (must show improvement)
3. Create ticket to reach quality threshold
4. Get 2 owner approvals
5. Merge with notice that doc is below standard
6. Complete follow-up within 2 weeks

**Conditions**:
- Quality score must improve (or be new content)
- Bypass limited to 1 per month per maintainer
- Follow-up ticket required
- Cannot bypass tier-1 protected docs

---

### Breaking Change Exception

**Valid Reasons**:
- Urgent deprecation due to security/compliance
- Coordinated with major code release
- User-requested clarification (not actual breaking change)

**Process**:
1. Add `breaking-exception` label
2. Provide detailed impact analysis
3. Show mitigation plan (communication, support)
4. Get 2 tech lead approvals
5. Merge with extended deprecation notice
6. Monitor user feedback channels

**Required Documentation**:
- Who is affected (user segments)
- What breaks (specific scenarios)
- When it takes effect (timeline)
- How to migrate (step-by-step)
- Where to get help (support channels)

---

## Gate Configuration

### GitHub Branch Protection Settings

```yaml
# .github/branch-protection.yml
branches:
  - name: main
    protection:
      required_status_checks:
        strict: true
        contexts:
          - "ci/quality-gate"
          - "ci/link-validation"
          - "ci/protected-paths"
          - "ci/breaking-change-detection"
      required_pull_request_reviews:
        required_approving_review_count: 1
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
      enforce_admins: false  # Allow emergency bypass
      required_signatures: true  # Signed commits
      restrictions: null  # No push restrictions (use reviews)
```

### CI Gate Implementation

**Quality Gate Check**:
```yaml
# .github/workflows/doc-quality-gate.yml
name: Documentation Quality Gate
on:
  pull_request:
    paths:
      - 'docs/**'
      - '.claude/**'

jobs:
  quality_check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run documentation-health validation
        run: |
          # Invoke documentation-health skill
          score=$(python scripts/check_doc_health.py --changed-files)
          echo "Quality score: $score"
          
          # Determine threshold based on path
          if [[ "$path" =~ ^docs/00-project/ ]]; then
            threshold=0.85
          elif [[ "$path" =~ ^docs/api/ ]]; then
            threshold=0.75
          else
            threshold=0.70
          fi
          
          # Gate logic
          if (( $(echo "$score < $threshold" | bc -l) )); then
            echo "::error::Quality score $score below threshold $threshold"
            exit 1
          fi
```

---

## Gate Metrics

Track per gate type:
- **Pass rate**: % PRs passing on first try
- **Bypass rate**: % PRs using bypass procedures
- **Average score**: For quality gate
- **Time to pass**: How long to fix gate failures
- **False positive rate**: Gates blocking valid changes

**Ideal Metrics**:
- Pass rate: >80%
- Bypass rate: <5%
- Average quality score: >0.80
- Time to pass: <24 hours
- False positives: <2%

**Red Flags**:
- Bypass rate >10%: Gates too strict or process broken
- Pass rate <60%: Need better contributor guidance
- False positives >5%: Gate logic needs refinement

---

## Gate Evolution

Review gates quarterly:
1. Analyze metrics (pass rates, bypasses)
2. Collect feedback from contributors/reviewers
3. Identify pain points and false positives
4. Propose adjustments (thresholds, rules)
5. Test changes in staging environment
6. Communicate updates to team
7. Deploy with monitoring period

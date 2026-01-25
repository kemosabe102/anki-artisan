---
name: documentation-governance
description: >
  Establishes and enforces documentation governance including review workflows, 
  approval gates, access control, and change tracking. Ensures documentation 
  quality through process controls.
  Use when: "require doc review", "set approval gates", "track doc changes", 
  "documentation permissions", "review workflow", "doc ownership".
  NOT for: content validation (documentation-health), style (documentation-standards).
---

# Documentation Governance Skill

Establishes process controls for documentation management.

---

## Core Principles

1. **Review-First Culture**: All documentation changes go through review
2. **Clear Ownership**: Every document has defined owners and maintainers
3. **Traceable Changes**: Full audit trail for all modifications
4. **Quality Gates**: Automated checks prevent substandard documentation from merging
5. **Graduated Access**: Permissions match expertise and responsibility

---

## Review Workflows

### PR-Based Review

**Standard Process**:
```
1. Author creates PR with documentation changes
2. Auto-assign reviewers based on CODEOWNERS
3. Run automated quality checks (doc-health validation)
4. Reviewers use checklist template
5. Approve or request changes
6. Merge only after all gates pass
```

**PR Template Fields**:
- Change type: [New | Update | Deprecation | Removal]
- Affected documents: [list]
- Breaking changes: [Yes/No + justification]
- Quality score: [auto-populated from doc-health]
- Target audience: [developer | user | operator]

**Automated Checks**:
- Link validation (no broken internal/external links)
- Spell check (technical dictionary aware)
- Format compliance (documentation-standards validation)
- Completeness score >= 0.75
- Consistency with codebase (version numbers, API signatures)

### Reviewer Assignment

**CODEOWNERS Patterns**:
```
# Core architecture docs - require 2 approvals
/docs/00-project/           @team-leads @tech-leads
/docs/architecture/         @architects @tech-leads

# API documentation - respective domain owners
/docs/api/agents/           @agent-team
/docs/api/skills/           @skills-team
/docs/api/database/         @data-team

# User-facing guides - require UX review
/docs/guides/               @docs-team @ux-team

# Planning and specifications
/docs/01-planning/          @product-team @tech-leads

# Agent/skill documentation
/.claude/agents/            @claude-code-ecosystems
/.claude/skills/            @skill-maintainers
```

**Review Team Sizes**:
- Critical docs (SPEC.md, architecture): 2-3 reviewers
- API documentation: 1-2 reviewers (domain experts)
- User guides: 1 technical + 1 UX reviewer
- Internal docs: 1 reviewer

**Review Checklist Template** (see `references/review-workflow.md`):
- [ ] Technical accuracy verified
- [ ] Links tested (internal + external)
- [ ] Examples executable/tested
- [ ] Completeness score >= 0.75
- [ ] Style guide compliance (documentation-standards)
- [ ] Appropriate detail level for audience
- [ ] Breaking changes documented and justified
- [ ] Version compatibility noted

---

## Approval Gates

### Quality Score Gate

**Requirement**: Documentation health score >= 0.75

**Score Components** (validated by documentation-health skill):
- Completeness: 40% (all required sections present)
- Clarity: 30% (readability, examples, structure)
- Accuracy: 20% (links work, code compiles, versions match)
- Freshness: 10% (last updated within 6 months)

**Gate Behavior**:
- Score >= 0.75: Auto-approve quality gate
- Score 0.60-0.74: Warning, requires explicit justification
- Score < 0.60: Block merge, must improve

**Bypass Conditions**:
- Emergency hotfix documentation (requires 2 lead approvals)
- Work-in-progress docs (must be in `/drafts/` path)

### Breaking Change Gate

**Trigger Conditions**:
- Removing or renaming documented APIs
- Changing required parameters in examples
- Deprecating entire document sections
- Major reorganization affecting external links

**Required Actions**:
1. Add deprecation notice (minimum 1 release cycle)
2. Provide migration guide
3. Update all cross-references
4. Notify stakeholders via changelog
5. Require 2+ lead approvals

**Staged Rollout**:
- Phase 1: Add deprecation warnings (maintain old + new docs)
- Phase 2: Mark as deprecated (old docs visible but flagged)
- Phase 3: Remove old documentation (redirect to new)

### Merge Requirements

**By Document Type**:

| Document Type | Required Approvals | Quality Gate | Additional Requirements |
|--------------|-------------------|--------------|------------------------|
| SPEC.md, CLAUDE.md | 2 tech leads | >= 0.85 | Architecture review |
| API docs | 1 domain expert | >= 0.75 | Code cross-reference validation |
| User guides | 1 tech + 1 UX | >= 0.70 | User testing notes |
| Tutorials | 1 reviewer | >= 0.75 | Execution test results |
| Internal docs | 1 team member | >= 0.60 | Peer review |
| Agent/skill docs | 1 architect | >= 0.75 | Integration test pass |

**See**: `references/approval-gates.md` for detailed gate configurations

---

## Access Control

### Permission Model

**Role Hierarchy**:
1. **Read-Only**: All team members (default)
2. **Contributor**: Can propose changes via PR
3. **Maintainer**: Can review and approve PRs
4. **Owner**: Can modify protected docs, configure gates
5. **Admin**: Can override gates, modify governance

**Permission Assignment**:
- Based on CODEOWNERS file
- Inherits from directory structure
- Can be document-specific

### Protected Paths

**Critical Documentation** (Owner+ required):
```
/docs/00-project/SPEC.md
/docs/00-project/COMPONENT_ALMANAC.md
/CLAUDE.md
/.claude/docs/00-core/*.md
```

**Domain-Specific** (Maintainer+ from domain team):
```
/docs/api/agents/*         - Agent team
/docs/api/skills/*         - Skills team
/docs/database/*           - Data team
/.claude/agents/*          - Agent architects
/.claude/skills/*          - Skill maintainers
```

**Open Documentation** (Contributor+ can propose):
```
/docs/guides/*
/docs/tutorials/*
/docs/examples/*
/docs/troubleshooting/*
```

**Permission Inheritance**:
- Subdirectories inherit parent permissions by default
- Exceptions defined in CODEOWNERS
- More restrictive child permissions override parent

**Edit Workflows by Permission**:
- **Read-Only**: Can view, clone, open issues
- **Contributor**: Can fork, create PR, comment
- **Maintainer**: Can review, approve, merge (non-protected)
- **Owner**: Can merge protected docs, modify CODEOWNERS
- **Admin**: Can bypass gates (with audit trail)

**See**: `references/access-control.md` for permission matrices

---

## Change Tracking

### Audit Trail Requirements

**Tracked Metadata** (every change):
```yaml
change_id: uuid
timestamp: ISO-8601
author: github_username
reviewer: github_username
document_path: absolute/path/to/doc.md
change_type: [new|update|deprecation|removal]
quality_score_before: 0.XX
quality_score_after: 0.XX
breaking_change: boolean
approval_chain: [reviewer1, reviewer2, ...]
```

**Storage**:
- Git commit history (primary source of truth)
- Pull request metadata (review discussions)
- CI/CD logs (automated gate results)
- Optional: External audit database for compliance

**Audit Queries**:
- Who last modified document X?
- All changes to section Y in last N days
- Breaking changes in release Z
- Documents with quality score decline
- Approval patterns by reviewer

### Change Attribution

**Commit Message Format**:
```
docs(scope): short description

- Detailed change 1
- Detailed change 2

Quality: 0.XX -> 0.XX
Breaking: [Yes/No]
Fixes: #issue-number
Reviewed-by: @username
```

**Scope Values**:
- `spec` - SPEC.md, architecture docs
- `api` - API documentation
- `guide` - User guides, tutorials
- `agent` - Agent documentation
- `skill` - Skill documentation
- `governance` - Process/policy docs

**Co-Authorship**:
- Significant contributions: Add `Co-authored-by: Name <email>`
- AI assistance: Add `AI-assisted: Claude Code` (transparency)

### History Preservation

**Retention Policy**:
- Git history: Permanent (never force-push to main)
- PR discussions: Permanent
- Draft branches: 90 days after merge/close
- Deprecated docs: Move to `/docs/archive/` (don't delete)

**Versioned Documentation**:
- Tag documentation snapshots with release versions
- Maintain last 3 major versions
- Archive older versions with deprecation notice
- Link to version-specific docs from current

**Protected History**:
- Main branch: No force-push, no history rewriting
- Protected docs: Require admin override to delete
- Archive directory: Immutable (append-only)

### Rollback Procedures

**Triggers**: Critical errors, premature breaking changes, quality <0.50, security issues  
**Process**: Hotfix branch → Fast-track review (30min SLA) → Deploy → Post-mortem (24hrs)  
**Approval**: Standard (1 maintainer) | Protected (2 owners) | Emergency (admin + post-mortem)

---

## Ownership Model

### CODEOWNERS Structure

**Format**: `/docs/path/ @team-name @owner-name`

**Responsibilities**: Review <48hrs, maintain quality ≥threshold, sync with code, quarterly freshness reviews

**Assignment**: Domain expertise, active contributor, proven doc skills, availability, diversity (no single points of failure)

### Responsibility Matrix

**RACI Model** (Responsible, Accountable, Consulted, Informed):

| Activity | Owner | Maintainer | Contributor | Reader |
|----------|-------|------------|-------------|--------|
| Write/update docs | R | R | R | - |
| Review PRs | A | R | C | - |
| Approve merges | A | R | - | - |
| Set quality gates | A | C | - | - |
| Handle issues | R | R | C | I |
| Deprecate docs | A | C | I | I |
| Emergency rollback | A | R | - | I |

**Legend**:
- R (Responsible): Does the work
- A (Accountable): Final decision authority
- C (Consulted): Provides input
- I (Informed): Kept updated

### Escalation Paths

**Level 1** (Document Issues):
- Reader → Contributor (via issue/PR)
- Contributor → Maintainer (via review request)
- SLA: 48 hours

**Level 2** (Quality/Process Issues):
- Maintainer → Owner (via direct communication)
- Owner → Tech Lead (if policy clarification needed)
- SLA: 24 hours

**Level 3** (Governance Disputes):
- Tech Lead → Documentation Committee
- Committee → Engineering Leadership
- SLA: 1 week

**Emergency Escalation**:
- Security issues: Immediate to Security Team
- Breaking production: Immediate to On-Call Lead
- Data breach in docs: Immediate to Security + Legal

### Ownership Transitions

**Triggers**: Role changes, reorganization, scope expansion  
**Process**: Knowledge transfer (1-2hrs) → Shadow period (2wks) → Update CODEOWNERS → Announce  
**Continuity**: 2+ owners for critical docs, cross-training, succession planning

---

## Governance Enforcement

**Automated Checks** (CI/CD):
- Blocking: CODEOWNERS validation, quality score, links, protected paths
- Warnings: Spell check, readability, freshness (>6mo), orphaned docs

**Manual Reviews**:
- Quarterly: Quality trends, SLA compliance, bypass frequency
- Monthly: 10 random PR spot checks, health reports

**Policy Updates**: Annual cycle | Emergency for security/compliance (immediate)

---

## Integration Points

### With Other Skills

**documentation-health**:
- Provides quality scores for approval gates
- Validates completeness for merge requirements
- Generates health reports for audits

**documentation-standards**:
- Defines style rules enforced in review checklist
- Provides formatting validation for CI checks
- Sets style baseline for contributor guidelines

**documentation-content**:
- Content creation follows governance workflows
- New docs go through approval gates
- Templates include ownership metadata

### With External Systems

**GitHub**:
- CODEOWNERS file for ownership
- Branch protection rules
- PR templates and automation
- Issue templates for doc requests
- Actions for CI/CD checks

**CI/CD Pipeline**:
- Quality gate enforcement
- Automated reviewer assignment
- Breaking change detection
- Audit log generation

**Communication Tools**:
- Slack notifications for review requests
- Email alerts for SLA breaches
- Dashboard for governance metrics

---

## Common Scenarios

**See detailed workflows in references**:
- New document creation → `references/review-workflow.md`
- Breaking changes → `references/approval-gates.md`
- Emergency fixes → Fast-track review (30min SLA)
- Ownership transfer → 2-week shadow period
- Quarterly audits → Metrics + 10 random PR samples

---

## Metrics and KPIs

**Review Efficiency**: Time to first review <24hrs, merge <72hrs, >80% first-pass approval
**Quality**: Avg health score >0.75, bypass rate <5%, rollback rate <2%
**Ownership**: 3-10 docs/owner, response <48hrs, bus factor ≥2 for critical docs
**Audit**: 100% PR coverage, >95% compliance, <10% SLA breaches

---

## Implementation Checklist

### Initial Setup

- [ ] Create CODEOWNERS file with ownership assignments
- [ ] Configure branch protection rules
- [ ] Set up CI/CD gates (quality, links, approvers)
- [ ] Create PR template with governance fields
- [ ] Define review checklist template
- [ ] Document escalation paths
- [ ] Train owners and maintainers
- [ ] Establish baseline metrics

### Ongoing Operations

- [ ] Review PRs within SLA (48 hours)
- [ ] Run quarterly governance audits
- [ ] Update CODEOWNERS as teams change
- [ ] Monitor quality score trends
- [ ] Investigate gate bypasses
- [ ] Handle ownership transitions
- [ ] Respond to escalations
- [ ] Annual policy review

---

## References

- `references/review-workflow.md` - Detailed PR review process and checklists
- `references/approval-gates.md` - Gate configurations and bypass procedures
- `references/access-control.md` - Permission matrices and workflows

---

## Anti-Patterns

**DO NOT**:
- Bypass gates without documented justification
- Merge without required approvals
- Skip review for "minor" changes
- Allow single-owner critical docs
- Ignore quality score warnings
- Force-push to protected branches
- Delete documentation history
- Approve PRs you authored

**DO**:
- Follow the review checklist thoroughly
- Enforce gates consistently
- Document all bypasses with rationale
- Maintain audit trail
- Balance reviewer workload
- Update governance docs when patterns emerge
- Celebrate good documentation practices

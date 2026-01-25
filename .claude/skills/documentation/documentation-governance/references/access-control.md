# Access Control Reference

Permission models and workflows for documentation access management.

---

## Permission Levels

### Read-Only

**Who**: All team members by default

**Capabilities**:
- View all documentation in repository
- Clone repository locally
- Search documentation
- Open issues for documentation problems
- Comment on existing PRs

**Restrictions**:
- Cannot create branches
- Cannot open PRs
- Cannot edit files

**Use Cases**:
- New team members
- Read-only access for contractors
- External stakeholders (public repos)

---

### Contributor

**Who**: Team members who write documentation occasionally

**Capabilities (all Read-Only +)**:
- Fork repository
- Create branches
- Open pull requests
- Respond to review feedback
- Edit own PRs before merge

**Restrictions**:
- Cannot approve PRs
- Cannot merge PRs
- Cannot edit protected paths directly
- Cannot bypass gates

**Use Cases**:
- Engineers contributing to their domain docs
- Community contributors (open source)
- Infrequent documentation updates

---

### Maintainer

**Who**: Regular documentation contributors, domain experts

**Capabilities (all Contributor +)**:
- Review and approve PRs
- Merge non-protected documentation
- Request changes on PRs
- Manage documentation issues
- Update CODEOWNERS (for owned paths)
- Close stale PRs

**Restrictions**:
- Cannot merge protected paths without owner approval
- Cannot bypass quality gates
- Cannot override branch protection
- Limited to owned domains (per CODEOWNERS)

**Use Cases**:
- Documentation team members
- Domain technical leads
- Subject matter experts

**Responsibilities**:
- Review PRs within 48 hours
- Maintain documentation quality
- Enforce style guidelines
- Respond to documentation issues

---

### Owner

**Who**: Senior engineers, architects, documentation leads

**Capabilities (all Maintainer +)**:
- Approve changes to protected documentation (tier 2-3)
- Modify CODEOWNERS file
- Configure approval gates for owned domains
- Grant/revoke maintainer access within domain
- Override quality gates (with justification)
- Fast-track emergency changes
- Archive deprecated documentation

**Restrictions**:
- Cannot edit tier-1 protected docs without admin
- Cannot bypass all gates simultaneously
- Must document all gate overrides
- Subject to audit review

**Use Cases**:
- System architecture documentation
- Critical API documentation
- Cross-domain documentation
- Governance policy documentation

**Responsibilities**:
- Maintain high-level documentation accuracy
- Coordinate cross-domain changes
- Mentor maintainers and contributors
- Participate in quarterly governance reviews

---

### Admin

**Who**: Engineering leadership, platform team leads

**Capabilities (all Owner +)**:
- Edit tier-1 protected documentation
- Bypass any gate (with audit trail)
- Modify global governance policies
- Grant/revoke owner permissions
- Configure branch protection rules
- Emergency rollback authority
- Access to all audit logs

**Restrictions**:
- All bypasses logged and reviewed
- Major changes require committee approval
- Subject to external audit

**Use Cases**:
- CLAUDE.md updates
- SPEC.md major revisions
- Core architecture changes
- Emergency security fixes
- Governance policy updates

**Responsibilities**:
- Ensure documentation governance compliance
- Review bypass audit logs monthly
- Approve governance policy changes
- Handle escalations from owners
- Maintain system documentation integrity

---

## Permission Matrix

### By Document Type

| Document Type | Read | Create PR | Review | Merge | Override Gates |
|--------------|------|-----------|--------|-------|----------------|
| `/docs/guides/` | All | Contributor+ | Maintainer+ | Maintainer+ | Owner+ |
| `/docs/api/` | All | Contributor+ | Owner+ | Owner+ | Owner+ |
| `/docs/00-project/SPEC.md` | All | Contributor+ | Owner+ | Owner+ (2) | Admin |
| `/CLAUDE.md` | All | Owner+ | Admin | Admin | Admin |
| `/.claude/agents/` | All | Maintainer+ | Owner+ | Owner+ | Owner+ |
| `/.claude/skills/` | All | Maintainer+ | Owner+ | Owner+ | Owner+ |

**Legend**: `Role+` means role or higher

### By Action Type

| Action | Required Permission | Notes |
|--------|-------------------|-------|
| View documentation | Read-Only | Public repos: anyone |
| Open issue | Read-Only | Feedback mechanism |
| Fork & create PR | Contributor | All non-protected docs |
| Review PR | Maintainer | Must be in CODEOWNERS |
| Approve PR | Maintainer | Count toward merge requirements |
| Merge non-protected | Maintainer | After approvals + gates |
| Merge tier-2 protected | Owner (2 approvals) | Requires elevated permissions |
| Merge tier-1 protected | Admin | Highest restriction level |
| Modify CODEOWNERS | Owner | For owned domains only |
| Bypass quality gate | Owner | Requires justification |
| Bypass all gates | Admin | Emergency only, audit logged |
| Configure branch rules | Admin | Platform-level change |

---

## Permission Inheritance

### Directory-Based Inheritance

**Rules**:
1. Child directories inherit parent permissions by default
2. CODEOWNERS entries override inheritance
3. More restrictive child permissions allowed
4. Less restrictive child permissions blocked

**Example**:
```
/docs/                   @docs-team (Maintainer)
  /guides/               [inherits] @docs-team
    /advanced/           @senior-docs @tech-leads (Owner)
  /api/                  @api-team (Owner)
    /agents/             @agent-team (Owner)
```

**Inheritance Chain**:
- `/docs/guides/intro.md` → @docs-team (Maintainer)
- `/docs/guides/advanced/perf.md` → @senior-docs @tech-leads (Owner)
- `/docs/api/agents/overview.md` → @agent-team (Owner)

### Permission Elevation

**Cannot elevate child permissions** (security):
```
# INVALID - child cannot be less restrictive
/docs/                   @admin-team (Owner)
  /public/               @contributors (Contributor)  ❌ BLOCKED
```

**Can restrict child permissions**:
```
# VALID - child more restrictive than parent
/docs/                   @docs-team (Maintainer)
  /critical/             @tech-leads (Owner)  ✓ ALLOWED
```

---

## Access Workflows

### Granting Contributor Access

**Process**:
1. User requests access (via issue or HR onboarding)
2. Manager approves request
3. Admin adds user to team with Contributor role
4. User receives welcome doc with contribution guidelines
5. User can immediately create PRs

**Timeline**: Same-day for team members

---

### Granting Maintainer Access

**Criteria**:
- 5+ merged documentation PRs
- Demonstrates documentation quality standards
- Domain expertise verified
- Nominated by owner or admin

**Process**:
1. Owner nominates contributor
2. Review contribution history
3. Verify domain knowledge
4. Admin approves and adds to CODEOWNERS
5. Provide maintainer onboarding (review guidelines)
6. Shadow existing maintainer for 2 weeks

**Timeline**: 1-2 weeks

---

### Granting Owner Access

**Criteria**:
- 6+ months as maintainer
- 20+ documentation reviews completed
- Demonstrates leadership in documentation
- Cross-domain knowledge
- Recommended by admin or tech lead

**Process**:
1. Tech lead nominates maintainer
2. Documentation committee reviews
3. Interview with admin (governance understanding)
4. Admin approves and updates CODEOWNERS
5. Owner onboarding (governance, escalation paths)
6. Listed in public ownership matrix

**Timeline**: 2-4 weeks

---

### Revoking Access

**Triggers**:
- Team member leaves company
- Role change (no longer domain expert)
- Prolonged inactivity (>6 months)
- Policy violations
- Security concerns

**Process**:
1. Manager notifies admin of change
2. Admin removes from team/CODEOWNERS
3. Open PRs reassigned to other reviewers
4. Owned documents reassigned to new owner
5. Access revoked within 24 hours (immediate for security)
6. Exit interview for feedback (optional)

**Transition Period**:
- Planned departures: 2-week handoff
- Immediate departures: Same-day reassignment
- Security issues: Immediate revocation

---

## CODEOWNERS Configuration

### File Format

```
# CODEOWNERS - Documentation ownership and permissions
# Format: <path-pattern> <owner1> <owner2> ...
# Owners must have write access to approve PRs

# Global owners (fallback)
* @docs-team

# Critical system documentation (Admin level)
/CLAUDE.md @platform-admin @tech-lead
/docs/00-project/SPEC.md @architects @platform-admin

# Core project docs (Owner level - 2 approvals)
/docs/00-project/ @tech-lead @product-lead

# API documentation (domain owners)
/docs/api/agents/ @agent-team-lead @claude-code-ecosystem
/docs/api/skills/ @skills-team-lead
/docs/api/database/ @data-team-lead @dba-lead

# User-facing guides (maintainer + UX review)
/docs/guides/ @docs-team
/docs/tutorials/ @docs-team @ux-reviewer

# Agent and skill documentation
/.claude/agents/ @claude-code-ecosystem @platform-team
/.claude/skills/ @skills-lead @claude-code-ecosystem

# Infrastructure documentation
/docs/infrastructure/ @sre-team @platform-team

# Planning documentation
/docs/01-planning/ @product-team @tech-leads

# Governance documentation (self-referential)
/.claude/skills/documentation/documentation-governance/ @docs-lead @platform-admin
```

### Pattern Matching

**Supported Patterns**:
- `*` - Match any file in current directory
- `**` - Match recursively (all subdirectories)
- `*.md` - Match by extension
- `/path/` - Match directory and contents
- `/path/file.md` - Match specific file

**Pattern Priority** (last match wins):
```
/docs/ @docs-team
/docs/api/ @api-team
/docs/api/agents/ @agent-team  # This wins for /docs/api/agents/file.md
```

### Team Definitions

**GitHub Teams** (centrally managed):
```
@org/docs-team         # Documentation maintainers
@org/tech-leads        # Engineering tech leads
@org/architects        # System architects
@org/platform-admin    # Platform administrators
@org/agent-team        # Agent domain experts
@org/skills-team       # Skills domain experts
```

**Benefits**:
- Centralized membership management
- Easy team changes (no CODEOWNERS edit needed)
- Consistent across all repositories
- Supports nested teams

---

## Access Audit

### Regular Audits

**Quarterly Review**:
1. List all users with Maintainer+ access
2. Verify employment status (no ex-employees)
3. Check activity (remove if inactive >6 months)
4. Validate domain alignment (still owns that code)
5. Review bypass/override usage
6. Update access control documentation

**Annual Deep Audit**:
- Review all CODEOWNERS entries
- Interview owners about workload
- Rebalance ownership (avoid overload)
- Identify single points of failure
- Succession planning

### Audit Metrics

Track per permission level:
- **User count**: Total users at each level
- **Activity rate**: % active in last 90 days
- **Approval velocity**: Average time to approve PRs
- **Override frequency**: Gate bypasses per user
- **Ownership distribution**: Docs per owner

**Red Flags**:
- Inactive users >6 months with Owner+ access
- Single owner for critical documentation
- Owner with >20 documents (overload risk)
- Admin accounts with regular activity (should delegate)
- High override frequency (>5/month per user)

### Access Logs

**What to Log**:
- Permission grants/revocations (who, when, why)
- Gate bypasses (user, gate, justification)
- Protected path edits (user, path, approvers)
- CODEOWNERS modifications (who changed what)
- Admin actions (all elevated operations)

**Retention**: Permanent (compliance requirement)

**Review Cadence**: 
- Security team: Weekly spot checks
- Documentation committee: Monthly review
- Compliance: Quarterly export

---

## Permission Scenarios

### Scenario: External Contributor

**Situation**: Open-source contributor wants to fix typo

**Access Level**: Read-Only (public repo)

**Workflow**:
1. Fork repository
2. Make changes in fork
3. Open PR from fork
4. Auto-assigned to docs-team via CODEOWNERS
5. Maintainer reviews and merges
6. Contributor has no direct access

---

### Scenario: New Team Member Documentation

**Situation**: New engineer needs to update API docs for their feature

**Access Level**: Contributor

**Workflow**:
1. Onboarding grants Contributor access
2. Create branch, update docs
3. Open PR
4. Domain owner reviews (from CODEOWNERS)
5. Owner merges after approval
6. Engineer cannot merge own PRs

---

### Scenario: Domain Expert Taking Ownership

**Situation**: Senior engineer becomes owner of database documentation

**Access Level**: Owner

**Workflow**:
1. Tech lead nominates for ownership
2. Admin reviews contribution history
3. Admin adds to CODEOWNERS: `/docs/database/ @new-owner`
4. New owner can now review and merge database doc PRs
5. New owner joins quarterly governance reviews
6. Cannot merge tier-1 docs (still needs Admin)

---

### Scenario: Emergency Security Fix

**Situation**: Code example in docs has SQL injection vulnerability

**Access Level**: Admin (emergency bypass)

**Workflow**:
1. Security team identifies issue
2. Admin creates hotfix PR
3. Admin bypasses quality gate (logs justification)
4. Single admin approval sufficient (emergency)
5. Merge immediately
6. Post-mortem within 24 hours
7. Bypass logged in audit trail

---

### Scenario: Reorganization

**Situation**: Moving `/docs/old-structure/` to `/docs/new-structure/`

**Access Level**: Owner (coordination across teams)

**Workflow**:
1. Owner creates reorganization plan
2. Update all cross-references
3. Set up redirects
4. PR affects multiple domains (multiple CODEOWNERS)
5. Requires approval from all affected owners
6. Coordinate merge timing with release
7. Update CODEOWNERS to reflect new structure

---

## Permission Best Practices

**DO**:
- Use GitHub teams instead of individual accounts in CODEOWNERS
- Assign 2+ owners to critical documentation
- Review permissions quarterly (remove inactive users)
- Grant minimum necessary permissions
- Document ownership changes in git history
- Provide onboarding for each permission level
- Monitor override/bypass usage patterns
- Balance workload across owners (3-10 docs each)

**DON'T**:
- Grant Admin access for routine work
- Use personal accounts in CODEOWNERS (use teams)
- Allow single-owner critical documentation
- Skip permission reviews (security risk)
- Grant permissions without onboarding
- Override gates without documentation
- Keep inactive users at elevated permissions

---

## Troubleshooting

### "PR blocked: No reviewer from CODEOWNERS"

**Cause**: Changed files not covered by CODEOWNERS or owners not available

**Solution**:
1. Check CODEOWNERS file for matching pattern
2. If no pattern, add to CODEOWNERS or use fallback owner
3. If owner unavailable, contact team lead for reassignment
4. Emergency: Admin can manually approve

---

### "Cannot merge: Protected path requires 2 approvals"

**Cause**: Attempting to merge tier-2 protected doc with only 1 approval

**Solution**:
1. Request second approval from another owner
2. Check CODEOWNERS for eligible approvers
3. Wait for second reviewer (SLA: 48 hours)
4. Emergency: Contact admin for bypass (with justification)

---

### "Access denied: You don't have permission to edit this file"

**Cause**: User lacks necessary permission level

**Solution**:
1. Verify current permission level (check team membership)
2. If contributor: create PR instead of direct edit
3. If need elevated access: request from manager
4. Check if file is in protected path (may require owner/admin)

---

## Summary

Access control ensures documentation integrity through graduated permissions. Start with minimum necessary access (Contributor), earn trust through contributions, and progress to higher levels (Maintainer → Owner → Admin) based on demonstrated expertise and need.

# Frameworks for Doc Librarian

**Purpose**: Methodology documentation for three-tier safety model and workflow operations

---

## Three-Tier Safety Model

### Tier 1: Read-Only Analysis (MVP - Always Safe)

**Capabilities**:
- Link validation (internal and external)
- Organization compliance checking
- Naming convention validation
- Cross-reference mapping
- Orphan file detection
- Health metrics calculation

**Tools**: Read, Grep, Glob only

**Output**: Health report with violations and recommendations

---

### Tier 2: Automated Enhancements (Safe Fixes)

**Capabilities**:
- Fix broken internal links (path corrections)
- Rename files for naming compliance
- Update cross-references after moves
- Add missing frontmatter metadata
- Markdown auto-fix (markdownlint-cli rules)

**Validation**: Mandatory read-back verification for all modifications

**Tools**: Read, Grep, Glob, Edit (sequential operations only)

**Output**: Health report + applied fixes with verification status

**Auto-Fix Rules** (via markdownlint-cli):
- Blanks, spaces, tabs normalization
- Heading formatting
- 24 fixable rules total (see `.pre-commit-config.yaml`)

---

### Tier 3: Supervised Restructuring (Future)

**Capabilities**:
- Move orphaned files to correct locations
- Reorganize directory structures
- Consolidate duplicate content
- Archive stale documentation

**Approval**: User confirmation required before execution

**Tools**: All tools with coordination

**Output**: Restructuring plan with impact analysis for user review

---

## Workflow Operations

### 1. Health Check Workflow (`check_health`)

**Input**:
```json
{
  "context": "Full health check with link validation",
  "scope": "docs/** OR .claude/docs/** OR both",
  "include_external_links": false,
  "execution_timestamp": "ISO 8601 UTC"
}
```

**6-Phase Process**:
1. **Analysis** - Determine scope, estimate file count, select Tier 1
2. **Validation** - Execute link/organization/naming checks
3. **Aggregation** - Calculate health scores, classify violations by severity
4. **Reporting** - Generate structured health report with recommendations
5. **Verification** - Validate report completeness, check critical issues
6. **Reflection** - Document coverage percentage, flag incomplete areas

**Performance**: ~2-5 minutes full scan, ~30s incremental

---

### 2. Fix Broken Links Workflow (`fix_links`)

**Input**:
```json
{
  "context": "Fix all broken internal links in docs/",
  "scope": "docs/**",
  "auto_apply": true,
  "execution_timestamp": "ISO 8601 UTC"
}
```

**6-Phase Process**:
1. **Analysis** - Parse context, identify broken links
2. **Research** - Search for correct target paths
3. **Planning** - Generate fix plan with file→link mapping
4. **Implementation** - Apply fixes sequentially (Tier 2)
5. **Validation** - Verify all links resolve, no new breaks
6. **Reflection** - Document fixes applied, success rate, escalations

**Safety**: Mandatory read-back verification, fix forward on failure

---

### 3. Rename for Compliance Workflow (`rename_files`)

**Input**:
```json
{
  "context": "Rename files for kebab-case compliance",
  "scope": "docs/04-guides/**",
  "preview_only": false,
  "execution_timestamp": "ISO 8601 UTC"
}
```

**6-Phase Process**:
1. **Analysis** - Identify naming violations, generate compliant names
2. **Validation** - Check conflicts, verify no reserved names
3. **Planning** - Create rename map with cross-reference updates
4. **Implementation** - Apply renames, update refs (Tier 2)
5. **Validation** - Verify no broken refs, check git history
6. **Reflection** - Document renames completed, cross-refs updated

**Note**: Actual rename may require orchestrator coordination (git mv)

---

### 4. Organization Audit Workflow (`audit_organization`)

**Input**:
```json
{
  "context": "Audit docs/ against DOCS-MANAGEMENT.md",
  "generate_move_plan": true,
  "execution_timestamp": "ISO 8601 UTC"
}
```

**6-Phase Process**:
1. **Analysis** - Load DOCS-MANAGEMENT.md rules, scan structure
2. **Research** - Analyze file content for correct placement
3. **Classification** - Categorize violations by severity
4. **Planning** - Generate move recommendations with rationale
5. **Validation** - Verify move targets, check conflicts
6. **Reflection** - Document audit findings, estimate effort

---

## Coordination Protocols

### Claude-Code Agent Overlap

For `.claude/docs/` files:
- **Agent-specific guides** → claude-code agent (e.g., agent prompt optimization)
- **General documentation guides** → doc-librarian (e.g., file operation protocol)
- **When uncertain** → Coordinate with orchestrator for assignment

### Git-GitHub Agent Handoff

1. Doc-librarian modifies files → Returns SUCCESS with changes list
2. Orchestrator reviews changes → Delegates to git-github for commit
3. Commit message format: `docs: <description> (doc-librarian automated fix)`

---

## Error Recovery Patterns

### Link Validation Failures
- Retry with exponential backoff for transient errors
- Classify permanent failures (404) vs temporary (timeout)
- Provide partial results for successful validations
- Document unreachable links with error details

### File Operation Failures
- Follow `file-operation-protocol.md` for fallback strategies
- Fix forward on validation failure (Git tracks changes)
- Document failure context for orchestrator escalation
- Validate content BEFORE writing (prevention over recovery)

### Graceful Degradation
- Return partial health report if full scan incomplete
- Document scan coverage percentage
- Prioritize critical violations in partial results
- Suggest retry strategy for incomplete operations

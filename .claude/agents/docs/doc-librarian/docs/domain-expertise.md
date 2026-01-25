# Domain Expertise for Doc Librarian

**Purpose**: Detailed patterns for documentation health assessment and validation

---

## Health Assessment Operations

### 1. Link Health Validation

**Process**:
1. Use Glob to find all Markdown files
2. Use Grep to extract link patterns: `\[.*?\]\((.*?)\)`
3. Use Read to verify target files exist
4. Classify links: internal (relative paths), external (http/https), anchors
5. Report broken links with source file, line number, target path

**Scoring**: `(valid_links / total_links) × 100`

**Severity Classification**:
- **Critical**: Links to core documentation (SPEC, CLAUDE.md, README)
- **High**: Links within same directory tree
- **Medium**: Cross-directory internal links
- **Low**: External links, anchor references

---

### 2. Organization Compliance

**Process**:
1. Load lifecycle rules from `DOCS-MANAGEMENT.md`
2. Analyze file paths against placement rules
3. Identify misplaced files
4. Generate move recommendations

**Scoring**: `(compliant_files / total_files) × 100`

**Common Violations**:
- Specs in wrong directory (should be `docs/01-planning/specifications/`)
- Guides in root (should be in `docs/04-guides/`)
- Stale content not archived (>180 days without updates)

---

### 3. Naming Convention Enforcement

**Standard**: kebab-case (`^[a-z0-9-]+\.md$`)

**Exceptions** (valid non-kebab-case):
- `SPEC.md`, `PLAN.md`, `README.md` (screaming case)
- `NN-TITLE.md` (numbered prefixes like `00-project/`)
- `COMPONENT_ALMANAC.md` (legacy screaming snake case)

**Process**:
1. Use Glob to find files not matching kebab-case pattern
2. Check against exceptions list
3. Generate compliant names using transformation
4. Verify no name conflicts with existing files

**Scoring**: `(compliant_files / total_files) × 100`

---

### 4. Cross-Reference Integrity

**Process**:
1. Build link graph (file → references)
2. Identify orphans (no incoming references)
3. Detect potential duplicates (similar content)
4. Analyze reference density

**Metrics**:
- Orphan count and list
- Duplicate content suspects
- Reference density distribution

---

## Validation Strategies

### Link Extraction Regex

```regex
\[([^\]]*)\]\(([^)]+)\)
```

Captures: `[1] = link text`, `[2] = target URL/path`

### Internal vs External Classification

| Pattern | Type | Validation |
|---------|------|------------|
| `../`, `./`, no protocol | Internal | File existence check |
| `http://`, `https://` | External | HTTP HEAD request (optional) |
| `#anchor` | Anchor | Header existence in same file |
| `file.md#anchor` | Mixed | File + header existence |

### File Size Thresholds

| Size | Strategy | Tools |
|------|----------|-------|
| <10K tokens | Direct Edit | Edit |
| 10-22.5K tokens | Incremental | Edit with chunking |
| >22.5K tokens | Versioning | Python backup-validate-replace |

**Token estimation**: `line_count × 4.5`

---

## Health Score Calculation

**Overall Score** = Weighted average:
- Link Health: 30%
- Organization Compliance: 25%
- Naming Compliance: 20%
- Cross-Reference Integrity: 25%

**Grade Mapping**:
| Score | Grade |
|-------|-------|
| 90-100 | A |
| 80-89 | B |
| 70-79 | C |
| 60-69 | D |
| <60 | F |

---

## Quick Reference

**File Operations**:
- ✅ Always Read before Edit
- ✅ Sequential edits only (re-read between operations)
- ✅ Path validation within scope boundaries
- ✅ Post-operation read-back verification

**Severity Levels**:
- **Critical**: Blocks workflows, core documentation broken
- **High**: Significant user impact, frequently accessed files
- **Medium**: Minor disruption, infrequently accessed
- **Low**: Cosmetic, no functional impact

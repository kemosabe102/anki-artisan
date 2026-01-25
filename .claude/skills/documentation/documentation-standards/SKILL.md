---
name: documentation-standards
description: >
  Enforces documentation style consistency including tone, formatting, completeness, 
  and structural patterns. Validates against style guides and generates compliance reports.
  Use when: "standardize tone", "fix formatting", "style check", "enforce consistency", 
  "documentation compliance", "lint docs". 
  NOT for: structure (documentation-organization), health (documentation-health).
---

# Documentation Standards

Comprehensive style enforcement for project documentation, ensuring consistency in tone, formatting, and completeness across all markdown files.

---

## When to Use This Skill

**TRIGGER KEYWORDS**: "standardize tone", "fix formatting", "style check", "enforce consistency", "documentation compliance", "lint docs", "validate style"

**USE FOR**:
- Style consistency validation
- Tone and voice standardization
- Formatting rule enforcement
- Completeness verification
- Style guide compliance scoring
- Documentation linting

**NOT FOR**:
- Structural organization (use `documentation-organization`)
- Health scoring and technical accuracy (use `documentation-health`)
- Content generation (use domain-specific skills)

---

## Core Principles

### 1. Consistency Over Perfection
- Apply rules uniformly across all documentation
- Prefer consistent "wrong" choices over inconsistent "right" ones
- Document exceptions explicitly in frontmatter

### 2. Readability First
- Optimize for scanning and comprehension
- Use visual hierarchy effectively
- Balance brevity with completeness

### 3. Progressive Disclosure
- Start with high-level overview
- Provide depth on demand (collapsibles, links to references)
- Use examples to illustrate complex rules

---

## Style Guidelines

### Voice and Tone

**IMPERATIVE VOICE** for instructions:
- ✅ "Run the command"
- ❌ "You should run the command"

**ACTIVE VOICE** preference:
- ✅ "The agent processes the request"
- ❌ "The request is processed by the agent"
- **EXCEPTION**: Passive when actor is irrelevant

**PRESENT TENSE** for facts:
- ✅ "The system validates inputs"
- ❌ "The system will validate inputs"

See `references/style-guide.md` for complete terminology glossary and voice guidelines.

---

## Formatting Rules

### Code Blocks

**ALWAYS** specify language:
```python
def example():
    pass
```

**NEVER** use plain fenced blocks without language tags.

### Lists

**UNORDERED**: Use `-` (hyphen) consistently
**ORDERED**: Use `1.` for all items (auto-numbering)
**NESTING**: Maximum 2 levels deep

### Tables

**REQUIREMENTS**:
- Header row mandatory
- Specify alignment (`:---`, `:---:`, `---:`)
- Minimum 3 characters in separator

### Links

**DESCRIPTIVE TEXT**: Never "click here"
**RELATIVE PATHS**: Use project-relative paths for internal links
**EXTERNAL**: Include protocol (`https://`)

See `references/formatting-rules.md` for complete Markdown standards.

---

## Completeness Checks

### Required Sections by Document Type

**README.md**: Title, Description, Installation, Quick Start, Documentation link
**SPEC.md**: Frontmatter, Purpose, Architecture, Components, API, Examples, References
**SKILL.md**: Frontmatter, When to Use, Core Principles, Methodology, Examples, References
**GUIDE.md**: Purpose, Prerequisites, Steps, Verification, Troubleshooting, Next Steps
**API.md**: Overview, Authentication, Endpoints, Parameters, Response Format, Errors, Examples

See `references/completeness-checklist.md` for detailed requirements per document type.

### Frontmatter Standards

**REQUIRED FIELDS**:
```yaml
---
title: Document Title
version: 1.0.0
last_updated: 2025-12-13
---
```

**OPTIONAL**: status, tags, author, reviewers

### Table of Contents

**REQUIREMENT**: Files >100 lines must include TOC
**PLACEMENT**: After frontmatter, before first H2
**FORMAT**: Auto-generated preferred

---

## Compliance Scoring

### Scoring Formula

```
Compliance Score = (Style×0.3) + (Formatting×0.3) + (Completeness×0.25) + (Examples×0.15)
```

### Component Scores

**Style (30%)**:
- Heading hierarchy (no skips)
- Voice consistency (imperative for instructions)
- Terminology alignment with glossary

**Formatting (30%)**:
- Code blocks with language tags
- List style consistency
- Table formatting (headers, alignment)
- Link descriptiveness

**Completeness (25%)**:
- Required sections present
- Frontmatter completeness
- TOC presence (for files >100 lines)
- Cross-references validity

**Examples (15%)**:
- Example presence (one per major concept)
- Runnable examples (executable code)
- Output demonstration

### Thresholds

| Score | Rating | Action |
|-------|--------|--------|
| ≥0.90 | Excellent | Maintain |
| 0.75-0.89 | Good | Minor improvements |
| 0.60-0.74 | Needs work | Prioritize fixes |
| <0.60 | Non-compliant | Immediate attention |

### Sample Report

```
Documentation Compliance Report
================================
File: docs/guides/authentication.md

Style:        0.85 (Good)
Formatting:   0.92 (Excellent)
Completeness: 0.78 (Good)
Examples:     0.70 (Needs improvement)

Overall:      0.82 (Good)

Issues:
- Missing imperative voice (lines 45, 67, 89)
- Missing language tag (line 123)
- No example for "token refresh" (section 4.2)

Recommendations:
1. Add runnable example for token refresh
2. Convert passive instructions to imperative
3. Tag code block at line 123 as 'python'
```

---

## Validation Workflow

### Pre-Commit Checks (Automated)

1. Heading hierarchy validation
2. Code block language tag presence
3. Required sections verification
4. Broken link detection

### Manual Review (Periodic)

1. Voice and tone consistency
2. Terminology alignment
3. Example quality and relevance
4. Cross-document consistency

### Common Violations

**HEADING SKIP** (Critical):
```markdown
# Title
### Subsection  ❌ Skipped H2
```
**FIX**: Insert H2 or demote H3

**UNTAGGED CODE** (High):
```markdown
\```
code  ❌ No language
\```
```
**FIX**: Add language tag

**PASSIVE VOICE INSTRUCTION** (Medium):
```markdown
"The config should be updated"  ❌
```
**FIX**: "Update the configuration"

**MISSING EXAMPLE** (Medium):
```markdown
## Feature Overview
Description only...  ❌ No example
```
**FIX**: Add code example

---

## Exception Handling

### Documented Exceptions

**FRONTMATTER OVERRIDE**:
```yaml
---
title: Legacy API Guide
style_exceptions:
  - heading_skip: "Intentional for visual hierarchy"
  - terminology: "Uses 'worker' for backward compatibility"
---
```

**INLINE MARKERS**:
```markdown
<!-- style-ignore: passive-voice -->
The system is designed to...
```

**USE SPARINGLY**: Exceptions should be rare and justified.

### Legacy Migration

**GRACE PERIOD**: 90 days for compliance after standard adoption

**PRIORITY**:
1. Critical (user-facing): Immediate
2. High (developer guides): 30 days
3. Medium (internal specs): 60 days
4. Low (archived): 90 days

---

## Integration with Other Skills

### Complementary Skills

**documentation-organization**: Structure (directory, files)
**documentation-health**: Technical accuracy, freshness
**documentation-standards**: Style, formatting, tone

### Workflow

1. Organization → Set up structure
2. **Standards** → Enforce style during creation
3. Health → Validate accuracy

### Anti-Patterns

**AVOID**:
- Enforcing style without teaching
- Rigidity without flexibility
- Style over substance
- Retroactive enforcement without grace period

---

## Quick Reference Checklist

### Style
- [ ] One H1 per document
- [ ] No heading level skips
- [ ] Imperative voice for instructions
- [ ] Active voice preference
- [ ] Consistent terminology
- [ ] Oxford comma in lists

### Formatting
- [ ] All code blocks have language tags
- [ ] Lists use consistent markers (`-`)
- [ ] Tables have headers and alignment
- [ ] Links have descriptive text
- [ ] Relative paths for internal links
- [ ] Horizontal rules use `---`

### Completeness
- [ ] Frontmatter with required fields
- [ ] All required sections present
- [ ] TOC for files >100 lines
- [ ] One example per major concept
- [ ] Valid cross-references

---

## Examples

### Example 1: Style Violation Fix

**BEFORE** (Score: 0.62):
```markdown
# API Guide
### Authentication
You should authenticate by sending your API key.
```

**AFTER** (Score: 0.94):
```markdown
# API Guide
## Authentication

Authenticate by sending your API key:

\```python
headers = {"Authorization": "Bearer YOUR_API_KEY"}
response = requests.get("https://api.example.com", headers=headers)
\```
```

**IMPROVEMENTS**: Added H2, imperative voice, runnable example

---

### Example 2: Completeness Enhancement

**BEFORE** (Score: 0.58):
```markdown
# Database Setup
Connect using the connection string.
```

**AFTER** (Score: 0.91):
```markdown
---
title: Database Setup Guide
version: 1.0.0
last_updated: 2025-12-13
---

# Database Setup

## Prerequisites
- PostgreSQL 14+
- Database credentials

## Connection

\```python
from sqlalchemy import create_engine

connection_string = "postgresql://user:pass@localhost:5432/db"
engine = create_engine(connection_string)
\```

## Verification

\```python
with engine.connect() as conn:
    result = conn.execute("SELECT version()")
    print(result.fetchone())
\```
```

**IMPROVEMENTS**: Frontmatter, prerequisites, examples, verification

---

### Example 3: Formatting Consistency

**BEFORE**:
```markdown
* Feature one
- Feature two
\```
code
\```
```

**AFTER**:
```markdown
- Feature one
- Feature two

\```python
def code():
    pass
\```
```

**IMPROVEMENTS**: Consistent list markers, language tag

---

## References

Detailed guides in `references/` directory:

- **style-guide.md** - Voice, tone, terminology glossary, capitalization rules
- **formatting-rules.md** - Markdown formatting standards, code blocks, lists, tables, links
- **completeness-checklist.md** - Required sections per document type, validation checklist

---

## Changelog

### Version 1.0.0 (2025-12-13)
- Initial release
- Style guidelines (voice, tone, terminology)
- Formatting rules (code blocks, lists, tables, links)
- Completeness checks (required sections, frontmatter, TOC)
- Compliance scoring methodology
- Validation workflow and common violations
- Exception handling and legacy migration strategy

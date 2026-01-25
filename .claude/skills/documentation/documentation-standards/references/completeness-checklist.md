# Documentation Completeness Checklist

Required sections and elements by document type to ensure comprehensive, useful documentation.

---

## Universal Requirements

All documentation files must include:

- [ ] **Title** (H1, one per document)
- [ ] **Frontmatter** (YAML with required fields)
- [ ] **Introduction** (1-2 sentence overview)
- [ ] **At least one example** per major concept
- [ ] **Horizontal rules** to separate major sections
- [ ] **Valid internal links** (no broken references)

### Frontmatter Requirements

```yaml
---
title: [required]
version: [required, format: X.Y.Z]
last_updated: [required, format: YYYY-MM-DD]
status: [optional, one of: draft | review | approved | archived]
tags: [optional, array of keywords]
---
```

---

## README.md

Root-level project overview and quick start guide.

### Required Sections

- [ ] **Title** (project name)
- [ ] **Description** (1-2 sentences, what the project does)
- [ ] **Features** (bullet list of key capabilities)
- [ ] **Installation** (step-by-step setup)
- [ ] **Quick Start** (minimal working example)
- [ ] **Documentation** (link to full docs)
- [ ] **License** (link or inline)

### Optional Sections

- [ ] **Badges** (build status, coverage, version)
- [ ] **Screenshots/Demos** (visual examples)
- [ ] **Contributing** (guidelines for contributors)
- [ ] **Support** (how to get help)
- [ ] **Acknowledgments** (credits)

### Example Template

```markdown
# Project Name

Brief description of what this project does and who it's for.

## Features

- Key feature one
- Key feature two
- Key feature three

## Installation

\```bash
uv pip install project-name
\```

## Quick Start

\```python
from project import main

result = main()
print(result)
\```

## Documentation

Full documentation available at [docs/](docs/).

## License

MIT License - see [LICENSE.md](LICENSE.md)
```

---

## SPEC.md

Technical specification for system design and architecture.

### Required Sections

- [ ] **Frontmatter** (version, date, status)
- [ ] **Purpose/Overview** (system goals and scope)
- [ ] **Architecture** (high-level design, diagrams)
- [ ] **Components** (major modules with descriptions)
- [ ] **Data Models** (entities and relationships)
- [ ] **APIs/Interfaces** (external and internal contracts)
- [ ] **Examples** (usage scenarios)
- [ ] **Dependencies** (external systems and libraries)
- [ ] **Deployment** (environment requirements)
- [ ] **References** (related documents)

### Optional Sections

- [ ] **Decision Log** (architectural decisions and rationale)
- [ ] **Performance Requirements** (latency, throughput targets)
- [ ] **Security Considerations** (authentication, authorization)
- [ ] **Scalability** (growth projections)
- [ ] **Monitoring** (observability strategy)

---

## SKILL.md

Agent skill definition with methodology and examples.

### Required Sections

- [ ] **Frontmatter** (name, description with trigger keywords)
- [ ] **When to Use** (trigger keywords, use cases, anti-use-cases)
- [ ] **Core Principles** (foundational concepts, 3-5 principles)
- [ ] **Methodology/Workflow** (step-by-step process)
- [ ] **Examples** (at least 2-3 complete scenarios)
- [ ] **References** (links to reference files in `references/`)

### Optional Sections

- [ ] **Anti-Patterns** (common mistakes to avoid)
- [ ] **Integration** (how to combine with other skills)
- [ ] **Troubleshooting** (common issues and solutions)
- [ ] **Changelog** (version history)

### Frontmatter Requirements

```yaml
---
name: skill-name
description: >
  Brief description of what the skill does.
  Use when: "keyword1", "keyword2", "keyword3".
  NOT for: other-skill-name.
---
```

---

## GUIDE.md

Step-by-step tutorial or how-to documentation.

### Required Sections

- [ ] **Purpose** (what you'll learn/accomplish)
- [ ] **Prerequisites** (required knowledge, tools, setup)
- [ ] **Steps** (numbered, imperative instructions)
- [ ] **Verification** (how to confirm success)
- [ ] **Examples** (complete walkthrough)
- [ ] **Troubleshooting** (common issues)
- [ ] **Next Steps** (what to do after)

### Optional Sections

- [ ] **Background** (contextual information)
- [ ] **Best Practices** (recommendations)
- [ ] **Advanced Usage** (beyond basics)
- [ ] **Related Guides** (cross-references)

### Example Structure

```markdown
# Guide: Setting Up PostgreSQL with TimescaleDB

## Purpose

Learn to install and configure PostgreSQL with TimescaleDB extension for time-series data storage.

## Prerequisites

- PostgreSQL 14+ installed
- Admin access to database
- Basic SQL knowledge

## Steps

1. Install PostgreSQL
   \```bash
   uv run install postgresql
   \```

2. Enable TimescaleDB extension
   \```sql
   CREATE EXTENSION IF NOT EXISTS timescaledb;
   \```

3. Verify installation
   \```sql
   SELECT * FROM pg_extension WHERE extname = 'timescaledb';
   \```

## Verification

Run test query to confirm TimescaleDB functions:
\```sql
SELECT timescaledb_version();
\```

Expected output: Version string (e.g., "2.11.0")

## Next Steps

- [Configure hypertables](hypertables-guide.md)
- [Set up retention policies](retention-guide.md)
```

---

## API.md

Reference documentation for APIs, functions, or interfaces.

### Required Sections

- [ ] **Overview** (purpose and scope of API)
- [ ] **Authentication** (how to authenticate requests)
- [ ] **Base URL** (endpoint root)
- [ ] **Endpoints/Functions** (organized by category)
- [ ] **Parameters** (name, type, required/optional, description)
- [ ] **Response Format** (structure and data types)
- [ ] **Error Codes** (status codes and meanings)
- [ ] **Examples** (request and response for each endpoint)

### Optional Sections

- [ ] **Rate Limiting** (throttling policies)
- [ ] **Pagination** (how to handle large result sets)
- [ ] **Versioning** (API version strategy)
- [ ] **Webhooks** (event notifications)
- [ ] **SDKs** (client libraries)

### Example Structure

```markdown
## GET /api/agents

Retrieve list of active agents.

**Parameters**:

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `status` | string | No | Filter by status (active, idle, error) |
| `limit` | integer | No | Maximum results (default: 100) |

**Response**:

\```json
{
  "agents": [
    {
      "id": "agent-123",
      "name": "researcher-codebase",
      "status": "active"
    }
  ],
  "total": 1
}
\```

**Error Responses**:

| Code | Meaning |
|------|---------|
| 400 | Invalid parameters |
| 401 | Unauthorized |
| 500 | Server error |
```

---

## CHANGELOG.md

Version history and release notes.

### Required Sections

- [ ] **Title** (CHANGELOG or Release Notes)
- [ ] **Format** (version headers with dates)
- [ ] **Categories** (Added, Changed, Deprecated, Removed, Fixed, Security)
- [ ] **Links** (to commits, PRs, or issues)

### Format

Follow [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

## [Unreleased]

### Added
- New feature description

### Changed
- Modified behavior description

## [1.0.0] - 2025-12-13

### Added
- Initial release
- Feature one
- Feature two

### Fixed
- Bug fix description

[Unreleased]: https://github.com/user/repo/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

---

## Table of Contents

Required for files exceeding 100 lines.

### Requirements

- [ ] **Placement** (after frontmatter, before first H2)
- [ ] **Section links** (all H2 sections included)
- [ ] **Anchor format** (lowercase with hyphens)
- [ ] **Nested structure** (reflects document hierarchy)

### Example

```markdown
---
title: Documentation Standards
version: 1.0.0
last_updated: 2025-12-13
---

# Documentation Standards

## Table of Contents

- [Style Guidelines](#style-guidelines)
  - [Voice and Tone](#voice-and-tone)
  - [Terminology](#terminology)
- [Formatting Rules](#formatting-rules)
  - [Code Blocks](#code-blocks)
  - [Lists](#lists)
- [Completeness Checks](#completeness-checks)

## Style Guidelines

[Content...]
```

---

## Validation Checklist

Use this checklist before committing documentation:

### Style
- [ ] Heading hierarchy has no skips (H1 → H2 → H3)
- [ ] Instructions use imperative voice
- [ ] Consistent terminology per glossary
- [ ] Sentence case for headings
- [ ] Oxford comma in lists

### Formatting
- [ ] All code blocks have language tags
- [ ] Lists use consistent markers (`-` for unordered)
- [ ] Tables have headers and alignment
- [ ] Links have descriptive text (no "click here")
- [ ] Internal links use project-relative paths
- [ ] Horizontal rules use `---`

### Completeness
- [ ] Frontmatter with required fields (title, version, last_updated)
- [ ] All required sections present for document type
- [ ] TOC included for files >100 lines
- [ ] At least one example per major concept
- [ ] All internal links are valid

### Examples
- [ ] Each example has descriptive heading
- [ ] Code examples include language tags
- [ ] Runnable examples include setup/imports
- [ ] Expected output shown where applicable
- [ ] Comments explain non-obvious logic

### Cross-References
- [ ] Links to related documents included
- [ ] References section lists external resources
- [ ] All links tested and valid
- [ ] Anchor links match heading format

---

## Scoring Thresholds

### Overall Compliance

| Score | Rating | Action Required |
|-------|--------|-----------------|
| ≥0.90 | Excellent | Maintain quality |
| 0.75-0.89 | Good | Minor improvements |
| 0.60-0.74 | Needs work | Address issues before merge |
| <0.60 | Non-compliant | Immediate revision required |

### Component Scores

**Style** (30% of total):
- ≥0.90: Excellent voice, tone, and terminology consistency
- 0.75-0.89: Good, minor inconsistencies
- 0.60-0.74: Multiple style issues
- <0.60: Major style problems

**Formatting** (30% of total):
- ≥0.90: Perfect Markdown formatting
- 0.75-0.89: Minor formatting issues
- 0.60-0.74: Several formatting problems
- <0.60: Widespread formatting errors

**Completeness** (25% of total):
- ≥0.90: All required sections present
- 0.75-0.89: Missing optional sections only
- 0.60-0.74: Missing some required sections
- <0.60: Missing critical sections

**Examples** (15% of total):
- ≥0.90: Comprehensive, runnable examples
- 0.75-0.89: Good examples, some improvements needed
- 0.60-0.74: Minimal examples, missing context
- <0.60: Insufficient or poor-quality examples

---

## Migration Planning

For existing documentation not meeting standards:

### Assessment
1. Run validation tool on all docs
2. Generate compliance report
3. Categorize by priority (Critical, High, Medium, Low)
4. Estimate effort per document

### Prioritization
- **Critical** (user-facing): Immediate (0-7 days)
- **High** (developer guides): 30 days
- **Medium** (internal specs): 60 days
- **Low** (archived docs): 90 days

### Batch Processing
1. Group similar documents
2. Apply automated fixes (code tags, list markers)
3. Manual review for style and content
4. Validate and generate report

### Grace Period
- 90 days from standard adoption
- Document exceptions in frontmatter
- Track progress with status field: `status: migrating`

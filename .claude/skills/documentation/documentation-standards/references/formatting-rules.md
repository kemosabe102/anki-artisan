# Markdown Formatting Rules

Standardized Markdown formatting conventions for consistent rendering and maintainability.

---

## Code Blocks

### Language Tags

**ALWAYS** specify language for syntax highlighting:

```markdown
\```python
def example():
    pass
\```
```

**NEVER** use plain fenced blocks:
```markdown
❌ \```
code here
\```
```

### Supported Language Tags

| Language | Tag | Use For |
|----------|-----|---------|
| Python | `python` | Python code |
| Shell | `bash` or `shell` | Shell commands |
| JSON | `json` | JSON data |
| YAML | `yaml` | YAML configuration |
| Markdown | `markdown` | Markdown examples |
| Text | `text` or `plaintext` | Command output |
| SQL | `sql` | Database queries |

### Inline Code

Use single backticks for inline code:
- File paths: `docs/guides/setup.md`
- Functions: `calculate_score()`
- Variables: `context_quality`
- Short commands: `uv run pytest`

**DO NOT** use backticks for:
- Emphasis (use **bold** or *italic*)
- Links or URLs
- General technical terms without specific reference

---

## Lists

### Unordered Lists

Use hyphen (`-`) consistently for all unordered lists:

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

**AVOID** mixing markers:
```markdown
❌ - Item one
   * Item two
   + Item three
```

### Ordered Lists

Use `1.` for all items (auto-numbering):

```markdown
1. First step
1. Second step
1. Third step
```

**NOT**:
```markdown
❌ 1. First step
   2. Second step
   3. Third step
```

**RATIONALE**: Auto-numbering simplifies reordering and prevents numbering errors.

### Task Lists

Use `- [ ]` for checkboxes:

```markdown
- [ ] Incomplete task
- [x] Completed task
- [ ] Another pending task
```

### Nesting Depth

**MAXIMUM**: 2 levels deep for readability

```markdown
✅ - Level 1
     - Level 2
       - Level 3 (acceptable but use sparingly)

❌ - Level 1
     - Level 2
       - Level 3
         - Level 4 (too deep - refactor)
```

**ALTERNATIVE**: Use sections instead of deep nesting.

---

## Tables

### Basic Structure

All tables must have:
1. Header row
2. Separator row with alignment
3. Data rows

```markdown
| Column A | Column B | Column C |
|:---------|:--------:|--------:|
| Left     | Center   | Right   |
| Aligned  | Aligned  | Aligned |
```

### Alignment Syntax

| Syntax | Alignment | Use For |
|--------|-----------|---------|
| `:---` | Left | Text, descriptions |
| `:---:` | Center | Short labels, status |
| `---:` | Right | Numbers, scores |

### Minimum Column Width

Use at least 3 characters in separator for readability:

```markdown
✅ | Column A | Column B |
   |:---------|:---------|

❌ | A | B |
   |:-|:-|
```

### Complex Data

For key-value pairs, consider definition lists:

```markdown
**Term**
: Definition or detailed explanation

**Another Term**
: Another definition
```

---

## Links and References

### Link Text

Use descriptive text that makes sense out of context:

```markdown
✅ See the [API reference guide](link) for details.
✅ Consult the [PostgreSQL documentation](link).

❌ Click [here](link) for more information.
❌ See [this page](link).
```

### Internal Links

Use project-relative paths:

```markdown
✅ [SPEC.md](docs/00-project/SPEC.md)
✅ [Orchestrator Guide](docs/01-guides/orchestration/README.md)

❌ [SPEC.md](../../../docs/00-project/SPEC.md)
```

### External Links

Always include protocol:

```markdown
✅ https://example.com
✅ [Example Site](https://example.com)

❌ example.com
❌ [Example Site](example.com)
```

### Anchor Links

Use lowercase with hyphens for section anchors:

```markdown
[Jump to installation](#installation-guide)

## Installation Guide
```

**GENERATION**: Most Markdown processors auto-generate anchors from headings.

---

## Visual Elements

### Horizontal Rules

Use three hyphens with blank lines before and after:

```markdown
Content before the rule.

---

Content after the rule.
```

**AVOID**:
```markdown
❌ Content before.
---
Content after.

❌ ***

❌ ___
```

### Emphasis

**Bold**: Use double asterisks
```markdown
**important text**
```

**Italic**: Use single asterisks
```markdown
*emphasized text*
```

**CONSISTENCY**: Prefer `**` and `*` over `__` and `_`.

### Blockquotes

Use for callouts and important notes:

```markdown
> **NOTE**: This is important context that readers should be aware of.

> **WARNING**: Breaking change introduced in version 2.0.

> **TIP**: Use caching to improve performance.
```

**STRUCTURE**: Lead with bold label, followed by colon.

---

## Headings

### Hierarchy

Maintain logical progression without skipping levels:

```markdown
✅ # Title (H1)
   ## Section (H2)
   ### Subsection (H3)
   #### Detail (H4)

❌ # Title (H1)
   ### Subsection (H3)  ← Skipped H2
```

### Spacing

Use blank lines before and after headings:

```markdown
Previous paragraph ends here.

## New Section

First paragraph of section.
```

### Formatting

**NO** trailing punctuation:
```markdown
✅ ## Installation guide
❌ ## Installation guide.
❌ ## Installation guide:
```

**NO** formatting inside headings:
```markdown
✅ ## API reference
❌ ## **API Reference**
❌ ## `API` reference
```

---

## Frontmatter

### YAML Format

Use YAML frontmatter at the top of documents:

```yaml
---
title: Document Title
version: 1.0.0
last_updated: 2025-12-13
status: draft
tags: [documentation, standards]
---
```

### Required Fields

All documentation files should include:
- `title`: Human-readable title
- `version`: Semantic version (MAJOR.MINOR.PATCH)
- `last_updated`: ISO date (YYYY-MM-DD)

### Optional Fields

- `status`: draft | review | approved | archived
- `tags`: Array of searchable keywords
- `author`: Original creator
- `reviewers`: List of people who reviewed
- `related`: Links to related documents

---

## Special Cases

### Escaping

Escape special Markdown characters when needed:

```markdown
Use \* for literal asterisks
Use \_ for literal underscores
Use \` for literal backticks
```

### HTML in Markdown

**AVOID** HTML when Markdown syntax exists:

```markdown
✅ **bold text**
❌ <strong>bold text</strong>

✅ *italic text*
❌ <em>italic text</em>
```

**ACCEPTABLE** HTML uses:
- Collapsible sections (no Markdown equivalent)
- Complex tables (when Markdown is insufficient)
- Custom styling (use sparingly)

### Line Length

**GUIDELINE**: Soft wrap at 80-100 characters for readability

**EXCEPTIONS**:
- URLs and links (don't break)
- Code blocks (preserve formatting)
- Tables (maintain structure)

---

## File Naming

### Document Files

Use descriptive, lowercase names with hyphens:

```
✅ installation-guide.md
✅ api-reference.md
✅ troubleshooting-common-issues.md

❌ InstallationGuide.md
❌ API_Reference.md
❌ troubleshooting_common_issues.md
```

### Special Files

Standard file names (preserve case):
- `README.md` (uppercase, repository root)
- `CHANGELOG.md` (uppercase, version history)
- `LICENSE.md` (uppercase, legal)

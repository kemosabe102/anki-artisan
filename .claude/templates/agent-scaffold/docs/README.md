# docs/ Directory

**Purpose**: Externalized domain knowledge that would bloat the main agent definition

---

## What Goes Here

| File Type | Description | Example |
|-----------|-------------|---------|
| `user-guide.md` | End-user documentation (source) | Quick reference, getting started |
| `user-guide.docx` | End-user documentation (Google Docs import) | Generated via Pandoc |
| `domain-expertise.md` | Core concepts, taxonomies, principles | World-building elements, code patterns |
| `frameworks.md` | Methodologies the agent applies | SCAMPER, OODA, 5 Whys |
| `{{topic}}.md` | Additional specialized knowledge | Character creation, testing strategies |

---

## Templates

| Template | Purpose | Target Length |
|----------|---------|---------------|
| `user-guide.template.md` | End-user guide source (Markdown) | ~100 lines |
| `user-guide.template.docx` | End-user guide (Google Docs import) | Generated via Pandoc |
| `domain-expertise.template.md` | Domain knowledge externalization | Variable |
| `frameworks.template.md` | Methodology documentation | Variable |


### User Guide Template

The `user-guide.template.md` follows progressive disclosure and human readability principles.

**Structure (in order):**

1. **Get Started in 30 Seconds** - Copy-paste examples FIRST
2. **What You Can Say** - Organized by action category, not dense tables
3. **Modes/Features** - Card format with emoji headers, not tables
4. **Tips for Best Results** - Numbered with good/bad examples
5. **What You'll Get** - Checklist of deliverables
6. **Learn More** - Self-service discovery prompts

**Reference**: `progressive-disclosure-validation-framework.md` for quality scoring.

---

## Formatting Guidelines

**See**: `.claude/docs/01-guides/documentation/markdown-style-guide.md` for:
- White space and visual breathing room
- Strategic emoji usage
- Table vs card format decisions
- Callout boxes and code blocks
- Markdown-to-DOCX best practices

---

## Google Docs Workflow

**See**: `.claude/docs/01-guides/documentation/pandoc-workflow-guide.md` for:
- Pandoc installation (Windows/macOS/Linux)
- Markdown to DOCX conversion
- Google Docs import process
- Batch conversion scripts


---

## Guidelines

1. **Externalize when >50 lines** - Keep main agent lean
2. **One concept per file** - Easy to find and update
3. **Reference from main agent** - Add to Knowledge Base section
4. **Include quick reference** - Tables/checklists at end for fast lookup
5. **Progressive disclosure** - Most important information FIRST

---

## File Template

```markdown
# {{Topic Name}} for {{Agent Domain}}

**Purpose**: {{What this document provides}}

---

## {{Main Section 1}}

{{Content organized for agent consumption}}

---

## {{Main Section 2}}

{{More content}}

---

## Quick Reference

- [ ] {{Checklist item 1}}
- [ ] {{Checklist item 2}}
```

---

## See Also

- **Reference example**: `.claude/agents/ttrpg-campaign-architect/docs/`
- **Framework patterns**: `00-core/frameworks/README.md`
- **Progressive disclosure**: `progressive-disclosure-validation-framework.md`

---
title: "Markdown Style Guide"
date: 2025-11-30
status: ACTIVE
tags: [documentation, formatting, claude-docs]
---

# Markdown Style Guide

**Purpose**: Guidelines for creating scannable, inviting, and visually breathable documentation.

---

## White Space & Visual Breathing Room

- Use `&nbsp;` between major sections for vertical spacing
- Keep paragraphs to **2-3 sentences max**
- Insert `---` horizontal rules between distinct topics
- Limit content blocks to **8-10 lines** before a visual break

---

## Strategic Emoji Usage

Assign consistent emojis to section types:

| Purpose | Emoji | Example |
|---------|-------|---------|
| Quick start / Launch | 🚀 | `## 🚀 Get Started` |
| Actions / Commands | 🎯 | `## 🎯 What You Can Say` |
| Features / Modes | 🎨 | `## 🎨 Modes & Features` |
| Tips / Best practices | ✨ | `## ✨ Tips for Best Results` |
| Deliverables / Output | 📦 | `## 📦 What You'll Get` |
| Questions / Help | ❓ | `## ❓ Learn More` |
| Warnings | ⚠️ | `> ⚠️ **Warning**: ...` |
| Tips (inline) | 📌 | `> 📌 **Tip**: ...` |
| Success / Checkmarks | ✅ | `✅ **Feature name**` |
| Bad example | ❌ | `> ❌ *Don't do this*` |

**Rule**: Emojis in headers and callouts only. Avoid emoji overload in body text.

---

## Avoid Dense Tables

Replace tables with **card format** using subsections:

```markdown
### 🌍 World Builder

*Trigger words: "world", "setting", "realm"*

Creates locations, factions, creatures, and magic systems.
```

This is more scannable than:

```markdown
| Mode | What It Does | Trigger Words |
|------|--------------|---------------|
| World Builder | Creates locations... | "world", "setting" |
```


---

## Callout Boxes for Emphasis

Use blockquotes with emoji prefixes:

```markdown
> 📌 **Tip**: Early system info helps the agent tailor content.

> ⚠️ **Warning**: This action cannot be undone.

> ❌ *"Do something completely different"*
>
> ✅ *"Make this more [specific change]"*
```

---

## Code Blocks for Examples

Wrap example prompts in code blocks for easy copy-paste:

```markdown
Just tell the agent what you want:

\`\`\`
Help me build a campaign about pirates
\`\`\`
```

---

## Markdown-to-DOCX Best Practices

For clean Pandoc conversion:

- ✅ Use standard Markdown (`##`, `**bold**`, `*italic*`, `-` lists)
- ✅ Use `>` for blockquotes/callouts
- ✅ Use `&nbsp;` for vertical spacing (converts to empty paragraphs)
- ❌ Avoid nested lists beyond 2 levels
- ❌ Avoid complex merged-cell tables
- ❌ Avoid custom HTML or CSS

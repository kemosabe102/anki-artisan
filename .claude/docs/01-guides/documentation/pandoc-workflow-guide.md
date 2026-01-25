---
title: "Pandoc Workflow Guide"
date: 2025-11-30
status: ACTIVE
tags: [documentation, pandoc, google-docs, claude-docs]
---

# Pandoc Workflow Guide

**Purpose**: Convert Markdown documentation to DOCX for Google Docs import.

---

## Overview

User guides are maintained in Markdown (`.md`) and converted to DOCX for Google Docs import. DOCX preserves tables, lists, code blocks, and formatting far better than HTML.

---

## Prerequisites

Install Pandoc (one-time setup):

```bash
# Windows (winget)
winget install JohnMacFarlane.Pandoc

# macOS (Homebrew)
brew install pandoc

# Linux (apt)
sudo apt install pandoc
```


---

## Converting User Guides

After editing a `user-guide.md` file, regenerate the DOCX:

```bash
# From the agent's docs/ directory
pandoc user-guide.md -f markdown -t docx -s -o user-guide.docx
```

---

## Importing to Google Docs

1. Open Google Drive
2. Click **New** → **File upload**
3. Select the `.docx` file
4. Once uploaded, right-click → **Open with** → **Google Docs**
5. Google Docs converts it automatically with formatting preserved

---

## Why DOCX Instead of HTML?

| Format | Tables | Code Blocks | Lists | Google Docs Support |
|--------|--------|-------------|-------|---------------------|
| HTML | ❌ Often breaks | ❌ Lost | ⚠️ Partial | ❌ Not supported for import |
| Markdown | N/A (source) | N/A | N/A | ❌ No native import |
| DOCX | ✅ Full support | ✅ Preserved | ✅ Full support | ✅ Native import |


---

## Batch Conversion

Convert all user guides at once:

```bash
# From repository root (Windows PowerShell)
Get-ChildItem -Recurse -Filter "user-guide.md" | ForEach-Object {
    $docx = $_.FullName -replace '\.md$', '.docx'
    pandoc $_.FullName -f markdown -t docx -s -o $docx
}

# From repository root (bash/zsh)
find . -name "user-guide.md" -exec sh -c 'pandoc "$1" -f markdown -t docx -s -o "${1%.md}.docx"' _ {} \;
```

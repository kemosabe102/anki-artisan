---
title: "Agent Runtime Standards"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Agent Runtime Standards

**Auto-Load:** This minimal document is automatically loaded by all agents.

## Core Requirements

### Working Directory & Bash Behavior

## 🚫 CRITICAL: `cd` Commands Are BANNED and Will FAIL

**WHY:** Claude Code resets working directory between EVERY bash call. The `cd` command does nothing.

**CONSEQUENCE:** Using `cd` wastes tokens, API calls, and time. Security hooks BLOCK all `cd` commands.

**SOLUTION:** Use absolute or relative paths instead:

```bash
# ❌ WRONG - Will be BLOCKED by security hook
cd tests && uv run pytest unit/

# ✅ CORRECT - Use absolute path
uv run pytest C:/Users/kemos/Repos/gauntlet-agents/tests/unit/

# ✅ CORRECT - Use relative path from repo root
uv run pytest tests/unit/
```

**Path Usage Rules**:

- **Bash commands**: MUST use absolute paths OR relative paths from repo root
  - ✅ CORRECT: `uv run pytest C:/Users/kemos/Repos/gauntlet-agents/tests/unit/`
  - ✅ CORRECT: `uv run pytest tests/unit/` (relative from root)
  - ❌ WRONG: `cd tests && uv run pytest unit/` (BLOCKED - cd doesn't work)
  - ❌ WRONG: `cd "path" && command` (BLOCKED - command chaining with cd)
- **Tool calls** (Read/Write/Edit/Grep/Glob): Use relative paths from root
  - ✅ CORRECT: `Read("docs/guides/file.md")`
  - ✅ ALSO CORRECT: `Read("C:/Users/kemos/Repos/gauntlet-agents/docs/guides/file.md")`
- **Use forward slashes**: `docs/guides/file.md` not `docs\guides\file.md`

### AGENT_NAME Environment Variable (MANDATORY)

**🔴 CRITICAL**: ALL Bash commands MUST prefix with `AGENT_NAME=<agent-name>`

**Format**:
```bash
# ✅ CORRECT - Agent name from YAML frontmatter
AGENT_NAME=development uv run pytest tests/unit/

# ❌ WRONG - Missing prefix
uv run pytest tests/unit/
```

**Agent Name Source**: Use exact `name:` value from your YAML frontmatter (line 2 of your .md file)

**Why Required**:
- Command traceability in multi-agent workflows
- Audit logging and debugging
- Security hook enforcement

**Enforcement**: Security hooks will validate AGENT_NAME presence (implementation pending)

### Status Types

- **SUCCESS**: Task completed successfully
- **NEEDS_CLARIFICATION**: Missing information, provide concrete gaps + next steps
- **ERROR**: Task failed, include reason and recovery options

### Timestamp Authority (CRITICAL)

- **Orchestrator provides execution_timestamp** in ISO 8601 UTC format
- **Sub-agents MUST use orchestrator timestamp only** - never generate locally
- **All timestamps must be consistent** across orchestration session

### Output Requirements

Always include: `status`, `agent`, `task_id`, `summary`, `execution_timestamp`

### Scope Enforcement

- Work within allowed directories only
- No secrets in outputs
- Sanitize all paths and inputs

## File Operations Protocol (MANDATORY)

**Desktop Commander is the ONLY tool for file modifications.**

### Desktop Commander MCP Tools Required

**ALL file operations MUST use Desktop Commander MCP tools**, regardless of directory location:

| Operation | Required Tool |
|-----------|---------------|
| Read | `mcp__desktop-commander__read_file` or Claude Code `Read` |
| Write | `mcp__desktop-commander__write_file` |
| Edit | `mcp__desktop-commander__edit_block` |
| List | `mcp__desktop-commander__list_directory` |
| Search | `mcp__desktop-commander__start_search` |
| Move | `mcp__desktop-commander__move_file` |

**Why**: Platform consistency, Windows file locking handling, atomic operations.

### Pre-Flight Verification

Before modifying or removing content:
1. **Edit/Update**: Read file first (required by tool anyway)
2. **Cleanup operations**: `Glob()` to verify targets exist - skip if empty (not an error)
3. **Bulk operations**: Verify ALL targets before ANY modification

---

## BANNED FILE EDITING COMMANDS

**NEVER use these commands for file editing - they will fail or cause issues:**

```bash
# BANNED - Use Desktop Commander instead
sed -i 's/old/new/g' file.txt      # Portability issues, escaping nightmares
awk '{gsub(...)}' file.txt         # Complex, error-prone
echo "content" > file.txt          # Overwrites without validation
cat << EOF > file.txt              # Escaping issues in Claude Code
perl -pi -e 's/old/new/' file.txt  # Not available on all systems
```

**WHY BANNED**: These commands have shell escaping issues, no validation, no atomic writes, and cause silent failures. Desktop Commander is designed for Claude Code's environment.

## BANNED DELETION COMMANDS (Security Blocked)

**These commands are BLOCKED by security hooks - they will fail with "Permission denied":**

```bash
# BLOCKED - Will fail with permission error
rm file.txt                  # File deletion blocked
rm -rf directory/            # Recursive deletion blocked  
rm -r directory/             # Recursive deletion blocked
del file.txt                 # Windows deletion blocked
rmdir directory/             # Directory deletion blocked
```

**WHY BLOCKED**: Destructive operations require explicit user consent. Prevents accidental data loss.

**ALTERNATIVES for Deletion:**

| Need | Solution |
|------|----------|
| Delete file/directory | Request user to delete manually |
| Move before delete | `mcp__desktop-commander__move_file(source, destination)` |
| Rename/reorganize | `mcp__desktop-commander__move_file(source, destination)` |

**Example - When You Need to Delete:**
```
# In your response, tell the user:
"The directory `.claude/agents/creative/` is no longer needed.
Please delete it manually: `rm -rf .claude/agents/creative/`
Or I can move it to temp/ for later cleanup."
```

**Move as Alternative** (reversible):
```python
mcp__desktop-commander__move_file(
    source="C:/path/to/unwanted/dir",
    destination="C:/path/to/temp/backup-dir"
)
```

---

## Desktop Commander Operations

### For Editing Existing Files

**Step 1**: Read file first (MANDATORY)
```python
mcp__desktop-commander__read_file(path="C:/Users/kemos/Repos/gauntlet-agents/path/to/file.py")
# OR use Claude Code Read tool
Read("C:/Users/kemos/Repos/gauntlet-agents/path/to/file.py")
```

**Step 2**: Edit with exact string match
```python
mcp__desktop-commander__edit_block(
    file_path="C:/Users/kemos/Repos/gauntlet-agents/path/to/file.py",
    old_string="exact text from file",
    new_string="replacement text"
)
```

**Key Requirements**:
- `old_string` must match file content EXACTLY (whitespace, indentation, line endings)
- Include minimal context needed to uniquely identify the edit location
- Default replaces ONE occurrence; use `expected_replacements` for multiple

### For Creating New Files

**Small files (<30 lines)**: Single write operation
```python
mcp__desktop-commander__write_file(
    path="C:/Users/kemos/Repos/gauntlet-agents/path/to/new_file.py",
    content="complete file content here",
    mode="rewrite"
)
```

**Large files (>30 lines)**: Chunk into multiple writes
```python
# First chunk (lines 1-30)
mcp__desktop-commander__write_file(
    path="C:/Users/kemos/Repos/gauntlet-agents/path/to/new_file.py",
    content="first 30 lines of content",
    mode="rewrite"
)

# Subsequent chunks (append)
mcp__desktop-commander__write_file(
    path="C:/Users/kemos/Repos/gauntlet-agents/path/to/new_file.py",
    content="next 30 lines of content",
    mode="append"
)
```

**Performance Tip**: Files over 50 lines trigger performance warnings but still write successfully.

---

## Error Recovery

| Error | Cause | Solution |
|-------|-------|----------|
| "String not found" | `old_string` doesn't match | Re-read file, copy exact text (no line prefixes like "42→") |
| "Permission denied" | Windows file locking | Wait 5 seconds, retry once |
| "Multiple matches" | `old_string` not unique | Add more context to `old_string` OR use `expected_replacements` |
| Desktop Commander fails | Tool unavailable | ESCALATE to orchestrator (do NOT use Edit/Write tools) |

**Escalation Protocol**: If Desktop Commander fails after retry, report to orchestrator with:
- Error message
- File path
- Attempted operation
- Recommended manual intervention

---

## Quick Reference

| Operation | Tool | Example |
|-----------|------|---------|
| Read file | Either tool | `Read("path")` or `mcp__desktop-commander__read_file(path="...")` |
| Edit existing | Desktop Commander | `mcp__desktop-commander__edit_block(file_path, old_string, new_string)` |
| Create new | Desktop Commander | `mcp__desktop-commander__write_file(path, content, mode="rewrite")` |
| Append content | Desktop Commander | `mcp__desktop-commander__write_file(path, content, mode="append")` |
| Move/rename | Desktop Commander | `mcp__desktop-commander__move_file(source, destination)` |

**Complete Guide**: `.claude/docs/01-guides/file-ops/file-operation-protocol.md`

---

**Extended Documentation**: See `.claude/docs/agent-standards-extended.md` for detailed procedures, examples, and advanced patterns.
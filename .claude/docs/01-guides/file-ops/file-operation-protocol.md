# File Operation Protocol

**Purpose**: Complete guide for file operations using available tools

**Last Updated**: 2025-12-26

**Applies To**: All agents with Write, Edit, or file modification capabilities

---

## Tool Selection

Use available file operation tools. Built-in tools (`Read`, `Edit`, `Write`) or MCP equivalents work interchangeably based on your environment configuration.

| Operation | Built-in Tool | MCP Equivalent |
|-----------|---------------|----------------|
| **Read files** | `Read` | `mcp__desktop-commander__read_file` |
| **Write files** | `Write` | `mcp__desktop-commander__write_file` |
| **Edit files** | `Edit` | `mcp__desktop-commander__edit_block` |
| **Find files** | `Glob` | `mcp__desktop-commander__list_directory` |
| **Search content** | `Grep` | `mcp__desktop-commander__start_search` |
| **Move/rename** | (use Bash mv) | `mcp__desktop-commander__move_file` |

**Platform Recommendations**:
- **Windows**: MCP tools preferred (better file locking handling in .claude/)
- **Mac/Linux**: Built-in tools work well

### Avoid Shell-Based File Operations

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `Bash(cat ...)` | Platform inconsistency | `Read` or MCP read_file |
| `Bash(echo > ...)` | No atomic write guarantee | `Write` or MCP write_file |
| `Bash(sed ...)` | Complex escaping, platform issues | `Edit` or MCP edit_block |
| `Bash(ls ...)` | Output parsing fragile | `Glob` or MCP list_directory |
| `Bash(find ...)` | Platform-specific behavior | `Grep` or MCP start_search |

**Why Dedicated Tools Over Shell Commands**:
1. **Atomic operations**: Write and edit operations are atomic
2. **Better error messages**: Structured errors vs shell output parsing
3. **No escaping issues**: Handles spaces, special characters correctly
4. **Platform consistency**: Same behavior across environments

---

## Pre-Flight Verification (MANDATORY)

Before ANY file/directory operation that modifies or removes content:

| Operation Type | Verification Required | Skip Condition |
|----------------|----------------------|----------------|
| **Edit/Update** | `Read(file_path)` or `mcp__desktop-commander__read_file` | Never skip |
| **Delete/Cleanup** | `Glob(pattern)` to verify targets exist | If empty result, skip operation (not an error) |
| **Move/Rename** | Verify source exists AND destination doesn't | Fail if source missing or destination exists |
| **Bulk Operations** | Verify ALL targets before ANY modification | Abort entire batch if any target missing |

**Why**: Prevents "file not found" errors and wasted API calls on non-existent targets.

**Pattern**:
```python
# Before cleanup
targets = Glob("path/to/cleanup/*")
if targets.empty:
    log("Nothing to clean up - skipping")
    return
# Proceed with cleanup only if targets exist
```

---

## Quick Start

### Key Principles

1. **Read before edit**: Always verify file content before modifying
2. **Chunk all modifications**: Keep edits and writes to ≤30 lines per operation
3. **Use dedicated tools**: Avoid shell commands for file operations

> **Chunking Rule**: All file modifications should target ≤30 lines per operation for optimal performance.

---

### Reading Files

```python
# Built-in Read tool
Read(file_path="path/to/file.py")

# With offset/limit for large files
Read(file_path="path/to/file.py", offset=100, limit=50)

# MCP equivalent (when configured)
mcp__desktop-commander__read_file(path="path/to/file.py")
```

---

### Editing Files (Surgical Replacements)

```python
# 1. Read file first (MANDATORY)
Read(file_path="path/to/file.py")

# 2. Built-in Edit tool
Edit(
    file_path="path/to/file.py",
    old_string="exact text to find",
    new_string="replacement text"
)

# MCP equivalent
mcp__desktop-commander__edit_block(
    file_path="path/to/file.py",
    old_string="exact text to find",
    new_string="replacement text"
)
```

**Chunking for Edits**: Keep replacement blocks to ≤30 lines. For larger changes, split into multiple sequential edits.

**Key Points**:
- Always read file before editing (verify actual content)
- `old_string` must match exactly (whitespace, indentation)
- Near-matches show character-level diff to help identify differences

---

### Writing New Files (with Chunking)

```python
# Built-in Write tool - small files (<30 lines)
Write(
    file_path="path/to/file.py",
    content="file content here"
)

# MCP equivalent with chunking for large files
# First chunk
mcp__desktop-commander__write_file(
    path="path/to/file.py",
    content="first 25-30 lines",
    mode="rewrite"
)
# Subsequent chunks
mcp__desktop-commander__write_file(
    path="path/to/file.py",
    content="next 25-30 lines",
    mode="append"
)
```

**Chunking Rules** (applies to ALL write operations):
- Target ≤30 lines per write operation for optimal performance
- For MCP: Use `mode="rewrite"` for first chunk, `mode="append"` for subsequent
- For built-in Write: Make multiple sequential Write calls for large files

---

## Banned Commands

**NEVER use these for file editing - they cause failures in Claude Code:**

| Command | Why Banned | Use Instead |
|---------|------------|-------------|
| `sed -i` | Shell escaping issues, no validation | `Edit` tool |
| `awk '{gsub(...)}'` | Complex escaping, no atomic writes | `Edit` tool |
| `echo > file` | Overwrites without validation | `Write` tool |
| `cat << EOF` | Heredoc escaping fails in Claude Code Bash | `Write` tool |
| `perl -pi -e` | Not available on all systems | `Edit` tool |

---

## Deletion Operations (BLOCKED - NEVER ATTEMPT)

### NEVER Execute These Commands

| Command | Why Blocked | What To Do Instead |
|---------|-------------|-------------------|
| `rm`, `rm -rf`, `rm -r` | Destructive, no recovery | Request user to delete manually |
| `rmdir` | In DANGEROUS_COMMANDS set | Request user to delete manually |
| `del` (Windows) | Destructive, no recovery | Request user to delete manually |
| `Remove-Item` (PowerShell) | Destructive, no recovery | Request user to delete manually |

### Correct Pattern for Cleanup Tasks

**NEVER attempt deletion. Instead, generate user instructions:**

```markdown
## Manual Cleanup Required

The following items can be safely deleted:
- `path/to/empty/directory/`
- `path/to/obsolete/file.txt`

To clean up, run:
```bash
rm -rf path/to/empty/directory/
rm path/to/obsolete/file.txt
```
```

**Why**: Security hooks block deletion commands. Attempting them wastes tokens and creates error noise. Delegating to user is faster and safer.

### Alternative - Move to temp location (reversible)

If immediate action is needed and user approval isn't practical:

```python
mcp__desktop-commander__move_file(
    source="path/to/unwanted",
    destination="temp/backup-unwanted"
)
```

---

## Error Recovery

### Error: "String not found in file"

**Cause**: Whitespace mismatch, content changed, line number prefix copied

**Solution**:
1. Re-read the file to get current content
2. Copy exact string from output (not from memory)
3. Check for hidden whitespace (tabs vs spaces)
4. Remove line number prefixes (e.g., "42→" from Read output)


### Error: "Permission denied" (Windows)

**Cause**: Windows file locking (antivirus, Git, indexing)

**Solution**:
- MCP tools handle retries automatically
- If still fails: Close VS Code, wait 5 seconds, retry
- Workaround: Copy file out of locked directory, edit, copy back

---

## Platform Notes

### Windows

MCP tools recommended on Windows for better file locking handling:
- Paths auto-normalized (forward or backslash both work)
- No shell escaping issues (MCP protocol)
- Handles Windows file locking gracefully

### Mac / Linux

Built-in tools (`Read`, `Edit`, `Write`) work well:
- No file locking issues
- Native performance
- MCP tools also work if configured


---

## Line Ending Handling

**Automatic Normalization**:
- Input content normalized to LF (`\n`)
- Original file line endings preserved (CRLF or LF)
- Prevents matching failures due to line ending differences

---

## Critical Rules Summary

| Rule | Description |
|------|-------------|
| **Read before edit** | ALWAYS read file before editing to verify actual content |
| **Use available tools** | Built-in (`Edit`, `Write`) or MCP equivalents based on environment |
| **Chunk ALL modifications** | ≤30 lines per edit/write operation |
| **No shell editing** | NEVER use sed, awk, echo, cat heredocs |
| **No deletions** | Request user action for rm/rmdir operations |
| **Fix-forward** | No backup files - Git tracks changes |

---

## References

- **Built-in tools**: `Read`, `Edit`, `Write`, `Glob`, `Grep`
- **MCP tools**: `desktop-commander` equivalents (when configured)
- **CLAUDE.md**: Project-wide command policy

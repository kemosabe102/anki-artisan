# Hook Event Catalog

Complete reference of Claude Code hook events and their characteristics.

---

## Event Types

### SessionStart

**Trigger**: When Claude Code session begins

**Characteristics**:
- Runs once per session
- Should complete within timeout (12s recommended)
- Output appears in session context
- Always exit 0 (never block session start)

**Use Cases**:
- Load critical documentation into context
- Run cleanup/maintenance tasks
- Initialize session state
- Display project information

**Input Format**:
```json
{
  "event": "SessionStart",
  "session_id": "unique-session-id",
  "timestamp": "2025-01-01T00:00:00Z"
}
```

**Best Practices**:
- Keep output minimal (HTML comments for Claude-only context)
- Implement graceful fallbacks
- Log errors but never block
- Target <3s execution time

---

### PreToolUse

**Trigger**: Before any tool is executed

**Characteristics**:
- Can BLOCK tool execution (exit code 2)
- Receives tool name and input
- Must complete within timeout (5s recommended)
- Security-critical hooks use this event

**Use Cases**:
- Command validation (Bash, shell)
- Path traversal prevention (Read, Write, Edit)
- URL validation (WebFetch, WebSearch)
- Input sanitization

**Input Format**:
```json
{
  "event": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git status"
  },
  "metadata": {
    "session_id": "abc123"
  }
}
```

**Exit Codes**:
| Code | Effect | When to Use |
|------|--------|-------------|
| 0 | Allow | Validation passed |
| 2 | Block | Validation failed, show stderr |
| Other | Allow | Treat errors as pass (fail-open) |

**Matcher Patterns**:
```
"Bash"                        # Single tool
"Read|Write|Edit|MultiEdit"   # Multiple tools (OR)
"WebFetch|WebSearch"          # Tool family
"mcp__*"                      # MCP tools wildcard
"*"                           # All tools
```

---

### PostToolUse

**Trigger**: After tool execution completes

**Characteristics**:
- Cannot block (tool already executed)
- Receives tool output
- Can run in background (`background: true`)
- Used for logging, formatting, validation

**Use Cases**:
- Code formatting (ruff, black)
- Documentation validation
- Usage logging/analytics
- Secret detection in output
- Reference validation

**Input Format**:
```json
{
  "event": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.py",
    "content": "..."
  },
  "tool_output": {
    "success": true,
    "bytes_written": 1234
  },
  "metadata": {
    "session_id": "abc123"
  }
}
```

**File Pattern Matchers**:
```
"Write|Edit(*.py)"            # Python files only
"Write|Edit(docs/**/*.md)"    # Docs markdown files
"Write|Edit|MultiEdit(*.py)"  # Multiple tools + pattern
```

**Background vs Foreground**:
| Mode | `background` | Blocking | Use For |
|------|--------------|----------|---------|
| Foreground | `false` | Waits | Formatting, validation |
| Background | `true` | Async | Logging, metrics |

---

## Available Tools Reference

### File Operations
| Tool | Description | Common Hooks |
|------|-------------|--------------|
| `Read` | Read file contents | Path validation |
| `Write` | Write file contents | Path validation, formatting |
| `Edit` | Edit file sections | Path validation, formatting |
| `MultiEdit` | Multiple edits | Path validation, formatting |

### Shell Operations
| Tool | Description | Common Hooks |
|------|-------------|--------------|
| `Bash` | Execute shell commands | Command validation, security |

### Web Operations
| Tool | Description | Common Hooks |
|------|-------------|--------------|
| `WebFetch` | Fetch URL content | SSRF prevention |
| `WebSearch` | Search the web | URL validation |

### MCP Tools
| Pattern | Description | Common Hooks |
|---------|-------------|--------------|
| `mcp__context7__*` | Context7 library docs | Usage logging |
| `mcp__perplexity__*` | Perplexity search | Usage logging |
| `mcp__desktop-commander__*` | Desktop Commander | Path validation |

---

## Hook Configuration Fields

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Always `"command"` |
| `command` | string | Command to execute |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `matcher` | string | (required for Pre/PostToolUse) | Tool pattern to match |
| `timeout` | number | 30000 | Timeout in milliseconds |
| `background` | boolean | false | Run asynchronously |
| `description` | string | - | Human-readable description |
| `successMessage` | string | - | Message on exit 0 |
| `errorMessage` | string | - | Message on non-zero exit |

### Environment Variables

| Variable | Description |
|----------|-------------|
| `${CLAUDE_PLUGIN_ROOT}` | Root of .claude directory |
| `$CLAUDE_FILE_PATHS` | Space-separated file paths |
| `$CLAUDE_CONTEXT` | JSON context from tool |
| `$CLAUDE_SESSION_ID` | Current session ID |

---

## Existing Hooks Reference

### Security Hooks (PreToolUse)

| Hook | Matcher | Purpose |
|------|---------|---------|
| `security-validate-command.py` | `Bash` | Command injection prevention |
| `security-validate-path.py` | `Read\|Write\|Edit\|MultiEdit` | Path traversal prevention |
| `security-validate-url.py` | `WebFetch\|WebSearch` | SSRF prevention |

### Validation Hooks (PostToolUse)

| Hook | Matcher | Purpose |
|------|---------|---------|
| `validate-references.py` | `Write\|Edit(CLAUDE.md)` | Documentation link validation |
| `ruff check --fix` | `Write\|Edit\|MultiEdit(*.py)` | Python formatting |
| `security-sanitize-content.py` | `*` | Secret detection in output |

### Startup Hooks (SessionStart)

| Hook | Purpose |
|------|---------|
| `startup-eval.py` | Load documentation context, cleanup |

### Maintenance Hooks

| Hook | Purpose |
|------|---------|
| `cleanup-temp-scripts.py` | Remove temporary agent scripts |
| `cleanup-artifacts.py` | Clean code review artifacts (deprecated) |

---

## Security Considerations

### Input Validation
- Always validate tool_input before processing
- Sanitize paths to prevent traversal
- Validate URLs against SSRF patterns

### Never Bypass (Critical Checks)
These checks should NEVER be bypassable, even for trusted agents:
- Destructive git operations (reset --hard, checkout file)
- Dangerous commands (rm -rf, sudo, eval)
- Command substitution ($(), backticks)
- Protected files (.env, credentials)
- Protected directories (/etc, /sys, .ssh)

### Logging Security
- Never log full commands with secrets
- Use sanitization functions for log output
- Include redaction markers in logs

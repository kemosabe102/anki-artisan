---
name: hook-automation
description: >
  Hook creation and automation for Claude Code. Use when creating event handlers,
  automating workflows, or managing hook lifecycle.
  Trigger keywords: hook, automation, event handler, create hook, pre-commit.
---

# Hook Automation Skill

*Create, configure, and manage Claude Code hooks for workflow automation*

## Quick Start

| User Says | Action |
|-----------|--------|
| "create a hook for X" | Design hook → Create files → Register in hooks.json |
| "add validation hook" | Create PreToolUse validator |
| "automate on startup" | Create SessionStart hook |
| "hook for file changes" | Create PostToolUse hook |

---

## When to Use This Skill

Use this skill when asked to:
- Create new Claude Code hooks (event handlers)
- Add workflow automation (startup, pre/post tool use)
- Implement security validation hooks
- Add logging or monitoring hooks
- Configure hook lifecycle and error handling

**Do NOT use for**:
- Agent definitions (use `claude-code-ecosystem`)
- Slash commands (use `workflow` agent with `create_command` mode)
- Application code changes

---

## Reference Documentation

**Templates and Examples**:
- **Hook Template** → [references/hook-template.md](references/hook-template.md)
- **Event Catalog** → [references/event-catalog.md](references/event-catalog.md)

**Project Standards**:
- `.claude/hooks/README.md` - Hook system documentation
- `.claude/hooks/hooks.json` - Hook registration file

---

## Hook System Architecture

### Directory Structure

```
.claude/hooks/
├── hooks.json              # Hook registration (event → handler mapping)
├── utils.py                # Project root detection, timestamp utilities
├── logging_utils.py        # Shared OTLP logging configuration
├── security/               # Security validation modules
│   ├── validate_command.py # Bash command validation (1600+ lines)
│   ├── validate_path.py    # Path traversal prevention
│   ├── validate_url.py     # SSRF prevention
│   └── sanitize_content.py # Secret detection in outputs
├── security-validate-*.py  # Entry point hooks (thin wrappers)
├── startup-eval.py         # Session startup hook
└── cleanup-*.py            # Maintenance hooks
```

### Two-Tier Architecture

**Tier 1: Entry Points** (hook files registered in hooks.json)
- Minimal imports, fast startup
- Early exit checks before heavy imports
- Lazy loading for performance (saves 40-50ms)
- Thin wrappers that delegate to Tier 2

**Tier 2: Core Modules** (security/ directory)
- All validation logic
- Comprehensive pattern detection
- Configurable bypass systems
- Detailed logging and audit trails

---

## Hook Event Types

| Event | Trigger | Use Case |
|-------|---------|----------|
| `SessionStart` | Claude Code session begins | Context loading, cleanup |
| `PreToolUse` | Before tool execution | Validation, blocking |
| `PostToolUse` | After tool execution | Logging, formatting |

### Matcher Patterns

```json
{
  "matcher": "Bash",                           // Single tool
  "matcher": "Read|Write|Edit|MultiEdit",      // Multiple tools
  "matcher": "WebFetch|WebSearch",             // Tool family
  "matcher": "Write|Edit(*.py)",               // Tool + file pattern
  "matcher": "mcp__context7__*",               // MCP tool prefix
  "matcher": "*"                               // All tools
}
```

---

## Hook Creation Process

### Step 1: Define Hook Purpose

- [ ] Identify trigger event (SessionStart, PreToolUse, PostToolUse)
- [ ] Define target tools (if PreToolUse/PostToolUse)
- [ ] Determine blocking vs. non-blocking behavior
- [ ] Plan error handling strategy

### Step 2: Create Hook File

**Location**: `.claude/hooks/<hook-name>.py`

**Template**: See [references/hook-template.md](references/hook-template.md)

### Step 3: Register in hooks.json

Add entry to `.claude/hooks/hooks.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "ToolName",
        "type": "command",
        "command": "uv run python ${CLAUDE_PLUGIN_ROOT}/hooks/<hook-name>.py",
        "timeout": 5000,
        "description": "Brief description of what this hook validates"
      }
    ]
  }
}
```

### Step 4: Test Hook

1. **Unit test**: Run hook directly with sample input
2. **Integration test**: Trigger in Claude Code session
3. **Error handling**: Verify graceful degradation

---

## Hook Input/Output Contract

### Input (stdin JSON)

```json
{
  "event": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "git status"
  },
  "metadata": {
    "session_id": "abc123",
    "timestamp": "2025-01-01T00:00:00Z"
  }
}
```

### Output (Exit Codes)

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| 0 | Allow | Tool execution proceeds |
| 2 | Block | Tool execution blocked, stderr shown to user |
| Other | Error | Treated as allow (fail-open) |

### Blocking Response

```python
print("🚫 BLOCKED: Reason for blocking", file=sys.stderr)
sys.exit(2)  # Exit code 2 blocks tool call
```

---

## Performance Optimization Patterns

### Lazy Imports

```python
def main():
    # EARLY EXIT: Check preconditions before heavy imports
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    
    if tool_name != "Bash":
        sys.exit(0)  # Exit before importing heavy modules
    
    # LAZY IMPORT: Now load modules (only when needed)
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent / "security"))
    from validate_command import validate_command_safety
```

### Skip Logging on Success

```python
if not result["safe"]:
    # Only setup logging when BLOCKING (saves 20-50ms)
    from logging_utils import setup_hook_logging
    logger = setup_hook_logging("hook-name")
    logger.warning(f"Blocked: {result['reason']}")
    sys.exit(2)
else:
    # Fast path: no logging overhead
    sys.exit(0)
```

### Environment Detection

```python
import os

# Skip validation in sandboxed web environment
if os.environ.get("CLAUDE_CODE_REMOTE") == "true":
    sys.exit(0)  # Web environment is sandboxed
```

---

## Agent Bypass Configuration

Some agents need elevated permissions. Configure in hook entry point:

```python
AGENT_BYPASS_CONFIG = {
    "agent-name": {
        "bypass_all": False,
        "bypass_checks": ["command_chain_validation"],
        "reason": "Agent requires chained commands for workflow"
    }
}

# Critical checks that can NEVER be bypassed
NEVER_BYPASS_CHECKS = [
    "destructive_git",      # git reset --hard, checkout <file>
    "dangerous_commands",   # rm -rf, sudo, eval
    "command_substitution", # $(), backticks
    "protected_files",      # .env, credentials
]
```

---

## Error Handling Philosophy

### Core Principles

1. **Never Block Development**: Hooks must never prevent Claude Code from functioning
2. **Graceful Degradation**: Provide fallback when components fail
3. **Silent Unless Important**: Only output messages when relevant
4. **Comprehensive Logging**: Log for debugging without cluttering output
5. **Fast Recovery**: Quick startup, minimal performance impact

### Error Handling Pattern

```python
def main():
    try:
        input_data = json.load(sys.stdin)
        # ... validation logic ...
    except json.JSONDecodeError:
        sys.exit(0)  # Don't block on JSON errors
    except Exception:
        sys.exit(0)  # Don't block on internal errors
```

### Fallback Context (SessionStart)

```python
try:
    context = generate_startup_context()
    print(context)
except Exception as e:
    logger.error(f"Startup failed: {e}")
    fallback = """<!--STARTUP_ERROR: Check logs-->"""
    print(fallback)
finally:
    sys.exit(0)  # Always exit 0 for startup hooks
```

---

## Logging Configuration

### Setup with OTLP

```python
from logging_utils import setup_hook_logging, shutdown_hook_logging

logger = setup_hook_logging(
    hook_name="my-hook",
    session_id=os.getenv("CLAUDE_SESSION_ID"),
    agent_name="optional-agent-name"
)

try:
    # Hook logic
    logger.info("Operation completed", extra={"key": "value"})
finally:
    shutdown_hook_logging()
```

### Structured Logging

```python
logger.warning(
    "Security event",
    extra={
        "component": "security_validate_command",
        "security_event": {
            "command": sanitized_command,
            "reason": result["reason"],
            "detected_issues": result.get("detected_issues", [])
        }
    }
)
```

---

## Utility Modules

### utils.py - Project Root Detection

```python
from utils import get_project_root, get_timestamp

project_root = get_project_root()  # Returns pathlib.Path
timestamp = get_timestamp()        # ISO-8601 with milliseconds
```

**Detection Strategy** (layered fallback):
1. `git rev-parse --show-toplevel` (universal Git standard)
2. pathlib `.git` detection (walk up from script)
3. Script location fallback (last resort)

### logging_utils.py - OTLP Logging

```python
from logging_utils import setup_hook_logging, shutdown_hook_logging

# Creates logger with OTLP export to observability system
logger = setup_hook_logging("hook-name", session_id="abc123")

# Clean shutdown (flushes pending records)
shutdown_hook_logging()
```

**Environment Variables**:
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP endpoint (e.g., `http://localhost:30317`)
- `HOOK_LOG_LEVEL`: Logging level (default: INFO)

---

## Hook Registration Reference

### hooks.json Structure

```json
{
  "description": "Hook system description",
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "uv run python ${CLAUDE_PLUGIN_ROOT}/hooks/startup-eval.py",
        "timeout": 12000,
        "background": false,
        "description": "Loading project context"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "type": "command",
        "command": "uv run python ${CLAUDE_PLUGIN_ROOT}/hooks/security-validate-command.py",
        "timeout": 5000,
        "description": "Validating Bash commands"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit(*.py)",
        "type": "command",
        "command": "uv run ruff check --fix $CLAUDE_FILE_PATHS",
        "timeout": 30,
        "background": false,
        "successMessage": "✅ Code formatted",
        "errorMessage": "⚠️ Formatting issues detected"
      }
    ]
  }
}
```

---

## Best Practices

### Design Principles

1. **Fail-open by default**: Internal errors should not block operations
2. **Performance first**: Target <100ms for validation hooks
3. **Minimal dependencies**: Reduce import overhead
4. **Structured output**: Use JSON for machine-readable results
5. **Audit trail**: Log security-relevant events

### Security Hook Design

- Validate early, exit fast
- Never log secrets (use sanitization)
- Implement granular bypass with safety nets
- Document all bypass configurations

### Maintenance Hook Design

- Run in background when possible
- Implement dry-run mode
- Track cleanup statistics
- Graceful handling of missing files

---

## Anti-Patterns (NEVER DO)

| Anti-Pattern | Why It's Wrong | Do Instead |
|--------------|----------------|------------|
| Bare `except:` that blocks | Prevents development | `sys.exit(0)` on errors |
| Logging on success path | Performance overhead | Log only on block/error |
| Heavy imports at top | Slow startup | Lazy import after checks |
| Hardcoded paths | Platform-specific | Use `get_project_root()` |
| Blocking on JSON errors | Input may be malformed | Graceful fallback |
| Secrets in logs | Security risk | Use sanitization |

---

## Thinking Frameworks

When facing complex hook challenges, these frameworks guide systematic problem-solving.

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Hook Automation**:

| Framework | When to Use |
|-----------|-------------|
| [ReACT](../../docs/00-core/frameworks/analysis.md) | Debugging hook failures, tracing execution |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Identifying failure modes before deployment |
| [5 Whys](../../docs/00-core/frameworks/analysis.md) | Root cause analysis for recurring issues |

> **Selection Tip**: debugging→ReACT, risk assessment→Pre-Mortem, root cause→5 Whys

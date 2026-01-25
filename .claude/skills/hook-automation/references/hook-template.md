# Hook Template

Standard template for creating Claude Code hooks.

---

## PreToolUse Validation Hook Template

```python
#!/usr/bin/env python3
"""
Security/Validation Hook: [Hook Name]

[Brief description of what this hook validates]

Hook Type: PreToolUse
Triggers: [Tool1, Tool2, ...]
Reference: [Link to relevant documentation]

PERFORMANCE OPTIMIZATIONS:
- Lazy imports: Heavy modules loaded only after early exit checks
- Skip logging on pass: Logging setup only on BLOCK
"""

import json
import sys


def main():
    """Main hook entry point for validation"""
    try:
        # Read hook input from stdin (minimal imports needed)
        input_data = json.load(sys.stdin)

        # Extract hook event details
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # EARLY EXIT: Only validate target tools (before heavy imports)
        if tool_name not in ["TargetTool1", "TargetTool2"]:
            sys.exit(0)

        # Extract relevant data from tool input
        data_to_validate = tool_input.get("key", "")
        if not data_to_validate:
            sys.exit(0)

        # LAZY IMPORT: Now load heavy modules (only when actually needed)
        from pathlib import Path

        HOOKS_DIR = Path(__file__).parent
        sys.path.insert(0, str(HOOKS_DIR / "security"))
        from validate_module import validate_function

        # Perform validation
        result = validate_function(data_to_validate)

        if not result["safe"]:
            # SKIP LOGGING ON PASS: Only setup logging when BLOCKING
            try:
                sys.path.insert(0, str(HOOKS_DIR))
                from logging_utils import setup_hook_logging

                logger = setup_hook_logging("hook-name")
                logger.warning(f"Blocked: {result['reason']}")
            except ImportError:
                pass  # Logging failure shouldn't block security action

            # Block unsafe operation
            print(f"🚫 BLOCKED: {result['reason']}", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call
        else:
            # Allow safe operation (NO LOGGING - fast path)
            sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)  # Don't block on JSON errors
    except Exception:
        sys.exit(0)  # Don't block on internal errors


if __name__ == "__main__":
    main()
```

---

## SessionStart Hook Template

```python
#!/usr/bin/env python3
"""
Startup Hook: [Hook Name]

[Brief description of what this hook does at session start]

Hook Type: SessionStart
Output: Context for Claude (typically HTML comments)
Performance: Target <3 seconds
"""

import json
import sys
from pathlib import Path

from utils import get_project_root
from logging_utils import setup_hook_logging, shutdown_hook_logging


def generate_startup_context() -> str:
    """Generate context for Claude session."""
    # Load configuration, documentation, or other context
    context_data = {
        "loaded_at": "timestamp",
        "key_context": "value"
    }
    
    # Return as HTML comment (invisible to user, accessible to Claude)
    return f"<!--\nSTARTUP_CONTEXT\n{json.dumps(context_data, indent=2)}\n-->"


def main():
    """Main function following established hook patterns."""
    logger = setup_hook_logging("hook-name")

    try:
        # Read hook input (required for SessionStart hooks)
        try:
            input_data = json.load(sys.stdin)
            event_type = input_data.get("event", "unknown")
            logger.info(f"SessionStart triggered: {event_type}")
        except json.JSONDecodeError:
            logger.info("No JSON input for SessionStart")

        # Generate and output startup context
        context = generate_startup_context()
        print(context)

        logger.info("Startup completed successfully")

    except Exception as e:
        # Graceful fallback - never block development workflow
        logger.error(f"Startup failed: {e}")
        fallback = """<!--STARTUP_ERROR: Check logs-->"""
        print(fallback)

    finally:
        shutdown_hook_logging()

    # Always exit 0 - follow established hook pattern
    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## PostToolUse Hook Template

```python
#!/usr/bin/env python3
"""
Post-Tool Hook: [Hook Name]

[Brief description of what this hook does after tool execution]

Hook Type: PostToolUse
Triggers: [Tool patterns]
Output: Optional success/error message
"""

import json
import sys


def main():
    """Main hook entry point for post-tool processing"""
    try:
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_output = input_data.get("tool_output", {})

        # Process based on tool output
        # Example: Log usage, format output, validate results
        
        if tool_output.get("success"):
            # Optional: Print success message
            # print("✅ Operation completed")
            pass
        
        sys.exit(0)

    except Exception:
        sys.exit(0)  # Never block on post-processing errors


if __name__ == "__main__":
    main()
```

---

## Background Hook Template

```python
#!/usr/bin/env python3
"""
Background Hook: [Hook Name]

[Brief description - runs asynchronously, doesn't block]

Hook Type: PostToolUse (background: true)
"""

import json
import sys


def main():
    """Background hook - fire and forget"""
    try:
        input_data = json.load(sys.stdin)
        
        # Perform background task (logging, metrics, etc.)
        # This runs async and doesn't affect tool execution
        
    except Exception:
        pass  # Silent failure for background hooks


if __name__ == "__main__":
    main()
```

---

## hooks.json Registration Examples

### Validation Hook (PreToolUse)

```json
{
  "matcher": "Bash",
  "type": "command",
  "command": "uv run python ${CLAUDE_PLUGIN_ROOT}/hooks/my-validator.py",
  "timeout": 5000,
  "description": "Validates Bash commands for safety"
}
```

### Formatter Hook (PostToolUse)

```json
{
  "matcher": "Write|Edit|MultiEdit(*.py)",
  "type": "command",
  "command": "uv run ruff check --fix $CLAUDE_FILE_PATHS",
  "timeout": 30000,
  "background": false,
  "successMessage": "✅ Code formatted successfully",
  "errorMessage": "⚠️ Formatting issues detected"
}
```

### Background Logger (PostToolUse)

```json
{
  "matcher": "mcp__context7__*",
  "type": "command",
  "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/log-usage.py $CLAUDE_CONTEXT",
  "timeout": 5000,
  "background": true,
  "description": "Logs tool usage for analytics"
}
```

### Startup Hook (SessionStart)

```json
{
  "type": "command",
  "command": "uv run python ${CLAUDE_PLUGIN_ROOT}/hooks/startup.py",
  "timeout": 12000,
  "background": false,
  "description": "Loading project context"
}
```

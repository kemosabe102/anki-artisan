---
title: "Context Monitoring Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Context Monitoring Guide

**Purpose**: Proactive context window management with automated threshold warnings

**Hook**: `monitor-context-size.py` (PostToolUse hook)

**Status**: Active - triggers after every tool use

---

## Overview

The context monitoring hook tracks cumulative token usage during your session and provides warnings when you approach context window limits (200,000 tokens for Claude).

### Thresholds

| Level    | Tokens  | Percentage | Action Required           |
| -------- | ------- | ---------- | ------------------------- |
| WARNING  | 150,000 | 75%        | Consider optimization     |
| COMPRESS | 170,000 | 85%        | Compression recommended   |
| CRITICAL | 190,000 | 95%        | Immediate action required |

---

## Warning Messages

### WARNING Level (75% / 150,000 tokens)

**Message Format**:

```
⚠️  CONTEXT WINDOW WARNING
========================
Current Usage: 150,234 / 200,000 tokens (75.1%)

You've crossed the 75% threshold. Consider:
- Summarizing long tool outputs
- Breaking down complex operations
- Using Memory tool for long-term storage

Session: 20251010_143022
Operations: 47
```

**What This Means**:

- You're approaching context limit but not urgent yet
- Start thinking about context optimization
- Good time to review what's in context

**Recommended Actions**:

1. Review recent tool outputs for unnecessarily verbose responses
2. Summarize completed work before continuing
3. Consider if you need all previous context for next task
4. Use Memory tool to store research findings externally

**Example Optimization**:

```markdown
Before (wasteful):

- Read entire 5000-line file to check one function
- Multiple Grep operations on same files
- Keeping all research findings in context

After (optimized):

- Use Grep with specific pattern first, then Read only relevant sections
- Batch related Grep operations
- Store research findings in Memory tool, reference as needed
```

---

### COMPRESS Level (85% / 170,000 tokens)

**Message Format**:

```
🔶 CONTEXT WINDOW COMPRESS NEEDED
==================================
Current Usage: 172,456 / 200,000 tokens (86.2%)

You've crossed the 85% threshold. RECOMMENDED ACTIONS:
- Compress previous conversation context
- Store research findings in Memory tool
- Consider starting fresh session for new work
- Archive completed work to documentation

Session: 20251010_143022
Operations: 89
```

**What This Means**:

- Context window is getting tight
- Compression or session restart recommended soon
- Next few operations should be strategic

**Recommended Actions**:

1. **Compress Conversation** (if using Claude.ai web interface):
   - Use "Compress context" feature in conversation menu
   - Preserves key information, reduces token usage

2. **Archive Completed Work**:
   - Document findings in `.claude/docs/`
   - Create handoff file if work is complete
   - Reference documentation instead of keeping in context

3. **Store in Memory Tool**:

   ```markdown
   Store research findings, completed specs, or analysis results
   in Memory tool for retrieval when needed
   ```

4. **Consider Session Restart**:
   - If starting new task, consider fresh session
   - Archive current work first
   - Link to previous session in handoff

**Example Compression Strategy**:

```markdown
Instead of keeping full codebase analysis:

- Archive analysis to docs/analysis/component-review.md
- Keep only summary and action items in context
- Reference doc when needed

Instead of keeping all research findings:

- Store in Memory tool with clear keys
- Retrieve specific findings as needed
- Keep only current task context
```

---

### CRITICAL Level (95% / 190,000 tokens)

**Message Format**:

```
🚨 CONTEXT WINDOW CRITICAL
==========================
Current Usage: 192,845 / 200,000 tokens (96.4%)

You've crossed the 95% threshold. IMMEDIATE ACTION REQUIRED:
- Start new session NOW to avoid context overflow
- Archive current work to handoff documentation
- Use Memory tool to preserve critical information
- Compress conversation aggressively

Session: 20251010_143022
Operations: 156

⚠️  Next few operations may exceed context window!
```

**What This Means**:

- You're about to hit context window limit
- Next few operations may fail or lose context
- Immediate action required to avoid losing work

**Immediate Actions Required**:

1. **Archive Current Work** (PRIORITY):

   ```bash
   # Create handoff document NOW
   .claude/handoff/session-YYYYMMDD-HHMMSS.md

   Include:
   - Work completed this session
   - Current task status
   - Blockers or open questions
   - Next steps
   - Links to created/modified files
   ```

2. **Store Critical Information**:
   - Use Memory tool for research findings
   - Document analysis results
   - Save specs/plans to appropriate docs/

3. **Start Fresh Session**:
   - Exit Claude Code
   - Restart with new session
   - Load handoff from previous session
   - Continue with clean context

**Critical Session Checklist**:

- [ ] Create handoff document with session summary
- [ ] Archive completed work to documentation
- [ ] Store research findings in Memory tool
- [ ] Document blockers and next steps
- [ ] Commit any code changes
- [ ] Exit and restart Claude Code
- [ ] Load handoff in new session

---

## Analytics File Structure

**Location**: `.claude/logs/context-usage.json`

**Structure**:

```json
{
  "session_id": "20251010_143022",
  "session_start": "2025-10-10T14:30:22.123456",
  "operations": [
    {
      "timestamp": "2025-10-10T14:30:25.789012",
      "tool": "Read",
      "estimated_tokens": 4500,
      "cumulative_tokens": 4500
    },
    {
      "timestamp": "2025-10-10T14:31:02.345678",
      "tool": "Grep",
      "estimated_tokens": 1200,
      "cumulative_tokens": 5700
    }
  ],
  "thresholds_crossed": [
    {
      "timestamp": "2025-10-10T15:45:12.901234",
      "threshold": "warn",
      "tokens_at_crossing": 151234,
      "operation_count": 47
    }
  ],
  "total_tokens": 151234,
  "last_threshold": "warn"
}
```

**Fields**:

- `session_id`: Unique session identifier (timestamp-based)
- `session_start`: ISO-8601 timestamp of session start
- `operations`: Array of all tool operations with token estimates
- `thresholds_crossed`: History of threshold crossings
- `total_tokens`: Current cumulative token count
- `last_threshold`: Last threshold crossed (warn/compress/critical/null)

---

## Token Estimation Logic

The hook uses a **rough estimation** approach:

**Formula**: `text_length / 4 ≈ token_count`

**Estimation Sources**:

1. **Tool Input**: Tool name + serialized parameters
2. **Tool Output**: Response text or serialized output
3. **Minimum**: 100 tokens per operation (baseline overhead)

**Why Rough Estimation?**:

- Exact token counting requires tokenizer access (not available in hooks)
- Estimation is conservative (errs on side of caution)
- Good enough for threshold warnings
- Reduces hook execution overhead

**Example Estimations**:

```python
Read(large_file.py)
  Input:  "Read" + {"file_path": "..."} ≈ 100 tokens
  Output: 5000 lines of code ≈ 20,000 tokens
  Total:  ~20,100 tokens

Grep(pattern="test_*")
  Input:  "Grep" + {"pattern": "test_*"} ≈ 100 tokens
  Output: 50 matching files ≈ 500 tokens
  Total:  ~600 tokens

Task(agent, input)
  Input:  "Task" + agent name + input ≈ 500 tokens
  Output: Agent response ≈ varies widely
  Total:  ~500+ tokens (very conservative)
```

**Accuracy**:

- Conservative estimates (slightly overestimates)
- Better to warn early than late
- Typical accuracy: ±20% of actual tokens

---

## Best Practices

### Proactive Context Management

1. **Watch for WARNING**:
   - Not urgent, but start thinking ahead
   - Review what's consuming context
   - Plan optimization strategy

2. **Act on COMPRESS**:
   - Don't ignore this level
   - Take action before CRITICAL
   - Archive, compress, or restart

3. **React to CRITICAL**:
   - Drop everything, archive work
   - Start fresh session immediately
   - Don't risk context overflow

### Context-Efficient Workflows

**DO**:

- Use Grep before Read (filter first, read second)
- Batch related operations
- Store research in Memory tool
- Archive completed work promptly
- Restart sessions between major tasks

**DON'T**:

- Read entire large files unnecessarily
- Keep all research findings in context
- Continue working after CRITICAL warning
- Ignore COMPRESS warnings
- Mix multiple unrelated tasks in one session

### Session Boundaries

**Good Session Boundaries**:

- After completing a feature/spec/plan
- Before starting unrelated work
- After COMPRESS warning if switching tasks
- After major research phase

**Example**:

```markdown
Session 1: Research distributed caching patterns
→ Archive findings to docs/research/
→ Store in Memory tool
→ End session

Session 2: Implement caching layer
→ Load research from docs/
→ Focus on implementation only
→ Archive on completion
```

---

## Troubleshooting

### Hook Not Running

**Symptom**: No warnings appearing despite heavy context usage

**Possible Causes**:

1. Hook not registered in `.claude/settings.json`
2. Python environment issue
3. Logs directory doesn't exist
4. Hook execution failed silently

**Diagnosis**:

```bash
# Check hook registration
cat .claude/settings.json | grep -A 5 "monitor-context-size"

# Check logs
cat .claude/logs/hooks.log | grep "monitor-context-size"

# Check logs directory
ls -la .claude/logs/

# Test hook manually
echo '{"tool": "Read", "parameters": {}, "output": "test"}' | \
  uv run python .claude/hooks/monitor-context-size.py
```

**Resolution**:

- Verify hook registered in PostToolUse section
- Ensure `.claude/logs/` directory exists
- Check `hooks.log` for error messages
- Verify Python environment with `uv run python --version`

### False Warnings

**Symptom**: Warnings appearing too early or too late

**Possible Causes**:

- Token estimation inaccuracy
- Session data not persisting
- Multiple sessions overwriting analytics

**Resolution**:

- Accept ±20% estimation variance as expected
- Verify `.claude/logs/context-usage.json` updating correctly
- Check session_id in analytics file matches current session
- If estimates way off, adjust estimation logic in hook

### Analytics File Corruption

**Symptom**: Hook fails, analytics file contains invalid JSON

**Resolution**:

```bash
# Backup corrupted file
cp .claude/logs/context-usage.json .claude/logs/context-usage.json.bak

# Reset analytics
cat > .claude/logs/context-usage.json << 'EOF'
{
  "session_id": "reset",
  "session_start": "2025-10-10T00:00:00.000000",
  "operations": [],
  "thresholds_crossed": [],
  "total_tokens": 0,
  "last_threshold": null
}
EOF

# Restart session
# Hook will create new session on next tool use
```

---

## Future Enhancements

Potential improvements for this hook:

1. **Exact Token Counting**:
   - Integrate with tiktoken library
   - More accurate usage tracking
   - Better threshold precision

2. **Automatic Compression**:
   - Auto-trigger Memory tool storage
   - Auto-create handoff documents
   - Auto-suggest compression points

3. **Visual Dashboard**:
   - Real-time context usage graph
   - Operation breakdown by tool type
   - Session comparison analytics

4. **Adaptive Thresholds**:
   - Adjust thresholds based on task type
   - Learn from historical patterns
   - Personalized warning levels

5. **Integration with Stop Hook**:
   - Auto-generate context summary on Stop
   - Include in handoff documentation
   - Track usage across sessions

---

## Hook Configuration & Activation

**Location**: `.claude/settings.json` → `hooks.PostToolUse`

```json
{
  "matcher": "*",
  "hooks": [
    {
      "type": "command",
      "command": "uv run python .claude/hooks/monitor-context-size.py",
      "timeout": 5000,
      "background": false,
      "description": "Monitoring context window usage with threshold warnings"
    }
  ]
}
```

**Key Settings**:
- `matcher: "*"` - Triggers on every tool use
- `timeout: 5000` - 5 second max execution time
- `background: false` - Provides inline warnings to user

### Activation

**IMPORTANT**: Hook requires Claude Code session restart to activate.

**Steps**:
1. Exit Claude Code (current session)
2. Restart Claude Code
3. Hook will auto-initialize on first tool use
4. Monitor warnings as context grows

### Testing the Hook

```bash
# Test hook with sample input
echo '{"tool": "Read", "parameters": {"file_path": "test.py"}, "output": "test content"}' | \
  uv run python .claude/hooks/monitor-context-size.py

# Check analytics updated
cat .claude/logs/context-usage.json

# Check logs
tail -20 .claude/logs/hooks.log | grep "monitor-context-size"
```

### Performance

**Execution Time**: <50ms per tool operation
- Lightweight JSON operations
- Minimal computation (simple arithmetic)
- No external API calls

**Overhead**: Negligible
- Does not block tool operations
- Silent operation (no output unless threshold crossed)

---

## Related Documentation

- `.claude/hooks/monitor-context-size.py` - Hook implementation
- `.claude/settings.json` - Hook configuration
- `.claude/logs/context-usage.json` - Analytics data
- `.claude/logs/hooks.log` - Hook execution logs

---

**Version**: 1.1.0 (Consolidated from context-monitoring-hook.md)
**Last Updated**: 2025-12-01
**Maintainer**: Gauntlet Agents Team

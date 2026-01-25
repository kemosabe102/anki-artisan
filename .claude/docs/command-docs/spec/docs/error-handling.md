# Spec Command Error Handling

Error scenarios and recovery strategies for the simplified `/spec` 2-phase workflow.

---

## Quick Reference

| Phase | Error | Severity | Recovery |
|-------|-------|----------|----------|
| GENERATE | File path not found | BLOCKING | Verify path, suggest alternatives |
| GENERATE | Directory creation fails | BLOCKING | Check permissions, create parent dirs |
| GENERATE | Template not found | BLOCKING | Use fallback path or halt |
| GENERATE | ICE score below threshold | WARNING | Ask user to confirm or defer |
| VALIDATE | Required section empty | WARNING | Flag for user, list missing sections |
| VALIDATE | Untestable acceptance criteria | WARNING | Suggest improvements |
| VALIDATE | No Must priorities | BLOCKING | Require at least one Must FR |

---

## Phase 1: GENERATE Errors

### File Path Not Found

**Symptoms**: `file:path` doesn't exist or isn't readable.

**Recovery**:
1. Verify file path is correct
2. Check file extension (.md supported)
3. Suggest similar files:
   ```
   ❌ File not found: docs/guides/auth.md
   
   Similar files:
   - docs/guides/authentication-guide.md
   - docs/guides/auth-patterns.md
   ```

### Directory Creation Fails

**Symptoms**: Cannot create spec directory.

**Recovery**:
1. Check parent directory exists
2. Verify write permissions
3. Report actionable error:
   ```
   ❌ Cannot create directory: Permission denied
   
   Location: docs/01-planning/specifications/016-feature/
   
   Fix: Check write permissions on docs/01-planning/specifications/
   ```

### Template Not Found

**Symptoms**: `spec-template.md` doesn't exist.

**Recovery**:
1. Check primary path: `.claude/docs/command-docs/spec/templates/spec-template.md`
2. If missing, halt and report:
   ```
   ❌ Spec template not found
   
   Expected: .claude/docs/command-docs/spec/templates/spec-template.md
   
   Fix: Restore template or check repository status
   ```

### ICE Score Below Threshold (< 200)

**Symptoms**: Calculated ICE score is very low.

**Recovery**:
1. Present score breakdown to user
2. Offer options:
   ```
   ⚠️ LOW ICE SCORE (180)
   
   Impact: 6 — Affects small user segment
   Confidence: 5 — Some unknowns remain
   Ease: 6 — Moderate complexity
   
   Options:
   1. Proceed anyway (save to spec)
   2. Reframe the problem for higher impact
   3. Defer to backlog
   ```

---

## Phase 2: VALIDATE Errors

### Required Section Empty

**Symptoms**: One or more required sections have no content.

**Recovery**:
1. List missing sections:
   ```
   ⚠️ Spec incomplete - missing required sections:
   
   - Section 3: Scope (In/Out of scope not defined)
   - Section 9: Dependencies (No dependencies listed)
   
   Add [NONE] if truly empty, or populate with content.
   ```

### Untestable Acceptance Criteria

**Symptoms**: Criteria are vague or not verifiable.

**Recovery**:
1. Flag problematic criteria:
   ```
   ⚠️ Some acceptance criteria may not be testable:
   
   - "System should be fast" → Suggest: "Response time < 500ms p95"
   - "User experience improved" → Suggest: "Task completion rate > 90%"
   
   Rewrite criteria with measurable outcomes.
   ```

### No Must Priorities

**Symptoms**: All FRs are Should/Could/Won't, none are Must.

**Recovery**:
1. Require at least one Must:
   ```
   ❌ No Must-priority requirements defined
   
   Every spec needs at least one Must requirement for MVP.
   
   Review FR table and mark critical requirements as Must.
   ```

### NEEDS CLARIFICATION Markers Found

**Symptoms**: Spec contains unresolved `[NEEDS CLARIFICATION]` tags.

**Recovery**:
1. List all markers:
   ```
   ⚠️ Unresolved clarifications found:
   
   - Section 2: [NEEDS CLARIFICATION: Which user type is primary?]
   - Section 8: [NEEDS CLARIFICATION: What is the latency constraint?]
   
   Resolve these before locking the spec.
   ```

---

## General Recovery Strategies

### Escalation Path

1. **Flag warning** — Continue with notice
2. **Block and ask** — Require user decision
3. **Halt workflow** — Cannot proceed

### Preserving User Work

- Never delete user-provided input
- Always preserve partial progress
- Offer resume capability where possible

### Logging

Each phase should log:
- Input received
- Action taken
- Errors encountered
- Recovery attempted

# Error Handling & Recovery

Error scenarios and recovery strategies for the `/roadmap` command.

---

## Phase 1: Discovery Errors

### No Files Found

**Scenario**: Glob returns empty results - no roadmap files exist

**Symptoms**:
- Empty file list from discovery
- No active or archive roadmaps

**Recovery Steps**:
1. Check if roadmaps directory exists: `docs/00-project/roadmaps/`
2. Verify expected path structure
3. Report to user: "No roadmap files found. Create a roadmap first."

**User Action**: Create initial roadmap or verify directory structure

---

### Permission Errors

**Scenario**: Cannot read discovered files

**Symptoms**:
- File paths found but Read fails
- Permission denied errors

**Recovery Steps**:
1. Report specific files with permission issues
2. Suggest checking file permissions
3. Continue with readable files if partial success

**User Action**: Fix file permissions or run with elevated access


---

## Phase 2: Analysis Errors

### Partial Agent Failure (1-2 agents fail)

**Scenario**: Some agents complete successfully, others fail

**Symptoms**:
- Missing health scores for some dimensions
- Agent timeout or error response

**Recovery Steps**:
1. Report results from successful agents
2. Mark failed dimensions as "N/A" in dashboard
3. Continue to Phase 3 with partial data
4. Note which agents failed in output

**Example Output**:
```
Dimensions: Sprint Compliance (0.95/A), Freshness (N/A - agent timeout),
Token Density (0.75/C+)
```

---

### Complete Agent Failure (all 3 fail)

**Scenario**: All agents fail to return results

**Symptoms**:
- No health scores available
- Multiple timeout or error responses

**Recovery Steps**:
1. Report error details for each agent
2. Suggest manual validation as fallback
3. Escalate to user for decision

**User Action**: 
- Check agent availability
- Run manual validation
- Retry with reduced scope


---

### Agent Timeout

**Scenario**: Individual agent exceeds 2-minute timeout

**Symptoms**:
- Agent does not respond within timeout
- Partial results may be available

**Recovery Steps**:
1. Treat timed-out agent as failure
2. Continue with remaining agents
3. Retry once with reduced file scope (active roadmaps only)

**Retry Pattern**:
```python
# Original scope
Task(subagent_type="planning", prompt="Analyze: {all_files}")

# Reduced scope retry
Task(subagent_type="planning", prompt="Analyze: {active_files_only}")
```

---

## Phase 3: Validation Errors

### Broken Links Detected

**Scenario**: Cross-reference validation finds invalid links

**Symptoms**:
- Link validation report shows broken references
- File paths or anchors don't resolve

**Recovery Steps**:
1. Report broken links with file:line numbers
2. Include suggested fixes where possible
3. Recommend `/roadmap update` for automated fixes

**Example Output**:
```
Broken Links: 2 found
- Q1-2026.md:92 -> Missing anchor #milestone-3
- Q1-2026.md:145 -> File not found: ../archive/Q3-2025.md
```


---

### Circular Dependencies

**Scenario**: Roadmap files reference each other in a loop

**Symptoms**:
- Validation detects circular reference chain
- File A -> File B -> File C -> File A

**Recovery Steps**:
1. Report circular dependency chain
2. Identify the link that should be removed
3. Manual fix required (cannot auto-resolve)

---

## Quick Reference Table

| Phase | Error Type | Severity | Recovery |
|-------|------------|----------|----------|
| 1 | No files found | BLOCKING | Check directory, create first roadmap |
| 1 | Permission errors | BLOCKING | Fix permissions, verify access |
| 2 | Partial agent failure | WARNING | Continue with partial results |
| 2 | Complete agent failure | BLOCKING | Escalate, suggest manual validation |
| 2 | Agent timeout | WARNING | Retry with reduced scope |
| 3 | Broken links | WARNING | Report with line numbers, suggest update |
| 3 | Circular dependencies | WARNING | Report chain, manual fix required |

---

## Escalation Protocol

When to escalate to user:

1. **Phase 1 blocking errors**: No files found, all files unreadable
2. **Phase 2 complete failure**: All 3 agents fail
3. **Repeated timeouts**: Same agent times out on retry
4. **User decision required**: Conflicting recommendations

**Escalation Format**:
```
ROADMAP CHECK BLOCKED

Error: [Description]
Phase: [1-4]
Recovery attempted: [Yes/No - what was tried]

Recommended action: [Specific user action]
```

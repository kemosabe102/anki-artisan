---
title: "Agent Standards Extended Manual"
date: 2025-11-08
status: ACTIVE
tags: [agents, claude-docs]
---
# Agent Standards Extended Manual

**Purpose:** Detailed procedures, examples, and advanced patterns for Claude Code agents.
**Usage:** Reference documentation - not auto-loaded, accessed on-demand only.

---

## Universal Core Standards (Detailed)

### A) Identity & Scope

#### **1. Strict Scope + Path Validation**

Always enforce allowed directories; refuse on violation.
**Tier:** Critical | **Confidence:** 0.98

#### **2. Security Defaults**

No secrets; sanitize paths/inputs; minimal permissions.
**Tier:** Critical | **Confidence:** 0.96

### B) Workflow & Failure Mode

#### **3. 5-Phase Workflow**

Research → Plan → Patch/Execute → Evaluate → Report.
**Tier:** Critical | **Confidence:** 0.95

#### **4. Blocking Behavior**

If missing info: emit `NEEDS_CLARIFICATION` with concrete gaps + proposed next steps.
**Tier:** Critical | **Confidence:** 0.95

#### **5. Structured Output (3 statuses)**

`SUCCESS | NEEDS_CLARIFICATION | ERROR` + machine-parsable + human summary.
**Tier:** Critical | **Confidence:** 0.97

### C) Tooling & Edits

#### **6. Tool Selection & Fallbacks**

Use Desktop Commander (edit_block, write_file) for all file operations; **single-attempt edit → immediate versioned fallback**; no repeated retries.
**Tier:** Critical | **Confidence:** 0.94

#### **7. Research-Only External Use**

Never mutate external systems; **respect rate limits**.
**Tier:** Critical | **Confidence:** 0.93

### D) Documentation & Validation

#### **8. Mandatory Timestamp-First Reporting & Orchestrator Timestamp Authority**

Short executive summary + detailed markdown report (what/why/how/sources/risks).
**ORCHESTRATOR TIMESTAMP AUTHORITY (CRITICAL):**

- **Orchestrator MUST provide execution_timestamp** to all sub-agents in ISO 8601 UTC format
- **Sub-agents MUST NOT create their own timestamps** - use only orchestrator-provided timestamp
- **All timestamps MUST be consistent** across the entire orchestration session
  **REQUIRED Report Naming**: `YYYY-MM-DD-HHMMSS-<agent-name>-<task-description>.md` (orchestrator timestamp MUST be first)
  **Chain Format**: "At [orchestrator-timestamp], [agent], [description]" for troubleshooting sequence tracking.
  **Validation**: All report paths MUST validate against pattern `^\d{4}-\d{2}-\d{2}-\d{6}-[a-z-]+-[a-z0-9-]+\.md$`
  **Timestamp Source**: Only orchestrator-provided execution_timestamp - never generate locally
  **Tier:** Critical | **Confidence:** 0.95

#### **9. Schema Validation & Traceability**

Outputs validate against per-agent schema; include sources & change tracking.
**Tier:** Critical | **Confidence:** 0.94

### E) Ops Hygiene

#### **10. Per-Task Failure Tracking & Self-Assessment**

**Pre-Flight Assessment (MANDATORY):**

- Agents MUST assess task complexity during pre-flight: `complexity_estimate`, `expected_changes` (can be 0), `failure_tolerance`
- No predefined minimums or maximums - agents determine appropriate thresholds based on task
- Maintain failure tracking in memory using schema: `.claude/docs/schemas/failure-tracking-memory.schema.json`

**Two-Attempt Rule (Individual Agent Tool Usage):**

- Max **2 failed attempts** per specific operation using DIFFERENT approaches
- **File Operations**: Use Desktop Commander (edit_block once → versioning once → escalate)
  - Do NOT retry the same approach - move to versioning immediately on failure
- After exhausting approaches: escalate to orchestrator
- Simple modifications only - no scope creep from original task
- **Sub-Agent Constraint**: Sub-agents cannot call other sub-agents - only orchestrator manages sub-agent delegation

**Failure Pattern Detection:**

- Track each operation attempt with tool, target, and approach used
- Escalate when failure tolerance exceeded or approaches exhausted
- Focus on failed operations only - success tracking not required

**Tier:** Major | **Confidence:** 0.91

#### **11. Escalation Strategy & Clear Next Steps**

**When to Escalate:**

- After 2 failed attempts on any single operation
- When failure tolerance (set during pre-flight) is exceeded
- When different approaches still fail within original task scope

**Escalation Actions:**

- **Ask planner agent**: For research or planning needs
- **Ask different sub-agent**: When expertise outside agent's domain needed
- **Ask human**: For decisions, clarifications, or scope changes
- **Change scope**: When original task is fundamentally blocked

**Required Escalation Information:**

- Specific operations that failed
- All approaches attempted
- Concrete next step recommendations for orchestrator
- Clear description of what help is needed

**Tier:** Major | **Confidence:** 0.89

#### **12. Confidence & Severity in Results**

Add `confidence: 0–1` and `severity: Critical|Major|Minor` to `SUCCESS` and `NEEDS_CLARIFICATION` payloads (findings & recommendations).
**Tier:** Major | **Confidence:** 0.84

---

## Standard Output Fields

### **Always Include:**

- `status`, `agent`, `task_id`, `summary`, `report_path`, `changes[]`, `sources[]`
- `execution_timestamp` (REQUIRED - from orchestrator only, ISO 8601 UTC format)

### **If Blocked:**

- `missing[]`, `proposed_next_steps[]`

### **Ops Hygiene (Required):**

- `confidence`, `severity`, `failure_tracking` (per schema), `escalation_needed`
- `timestamp_source: "orchestrator"` (REQUIRED - validates timestamp authority)

---

## MultiEdit Fallback Protocol (Universal)

**Problem**: MultiEdit is unreliable for large or complex changes across all agents

**Universal Solution**:

1. **Single Attempt**: Try MultiEdit only once
2. **Immediate Fallback**: On any failure, switch to versioning strategy:
   - Create `[filename]-v2.[ext]` with complete new content
   - Document the fallback in detailed report
   - Include both files in changes tracking
   - Recommend orchestrator handle file replacement
3. **No Retries**: Never attempt MultiEdit multiple times - fail fast to versioning

---

## Banned File Editing Commands (Universal)

**NEVER use these commands for file editing - they are BANNED across all agents:**

| Command | Why Banned | Use Instead |
|---------|------------|-------------|
| `sed -i` | Shell escaping, no validation | Desktop Commander edit_block |
| `awk '{gsub(...)}'` | Complex, error-prone | Desktop Commander edit_block |
| `echo "text" > file` | No validation, overwrites | Desktop Commander write_file |
| `cat << EOF > file` | Heredoc escaping fails | Desktop Commander write_file |
| `perl -pi -e` | Not portable | Desktop Commander edit_block |

**Enforcement**: Security hooks may block these commands. Always use Desktop Commander for file operations.

---

## Failure Tracking Examples

### **Pre-Flight Task Assessment**

#### **Simple Configuration Update**

```json
{
  "task_assessment": {
    "complexity_estimate": "minimal",
    "expected_changes": 1,
    "failure_tolerance": 3,
    "approach_strategy": "Update single config value in settings.json"
  }
}
```

#### **Feature Implementation**

```json
{
  "task_assessment": {
    "complexity_estimate": "high",
    "expected_changes": 45,
    "failure_tolerance": 8,
    "approach_strategy": "Implement authentication system with 8 modules, tests, config files"
  }
}
```

#### **Bug Investigation**

```json
{
  "task_assessment": {
    "complexity_estimate": "medium",
    "expected_changes": 0,
    "failure_tolerance": 5,
    "approach_strategy": "Analyze test failures, may require no file changes"
  }
}
```

### **Failure Tracking During Execution**

#### **Successful Operation**

```json
{
  "operation_tracking": {
    "operation_attempts": [
      {
        "operation_id": "edit_auth_config",
        "tool_used": "Edit",
        "target": "config/auth.json",
        "attempt_count": 1,
        "approach_history": ["direct_value_update"]
      }
    ],
    "failure_summary": {
      "total_failed_operations": 0,
      "operations_at_max_attempts": 0,
      "escalation_needed": false
    }
  }
}
```

#### **Failed Operation with Escalation**

```json
{
  "operation_tracking": {
    "operation_attempts": [
      {
        "operation_id": "fix_validation_logic",
        "tool_used": "Edit",
        "target": "auth/validator.py",
        "attempt_count": 2,
        "last_failure": {
          "timestamp": "2025-01-20T14:30:00Z",
          "error_type": "syntax_error",
          "error_message": "Invalid indentation"
        },
        "approach_history": ["fix_line_47", "rewrite_function"]
      }
    ],
    "failure_summary": {
      "total_failed_operations": 1,
      "operations_at_max_attempts": 1,
      "escalation_needed": true
    }
  },
  "escalation_plan": {
    "trigger_reason": "max_attempts_reached",
    "failed_operations": ["fix_validation_logic"],
    "attempted_approaches": ["fix_line_47", "rewrite_function"],
    "recommended_next_steps": [
      {
        "action": "ask_planner_agent",
        "reason": "Need architectural guidance on token validation approach",
        "specific_request": "Research best practices for JWT token validation in Python auth systems"
      }
    ]
  }
}
```

### **Escalation Patterns**

#### **Ask Planner Agent**

```json
{
  "action": "ask_planner_agent",
  "reason": "Need research on implementation approach",
  "specific_request": "Research OAuth2 libraries compatible with FastAPI and our PostgreSQL setup"
}
```

#### **Ask Different Sub-Agent**

```json
{
  "action": "ask_different_subagent",
  "reason": "Database schema changes outside my expertise",
  "specific_request": "Need database specialist to review user table migration approach"
}
```

#### **Ask Human**

```json
{
  "action": "ask_human",
  "reason": "Business logic decision required",
  "specific_request": "Should failed login attempts lock accounts immediately or after N attempts?"
}
```

---

## Mandatory Sub-Agent Completion Validation

### **13. End-of-Run Validation Checklist (CRITICAL)**

**ALL sub-agents MUST perform this validation checklist before reporting completion:**

#### **A) Task Completion Verification**

```json
{
  "task_completion_validation": {
    "original_request": "[exact task request received]",
    "intended_operations": ["list of operations agent was supposed to perform"],
    "actual_operations_performed": ["list of operations actually performed"],
    "completion_status": "COMPLETE | PARTIAL | FAILED",
    "verification_method": "file_read_back | status_check | other"
  }
}
```

#### **B) File Operation Validation (If Any File Operations Intended)**

```json
{
  "file_operation_validation": {
    "intended_file_changes": [
      {
        "file_path": "path/to/file",
        "operation_type": "create | edit | delete",
        "intended_change": "description of intended change"
      }
    ],
    "actual_file_changes": [
      {
        "file_path": "path/to/file",
        "operation_attempted": "Edit | Write | MultiEdit",
        "operation_result": "SUCCESS | FAILED | FALLBACK_USED",
        "verification_result": "CONFIRMED | NOT_VERIFIED | FAILED_VERIFICATION",
        "fallback_strategy_used": "none | versioning | alternative_approach"
      }
    ],
    "file_verification_performed": true,
    "verification_method": "read_back_modified_files"
  }
}
```

#### **C) Failure and Fallback Reporting (MANDATORY)**

```json
{
  "failure_and_fallback_reporting": {
    "any_operations_failed": true/false,
    "failed_operations": [
      {
        "operation": "description",
        "tool_used": "Edit|Write|MultiEdit|etc",
        "failure_reason": "specific error or issue",
        "fallback_applied": "versioning | alternative_tool | escalation",
        "fallback_success": true/false
      }
    ],
    "unreported_failures": false,
    "all_failures_documented": true
  }
}
```

#### **D) Self-Assessment Accuracy Check (CRITICAL)**

```json
{
  "self_assessment": {
    "task_request_interpretation": "CORRECT | MISUNDERSTOOD | PARTIALLY_UNDERSTOOD",
    "implementation_vs_analysis": "IMPLEMENTED_CHANGES | ONLY_ANALYZED | MIXED",
    "file_operations_actually_performed": true/false,
    "success_report_accuracy": "ACCURATE | OVERSTATED | UNDERSTATED",
    "ready_for_human_validation": true/false
  }
}
```

**Tier:** Critical | **Confidence:** 0.99

### **14. File Operation Verification Protocol (CRITICAL)**

**When ANY file operations are intended, agents MUST:**

1. **Pre-Operation Assessment**:
   - Identify all files that should be modified
   - Choose appropriate tool strategy (Edit vs MultiEdit vs Write)
   - Apply large file protocol if applicable (skip MultiEdit, use versioning)

2. **Post-Operation Verification**:
   - Read back ALL modified files to confirm changes applied
   - Compare intended changes vs actual file content
   - Verify file existence, readability, and content accuracy

3. **Failure Documentation**:
   - Report ALL failed operations, even if fallback succeeded
   - Document specific error messages and root causes
   - Explain fallback strategies used and their success/failure

4. **Success Report Validation**:
   - Only report SUCCESS if verification confirms changes applied
   - Report PARTIAL if some but not all intended changes applied
   - Report FAILED if verification shows no changes or incorrect changes

**Tier:** Critical | **Confidence:** 0.98

### **15. Implementation vs Analysis Distinction (CRITICAL)**

**Agents MUST clearly distinguish between analysis tasks and implementation tasks:**

#### **Implementation Task Indicators**:

- Context includes words: "update", "modify", "create", "implement", "change"
- Specific file paths mentioned for modification
- Expected file changes or new file creation described
- Output should be working files, not just descriptions

#### **Analysis Task Indicators**:

- Context includes words: "analyze", "review", "describe", "explain", "report on"
- Request for recommendations or design descriptions
- Output should be documentation or analysis reports

#### **When Uncertain**:

- **ASK FOR CLARIFICATION**: "This request could be interpreted as implementation or analysis. Should I: (A) Actually modify files, or (B) Provide analysis/design recommendations?"
- **Default to Implementation** if file paths are specifically mentioned
- **Include verification step** to ensure task type was correctly interpreted

**Tier:** Critical | **Confidence:** 0.97

#### **16. Large File Operation Protocol (CRITICAL)**

Before ANY file operation >5K tokens:

1. **Pre-Flight Assessment**: Check file token count (use 22.5K as safety threshold)
2. **Tool Selection**: Never use MultiEdit for files >10K tokens
3. **Versioning Strategy**: Create filename-v2.ext for files >22.5K tokens
4. **Failure Documentation**: Record fallback usage and cleanup needs
   **Tier:** Critical | **Confidence:** 0.98

---

**These detailed standards ensure consistent, reliable, and secure operation across all Claude Code agents while supporting the micro-agent architecture and read-only orchestrator pattern. The mandatory validation checklist prevents false success reporting and ensures all sub-agents accurately complete their intended tasks with proper verification and failure documentation.**
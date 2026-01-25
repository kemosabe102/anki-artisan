# Orchestrator Timestamp Management Guide

## Overview

This guide defines the **Timestamp Authority System** that ensures consistent, accurate timestamps across all sub-agent interactions in the orchestration system.

## Problem Statement

### Issues Identified

- **Inconsistent Timestamps**: Sub-agents generating their own timestamps leads to chronological inconsistencies
- **Past Dates**: Reports showing outdated timestamps (e.g., `2025-01-27` when current date is `2025-09-20`)
- **Multiple Formats**: Mixed timestamp formats across different agents and reports
- **Troubleshooting Difficulty**: Inconsistent timestamps make debugging multi-agent workflows nearly impossible

### Root Cause

Sub-agents creating their own timestamps without coordination from the orchestrator agent.

## Timestamp Authority System

### Core Principle

**The orchestrator agent is the SINGLE SOURCE OF TRUTH for all timestamps in the system.**

### Implementation Rules

#### 1. Orchestrator Responsibilities

- **Generate execution_timestamp** at the start of each workflow session
- **Use ISO 8601 UTC format**: `YYYY-MM-DDTHH:MM:SS.sssZ`
- **Pass execution_timestamp** to ALL sub-agent delegations
- **Ensure consistency** across the entire orchestration session

#### 2. Sub-Agent Requirements

- **MUST accept execution_timestamp** parameter from orchestrator
- **MUST NOT generate own timestamps** under any circumstances
- **MUST use orchestrator timestamp** for all reports, logs, and outputs
- **MUST validate timestamp_source: "orchestrator"** in output schemas

#### 3. Report Naming Convention

- **Format**: `YYYY-MM-DD-HHMMSS-<agent-name>-<task-description>.md`
- **Timestamp Source**: Extract from orchestrator execution_timestamp (convert to filename format)
- **Example**: `2025-09-20-143022-claude-code-agent-timestamp-management-update.md`

## Implementation Guide

### Orchestrator Delegation Pattern

```javascript
// Generate execution timestamp at workflow start
const execution_timestamp = new Date().toISOString(); // "2025-09-20T14:30:22.456Z"

// Pass to ALL sub-agent delegations
const delegation_input = {
  context: 'Your task description here...',
  execution_timestamp: execution_timestamp,
  // ... other parameters
};

// Delegate to sub-agent
const result = await delegate_to_agent('claude-code-agent', delegation_input);

// Validate timestamp consistency in response
if (
  result.timestamp_source !== 'orchestrator' ||
  result.execution_timestamp !== execution_timestamp
) {
  throw new Error('Timestamp authority violation detected');
}
```

### Sub-Agent Input Processing

```javascript
// Sub-agent must accept and validate orchestrator timestamp
function process_input(input) {
  // Validate required timestamp
  if (!input.execution_timestamp) {
    return {
      status: 'ERROR',
      message: 'Missing required execution_timestamp from orchestrator',
      hint: 'Orchestrator must provide execution_timestamp in all delegations',
    };
  }

  // Validate timestamp format
  if (!isValidISO8601(input.execution_timestamp)) {
    return {
      status: 'ERROR',
      message: 'Invalid execution_timestamp format',
      hint: 'execution_timestamp must be ISO 8601 UTC format',
    };
  }

  // Use orchestrator timestamp for all outputs
  const report_timestamp = convertToFilename(input.execution_timestamp);
  const report_path = `.claude/docs/reports/${report_timestamp}-${agent_name}-${task_id}.md`;

  return {
    status: 'SUCCESS',
    execution_timestamp: input.execution_timestamp,
    timestamp_source: 'orchestrator',
    report_path: report_path,
    // ... other outputs
  };
}
```

### Timestamp Utilities

```javascript
// Convert ISO 8601 to filename format
function convertToFilename(iso_timestamp) {
  const date = new Date(iso_timestamp);
  return date
    .toISOString()
    .replace(/T/, '-')
    .replace(/:/g, '')
    .replace(/\.\d{3}Z$/, '')
    .substring(0, 15); // "2025-09-20-143022"
}

// Validate ISO 8601 format
function isValidISO8601(timestamp) {
  const iso8601Regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$/;
  return iso8601Regex.test(timestamp) && !isNaN(Date.parse(timestamp));
}

// Generate current UTC timestamp
function generateExecutionTimestamp() {
  return new Date().toISOString();
}
```

## Schema Requirements

### Updated Input Schemas

All sub-agent input schemas MUST include:

```json
{
  "execution_timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Orchestrator-provided execution timestamp in ISO 8601 UTC format"
  }
}
```

### Updated Output Schemas

All sub-agent output schemas MUST include:

```json
{
  "execution_timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Orchestrator-provided execution timestamp in ISO 8601 UTC format"
  },
  "timestamp_source": {
    "const": "orchestrator",
    "description": "Validates that timestamp came from orchestrator, not sub-agent"
  }
}
```

## Validation & Testing

### Orchestrator Validation

- **Before delegation**: Ensure execution_timestamp is generated and valid
- **After delegation**: Validate sub-agent returned same timestamp
- **Schema compliance**: Verify timestamp_source === "orchestrator"

### Sub-Agent Validation

- **Input validation**: Reject delegations without valid execution_timestamp
- **Output validation**: Always include execution_timestamp and timestamp_source
- **Report generation**: Use orchestrator timestamp for all file naming

### Testing Scenarios

1. **Happy Path**: Orchestrator provides timestamp, sub-agent uses it correctly
2. **Missing Timestamp**: Sub-agent rejects delegation without execution_timestamp
3. **Invalid Format**: Sub-agent rejects malformed timestamp
4. **Consistency Check**: Multiple sub-agents in sequence use same timestamp
5. **Troubleshooting**: Chronological chain analysis works correctly

## Migration Plan

### Phase 1: Update Documentation and Standards ✅

- [x] Update agent-standards-runtime.md and agent-standards-extended.md with timestamp authority requirements
- [x] Update orchestrator-workflow.md with orchestrator timestamp coordination
- [x] Update report templates to use orchestrator timestamps
- [x] Create orchestrator timestamp management guide

### Phase 2: Update Schemas

- [x] Add execution_timestamp and timestamp_source to claude-code-agent.result.schema.json
- [ ] Update planner-agent input/output schemas
- [ ] Update all other agent input/output schemas
- [ ] Create input schema validation for execution_timestamp

### Phase 3: Update Agent Configurations

- [x] Update claude-code-agent.md to require orchestrator timestamps
- [ ] Update planner-agent.md with timestamp requirements
- [ ] Update all other agent configurations
- [ ] Add timestamp validation to agent instructions

### Phase 4: Implementation Testing

- [ ] Test orchestrator delegation with execution_timestamp
- [ ] Validate sub-agent timestamp compliance
- [ ] Test report generation with consistent timestamps
- [ ] Verify chronological troubleshooting chain functionality

### Phase 5: Full Deployment

- [ ] Update orchestrator agent logic to generate and pass timestamps
- [ ] Deploy updated sub-agent configurations
- [ ] Monitor for timestamp consistency violations
- [ ] Document any exceptions or edge cases

## Troubleshooting

### Common Issues

#### Sub-Agent Generates Own Timestamp

**Symptoms**: Different timestamps in reports from same orchestration session
**Solution**: Check agent configuration ensures timestamp_source validation

#### Missing execution_timestamp in Delegation

**Symptoms**: Sub-agent returns ERROR status about missing timestamp
**Solution**: Update orchestrator to include execution_timestamp in all delegations

#### Invalid Timestamp Format

**Symptoms**: Sub-agent rejects timestamp or validation fails
**Solution**: Ensure orchestrator generates proper ISO 8601 UTC format

#### Past Dates in Reports

**Symptoms**: Reports show dates like 2025-01-27 when current date is later
**Solution**: This indicates sub-agent is generating own timestamp - enforce orchestrator authority

### Debugging Commands

```bash
# Find reports with inconsistent timestamps
grep -r "Generated At:" .claude/docs/reports/ | sort

# Check for timestamp format violations
find .claude/docs/reports/ -name "*.md" | grep -v "^[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{6}"

# Validate chronological ordering
ls -la .claude/docs/reports/*.md | sort -k9
```

## Success Metrics

- **Timestamp Consistency**: 100% of reports in same session use identical base timestamp
- **Format Compliance**: 100% of timestamps follow ISO 8601 UTC format
- **Authority Compliance**: 100% of outputs include timestamp_source: "orchestrator"
- **Troubleshooting Effectiveness**: Chronological chain analysis works reliably
- **Zero Past Dates**: No reports show dates earlier than orchestration start time

## Related Documentation

- [Agent Standards Runtime](../agents/agent-standards-runtime.md) - Auto-loaded universal baseline including timestamp requirements
- [Agent Standards Extended](../agents/agent-standards-extended.md) - Detailed timestamp management procedures
- [Workflow](../../03-workflows/orchestrator-workflow.md) - Orchestrator coordination and timestamp persistence
- [Claude Code Report Template](../../../templates/claude-code-report.md) - Updated template format
- [Base Agent Schema](../../shared/schemas/base-agent.schema.json) - Output validation requirements
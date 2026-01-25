---
title: "Claude Code Workflow Patterns & Templates"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Claude Code Workflow Patterns & Templates

**Last Updated**: 2025-09-21
**Pattern Library Version**: 1.0.0

## Overview

This document provides reusable patterns and templates for designing effective Claude Code workflows. These patterns have been validated through production use and research-backed best practices.

## Core Workflow Patterns

### 1. **Hub-and-Spoke Pattern** (Sub-Agent Coordination)

**Use Case**: Orchestrating multiple specialized sub-agents for complex tasks

**Pattern Structure**:

```
Orchestrator (Hub)
├── Sub-Agent A (Planning)
├── Sub-Agent B (Implementation)
├── Sub-Agent C (Testing)
└── Sub-Agent D (Review)
```

**Implementation Template**:

```json
{
  "pattern_name": "hub_and_spoke_coordination",
  "orchestrator_role": "context_management_and_delegation",
  "sub_agent_roles": {
    "planner": "strategic_analysis_and_research",
    "development": "code_implementation_and_execution",
    "test_runner": "validation_and_quality_assurance",
    "code_reviewer": "quality_gates_and_standards"
  },
  "coordination_rules": {
    "no_direct_sub_agent_communication": true,
    "orchestrator_maintains_state": true,
    "2_attempt_rule_applies": true,
    "human_escalation_after_failure": true
  }
}
```

**Benefits**:

- Centralized state management
- Clear responsibility boundaries
- Consistent error handling
- Scalable coordination

**Example Applications**:

- Feature development workflow
- Code review workflow
- Quality assurance processes

### 2. **Pipeline Pattern** (Sequential Workflow Stages)

**Use Case**: Multi-stage workflows with validation gates and quality checkpoints

**Pattern Structure**:

```
Input → Stage 1 → Gate 1 → Stage 2 → Gate 2 → Stage 3 → Output
```

**Implementation Template**:

```markdown
## Pipeline Workflow Template

### Stage Definitions

1. **[Stage Name]**: [Purpose and responsibilities]
   - Input: [Expected input format]
   - Process: [Key activities and validations]
   - Output: [Output format and validation criteria]
   - Gate Criteria: [Requirements for advancement]

### Quality Gates

- **Gate [N]**: [Validation requirements]
  - Success Criteria: [Specific measurable criteria]
  - Failure Handling: [Rollback or retry procedures]
  - Escalation: [When to escalate to human or different sub-agent]

### Error Handling

- **Rollback Capability**: [How to return to previous stage]
- **Retry Logic**: [When and how to retry failed stages]
- **Alternative Paths**: [Alternative approaches for persistent failures]
```

**Benefits**:

- Clear progression model
- Quality validation at each stage
- Rollback capability
- Predictable outcomes

**Example Applications**:

- Feature development: `/spec` → `/plan` → `/tasks` → `/implement`
- Code review: Changes → Validation → Review → Integration
- Documentation: Research → Draft → Review → Publication

### 3. **Observer Pattern** (Event-Driven Updates)

**Use Case**: Automated updates across multiple systems when events occur

**Pattern Structure**:

```
Event Source → Event → Multiple Observers → Independent Updates
```

**Implementation Template**:

```json
{
  "pattern_name": "event_driven_updates",
  "event_sources": ["sub_agent_completion", "milestone_achievement", "workflow_state_change"],
  "observers": [
    "living_sprint_tracker",
    "roadmap_updater",
    "startup_evaluator",
    "progress_reporter"
  ],
  "update_protocol": {
    "event_format": "structured_json_with_metadata",
    "observer_independence": true,
    "failure_isolation": true,
    "retry_mechanism": "exponential_backoff"
  }
}
```

**Benefits**:

- Decoupled systems
- Automatic synchronization
- Failure isolation
- Scalable event handling

**Example Applications**:

- Progress tracking across documents
- Status updates in multiple systems
- Notification and alert systems

### 4. **Research-First Pattern** (Context7 Integration)

**Use Case**: Incorporating external research and best practices into workflows

**Pattern Structure**:

```
Problem → Research Phase → Pattern Application → Implementation → Validation
```

**Implementation Template**:

````markdown
## Research-First Workflow Template

### Research Phase

1. **Context7 Library Resolution**
   ```json
   {
     "operation": "resolve-library-id",
     "library_name": "[relevant library/framework]"
   }
   ```
````

2. **Best Practices Research**

   ```json
   {
     "operation": "get-library-docs",
     "context7CompatibleLibraryID": "[resolved ID]",
     "topic": "[specific implementation topic]",
     "tokens": 5000
   }
   ```

3. **Pattern Documentation**
   - Extract key patterns and practices
   - Document application to current context
   - Create implementation guidance

### Application Phase

1. **Pattern Integration**: Apply researched patterns to workflow design
2. **Context Adaptation**: Adapt patterns to Claude Code ecosystem constraints
3. **Validation Design**: Create validation criteria based on best practices

### Implementation Phase

1. **Pattern Application**: Implement workflow using researched patterns
2. **Continuous Validation**: Validate against researched best practices
3. **Documentation**: Document pattern usage for future reference

````

**Benefits**:
- Research-backed decisions
- Industry best practices integration
- Reduced trial-and-error
- Knowledge accumulation

**Example Applications**:
- Feature development with architecture research
- Workflow optimization with performance patterns
- Quality assurance with testing best practices

## Slash Command Design Patterns

### 1. **Command Composition Pattern**

**Use Case**: Building commands that coordinate multiple sub-processes

**Template Structure**:
```markdown
---
argument-hint: "<primary argument | option:value>"
description: [Clear, concise description of command purpose]
allowed-tools: [Specific tools with parameter restrictions]
model: [Appropriate model for command complexity]
---

# [Command Name] - [Purpose]

## Phase 1: Context Loading & Validation
[Document loading, input validation, prerequisite checks]

## Phase 2: [Primary Process]
[Main command logic and sub-agent coordination]

## Phase 3: [Output Generation]
[Result formatting and artifact creation]

## Phase 4: [Integration & Handoff]
[Integration with other workflows and next steps]
````

**Example**: `/spec` command structure

### 2. **Research Integration Pattern**

**Use Case**: Commands that require external research and best practices

**Template Structure**:

```markdown
## Phase 1: Research & Discovery

### Context7 Research Protocol

1. **Library Resolution**: Identify relevant libraries/frameworks
2. **Best Practices Research**: Query specific implementation patterns
3. **Pattern Documentation**: Document findings for application

### Research Integration

- Apply researched patterns to command implementation
- Validate against industry best practices
- Document research sources and rationale
```

**Example**: Feature development commands with Context7 integration

### 3. **Validation Gate Pattern**

**Use Case**: Commands with quality gates and validation requirements

**Template Structure**:

```markdown
## Quality Gates

### [Gate Name]

- **Criteria**: [Specific validation requirements]
- **Validation**: [How criteria are checked]
- **Failure Handling**: [What happens on validation failure]
- **Success Path**: [Next steps on validation success]

## Error Handling Protocol

- **Retry Logic**: [When and how to retry]
- **Escalation**: [When to escalate to human]
- **Recovery**: [How to recover from failures]
```

**Example**: Code review workflow with quality validation

## Hook Design Patterns

### 1. **Validation Hook Pattern**

**Use Case**: Automated validation and quality control

**Template Structure**:

```python
#!/usr/bin/env python3
"""
[Hook Name] - [Purpose]
[Description of validation performed]
"""

import sys
import json
from pathlib import Path

def validate_specific_aspect:
    """Validate specific aspect of workflow/tool usage."""
    # Validation logic
    pass

def main():
    """Main hook execution with error handling."""
    try:
        context = load_context()
        validation_results = validate_specific_aspect

        if validation_results['success']:
            sys.exit(0)  # Allow operation
        else:
            print(json.dumps({
                "error": validation_results['error'],
                "guidance": validation_results['guidance']
            }))
            sys.exit(1)  # Block operation

    except Exception as e:
        # Graceful degradation
        print(f"Hook validation failed: {e}", file=sys.stderr)
        sys.exit(0)  # Allow operation to proceed

if __name__ == "__main__":
    main()
```

**Example**: Pre-tool validation hooks

### 2. **Progress Tracking Hook Pattern**

**Use Case**: Automated progress updates and status tracking

**Template Structure**:

```python
#!/usr/bin/env python3
"""
[Hook Name] - Progress Tracking
Automatically update progress tracking systems
"""

import json
from datetime import datetime
from pathlib import Path

def update_living_sprint(completion_event):
    """Update living sprint with completion information."""
    # Progress update logic
    pass

def update_roadmap_status(completion_event):
    """Update roadmap item status based on completion."""
    # Roadmap update logic
    pass

def main():
    """Main progress tracking execution."""
    try:
        completion_event = detect_completion_event()

        if completion_event:
            update_living_sprint(completion_event)
            update_roadmap_status(completion_event)

        sys.exit(0)  # Non-blocking

    except Exception as e:
        # Non-blocking error handling
        print(f"Progress tracking failed: {e}", file=sys.stderr)
        sys.exit(0)  # Continue workflow

if __name__ == "__main__":
    main()
```

**Example**: Sub-agent completion tracking hooks

## Documentation Patterns

### 1. **Living Documentation Pattern**

**Use Case**: Documentation that stays current with workflow changes

**Template Structure**:

```markdown
# [Document Title]

**Last Updated**: [Auto-updated timestamp]
**Version**: [Semantic version]
**Status**: [Current/Draft/Deprecated]

## Quick Reference

[Essential information for immediate use]

## Detailed Documentation

[Comprehensive information organized by use case]

## Examples

[Practical examples and usage patterns]

## Integration Points

[How this connects to other workflows/documents]

## Change History

[Recent changes and their rationale]
```

**Benefits**:

- Always current information
- Clear change tracking
- Easy navigation
- Integration awareness

### 2. **Progressive Disclosure Pattern**

**Use Case**: Documentation that serves multiple experience levels

**Template Structure**:

```markdown
## Quick Start (New Users)

[Essential commands and immediate actions]

## Standard Usage (Regular Users)

[Common patterns and workflows]

## Advanced Usage (Expert Users)

[Complex scenarios and customization]

## Troubleshooting (All Users)

[Common issues and solutions by symptom]

## Reference (All Users)

[Complete command/API reference]
```

**Benefits**:

- Serves all experience levels
- Reduces cognitive overload
- Clear progression path
- Comprehensive coverage

## Quality Assurance Patterns

### 1. **Multi-Tier Validation Pattern**

**Use Case**: Graduated validation with appropriate time/accuracy tradeoffs

**Pattern Structure**:

```
Quick Validation (30s) → Standard Validation (2min) → Comprehensive Validation (5min)
```

**Implementation Template**:

```bash
# Tier 1: Quick (lint-only)
--lint-only    # Formatting and basic syntax only

# Tier 2: Standard (default)
[no flag]      # Linting + unit tests

# Tier 3: Comprehensive
--full         # All validation including integration tests
```

**Benefits**:

- Appropriate validation for context
- Fast feedback for daily development
- Comprehensive validation for critical changes
- Clear escalation path

### 2. **Artifact Generation Pattern**

**Use Case**: Comprehensive output for review and decision-making

**Template Structure**:

```
Process → Multiple Artifacts → Human Review → Decision
```

**Artifact Types**:

- **Diff Reports**: Comprehensive change analysis
- **AI Review Prompts**: Ready-to-submit review requests
- **Summary Documents**: Consolidated recommendations
- **Validation Reports**: Quality gate results

**Benefits**:

- Complete information for decisions
- Reproducible analysis
- Clear review workflow
- Audit trail

## Anti-Patterns to Avoid

### 1. **Direct Sub-Agent Communication**

**Problem**: Sub-agents calling other sub-agents directly
**Solution**: All communication through orchestrator hub

### 2. **Manual State Synchronization**

**Problem**: Inconsistent state across workflow documents
**Solution**: Automated synchronization with validation

### 3. **Monolithic Commands**

**Problem**: Single commands doing too many unrelated things
**Solution**: Compose smaller, focused commands

### 4. **Implicit Dependencies**

**Problem**: Workflows that depend on undocumented assumptions
**Solution**: Explicit dependency declaration and validation

### 5. **Error Swallowing**

**Problem**: Hiding errors without proper fallback mechanisms
**Solution**: Graceful degradation with clear error reporting

## Pattern Selection Guide

### By Workflow Complexity

#### **Simple Workflows** (Single sub-agent, linear process)

- Use basic command composition pattern
- Minimal validation gates
- Direct output generation

#### **Moderate Workflows** (Multiple sub-agents, some branching)

- Use hub-and-spoke pattern for coordination
- Pipeline pattern for stage progression
- Multi-tier validation for quality

#### **Complex Workflows** (Many sub-agents, complex dependencies)

- Combine hub-and-spoke with pipeline patterns
- Event-driven updates for status tracking
- Research-first pattern for decision support

### By Integration Requirements

#### **Standalone Workflows**

- Focus on command composition patterns
- Minimal external dependencies
- Self-contained validation

#### **Integrated Workflows**

- Observer pattern for cross-system updates
- Progressive documentation for discoverability
- Automated synchronization patterns

#### **Ecosystem Workflows**

- Research-first pattern for best practices
- Living documentation for currency
- Multi-tier validation for reliability

---

## Section Addressing Patterns [NEW - Workflow Agent v1.1.0+]

### 1. **Document Section Targeting Pattern**

**Use Case**: Precise, surgical updates to specific document sections with minimal change footprint

**Pattern Structure**:

```
Operation Input → Section Discovery → Validation → Precise Update → Provenance Tracking
```

**Implementation Template**:

```json
{
  "pattern_name": "section_precision_targeting",
  "section_key_format": "hierarchical.dot.notation[array_key]",
  "examples": {
    "registry_update": "registry.workflows[daily-development].maturity",
    "integration_mapping": "integration_map.edges[planner->development].workflow",
    "usage_guide": "usage_guide.commands[/daily].testing",
    "living_sprint": "living_sprint.developers[human].current_task"
  },
  "validation_steps": [
    "verify_section_exists",
    "check_access_permissions",
    "validate_change_compatibility",
    "generate_rollback_point"
  ]
}
```

**Benefits**:

- Minimal change footprint
- Precise targeting
- Conflict reduction
- Clear rollback capability

### 2. **Machine-Actionable Change Pattern**

**Use Case**: Generating CI/CD compatible document changes with full audit trails

**Pattern Structure**:

```
Change Request → Hash Generation → Patch Creation → Provenance Stamping → Validation
```

**Implementation Template**:

```json
{
  "change_artifact": {
    "path": "[canonical_file_path]",
    "sections": ["[precise_section_keys]"],
    "change_type": "updated|created|synchronized|deprecated",
    "before_hash": "[sha256_of_original]",
    "after_hash": "[sha256_of_modified]",
    "patch": "[unified_diff_or_json_patch]",
    "applied": true,
    "provenance": {
      "agent": "workflow",
      "operation": "[operation_type]",
      "operation_id": "[uuid_or_ulid]",
      "execution_timestamp": "[iso_8601_utc]",
      "inputs_hash": "[sha256_of_inputs]"
    }
  }
}
```

**Benefits**:

- CI/CD integration ready
- Full audit trail
- Rollback capability
- Change verification

### 3. **Idempotent Operation Pattern**

**Use Case**: Preventing duplicate operations and ensuring consistent results for identical inputs

**Pattern Structure**:

```
Input → Hash Generation → Duplicate Check → Operation Execution → Result Caching
```

**Implementation Template**:

```python
def execute_workflow_operation(operation_input):
    # Generate stable input hash
    inputs_hash = hashlib.sha256(
        json.dumps(operation_input, sort_keys=True).encode()
    ).hexdigest()

    # Check for existing operation with same hash
    if operation_exists(operation_input.operation_id, inputs_hash):
        return get_cached_result(operation_input.operation_id)

    # Execute operation
    result = perform_operation(operation_input)

    # Cache result with provenance
    cache_result(operation_input.operation_id, inputs_hash, result)

    return result
```

**Benefits**:

- Duplicate prevention
- Consistent results
- Operation traceability
- Safe retry capability

### 4. **Dry-Run Validation Pattern**

**Use Case**: Safe testing of document changes without file modifications

**Pattern Structure**:

```
Operation → Simulation Mode → Change Generation → Validation → Report (No File Changes)
```

**Implementation Template**:

```json
{
  "dry_run_config": {
    "apply_mode": "dry_run",
    "generate_patches": true,
    "validate_changes": true,
    "simulate_conflicts": true,
    "report_only": true
  },
  "dry_run_output": {
    "changes_simulated": "[number_of_changes]",
    "validation_results": {
      "intent_result_mapping": true,
      "section_precision": true,
      "provenance_completeness": true
    },
    "potential_conflicts": [],
    "estimated_impact": "[low|medium|high]"
  }
}
```

**Benefits**:

- Safe change testing
- Conflict detection
- Impact assessment
- Validation confirmation

## Section Key Reference Patterns

### Registry Documents

```
registry.workflows[<workflow-name>].maturity
registry.workflows[<workflow-name>].capabilities
registry.workflows[<workflow-name>].integration_points
registry.capabilities[<capability>].agents
registry.capabilities[<capability>].maturity_level
```

### Integration Maps

```
integration_map.edges[<from>-><to>].workflow
integration_map.edges[<from>-><to>].data_flow
integration_map.nodes[<agent>].capabilities
integration_map.nodes[<agent>].dependencies
```

### Usage Guides

```
usage_guide.commands[<command>].testing
usage_guide.commands[<command>].examples
usage_guide.workflows[<type>].best_practices
usage_guide.workflows[<type>].common_patterns
```

### Living Sprint Tracking

```
living_sprint.developers[<name>].current_task
living_sprint.developers[<name>].progress_percentage
living_sprint.current_sprint.focus_area
living_sprint.current_sprint.completion_percentage
```

## Enhanced Quality Patterns

### 5. **Intent-Result Validation Pattern**

**Use Case**: Ensuring 1:1 mapping between requested documents and actual changes

**Validation Logic**:

```python
def validate_intent_result_mapping(sync_requirements, cross_document_changes):
    requested_paths = {doc.path for doc in sync_requirements.documents_to_sync}
    changed_paths = {change.path for change in cross_document_changes}

    missing_changes = requested_paths - changed_paths
    unexpected_changes = changed_paths - requested_paths

    return {
        "intent_result_mapping": len(missing_changes) == 0,
        "missing_changes": list(missing_changes),
        "unexpected_changes": list(unexpected_changes),
        "mapping_completeness": len(changed_paths) / len(requested_paths) if requested_paths else 1.0
    }
```

### 6. **Provenance Completeness Pattern**

**Use Case**: Ensuring full audit trail for all document changes

**Validation Requirements**:

- Every change includes operation_id, timestamp, agent, inputs_hash
- All changes traceable to specific operation inputs
- Full rollback capability maintained
- Change history preserved

---

## Examples

**For concrete agent execution examples demonstrating these patterns**, see:

- **`.claude/docs/04-examples/claude-code-agent-flows.md`** - Real-world execution flows including:
  - Success flow: Agent model update with validation
  - Clarification flow: Blocked operations with structured feedback
  - Complete workflow orchestration with quality gates

**These examples show how patterns translate to actual agent operations with input/output contracts and state transitions.**

---

**These enhanced patterns provide the foundation for reliable, traceable, and CI/CD-ready workflow operations with enterprise-grade auditability and consistency.**

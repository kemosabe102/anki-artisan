# Interactive Agent Definition Creation - Quick Reference

**Purpose**: Fast reference card for orchestrators implementing the interactive workflow.

**Full Spec**: `.claude/docs/guides/interactive-agent-definition-workflow.md`

---

## Command Signature

```bash
/create-agent --create-definition output.md [--context-dir=path] [--dry-run]
```

**New Flag**: `--create-definition` triggers interactive mode (5 phases) before standard workflow.

---

## 5-Phase Quick Reference

| Phase           | Actor           | Time    | Key Actions                                          |
| --------------- | --------------- | ------- | ---------------------------------------------------- |
| **1. Capture**  | Orchestrator    | 1-2 min | Prompt user for 2-3 sentence idea                    |
| **2. Analyze**  | claude-code-ecosystem | 15 sec  | Generate structured proposal with confidence scores  |
| **3. Refine**   | Orchestrator    | 3-5 min | Walk through Q&A for each section (10 sections)      |
| **4. Generate** | claude-code-ecosystem | 10 sec  | Create definition file from refined requirements     |
| **5. Present**  | Orchestrator    | 1 min   | Show preview, offer 3 options (proceed/review/regen) |

**Total**: 5-10 minutes

---

## Phase 1: Capture User Idea

**Prompt Template**:

```
Let's create your agent definition together!

Please describe your agent idea in 2-3 sentences:
1. What problem does it solve?
2. What does it do?
3. When would the orchestrator call it?

Example: "I want an agent that scans code for security vulnerabilities
using Semgrep. It should run before commits and catch SQL injection."

Your idea:
```

**Validation**: Reject if too vague (<20 words or no clear action verb). Max 3 retries.

**Output**: `user_idea_text`

---

## Phase 2: Analyze Idea & Propose Structure

**Delegation**:

```python
Task(subagent_type="claude-code-ecosystem", prompt=f"""
ANALYZE AGENT IDEA and propose structured agent definition.

User Idea:
\"\"\"{user_idea_text}\"\"\"

Generate proposed agent structure with confidence-scored recommendations:
1. Agent name options (2-3 with confidence + rationale)
2. Domain scope (recommendation + rationale)
3. Agent type (Creator/Reviewer/Enhancer/Runner/Analyzer/Planner)
4. Purpose statement (1-2 sentences for orchestrator)
5. Core capabilities (4-6 specific items)
6. Expected inputs (with types + validation)
7. Expected outputs (SUCCESS + FAILURE states)
8. Domain knowledge areas (confidence scored, High/Medium/Low priority)
9. Tool recommendations (confidence + rationale)
10. Integration points (agents, triggers, dependencies)

Return structured proposal with confidence scores (0.0-1.0) for each recommendation.
Make implicit assumptions explicit. Provide rationale for all recommendations.
""")
```

**New Operation**: `analyze_agent_idea`

**Expected Output**: `agent_proposal` (JSON with 10 sections, all scored)

**Error Handling**: If FAILURE, extract `missing_information` and re-prompt user.

---

## Phase 3: Interactive Refinement

**Q&A Pattern for Each Section**:

### Section: Agent Name

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT NAME OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. {name_1} (confidence: {conf_1})
   Rationale: {rationale_1}

2. {name_2} (confidence: {conf_2})
   Rationale: {rationale_2}

3. {name_3} (confidence: {conf_3})
   Rationale: {rationale_3}

Which name do you prefer?
(Type 1, 2, or 3, or provide your own name)

>
```

**Store**: `refined_requirements['name']`

---

### Section: Domain Scope

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAIN SCOPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation: {domain}
Confidence: {confidence}
Rationale: {rationale}

Read Access: {read_paths}
Write Access: {write_paths}

Is this correct?
(Type 'y' for yes, 'n' to specify different scope)

>
```

**Store**: `refined_requirements['domain']`, `read_access`, `write_access`

---

### Section: Agent Type

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT TYPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation: {type}
Confidence: {confidence}
Rationale: {rationale}

Is this correct?
(Type 'y' for yes, 'n' to specify different type)

>
```

**Store**: `refined_requirements['type']`

---

### Section: Purpose (Orchestrator Description)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PURPOSE (ORCHESTRATOR DESCRIPTION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"{purpose_text}"

Is this accurate?
(Type 'y' for yes, or provide your improved version)

>
```

**Store**: `refined_requirements['purpose']`

---

### Section: Core Capabilities (List)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE CAPABILITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. {capability_1}
2. {capability_2}
3. {capability_3}
4. {capability_4}

Are these correct?
(Type 'y' for yes, 'a' to add, 'r' to remove, 'e' to edit)

>
```

**If 'a' (add)**:

```
What capability would you like to add?

> {user_input}

Added: "{user_input}"

Updated capabilities:
1. ...
2. ...
N. {user_input}

Any more changes? (y/a/r/e)
```

**If 'r' (remove)**:

```
Which capability number to remove? (1-N)

> {number}

Removed: "{capability_N}"

Updated capabilities:
1. ...
...

Any more changes? (y/a/r/e)
```

**If 'e' (edit)**:

```
Which capability number to edit? (1-N)

> {number}

Current: "{capability_N}"
New version:

> {user_input}

Updated capabilities:
1. ...
N. {user_input}
...

Any more changes? (y/a/r/e)
```

**Store**: `refined_requirements['capabilities']`

---

**Repeat for**:

- Expected Inputs (list with add/remove/edit)
- Expected Outputs (SUCCESS + FAILURE descriptions)
- Domain Knowledge Areas (list with add/remove/edit)
- Tool Recommendations (list with add/remove/edit)
- Integration Points (description text)

**Output**: `refined_requirements` (complete dict)

---

## Phase 4: Generate Definition File

**Delegation**:

```python
Task(subagent_type="claude-code-ecosystem", prompt=f"""
GENERATE AGENT DEFINITION FILE from structured requirements.

Requirements (refined with user feedback):
{json.dumps(refined_requirements, indent=2)}

Output Path: {output_path}
Template: .claude/templates/agent-definition-input.template.md

Instructions:
1. Use template structure exactly
2. Fill ALL sections completely with refined requirements
3. Include confidence scores where provided
4. Add clear examples and context
5. Make all implicit context explicit
6. Include user's original idea in comments for reference

Generate complete agent definition file following template.
Include rationale and examples to help user understand definition.
""")
```

**New Operation**: `generate_agent_definition`

**Expected Output**: Definition file created at `output_path`

**Error Handling**:

- FAILURE → Show `failure_details.reasons`
- Offer: Retry (attempt 2-3), Return to Phase 3, or Cancel

---

## Phase 5: Present Completion & Options

**Completion Template**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT DEFINITION CREATED SUCCESSFULLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: {output_path}

Agent: {agent_name}
Type: {agent_type}
Domain: {domain_scope}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The definition file is ready for agent creation. The full workflow will:

1. Research domain knowledge (automatically)
2. Generate agent and schema files
3. Create AI-readable documentation
4. Validate quality (9-dimensional matrix)
5. Update integration points

Estimated time: 10-15 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREVIEW YOUR DEFINITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{first_30_lines}

[... file continues with {remaining_lines} more lines ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Proceed with agent creation NOW (run /create-agent automatically)
2. Review/edit definition first (stop here, manual /create-agent later)
3. Regenerate definition with different answers

(Type 1, 2, or 3)

>
```

**User Choice Handling**:

### Option 1: Proceed Immediately

```python
# User chose to continue immediately
print("Starting agent creation workflow...")
print("This will take approximately 10-15 minutes.")

# Execute standard 10-phase workflow
execute_create_agent_workflow(definition_file=output_path)
```

### Option 2: Review First

```python
# User chose to review/edit first
print(f"""
Definition saved to: {output_path}

Review and edit the file as needed, then run:

    /create-agent {output_path}

when you're ready to proceed with agent creation.
""")

# Command completes successfully
return SUCCESS
```

### Option 3: Regenerate

```python
# User wants to refine with different answers
print("Let's refine your agent definition...")
print("I'll walk you through the sections again.")

# Loop back to Phase 3 with same proposal
# User can provide different answers this time
return run_phase_3_refinement(agent_proposal)
```

---

## Error Handling Quick Reference

| Error               | Phase | Recovery                                           |
| ------------------- | ----- | -------------------------------------------------- |
| Vague idea          | 1     | Re-prompt (max 3), then suggest manual template    |
| Analysis failure    | 2     | Extract `missing_information`, re-prompt user      |
| Invalid name format | 3     | Validate pattern `^[a-z][a-z0-9-]*$`, re-prompt    |
| Generation failure  | 4     | Retry (2-3 attempts), return to Phase 3, or cancel |
| File exists         | 4     | Offer overwrite, rename, or cancel                 |
| Permission error    | 4     | Request new writable path or cancel                |

---

## Integration with Standard Workflow

```python
def execute_create_agent_command(args):
    """Handle both interactive and standard modes."""

    # Check for interactive mode flag
    if args.get('--create-definition'):
        output_path = args['--create-definition']

        # Run interactive workflow (Phases 1-5)
        result = run_interactive_workflow(output_path)

        # Handle user choice from Phase 5
        if result.user_choice == "proceed_immediately":
            definition_file = output_path
            # Fall through to standard workflow below

        elif result.user_choice == "review_first":
            return SUCCESS  # Exit

        elif result.user_choice == "regenerate":
            return SUCCESS  # Already handled by loop

    else:
        # Standard mode: definition file provided
        definition_file = args['agent-definition-file']

    # Execute standard 10-phase workflow
    return execute_standard_workflow(definition_file, **args)
```

---

## claude-code-ecosystem Schema Updates

**Add to `operation_type` enum**:

```json
{
  "operation_type": {
    "enum": [
      "create_agent",
      "evaluate_agent",
      "implement_feedback",
      "update_agent",
      "create_design_guide",
      "validate_workflow",
      "update_maturity",
      "analyze_agent_idea", // NEW
      "generate_agent_definition" // NEW
    ]
  }
}
```

**New Input Structures**: See `.claude/docs/schemas/claude-code-ecosystem.schema.json` for complete schemas.

---

## Time Estimates

| Activity                        | Time             |
| ------------------------------- | ---------------- |
| Interactive Mode (Phases 1-5)   | 5-10 min         |
| Standard Workflow (Phases 1-10) | 10-15 min        |
| **Total (end-to-end)**          | **15-25 min**    |
| Manual Template Filling         | 30-60 min        |
| **Time Savings**                | **5-10x faster** |

---

## Success Metrics

| Metric                  | Target   | Manual Comparison |
| ----------------------- | -------- | ----------------- |
| Definition Time         | 5-10 min | 30-60 min         |
| Template Compliance     | 100%     | ~70%              |
| User Expertise Required | None     | High              |
| Error Rate              | <1%      | ~30%              |

---

## Related Documentation

- **Full Workflow Spec**: `.claude/docs/03-workflows/interactive-agent-definition-workflow.md`
- **Input Template**: `.claude/templates/agent-definition-input.template.md`
- **Command File**: `.claude/commands/create-agent.md`

> **Note**: Workflow diagrams archived to `.claude/docs/archive/cleanup-2025-12-01/`

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-22
**Status**: Ready for Implementation

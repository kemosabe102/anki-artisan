---
title: "Interactive Agent Definition Creation Workflow"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Interactive Agent Definition Creation Workflow

**Purpose**: Enable users to create agent definitions interactively through `/create-agent --create-definition output.md` command, guiding them from a simple idea to a complete agent definition file ready for automated generation.

**Design Philosophy**: Conversational guidance with progressive refinement, automated research integration, and immediate execution options.

---

## Overview

This workflow enables users to create agent definitions WITHOUT needing to understand the complete template structure upfront. Instead, the orchestrator guides them through a series of focused questions, delegates analysis to claude-code-ecosystem, and produces a complete agent definition file ready for the full 10-phase agent creation workflow.

**Key Benefits**:

- No need to study template structure beforehand
- Interactive Q&A format with immediate feedback
- Automated proposal generation based on user's idea
- Progressive refinement with confidence scoring
- Option to proceed immediately to agent creation or review/edit first

---

## Command Signature

### Updated Arguments

```yaml
arguments:
  - name: agent-definition-file
    description: Path to agent definition file (optional if using --create-definition)
    required: false # Changed from true
    type: path

  - name: --create-definition
    description: Interactive mode to create agent definition from idea (output path required)
    required: false
    type: path
    example: /create-agent --create-definition my-agent-definition.md

  - name: --context-dir
    description: Directory containing additional context files
    required: false
    type: path

  - name: --dry-run
    description: Preview agent without writing files
    required: false
    type: flag

  - name: --skip-validation
    description: Skip quality matrix validation (rapid prototyping)
    required: false
    type: flag

  - name: --template
    description: Token budget control (minimal|standard|comprehensive)
    required: false
    type: enum
    default: standard
```

### Usage Examples

```bash
# Interactive definition creation only
/create-agent --create-definition my-agent-definition.md

# Create agent from existing definition (current behavior)
/create-agent my-agent-definition.md

# Interactive creation with immediate execution (user chooses option 1)
/create-agent --create-definition my-agent-definition.md
# (After completion, user selects option 1 to proceed immediately)

# Interactive with dry-run preview
/create-agent --create-definition my-agent-definition.md --dry-run
```

---

## Workflow Phases (5 Phases)

### Phase 1: Capture User Idea

**Goal**: Extract the core agent concept from user in 2-3 sentences without overwhelming them with template complexity.

**Orchestrator Actions**:

1. **Present Friendly Prompt**:

```
Let's create your agent definition together!

Please describe your agent idea in 2-3 sentences:

1. What problem does it solve?
2. What does it do?
3. When would the orchestrator call it?

Example: "I want an agent that scans code for security vulnerabilities using Semgrep. It should integrate with the git workflow and run before commits to catch issues early."

Your idea:
```

2. **Collect User Response**:
   - User provides their 2-3 sentence description
   - Capture as `user_idea_text`

3. **Acknowledge and Proceed**:

   ```
   Got it! Analyzing your idea and proposing agent structure...
   ```

4. **Transition to Phase 2**: Immediately delegate to claude-code-ecosystem

**Success Criteria**:

- User provides at least 2 sentences describing their agent idea
- Idea includes problem statement and high-level approach
- Description is concrete enough to analyze (not "make things better")

---

### Phase 2: Analyze Idea & Propose Structure

**Goal**: Transform user's informal idea into a structured agent proposal with confidence-scored recommendations.

**Orchestrator Actions**:

1. **Delegate to claude-code-ecosystem for Analysis**:

```python
Task(subagent_type="claude-code-ecosystem", prompt="""
ANALYZE AGENT IDEA and propose structured agent definition.

User Idea:
\"\"\"
{user_idea_text}
\"\"\"

Generate proposed agent structure with confidence-scored recommendations:

1. **Agent Name Options** (provide 2-3 options with confidence and rationale):
   - Suggest names following [domain]-[action] pattern
   - Explain why each name fits the idea
   - Score confidence (0.0-1.0) based on clarity and conventions

2. **Domain Scope** (determine which directories this agent operates on):
   - Options: .claude/**, packages/**, docs/**, tests/**, cross-domain
   - Provide confidence score and rationale for recommendation
   - Identify read/write boundaries

3. **Agent Type** (Creator/Reviewer/Enhancer/Runner/Analyzer/Planner):
   - Determine primary work pattern from idea
   - Confidence score and rationale

4. **Purpose Statement** (orchestrator description):
   - Draft 1-2 sentence description for when orchestrator should call this agent
   - Include trigger conditions and context signals

5. **Core Capabilities** (4-6 specific, actionable capabilities):
   - Extract from user idea and expand with domain expertise
   - Each capability should be concrete and testable

6. **Expected Inputs** (required data for operation):
   - Infer from capabilities and purpose
   - Suggest data types and validation rules

7. **Expected Outputs** (SUCCESS and FAILURE states):
   - Define deliverables on success
   - Define error information on failure

8. **Domain Knowledge Areas** (frameworks, standards, methodologies):
   - Identify knowledge requirements with confidence scores (0.0-1.0)
   - Categorize as High (≥0.8), Medium (0.5-0.79), Low (<0.5) priority

9. **Tool Recommendations** (Claude Code tools needed):
   - Suggest tools with confidence scores and rationale
   - Available: Read, Write, Edit, Glob, Grep, Bash, WebFetch, Task

10. **Integration Points** (workflow coordination):
    - Identify which existing agents this coordinates with
    - Determine trigger conditions and dependencies

Return structured proposal with confidence scores for each recommendation.

Focus on clarity and actionable recommendations. Make implicit assumptions explicit.
Include rationale for each recommendation so user understands the reasoning.
""")
```

2. **Receive Proposal**:
   - Agent-architect returns structured proposal with confidence scores
   - Store proposal as `agent_proposal`

3. **Transition to Phase 3**: Present proposal to user for refinement

**Success Criteria**:

- Agent-architect returns complete proposal with all 10 sections
- All recommendations include confidence scores (0.0-1.0)
- Rationale provided for non-obvious recommendations
- Proposal is actionable (user can say yes/no without research)

---

### Phase 3: Interactive Refinement

**Goal**: Walk user through each section of the proposal, allowing them to accept, modify, or provide additional context.

**Orchestrator Actions**:

1. **Present Proposal Section-by-Section**:

```
Based on your idea, here's what I propose:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT NAME OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. {name_option_1} (confidence: {confidence_1})
   Rationale: {rationale_1}

2. {name_option_2} (confidence: {confidence_2})
   Rationale: {rationale_2}

3. {name_option_3} (confidence: {confidence_3})
   Rationale: {rationale_3}

Which name do you prefer?
(Type 1, 2, or 3, or provide your own name)

>
```

2. **Collect User Response**: Store as `selected_name`

3. **Continue with Domain Scope**:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAIN SCOPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation: {proposed_scope}
Confidence: {confidence}
Rationale: {rationale}

Read Access: {read_paths}
Write Access: {write_paths}

Is this correct?
(Type 'y' for yes, 'n' to specify different scope)

>
```

4. **Repeat for Each Section**:
   - Agent Type
   - Purpose (orchestrator description)
   - Core Capabilities
   - Expected Inputs
   - Expected Outputs
   - Domain Knowledge Areas
   - Tool Recommendations
   - Integration Points

5. **Section-Specific Interaction Patterns**:

**For Lists (Capabilities, Inputs, Outputs, Knowledge, Tools)**:

```
Are these correct?
(Type 'y' for yes, 'a' to add items, 'r' to remove items, 'e' to edit)

>
```

**For Text (Purpose, Rationale)**:

```
Is this accurate?
(Type 'y' for yes, or provide your improved version)

>
```

6. **Build Refined Requirements**:
   - Store all user selections and modifications
   - Accumulate as `refined_requirements`

7. **Transition to Phase 4**: Generate definition file with refinements

**Success Criteria**:

- User has reviewed and approved/modified all 10 proposal sections
- All required fields have user-confirmed values
- User understands what each section means (no confusion)
- Refined requirements ready for file generation

---

### Phase 4: Generate Definition File

**Goal**: Create a complete agent definition file from refined requirements using the official template.

**Orchestrator Actions**:

1. **Delegate to claude-code-ecosystem for Generation**:

```python
Task(subagent_type="claude-code-ecosystem", prompt="""
GENERATE AGENT DEFINITION FILE from structured requirements.

Requirements (refined with user feedback):

**Agent Name**: {refined_requirements.name}

**Domain Scope**: {refined_requirements.domain}
- Read Access: {refined_requirements.read_access}
- Write Access: {refined_requirements.write_access}

**Agent Type**: {refined_requirements.type}

**Purpose** (Orchestrator Description):
{refined_requirements.purpose}

**Core Capabilities**:
{refined_requirements.capabilities}

**Expected Inputs**:
{refined_requirements.inputs}

**Expected Outputs**:
- SUCCESS: {refined_requirements.success_output}
- FAILURE: {refined_requirements.failure_output}

**Domain Knowledge Areas** (with confidence scores):
{refined_requirements.knowledge_areas}

**Tool Requirements** (with confidence and rationale):
{refined_requirements.tools}

**Integration Points**:
{refined_requirements.integration_points}

**Instructions**:
1. Use template: .claude/templates/agent-definition-input.template.md
2. Fill ALL sections completely with refined requirements
3. Include confidence scores where provided
4. Add clear examples and context where helpful
5. Follow template structure exactly
6. Include user's original idea in comments for reference
7. Make all implicit context explicit

Output file path: {output_path}

Generate complete agent definition file following template structure.
Include rationale and examples to help user understand the definition.
""")
```

2. **Receive Generated File**:
   - Agent-architect creates definition file at specified path
   - Returns confirmation and file preview (first 30 lines)

3. **Transition to Phase 5**: Present completion options

**Success Criteria**:

- Definition file created at user-specified path
- File follows template structure completely
- All sections filled with refined requirements
- File is valid and ready for /create-agent execution

---

### Phase 5: Present Completion & Options

**Goal**: Provide user with clear next steps and options to proceed immediately or review/edit first.

**Orchestrator Actions**:

1. **Present Completion Summary**:

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

{first_30_lines_of_file}

[... file continues with {remaining_line_count} more lines ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Proceed with agent creation NOW (run /create-agent automatically)
2. Review/edit definition first (stop here, manual /create-agent later)
3. Regenerate definition with different answers

(Type 1, 2, or 3)

>
```

2. **Handle User Choice**:

**Option 1: Proceed Immediately**:

```python
# Orchestrator automatically runs full agent creation workflow
# Equivalent to: /create-agent {output_path}

# Present transition message:
print("Starting agent creation workflow...")
print("This will take approximately 10-15 minutes.")

# Delegate to existing 10-phase workflow (Phase 1-10 from create-agent command)
execute_create_agent_workflow(definition_file=output_path)
```

**Option 2: Stop for Review**:

```python
# Present final message:
print(f"""
Definition saved to: {output_path}

Review and edit the file as needed, then run:

    /create-agent {output_path}

when you're ready to proceed with agent creation.
""")

# Command completes successfully
```

**Option 3: Regenerate**:

```python
# Return to Phase 3 (Interactive Refinement)
# Present same proposal sections again
# User can provide different answers

print("Let's refine your agent definition...")
print("I'll walk you through the sections again.")

# Re-run Phase 3 with same proposal (or re-analyze if user wants to change idea)
```

3. **Command Completion**:
   - If Option 1: Continue to full 10-phase workflow
   - If Option 2: Exit successfully with file path
   - If Option 3: Loop back to Phase 3

**Success Criteria**:

- User has clear understanding of what was created
- User knows their next steps (review, run, or regenerate)
- File path is clearly communicated
- Option to proceed immediately is available

---

## Agent Delegation Summary

| Phase        | Task                     | Agent                      | Rationale                                 |
| ------------ | ------------------------ | -------------------------- | ----------------------------------------- |
| 1            | Capture user idea        | Orchestrator               | Simple text collection, no delegation     |
| 2            | Analyze idea             | claude-code-ecosystem            | Agent expertise, structured analysis      |
| 2            | Propose structure        | claude-code-ecosystem            | Agent design patterns, confidence scoring |
| 3            | Interactive refinement   | Orchestrator               | User interaction, choice collection       |
| 4            | Generate definition file | claude-code-ecosystem            | Template application, file generation     |
| 5            | Present completion       | Orchestrator               | User communication, option handling       |
| 5 (Option 1) | Execute creation         | Existing 10-phase workflow | Full agent creation pipeline              |

**Key Principle**: Orchestrator handles user interaction and coordination. claude-code-ecosystem handles all agent-specific analysis, design, and generation work.

---

## Schema Updates

### claude-code-ecosystem.schema.json

**New Operations to Add**:

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
      "analyze_agent_idea", // NEW - Phase 2
      "generate_agent_definition" // NEW - Phase 4
    ]
  }
}
```

**New Input Structure for `analyze_agent_idea`**:

```json
{
  "agent_idea_analysis": {
    "type": "object",
    "description": "User idea analysis request (analyze_agent_idea operation)",
    "properties": {
      "user_idea_text": {
        "type": "string",
        "description": "User's 2-3 sentence description of their agent idea"
      },
      "analysis_depth": {
        "enum": ["quick", "comprehensive"],
        "default": "comprehensive",
        "description": "How deep to analyze (quick = essential only, comprehensive = full proposal)"
      }
    },
    "required": ["user_idea_text"]
  }
}
```

**New Output Structure for `analyze_agent_idea`**:

```json
{
  "agent_idea_proposal": {
    "type": "object",
    "description": "Structured agent proposal from user idea",
    "properties": {
      "name_options": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string", "pattern": "^[a-z][a-z0-9-]*[a-z0-9]$" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
            "rationale": { "type": "string" }
          },
          "required": ["name", "confidence", "rationale"]
        },
        "minItems": 2,
        "maxItems": 3
      },
      "domain_scope": {
        "type": "object",
        "properties": {
          "recommendation": {
            "enum": [".claude/**", "packages/**", "docs/**", "tests/**", "cross-domain"]
          },
          "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
          "rationale": { "type": "string" },
          "read_access": { "type": "array", "items": { "type": "string" } },
          "write_access": { "type": "array", "items": { "type": "string" } }
        },
        "required": ["recommendation", "confidence", "rationale"]
      },
      "agent_type": {
        "type": "object",
        "properties": {
          "recommendation": {
            "enum": ["Creator", "Reviewer", "Enhancer", "Runner", "Analyzer", "Planner"]
          },
          "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
          "rationale": { "type": "string" }
        },
        "required": ["recommendation", "confidence", "rationale"]
      },
      "purpose_statement": {
        "type": "string",
        "description": "1-2 sentence orchestrator description with trigger conditions"
      },
      "capabilities": {
        "type": "array",
        "items": { "type": "string" },
        "minItems": 4,
        "maxItems": 6,
        "description": "Specific, actionable capabilities extracted from idea"
      },
      "expected_inputs": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "field_name": { "type": "string" },
            "description": { "type": "string" },
            "data_type": { "type": "string" },
            "validation": { "type": "string" }
          },
          "required": ["field_name", "description", "data_type"]
        }
      },
      "expected_outputs": {
        "type": "object",
        "properties": {
          "success": {
            "type": "string",
            "description": "What agent delivers on SUCCESS"
          },
          "failure": {
            "type": "string",
            "description": "What agent provides on FAILURE"
          }
        },
        "required": ["success", "failure"]
      },
      "knowledge_areas": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "topic": { "type": "string" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
            "priority": { "enum": ["High", "Medium", "Low"] },
            "rationale": { "type": "string" }
          },
          "required": ["topic", "confidence", "priority", "rationale"]
        }
      },
      "tool_recommendations": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "tool": {
              "enum": ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebFetch", "Task"]
            },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
            "rationale": { "type": "string" }
          },
          "required": ["tool", "confidence", "rationale"]
        }
      },
      "integration_points": {
        "type": "object",
        "properties": {
          "coordinates_with": { "type": "array", "items": { "type": "string" } },
          "trigger_conditions": { "type": "array", "items": { "type": "string" } },
          "dependencies": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    "required": [
      "name_options",
      "domain_scope",
      "agent_type",
      "purpose_statement",
      "capabilities",
      "expected_inputs",
      "expected_outputs",
      "knowledge_areas",
      "tool_recommendations",
      "integration_points"
    ]
  }
}
```

**New Input Structure for `generate_agent_definition`**:

```json
{
  "definition_generation": {
    "type": "object",
    "description": "Agent definition file generation request (generate_agent_definition operation)",
    "properties": {
      "output_path": {
        "type": "string",
        "description": "Absolute path where definition file should be written"
      },
      "refined_requirements": {
        "type": "object",
        "description": "User-refined requirements from interactive session",
        "properties": {
          "name": { "type": "string" },
          "domain": { "type": "string" },
          "type": {
            "enum": ["Creator", "Reviewer", "Enhancer", "Runner", "Analyzer", "Planner"]
          },
          "purpose": { "type": "string" },
          "capabilities": { "type": "array", "items": { "type": "string" } },
          "inputs": { "type": "array", "items": { "type": "object" } },
          "success_output": { "type": "string" },
          "failure_output": { "type": "string" },
          "knowledge_areas": { "type": "array", "items": { "type": "object" } },
          "tools": { "type": "array", "items": { "type": "object" } },
          "integration_points": { "type": "object" },
          "original_idea": {
            "type": "string",
            "description": "User's original 2-3 sentence idea for reference"
          }
        },
        "required": [
          "name",
          "domain",
          "type",
          "purpose",
          "capabilities",
          "inputs",
          "success_output",
          "failure_output"
        ]
      }
    },
    "required": ["output_path", "refined_requirements"]
  }
}
```

---

## Example Q&A Flow

### Complete Example Session

**User runs**: `/create-agent --create-definition security-scanner-definition.md`

**Phase 1: Capture Idea**

```
Orchestrator:
Let's create your agent definition together!

Please describe your agent idea in 2-3 sentences:
1. What problem does it solve?
2. What does it do?
3. When would the orchestrator call it?

Your idea:

User:
I want an agent that scans Python code for security vulnerabilities using Semgrep. It should run automatically before commits and catch common issues like SQL injection and XSS.

Orchestrator:
Got it! Analyzing your idea and proposing agent structure...
```

**Phase 2: Analyze Idea** (claude-code-ecosystem works)

```
Orchestrator:
[claude-code-ecosystem analyzes idea for 10-15 seconds]

Analysis complete! Here's my proposal...
```

**Phase 3: Interactive Refinement**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT NAME OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. security-scanner (confidence: 0.95)
   Rationale: Clear domain (security) + action (scanner). Follows pattern of existing agents like code-quality, test-runner.

2. sast-analyzer (confidence: 0.80)
   Rationale: Uses industry term SAST (Static Application Security Testing). More technical but less immediately clear.

3. vulnerability-detector (confidence: 0.70)
   Rationale: Descriptive but slightly verbose. Detector is less common than scanner in our agent ecosystem.

Which name do you prefer?
(Type 1, 2, or 3, or provide your own name)

User:
1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DOMAIN SCOPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation: packages/** (main codebase)
Confidence: 0.95
Rationale: Semgrep scans Python code, which lives in packages/. Security scans shouldn't modify code (read-only on packages/**), but will write reports to docs/security/.

Read Access: packages/**, tests/** (for context)
Write Access: docs/security/** (for reports)

Is this correct?
(Type 'y' for yes, 'n' to specify different scope)

User:
y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT TYPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommendation: Analyzer
Confidence: 0.90
Rationale: Analyzes code and reports findings without modifying it. Distinct from Reviewer (which validates quality/style) and Runner (which executes tests/builds).

Is this correct?
(Type 'y' for yes, 'n' to specify different type)

User:
y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PURPOSE (ORCHESTRATOR DESCRIPTION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Performs static application security testing (SAST) on modified Python code using Semgrep to detect OWASP Top 10 vulnerabilities before commit. Integrates with git workflow as a parallel quality gate alongside code-quality. Triggers automatically when files in packages/** are modified."

Is this accurate?
(Type 'y' for yes, or provide your improved version)

User:
y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE CAPABILITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Scans Python code for SQL injection vulnerabilities using Semgrep OWASP ruleset
2. Detects insecure deserialization patterns and command injection risks
3. Validates authentication/authorization implementation against OWASP guidelines
4. Generates security reports with severity scoring (Critical/High/Medium/Low) and remediation steps
5. Integrates with pre-commit workflow as validation gate (blocks commit on Critical findings)

Are these correct?
(Type 'y' for yes, 'a' to add items, 'r' to remove items, 'e' to edit)

User:
a

What capability would you like to add?

User:
Detects hardcoded secrets and credentials in code

Added: "Detects hardcoded secrets and credentials in code"

Updated capabilities:
1. Scans Python code for SQL injection vulnerabilities using Semgrep OWASP ruleset
2. Detects insecure deserialization patterns and command injection risks
3. Validates authentication/authorization implementation against OWASP guidelines
4. Detects hardcoded secrets and credentials in code
5. Generates security reports with severity scoring (Critical/High/Medium/Low) and remediation steps
6. Integrates with pre-commit workflow as validation gate (blocks commit on Critical findings)

Any more changes?
(Type 'y' to continue, 'a' to add more, 'r' to remove, 'e' to edit)

User:
y

[... continues through remaining sections: Inputs, Outputs, Knowledge Areas, Tools, Integration ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REFINEMENT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All sections reviewed! Generating your agent definition file...
```

**Phase 4: Generate Definition File** (claude-code-ecosystem works)

```
Orchestrator:
[claude-code-ecosystem generates definition file for 5-10 seconds]

Definition file created successfully!
```

**Phase 5: Present Completion**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AGENT DEFINITION CREATED SUCCESSFULLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

File: security-scanner-definition.md

Agent: security-scanner
Type: Analyzer
Domain: packages/** (main codebase)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The definition file is ready for agent creation. The full workflow will:

1. Research domain knowledge (OWASP patterns, Semgrep usage)
2. Generate agent and schema files
3. Create AI-readable documentation
4. Validate quality (9-dimensional matrix)
5. Update integration points

Estimated time: 10-15 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PREVIEW YOUR DEFINITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Agent Definition Input Template

## 1. Basic Information

### Agent Name
**Name**: security-scanner

### Domain Scope
**Selected**: packages/**

**Directory Boundaries**:
- Read access: packages/**, tests/**
- Write access: docs/security/**
- Forbidden paths: .env, secrets/, credentials/

### Agent Type
**Selected**: Analyzer

[... file continues with 625 more lines ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WHAT WOULD YOU LIKE TO DO?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Proceed with agent creation NOW (run /create-agent automatically)
2. Review/edit definition first (stop here, manual /create-agent later)
3. Regenerate definition with different answers

(Type 1, 2, or 3)

User:
1

Orchestrator:
Starting agent creation workflow...
This will take approximately 10-15 minutes.

[Proceeds to existing 10-phase workflow from /create-agent command]

Phase 1: Parse agent definition & validate preconditions...
```

---

## Integration with Existing Workflow

### Command Logic Flow

```python
def execute_create_agent_command(args):
    """
    Main command execution logic with interactive mode support.
    """

    # Check if interactive mode requested
    if args.get('--create-definition'):
        output_path = args['--create-definition']

        # Execute interactive workflow (Phases 1-5)
        result = run_interactive_definition_workflow(output_path)

        if result.user_choice == "proceed_immediately":
            # User chose option 1: proceed with agent creation
            definition_file = output_path
            # Fall through to standard workflow below

        elif result.user_choice == "review_first":
            # User chose option 2: stop for review
            print(f"Definition saved to: {output_path}")
            print(f"Run '/create-agent {output_path}' when ready.")
            return SUCCESS

        elif result.user_choice == "regenerate":
            # User chose option 3: already handled by interactive workflow loop
            return SUCCESS

    else:
        # Standard mode: user provided definition file
        definition_file = args['agent-definition-file']

        if not definition_file:
            raise ValueError("Either agent-definition-file or --create-definition must be provided")

    # Execute standard 10-phase workflow
    # (Existing Phase 1-10 logic from /create-agent command)
    return execute_standard_workflow(
        definition_file=definition_file,
        context_dir=args.get('--context-dir'),
        dry_run=args.get('--dry-run', False),
        skip_validation=args.get('--skip-validation', False),
        template=args.get('--template', 'standard')
    )
```

### Workflow State Management

The interactive workflow maintains state for potential retries and regeneration:

```python
class InteractiveWorkflowState:
    """
    State container for interactive agent definition workflow.
    """

    def __init__(self):
        self.output_path = None
        self.user_idea_text = None
        self.agent_proposal = None
        self.refined_requirements = {}
        self.current_phase = 1
        self.iteration_count = 0

    def save_checkpoint(self):
        """Save state for potential resume after errors."""
        pass

    def load_checkpoint(self):
        """Restore state after error recovery."""
        pass
```

---

## Error Handling & Edge Cases

### User Input Validation

**Phase 1 - Idea Too Vague**:

```
User: "Make security better"

Orchestrator:
I need a bit more detail to create an effective agent!

Please describe:
1. WHAT specifically should it do? (scan code? review configs? monitor logs?)
2. HOW should it work? (what tools or methods?)
3. WHEN should it run? (before commits? on schedule? manually?)

Try again:
```

**Phase 3 - Invalid Name Format**:

```
User: "Security Scanner Agent"

Orchestrator:
Agent names must follow [domain]-[action] format in lowercase with hyphens only.

Examples: security-scanner, code-quality, test-runner

Please provide a valid name:
```

### claude-code-ecosystem Failures

**Analysis Failure (Phase 2)**:

```
If claude-code-ecosystem returns FAILURE:

Orchestrator:
I'm having trouble analyzing your idea. Let me try to understand it better.

Could you elaborate on:
- {specific_missing_information from failure_details}

Or would you like to:
1. Rephrase your idea differently
2. Cancel and try later
```

**Generation Failure (Phase 4)**:

```
If claude-code-ecosystem returns FAILURE:

Orchestrator:
I encountered an issue generating the definition file:

{failure_details.reasons[0]}

What would you like to do?
1. Retry generation with current requirements
2. Go back and refine requirements (return to Phase 3)
3. Cancel workflow
```

### File System Errors

**Output Path Already Exists**:

```
Orchestrator:
File already exists: {output_path}

What would you like to do?
1. Overwrite existing file
2. Choose a different output path
3. Cancel workflow
```

**Write Permission Error**:

```
Orchestrator:
Unable to write to: {output_path}

Error: {permission_error_details}

Please provide a writable path or cancel:
```

---

## Success Metrics

### Time Efficiency

- **Target**: 5-10 minutes for interactive definition creation (Phases 1-5)
- **Comparison**: 30-60 minutes to manually fill out complete template
- **Improvement**: 5-10x faster than manual approach

### Quality Consistency

- **Structured Validation**: All required fields enforced through interactive prompts
- **Confidence Scoring**: Agent-architect provides confidence for recommendations (helps user make informed decisions)
- **Template Compliance**: Generated file guaranteed to follow template structure

### User Experience

- **Low Barrier**: User needs only 2-3 sentence idea to start
- **Progressive Disclosure**: Complex template structure revealed gradually through Q&A
- **Clear Guidance**: Rationale provided for all recommendations (no "magic" decisions)
- **Flexible Workflow**: Option to review/edit before agent creation OR proceed immediately

---

## Future Enhancements

### Potential Improvements

1. **Saved Sessions**: Checkpoint workflow state to allow resumption after interruption
2. **Template Variations**: Support different definition templates for specialized agent types
3. **Batch Creation**: Create multiple related agents in one session (e.g., security-scanner + security-fixer + security-monitor)
4. **Learning from Usage**: Track which proposals users accept/reject to improve future recommendations
5. **Context Analysis**: Analyze existing agents to suggest complementary capabilities
6. **Voice Mode**: Natural language conversation instead of structured Q&A (when Claude supports voice)

---

## Related Documentation

- **Agent Template**: `.claude/templates/agent.template.md` (structure for final agent)
- **Input Template**: `.claude/templates/agent-definition-input.template.md` (structure for definition file)
- **Full Workflow**: `.claude/commands/create-agent.md` (existing 10-phase agent creation)
- **Agent Architect**: `.claude/agents/claude-code-ecosystem.md` (agent handling all analysis/generation)
- **Schema Reference**: `.claude/docs/schemas/claude-code-ecosystem.schema.json` (input/output contracts)

---

**Document Version**: 1.0.0
**Last Updated**: 2025-10-22
**Compatibility**: Claude Code v1.0.111+, claude-code-ecosystem v2.2.0+

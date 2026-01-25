# Interactive Mode for Agent Creation

Detailed documentation for the 5-phase interactive workflow (`--create-definition` flag).

---

## Overview

**Purpose**: Create agent definition interactively from a simple idea without needing to understand the complete template structure.

**Entry Point**: `/create-agent --create-definition path/to/output.md`

**Time**: 5-10 minutes (vs. 30-60 minutes manual template filling)

**Output**: Complete agent definition file ready for standard 10-phase workflow

---

## Phase I-1: Capture User Idea

**Goal**: Extract core agent concept in 2-3 sentences

**Orchestrator Role**: Direct interaction (no delegation)

**User Action**: Describe what problem agent solves, what it does, when to call it

**Time**: 1-2 minutes

### Prompt Template

```text
Describe your agent idea in 2-3 sentences:

Use the "What, How, When" framework:
- WHAT problem does this agent solve?
- HOW does it accomplish this (key actions)?
- WHEN should it be called instead of other agents?

Example:
"An agent that analyzes Python code for performance bottlenecks
by profiling function execution times and memory usage. Call it
when optimizing slow code paths after functionality is correct."
```

### Success Criteria
- User provides substantive description (>20 words)
- At least 2 of 3 framework elements present
- Clear domain/scope implied

### Failure Handling
- If too vague: Re-prompt with guidance
- Max 3 attempts before suggesting manual template
- Show examples of good vs. vague ideas

---

## Phase I-2: Analyze Idea & Propose Structure

**Goal**: Transform informal idea into structured proposal with confidence-scored recommendations

**Delegation**: claude-code-ecosystem (analyze_agent_idea operation)

**Time**: 10-15 seconds

### Input Schema

```json
{
  "operation_type": "analyze_agent_idea",
  "task_id": "uuid",
  "description": "Analyze user idea and propose agent structure",
  "agent_idea_analysis": {
    "user_idea_text": "2-3 sentence description from user",
    "analysis_depth": "comprehensive"
  },
  "execution_timestamp": "2025-10-22T10:30:00Z"
}
```

### Output Structure

The claude-code-ecosystem returns structured proposal with 10 sections:

1. **Agent Name Options** (2-3 choices with rationale)
   - Primary recommendation with confidence
   - Alternatives with trade-offs

2. **Domain Scope** (directory boundaries)
   - `.claude/**`, `packages/**`, `docs/**`, etc.
   - Confidence score and justification

3. **Agent Type** (classification)
   - Creator / Reviewer / Enhancer / Runner / Analyzer
   - Based on primary action pattern

4. **Purpose Statement** (orchestrator description)
   - 1-2 sentences for when orchestrator should call
   - Differentiation from similar agents

5. **Core Capabilities** (4-6 items)
   - Primary functions with confidence scores
   - Prioritized by importance

6. **Expected Inputs**
   - Required context and parameters
   - Schema hints for Phase 6

7. **Expected Outputs**
   - Success deliverables
   - Failure information needs

8. **Domain Knowledge Areas**
   - Frameworks, methodologies needed
   - Research topics for Phase 4

9. **Tool Recommendations**
   - Read, Write, Edit, Bash, Task, etc.
   - Confidence scores with rationale

10. **Integration Points**
    - Upstream dependencies
    - Downstream consumers

All recommendations include:
- Confidence score (0.0-1.0)
- Rationale explaining the recommendation
- Alternatives considered

---

## Phase I-3: Interactive Refinement

**Goal**: Walk through proposal with user Q&A

**Orchestrator Role**: Direct interaction (no delegation)

**Time**: 3-5 minutes

### Interaction Patterns

**Name Selection**:
```text
Recommended agent names:
1. python-performance-analyzer (confidence: 0.92)
   - Clear purpose, follows naming convention
2. code-profiler (confidence: 0.78)
   - More generic, could conflict with future agents
3. perf-bottleneck-finder (confidence: 0.71)
   - Descriptive but verbose

Choose [1/2/3] or provide custom name:
```

**Domain/Type Confirmation**:
```text
Proposed domain: packages/** (confidence: 0.95)
Rationale: Agent works on Python source code in packages/

Proposed type: Analyzer (confidence: 0.88)
Rationale: Primary action is analysis, not creation or modification

Accept? [Y/n] or specify different:
```

**Purpose Refinement**:
```text
Proposed purpose statement:
"Analyze Python code for performance bottlenecks by profiling
execution times and memory usage. Call when optimizing slow
code paths after functionality is verified correct."

Accept? [Y/n] or provide improved version:
```

**List Items (Capabilities, Tools)**:
```text
Proposed capabilities:
1. Profile function execution times
2. Analyze memory allocation patterns
3. Identify CPU-bound vs I/O-bound bottlenecks
4. Generate optimization recommendations
5. Compare before/after performance metrics

Options:
- [A] Accept all
- [R] Remove item (specify number)
- [E] Edit item (specify number)
- [+] Add new capability
```

### Refinement Rules

- User can accept defaults for rapid completion
- Each section can be individually refined
- Changes propagate to dependent sections
- Can return to previous sections

---

## Phase I-4: Generate Definition File

**Goal**: Create complete agent definition file from refined requirements

**Delegation**: claude-code-ecosystem (generate_agent_definition operation)

**Time**: 5-10 seconds

### Input Schema

```json
{
  "operation_type": "generate_agent_definition",
  "task_id": "uuid",
  "description": "Generate agent definition file",
  "definition_generation": {
    "output_path": "path/to/agent-definition.md",
    "refined_requirements": {
      "name": "python-performance-analyzer",
      "domain": "packages/**",
      "type": "Analyzer",
      "purpose": "Orchestrator description",
      "capabilities": ["capability 1", "capability 2"],
      "inputs": [],
      "success_output": "Description",
      "failure_output": "Description",
      "knowledge_areas": [],
      "tools": [],
      "integration_points": {},
      "original_idea": "User's original 2-3 sentences"
    }
  },
  "execution_timestamp": "2025-10-22T10:35:00Z"
}
```

### Output

Agent definition file at specified path following `.claude/templates/agent-definition-input.template.md` structure.

### Validation

- File created at specified path
- All required sections populated
- Format matches template structure
- Ready for standard 10-phase workflow

---

## Phase I-5: Present Completion & Options

**Goal**: Offer next steps to user

**Orchestrator Role**: Direct interaction (no delegation)

**Time**: 1 minute

### Presentation Format

```text
Agent Definition Created: python-performance-analyzer.md

Preview (first 30 lines):
---
# Agent Definition Input
name: python-performance-analyzer
domain: packages/**
type: Analyzer
...
---

Options:
1. [P] Proceed immediately - Run standard 10-phase workflow now (10-15 min)
2. [R] Review first - Exit, manually review file, run /create-agent later
3. [G] Regenerate - Return to Phase I-3 with different answers

Choose [P/R/G]:
```

### Option Handling

**Option 1: Proceed Immediately**
- Continues to standard 10-phase workflow (Phase 1)
- Uses just-generated definition file as input
- Full research, documentation, schema, validation

**Option 2: Review First**
- Command completes
- Definition file saved at specified path
- User can manually edit before running:
  ```bash
  /create-agent python-performance-analyzer.md
  ```

**Option 3: Regenerate**
- Returns to Phase I-3 (Interactive Refinement)
- Previous answers preserved as defaults
- User can modify specific sections
- New definition file generated

---

## Agent Assignments (Interactive Mode)

| Phase | Task | Agent | Rationale |
|-------|------|-------|-----------|
| I-1 | Capture user idea | Orchestrator | Simple text collection |
| I-2 | Analyze idea | claude-code-ecosystem | Agent expertise, structured analysis |
| I-2 | Propose structure | claude-code-ecosystem | Design patterns, recommendations |
| I-3 | Interactive refinement | Orchestrator | User interaction, Q&A flow |
| I-4 | Generate definition | claude-code-ecosystem | Template application, validation |
| I-5 | Present completion | Orchestrator | User communication, options |

---

## Error Handling (Interactive Mode)

### Vague User Idea (Phase I-1)

**Trigger**: User idea lacks specificity (<20 words or missing framework elements)

**Response**:
```text
Your idea needs more detail. Please include:
- WHAT problem does it solve? (missing)
- HOW does it accomplish this? (present)
- WHEN should it be called? (missing)

Try again with more specific description:
```

**Max Retries**: 3 attempts before suggesting manual template

### Analysis Failure (Phase I-2)

**Trigger**: claude-code-ecosystem returns FAILURE status

**Response**:
1. Extract `missing_information` from failure_details
2. Present to user with specific questions
3. Offer options: Rephrase, Provide detail, Cancel

### Generation Failure (Phase I-4)

**Trigger**: claude-code-ecosystem cannot generate valid definition

**Response**:
1. Show `failure_details.reasons`
2. Offer: Retry, Return to I-3, Cancel

### File System Errors

| Error | Response |
|-------|----------|
| Output path exists | Offer: Overwrite, Rename, Cancel |
| Write permission denied | Request new writable path |
| Invalid path format | Validate and suggest corrections |

---

## Complete Example Flow

```text
User: /create-agent --create-definition perf-analyzer.md

Phase I-1:
Claude: Describe your agent idea...
User: "An agent that profiles Python code performance and identifies
       bottlenecks. It should analyze execution time and memory usage
       to help optimize slow code."

Phase I-2:
Claude: [Delegates to claude-code-ecosystem]
Claude: Analysis complete. Proposed structure:
        Name: python-performance-analyzer (0.92)
        Domain: packages/** (0.95)
        Type: Analyzer (0.88)
        ...

Phase I-3:
Claude: Choose name [1/2/3] or custom:
User: 1
Claude: Accept domain packages/**? [Y/n]
User: Y
Claude: Accept capabilities? [A/R/E/+]
User: A
...

Phase I-4:
Claude: [Generates definition file]
Claude: Definition created at perf-analyzer.md

Phase I-5:
Claude: Choose [P/R/G]:
User: P

[Continues to standard 10-phase workflow...]
```

---

## Related Documentation

- **Input Template**: `.claude/templates/agent-definition-input.template.md`
- **Workflow Spec**: `.claude/docs/01-guides/interactive-agent-definition-workflow.md`
- **Standard Workflow**: `workflow-phases.md` (this directory)
- **Delegation Patterns**: `delegation-patterns.md` (this directory)

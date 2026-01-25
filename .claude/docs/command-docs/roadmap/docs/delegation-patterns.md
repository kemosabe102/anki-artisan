# Delegation Patterns

Exact Task() call syntax for agent delegation in the `/roadmap` command.

---

## Critical Rule: Parallel Launch

**ALWAYS launch Phase 2 agents in a SINGLE MESSAGE with 3 Task calls.**

Sequential launch wastes ~50 seconds. Parallel execution completes in ~40 seconds.

---

## Check Mode (Multi-Agent)

### Phase 2: Parallel Launch Pattern

```python
# Single message with 3 Task calls - CRITICAL for parallel execution
Task(
    subagent_type="planning",
    prompt="""Analyze roadmap health for the following files:
    {roadmap_files}
    
    Evaluate these dimensions:
    1. Sprint Compliance: Are sprints following standard structure?
    2. Freshness: When was each file last updated? Flag >30 days stale.
    3. Completeness: Are required sections present?
    
    Output: Health scores (0.0-1.0) for each dimension + specific issues found."""
)

Task(
    subagent_type="documentation",
    prompt="""Validate cross-references in roadmap files:
    {roadmap_files}
    
    Check:
    1. Cross-Reference Integrity: Are all internal links valid?
    2. Progressive Disclosure: Are files appropriately sized (<500 lines)?
    
    Output: Link validation report with broken links (file:line) + oversized files."""
)


Task(
    subagent_type="context-optimizer",
    prompt="""Analyze token density for roadmap files:
    {roadmap_files}
    
    Evaluate:
    1. Token Density: Calculate filler word ratio
    2. AI-Readability: Check passive voice %, structure clarity
    
    Output: Optimization opportunities with estimated token savings."""
)
```

### Orchestrator Flow (Check Mode)

```text
Claude Code (orchestrator)
|-- PHASE 1: Discovery (Glob, Read) - 5s
|-- PHASE 2: Multi-Agent Analysis (PARALLEL) - 40s
|   |-- [planning] -> Sprint Compliance, Freshness, Completeness
|   |-- [documentation] -> Cross-Ref Integrity, Progressive Disclosure
|   |-- [context-optimizer] -> Token Density
|-- PHASE 3: Synthesis & Aggregation - 10s
|   |-- Calculate weighted health score
|   |-- Detect overlapping recommendations (>0.7 similarity)
|   |-- Apply synthesis framework if needed
|   |-- Rank top 5 opportunities by ROI
|-- PHASE 4: Present unified dashboard -> HUMAN REVIEW
```

---

## Update Mode (Single Agent)

```python
Task(
    subagent_type="planning",
    prompt="""Update status for roadmap files:
    {roadmap_files}
    
    Actions:
    1. Update completion percentages based on task status
    2. Refresh timestamps to current date
    3. Update status fields (PLANNING -> IN PROGRESS, etc.)
    
    Output: List of files updated with changes made."""
)
```


### Orchestrator Flow (Update Mode)

```text
Claude Code (orchestrator)
|-- Discovery (Glob, Read)
|-- [planning] update_roadmap_status
|   |-- Update completion %, timestamps, status fields
|-- Present update summary -> HUMAN REVIEW
```

---

## Optimize Mode (Single Agent)

```python
Task(
    subagent_type="context-optimizer",
    prompt="""Optimize token density for roadmap files:
    {roadmap_files}
    
    Apply AI-readable best practices:
    1. Remove filler words and redundant phrases
    2. Convert passive voice to active voice
    3. Improve structural formatting
    
    Output: Token savings report with techniques applied per file."""
)
```

### Orchestrator Flow (Optimize Mode)

```text
Claude Code (orchestrator)
|-- Discovery (Glob, Read)
|-- [context-optimizer] apply_ai_best_practices
|   |-- Filler removal, active voice, structured formats
|-- Present optimization metrics -> HUMAN REVIEW
```

---

## Multi-Agent Coordination

### Agent Responsibilities

| Agent | Primary Focus | Secondary Focus |
|-------|---------------|-----------------|
| planning | Sprint compliance | Freshness, completeness |
| documentation | Link validation | Progressive disclosure, file structure |
| context-optimizer | Token density | AI-readability, formatting |

### Result Aggregation

The orchestrator collects outputs and applies the synthesis framework:

1. **Collect**: Gather health scores from all agents
2. **Weight**: Apply dimension weights (see workflow-phases.md)
3. **Synthesize**: Merge overlapping recommendations
4. **Rank**: Sort by ROI = (impact x confidence) / effort
5. **Present**: Generate dashboard with top 5 actions

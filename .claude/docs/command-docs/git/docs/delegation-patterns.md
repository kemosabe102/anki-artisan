# Delegation Patterns for /git Command

**CRITICAL**: Use these EXACT Task() call patterns. Phase 3 runs as an ITERATIVE LOOP with human checkpoints.

---

## Phase-to-Framework Mapping

| Phase | Cognitive Task | Framework | Why |
|-------|---------------|-----------|-----|
| **1: Validation** | Debug failures, fix issues | **ReACT** | Hypothesis -> Act -> Observe -> Refine loop |
| **2: File Grouping** | Classify changes, pattern match | **Cynefin** | Classify problem type -> select strategy |
| **3: Iterative Review** | Per-group quality + human decision | **DMAIC + Pre-Mortem** | Measure -> Analyze -> Present risks -> Decide |

**See**: `.claude/docs/00-core/frameworks/README.md` for full framework definitions.

---

## Phase 1: Validation

**Framework**: ReACT (Reason -> Act -> Observe -> Refine)

**Why ReACT**: Validation failures require hypothesis-driven debugging with iterative fix attempts.

**Apply Framework**:
1. **REASON**: Form hypothesis about failure cause from error output
2. **ACT**: Apply fix (auto-format, fix import, modify code)
3. **OBSERVE**: Re-run validation, check if fixed
4. **REFINE**: If still failing, update hypothesis, iterate (max 3)

```
Task(
  subagent_type="debugger",
  prompt="Execute validate_pre_commit operation using ReACT framework:

    REASON: Analyze prepare-code-review.py output, form hypothesis about failures
    ACT: Run uv run python scripts/prepare-code-review.py --fast
    OBSERVE: Check results - linting, formatting, test outcomes
    REFINE: If failures, fix and retry (max 3 iterations)

    Return: {status: PASS|FAIL, fixes_applied: [], blockers: [], iterations: N}"
)
```

**Expected Output:**
```json
{
  "status": "SUCCESS|FAILURE",
  "validation_status": "PASS|FAIL",
  "fixes_applied": [],
  "blockers": []
}
```

---

## Phase 2: File Grouping

**Framework**: Cynefin (Classify -> Select Strategy)

**Why Cynefin**: File changes fall into different complexity domains requiring different grouping strategies.

**Apply Framework**:
1. **OBSERVE**: Gather all changed files via `git status --porcelain`
2. **CLASSIFY** each change:
   - SIMPLE: Single-file changes, obvious scope -> Direct grouping
   - COMPLICATED: Related files, test+implementation pairs -> Heuristic coupling
   - COMPLEX: Cross-cutting changes, multiple domains -> Domain-based separation
3. **SELECT** grouping strategy per classification
4. **VALIDATE**: Confidence score reflects classification certainty

```
Task(
  subagent_type="source-control",
  prompt="Execute analyze_changes operation using Cynefin framework:

    OBSERVE: Run git status --porcelain to identify all changes
    CLASSIFY: For each file, determine complexity domain:
      - SIMPLE: Isolated change, clear scope
      - COMPLICATED: Related files (test+impl, config+code)
      - COMPLEX: Cross-domain, multiple concerns
    SELECT: Apply appropriate FileGrouper heuristic per domain
    VALIDATE: Assign confidence based on classification clarity

    Return: {commit_groups: [{group_id, files, change_type, scope, message, confidence, complexity_domain}]}"
)
```

**Expected Output:**
```json
{
  "commit_groups": [
    {
      "group_id": "group_1",
      "files": ["file1.py", "file2.py"],
      "change_type": "feat",
      "scope": "agents",
      "message": "feat(agents): add new capability",
      "confidence": 0.92
    }
  ]
}
```

---

## Phase 3: Iterative Review + Commit Loop

**Frameworks**: DMAIC (Measure -> Analyze -> Improve) + Pre-Mortem (Present risks -> Decide)

**Why Combined**: Quality assessment requires measurement (DMAIC), while human checkpoints need risk presentation (Pre-Mortem).

**CRITICAL**: Process groups ONE AT A TIME with human approval checkpoint between each group.

### Step A: Stage Group

Stage only the files for the current group being reviewed.

```
Task(
  subagent_type="source-control",
  prompt="Execute stage_group operation:
    Files to stage: {group.files}
    Return: {status: SUCCESS, staged_files: []}"
)
```

---

### Step B: Quality Gates (PARALLEL)

Run these three Task() calls in parallel (single message with multiple Task calls):

```
Task(
  subagent_type="tech-debt-investigator",
  prompt="DMAIC quality analysis for group {group.group_id}:
    DEFINE: Scope is {group.files} only
    MEASURE: Calculate debt_score, count issues by severity
    ANALYZE: Identify patterns causing debt
    IMPROVE: Prioritized recommendations
    Return: {debt_score, issues: [], recommendations: []}"
)

Task(
  subagent_type="sast-scanner",
  prompt="DMAIC security analysis for group {group.group_id}:
    DEFINE: Scope is {group.files} only
    MEASURE: Scan for vulnerabilities
    ANALYZE: Root cause of each vulnerability
    IMPROVE: Specific remediation steps
    Return: {vulnerabilities: [], severity_counts: {}, remediations: []}"
)

Task(
  subagent_type="code-quality",
  prompt="Full code review for group {group.group_id}:
    Files: {group.files}
    Scope: {group.scope}
    
    Perform detailed line-by-line code review:
    - Check for bugs, logic errors, edge cases
    - Verify adherence to coding standards
    - Identify security concerns
    - Suggest improvements
    
    Return: {review_status: APPROVED|CHANGES_REQUIRED|BLOCKED, 
            suggestions: [], 
            blocking_issues: [],
            line_comments: [{file, line, severity, comment}]}"
)
```

---

### Step C: Present Checkpoint (Orchestrator)

**No delegation** - orchestrator presents checkpoint directly using Pre-Mortem framework.

**Apply Pre-Mortem**:
1. **ASSUME FAILURE**: "What if this commit causes problems?"
2. **IDENTIFY CAUSES**: Surface blocking issues, security risks, tech debt
3. **PRESENT RISKS**: Show quality results with severity
4. **AWAIT DECISION**: Present options to user

**Checkpoint Output Format**:
```
GROUP {N} of {TOTAL}: {group.message}
Files: {group.files}

Quality Results:
- Tech Debt Score: {debt_score}
- Security: {vulnerability_count} issues ({severity_breakdown})
- Code Review: {review_status}

{If blocking issues exist}:
BLOCKING ISSUES:
- {issue_1}
- {issue_2}

Options:
[c] Commit this group
[s] Skip this group
[e] Edit files (pause workflow)
[a] Abort remaining groups
```

---

### Step D: Human Decision

**No delegation** - wait for user input.

| User Input | Action |
|------------|--------|
| `c` or `commit` | Proceed to Step E (Commit) |
| `s` or `skip` | Proceed to Step F (Unstage), then next group |
| `e` or `edit` | Pause workflow, user makes changes |
| `a` or `abort` | Exit loop, report summary |

---

### Step E: Commit (if approved)

Execute commit for the approved group.

```
Task(
  subagent_type="source-control",
  prompt="Execute execute_single_commit operation:
    Message: {group.message}
    
    BUILD: Verify files staged, create commit
    MEASURE: Check commit hash created
    LEARN: If failure, report cause
    
    Return: {status: SUCCESS|FAILURE, commit_hash: 'abc123', message: '...'}"
)
```

---

### Step F: Unstage

Clean up staging area for next group (or after skip).

```
Task(
  subagent_type="source-control",
  prompt="Execute unstage_all operation:
    Return: {status: SUCCESS}"
)
```

---

## Complete Iterative Loop Pattern

Shows the complete Task() call sequence for processing all groups:

```
# Phase 3: Iterative Review + Commit Loop
FOR EACH group in commit_groups:
  
  # Step A: Stage
  Task(source-control, stage_group, files=group.files)
  
  # Step B: Quality (PARALLEL - single message with 3 Task calls)
  Task(tech-debt-investigator, ...)
  Task(sast-scanner, ...)
  Task(code-quality, ...)
  
  # Step C: Present Checkpoint (orchestrator, no delegation)
  # Display quality results + options to user
  
  # Step D: Wait for Human Decision
  # User chooses: [c]ommit, [s]kip, [e]dit, [a]bort
  
  IF user_choice == 'commit':
    # Step E: Commit
    Task(source-control, execute_single_commit, message=group.message)
  
  # Step F: Unstage (always, prepares for next group)
  Task(source-control, unstage_all)
  
  IF user_choice == 'abort':
    BREAK
  
END FOR

# Report final summary
```

---

## /git continue Resume Pattern

When resuming from a paused workflow (user selected `[e]dit` to make changes):

```
# Resume from paused state
group = groups[paused_at_group]

# Re-stage and re-run quality gates (files may have changed)
Task(source-control, stage_group, files=group.files)

# Quality gates (PARALLEL)
Task(tech-debt-investigator, ...)
Task(sast-scanner, ...)
Task(code-quality, ...)

# Present checkpoint again with fresh results
# ... continue normal flow from Step C
```

**Key Points for Resume**:
- Re-run quality gates because files may have been modified
- Do NOT skip directly to commit
- Present checkpoint with updated results
- User gets fresh decision point

---

## Domain Agent Selection

| File Pattern | Domain Agent |
|--------------|--------------|
| `.claude/agents/**` | claude-code-ecosystem, claude-code-ecosystem |
| `docs/**` | documentation, planning |
| `packages/**` | code-quality |
| `tests/**` | code-quality |

---

## Why Iterative Per-Group Processing?

| Benefit | Explanation |
|---------|-------------|
| **Human control** | User approves each group individually |
| **Focused analysis** | 5-10 files per group vs 50+ files at once |
| **Traceable findings** | Know exactly which group has which issues |
| **Partial commits** | Commit approved groups, skip problematic ones |
| **Better agent performance** | Agents work better with smaller, cohesive changesets |
| **Actionable reports** | "Group 2 has security issue" vs "somewhere in 51 files" |
| **Pause and edit** | User can fix issues mid-workflow |

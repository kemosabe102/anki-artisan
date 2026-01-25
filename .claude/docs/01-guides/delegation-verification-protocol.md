---
title: "Delegation Verification Protocol"
date: 2025-11-08
status: DRAFT
tags: [claude-docs]
---
# Delegation Verification Protocol

**Purpose**: Complete delegation verification process, checkpoints, and coordination patterns

**Auto-loaded**: No (on-demand reference from orchestrator-workflow.md)

---

## Verification-First Delegation Protocol

**6-Step Process for All Sub-Agent Delegations**:

### Step 1: PRE-DELEGATION

**Verify preconditions and prepare context**

**Actions**:
- Check if agent exists and is appropriate for task (agent-selection-protocol)
- Verify required inputs available (files, data, context)
- Assess Context_Quality if implementation work (OODA ORIENT phase)
- Prepare delegation prompt with clear objective

**Gate**: Preconditions met → Proceed to Step 2 | Not met → Gather context first

**Example**:
```
Task: "Enhance plan-PLAN.md"
Preconditions:
  ✅ planning exists
  ✅ plan-PLAN.md exists (Read verification)
  ✅ SPEC.md available for context
  ✅ Context_Quality ≥ 0.5
→ Proceed to delegation
```

---

### Step 2: INITIAL ATTEMPT

**Delegate to appropriate sub-agent with current context**

**Actions**:
- Launch Task with clear objective
- Include relevant context (file paths, requirements, constraints)
- Specify expected outputs
- Monitor progress

**Pattern**:
```
Task(
    agent="planning",
    prompt="Enhance docs/plans/core-PLAN.md with business context. "
           "Use Planning Recommendations from SPEC.md. "
           "Expected output: Business Context section populated."
)
```

---

### Step 3: VERIFICATION

**Verify expected outputs exist and meet quality standards**

**File Creation Verification**:
- Files exist at expected locations (Read check)
- File size > 0 (not empty)
- File structure matches expected template

**Content Enhancement Verification**:
- Specific sections populated (not placeholders)
- Content quality meets minimum standards
- Cross-references valid

**Technical Analysis Verification**:
- Technical decisions documented
- Architecture patterns specified
- Integration points defined

**Gate**: Verification passed → Proceed to Step 6 (success) | Failed → Proceed to Step 4 (analysis)

---

### Step 4: ANALYSIS

**If failure or incomplete, analyze what was missing**

**Root Cause Analysis**:
- **Missing Context**: Agent lacked necessary information
- **Ambiguous Requirements**: Objective unclear
- **Technical Limitation**: Agent capability gap
- **File Access Issue**: Read/Write/Edit failure
- **Validation Failure**: Output didn't meet standards

**Example**:
```
Verification Failed: Business Context section still has placeholders

Root Cause Analysis:
- Missing Context: SPEC.md Planning Recommendations not found
- Agent reported: "Planning Recommendations section missing in SPEC.md"
→ Need to provide explicit business context in delegation prompt
```

---

### Step 5: SECOND ATTEMPT

**Retry with enhanced context OR try different sub-agent**

**Strategy A: Enhanced Context (Same Agent)**
```
# First attempt failed due to missing context
# Second attempt with explicit context:
Task(
    agent="planning",
    prompt="Enhance docs/plans/core-PLAN.md with business context. "
           "Business requirements: [explicit requirements from user]. "
           "Target users: [explicit users]. "
           "Success metrics: [explicit metrics]. "
           "NFRs: [explicit NFRs]."
)
```

**Strategy B: Different Agent (Capability Mismatch)**
```
# First attempt: planning failed at technical design
# Second attempt: architecture (better fit)
Task(
    agent="architecture",
    prompt="Add technical design to docs/plans/core-PLAN.md. "
           "Architecture patterns: [patterns from SPEC]."
)
```

**Gate**: Second attempt succeeded → Proceed to Step 6 | Failed → Proceed to Step 6 (escalation)

---

### Step 6: ESCALATION or SUCCESS

**If Successful (Steps 3 or 5)**:
- Document success path for future delegations
- Update agent performance metrics
- Return results to user

**If Still Unsuccessful (After Step 5)**:
- Provide human summary of attempts
- Document what was tried and why it failed
- Recommend:
  - Manual intervention required
  - Agent capability enhancement needed
  - Context gathering required (research delegation)
  - Task decomposition (break into smaller sub-tasks)

**Example Escalation Report**:
```
Delegation Failed After 2 Attempts:

Agent: planning
Objective: Enhance core-PLAN.md

Attempt 1: Missing Planning Recommendations in SPEC.md
Attempt 2: Provided explicit business context, but agent failed file write (Edit tool error)

Root Cause: File locking issue in .claude/docs/ directory

Recommendation:
- Use file_ops.py script (Python fallback) for .claude/** modifications
- OR: Manual file edit with provided business context

Provided Context for Manual Edit:
[Business requirements, target users, success metrics, NFRs]
```

---

## Verification Checkpoints by Task Type

### File Creation Tasks

**Checkpoint 1: File Exists**
```python
# Verify file created
file_path = Path("docs/plans/core-PLAN.md")
if not file_path.exists():
    # FAIL: File not created
    proceed_to_step_4_analysis()
```

**Checkpoint 2: File Not Empty**
```python
# Verify content written
if file_path.stat().st_size == 0:
    # FAIL: Empty file
    proceed_to_step_4_analysis()
```

**Checkpoint 3: Structure Matches Template**
```python
# Verify expected sections present
content = file_path.read_text()
required_sections = ["# Overview", "## Business Context", "## Technical Design"]
for section in required_sections:
    if section not in content:
        # FAIL: Missing required section
        proceed_to_step_4_analysis()
```

---

### Content Enhancement Tasks

**Checkpoint 1: Sections Populated**
```python
# Verify no placeholders remain
content = file_path.read_text()
placeholders = ["[TODO]", "[TBD]", "[PLACEHOLDER]"]
for placeholder in placeholders:
    if placeholder in content:
        # FAIL: Placeholder not replaced
        proceed_to_step_4_analysis()
```

**Checkpoint 2: Content Quality**
```python
# Verify minimum content length (not just one-liners)
section_content = extract_section(content, "## Business Context")
if len(section_content.split()) < 50:  # Minimum 50 words
    # FAIL: Insufficient content
    proceed_to_step_4_analysis()
```

**Checkpoint 3: Cross-References Valid**
```python
# Verify links to other documents
links = extract_links(content)
for link in links:
    target_path = resolve_path(link)
    if not target_path.exists():
        # FAIL: Broken link
        proceed_to_step_4_analysis()
```

---

### Technical Analysis Tasks

**Checkpoint 1: Decisions Documented**
```python
# Verify technical decisions present
if "## Technical Design" not in content:
    # FAIL: Technical design section missing
    proceed_to_step_4_analysis()

tech_design = extract_section(content, "## Technical Design")
if "### Architecture" not in tech_design:
    # FAIL: Architecture not specified
    proceed_to_step_4_analysis()
```

**Checkpoint 2: Patterns Specified**
```python
# Verify architecture patterns documented
patterns = extract_patterns(tech_design)
if len(patterns) == 0:
    # FAIL: No architecture patterns
    proceed_to_step_4_analysis()
```

**Checkpoint 3: Integration Points Defined**
```python
# Verify integration points specified
if "### Integration" not in tech_design:
    # FAIL: Integration section missing
    proceed_to_step_4_analysis()
```

---

## Sub-Agent Coordination Patterns

### Pattern 1: Sequential Dependency

**When**: Output of Agent A feeds into Agent B

**Example**:
```text
Step 1: /spec command creates SPEC.md
  ↓ Verify SPEC.md exists
Step 2: planning creates *-PLAN.md from SPEC.md
  ↓ Verify *-PLAN.md exists
Step 3: architecture enhances *-PLAN.md
```

**Critical**: NEVER parallelize dependent agents

---

### Pattern 2: Parallel Independent

**When**: Multiple agents work on different files

**Example**:
```text
[Parallel Launch]:
  ├─ planning: core-PLAN.md
  ├─ planning: analysis-PLAN.md
  └─ planning: integration-PLAN.md

[After completion, verify all]:
  ✅ core-PLAN.md enhanced
  ✅ analysis-PLAN.md enhanced
  ✅ integration-PLAN.md enhanced
```

---

### Pattern 3: Review-Then-Enhance

**When**: Fast review before expensive enhancement

**Example**:
```text
Step 1: planning validates SPEC.md (30s)
  ↓ Verify quality score ≥ 0.7
  ├─ PASS → Proceed to enhancement
  └─ FAIL → Escalate quality issues to user
Step 2: planning creates plans (2min)
```

**Benefits**: Fast feedback, avoid wasted enhancement effort

---

### Pattern 4: Multi-Agent Analysis

**When**: 3+ agents provide different perspectives

**Example**:
```text
[Parallel Launch - 3 core + 2 dynamic]:
  ├─ planning: Business review
  ├─ architecture: Technical review
  ├─ tech-debt-investigator: Debt analysis
  ├─ code-quality: Security review (dynamic, confidence >0.8)
  └─ code-quality: Test validation (dynamic, confidence >0.8)

[After completion, synthesize]:
  ↓ Apply synthesis-and-recommendation-framework.md
  → Consolidated recommendations (no redundancy)
```

---

## Coordination Rules

### Rule 1: Orchestrator-Only Delegation

**Principle**: Only orchestrator delegates to sub-agents

**Correct**:
```
Orchestrator → Task(agent="planning", ...)
```

**Incorrect**:
```
planning → Task(agent="architecture", ...)  # ❌ Sub-agents cannot delegate
```

---

### Rule 2: No Direct Sub-Agent Communication

**Principle**: All sub-agent communication flows through orchestrator

**Correct**:
```
planning → Output → Orchestrator → Task(agent="architecture", ...)
```

**Incorrect**:
```
planning → architecture  # ❌ No direct sub-agent communication
```

---

### Rule 3: Orchestrator Maintains Context

**Principle**: Orchestrator maintains state across sub-agent interactions

**Context Tracking**:
- Previous attempts and outcomes
- Context accumulated across interactions
- Blockers and resolution strategies
- Decision history and rationale

**Example**:
```text
Orchestrator State:
  ├─ Attempt 1: planning (failed - missing Planning Recommendations)
  ├─ Context Gathered: Explicit business requirements from user
  └─ Attempt 2: planning (success - with explicit context)
```

---

### Rule 4: Parallel Execution for Independent Work

**Principle**: Launch multiple sub-agents in parallel when no file conflicts exist

**Parallel Safe**:
- Different files in different directories ✅
- Independent research tasks ✅
- Multi-agent analysis (read-only) ✅

**Parallel Unsafe**:
- `.claude/**` directory modifications ❌ (file locking)
- Single file by multiple agents ❌ (conflicts)
- Agent dependencies (A → B) ❌ (ordering)

---

## Complete Delegation Example

**Task**: Enhance 3 component plans with business context

### Step 1: PRE-DELEGATION

```text
Preconditions:
  ✅ planning exists
  ✅ All 3 *-PLAN.md files exist
  ✅ SPEC.md available with Planning Recommendations
  ✅ No file conflicts (different files)
→ Safe to parallelize
```

---

### Step 2: INITIAL ATTEMPT (Parallel)

```python
# Launch 3 agents in parallel:
Task(agent="planning", prompt="Enhance core-PLAN.md")
Task(agent="planning", prompt="Enhance analysis-PLAN.md")
Task(agent="planning", prompt="Enhance integration-PLAN.md")
```

---

### Step 3: VERIFICATION

```text
# Verify all 3 outputs:
for plan in ["core-PLAN.md", "analysis-PLAN.md", "integration-PLAN.md"]:
    ✅ File exists
    ✅ Business Context section populated (no placeholders)
    ✅ NFR specifications added
    ✅ Success Metrics defined
→ All verifications passed
```

---

### Step 6: SUCCESS

```text
All 3 plans enhanced successfully.

Delegation Metrics:
- Total Time: 2min (vs 6min sequential)
- Speedup: 3x faster
- Success Rate: 100% (3/3)

Output:
- core-PLAN.md: Business Context complete
- analysis-PLAN.md: Business Context complete
- integration-PLAN.md: Business Context complete
```

---

**This protocol provides complete delegation verification and coordination patterns for orchestrator sub-agent management.**
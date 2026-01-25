# Pattern Rubrics Reference

Detailed scoring rubrics for each of the 7 mandatory agent workflow patterns.

---

## P1: Mode Detection Table (10 points)

### Purpose
Deterministic keyword → skill/action mapping enables reliable agent behavior routing.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | Table present, all modes have specific keywords, each maps to one skill, no ambiguity |
| **8-9** | Table present, minor gaps (1 vague keyword or missing mapping) |
| **5-7** | Table present but incomplete (missing modes or vague keywords throughout) |
| **2-4** | Informal mode description exists but no structured table |
| **0-1** | No mode detection mechanism at all |

### Required Elements

1. **Table Header**: `| Mode | Trigger Keywords | Primary Skill |`
2. **Specific Keywords**: "find code" ✓, "complex" ✗
3. **One-to-One Mapping**: Each mode → exactly one skill/action
4. **Completeness**: All operational modes documented

### Detection Patterns

Search for:
- `## Mode Detection` or `## Modes`
- Markdown table with 3+ columns
- Keywords like "trigger", "when", "use when"

---

## P2: OODA Workflow (10 points)

### Purpose
Ensures systematic execution through all cognitive phases.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | All 4 phases with 3-4 concrete bullets each, ORIENT has mandatory skill invocation |
| **8-9** | All 4 phases present, minor detail gaps |
| **5-7** | 3 of 4 phases present OR phases present but too vague |
| **2-4** | Only 1-2 phases documented |
| **0-1** | No OODA structure at all |

### Required Elements

**OBSERVE** (2 pts):
- Parse objective/input
- Identify targets/constraints
- Detect mode from keywords

**ORIENT** (3 pts - weighted higher):
- **MUST have skill invocation** ("Invoke: Skill(X)")
- Load context (max 5 files recommended)
- Read skill reference documentation

**DECIDE** (2 pts):
- Plan strategy per methodology
- Determine tool execution order
- Set confidence thresholds

**ACT** (3 pts - weighted higher):
- Execute per skill methodology
- Apply compression/synthesis
- Generate structured output

### Detection Patterns

Search for:
- `### OBSERVE`, `### ORIENT`, `### DECIDE`, `### ACT`
- `## OODA Workflow`
- Phase-like headers with execution steps

---

## P3: Mode-Specific Sections (10 points)

### Purpose
Dedicated workflow sections per mode ensure each operational context has explicit, unambiguous execution steps.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | Separate section per mode, each starts with Skill() invocation, 3-5 concrete steps each |
| **8-9** | Sections present, minor gaps (1 mode missing skill invocation or vague steps) |
| **5-7** | Mode sections exist but inconsistent structure or missing skill invocations |
| **2-4** | Modes mentioned but lumped together or lack actionable steps |
| **0-1** | No mode-specific sections at all |

### Required Elements

1. **Section per Mode**: `### [Mode Name] Workflow` or equivalent
2. **Step 1 = Skill Invocation**: First action must be `Skill(skill-name)`
3. **Numbered Steps**: 3-5 concrete execution steps per mode
4. **Exit Criteria**: When is this mode complete?

### Detection Patterns

Search for:
- `### [Mode] Mode` or `### [Mode] Workflow`
- `Step 1:` or `1.` followed by `Skill(`
- Multiple workflow sections with distinct headers

---


## P4: Anti-Patterns Section (10 points)

### Purpose
Explicit forbidden behaviors prevent common failure modes and ensure consistent agent quality.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | 4-6 explicit "NEVER DO" items, includes phase-skipping prohibition, actionable specifics |
| **8-9** | Anti-patterns present, 3-5 items, minor gaps in specificity |
| **5-7** | Some anti-patterns mentioned but vague or fewer than 3 items |
| **2-4** | Implicit warnings scattered throughout but no dedicated section |
| **0-1** | No anti-pattern documentation at all |

### Required Elements

1. **Dedicated Section**: `## Anti-Patterns` or `## NEVER DO`
2. **4-6 Items**: Minimum threshold for comprehensive coverage
3. **Phase-Skipping Prohibition**: MUST forbid jumping from OBSERVE to ACT
4. **Specific Examples**: "NEVER modify files without reading first" not "be careful"
5. **Consequence Indication**: Why each anti-pattern is harmful (optional but preferred)

### Detection Patterns

Search for:
- `## Anti-Patterns`, `## NEVER`, `## Forbidden`
- `NEVER`, `DO NOT`, `BANNED`, `PROHIBITED`
- Bulleted list with negative imperatives

---


## P5: Ask-First Rules (10 points)

### Purpose
Measurable stop conditions define when agent must pause and request user input before proceeding.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | 3-5 measurable stop conditions, each has clear threshold/trigger, table format preferred |
| **8-9** | Ask-first rules present, minor gaps (1 vague condition or missing threshold) |
| **5-7** | Some pause conditions mentioned but not measurable or fewer than 3 |
| **2-4** | General guidance to "ask when unsure" without specifics |
| **0-1** | No ask-first rules documented |

### Required Elements

1. **Dedicated Section**: `## Ask-First Rules` or `## Stop Conditions`
2. **3-5 Conditions**: Minimum coverage for safety
3. **Measurable Triggers**: "confidence < 0.70" not "when uncertain"
4. **Specific Scenarios**: "destructive git operation", "scope > 10 files"
5. **Table Format**: `| Condition | Trigger | Action |` (preferred)

### Detection Patterns

Search for:
- `## Ask-First`, `## Stop Conditions`, `## Pause When`
- Threshold values (percentages, counts, confidence scores)
- `STOP`, `ASK`, `PAUSE`, `ESCALATE` keywords

---


## P6: Output Structure (10 points)

### Purpose
Consistent output templates enable reliable parsing, automation, and quality assessment.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | SUCCESS + FAILURE templates, JSON format, confidence scores, file:line references |
| **8-9** | Both templates present, minor gaps (missing confidence or incomplete fields) |
| **5-7** | One template present OR templates lack structure |
| **2-4** | Output mentioned but no structured templates |
| **0-1** | No output structure documentation |

### Required Elements

1. **SUCCESS Template**: JSON structure for successful completion
2. **FAILURE Template**: JSON structure for error/incomplete states
3. **Confidence Field**: `"confidence": 0.XX` in output
4. **Status Field**: `"status": "SUCCESS|FAILURE"`
5. **Evidence References**: `"files_modified": []` or `"findings": []` with paths

### Detection Patterns

Search for:
- `## Output`, `## Response Format`, `## Template`
- JSON code blocks with `status`, `confidence`
- `SUCCESS` and `FAILURE` in same section

---


## P7: Role & Boundaries (10 points)

### Purpose
Explicit scope definition prevents domain overlap and ensures agents operate within intended responsibilities.

### Scoring Rubric

| Score | Criteria |
|-------|----------|
| **10** | "Your Job" statement + explicit "NOT for/Boundaries" list, 3+ boundary items |
| **8-9** | Both sections present, minor gaps (vague boundaries or incomplete scope) |
| **5-7** | Role defined but boundaries missing OR vice versa |
| **2-4** | Implicit role from context but no explicit statement |
| **0-1** | No role or boundary documentation |

### Required Elements

1. **"Your Job" Statement**: 1-2 sentence explicit responsibility definition
2. **Boundaries Section**: `## Boundaries` or `## NOT for`
3. **3+ Boundary Items**: Minimum for meaningful scope restriction
4. **Positive + Negative**: What agent DOES + what agent does NOT do
5. **Domain Clarity**: Clear handoff points to other agents/skills

### Detection Patterns

Search for:
- `## Role`, `## Boundaries`, `## Scope`, `## NOT for`
- `Your Job:`, `This agent`, `Responsible for`
- `NOT`, `NEVER`, `Outside scope`, `Delegate to`

---

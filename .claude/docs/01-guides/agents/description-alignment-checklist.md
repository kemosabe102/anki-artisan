---
title: "Description Alignment Checklist"
date: 2025-11-21
status: ACTIVE
tags: [agents, descriptions, alignment, tokens]
---
# Description Alignment Checklist

**Purpose**: Evaluation framework for agent description accuracy and token efficiency.

**Primary User**: claude-code-ecosystem (during agent quality assessment)

**Focus**: Does the description accurately represent the agent's capabilities AND use tokens efficiently?

**Scope**: Description-to-prompt alignment (accuracy, completeness, efficiency), token optimization

**Not Covered**: Orchestrator delegation effectiveness (see description-delegation-checklist.md)

---

## Overview

Agent descriptions must balance **three competing priorities**:

1. **Accuracy**: Description matches agent's actual capabilities (no false promises)
2. **Completeness**: All major capabilities mentioned (no critical omissions)
3. **Efficiency**: Minimal token usage while maintaining clarity (90-110 token target)

**Critical Insight**: Descriptions are loaded into EVERY orchestrator session. Inefficient descriptions compound costs across thousands of sessions. A 50-token bloated description × 1,000 sessions = 50,000 wasted tokens.

**Relationship to Delegation Quality**: This checklist complements description-delegation-checklist.md:
- **Delegation Checklist** (claude-code-ecosystem): "Will orchestrator select this agent correctly?"
- **Alignment Checklist** (claude-code-ecosystem): "Is the description accurate AND efficient?"

---

## The 6 Alignment Criteria

### ✅ Criterion 1: Capability Accuracy

**Question Answered**: "Does the description match the agent's actual capabilities?"

**Requirements**:
- [ ] Every capability mentioned in description exists in agent prompt
- [ ] No exaggerated claims (e.g., "perfect", "always succeeds", "comprehensive" without evidence)
- [ ] Action verbs match agent's Primary Responsibilities section
- [ ] Technology stack mentioned matches agent's Tools/Integration Points

**Validation Method**:

```bash
# Step 1: Extract description from agent file
description=$(grep -A 5 "^description:" .claude/agents/[agent-name].md | tail -n +2)

# Step 2: Extract capabilities from description (manual review)
# List: [capability 1, capability 2, ...]

# Step 3: Verify each capability in agent prompt
grep -i "[capability keyword]" .claude/agents/[agent-name].md
# Confirm: Appears in Primary Responsibilities, Workflow Operations, or Tool Usage sections

# Step 4: Check for exaggerated claims
echo "$description" | grep -iE "perfect|always|never|100%|comprehensive|complete"
# If found: Verify with evidence in prompt
```

**Evidence Format**:
```markdown
**Capability Accuracy Score**: X/5

**Capabilities Claimed**:
1. [capability 1] - ✅ Found in Primary Responsibilities (line X)
2. [capability 2] - ✅ Found in Tool Usage (line Y)
3. [capability 3] - ❌ NOT FOUND in prompt (MISMATCH)

**Exaggerated Claims**:
- ❌ "comprehensive analysis" - No evidence of scope completeness
- ✅ "proactively reviews" - Confirmed in Workflow Operations (line Z)

**Result**: X/5 capabilities verified, Y exaggerated claims detected
```

**Examples**:

✅ **GOOD**:
```
Description: "Debugging specialist. Analyzes errors, formulates hypotheses,
executes tests, and iterates until resolution."

Verification:
- "Analyzes errors" → Found in Primary Responsibilities: "Error Analysis Workflow"
- "Formulates hypotheses" → Found in Workflow: "Hypothesis Formation"
- "Executes tests" → Found in Tool Usage: "Test Execution Pattern"
- "Iterates until resolution" → Found in Error Recovery: "Iterative Refinement"
All capabilities verified ✅
```

❌ **BAD**:
```
Description: "Perfect code generator that always produces bug-free implementations."

Verification:
- "Perfect" → Exaggerated claim, no evidence
- "Always produces bug-free" → Impossible guarantee, not in prompt
- No capabilities match prompt sections
Capabilities NOT verified ❌
```

---

### ✅ Criterion 2: Scope Completeness

**Question Answered**: "Are all major capabilities mentioned?"

**Requirements**:
- [ ] Primary domain covered (e.g., "Python implementation" for development)
- [ ] Key differentiators mentioned (what makes this agent unique vs others)
- [ ] Major workflows included (not exhaustive, but representative)
- [ ] No critical omissions (e.g., security scanning missing from SAST agent description)

**Validation Method**:

```bash
# Step 1: Extract Primary Responsibilities from agent prompt
grep -A 50 "^## Primary Responsibilities" .claude/agents/[agent-name].md

# Step 2: Identify top 3-5 capabilities (by workflow count, section length, or mentions)
# Manual review: [capability 1, capability 2, capability 3, ...]

# Step 3: Check if each is mentioned in description
description=$(grep -A 5 "^description:" .claude/agents/[agent-name].md | tail -n +2)
echo "$description" | grep -i "[capability keyword]"

# Step 4: Calculate coverage
# Coverage = (capabilities_in_description / top_capabilities) × 100
```

**Evidence Format**:
```markdown
**Scope Completeness Score**: X/5

**Top Capabilities from Prompt**:
1. [Primary capability 1] - ✅ Mentioned in description
2. [Primary capability 2] - ✅ Mentioned in description
3. [Primary capability 3] - ❌ NOT mentioned (omission)
4. [Secondary capability 4] - ✅ Mentioned
5. [Secondary capability 5] - ❌ NOT mentioned (acceptable for secondary)

**Coverage**: 3/5 top capabilities = 60%
**Critical Omissions**: [list any missing primary capabilities]

**Result**: X/5 (based on coverage %)
```

**Examples**:

✅ **GOOD**:
```
Agent Prompt Primary Responsibilities:
1. Code implementation (packages/**)
2. FastAPI route handlers
3. SQLAlchemy models
4. Async patterns
5. Type safety

Description:
"Python implementation specialist for packages/**, tests/**, and core modules.
Handles FastAPI, SQLAlchemy, and async patterns."

Coverage: 4/5 = 80% (Type safety not critical for description)
All primary capabilities covered ✅
```

❌ **BAD**:
```
Agent Prompt Primary Responsibilities:
1. Security vulnerability scanning (SAST)
2. OWASP Top 10 detection
3. Dependency analysis
4. Secret scanning
5. Compliance reporting

Description:
"Code analysis agent for quality checks."

Coverage: 0/5 = 0%
Critical omissions: Security, OWASP, SAST (core purpose missing) ❌
```

---

### ✅ Criterion 3: No Misleading Claims

**Question Answered**: "Could this description mislead the orchestrator?"

**Requirements**:
- [ ] No capabilities mentioned that don't exist in prompt
- [ ] No implied scope beyond agent's boundaries (e.g., "all testing tasks" when agent only does unit tests)
- [ ] No conflicting statements (e.g., "Python specialist" but prompt shows multi-language support)
- [ ] No outdated information (e.g., mentions removed features)

**Validation Method**:

```bash
# Step 1: Extract description
description=$(grep -A 5 "^description:" .claude/agents/[agent-name].md | tail -n +2)

# Step 2: Check for scope overreach
echo "$description" | grep -iE "all|any|every|complete|comprehensive|full"
# Manual review: Verify each claim against prompt's Scope/Boundaries sections

# Step 3: Check for technology mismatches
# Extract technologies from description → Verify in prompt's Tools/Integration Points

# Step 4: Check for conflicting statements
grep -A 10 "^## Boundaries" .claude/agents/[agent-name].md
# Compare boundaries to description claims
```

**Evidence Format**:
```markdown
**Misleading Claims Score**: X/5

**Potential Misleading Statements**:
1. "[claim 1]" - ✅ Verified against Scope section (line X)
2. "[claim 2]" - ❌ MISLEADING - Prompt boundaries exclude this (line Y)
3. "[claim 3]" - ⚠️ AMBIGUOUS - Could be interpreted as broader than intended

**Technology Mismatches**: [list if any]
**Scope Overreach**: [list if any]

**Result**: X/5 (5 = no misleading claims, 0 = multiple misleading claims)
```

**Examples**:

✅ **GOOD**:
```
Description: "Unit test creator for Python packages. Generates pytest fixtures
and test cases for functions and classes."

Prompt Boundaries:
- Scope: Unit tests only (NOT integration tests)
- Technologies: pytest, Python 3.13+
- Exclusions: End-to-end tests, performance tests

No misleading claims ✅
```

❌ **BAD**:
```
Description: "Complete testing solution for all test types and languages."

Prompt Boundaries:
- Scope: Unit tests only
- Technologies: pytest (Python only)
- Exclusions: Integration, E2E, performance tests

Misleading claims:
- "Complete testing solution" → Scope overreach
- "All test types" → Contradicts exclusions
- "All languages" → Python only
Multiple misleading claims ❌
```

---

### ✅ Criterion 4: Boundary Clarity

**Question Answered**: "Does the orchestrator understand what this agent does NOT do?"

**Requirements**:
- [ ] Domain scope is clear (e.g., "packages/**" vs "all Python code")
- [ ] Technology stack is specific (e.g., "pytest" vs "testing")
- [ ] Exclusions are implied or stated (e.g., "unit test creator" implies NOT integration tests)
- [ ] No overlapping confusion with similar agents (e.g., debugger vs code-quality)

**Validation Method**:

```bash
# Step 1: Extract description and boundaries
description=$(grep -A 5 "^description:" .claude/agents/[agent-name].md | tail -n +2)
grep -A 20 "^## Boundaries" .claude/agents/[agent-name].md

# Step 2: Check for scope specificity
echo "$description" | grep -iE "packages/|\.claude/|docs/|tests/|k8s/"
# Directory-specific = clear boundaries ✅
# Generic ("code", "files") = unclear boundaries ❌

# Step 3: Check for technology specificity
echo "$description" | grep -iE "pytest|fastapi|sqlalchemy|prometheus|grafana"
# Specific tools = clear boundaries ✅
# Generic ("testing", "web framework") = unclear ❌

# Step 4: Compare to similar agents (manual review)
# Identify: What makes this agent different from [similar-agent]?
```

**Evidence Format**:
```markdown
**Boundary Clarity Score**: X/5

**Scope Specificity**:
- Domain: [specific directory/domain] OR [generic "code"]
- Technologies: [specific tools listed] OR [generic categories]
- Exclusions: [clearly implied] OR [ambiguous]

**Differentiation from Similar Agents**:
- vs [similar-agent-1]: [clear difference] OR [overlapping/unclear]
- vs [similar-agent-2]: [clear difference] OR [overlapping/unclear]

**Result**: X/5 (5 = crystal clear boundaries, 0 = completely ambiguous)
```

**Examples**:

✅ **GOOD**:
```
Description: "Python implementation specialist for packages/**, tests/**,
and core modules. Handles FastAPI, SQLAlchemy, and async patterns."

Boundaries:
- Scope: packages/** and tests/** (clear directories)
- Technologies: FastAPI, SQLAlchemy, async (specific tools)
- Implied exclusions: NOT .claude/** (not mentioned), NOT docs/** (not mentioned)

Differentiation:
- vs debugger: Implementation (not error fixing)
- vs code-quality: Code creation (not test running)
Clear boundaries ✅
```

❌ **BAD**:
```
Description: "General code assistant for Python tasks."

Boundaries:
- Scope: "Python tasks" (what tasks? which directories?)
- Technologies: None specified (all Python? specific frameworks?)
- Implied exclusions: None

Differentiation:
- vs development: Unclear overlap
- vs debugger: Unclear overlap
Ambiguous boundaries ❌
```

---

### ✅ Criterion 5: Natural Language Quality

**Question Answered**: "Is the description readable and professional?"

**Requirements**:
- [ ] Grammatically correct (no typos, no sentence fragments)
- [ ] Professional tone (not casual, not overly technical jargon)
- [ ] Concise sentences (avg 15-20 words, max 30 words)
- [ ] Logical flow (trigger → capabilities → use case)

**Validation Method**:

```bash
# Step 1: Extract description
description=$(grep -A 5 "^description:" .claude/agents/[agent-name].md | tail -n +2)

# Step 2: Manual review checklist
# - Grammar check (use grammar tool or manual review)
# - Sentence length (count words per sentence)
# - Tone assessment (professional vs casual)
# - Flow assessment (logical progression)

# Step 3: Readability scoring (optional)
# Use readability formulas (Flesch-Kincaid, Gunning Fog) if needed
```

**Evidence Format**:
```markdown
**Natural Language Quality Score**: X/5

**Grammar**: ✅ No errors OR ❌ [list errors]
**Tone**: ✅ Professional OR ❌ [issues]
**Sentence Length**: Avg [X] words, Max [Y] words
**Flow**: ✅ Logical progression OR ❌ [issues]

**Improvements Suggested**: [if score <5]

**Result**: X/5
```

**Examples**:

✅ **GOOD**:
```
"Expert code review specialist. Proactively reviews code for quality,
security, and maintainability. Use immediately after writing or modifying code."

Grammar: ✅ Correct
Tone: ✅ Professional ("Expert", "Proactively")
Sentence Length: 5, 9, 9 words (avg 7.7, well under 30)
Flow: ✅ Role → Action → Trigger
Natural language quality ✅
```

❌ **BAD**:
```
"Does code stuff and things when u need help lol also can review idk"

Grammar: ❌ No capitalization, "u" instead of "you", "lol", "idk"
Tone: ❌ Casual, unprofessional
Sentence Length: 12 words (single run-on)
Flow: ❌ No structure
Poor natural language quality ❌
```

---

### ✅ Criterion 6: Token Efficiency (QUANTITATIVE)

**Question Answered**: "Is the description using tokens optimally?"

**Requirements**:
- [ ] **Target range**: 90-110 tokens (optimal), 80-120 tokens (acceptable)
- [ ] Character count: ~360-440 characters for optimal range
- [ ] No redundant phrases (e.g., "This agent is a specialist that specializes in...")
- [ ] No filler words (e.g., "basically", "essentially", "generally")
- [ ] Information density: Every token adds value

**CRITICAL**: This criterion is **EXCLUSIVE to claude-code-ecosystem** (requires Bash tool + token analysis expertise)

**Validation Method** (claude-code-ecosystem ONLY):

```bash
# Step 1: Extract description
description=$(python -c "
import yaml
import sys

with open('.claude/agents/[agent-name].md', 'r') as f:
    content = f.read()
    # Extract YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1])
            print(metadata.get('description', ''))
        else:
            print('ERROR: Invalid YAML frontmatter', file=sys.stderr)
            sys.exit(1)
    else:
        print('ERROR: No frontmatter found', file=sys.stderr)
        sys.exit(1)
")

# Step 2: Count tokens using calculate_tokens.py
AGENT_NAME=claude-code-ecosystem uv run python scripts/calculate_tokens.py \
  --text "$description" \
  --format=json \
  --model=claude-3

# Output format:
# {
#   "token_count": 105,
#   "char_count": 420,
#   "model": "claude-3"
# }

# Step 3: Calculate score based on token count
# Scoring formula:
# - 90-110 tokens: 1.0 (optimal)
# - 80-89 or 111-120 tokens: 0.7 (acceptable)
# - 60-79 or 121-150 tokens: 0.5 (suboptimal)
# - <60 or >150 tokens: 0.3 (out of range)

# Step 4: Check for redundancy and filler
echo "$description" | grep -iE "basically|essentially|generally|actually|really|very|quite"
# Found = potential inefficiency

# Step 5: Manual information density review
# Count unique concepts vs total tokens (aim for ≥0.3 concepts/token)
```

**Token Scoring Formula**:

```python
def calculate_token_efficiency_score(token_count: int) -> tuple[float, str]:
    """
    Calculate token efficiency score (0.0-1.0) and grade.

    Returns: (score, grade)
    """
    if 90 <= token_count <= 110:
        return (1.0, "OPTIMAL")
    elif 80 <= token_count <= 120:
        return (0.7, "ACCEPTABLE")
    elif 60 <= token_count <= 150:
        return (0.5, "SUBOPTIMAL")
    else:
        return (0.3, "OUT_OF_RANGE")
```

**Evidence Format**:
```markdown
**Token Efficiency Score**: X/5

**Token Count**: [count]
**Character Count**: [count]
**Model**: claude-3
**Efficiency Grade**: OPTIMAL/ACCEPTABLE/SUBOPTIMAL/OUT_OF_RANGE

**Scoring Breakdown**:
- Raw score: [0.3-1.0]
- Scaled to /5: [score × 5]

**Redundancy Check**:
- ✅ No redundant phrases OR ❌ [list redundant phrases]

**Filler Words**:
- ✅ No filler words OR ❌ [list filler words]

**Information Density**:
- Unique concepts: [count]
- Concepts per token: [ratio]
- ✅ ≥0.3 OR ❌ <0.3

**Optimization Recommendations**: [if score <1.0]
```

**Examples**:

✅ **GOOD**:
```
Description: "Expert code review specialist. Proactively reviews code for quality,
security, and maintainability. Use immediately after writing or modifying code."

Token count: 23 tokens (WAIT - this is TOO SHORT for standalone, but acceptable if combined with other metadata)
Character count: ~120 chars

Note: This is a SHORT description. For complete descriptions (90-110 tokens),
would need more detail while maintaining efficiency.
```

✅ **OPTIMAL EXAMPLE** (hypothetical):
```
Description: "Python implementation specialist for packages/**, tests/**, and core modules.
Proactively handles FastAPI route handlers, SQLAlchemy models, async patterns, and type safety.
Use immediately for implementation tasks, pre-flight validation, and dependency management.
Integrates with code-quality for quality assurance and debugger for error resolution."

Token count: ~95 tokens (OPTIMAL range)
Character count: ~380 chars
Information density: 12 concepts / 95 tokens = 0.13 concepts/token
No redundancy, no filler words ✅
```

❌ **BAD** (TOO LONG):
```
Description: "This agent is basically a specialist that specializes in the domain
of Python programming language implementation work, and it generally can help with
essentially all tasks related to writing code in the packages directory and also
the tests directory. It's really quite useful for actually implementing features
and also creating new modules. You can essentially use this agent for very many
different kinds of implementation activities."

Token count: ~180 tokens (OUT OF RANGE - too long)
Redundancy: "specialist that specializes", "essentially" (3x), "basically", "really quite"
Filler words: basically, essentially, generally, actually, really, quite, very
Information density: 5 concepts / 180 tokens = 0.03 concepts/token (POOR)
Multiple inefficiencies ❌
```

---

## Overall Scoring Rubric

**Alignment Quality Score** = Weighted average of 6 criteria

| **Criterion** | **Weight** | **Max Points** |
|--------------|-----------|---------------|
| 1. Capability Accuracy | 25% | 1.25 |
| 2. Scope Completeness | 20% | 1.00 |
| 3. No Misleading Claims | 20% | 1.00 |
| 4. Boundary Clarity | 15% | 0.75 |
| 5. Natural Language Quality | 10% | 0.50 |
| 6. Token Efficiency | 10% | 0.50 |
| **TOTAL** | **100%** | **5.00** |

**Grading Scale**:

| **Total Score** | **Grade** | **Interpretation** | **Action** |
|----------------|-----------|-------------------|------------|
| **4.5-5.0** | A+ | Excellent alignment - Production ready | PASS - No changes needed |
| **4.0-4.4** | A | Strong alignment - Minor improvements optional | PASS - Consider optimizations |
| **3.5-3.9** | B+ | Good alignment - Some improvements recommended | CONSIDER - Address low-scoring criteria |
| **3.0-3.4** | B | Adequate alignment - Improvements needed | REVISE - Focus on accuracy/completeness |
| **2.5-2.9** | C | Weak alignment - Significant revisions required | FAIL - Major rewrite |
| **<2.5** | D/F | Poor alignment - Complete rewrite required | FAIL - Start over |

**Confidence Threshold**: ≥4.0/5.0 recommended for production agents (80%+ alignment quality)

---

## Complete Validation Workflow (claude-code-ecosystem)

### Step-by-Step Process

```markdown
## Description Alignment Analysis

**Agent**: [agent-name]
**Date**: [YYYY-MM-DD]
**Reviewer**: claude-code-ecosystem

---

### STEP 1: Extract Description

```bash
description=$(python -c "
import yaml
with open('.claude/agents/[agent-name].md', 'r') as f:
    content = f.read()
    if content.startswith('---'):
        parts = content.split('---', 2)
        metadata = yaml.safe_load(parts[1])
        print(metadata.get('description', ''))
")

echo "$description"
```

**Description Text**:
```
[paste extracted description]
```

---

### STEP 2: Criterion 1 - Capability Accuracy

**Capabilities Claimed**:
1. [capability 1]
2. [capability 2]
3. [capability 3]

**Verification** (grep against prompt):
```bash
grep -i "[capability 1 keyword]" .claude/agents/[agent-name].md
grep -i "[capability 2 keyword]" .claude/agents/[agent-name].md
grep -i "[capability 3 keyword]" .claude/agents/[agent-name].md
```

**Results**:
- [capability 1]: ✅/❌ (line X)
- [capability 2]: ✅/❌ (line Y)
- [capability 3]: ✅/❌ (line Z)

**Exaggerated Claims Check**:
```bash
echo "$description" | grep -iE "perfect|always|never|100%|comprehensive|complete"
```
**Results**: [list or "none found"]

**Score**: X/5 (X capabilities verified / Y total claimed)

---

### STEP 3: Criterion 2 - Scope Completeness

**Top Capabilities from Prompt** (Primary Responsibilities section):
```bash
grep -A 50 "^## Primary Responsibilities" .claude/agents/[agent-name].md
```

**Extracted Top 5**:
1. [primary capability 1]
2. [primary capability 2]
3. [primary capability 3]
4. [secondary capability 4]
5. [secondary capability 5]

**Coverage Analysis**:
- [capability 1]: ✅/❌ in description
- [capability 2]: ✅/❌ in description
- [capability 3]: ✅/❌ in description
- [capability 4]: ✅/❌ in description
- [capability 5]: ✅/❌ in description

**Coverage**: X/5 = Y%

**Score**: X/5 (based on coverage: 100%=5, 80%=4, 60%=3, 40%=2, 20%=1, 0%=0)

---

### STEP 4: Criterion 3 - No Misleading Claims

**Scope Overreach Check**:
```bash
echo "$description" | grep -iE "all|any|every|complete|comprehensive|full"
grep -A 10 "^## Boundaries" .claude/agents/[agent-name].md
```

**Potential Misleading Statements**:
1. "[claim 1]" - ✅/❌/⚠️ (verified against boundaries)
2. "[claim 2]" - ✅/❌/⚠️

**Technology Mismatches**: [list or "none"]
**Scope Overreach**: [list or "none"]

**Score**: X/5 (5 = no misleading claims, deduct 1 per misleading claim)

---

### STEP 5: Criterion 4 - Boundary Clarity

**Scope Specificity**:
```bash
echo "$description" | grep -iE "packages/|\.claude/|docs/|tests/|k8s/"
```
**Result**: [specific directories listed] OR [generic terms only]

**Technology Specificity**:
```bash
echo "$description" | grep -iE "pytest|fastapi|sqlalchemy|prometheus|grafana"
```
**Result**: [specific tools listed] OR [generic categories only]

**Differentiation from Similar Agents**:
- vs [agent-1]: [clear difference description]
- vs [agent-2]: [clear difference description]

**Score**: X/5 (5 = crystal clear, 3 = some ambiguity, 1 = completely unclear)

---

### STEP 6: Criterion 5 - Natural Language Quality

**Grammar Check**: ✅/❌ [list errors if any]
**Tone Assessment**: ✅ Professional OR ❌ [issues]
**Sentence Length Analysis**:
- Sentence 1: [X] words
- Sentence 2: [Y] words
- Sentence 3: [Z] words
- Average: [avg] words (target: 15-20, max: 30)

**Flow Assessment**: ✅ Logical OR ❌ [issues]

**Score**: X/5 (all criteria met = 5, deduct 1 per issue)

---

### STEP 7: Criterion 6 - Token Efficiency (QUANTITATIVE)

**Token Count**:
```bash
AGENT_NAME=claude-code-ecosystem uv run python scripts/calculate_tokens.py \
  --text "$description" \
  --format=json \
  --model=claude-3
```

**Results**:
```json
{
  "token_count": [X],
  "char_count": [Y],
  "model": "claude-3"
}
```

**Efficiency Grade**:
- 90-110 tokens: OPTIMAL (1.0)
- 80-120 tokens: ACCEPTABLE (0.7)
- 60-150 tokens: SUBOPTIMAL (0.5)
- Other: OUT_OF_RANGE (0.3)

**Grade**: [OPTIMAL/ACCEPTABLE/SUBOPTIMAL/OUT_OF_RANGE]
**Raw Score**: [0.3-1.0]
**Scaled Score**: [raw × 5] / 5

**Redundancy Check**:
```bash
echo "$description" | grep -iE "basically|essentially|generally|actually|really|very|quite"
```
**Results**: ✅ None found OR ❌ [list filler words]

**Information Density**:
- Unique concepts: [count]
- Tokens: [count]
- Ratio: [concepts/tokens]
- ✅ ≥0.3 OR ❌ <0.3

**Score**: X/5 (based on efficiency grade × 5)

---

### FINAL SCORING

| **Criterion** | **Weight** | **Score** | **Weighted** |
|--------------|-----------|-----------|-------------|
| Capability Accuracy | 25% | X/5 | X × 0.25 |
| Scope Completeness | 20% | X/5 | X × 0.20 |
| No Misleading Claims | 20% | X/5 | X × 0.20 |
| Boundary Clarity | 15% | X/5 | X × 0.15 |
| Natural Language Quality | 10% | X/5 | X × 0.10 |
| Token Efficiency | 10% | X/5 | X × 0.10 |
| **TOTAL** | **100%** | — | **X.XX/5.00** |

**Grade**: [A+/A/B+/B/C/D/F]
**Decision**: PASS/REVISE/FAIL

**Recommendations**: [if score <4.0]
1. [recommendation 1]
2. [recommendation 2]
3. [recommendation 3]

---
```

---

## Responsibility Separation

**claude-code-ecosystem (this checklist)**:
- ✅ Runs token counter (has Bash tool + token analysis expertise)
- ✅ Analyzes description-to-prompt alignment
- ✅ Evaluates token efficiency quantitatively
- ✅ Validates capability accuracy
- ✅ Assesses natural language quality

**claude-code-ecosystem (description-delegation-checklist.md)**:
- ✅ Evaluates delegation effectiveness
- ✅ Checks orchestrator selection triggers
- ✅ Validates domain keywords
- ❌ Does NOT run token counter (no duplication)
- ❌ Does NOT analyze alignment (different focus)

**No Overlap**: Each agent has exclusive responsibility for their checklist.

---

## Official Claude Code Examples

**Source**: Claude Code official agent descriptions (validated for alignment quality)

### Example Analysis: Code Review Specialist

```
Description: "Expert code review specialist. Proactively reviews code for quality,
security, and maintainability. Use immediately after writing or modifying code."

Token count: ~23 tokens (NOTE: This is SHORT - actual descriptions should be 90-110)
Character count: ~120 chars

Analysis:
1. Capability Accuracy: 5/5 (reviews, quality, security, maintainability all in prompt)
2. Scope Completeness: 4/5 (covers main capabilities, could mention standards/frameworks)
3. No Misleading Claims: 5/5 (no exaggerations, clear scope)
4. Boundary Clarity: 4/5 (clear role, could specify file types)
5. Natural Language Quality: 5/5 (perfect grammar, professional tone, concise)
6. Token Efficiency: 3/5 (too short for standalone, but acceptable as brief description)

Overall: 4.3/5 (A grade)
```

---

## Key Reminders

1. **This checklist focuses on accuracy + token efficiency** - NOT delegation quality (see description-delegation-checklist.md)

2. **claude-code-ecosystem EXCLUSIVELY runs token counter** - claude-code-ecosystem does NOT (no duplication)

3. **Target token range: 90-110 tokens** (optimal), 80-120 tokens (acceptable)

4. **Character count correlation**: ~360-440 chars for optimal token range

5. **Information density matters**: Aim for ≥0.3 unique concepts per token

6. **Every token must add value** - No redundancy, no filler words

7. **Capability accuracy is weighted highest** (25%) - Misleading descriptions break trust

---

## See Also

- **description-delegation-checklist.md** - Orchestrator delegation effectiveness (claude-code-ecosystem)
- **golden-agent-standards.md** - Reference examples of excellent agent design
- **agent-standards-extended.md** - Complete agent design standards and patterns
- **scripts/calculate_tokens.py** - Token counting script (claude-code-ecosystem tool)

---

**Version**: 1.0
**Last Updated**: 2025-11-21
**Maintained By**: claude-code-ecosystem

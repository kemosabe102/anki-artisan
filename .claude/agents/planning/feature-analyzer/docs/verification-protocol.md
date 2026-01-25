# Feature Analyzer - Verification Protocol

**Purpose**: Provide orchestrator-executable verification commands to validate feature-analyzer recommendations with auditability and reproducibility.

**Audience**: Orchestrator (Claude Code) - validates feature-analyzer analysis before accepting recommendations.

**Important Note**: The commands in this guide are for **orchestrator execution via Bash tool**, not for agent execution. The feature-analyzer agent uses Grep tool (Claude Code tool) for internal analysis.

---

## Overview

**Auditability Principle**: Every major recommendation (merge/separate/refactor) should include <=2 verification commands that the orchestrator can run to validate overlap claims, conflict detection, or synergy identification.

**Benefits**:
- Orchestrator can verify claims before accepting recommendation
- Reproducible analysis (same inputs -> same verification outputs)
- Catch analysis errors early (if verification fails, flag for review)
- Build trust in agent recommendations through transparency

---

## Command Types

### 1. Quick Check (Always Include)

**Purpose**: Validate overlap claim or requirement count

**Tool**: `grep` with count flag `-c` or simple file inspection

**When to Use**: All recommendations (merge/separate/refactor)

**Example Commands**:

```bash
# Count duplicate requirements
grep -c "FR-XXX" docs/01-planning/specifications/feature_{a,b}/SPEC.md

# Count entity mentions
grep -c "StateManager" docs/01-planning/specifications/012-feature-a/SPEC.md

# Verify requirement overlap
grep -ri "state management\|checkpoint\|recovery" docs/01-planning/specifications/{012-feature-a,013-feature-b}/ | wc -l
```

**Expected Output**: Numeric count matching analysis claim

**Interpretation**: Confirms overlap percentage calculation accuracy

---

### 2. Deep Validation (For Merge/Refactor Recommendations)

**Purpose**: Show exact overlap or conflict evidence with file:line references

**Tool**: `diff`, `grep` with context, or entity extraction

**When to Use**: Merge or refactor recommendations requiring detailed evidence

**Example Commands**:

```bash
# Show exact shared entities with file:line
grep -n "StateManager" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md

# Compare entity lists
diff <(grep "^- " feature_a_entities.txt | sort) <(grep "^- " feature_b_entities.txt | sort)

# Show requirement overlap with context
grep -A 2 -B 2 "checkpoint" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md
```

**Expected Output**: File:line references or diff output showing exact overlaps

**Interpretation**: Validates specific overlap claims with concrete evidence

---

## Verification Output Format

### Standard Structure

```json
{
  "verification_commands": [
    {
      "purpose": "Validate 41.7% requirement overlap claim",
      "command": "grep -ri \"state management\\|checkpoint\\|recovery\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/ | wc -l",
      "expected_output": "15 duplicate requirements found across 36 total",
      "interpretation": "Confirms 15/36 = 41.7% overlap as claimed"
    },
    {
      "purpose": "Verify shared StateManager entity",
      "command": "grep -n \"StateManager\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "feature-a/SPEC.md:145:StateManager\\nfeature-b/SPEC.md:203:StateManager",
      "interpretation": "Both features reference StateManager entity, confirming infrastructure overlap"
    }
  ]
}
```

---

## When to Include Verification

### MERGE Recommendations

**Required Verification** (2 commands):
1. **Overlap % validation**: Verify >70% overlap claim
2. **Shared entity count**: Confirm infrastructure overlap claim

**Example**:
```json
{
  "verification_commands": [
    {
      "purpose": "Validate 82.5% overlap claim",
      "command": "grep -c \"Checkpoint\\|ValidationState\\|StateManager\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "Feature A: 18 matches, Feature B: 15 matches -> High shared entity density",
      "interpretation": "Confirms >70% overlap threshold for merge decision"
    },
    {
      "purpose": "Verify shared infrastructure (90% claim)",
      "command": "grep -n \"StateManager\\|CheckpointConfig\\|RecoveryHandler\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md | wc -l",
      "expected_output": "27 total references across both features",
      "interpretation": "Both features heavily reference shared components (90% infrastructure overlap)"
    }
  ]
}
```

---

### REFACTOR Recommendations

**Required Verification** (2 commands):
1. **Shared foundation validation**: Verify infrastructure overlap claim (typically 50-70%)
2. **Distinct value proposition check**: Confirm responsibility separation claim

**Example**:
```json
{
  "verification_commands": [
    {
      "purpose": "Validate 65% infrastructure overlap (StateManager foundation)",
      "command": "grep -c \"StateManager\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "Feature A: 3, Feature B: 2 -> 5 total references",
      "interpretation": "Both features depend on StateManager, justifying extraction"
    },
    {
      "purpose": "Verify distinct responsibilities (25% responsibility overlap)",
      "command": "grep -E \"^Core Responsibility:\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "Feature A: checkpointing\\nFeature B: context monitoring",
      "interpretation": "Different core purposes despite shared infrastructure (refactor appropriate)"
    }
  ]
}
```


---

### SEPARATE Recommendations

**Required Verification** (1 command):
- **Overlap validation**: Verify <30% overlap claim

**Example**:
```json
{
  "verification_commands": [
    {
      "purpose": "Validate <30% overlap claim (5% actual)",
      "command": "diff <(grep -oP \"(?<=Entity: ).*\" docs/01-planning/specifications/012-feature-a/SPEC.md | sort) <(grep -oP \"(?<=Entity: ).*\" docs/01-planning/specifications/013-feature-b/SPEC.md | sort)",
      "expected_output": "No common entities found",
      "interpretation": "Confirms 0% entity overlap, supporting separate decision"
    }
  ]
}
```

---

### CONFLICT Findings

**Required Verification** (1 command):
- **Contradiction evidence**: Show conflicting requirements with file:line

**Example**:
```json
{
  "verification_commands": [
    {
      "purpose": "Verify circular dependency claim",
      "command": "grep -n \"depends on Feature [AB]\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "feature-a/SPEC.md:156:depends on Feature B\\nfeature-b/SPEC.md:203:depends on Feature A",
      "interpretation": "Circular dependency confirmed (A->B, B->A)"
    }
  ]
}
```


---

## Orchestrator Usage Pattern

### Workflow Integration

1. **Receive feature-analyzer recommendation**
2. **Extract verification_commands from output**
3. **Execute commands via Bash tool**
4. **Compare actual output to expected_output**
5. **Validate interpretation matches analysis**
6. **Accept or reject recommendation based on verification**

### Example Orchestrator Execution

```bash
# Orchestrator runs verification commands to validate analysis
$ grep -c "StateManager" docs/01-planning/specifications/012-feature-a/SPEC.md
3
$ grep -c "StateManager" docs/01-planning/specifications/013-feature-b/SPEC.md
2

# Output confirms both features use StateManager (5 total references)
# -> 65% infrastructure overlap claim validated
```

### Handling Verification Failures

**If verification fails** (actual != expected):
1. Flag recommendation for review
2. Request feature-analyzer to re-analyze with explicit validation
3. Document discrepancy in orchestrator logs
4. Consider lowering confidence in recommendation


**Example Failure**:
```bash
# Expected: 15 duplicate requirements
$ grep -ri "state management" docs/01-planning/specifications/{012-feature-a,013-feature-b}/ | wc -l
8

# Actual: Only 8 matches (not 15) -> Overlap claim inflated
# -> Reject merge recommendation, request re-analysis
```

---

## Command Reference

### Common Patterns

**Entity Overlap**:
```bash
# Count entity mentions
grep -c "EntityName" docs/01-planning/specifications/XXX-feature/SPEC.md

# Show entity definitions with line numbers
grep -n "class EntityName\|^EntityName:" docs/01-planning/specifications/XXX-feature/SPEC.md
```

**Requirement Overlap**:
```bash
# Count requirements matching pattern
grep -c "FR-[0-9]\{3\}" docs/01-planning/specifications/XXX-feature/SPEC.md

# Find duplicate requirements across features
comm -12 <(grep "^- FR" feature_a/SPEC.md | sort) <(grep "^- FR" feature_b/SPEC.md | sort)
```


**Dependency Analysis**:
```bash
# Show dependency graph
grep -n "depends on\|requires\|uses" docs/01-planning/specifications/XXX-feature/SPEC.md

# Detect circular dependencies
grep -E "Feature [AB].*depends on.*Feature [AB]" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md
```

**Infrastructure Overlap**:
```bash
# Count shared components
grep -c "StateManager\|HookName\|SchemaName" docs/01-planning/specifications/XXX-feature/SPEC.md

# Compare infrastructure lists
diff <(grep "^Infrastructure:" feature_a/SPEC.md | sort) <(grep "^Infrastructure:" feature_b/SPEC.md | sort)
```

---

## Anti-Patterns

### Do Not: Provide >2 verification commands per recommendation
**Why**: Analysis paralysis - orchestrator shouldn't need extensive validation
**Instead**: Provide 1-2 high-impact commands that validate core claims

### Do Not: Use complex multi-pipe commands requiring interpretation
**Why**: Verification should be simple and unambiguous
**Instead**: Use straightforward grep/diff commands with clear expected outputs

### Do Not: Omit expected_output or interpretation
**Why**: Orchestrator can't validate if unclear what to expect
**Instead**: Always include expected_output and interpretation fields


### Do Not: Verify every finding in the analysis
**Why**: Overwhelming and unnecessary (focus on decision-critical claims)
**Instead**: Verify only major recommendations (merge/separate/refactor decision, critical conflicts)

---

## Best Practices

### Do: Focus on decision-critical claims
- Verify overlap % for merge decisions (>70% threshold)
- Verify shared infrastructure for refactor decisions (30-70% range)
- Verify conflict evidence for critical conflicts

### Do: Use file:line references
- Enables orchestrator to jump to exact specification location
- Provides concrete evidence for manual review if needed

### Do: Keep commands portable
- Use POSIX-compliant commands (grep, diff, wc)
- Avoid environment-specific paths or aliases
- Test commands in orchestrator environment before including

### Do: Provide clear interpretation
- Explain what the output means for the recommendation
- Connect verification result to decision rationale
- Make pass/fail criteria explicit

---

## Example: Complete Verification Block

```json
{
  "recommended_action": {
    "action": "refactor",
    "confidence": 0.85,
    "rationale": "30-70% overlap triggers refactor. Shared infrastructure (65%) justifies StateManager extraction. Distinct value propositions (checkpointing vs monitoring) justify keeping features separate after foundation."
  },
  "verification_commands": [
    {
      "purpose": "Validate 65% infrastructure overlap claim",
      "command": "grep -c \"StateManager\\|ProgressTracker\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "Feature A: 5 matches, Feature B: 3 matches -> Shared foundation confirmed",
      "interpretation": "Both features heavily use StateManager/ProgressTracker, justifying extraction (65% infrastructure overlap validated)"
    },
    {
      "purpose": "Verify distinct responsibilities (25% responsibility overlap)",
      "command": "grep -n \"^Core Responsibility:\" docs/01-planning/specifications/{012-feature-a,013-feature-b}/SPEC.md",
      "expected_output": "feature-a/SPEC.md:15:Core Responsibility: Progressive checkpointing\\nfeature-b/SPEC.md:18:Core Responsibility: Context size monitoring",
      "interpretation": "Different core purposes confirmed (checkpointing != monitoring), supporting refactor over merge"
    }
  ]
}
```

---

**See Also**:
- `./response-examples.md` for complete JSON response structures
- `../examples/simulation-examples.md` for walkthrough examples with verification
- `../feature-analyzer.md` for agent methodology

# Error Handling & Recovery

Complete error recovery patterns for the `/create-agent` command workflow.

---

## A. Definition Parse Failures (Phase 1)

**Scenario**: Agent definition file malformed, missing required fields, invalid format

**Orchestrator Action**: Stop workflow, report validation errors with guidance

**Example Output**:
```text
Definition Parse FAILED

Validation Errors:
- Missing required field: 'purpose' (line 5)
- Invalid agent name format: 'my agent' (should be kebab-case: 'my-agent')
- Domain scope not recognized: 'custom/' (must be .claude/**, packages/**, docs/**, etc.)

Template Reference: .claude/templates/agent-definition-input.template.md

Workflow STOPPED. Fix definition file and re-run.
```

### Recovery Options

1. **Fix and Retry (RECOMMENDED)**:
   ```bash
   # Edit definition file to fix errors
   # Re-run command
   /create-agent path/to/fixed-definition.md
   ```

2. **Use Interactive Mode**:
   ```bash
   # Start fresh with guided Q&A
   /create-agent --create-definition new-agent.md
   ```

3. **Validate Template Compliance**:
   - Compare against `.claude/templates/agent-definition-input.template.md`
   - Ensure all required sections present
   - Check naming conventions (kebab-case)

---

## B. Duplicate Agent Detection (Phase 1)

**Scenario**: Agent with same name or overlapping capabilities already exists

**Orchestrator Action**: Present duplicate analysis, offer options

**Example Output**:
```text
Duplicate Detection: CONFLICT FOUND

Proposed: python-analyzer
Existing: code-quality (similarity: 0.85)

Overlap Analysis:
- 4 of 6 proposed capabilities overlap with code-quality
- Same domain scope: packages/**
- Similar purpose statement

Recommendations:
1. RENAME: Choose distinct name (e.g., 'python-performance-analyzer')
2. MERGE: Enhance existing code-quality with new capabilities
3. CANCEL: Abort agent creation
```

### Recovery Options

1. **Rename Agent**:
   - Update definition file with unique name
   - Differentiate purpose statement
   - Re-run `/create-agent`

2. **Merge with Existing**:
   - Use claude-code-ecosystem to enhance existing agent
   - `Task(claude-code-ecosystem, "Enhance code-quality with capabilities: [list]")`

3. **Proceed Anyway** (if genuinely distinct):
   - Confirm to orchestrator that agents serve different purposes
   - Document distinction in agent purpose

---

## C. Research Confidence Failures (Phase 4)

**Scenario**: Research workers return low confidence (<0.7) for critical topics

**Orchestrator Action**: Auto-retry with refined queries (max 2 iterations)

**Example Output**:
```text
Research Iteration 1: PARTIAL SUCCESS

Topics with low confidence:
- "OWASP security patterns for agents" (confidence: 0.45)
  Reason: Generic results, need more specific query
- "Agent error recovery best practices" (confidence: 0.62)
  Reason: Found patterns but lacking examples

Refining queries for iteration 2...

Iteration 2 Results:
- "OWASP security patterns for agents" (confidence: 0.78) - PASS
- "Agent error recovery best practices" (confidence: 0.71) - PASS

Proceeding to Phase 5.
```

### Recovery Options

1. **Automatic Re-Research** (default):
   - Orchestrator refines queries based on failure reasons
   - Max 2 iterations
   - If still <0.7 after iterations: escalate

2. **Manual Context Provision**:
   ```bash
   # Provide additional context directory
   /create-agent definition.md --context-dir=docs/security-patterns/
   ```

3. **Accept Lower Confidence**:
   - Acknowledge gaps will exist in generated documentation
   - Plan for manual documentation enhancement post-creation

4. **Expand Research Sources**:
   - Request orchestrator to include additional researcher agents
   - `researcher-external` for external sources and library-specific docs (auto-routes)

---

## D. Quality Gate Failures (Phase 8)

**Scenario**: Agent fails quality validation (template, documentation, prompt, context, or matrix)

**Orchestrator Action**: Present detailed failure report, offer fix options

**Example Output**:
```text
Quality Validation: FAILED (2 of 5 validators)

FAILED: Template Compliance
- YAML frontmatter not on line 1 (found on line 3)
- Tools field is YAML list (should be comma-separated string)
- Missing section: "Error Recovery"

FAILED: Quality Matrix (Score: 58/100)
- Role clarity: 3/5 (boundary with similar agents unclear)
- Error recovery: 2/5 (incomplete failure handling)
- Validation coverage: 2/5 (no quality gates defined)

PASSED: Documentation Health (85/100)
PASSED: Prompt Quality (no high-severity anti-patterns)
PASSED: Context Optimization (4,200 tokens)

Options:
1. AUTO-FIX: Delegate fixes to claude-code-ecosystem (recommended)
2. MANUAL FIX: Edit files, re-run validation
3. SKIP VALIDATION: Proceed anyway (HIGH RISK - not recommended)
```

### Recovery Options

1. **Auto-Fix (RECOMMENDED)**:
   - Orchestrator delegates to claude-code-ecosystem for template fixes
   - Re-validates after fixes (max 3 attempts)
   - If still failing: escalate to manual fix

2. **Manual Fix + Re-Validate**:
   ```bash
   # Edit agent file to fix issues
   # Re-run validation only
   /create-agent definition.md  # Will detect existing partial work
   ```

3. **Skip Validation (HIGH RISK)**:
   ```bash
   /create-agent definition.md --skip-validation
   ```
   - **Risk**: Agent may not function correctly
   - **Use only for**: Rapid prototyping, experimental agents

### Quality Gate Thresholds

| Gate | PASS | CONDITIONAL | FAIL |
|------|------|-------------|------|
| Template Compliance | 100% | N/A | <100% |
| Documentation Health | >=80 | 60-79 | <60 |
| Prompt Quality | No HIGH | MEDIUM only | Any HIGH |
| Context Optimization | <=5000 tokens | 5000-7000 | >7000 |
| Quality Matrix | >=70/100 | 60-69 | <60 |

---

## E. User Cancellation (Phase 9)

**Scenario**: User chooses to cancel after reviewing agent summary

**Orchestrator Action**: Clean up partial artifacts, confirm cancellation

**Example Output**:
```text
User requested: CANCEL

Cleaning up partial artifacts...
- Removed: .claude/agents/dev-tools/my-agent/ (directory)
- Preserved: Original definition file (user input)

Cancellation complete. No agent created.

To try again:
- Modify definition file
- Run: /create-agent path/to/definition.md
```

### Cleanup Actions

1. **Remove Created Directories**:
   - `.claude/agents/{domain}/{agent-name}/` (entire directory)

2. **Preserve User Input**:
   - Original definition file (user created)
   - Context directory (if provided via --context-dir)

3. **No Integration Updates**:
   - CLAUDE.md not modified
   - orchestrator-workflow.md not modified
   - DOC-INDEX.md not modified

---

## F. Interactive Mode Errors

### Vague User Idea (Phase I-1)

**Scenario**: User provides insufficient description

**Example Output**:
```text
Idea Analysis: INSUFFICIENT DETAIL

Your idea: "An agent that helps with code"

Missing information:
- What specific problem does it solve?
- What actions does the agent perform?
- When should the orchestrator call this agent?

Please provide more detail using the "What, How, When" framework:
- WHAT: What problem does this agent solve?
- HOW: What specific actions does it take?
- WHEN: When should it be called vs other agents?

Example: "An agent that analyzes Python code for performance bottlenecks
by profiling function execution times and memory usage. Call it when
optimizing slow code paths after functionality is correct."
```

**Recovery**: Re-prompt with guidance (max 3 attempts before suggesting manual template)

### Analysis Failure (Phase I-2)

**Scenario**: claude-code-ecosystem cannot generate structured proposal

**Recovery Options**:
1. Extract `missing_information` from failure_details
2. Re-prompt user for specific clarifications
3. Offer: Rephrase idea, Provide more detail, or Cancel

### Generation Failure (Phase I-4)

**Scenario**: claude-code-ecosystem cannot generate definition file

**Recovery Options**:
1. Show `failure_details.reasons` to user
2. Offer: Retry generation, Return to refinement, or Cancel

---

## Error Recovery Patterns

### Pattern 1: Iterative Fix Loop

**Use For**: Quality gate failures, template compliance issues

```text
/create-agent definition.md
|
FAIL (quality gates)
|
Auto-fix via claude-code-ecosystem
|
Re-validate (attempt 2 of 3)
|
PASS -> Continue to Phase 9
|
or FAIL -> Escalate to user
```

### Pattern 2: Research Refinement

**Use For**: Low confidence research results

```text
Phase 4: Research
|
Confidence < 0.7 for topic X
|
Refine query based on failure reason
|
Re-research (iteration 2 of 2)
|
Confidence >= 0.7 -> Continue
|
or Still < 0.7 -> Accept with documented gaps
```

### Pattern 3: User Decision Points

**Use For**: Duplicate detection, final approval

```text
Phase 1 or 9: Decision required
|
Present options with clear trade-offs
|
Wait for user input
|
Execute user's choice
|
Continue or Cancel based on choice
```

---

## Iteration Limits

| Phase | Max Iterations | Escalation Action |
|-------|---------------|-------------------|
| Phase 1 (Parse) | 1 | User must fix definition file |
| Phase 4 (Research) | 2 | Accept with documented gaps |
| Phase 8 (Validation) | 3 | Present manual fix options |
| Phase 9 (Refinement) | Unlimited | User-driven |
| Interactive Mode | 3 per phase | Suggest manual template |

---

## Dry-Run Mode Behavior

When `--dry-run` flag provided:

1. Execute all phases through Phase 9
2. **DO NOT** write any files in Phase 10
3. Present complete summary of what WOULD be created
4. Include all file paths and content previews
5. User can review before running without --dry-run

```bash
/create-agent definition.md --dry-run

# Output shows:
# - All validation results
# - Proposed file structure
# - Content previews (first 50 lines each)
# - Quality scores
# - Integration changes that WOULD be made
```

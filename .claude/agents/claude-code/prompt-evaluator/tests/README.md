# Prompt Evaluator Test Cases

## Purpose
Validation examples for verifying prompt-evaluator accuracy and consistency.

## Test Categories

### 1. `valid-agents/` - Well-formed agents that should evaluate successfully
- **grade-a-agent.md** - High-quality agent meeting all 16 structural criteria (target: Grade A, score >= 4.5)
- **grade-c-agent.md** - Mediocre agent with gaps (target: Grade C, score 2.5-3.49)

### 2. `invalid-agents/` - Malformed agents that should produce specific failures
- **empty-agent.md** - Empty file (expected: FAILURE, type: INVALID_CONTENT)
- **no-frontmatter.md** - Agent without YAML frontmatter (expected: FAILURE, type: INVALID_PATH or partial evaluation)

### 3. `expected-outputs/` - Expected JSON outputs for each test case
- **grade-a-agent.json** - Expected SUCCESS output with high scores
- **grade-c-agent.json** - Expected SUCCESS output with medium scores

## Running Tests

### Manual Validation
```bash
# Evaluate a test agent
Task(prompt-evaluator, "Evaluate .claude/agents/dev-tools/prompt-evaluator/tests/valid-agents/grade-a-agent.md")

# Compare output against expected
# Variance threshold: Grade +/-1, Score +/-0.3
```

### Validation Criteria
| Metric | Tolerance | Notes |
|--------|-----------|-------|
| Overall Grade | +/- 1 letter | A->B acceptable, A->C failure |
| Weighted Score | +/- 0.3 | 4.5->4.2 acceptable |
| Structural Score | +/- 2/16 | 16/16->14/16 acceptable |
| Confidence | +/- 0.1 | 0.9->0.8 acceptable |

## Test Case Design Philosophy

### Grade A Agent (grade-a-agent.md)
Minimal but complete agent demonstrating:
- Valid YAML frontmatter with all required fields
- Clear single responsibility
- Schema reference and base pattern extension
- Complete workflow structure
- Proper error handling
- Tool descriptions meeting "new team member" standard

### Grade C Agent (grade-c-agent.md)
Intentionally mediocre agent with:
- Valid frontmatter but minimal description
- Vague scope definition
- Missing or incomplete workflow phases
- No error handling documentation
- Generic tool descriptions

### Invalid Agents
Test error handling paths:
- Empty file tests FILE_UNREADABLE or INVALID_CONTENT handling
- Missing frontmatter tests parser resilience

## Adding New Test Cases

1. Create agent file in appropriate category folder
2. Document expected grade/score in this README
3. Create expected output JSON in `expected-outputs/`
4. Run evaluation and verify within tolerance

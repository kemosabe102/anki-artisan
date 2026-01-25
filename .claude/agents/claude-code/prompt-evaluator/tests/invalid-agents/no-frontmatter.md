# Agent Without Frontmatter

This agent definition is missing the required YAML frontmatter block.

## What It Does

This is a test file to verify the prompt-evaluator correctly handles
agents that are missing the required `---` delimited YAML frontmatter.

## Expected Behavior

The prompt-evaluator should detect the missing frontmatter and either:
1. Return FAILURE with type INVALID_PATH or similar
2. Return partial evaluation with structural_quality failures

## Tools

- Read
- Grep

## Workflow

1. Input
2. Process
3. Output

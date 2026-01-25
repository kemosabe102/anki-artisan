---
name: test-grade-c-agent
description: 'Mediocre test agent with gaps.'
model: sonnet
tools: Read, Grep
---

# Test Grade-C Agent

A test agent for validating prompt-evaluator can detect quality issues.

## What It Does

This agent reads files and does some analysis. It can be used for testing.

## How to Use

Give it a file path and it will analyze it.

## Tools

- Read - reads files
- Grep - searches for patterns

## Workflow

1. Get input
2. Do analysis
3. Return results

## Errors

If something goes wrong, it will fail.

## Output

Returns JSON with findings.

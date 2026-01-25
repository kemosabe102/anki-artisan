# Workflow Agent Delegation Examples

How the orchestrator delegates tasks to the workflow agent.

---

## Build Workflow

```
Task(workflow, "Build a new slash command workflow for automated code review that integrates linting (ruff), type checking (mypy), and test execution (pytest). Target maturity: MVP.")
```

**Expected Input Context**:
- Workflow name and purpose
- Integration points (tools, agents)
- Maturity target

---

## Sync Ecosystem

```
Task(workflow, "Sync ecosystem after plan-enhancer agent updates. Update workflow registry with new capabilities, synchronize CLAUDE.md agent references, and update living sprint progress. Operation ID: 01HXYZ123ABC. Apply mode: dry-run first.")
```

**Expected Input Context**:
- Documents to sync
- Operation ID for idempotency
- Apply mode (dry-run/commit)

---

## Optimize Workflow

```
Task(workflow, "Analyze and optimize the /code-review workflow. Current bottleneck: multiple sequential tool calls causing 30+ second delays. Goal: reduce to under 15 seconds through parallelization.")
```

**Expected Input Context**:
- Workflow name
- Optimization goals
- Bottleneck indicators

---

## Create Command

```
Task(workflow, "Create a new /deploy slash command that coordinates with k8s-deployment agent. Should accept environment (dev/staging/prod) and version parameters. Tools needed: Read, Write, Edit.")
```

**Expected Input Context**:
- Command name and purpose
- Tool permissions
- Workflow integration

---

## Maintain Registry

```
Task(workflow, "Update workflow registry to reflect new agent maturity levels. plan-enhancer moved from MVP to Alpha, architecture-enhancer from Alpha to Beta. Validate all registry entries for accuracy.")
```

**Expected Input Context**:
- Registry scope
- Update type
- Maturity changes

---

## Analyze Bottlenecks

```
Task(workflow, "Analyze bottlenecks in the agent creation workflow. Users report friction at the 'definition validation' step - taking 5+ minutes. Identify root causes and recommend improvements.")
```

**Expected Input Context**:
- Workflow scope
- Bottleneck indicators
- User feedback context

---

## Update Documentation

```
Task(workflow, "Update workflow documentation for all slash commands in .claude/commands/. Ensure each command has: purpose, usage examples, tool requirements, and integration notes.")
```

**Expected Input Context**:
- Documentation scope
- Update type
- Integration context

---

## Create Automation

```
Task(workflow, "Create a pre-commit hook that validates agent definitions before commit. Should check: frontmatter format, required sections present, schema compliance. Trigger: file changes in .claude/agents/**.")
```

**Expected Input Context**:
- Automation purpose
- Hook trigger
- Validation requirements

---

## Pre-Mortem

```
Task(workflow, "Run pre-mortem on the new /deploy slash command before we ship it. Identify what could go wrong with k8s-deployment integration, parameter validation, and environment switching. Risk tolerance: medium.")
```

**Expected Input Context**:
- Target artifact (workflow/command/hook)
- Scope of analysis
- Risk tolerance level

---

## Analyze Failures

```
Task(workflow, "The /code-review workflow failed mid-execution yesterday. Symptoms: timeout after 45 seconds, partial output. Context: ran on large PR with 50+ files. Investigate root cause and recommend fixes.")
```

**Expected Input Context**:
- Failed artifact name
- Failure symptoms
- Execution context and logs

---

## Multi-Operation Example

```
Task(workflow, "After agent-architect updates: (1) sync ecosystem to update CLAUDE.md references, (2) maintain registry with new agent capabilities, (3) update documentation with usage examples. Execute in sequence, validate each step.")
```

**Orchestrator Pattern**: Chain operations with validation gates between each step.

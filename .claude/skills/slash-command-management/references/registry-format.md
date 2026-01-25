# Command Registry Format

*Structure and maintenance of the slash command registry*

## Registry Location

**Primary Registry**: `.claude/docs/03-workflows/workflow-registry.md`

The registry tracks:
- All available slash commands
- Command capabilities and maturity
- Integration points between commands
- Deprecation schedules

---

## Registry Structure

### Top-Level Organization

```markdown
# Claude Code Workflow Capabilities Registry

**Last Updated**: YYYY-MM-DD
**Registry Version**: X.Y.Z
**Total Workflows Tracked**: N

## Overview
[Purpose and usage guidance]

## Workflow Capabilities Matrix
[Commands organized by maturity level]

## Workflow Integration Map
[Dependency and integration documentation]

## Workflow Selection Guide
[Decision support for command selection]

## Missing Workflows & Development Priorities
[Gap analysis and roadmap]

## Deprecation Schedule
[Planned deprecations with migration paths]

## Quality Metrics
[Reliability and documentation metrics]
```

---

## Command Entry Format

### Maturity Levels

| Level | Emoji | Meaning |
|-------|-------|---------|
| Production Ready (GA) | Green | Stable, fully documented |
| Testing Ready (Beta) | Yellow | Functional, improving |
| Development Ready (Alpha) | Blue/Cycle | Core patterns established |
| Concept Phase (MVP) | Orange | Concept validation |

### Entry Structure

```markdown
#### **[Command Name]** (vX.Y)

- **Commands**: `/command1` -> `/command2` -> `/command3`
- **Strong At**: [Primary capabilities]
- **Capabilities**: [Detailed capability list]
- **Integration Points**: [Related agents and workflows]
- **Documentation**: `[path/to/docs]`
- **Maturity**: [Description of maturity status]
```

### Example Entry

```markdown
#### **Feature Development Workflow** (v3.1)

- **Commands**: `/spec` -> `/plan` -> `/tasks` -> `/implement`
- **Strong At**: Strategic feature delivery, Context7 integration, sub-agent coordination
- **Capabilities**: Complete SDLC support, deterministic outcomes, roadmap integration
- **Integration Points**: planner-agent, development, test-runner-agent
- **Documentation**: `.claude/commands/spec.md`, `.claude/commands/plan.md`
- **Maturity**: Full SDLC support with proven reliability in production use
```



---

## Integration Map Format

### Cluster Structure

```markdown
#### **[Cluster Name] Cluster**

\`\`\`
/command1 <- -> agent-1
    |
/command2 <- -> agent-2 + research
    |
/command3 <- -> agent-3
    |
Output <- -> downstream-workflow
\`\`\`
```

### Dependencies Section

```markdown
#### **High-Level Dependencies**

- **[Workflow Name]** depends on: [dependency1], [dependency2], [dependency3]
- **[Workflow Name]** depends on: [dependency1], [dependency2]

#### **Shared Components**

- **[Component Name]**: Used by [workflow1], [workflow2], [workflow3]
- **[Component Name]**: Used by [workflow1], [workflow2]
```

---

## Registry Update Protocol

### When to Update

1. **New Command Created**: Add entry to appropriate maturity section
2. **Command Enhanced**: Update version, capabilities, documentation links
3. **Command Deprecated**: Move to deprecation schedule, add migration path
4. **Maturity Change**: Move to new section, update maturity description

### Update Process

```
1. DISCOVER: Glob .claude/commands/*.md
2. PARSE: Extract frontmatter from each command
3. COMPARE: Check against current registry entries
4. UPDATE:
   - New commands -> Add to appropriate section
   - Changed commands -> Update entry
   - Removed commands -> Add to deprecation schedule
5. VALIDATE: Verify all links and references
6. TIMESTAMP: Update "Last Updated" and version
```

### Version Increment Rules

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| New command added | MINOR | 1.0.0 -> 1.1.0 |
| Command capability updated | PATCH | 1.1.0 -> 1.1.1 |
| Command deprecated | MINOR | 1.1.1 -> 1.2.0 |
| Breaking change | MAJOR | 1.2.0 -> 2.0.0 |

---

## Deprecation Entry Format

```markdown
### Planned Deprecations

#### **[Feature/Command Name]** (Deprecate: QN YYYY)

- **Replacement**: [New workflow/command]
- **Migration Path**: [How to transition]
- **Reason**: [Why deprecated]
```

### Example

```markdown
#### **Manual Progress Tracking** (Deprecate: Q1 2026)

- **Replacement**: Automated progress tracking workflow
- **Migration Path**: Gradual automation rollout with manual fallback
- **Reason**: Reduces manual overhead and improves consistency
```

---

## Quality Metrics Format

```markdown
## Quality Metrics

### Workflow Reliability Metrics

- **[Workflow Name]**: XX% successful completion rate
- **[Workflow Name]**: XX% compliance rate

### Documentation Quality Metrics

- **Coverage**: XX% of GA workflows fully documented
- **Accuracy**: [Validation frequency]
- **Usability**: [Feedback integration process]
- **Discoverability**: [Guidance quality]

### Integration Health Metrics

- **Dependency Tracking**: [Status]
- **Cross-Document Consistency**: [Validation method]
- **Version Compatibility**: [Compatibility policy]
```

---

## Selection Guide Format

```markdown
## Workflow Selection Guide

### By Use Case

#### **[Use Case Category]**

1. **[Scenario A]**: Use [workflow] -> [steps]
2. **[Scenario B]**: Use [workflow] -> [steps]
3. **[Scenario C]**: Use [workflow] -> [steps]

### By Maturity Requirements

#### **Production Use (GA Required)**
- [Workflow 1]
- [Workflow 2]

#### **Development Use (Beta Acceptable)**
- [Workflow 1]
- [Workflow 2]

#### **Experimental Use (Alpha/MVP)**
- [Workflow 1]
- [Workflow 2]
```

---

## Validation Checklist

When updating the registry, verify:

- [ ] All command paths are valid (`.claude/commands/*.md` exists)
- [ ] Version numbers follow semantic versioning
- [ ] Maturity levels match actual command state
- [ ] Integration points reference valid agents/workflows
- [ ] Deprecation entries have migration paths
- [ ] Quality metrics are current (within 30 days)
- [ ] "Last Updated" timestamp is accurate
- [ ] Registry version is incremented appropriately

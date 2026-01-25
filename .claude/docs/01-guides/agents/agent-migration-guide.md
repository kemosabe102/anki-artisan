# Agent Migration Guide: Flat Files to Directory Structure

**Purpose**: Step-by-step guide for converting existing flat agent files to self-contained directory structure

**Reference Implementation**: `.claude/agents/ttrpg-campaign-architect/`

**Scaffold Template**: `.claude/templates/agent-scaffold/`

---

## Overview

### Why We're Migrating

The directory-based agent structure provides significant advantages over flat files:

| Aspect | Flat File | Directory Structure |
|--------|-----------|---------------------|
| **Self-contained** | Dependencies scattered across `.claude/docs/` | All related files in one place |
| **Portability** | Must track multiple file locations | Copy entire directory to move agent |
| **Token efficiency** | Large single file loaded entirely | Load only needed docs/examples |
| **Maintainability** | Hard to find related documentation | Clear organization with README files |
| **Testability** | Schema location varies | Consistent `schemas/` subdirectory |

### Directory Structure Target

```
.claude/agents/{domain}/{agent-name}/
├── {agent-name}.md           # Core agent definition (<200 lines ideal)
├── docs/                     # Domain-specific knowledge
│   ├── README.md            # Index of documentation files
│   └── *.md                 # Methodologies, frameworks, expertise
├── examples/                 # Usage patterns
│   ├── README.md            # Index of examples
│   ├── delegation-examples.md  # How orchestrator calls this agent
│   └── output-template.md   # Expected output formats
└── schemas/
    ├── README.md            # Schema documentation
    └── {agent-name}.schema.json  # Input/output validation
```


### Coexistence Model

**Both structures are supported simultaneously.** Flat agents continue to work. Migrate opportunistically.

---

## Before You Start

### Pre-Migration Checklist

Complete this checklist before beginning migration:

- [ ] **Identify current location**: `.claude/agents/{domain}/{agent-name}.md`
- [ ] **Check for external docs**: Search `.claude/docs/guides/` for agent-specific files
- [ ] **Check for schema**: Look in `.claude/agents/dev-tools/schemas/` or `.claude/docs/shared/schemas/`
- [ ] **Verify agent not in active use**: Check if orchestrator is currently using this agent
- [ ] **Review agent line count**: Agents >300 lines benefit most from migration

### Find Related Files

```bash
# Find agent-specific documentation
AGENT_NAME=documentation find .claude/docs -name "*{agent-name}*" -type f

# Find agent schema
AGENT_NAME=documentation find .claude -name "*{agent-name}*.schema.json" -type f

# Count agent file lines (migration benefit assessment)
AGENT_NAME=documentation wc -l .claude/agents/{domain}/{agent-name}.md
```

### Migration Benefit Assessment

| Agent Size | Migration Benefit | Recommendation |
|------------|-------------------|----------------|
| <150 lines | Low | Optional - migrate during updates |
| 150-300 lines | Medium | Migrate when convenient |
| >300 lines | High | Prioritize migration |

---

## Step-by-Step Migration

### Step 1: Create Directory Structure

```bash
# Create all required directories
mkdir -p .claude/agents/{domain}/{agent-name}/docs
mkdir -p .claude/agents/{domain}/{agent-name}/examples
mkdir -p .claude/agents/{domain}/{agent-name}/schemas
```

**Example for debugger:**
```bash
mkdir -p .claude/agents/dev-tools/debugger/docs
mkdir -p .claude/agents/dev-tools/debugger/examples
mkdir -p .claude/agents/dev-tools/debugger/schemas
```


### Step 2: Move Main Agent File

```bash
# Move (not copy) the main agent definition
mv .claude/agents/{domain}/{agent-name}.md .claude/agents/{domain}/{agent-name}/{agent-name}.md
```

**Example:**
```bash
mv .claude/agents/dev-tools/debugger.md .claude/agents/dev-tools/debugger/debugger.md
```

**Important**: Use `mv` (move), not `cp` (copy), to avoid duplicate agent definitions.

### Step 3: Move Schema (If Exists)

Schemas may be in one of two locations:

```bash
# Option A: From dev-tools/schemas/ (most common)
mv .claude/agents/dev-tools/schemas/{agent-name}.schema.json \
   .claude/agents/{domain}/{agent-name}/schemas/

# Option B: From shared schemas (less common)
mv .claude/docs/shared/schemas/{agent-name}.schema.json \
   .claude/agents/{domain}/{agent-name}/schemas/
```

**Note**: Base schemas (`base-agent.schema.json`) stay in `.claude/docs/shared/schemas/` - only move agent-specific schemas.

### Step 4: Move or Create Documentation

**If agent-specific docs exist:**
```bash
# Move existing documentation
mv .claude/docs/guides/{agent-name}/*.md .claude/agents/{domain}/{agent-name}/docs/
```

**If no docs exist, create minimal README:**
```markdown
# docs/ Directory

**Agent**: {agent-name}

## Contents

This directory contains domain knowledge for the {agent-name} agent.

## Files

| File | Purpose |
|------|---------|
| README.md | This index file |

## See Also

- Main agent definition: `../{agent-name}.md`
- Schema: `../schemas/{agent-name}.schema.json`
```


### Step 5: Create Examples

Create at least one example file showing realistic orchestrator delegation:

**File**: `examples/delegation-examples.md`

```markdown
# Delegation Examples for {agent-name}

## Basic Delegation

**Orchestrator call:**
```
Task({agent-name},
  "Brief description of what the orchestrator asks for.
   Include any required context or constraints.")
```

**Expected response structure:**
```json
{
  "status": "SUCCESS",
  "agent": "{agent-name}",
  "confidence": 0.85,
  "agent_specific_output": {
    // Agent-specific fields here
  }
}
```

## Common Scenarios

### Scenario 1: {Common Use Case}

**Context**: {When this scenario occurs}

**Delegation**:
```
Task({agent-name}, "...")
```

**Output**: {What to expect}
```

### Step 6: Update Schema Reference in Agent Definition

Open the main agent file and update any schema references:

**Before (pointing to old location):**
```markdown
## Schema Reference

**Input/Output Contract**: `.claude/agents/dev-tools/schemas/{agent-name}.schema.json`
```

**After (pointing to local schemas/):**
```markdown
## Schema Reference

**Input/Output Contract**: `./schemas/{agent-name}.schema.json`
```

### Step 7: Create README Files

Each subdirectory should have a README. Copy from scaffold template:

```bash
# Copy README templates from scaffold
cp .claude/templates/agent-scaffold/docs/README.md \
   .claude/agents/{domain}/{agent-name}/docs/

cp .claude/templates/agent-scaffold/examples/README.md \
   .claude/agents/{domain}/{agent-name}/examples/

cp .claude/templates/agent-scaffold/schemas/README.md \
   .claude/agents/{domain}/{agent-name}/schemas/
```


---

## Validation Checklist

After migration, verify all requirements are met:

### Structure Validation

- [ ] Directory structure matches scaffold:
  ```
  .claude/agents/{domain}/{agent-name}/
  ├── {agent-name}.md
  ├── docs/
  │   └── README.md
  ├── examples/
  │   └── README.md (or delegation-examples.md)
  └── schemas/
      └── {agent-name}.schema.json
  ```

### File Validation

- [ ] Main agent file moved (not copied) - no duplicate at old location
- [ ] Schema moved and references updated to `./schemas/`
- [ ] At least one example exists in `examples/`
- [ ] README.md files present in each subdirectory

### Functional Validation

- [ ] Agent can be invoked successfully by orchestrator
- [ ] Schema validation passes:
  ```bash
  uv run python scripts/validate_agent_file.py \
    .claude/agents/{domain}/{agent-name}/{agent-name}.md
  ```
- [ ] No broken internal links in agent definition

### Git Validation

- [ ] Old file location shows as deleted in `git status`
- [ ] New directory structure shows as added
- [ ] Commit message follows pattern: `refactor(agents): migrate {agent-name} to directory structure`

---

## Rollback Procedure

If migration fails validation:

### Option 1: Git Restore (Recommended)

```bash
# Discard all migration changes
git checkout -- .claude/agents/{domain}/{agent-name}.md
git clean -fd .claude/agents/{domain}/{agent-name}/
```

### Option 2: Manual Restore

```bash
# Move main file back
mv .claude/agents/{domain}/{agent-name}/{agent-name}.md \
   .claude/agents/{domain}/{agent-name}.md

# Move schema back
mv .claude/agents/{domain}/{agent-name}/schemas/{agent-name}.schema.json \
   .claude/agents/dev-tools/schemas/

# Remove empty directory
rm -rf .claude/agents/{domain}/{agent-name}/
```

**Safety Note**: Keep original files until migration is verified and committed.


---

## Migration Priority

### Recommended Migration Order

**Tier 1 - High Priority** (migrate first):
- Agents with >300 lines
- Frequently updated agents
- Agents with existing external documentation

**Tier 2 - Medium Priority**:
- Agents with 150-300 lines
- Agents with schemas in `dev-tools/schemas/`

**Tier 3 - Low Priority** (migrate opportunistically):
- Agents <150 lines
- Simple, stable agents rarely modified

### Current Flat Agents by Domain

**dev-tools/** (high-use, prioritize):
- `development.md` - High priority
- `debugger.md` - High priority
- `code-quality.md` - High priority
- `code-quality.md` - High priority
- `claude-code-ecosystem.md` - Medium priority

**research/**:
- `researcher-lead.md` - Medium priority
- `researcher-codebase.md` - Medium priority
- `researcher-external.md` - Low priority [consolidated from researcher-web + researcher-library]

**investing/**:
- All agents - Low priority (stable, specialized)

### Migration Strategy

1. **New agents**: Always use directory structure from creation
2. **High-use agents**: Prioritize migration during next update
3. **Stable agents**: Migrate opportunistically when making changes
4. **Batch migration**: Avoid migrating multiple agents simultaneously

---

## FAQ

### General Questions

**Q: Do I need to migrate all agents at once?**

A: No. Both flat files and directory structures work simultaneously. Migrate opportunistically when updating agents or when benefits justify the effort.

**Q: Will flat agents stop working?**

A: No. The orchestrator handles both structures. Flat agents continue to function indefinitely.

**Q: What about shared schemas like `base-agent.schema.json`?**

A: Shared schemas stay in `.claude/docs/shared/schemas/`. Only agent-specific schemas move to the agent's `schemas/` directory. Agent schemas reference the shared base via `$ref`.


### Technical Questions

**Q: How do I update schema references in the agent file?**

A: Change absolute paths to relative paths:
- Before: `.claude/agents/dev-tools/schemas/debugger.schema.json`
- After: `./schemas/debugger.schema.json`

**Q: What if my agent has no schema?**

A: Create one. Use the scaffold template at `.claude/templates/agent-scaffold/schemas/{{agent-name}}.schema.template.json` as a starting point. All agents should have schemas for validation.

**Q: Can I have multiple schema files?**

A: Yes. Place all agent-specific schemas in the `schemas/` directory. Common pattern:
- `{agent-name}.schema.json` - Main input/output schema
- `{agent-name}-config.schema.json` - Configuration schema (if needed)

**Q: What goes in docs/ vs examples/?**

A: 
- **docs/**: Domain knowledge, methodologies, frameworks (reference material)
- **examples/**: Usage patterns, delegation examples, output templates (how-to material)

### Process Questions

**Q: Should I update CLAUDE.md after migration?**

A: No. Agent paths in CLAUDE.md use domain-level references (e.g., "dev-tools agents") not specific file paths. The orchestrator discovers agents by scanning directories.

**Q: Do I need to restart Claude Code after migration?**

A: Yes, if you're creating NEW files. Moving existing files doesn't require restart, but the safest approach is to restart after any structural changes.

**Q: How do I handle agents that reference each other?**

A: Use relative paths from the agent's location:
- Same domain: `../other-agent/other-agent.md`
- Different domain: `../../other-domain/other-agent/other-agent.md`

---

## Complete Migration Example

### Migrating `debugger` Agent

**Before:**
```
.claude/agents/dev-tools/debugger.md
.claude/agents/dev-tools/schemas/debugger.schema.json
.claude/docs/01-guides/debugger/validate-pre-commit-operation.md
.claude/docs/01-guides/debugger/fix-failing-tests-operation.md
```

**Commands:**
```bash
# 1. Create structure
mkdir -p .claude/agents/dev-tools/debugger/{docs,examples,schemas}

# 2. Move main file
mv .claude/agents/dev-tools/debugger.md \
   .claude/agents/dev-tools/debugger/debugger.md

# 3. Move schema
mv .claude/agents/dev-tools/schemas/debugger.schema.json \
   .claude/agents/dev-tools/debugger/schemas/

# 4. Move documentation
mv .claude/docs/01-guides/debugger/*.md \
   .claude/agents/dev-tools/debugger/docs/

# 5. Create examples
cat > .claude/agents/dev-tools/debugger/examples/delegation-examples.md << 'EOF'
# Delegation Examples for debugger

## Basic Debugging Task

Task(debugger,
  "Investigate failing test test_auth_flow in tests/unit/test_auth.py.
   Error: AssertionError on line 42.")
EOF

# 6. Copy README templates
cp .claude/templates/agent-scaffold/docs/README.md \
   .claude/agents/dev-tools/debugger/docs/
cp .claude/templates/agent-scaffold/examples/README.md \
   .claude/agents/dev-tools/debugger/examples/
cp .claude/templates/agent-scaffold/schemas/README.md \
   .claude/agents/dev-tools/debugger/schemas/
```


**After:**
```
.claude/agents/dev-tools/debugger/
├── debugger.md
├── docs/
│   ├── README.md
│   ├── validate-pre-commit-operation.md
│   └── fix-failing-tests-operation.md
├── examples/
│   ├── README.md
│   └── delegation-examples.md
└── schemas/
    ├── README.md
    └── debugger.schema.json
```

**Validation:**
```bash
# Verify structure
ls -la .claude/agents/dev-tools/debugger/

# Validate agent file
uv run python scripts/validate_agent_file.py \
  .claude/agents/dev-tools/debugger/debugger.md

# Verify no duplicates
ls .claude/agents/dev-tools/debugger.md  # Should fail (file not found)
```

**Commit:**
```bash
git add .claude/agents/dev-tools/debugger/
git add .claude/agents/dev-tools/debugger.md  # Stages deletion
git commit -m "refactor(agents): migrate debugger to directory structure"
```

---

## See Also

- **Scaffold Template**: `.claude/templates/agent-scaffold/`
- **Reference Implementation**: `.claude/agents/ttrpg-campaign-architect/`
- **Agent Creation Guide**: `docs/04-guides/agent-creation-guide.md`
- **Agent Standards**: `.claude/docs/01-guides/agents/agent-standards-runtime.md`
- **Base Schema**: `.claude/docs/shared/schemas/base-agent.schema.json`

---

**Document Version**: 1.0
**Last Updated**: 2025-01-28
**Author**: documentation agent

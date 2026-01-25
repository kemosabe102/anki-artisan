# Anti-Pattern Catalog

**Purpose**: Comprehensive catalog of agent prompt anti-patterns with detection methods and severity

**Version**: 1.0

---

## Severity Classification

| Level | Impact | Action Required |
|-------|--------|-----------------|
| **CRITICAL** | Breaks functionality or security | Immediate fix required |
| **MAJOR** | Significant quality/performance impact | Fix before deployment |
| **MINOR** | Suboptimal but functional | Fix when convenient |

---

## Performance Anti-Patterns

### AP-1: Tool Initialization Bloat
**Severity**: MAJOR

**Description**: Agent declares multiple heavy tools (Bash + WebSearch + Context7 + Write) without justification.

**Impact**: Increases initialization time ~5-10s, wastes context window.

**Detection**:
```
Grep("^tools:", agent_path)
# Count heavy tools: Write, Bash, WebSearch, Context7, WebFetch
# >3 heavy tools = bloat
```

**Indicators**:
- Agent declares 4+ heavy tools
- No justification for tool combination
- Tools not used in workflows
- Read-only agent with Write tool

**Fix**: Remove unused tools, use lighter alternatives, justify heavy combinations.

---

### AP-2: Scope Creep
**Severity**: CRITICAL

**Description**: Agent tries to handle multiple responsibilities instead of single purpose.

**Detection**: Look for "and", "or", multiple verbs in Role & Boundaries section.

**Indicators**:
- Description contains multiple distinct actions
- "and also", "additionally handles"
- No clear boundary statements

**Fix**: Split into multiple single-purpose agents, define clear boundaries.

---

### AP-3: Missing Base Pattern
**Severity**: MAJOR

**Description**: Agent does not extend base-agent-pattern.md, duplicating ~1,150 tokens.

**Detection**:
```
Grep("base.agent.pattern", agent_path, "-i")
# No matches = missing base pattern
```

**Impact**: Wastes tokens, increases maintenance burden.

**Fix**: Add "Base Agent Pattern Extension" section, list inherited sections.

---

## Schema & Compliance Anti-Patterns

### AP-4: Schema Non-Compliance
**Severity**: CRITICAL

**Description**: Agent does not extend base-agent.schema.json or lacks schema reference.

**Detection**: Check for schema reference and SUCCESS/FAILURE structures.

**Impact**: Breaks validation, inconsistent output structure.

**Fix**: Add Schema Reference section, ensure base schema inheritance.

---

### AP-5: Vague Tool Descriptions
**Severity**: MAJOR

**Description**: Tool usage not explained clearly for new team members.

**Detection**: Tool descriptions <1 sentence, no examples.

**Indicators**:
- "Use Read to read files" (tautology)
- No when/why guidance
- Missing error handling for tool

**Fix**: Apply "new team member" standard, add specific usage examples.

---

## Operational Anti-Patterns

### AP-6: No Termination Rules
**Severity**: MAJOR

**Description**: Missing <20s per task completion guidance or explicit termination criteria.

**Detection**:
```
Grep("terminat|<20s|completion|timeout", agent_path, "-i")
```

**Impact**: Leads to long-running operations, context exhaustion.

**Fix**: Add time targets, "good enough" criteria, iteration limits.

---

### AP-7: MultiEdit on Large Files
**Severity**: CRITICAL

**Description**: Using MultiEdit for files >22.5K tokens (breaks Claude's editing capability).

**Detection**: Check for MultiEdit usage guidance and size warnings.

**Impact**: Operation will fail silently or corrupt file.

**Fix**: Document MultiEdit size limit, add decision tree for Edit vs MultiEdit vs Write.

---

### AP-8: Parallel Write Operations
**Severity**: CRITICAL

**Description**: Concurrent edits on same file or directory without coordination.

**Detection**: Check Write/Edit tools + parallel execution awareness.

**Indicators**:
- Multiple agents can write to same path
- No serialization requirements documented
- Missing coordination protocol

**Impact**: Race conditions, data loss.

**Fix**: Document serialization requirements, add coordination protocol.

---

## Security & Error Handling Anti-Patterns

### AP-9: Missing Error Recovery
**Severity**: CRITICAL

**Description**: No FAILURE mode documentation or recovery guidance.

**Detection**:
```
Grep("failure|error.recovery", agent_path, "-i")
```

**Indicators**:
- No FAILURE response structure
- No error handling section
- Missing recovery strategies

**Impact**: Integration failures, poor error messages.

**Fix**: Document FAILURE response structure, add recovery strategies.

---

### AP-10: No Security Validation
**Severity**: CRITICAL

**Description**: Security-critical operations without validation or safety checks.

**Detection**: Check for Bash without command whitelisting, URLs without domain whitelist.

**Indicators**:
- Bash tool with no command restrictions
- External API calls without validation
- No input sanitization

**Impact**: Security vulnerabilities, data exposure.

**Fix**: Add input validation, document security boundaries, include validation checkpoints.

---

## Prompt Engineering Anti-Patterns

### AP-11: Kitchen-Sink Prompts
**Severity**: MAJOR

**Description**: Including guidance for failures that haven't occurred (hypothetical scenarios).

**Detection**:
```
Grep("if.*fails|in case|might.*happen", agent_path, "-i")
```

**Impact**: Wastes 200-500+ tokens on unlikely edge cases.

**Pruning Decision Tree**:
1. Has this failure occurred? NO -> Remove section
2. Is failure documented? NO -> Remove or add evidence
3. Is guidance actionable? NO -> Remove or clarify
4. Is section >50 tokens? YES -> Externalize to guide

**Fix**: Apply MVP methodology, remove guidance for undocumented failures.

---

### AP-12: Full Path Doc References
**Severity**: MAJOR

**Description**: Using full directory paths instead of filename-only references.

**Detection**:
```
Grep("\\.claude/docs/|docs/[0-9]+-", agent_path)
# Any matches = FAIL
```

**Examples**:
```markdown
# WRONG
**Extends**: `.claude/docs/01-guides/agents/base-agent-pattern.md`
See `docs/04-guides/documentation/creating-ai-readable-documentation-framework.md`

# CORRECT
**Extends**: `base-agent-pattern.md`
See `creating-ai-readable-documentation-framework.md`
```

**Why This Matters**:
- Files move during documentation reorganization
- AI can search for filename, cannot predict new paths
- Maintenance burden: every reorg requires updating all paths

**Fix**: Replace full paths with filename only. Agent should use `Glob("**/{filename}")` to locate file.

**Exception**: Glob patterns for directory scanning are acceptable.

---

## Detection Workflow

1. **Read agent definition** (full file)
2. **Scan for anti-patterns** (Grep patterns for each)
3. **Classify severity** (Critical/Major/Minor)
4. **Collect evidence** (file:line citations)
5. **Generate fix guidance** (specific, actionable steps)
6. **Priority score**: `(Impact * 0.4) + (Effort^-1 * 0.3) + (Risk * 0.3)`

---

## Anti-Pattern Summary Table

| ID | Name | Severity | Category |
|----|------|----------|----------|
| AP-1 | Tool Initialization Bloat | MAJOR | Performance |
| AP-2 | Scope Creep | CRITICAL | Performance |
| AP-3 | Missing Base Pattern | MAJOR | Performance |
| AP-4 | Schema Non-Compliance | CRITICAL | Schema |
| AP-5 | Vague Tool Descriptions | MAJOR | Schema |
| AP-6 | No Termination Rules | MAJOR | Operational |
| AP-7 | MultiEdit on Large Files | CRITICAL | Operational |
| AP-8 | Parallel Write Operations | CRITICAL | Operational |
| AP-9 | Missing Error Recovery | CRITICAL | Security |
| AP-10 | No Security Validation | CRITICAL | Security |
| AP-11 | Kitchen-Sink Prompts | MAJOR | Prompt Engineering |
| AP-12 | Full Path Doc References | MAJOR | Prompt Engineering |

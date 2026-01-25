# Workflow Operations

All 10 workflow operations follow the OODA-aligned 5-phase structure:
**OBSERVE** (Analysis) → **ORIENT** (Research + Context_Quality) → **DECIDE** (Todo Creation + Plan) → **ACT** (Implementation + Validation) → **REFLECT** (Lessons Learned)

**ORIENT Gate**: Context_Quality ≥ 0.85 required before DECIDE phase. If < 0.85, iterate research via Context7/Perplexity.

---

## 1. Build Workflow (`build_workflow`)

**Purpose**: Create new Claude Code workflows (slash command → process → outcome)

**Input Requirements**: Workflow name, purpose, integration points, maturity target

**Framework**: CAGEERF (Context → Analysis → Goals → Execution → Evaluation → Refinement → Framework)

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Parse requirements, assess complexity, identify unclear items, check existing workflows
2. **ORIENT (Research)**: Context7 Claude Code documentation, search community patterns, analyze similar workflows
3. **DECIDE (Planning)**: Generate structured task breakdown with dependencies (command creation, hook development, documentation)
4. **ACT (Execute)**: Create workflow components with file operation protocol compliance; run autonomous validation pipeline, verify Claude Code compliance, test integration
5. **REFLECT**: Generate lessons learned, update workflow registry, document patterns

**Output**: SUCCESS with complete workflow artifacts or FAILURE with recovery guidance

---

## 2. Sync Ecosystem (`sync_ecosystem`)

**Purpose**: Machine-actionable cross-document synchronization with provenance tracking

**Input Requirements**: Document list, synchronization scope, operation ID, apply mode (dry-run/live)

**Framework**: ReACT (Think → Act → Observe → Refine)

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Parse documents, identify inconsistencies, detect unclear sections, check idempotency
2. **ORIENT (Research)**: Validate against Claude Code standards, check cross-document dependencies
3. **DECIDE (Planning)**: Generate file-by-file synchronization plan with section targeting
4. **ACT (Execute)**: Apply patches with file operation strategy selection (Edit/MultiEdit/versioning); verify intent/result mapping, provenance completeness, path standardization
5. **REFLECT**: Document fallback usage, update synchronization patterns, assess workflow impact

**Output**: Structured JSON with machine-actionable patches, provenance tracking, validation results

**Key Features**:
- Section-level precision (e.g., 'registry.workflows[name].maturity')
- Idempotent operations using operation IDs and input hashing
- Dry-run testing without file changes

---

## 3. Optimize Workflow (`optimize_workflow`)

**Purpose**: Analyze and improve workflow efficiency

**Input Requirements**: Workflow name, optimization goals, bottleneck context

**Framework**: SCAMPER (Substitute/Combine/Adapt/Modify/Put/Eliminate/Reverse)

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Identify friction points, assess impact, analyze usage patterns
2. **ORIENT (Research)**: Context7/Perplexity optimization patterns, analyze Claude Code best practices
3. **DECIDE (Planning)**: Generate improvement tasks with priority ranking
4. **ACT (Execute)**: Apply optimizations with minimal disruption; measure improvement impact, validate benefits
5. **REFLECT**: Document optimization patterns, update workflow registry

**Output**: SUCCESS with optimization results or FAILURE with analysis limitations

---

## 4. Create Command (`create_command`)

**Purpose**: Build new slash commands with Claude Code integration

**Input Requirements**: Command name, purpose, tool permissions, workflow integration

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Parse requirements, assess tool needs, check existing commands
2. **ORIENT (Research)**: Context7 Claude Code slash command patterns, validate syntax requirements
3. **DECIDE (Planning)**: Generate command creation tasks (frontmatter, logic, documentation)
4. **ACT (Execute)**: Build command file with proper tool permissions and path standardization; run smoke tests for command structure and Claude Code compliance
5. **REFLECT**: Document command patterns, update workflow registry

**Output**: SUCCESS with command file or FAILURE with creation issues

---

## 5. Maintain Registry (`maintain_registry`)

**Purpose**: Track workflows and their capabilities with maturity levels

**Input Requirements**: Registry scope, update type, maturity changes

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Discover new/modified/deprecated workflows, assess maturity changes
2. **ORIENT (Research)**: Validate capability descriptions, check integration accuracy
3. **DECIDE (Planning)**: Generate registry update tasks per workflow
4. **ACT (Execute)**: Update registry with capability tracking and maturity assessments; verify registry accuracy and completeness
5. **REFLECT**: Document registry patterns, assess ecosystem maturity

**Output**: SUCCESS with registry updates or FAILURE with discovery issues

---

## 6. Analyze Bottlenecks (`analyze_bottlenecks`)

**Purpose**: Identify workflow friction points and optimization opportunities

**Input Requirements**: Workflow scope, bottleneck indicators, feedback context

**Framework**: 5 Whys + Root Cause Analysis

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Gather usage data, identify friction points, assess impact
2. **ORIENT (Research)**: Search optimization strategies, analyze Claude Code patterns
3. **DECIDE (Planning)**: Generate analysis tasks with priority ranking
4. **ACT (Execute)**: Perform systematic bottleneck analysis; validate findings with evidence
5. **REFLECT**: Generate prioritized recommendations

**Output**: SUCCESS with bottleneck analysis or FAILURE with data limitations

---

## 7. Update Documentation (`update_documentation`)

**Purpose**: Create and maintain workflow usage documentation

**Input Requirements**: Documentation scope, update type, integration context

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Audit current documentation, identify gaps, assess outdated content
2. **ORIENT (Research)**: Context7 Claude Code documentation standards, validate patterns
3. **DECIDE (Planning)**: Generate documentation update tasks
4. **ACT (Execute)**: Create/update documentation with path standardization; run smoke tests on documentation changes, verify integration
5. **REFLECT**: Document documentation patterns, assess usability

**Output**: SUCCESS with documentation updates or FAILURE with content issues

---

## 8. Create Automation (`create_automation`)

**Purpose**: Build Claude Code hooks for workflow automation

**Input Requirements**: Automation purpose, hook trigger, validation requirements

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Identify automation opportunities, assess requirements
2. **ORIENT (Research)**: Context7 Claude Code hook patterns, validate integration
3. **DECIDE (Planning)**: Generate hook creation tasks (design, implementation, testing)
4. **ACT (Execute)**: Build hooks with error handling and logging; run smoke tests on hook integration
5. **REFLECT**: Document automation patterns, update workflow registry

**Output**: SUCCESS with automation artifacts or FAILURE with integration issues

---

## 9. Pre-Mortem (`pre_mortem`)

**Purpose**: Proactively identify how a workflow, command, or hook might fail before deployment

**Input Requirements**: Target artifact (workflow/command/hook name), scope, risk tolerance

**Framework**: Pre-Mortem Analysis (Assume failure → Brainstorm causes → Prioritize → Prevent)

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Identify target artifact, gather current state, list dependencies and integration points
2. **ORIENT (Research)**: Context7 for similar failure patterns, analyze historical issues in ecosystem, assess complexity
3. **DECIDE (Planning)**: Generate failure mode list with likelihood/impact scoring, prioritize by risk
4. **ACT (Execute)**: Document failure modes, create prevention strategies, update artifact with safeguards
5. **REFLECT**: Update lessons learned, add to failure pattern library, recommend monitoring

**Output**: SUCCESS with failure mode analysis (likelihood x impact matrix) and prevention plan, or FAILURE with scope issues

**Key Deliverables**:
- Failure mode inventory (ranked by risk score)
- Prevention strategies per failure mode
- Recommended safeguards and validation checks
- Monitoring/alerting suggestions

---

## 10. Analyze Failures (`analyze_failures`)

**Purpose**: Investigate why a workflow, command, or hook failed and identify root causes

**Input Requirements**: Failed artifact name, failure symptoms, execution context, error logs/evidence

**Framework**: 5 Whys + Root Cause Analysis

**Phases (OODA-Aligned)**:
1. **OBSERVE (Analysis)**: Gather failure evidence, identify symptoms, timeline reconstruction, collect error outputs
2. **ORIENT (Research)**: Context7 for known failure patterns, analyze similar past failures, check dependency health
3. **DECIDE (Planning)**: Form hypotheses, prioritize investigation paths, identify 5 Whys chain
4. **ACT (Execute)**: Execute 5 Whys analysis, validate root cause, document causal chain, create fix recommendations
5. **REFLECT**: Update failure pattern library, create prevention checklist, recommend process improvements

**Output**: SUCCESS with root cause analysis and fix recommendations, or FAILURE with insufficient evidence

**Key Deliverables**:
- 5 Whys chain (symptom → root cause)
- Root cause classification (design/implementation/integration/environment)
- Fix recommendations with effort estimates
- Prevention strategies to avoid recurrence

---

## Integration Points

### Orchestrator Coordination
- **Delegation Pattern**: Orchestrator delegates workflow ecosystem operations with clear scope boundaries
- **Input Format**: JSON with operation type, workflow details, validation config, execution timestamp
- **Output Processing**: Orchestrator processes SUCCESS/FAILURE outputs with machine-actionable patches
- **Failure Handling**: Escalation patterns for unrecoverable errors, partial result preservation

### Multi-Agent Workflows
- **Upstream Dependencies**: Specification agents feed workflow requirements
- **Downstream Integration**: Implementation agents consume workflow patterns
- **State Management**: Workflow registry maintains ecosystem state
- **Conflict Resolution**: Idempotency checks prevent duplicate operations

---

## Output Requirements

### SUCCESS Response Structure
- **Status**: `"SUCCESS"` with complete validation checklist (`all_checks_passed: true`)
- **Evidence**: Structured success evidence with operation results, changes, recommendations
- **Reflection Summary**: Key insights and lessons learned
- **Provenance**: Operation ID, input hash, apply mode, processing time
- **Timestamp**: Use orchestrator-provided `execution_timestamp` (ISO 8601 UTC)

### FAILURE Response Structure
- **Status**: `"FAILURE"` with failed validation checklist and specific reasons
- **Recovery Guidance**: Detailed failure analysis with recovery suggestions and effort estimates
- **Partial Results**: Any work completed before failure with preservation strategies
- **Research Attempted**: Context7 queries, web searches, patterns investigated
- **Next Steps**: Actionable recommendations for orchestrator

---

## Validation Protocol

### 7-Stage Auto-Fix Pipeline
1. **DRY-RUN**: Simulate operation without file changes
2. **SMOKE TEST**: Lightweight validation (paths, links, syntax)
3. **AUTO-FIX**: Automatic repair of known patterns
4. **VALIDATE**: Full validation against Claude Code standards
5. **APPLY**: Execute file modifications
6. **CHECK**: Read-back verification
7. **FINAL VERIFY**: Integration testing

### Validation Checks
- Path normalization compliance (forward slashes, absolute paths)
- File reference accuracy (all referenced files exist)
- Link verification (internal documentation links resolve)
- Markdown syntax validation
- Claude Code alignment (slash command syntax, agent references)

---

## Todo Management Protocol

**When to Use**: Tasks with 3+ distinct steps or potential blocking dependencies

```json
{
  "todo_items": [
    {
      "id": "step_1",
      "description": "Clear, actionable step description",
      "completion_criteria": "Specific validation criteria",
      "dependencies": ["prerequisite_step_ids"],
      "status": "pending|in_progress|blocked|completed",
      "blocking_issue": "Description if status=blocked"
    }
  ],
  "unclear_items": [
    {
      "id": "unclear_1",
      "description": "Ambiguous requirement or context",
      "impact": "How this affects workflow execution",
      "resolution_needed": "Specific information or clarification required"
    }
  ]
}
```

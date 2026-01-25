# Phase 3: DECIDE - Operation Selection & Risk Assessment

**OODA Stage**: DECIDE | **Time Allocation**: 10-15%

**Purpose**: Select operation approach, assess risks, establish approval gates before execution

**Deliverable**: Approved execution plan with risk mitigations

---

## Workflow Steps

### Step 3.1: Operation Category Confirmation

**Input**: Category from Phase 1, analysis from Phase 2

**Process**:
1. Confirm detected category matches analysis findings
2. Select specific operation within category:

| Category | Possible Operations |
|----------|---------------------|
| CREATE | `analyze_agent_idea`, `generate_agent_definition`, `create_agent`, `populate_subdirectories` |
| ANALYZE | `evaluate_agent` (quality matrix evaluation) |
| UPDATE | `update_agent`, `implement_feedback`, `update_maturity` |
| VALIDATE | `validate_workflow`, frontmatter validation |
| DESIGN | `create_design_guide` |

3. Document operation selection rationale

**Output**: Confirmed operation with justification


### Step 3.2: Agent Selection Criteria (for CREATE)

**Input**: Agent requirements from simulation

**Process**:
1. Verify domain assignment:
   - `claude-code/` - Development tools, code operations
   - `investing/` - Financial analysis, research
   - `research/` - General research, exploration
2. Verify color assignment via `agent-color-taxonomy.md`
3. Confirm tool selection matches capabilities
4. Validate description format (<200 chars, trigger keywords, NOT-for)

**Output**: Domain, color, tools, description validated

### Step 3.3: Risk Assessment

**Input**: Selected operation, agent design

**Process**:
1. Identify failure modes:
   | Risk | Likelihood | Impact | Mitigation |
   |------|------------|--------|------------|
   | Invalid frontmatter | Medium | High | Validate against spec before write |
   | Agent too large | Low | Medium | Check line count, externalize to docs/ |
   | Template non-compliance | Medium | High | Validate against agent.template.md |
   | CLAUDE.md update failure | Low | Medium | Prepare manual fallback |

2. For new agents, assess:
   - Overlap with existing agents (check COMPONENT_ALMANAC.md)
   - Scope clarity (boundaries well-defined?)
   - Integration points (workflows, orchestrator)

**Output**: Risk register with mitigations


### Step 3.4: Approval Gates

**Input**: Operation plan, risk assessment

**Process**:
1. **CREATE operations**:
   - Directory structure confirmed
   - Template compliance verified
   - No duplicate agent exists
   - Proceed when all gates pass

2. **UPDATE operations**:
   - Current agent state loaded
   - Changes scoped and reversible
   - Backup strategy defined (git)

3. **ANALYZE operations**:
   - Target agent exists and readable
   - Quality matrix criteria loaded
   - Output format confirmed

**Output**: Approval status (APPROVED/BLOCKED with reason)

---

## Exit Criteria

**Approval required to proceed to ACT**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Operation confirmed | 0.30 | Single operation selected with rationale |
| Risks assessed | 0.25 | >=3 risks identified with mitigations |
| Gates passed | 0.25 | All approval gates green |
| Plan complete | 0.20 | Execution steps defined |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping risk assessment | ALWAYS identify >=3 failure modes |
| Proceeding without approval | Gates MUST pass before ACT |
| Creating duplicate agents | Check COMPONENT_ALMANAC.md first |
| Wrong domain assignment | Verify against domain definitions |

---

**Previous Phase**: [Phase 2: ORIENT](phase-2-orient.md)
**Next Phase**: [Phase 4: ACT](phase-4-act.md)

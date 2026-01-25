# Report Format

Full report template for `/analyze-agent` output.

---

## Report Structure

```markdown
# Agent Analysis Report: {agent-name}

**Analysis Date**: {ISO 8601 timestamp}
**Analysts**: claude-code-ecosystem, claude-code-ecosystem, documentation, tech-debt-investigator
**Overall Confidence**: {0.0-1.0}

---

## Executive Summary

{2-3 sentence summary of overall quality, key strengths, top priority improvements}

---

## Overall Quality Score: {0-100}

**Grade**: {A (90-100) | B (80-89) | C (70-79) | D (60-69) | F (<60)}

**Dimension Breakdown**:

| **Dimension** | **Score** | **Grade** | **Status** |
|---------------|-----------|-----------|------------|
| Prompt Quality | {0-100} | {A-F} | {PASS/NEEDS IMPROVEMENT/FAIL} |
| Schema Design | {0-100} | {A-F} | {PASS/NEEDS IMPROVEMENT/FAIL} |

| Documentation | {0-100} | {A-F} | {PASS/NEEDS IMPROVEMENT/FAIL} |
| Integration | {0-100} | {A-F} | {PASS/NEEDS IMPROVEMENT/FAIL} |
| Methodology | {PASS/PARTIAL/FAIL} | - | {PASS/NEEDS IMPROVEMENT/FAIL} |

**Overall Assessment**: {Excellent | Good | Acceptable | Needs Improvement | Poor}

---

## Top 3 Findings (P1 Priority)

### 1. {Finding Title}
**Source**: {claude-code-ecosystem | claude-code-ecosystem | documentation | tech-debt-investigator}
**Impact**: {High | Medium | Low}
**Effort**: {Low | Medium | High}
**Priority Score**: {0.0-1.0}

**Description**: {What was found}

**Evidence**: {File:line citations}

**Recommendation**: {Specific actionable fix}

**Token Impact**: {Quantified savings if applicable}

---

### 2. {Finding Title}
{... same structure ...}

---

### 3. {Finding Title}
{... same structure ...}


---

## Detailed Findings by Dimension

### Prompt Quality (Score: {0-100}, Grade: {A-F})

**Anthropic Standards Compliance**:
- Clarity & Directness: {PASS/PARTIAL/FAIL} {notes}
- XML Structure: {PASS/PARTIAL/FAIL} {notes}
- Chain-of-Thought: {PASS/PARTIAL/FAIL} {notes}
- Prefill Guidance: {PASS/PARTIAL/FAIL} {notes}
- Uncertainty Handling: {PASS/PARTIAL/FAIL} {notes}
- Context Management: {PASS/PARTIAL/FAIL} {notes}

**Framework Scores**:
- Structural Quality: {Pass/Fail count} / 16 criteria
- Prompt Engineering: {A-F grade}
- Token Optimization: {A-F grade}
- Testing Strategy: {A-F grade}
- Progressive Disclosure: {A-F grade}
- Token Density: {A-F grade}

**Key Findings**:
- {Finding 1}
- {Finding 2}
- {Finding 3}

---

### Schema Design (Score: {0-100}, Grade: {A-F})


**14-Criterion Evaluation**:
1. Documentation Completeness: {0-100}
2. Type Specificity: {0-100}
3. Constraint Coverage: {0-100}
4. Composition Clarity: {0-100}
5. Validation Accuracy: {0-100}
6. Error Reporting Quality: {0-100}
7. Security Compliance: {0-100}
8. Reusability Factor: {0-100}
9. Format Validation: {0-100}
10. Evolution Support: {0-100}
11. Cross-Field Validation: {0-100}
12. Serialization Consistency: {0-100}
13. Performance: {0-100}
14. Interoperability: {0-100}

**Overall Schema Score**: {weighted average}

**Key Findings**:
- {Finding 1}
- {Finding 2}
- {Finding 3}

---

### Documentation (Score: {0-100}, Grade: {A-F})

**Token Efficiency**:
- Current tokens: {count}
- Optimized potential: {count}
- Compression ratio: {X:1}
- Savings opportunity: {tokens} ({percentage}%)


**Anti-Patterns Detected**:
- Buried Essentials: {count, examples}
- Vague Labels: {count, examples}
- Excessive Depth: {count, examples}
- Content Duplication: {count, ~tokens wasted}
- Inline Verbose Examples: {count, ~tokens wasted}
- Missing Quick Reference: {Yes/No}

**Progressive Disclosure Compliance**:
- Layering: {A-F grade} (depth <=2 levels?)
- Essential Visibility: {percentage}% (target: 80%+)
- Information Scent: {percentage}% first-click accuracy (target: 80%+)

**Key Findings**:
- {Finding 1}
- {Finding 2}
- {Finding 3}

---

### Integration (Score: {0-100}, Grade: {A-F})

**7-Point Checklist**:
- [PASS/FAIL] Frontmatter compliance (7/7 valid fields)
- [PASS/FAIL] Base-pattern extension
- [PASS/FAIL] orchestrator-workflow.md entry
- [PASS/FAIL] CLAUDE.md entry
- [PASS/FAIL] Schema reference
- [PASS/FAIL] Pre-flight assessment
- [PASS/FAIL] Two-attempt rule

**Score**: {PASS (7/7) | PARTIAL (5-6/7) | FAIL (<5/7)}


**Missing**: {list if any}

**Key Findings**:
- {Finding 1}
- {Finding 2}
- {Finding 3}

---

### Methodology Appropriateness

**Domain**: {detected}
**Complexity**: {Simple | Medium | High}
**Primary OODA Phase**: {OBSERVE | ORIENT | DECIDE | ACT} ({percentage}% of workflow)

**Recommended Methodology**: {CAGEERF | ReACT | 5W1H | SCAMPER}
**Current Usage**: {detected or "None"}
**Assessment**: {PASS | PARTIAL | FAIL}

**Rationale**: {why this methodology fits this agent}

**Recommendation**: {specific guidance if not PASS}

---

## Documentation Debt Analysis

**Debt Score**: {0-100} (0 = no debt, 100 = severe debt)
**TDR**: {ratio} (Technical Debt Ratio)
**SQALE Grade**: {A-E}
**SIG Star Rating**: {1-5 stars}

**6-Category Breakdown**:
1. Code Quality: {score}
2. Testing: {score}
3. Architecture: {score}

4. Documentation: {score}
5. Infrastructure: {score}
6. Historical: {score}

**Impact/Effort Matrix**:
- **P1 Quick Wins** (high impact, low effort): {count findings}
- **P2 Strategic** (high impact, high effort): {count findings}
- **P3 Defer** (low impact, low effort): {count findings}
- **P4 Opportunistic** (low impact, high effort): {count findings}

---

## Token Savings Opportunities

**Total Potential Savings**: {tokens} ({percentage}% reduction)

**Top Opportunities** (ranked by value score):

1. {Opportunity title}: {tokens saved}
   - **Strategy**: {reference_existing | extend_base | externalize | compress}
   - **Confidence**: {0.0-1.0}
   - **Effort**: {Low | Medium | High}
   - **Value Score**: {tokens_saved x confidence / effort}

2. {Opportunity title}: {tokens saved}
   {... same structure ...}

3. {Opportunity title}: {tokens saved}
   {... same structure ...}

---

## Consolidated Recommendations


### P1 Priorities (High Impact, Quick Wins)

{Sequenced list of P1 recommendations with dependencies noted}

1. **{Recommendation title}**
   - **Impact**: {specific benefit}
   - **Effort**: {time estimate}
   - **Implementation**: {step-by-step}
   - **Token Savings**: {if applicable}
   - **Dependencies**: {none | depends on #X}

### P2 Strategic Improvements

{List of P2 recommendations}

### P3 Opportunistic Enhancements

{List of P3 recommendations if any}

---

## Implementation Roadmap

**Sprint 1** (Immediate - P1):
- [ ] {Task 1}
- [ ] {Task 2}
- [ ] {Task 3}

**Sprint 2** (Short-term - P2):
- [ ] {Task 1}
- [ ] {Task 2}

**Sprint 3** (Long-term - P3):
- [ ] {Task 1}


**Estimated Total Effort**: {hours/days}
**Expected Quality Improvement**: {current score} -> {projected score} ({+X points})
**Expected Token Savings**: {tokens} ({percentage}% reduction)

---

## Maturity Assessment

**Current Maturity**: {v0.x MVP | v1.x Alpha | v2.x Beta | v3.x+ GA}
**Target Maturity**: {recommended level}

**Progression Criteria** (for next level):
- {Criterion 1}: {Met / Partial / Not Met}
- {Criterion 2}: {Met / Partial / Not Met}
- {Criterion 3}: {Met / Partial / Not Met}

**Path to Next Level**: {specific requirements}

---

## Confidence & Iteration Support

**Overall Confidence**: {0.0-1.0}

**Confidence Breakdown**:
- Analysis Coverage: {0.0-1.0} (all dimensions assessed?)
- Evidence Quality: {0.0-1.0} (file:line citations?)
- Recommendation Clarity: {0.0-1.0} (actionable specifics?)

**Open Questions**: {list if any, or "None"}

**Iteration Support**:
- {Follow-up research needed?}
- {Additional validation required?}
- {Alternative approaches to consider?}


---

## Multi-Agent Synthesis Summary

**Agents Consulted**: 4 (claude-code-ecosystem, claude-code-ecosystem, documentation, tech-debt-investigator)
**Findings Overlap**: {percentage}% similarity across agents
**Synthesis Applied**: {Yes (>0.7 overlap) | No (<0.7 overlap)}
**Conflicts Detected**: {count, or "None"}
**Conflict Resolution**: {approach used if any}

**Consensus Findings** (all 4 agents agree):
- {Finding 1}
- {Finding 2}
- {Finding 3}

**Divergent Findings** (agent-specific insights):
- {Finding 1 from specific agent}
- {Finding 2 from specific agent}

---

**End of Report**
```

---

## Post-Analysis Actions

After report generation, offer:

1. "Apply recommendations automatically?" (delegate fixes)
2. "Generate implementation tasks?" (TODO list from P1)
3. "Analyze another agent?"
4. "Run ecosystem-wide audit?" (if --all not used)

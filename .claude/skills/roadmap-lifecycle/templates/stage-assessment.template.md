# Stage Assessment Report

**Project**: {{project_name}}
**Assessment Date**: {{date}}
**Assessed By**: roadmap-lifecycle skill

---

## Current Stage: {{detected_stage}}

**Confidence**: {{confidence}}% (based on {{evidence_count}} artifacts analyzed)

**Stage Definition**: [{{detected_stage}}-stage.md](../stages/{{detected_stage}}-stage.md)

---

## Maturity Dimension Scores

| Dimension | Current | {{detected_stage}} Min | {{next_stage}} Target | Gap |
|-----------|---------|------------------------|----------------------|-----|
| Architecture | {{arch_score}} | {{arch_min}} | {{arch_target}} | {{arch_gap}} |
| Data & Migrations | {{data_score}} | {{data_min}} | {{data_target}} | {{data_gap}} |
| Observability | {{obs_score}} | {{obs_min}} | {{obs_target}} | {{obs_gap}} |
| Testing | {{test_score}} | {{test_min}} | {{test_target}} | {{test_gap}} |
| Release & Deployment | {{rel_score}} | {{rel_min}} | {{rel_target}} | {{rel_gap}} |
| Security | {{sec_score}} | {{sec_min}} | {{sec_target}} | {{sec_gap}} |
| Capacity & Cost | {{cap_score}} | {{cap_min}} | {{cap_target}} | {{cap_gap}} |
| Documentation | {{doc_score}} | {{doc_min}} | {{doc_target}} | {{doc_gap}} |
| LLM Integration | {{llm_score}} | {{llm_min}} | {{llm_target}} | {{llm_gap}} |

**Overall Score**: {{overall_score}}/10
**Stage Range**: {{stage_min}} - {{stage_max}}

---

## Stage Gate Validation

### Quality Thresholds

| Metric | Required | Actual | Status |
|--------|----------|--------|--------|
| Overall Score | ≥{{quality_min}} | {{overall_score}} | {{quality_status}} |
| Architecture | ≥{{arch_required}} | {{arch_score}} | {{arch_status}} |
| Implementation | ≥{{impl_required}} | {{impl_score}} | {{impl_status}} |
| Production | ≥{{prod_required}} | {{prod_score}} | {{prod_status}} |

### Risk Assessment

| Risk Level | Allowed | Actual | Status |
|------------|---------|--------|--------|
| Critical | {{critical_allowed}} | {{critical_count}} | {{critical_status}} |
| High | {{high_allowed}} | {{high_count}} | {{high_status}} |
| Medium | Unlimited | {{medium_count}} | ✅ |

---

## Artifacts Analyzed

### Found ✅
{{#each artifacts_found}}
- [{{category}}] `{{path}}`
{{/each}}

### Missing ⚠️
{{#each artifacts_missing}}
- [{{category}}] {{expected_path}} - {{recommendation}}
{{/each}}

---

## Gaps to {{next_stage}}

### Critical Gaps (Must Address)

{{#each critical_gaps}}
#### {{number}}. {{dimension}}: {{gap_title}}

**Current**: {{current_state}}
**Required for {{next_stage}}**: {{required_state}}
**Remediation**: {{remediation_suggestion}}
**Effort**: {{effort_estimate}}

{{/each}}

### Recommended Improvements

{{#each recommended_improvements}}
- **{{dimension}}**: {{improvement}}
{{/each}}

---

## Exit Criteria Status ({{detected_stage}} → {{next_stage}})

{{#each exit_criteria}}
- [{{status}}] {{criterion}}
{{/each}}

**Completion**: {{exit_completion_percent}}%

---

## Next Steps

1. {{#if ready_to_advance}}
   ✅ Ready to advance to {{next_stage}}. Run `/roadmap advance` to generate transition plan.
   {{else}}
   ⚠️ Address {{critical_gap_count}} critical gaps before advancing.
   {{/if}}

2. Review this assessment with stakeholders

3. {{#if has_gaps}}
   Run `/roadmap advance` to generate remediation tasks for identified gaps.
   {{/if}}


---

## Assessment Metadata

- **Skill Version**: roadmap-lifecycle v1.0
- **Assessment Method**: 9-dimension maturity scoring
- **Source Documents**:
  - MATURITY-MATRIX.md
  - architecture-stage-policies.md
  - Project artifacts ({{artifact_count}} files)

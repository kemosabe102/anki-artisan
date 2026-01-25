# Plan Enhancer Validation Checklist

Complete validation checklist for plan enhancement quality assurance.

**Extends**: `base-agent-pattern.md` (Validation Checklist)

---

## Pre-Enhancement Checklist

**Purpose**: Verify all prerequisites before starting enhancement work

- [ ] Plan file exists at specified path (`Read(plan_path)` succeeds)
- [ ] Plan file is not empty (content length > 0)
- [ ] SPEC.md accessible at `docs/00-project/SPEC.md`
- [ ] SPEC.md contains business goals section
- [ ] SPEC.md contains success criteria or metrics
- [ ] COMPONENT_ALMANAC.md accessible for reuse opportunities
- [ ] Plan file contains business placeholders to enhance (Grep finds matches)
- [ ] Plan file is not a template file (no `.template.md` extension)

### Pre-Enhancement Failure Recovery

| Check Failed | Recovery Action |
|--------------|-----------------|
| Plan file missing | FAILURE: Return path error, suggest correct location |
| SPEC.md missing | FAILURE: Recommend /spec command first |
| SPEC.md lacks business goals | FAILURE: Identify specific gap, request user input |
| COMPONENT_ALMANAC.md missing | WARNING: Proceed without reuse analysis |
| No placeholders found | SUCCESS: Plan already enhanced, return no-op result |

---

## During-Enhancement Checklist

**Purpose**: Ensure quality during placeholder replacement process

### Placeholder Tracking

- [ ] Initial placeholder count captured (before enhancement)
- [ ] All placeholder patterns scanned: `\[.*\]` regex applied
- [ ] Business placeholders categorized by type:
  - [ ] Goals/Objectives: `[Business Goal]`, `[Primary Objective]`, `[Strategic Alignment]`
  - [ ] Metrics: `[Success Metric]`, `[KPI]`, `[Measurable Outcome]`
  - [ ] Value Props: `[Value Proposition]`, `[User Benefit]`, `[ROI Statement]`
  - [ ] Components: `[Component1]`, `[Feature Name]`, `[Module Name]`
  - [ ] Requirements: `[FR-XXX]`, `[Requirement]`, `[NFR-XXX]`
- [ ] Technical placeholders identified and PRESERVED (not modified)
- [ ] Running count maintained during replacement

### Evidence Citation

- [ ] Every business claim traces to SPEC.md section
- [ ] Citation format used: `(Source: SPEC.md, Section X)` or `(SPEC.md:line)`
- [ ] COMPONENT_ALMANAC.md citations for reuse opportunities
- [ ] No content fabricated without source document backing

### Confidence Scoring (Per Replacement)

- [ ] Confidence score (0.0-1.0) assigned to each replacement
- [ ] High confidence (>=0.8): Direct SPEC.md quote or metric available
- [ ] Medium confidence (0.7-0.79): Derived from SPEC.md context
- [ ] Low confidence (<0.7): Marked with `[UNVERIFIED]` tag
- [ ] Average confidence tracked across all replacements

### Content Quality

- [ ] Replacements are specific (not generic paraphrases)
- [ ] Metrics are measurable (numbers, percentages, timeframes)
- [ ] Goals are actionable (verb + outcome + measure)
- [ ] FR-IDs mapped to business value (not just technical description)
- [ ] Progressive disclosure applied (essential visible, details externalized)

---

## Post-Enhancement Checklist (BLOCKING)

**Purpose**: Final validation before reporting success

### Zero Placeholder Validation (CRITICAL)

- [ ] Final Grep scan executed: `Grep('\[Business|\[Component|\[TODO|\[TBD|\[Placeholder', plan_path)`
- [ ] Zero business placeholders remaining (count == 0)
- [ ] Zero generic markers: `[TBD]`, `[TODO]`, `[Placeholder]`
- [ ] Zero unnamed components: `[Component1]`, `[Component2]`
- [ ] Zero unresolved references: `[See SPEC]`, `[See X]`

### Technical Section Preservation

- [ ] Technical placeholders untouched (architecture-enhancer responsibility)
- [ ] Preserved patterns verified: `[Architecture Decision]`, `[Technical Implementation]`, `[API Specification]`, `[System Integration]`, `[Performance Strategy]`, `[Database Schema]`
- [ ] No accidental modification to technical sections

### Output Schema Compliance

- [ ] JSON completion evidence generated
- [ ] Required fields present:
  - [ ] `status`: "success" | "partial" | "failure"
  - [ ] `placeholders_found`: integer (initial count)
  - [ ] `placeholders_replaced`: integer (final count)
  - [ ] `placeholders_remaining`: integer (should be 0)
  - [ ] `confidence`: float (0.0-1.0)
  - [ ] `evidence`: array of citation objects
- [ ] Output validates against `plan-enhancer.schema.json`

### Confidence Score Calculation

Formula: `confidence = (spec_coverage x 0.4) + (replacement_rate x 0.3) + (citation_quality x 0.2) + (specificity x 0.1)`

- [ ] SPEC coverage assessed (40% weight): % of replacements with direct SPEC source
- [ ] Replacement rate calculated (30% weight): replaced / found
- [ ] Citation quality evaluated (20% weight): % with file:line references
- [ ] Specificity score (10% weight): measurable metrics vs vague statements
- [ ] Overall confidence >= 0.7 for success status
- [ ] Overall confidence < 0.7 triggers partial status with gaps documented


---

## Quality Gates (Minimum Thresholds)

| Gate | Threshold | Severity | Action if Failed |
|------|-----------|----------|------------------|
| Business placeholders remaining | 0 | BLOCKING | Re-scan and retry replacement |
| Overall confidence score | >= 0.7 | BLOCKING | Document gaps, return partial status |
| SPEC.md citation rate | >= 80% | WARNING | Flag uncited content as [UNVERIFIED] |
| Technical section preservation | 100% | BLOCKING | Revert changes, re-process |
| Schema validation | PASS | BLOCKING | Fix output format before returning |

### Gate Evaluation Order

1. **Pre-Enhancement Gates** (stop if fail)
2. **Schema Compliance** (validate output structure)
3. **Zero Placeholder** (core success metric)
4. **Technical Preservation** (scope discipline)
5. **Confidence Threshold** (quality assurance)
6. **Citation Rate** (evidence quality)

---

## Common Validation Failures & Remediation

### Failure: Placeholders Remain After Processing

**Symptoms**: Final Grep returns matches > 0

**Root Causes**:
- Regex pattern missed variant (e.g., `[Business goal]` vs `[Business Goal]`)
- Desktop Commander edit_block failed silently
- Placeholder nested in code block or table

**Remediation**:
1. Re-run case-insensitive Grep: `Grep('\[business|\[component|\[todo', plan_path, -i=true)`
2. Verify edit_block success (check return status)
3. Retry with exact match string from Grep output
4. If stuck after 3 retries, report partial with remaining list

---

### Failure: SPEC.md Lacks Required Business Content

**Symptoms**: Cannot find business goals, metrics, or requirements in SPEC.md

**Root Causes**:
- SPEC.md is incomplete or draft state
- Business content in different section than expected
- SPEC.md uses different terminology

**Remediation**:
1. Search alternative patterns: `Grep('goal|objective|metric|success|criteria', spec_path)`
2. Check for Business Case, Value Proposition, or ROI sections
3. If truly missing, return FAILURE with specific gap: "SPEC.md missing business goals section"
4. Recommend: "Run /spec command to populate SPEC.md business sections first"


---

### Failure: Low Confidence Score (<0.7)

**Symptoms**: Enhancement completed but confidence below threshold

**Root Causes**:
- Many replacements derived/inferred rather than directly quoted
- SPEC.md content vague or high-level
- Missing citations for substantial content

**Remediation**:
1. Review replacements with confidence < 0.7
2. Add `[UNVERIFIED]` tags to uncertain content
3. Document specific gaps in output evidence
4. Return partial status with improvement recommendations
5. Suggest: "User review needed for [UNVERIFIED] sections"

---

### Failure: Accidental Technical Section Modification

**Symptoms**: Technical placeholders replaced or modified

**Root Causes**:
- Pattern matching too broad (caught technical patterns)
- Misidentified section boundaries
- Copy-paste error during edit_block

**Remediation**:
1. Identify affected technical sections
2. Restore from original (re-read plan, find diff)
3. Tighten placeholder patterns to exclude technical markers
4. Re-run enhancement with business-only scope


---

### Failure: Desktop Commander Edit Block Errors

**Symptoms**: `mcp__desktop-commander__edit_block` returns error or no change

**Root Causes**:
- old_string not found (whitespace/encoding mismatch)
- File path incorrect or inaccessible
- Concurrent modification conflict

**Remediation**:
1. Verify exact string match (Read file, copy exact content)
2. Check path is absolute and exists
3. Retry with smaller chunk if content is long
4. Use `mcp__desktop-commander__write_file` with mode="rewrite" as fallback (full file replacement)

---

## Validation Algorithm Summary

```
PRE-ENHANCEMENT:
  IF NOT file_exists(plan_path): RETURN FAILURE("Plan file not found")
  IF NOT file_exists(spec_path): RETURN FAILURE("SPEC.md required")
  placeholders_found = count(Grep('[Business|Component|TODO]', plan_path))
  IF placeholders_found == 0: RETURN SUCCESS("Already enhanced")

DURING-ENHANCEMENT:
  FOR each placeholder P in plan:
    source = find_source(P, spec_md, component_almanac)
    IF source.confidence >= 0.7:
      replace(P, source.content)
      citations.append(source.reference)
    ELSE:
      replace(P, source.content + " [UNVERIFIED]")
    track(replaced_count, confidence_scores)

POST-ENHANCEMENT:
  remaining = count(Grep('[Business|Component|TODO]', plan_path))
  IF remaining > 0: retry_replacement(remaining) OR RETURN PARTIAL
  
  confidence = calculate_confidence(spec_coverage, replacement_rate, citation_quality, specificity)
  IF confidence < 0.7: RETURN PARTIAL(gaps)
  
  validate_schema(output)
  RETURN SUCCESS(evidence)
```

---

## Quick Self-Validation Checklist

Use this abbreviated checklist for rapid validation:

```markdown
## Quick Validation (Copy-Paste)
- [ ] Plan file exists and readable
- [ ] SPEC.md accessible with business content
- [ ] All business placeholders identified
- [ ] Every replacement cites SPEC.md source
- [ ] Zero business placeholders remaining
- [ ] Technical sections untouched
- [ ] Confidence >= 0.7
- [ ] Output schema valid
```

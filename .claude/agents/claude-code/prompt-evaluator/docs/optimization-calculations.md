# Optimization Calculations & Priority Scoring

**Purpose**: Mathematical formulas and algorithms for priority scoring and optimization quantification

**Single source of truth** - do not duplicate formulas elsewhere; reference this file.

---

## Priority Scoring Algorithm

### Core Formula

```
Priority = (Impact × 0.4) + (Effort⁻¹ × 0.3) + (Risk × 0.3)
```

**Weights Rationale**:
- **Impact (40%)**: Primary driver - what matters most is fixing high-impact issues
- **Effort Inverse (30%)**: Favor low-effort fixes for quick wins
- **Risk (30%)**: Prioritize high-risk agents (security, data loss potential)

---

### Impact Scoring (0.0-1.0)

| Level | Score | Examples |
|-------|-------|----------|
| Critical | 1.0 | Schema non-compliance, security gaps, missing testing for high-risk |
| Major | 0.6 | Tool ambiguity, token bloat >500, missing error recovery |
| Minor | 0.3 | Inconsistent XML, missing examples, suboptimal compression |

---

### Effort Inverse Scoring (0.0-1.0)

| Effort | Score | Time | Examples |
|--------|-------|------|----------|
| Low | 1.0 | <30 min | Reference docs, add schema section, remove filler words |
| Medium | 0.5 | 1-3 hrs | Restructure workflow, add examples, externalize framework |
| High | 0.2 | >3 hrs | Full redesign, new testing framework, multi-file refactor |

---

### Risk Scoring (0.0-1.0)

| Level | Score | Tools | Examples |
|-------|-------|-------|----------|
| High | 1.0 | Write + Bash + External APIs | python-code-implementer, k8s-deployment |
| Medium | 0.5 | Edit OR single heavy tool | agent-architect, debugger |
| Low | 0.2 | Read-only operations | prompt-evaluator, researcher-codebase |

---

### Priority Interpretation

| Score | Action | Timeline |
|-------|--------|----------|
| >0.7 | Immediate | Fix within current sprint |
| 0.4-0.7 | Short-term | Next maintenance cycle |
| <0.4 | Long-term | Backlog for future improvement |

---

## Token Optimization Quantification

### Current State Calculation

```bash
AGENT_NAME=prompt-evaluator uv run python scripts/calculate_tokens.py .claude/agents/agent-name.md --format=json
```

**Output**: `{"summary": {"total_tokens": 8002}}`

### Optimization Potential Formula

```
Optimization_Potential = Σ (Applicable_Technique_Savings)
Optimization_Percentage = (Optimization_Potential / Current_Tokens) × 100
```

### Technique-Specific Savings

| Technique | Savings | Effort |
|-----------|---------|--------|
| Base pattern inheritance | ~1,150 tokens | Low |
| Documentation references | 100-300/section | Low |
| Compression (10:1) | Variable | Medium |
| Tool description optimization | 50-150 tokens | Low |
| Example consolidation | 100-500 tokens | Low |
| Workflow compression | 200-400 tokens | Low |
| Redundant section removal | 100-300/section | Low |

---

## Progressive Disclosure Scoring

### Size Compliance Score

```
Size_Score = max(0.0, 1.0 - ((Line_Count - 500) / 500))
```

| Lines | Score | Status |
|-------|-------|--------|
| ≤500 | 1.0 | PASS |
| 750 | 0.5 | PARTIAL |
| ≥1000 | 0.0 | FAIL |

---

## Confidence Scoring

### Per-Dimension Formula

```
Confidence = Data_Completeness × Evidence_Quality × Methodology_Soundness
```

| Factor | 1.0 | 0.75 | 0.5 | 0.25 |
|--------|-----|------|-----|------|
| Data Completeness | All required | Minor gaps | Significant gaps | Critical gaps |
| Evidence Quality | Direct citations | Strong indicators | Weak indicators | No evidence |
| Methodology | Established | Adapted | Novel | Ad-hoc |

### Overall Confidence

```
Overall = (Σ (Dimension_Confidence × Dimension_Weight)) / (Σ Weights)
```

**Dimension Weights**: Structural (0.25), Prompt Engineering (0.20), Token Optimization (0.20), Testing (0.15), Progressive Disclosure (0.10), Token Density (0.10)

---

## Validation & Accuracy

| Metric | Accuracy |
|--------|----------|
| Token counts | ±10% (tiktoken) |
| Effort estimates | ±50% (inherent uncertainty) |
| Priority scores | ±0.1 (input sensitivity) |
| Confidence scores | ±0.15 (subjective components) |

# Semantic Extraction Guide

**Purpose**: Extract content from project specs using semantic markers, not section numbers.

**Why**: Hard-coded section numbers (e.g., "Section 5: Features") are brittle. If spec structure changes, extraction fails silently. Semantic markers are resilient.

---

## Semantic Markers

Use these patterns to find content regardless of document structure:

| Content Type | Primary Markers | Secondary Markers |
|--------------|-----------------|-------------------|
| **Features** | `FR-XXX` IDs, `P0/P1/P2` tags | MoSCoW keywords (Must/Should/Could/Won't), heading contains "Functional Requirements" |
| **Success Metrics** | `Target:` + `Measurement:` pairs | Tables with columns: Metric, Target, Current |
| **Phases/Timeline** | `## Phase N:` headings, `### Phase N:` | Timeline tables, `**Phase**` labels |
| **Success Criteria** | `- [ ]` checkbox lists with criteria | `**Success Criteria:**` label, `**Exit Criteria:**` |
| **Priorities** | `P0:`, `P1:`, `P2:` prefixes | `**Priority:**` label, MoSCoW tags |

---

## Extraction Patterns

### Features

```python
# Primary: Look for FR-XXX identifiers
pattern_fr_id = r'FR-\d{3,4}'

# Secondary: Look for P0/P1/P2 tags
pattern_priority = r'\b(P0|P1|P2)\b'

# Fallback: Look for heading containing "Features" or "Requirements"
pattern_heading = r'^##\s+.*(?:Features|Requirements)'
```

### Success Metrics

```python
# Primary: Target/Measurement pairs
pattern_target = r'Target:\s*(.+)'
pattern_measurement = r'Measurement:\s*(.+)'

# Secondary: Tables with metric structure
# Look for rows with: | Metric | Target | Current |
```

### Phases

```python
# Primary: Phase headings
pattern_phase = r'^##\s+Phase\s+(\d+)'

# Secondary: Timeline sections
pattern_timeline = r'(?:Timeline|Schedule|Milestones?)'
```

---

## Extraction Workflow

1. **Scan for Primary Markers First**
   - Use Grep with primary patterns
   - High confidence (>0.90) if markers found

2. **Fall Back to Secondary Markers**
   - If primary yields no results, try secondary
   - Medium confidence (0.70-0.89)

3. **Last Resort: Heading Text Match**
   - If no markers, look for section headings
   - Low confidence (0.50-0.69), flag for review

4. **Extraction Failure Protocol**
   - If confidence <0.50, return FAILURE
   - Include `extraction_failure` error type
   - Suggest user add semantic markers to spec

---

## Anti-Patterns

**NEVER**:
- Hard-code section numbers ("Section 5", "Section 10")
- Assume spec structure is stable
- Skip confidence scoring on extractions

**ALWAYS**:
- Use pattern matching on content markers
- Report extraction confidence in output
- Handle missing markers gracefully

---

## Integration with ICE Scoring

When extracting features for ICE scoring:

1. Find features via FR-XXX or P0/P1/P2 markers
2. Extract each feature's description
3. Apply ICE scoring per [orchestrator-thresholds.md](../../../../docs/00-core/orchestrator-thresholds.md#ice-score-thresholds)
4. Report extraction confidence alongside ICE scores

---

## Example

**Spec Content**:
```markdown
## 5. Core Functional Requirements

### FR-001: User Authentication (P0)
Users must be able to log in with email/password.

### FR-002: Data Export (P1)
Users should be able to export their data as CSV.
```

**Extraction Result**:
```json
{
  "features": [
    {
      "id": "FR-001",
      "name": "User Authentication",
      "priority": "P0",
      "extraction_confidence": 0.95,
      "markers_found": ["FR-XXX", "P0"]
    },
    {
      "id": "FR-002",
      "name": "Data Export",
      "priority": "P1",
      "extraction_confidence": 0.95,
      "markers_found": ["FR-XXX", "P1"]
    }
  ],
  "extraction_method": "primary_markers",
  "overall_confidence": 0.95
}
```

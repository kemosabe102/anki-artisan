---
name: plan-context-synthesis
description: >
  Use this skill when extracting functional requirements from SPEC.md 
  and classifying complexity. Detects FR-IDs, MoSCoW priorities, ICE scores,
  non-functional requirements, and acceptance criteria. Trigger keywords: 
  FR extraction, spec analysis, complexity classification, requirement parsing.
---

# Plan Context Synthesis

*Extract functional requirements from SPEC.md and classify complexity for plan generation.*

## Contents

- [Context Building Protocol](#context-building-protocol)
- [SPEC Section Extraction](#spec-section-extraction)
- [FR Detection Algorithm](#fr-detection-algorithm)
- [MoSCoW Priority Extraction](#moscow-priority-extraction)
- [ICE Score Detection](#ice-score-detection)
- [Complexity Classification](#complexity-classification)
- [Dependency Detection](#dependency-detection)
- [Output Contract](#output-contract)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---


## Context Building Protocol

**Framework Alignment**: CAGEERF (Context -> Analysis -> Goals -> Execution -> Evaluation -> Refinement -> Framework)

### Phase 1: Context Gathering (CAGEERF-C)

```
1. LOCATE source artifacts:
   - SPEC.md (primary source - REQUIRED)
   - docs/00-project/COMPONENT_ALMANAC.md (existing components)
   - Related specifications (cross-references)
   
2. VALIDATE artifact presence:
   - SPEC.md MUST exist (FAILURE if missing)
   - Minimum 3 of 5 required sections present
   - COMPONENT_ALMANAC.md RECOMMENDED (warn if missing)

3. EXTRACT metadata:
   - Feature name from SPEC.md title
   - Feature branch from header
   - Status (Draft/In Review/Approved)
   - Roadmap ID reference
   - Creation date
```

### Phase 2: Analysis (CAGEERF-A)

```
1. PARSE SPEC.md sections (see SPEC Section Extraction)
2. DETECT functional requirements (see FR Detection Algorithm)
3. EXTRACT MoSCoW priorities (see MoSCoW Priority Extraction)
4. DETECT ICE scores if present (see ICE Score Detection)
5. CLASSIFY overall complexity (see Complexity Classification)
6. IDENTIFY dependencies (see Dependency Detection)
```

### Phase 3: Goals Definition (CAGEERF-G)

```
1. MAP functional requirements to categories:
   - Core implementation (Must priority)
   - Enhancement features (Should priority)
   - Optional features (Could priority)
   - Excluded scope (Won't priority)
   
2. IDENTIFY requirement dependencies
3. DETERMINE parallel vs sequential execution eligibility
4. CALCULATE total effort estimation baseline
```

---


## SPEC Section Extraction

### Required Sections (>=3 must be present for valid SPEC.md)

| Section | Canonical Header | Fuzzy Matches | Plan Relevance |
|---------|------------------|---------------|----------------|
| Context & Vision | `## Pain Point Alignment` | "Context", "Vision", "Problem", "Background" | HIGH - motivation source |
| Functional Requirements | `## Functional Requirements` | "FR-", "Requirements", "Features" | CRITICAL - primary FR source |
| User Scenarios | `## User Scenarios` | "Scenarios", "Use Cases", "Stories", "Acceptance" | HIGH - acceptance criteria source |
| Non-Functional Requirements | `## Non-Functional Requirements` | "NFR-", "Performance", "Quality", "Constraints" | MEDIUM - quality gates |
| Technical Constraints | `## Technical Constraints` | "TC-", "Platform", "Architecture" | MEDIUM - implementation bounds |

### Section Detection Algorithm

```python
def extract_spec_sections(spec_content: str) -> dict[str, SectionData]:
    """Extract recognized sections from SPEC.md content."""
    sections = {}
    current_section = None
    current_content = []
    line_start = 0
    
    for line_num, line in enumerate(spec_content.split('\n'), 1):
        if line.startswith('## '):
            # Save previous section
            if current_section:
                sections[current_section] = SectionData(
                    header=current_header,
                    content='\n'.join(current_content),
                    line_start=line_start,
                    line_end=line_num - 1
                )
            
            # Detect new section
            header = line.strip('# ').strip()
            current_section = match_section_type(header)
            current_header = header
            current_content = []
            line_start = line_num
        elif current_section:
            current_content.append(line)
    
    # Save final section
    if current_section:
        sections[current_section] = SectionData(
            header=current_header,
            content='\n'.join(current_content),
            line_start=line_start,
            line_end=line_num
        )
    
    return sections
```


### Section Type Matching

```python
def match_section_type(header: str) -> str | None:
    """Match header to canonical section type using fuzzy matching."""
    canonical_map = {
        "Context & Vision": ["pain point", "context", "vision", "problem", "background", "alignment"],
        "Functional Requirements": ["functional requirement", "requirements", "fr-", "features"],
        "User Scenarios": ["scenario", "use case", "story", "stories", "acceptance"],
        "Non-Functional Requirements": ["non-functional", "nfr-", "performance", "quality"],
        "Technical Constraints": ["constraint", "tc-", "platform", "technical", "architecture"]
    }
    
    header_lower = header.lower()
    for canonical, patterns in canonical_map.items():
        if any(p in header_lower for p in patterns):
            return canonical
    return None
```

### Section Validation Rules

| Rule | Threshold | Action if Failed |
|------|-----------|------------------|
| Min sections | >=3 of 5 | FAILURE: `missing_spec_sections` |
| FR section exists | Required | FAILURE: `no_functional_requirements` |
| Section has content | >0 non-empty lines | WARNING: log empty section |
| FR table detected | Required in FR section | WARNING: `no_fr_table_detected` |

---


## FR Detection Algorithm

### FR Sources in SPEC.md

| Source Location | Detection Pattern | Priority |
|-----------------|-------------------|----------|
| `## Functional Requirements` | Tables with FR-XXX | Primary |
| `## Requirements` | Bullet lists with FR-XXX | Secondary |
| Inline references | `FR-\d{3}` pattern anywhere | Cross-reference |

### FR Table Detection

```python
def detect_fr_table(section_content: str) -> list[FREntry]:
    """Detect and parse FR table from section content."""
    fr_entries = []
    in_table = False
    header_row_seen = False
    
    for line in section_content.split('\n'):
        # Detect table start
        if '|' in line and ('FR-' in line.upper() or is_table_header(line)):
            in_table = True
            if is_table_header(line):
                header_row_seen = True
                continue
            if is_separator_row(line):  # |---|---|
                continue
        
        if in_table and '|' in line:
            if 'FR-' in line.upper():
                fr = parse_fr_row(line)
                if fr:
                    fr_entries.append(fr)
        elif in_table and not line.strip().startswith('|'):
            in_table = False
            header_row_seen = False
    
    return fr_entries


def is_table_header(line: str) -> bool:
    """Check if line is a markdown table header."""
    cells = [c.strip().lower() for c in line.split('|') if c.strip()]
    header_keywords = ['id', 'description', 'priority', 'requirement', 'fr']
    return any(kw in cell for cell in cells for kw in header_keywords)


def is_separator_row(line: str) -> bool:
    """Check if line is a table separator (|---|---|)."""
    return bool(re.match(r'^\s*\|[\s\-:]+\|', line))
```


### FR Row Parsing

```python
def parse_fr_row(line: str) -> FREntry | None:
    """Parse a single FR row from markdown table."""
    cells = [c.strip() for c in line.split('|') if c.strip()]
    
    if len(cells) < 2:
        return None
    
    fr_id = extract_fr_id(cells[0])
    if not fr_id:
        # Try to find FR-ID anywhere in the row
        for cell in cells:
            fr_id = extract_fr_id(cell)
            if fr_id:
                break
    
    if not fr_id:
        return None
    
    description = cells[1] if len(cells) > 1 else ""
    priority = detect_moscow_priority(line)
    
    # Extract acceptance criteria if inline
    acceptance_criteria = extract_inline_criteria(description)
    
    return FREntry(
        id=fr_id,
        description=clean_fr_description(description),
        priority=priority,
        acceptance_criteria=acceptance_criteria,
        line_number=None,  # Set by caller
        raw_text=line
    )


def extract_fr_id(text: str) -> str | None:
    """Extract FR-XXX pattern from text."""
    match = re.search(r'FR-(\d{3})', text, re.IGNORECASE)
    if match:
        return f"FR-{match.group(1)}"
    return None


def clean_fr_description(description: str) -> str:
    """Clean FR description by removing embedded IDs and keywords."""
    # Remove FR-ID prefix
    desc = re.sub(r'^FR-\d{3}[:\s]*', '', description)
    # Remove MUST/SHOULD/COULD keywords (preserve meaning elsewhere)
    desc = re.sub(r'\bSystem\s+(MUST|SHOULD|COULD|SHALL|MAY)\s+', '', desc, flags=re.I)
    # Clean whitespace
    return ' '.join(desc.split()).strip()
```

---


## MoSCoW Priority Extraction

### Priority Detection Hierarchy

| Priority | Keywords | Inference Rules | Phase Mapping |
|----------|----------|-----------------|---------------|
| Must | `MUST`, `SHALL`, `REQUIRED` | FR-001 to FR-010 default to Must | Phase 1 (100%) |
| Should | `SHOULD`, `RECOMMENDED` | FR-011 to FR-020 default to Should | Phase 1-2 (40%/60%) |
| Could | `COULD`, `MAY`, `OPTIONAL` | FR-021+ default to Could | Phase 2-3 (30%/70%) |
| Won't | `WON'T`, `WILL NOT`, `OUT OF SCOPE` | Explicit exclusion only | Excluded |

### Priority Detection Algorithm

```python
def detect_moscow_priority(text: str) -> str:
    """Detect MoSCoW priority from text content."""
    text_upper = text.upper()
    
    # Explicit priority keywords (highest precedence)
    if 'MUST' in text_upper and 'SHOULD' not in text_upper:
        return 'Must'
    elif 'SHOULD' in text_upper and 'COULD' not in text_upper:
        return 'Should'
    elif 'COULD' in text_upper or 'MAY' in text_upper:
        return 'Could'
    elif "WON'T" in text_upper or 'WILL NOT' in text_upper or 'OUT OF SCOPE' in text_upper:
        return "Won't"
    
    # Priority column detection (table format)
    priority_match = re.search(r'\|\s*(Must|Should|Could|Won\'t)\s*\|', text, re.I)
    if priority_match:
        return priority_match.group(1).capitalize()
    
    # Infer from FR-ID pattern if no explicit priority
    fr_num = extract_fr_number(text)
    if fr_num:
        if fr_num <= 10:
            return 'Must'
        elif fr_num <= 20:
            return 'Should'
        else:
            return 'Could'
    
    # Default to Should for ambiguous cases
    return 'Should'


def extract_fr_number(text: str) -> int | None:
    """Extract numeric portion of FR-XXX identifier."""
    match = re.search(r'FR-(\d{3})', text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None
```


### Priority Distribution Analysis

```python
def analyze_priority_distribution(fr_entries: list[FREntry]) -> dict:
    """Analyze distribution of priorities across FRs."""
    distribution = {'Must': 0, 'Should': 0, 'Could': 0, "Won't": 0}
    
    for fr in fr_entries:
        priority = fr.priority or 'Should'
        distribution[priority] += 1
    
    total = len(fr_entries)
    ratios = {k: v / total if total > 0 else 0 for k, v in distribution.items()}
    
    # Validate distribution (warn if unbalanced)
    warnings = []
    if ratios['Must'] > 0.7:
        warnings.append("Heavy Must ratio (>70%) - consider reprioritization")
    if ratios['Must'] < 0.2:
        warnings.append("Light Must ratio (<20%) - MVP may lack focus")
    if ratios["Won't"] > 0.3:
        warnings.append("High exclusion ratio (>30%) - scope may be too narrow")
    
    return {
        'counts': distribution,
        'ratios': ratios,
        'total': total,
        'warnings': warnings
    }
```

---


## ICE Score Detection

> **Canonical ICE Thresholds**: `.claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds`

### ICE Score Schema

ICE (Impact, Confidence, Ease) scoring is optional but enhances prioritization when present.

| Dimension | Range | Description |
|-----------|-------|-------------|
| Impact | 1-10 | Business value delivered (10 = highest) |
| Confidence | 1-10 | Certainty of success (10 = most certain) |
| Ease | 1-10 | Implementation simplicity (10 = easiest) |

**ICE Score Formula**: `Impact × Confidence × Ease` = raw score (1-1000)

### ICE Detection Algorithm

```python
def detect_ice_score(fr_entry: FREntry, section_content: str) -> ICEScore | None:
    """Detect ICE score from FR entry or surrounding context."""
    
    # Pattern 1: Inline ICE notation (I:7, C:8, E:6) - scale 1-10
    inline_match = re.search(
        r'I[:\s]*(\d{1,2})[,\s]*C[:\s]*(\d{1,2})[,\s]*E[:\s]*(\d{1,2})',
        fr_entry.raw_text,
        re.IGNORECASE
    )
    if inline_match:
        return ICEScore(
            impact=int(inline_match.group(1)),
            confidence=int(inline_match.group(2)),
            ease=int(inline_match.group(3))
        )
    
    # Pattern 2: Table column detection
    # Look for ICE columns in FR table
    ice_table_match = detect_ice_from_table(fr_entry.id, section_content)
    if ice_table_match:
        return ice_table_match
    
    # Pattern 3: Separate ICE scoring section
    ice_section = extract_ice_section(section_content)
    if ice_section:
        return lookup_ice_for_fr(fr_entry.id, ice_section)
    
    return None


def detect_ice_from_table(fr_id: str, content: str) -> ICEScore | None:
    """Extract ICE score from table columns."""
    # Find row containing this FR-ID
    for line in content.split('\n'):
        if fr_id in line and '|' in line:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            # Look for numeric cells that could be ICE scores (1-10 scale)
            scores = [int(c) for c in cells if c.isdigit() and 1 <= int(c) <= 10]
            if len(scores) >= 3:
                return ICEScore(
                    impact=scores[0],
                    confidence=scores[1],
                    ease=scores[2]
                )
    return None
```


### ICE Score Inference

```python
def infer_ice_score(fr_entry: FREntry) -> ICEScore:
    """Infer ICE score when not explicitly provided (1-10 scale)."""

    # Impact inference from priority (1-10 scale)
    impact_map = {'Must': 10, 'Should': 6, 'Could': 4, "Won't": 1}
    impact = impact_map.get(fr_entry.priority, 5)

    # Confidence inference from description clarity (1-10 scale)
    confidence = 5  # Default
    if len(fr_entry.acceptance_criteria) >= 2:
        confidence = 7
    if len(fr_entry.acceptance_criteria) >= 3:
        confidence = 9
    if 'unclear' in fr_entry.description.lower() or '?' in fr_entry.description:
        confidence = 3

    # Ease inference from complexity indicators (1-10 scale)
    ease = 5  # Default
    complexity_indicators = ['complex', 'integration', 'multi', 'system-wide']
    simplicity_indicators = ['simple', 'add', 'update', 'single', 'config']

    desc_lower = fr_entry.description.lower()
    if any(ind in desc_lower for ind in complexity_indicators):
        ease = 3
    if any(ind in desc_lower for ind in simplicity_indicators):
        ease = 8

    return ICEScore(impact=impact, confidence=confidence, ease=ease)
```

---


## Complexity Classification

**Reference**: Cynefin framework from [generating-plans skill](../generating-plans/SKILL.md)

### Cynefin Domains for SPEC Analysis

| Domain | FR Count | Dependency Density | Characteristics | Plan Strategy |
|--------|----------|-------------------|-----------------|---------------|
| SIMPLE | 1-5 | Low (<20% cross-refs) | Clear cause-effect, patterns exist | 1 phase, linear execution |
| COMPLICATED | 6-15 | Medium (20-50% cross-refs) | Analyzable, expert knowledge needed | 2-3 phases, structured approach |
| COMPLEX | 16-30 | High (>50% cross-refs) | Emergent patterns, probe-sense-respond | 3-4 phases, iterative checkpoints |
| CHAOTIC | >30 or unclear | Very High/Unknown | Novel territory, act-sense-respond | MVP phase + discovery phases |

### Complexity Classification Algorithm

```python
def classify_complexity(spec_analysis: SpecAnalysis) -> ComplexityResult:
    """Classify specification complexity using Cynefin framework."""
    fr_count = len(spec_analysis.functional_requirements)
    dependency_density = calculate_dependency_density(spec_analysis)
    novel_tech_count = count_novel_technologies(spec_analysis)
    nfr_count = len(spec_analysis.non_functional_requirements)
    
    # Score each dimension (0.0 - 1.0)
    fr_score = categorize_fr_count(fr_count)
    dep_score = categorize_dependency_density(dependency_density)
    novel_score = categorize_novelty(novel_tech_count)
    nfr_score = min(nfr_count / 10, 1.0)  # NFRs add complexity
    
    # Weighted complexity score
    complexity_score = (
        fr_score * 0.35 +      # FR count weight
        dep_score * 0.30 +     # Dependency weight
        novel_score * 0.20 +   # Novelty weight
        nfr_score * 0.15       # NFR weight
    )
    
    if complexity_score < 0.25:
        return ComplexityResult(domain='SIMPLE', phases=1, approach='linear')
    elif complexity_score < 0.50:
        return ComplexityResult(domain='COMPLICATED', phases=2, approach='structured')
    elif complexity_score < 0.75:
        return ComplexityResult(domain='COMPLEX', phases=3, approach='iterative')
    else:
        return ComplexityResult(domain='CHAOTIC', phases=4, approach='emergent')
```


### Dependency Density Calculation

```python
def calculate_dependency_density(spec: SpecAnalysis) -> float:
    """Calculate FR cross-reference density."""
    total_frs = len(spec.functional_requirements)
    if total_frs == 0:
        return 0.0
    
    cross_references = 0
    for fr in spec.functional_requirements:
        # Count FR-XXX mentions in description
        refs = len(re.findall(r'FR-\d{3}', fr.description, re.I))
        cross_references += refs
    
    # Also check acceptance criteria
    for fr in spec.functional_requirements:
        for criterion in fr.acceptance_criteria:
            refs = len(re.findall(r'FR-\d{3}', criterion, re.I))
            cross_references += refs
    
    return cross_references / total_frs


def categorize_fr_count(count: int) -> float:
    """Map FR count to complexity score."""
    if count <= 5: return 0.1
    elif count <= 10: return 0.3
    elif count <= 15: return 0.5
    elif count <= 25: return 0.7
    else: return 0.9


def categorize_dependency_density(density: float) -> float:
    """Map dependency density to complexity score."""
    if density < 0.2: return 0.1
    elif density < 0.5: return 0.4
    elif density < 1.0: return 0.7
    else: return 0.9


def categorize_novelty(novel_count: int) -> float:
    """Map novel technology count to complexity score."""
    if novel_count == 0: return 0.1
    elif novel_count <= 2: return 0.4
    elif novel_count <= 4: return 0.7
    else: return 0.9
```


### Novel Technology Detection

```python
def count_novel_technologies(spec: SpecAnalysis) -> int:
    """Count novel/unfamiliar technologies in specification."""
    novel_indicators = [
        'new', 'novel', 'experimental', 'prototype', 'poc',
        'first time', 'unfamiliar', 'emerging', 'cutting-edge'
    ]
    
    novel_count = 0
    
    # Check technical constraints section
    if spec.technical_constraints:
        content_lower = spec.technical_constraints.lower()
        for indicator in novel_indicators:
            if indicator in content_lower:
                novel_count += 1
    
    # Check for specific tech mentions without existing patterns
    tech_patterns = ['api', 'sdk', 'library', 'framework', 'service']
    for fr in spec.functional_requirements:
        desc_lower = fr.description.lower()
        if any(tech in desc_lower for tech in tech_patterns):
            if any(ind in desc_lower for ind in novel_indicators):
                novel_count += 1
    
    return min(novel_count, 5)  # Cap at 5
```

---


## Dependency Detection

### Dependency Types

| Type | Detection Pattern | Impact |
|------|-------------------|--------|
| FR Cross-Reference | `FR-XXX` in description/criteria | Execution order constraint |
| Component Dependency | Shared module/service references | Integration requirement |
| External Dependency | Third-party libraries, APIs | Risk factor |
| Data Dependency | Shared data models/schemas | Schema coordination |

### Dependency Detection Algorithm

```python
def detect_dependencies(spec_analysis: SpecAnalysis) -> DependencyGraph:
    """Build dependency graph from SPEC.md analysis."""
    graph = DependencyGraph()
    
    for fr in spec_analysis.functional_requirements:
        graph.add_node(fr.id)
        
        # Explicit FR references
        explicit_deps = find_fr_references(fr.description)
        for dep in explicit_deps:
            if dep != fr.id:  # Avoid self-reference
                graph.add_edge(dep, fr.id, type='explicit')
        
        # Acceptance criteria references
        for criterion in fr.acceptance_criteria:
            criterion_deps = find_fr_references(criterion)
            for dep in criterion_deps:
                if dep != fr.id:
                    graph.add_edge(dep, fr.id, type='criterion')
        
        # Component-based inference
        component = extract_component(fr.description)
        component_deps = find_component_dependencies(component, spec_analysis)
        for dep in component_deps:
            graph.add_edge(dep, fr.id, type='component')
    
    # Validate graph (detect cycles)
    if graph.has_cycle():
        cycles = graph.find_cycles()
        graph.add_warning(f"Circular dependencies detected: {cycles}")
    
    return graph


def find_fr_references(text: str) -> list[str]:
    """Extract all FR-XXX references from text."""
    matches = re.findall(r'FR-\d{3}', text, re.IGNORECASE)
    return [m.upper() for m in matches]
```


### External Dependency Detection

```python
def detect_external_dependencies(spec: SpecAnalysis) -> list[ExternalDep]:
    """Detect external library/service dependencies."""
    external_deps = []
    
    # Technical constraints often list external dependencies
    if spec.technical_constraints:
        deps = extract_package_references(spec.technical_constraints)
        external_deps.extend(deps)
    
    # NFRs may reference external services
    for nfr in spec.non_functional_requirements:
        if 'api' in nfr.lower() or 'service' in nfr.lower():
            deps = extract_service_references(nfr)
            external_deps.extend(deps)
    
    return deduplicate(external_deps)


def extract_package_references(text: str) -> list[ExternalDep]:
    """Extract Python package or library references."""
    packages = []
    
    # Common patterns: "uses X", "requires Y", "depends on Z"
    patterns = [
        r'uses?\s+([a-z][a-z0-9_-]+)',
        r'requires?\s+([a-z][a-z0-9_-]+)',
        r'depends?\s+on\s+([a-z][a-z0-9_-]+)',
        r'([a-z][a-z0-9_-]+)\s+library',
        r'([a-z][a-z0-9_-]+)\s+package',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            packages.append(ExternalDep(name=match, type='package'))
    
    return packages
```

### Blocker Identification

```python
def identify_blockers(graph: DependencyGraph) -> list[str]:
    """Identify FRs that block multiple other FRs."""
    blockers = []
    
    for node in graph.nodes:
        dependents = graph.get_dependents(node)
        if len(dependents) >= 2:
            blockers.append({
                'fr_id': node,
                'blocks_count': len(dependents),
                'blocks': dependents,
                'priority': 'critical' if len(dependents) >= 3 else 'high'
            })
    
    return sorted(blockers, key=lambda x: -x['blocks_count'])
```

---


## Output Contract

### Success Response

```json
{
  "status": "SUCCESS",
  "feature_name": "executable-task-system",
  "description": "Transform technical implementation plans into structured, parallel-optimized executable task lists",
  "spec_source": "docs/01-planning/specifications/002-executable-task-system/SPEC.md",
  "functional_requirements": [
    {
      "id": "FR-001",
      "description": "Generate complete executable task list from technical implementation plan within 10 minutes",
      "priority": "Must",
      "acceptance_criteria": [
        "All components covered by specific implementation tasks",
        "Task sequencing based on dependencies"
      ],
      "category": "functional",
      "ice_score": {
        "impact": 5,
        "confidence": 4,
        "ease": 3,
        "total": 48
      },
      "line_number": 129
    }
  ],
  "non_functional_requirements": [
    {
      "id": "NFR-001",
      "description": "Performance - Task generation completes within 10 minutes",
      "category": "performance",
      "threshold": "10 minutes",
      "line_number": 219
    }
  ],
  "complexity_classification": "COMPLICATED",
  "complexity_details": {
    "domain": "COMPLICATED",
    "fr_count": 29,
    "dependency_density": 0.34,
    "novel_tech_count": 1,
    "recommended_phases": 2,
    "approach": "structured"
  },
  "dependencies": {
    "internal": ["FR-001 -> FR-003", "FR-006 -> FR-007"],
    "external": ["claude-code-task-tool"],
    "blockers": [
      {
        "fr_id": "FR-001",
        "blocks_count": 4,
        "blocks": ["FR-003", "FR-004", "FR-005", "FR-019"]
      }
    ]
  },
  "priority_distribution": {
    "counts": {"Must": 12, "Should": 10, "Could": 7, "Won't": 0},
    "ratios": {"Must": 0.41, "Should": 0.34, "Could": 0.24, "Won't": 0.0}
  },
  "context_confidence": 0.92,
  "metadata": {
    "sections_found": ["Functional Requirements", "User Scenarios", "Technical Constraints", "Non-Functional Requirements"],
    "sections_missing": ["Context & Vision"],
    "synthesis_timestamp": "2025-01-15T10:30:00Z",
    "warnings": []
  }
}
```


### Failure Response

```json
{
  "status": "FAILURE",
  "error_code": "MISSING_SPEC_SECTIONS",
  "error_message": "SPEC.md missing required sections: Functional Requirements",
  "spec_source": "docs/01-planning/specifications/feature-x/SPEC.md",
  "sections_found": ["Context & Vision", "Technical Constraints"],
  "sections_required": 3,
  "recovery_action": "Add Functional Requirements section with FR-XXX entries to SPEC.md",
  "partial_data": {
    "feature_name": "feature-x",
    "sections_parsed": 2
  }
}
```

### Error Codes

| Code | Condition | Recovery Action |
|------|-----------|-----------------|
| `SPEC_NOT_FOUND` | SPEC.md file does not exist | Create SPEC.md using spec template |
| `MISSING_SPEC_SECTIONS` | <3 required sections present | Add missing sections to SPEC.md |
| `NO_FUNCTIONAL_REQUIREMENTS` | FR section empty or missing | Add FR-XXX entries to requirements section |
| `NO_FR_TABLE_DETECTED` | FR section exists but no table | Format requirements as markdown table |
| `CIRCULAR_DEPENDENCY` | FR dependencies form cycle | Resolve circular references in SPEC.md |
| `PARSE_ERROR` | Malformed markdown structure | Fix markdown syntax errors |

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | SUCCESS or FAILURE |
| `feature_name` | string | On success | Extracted from SPEC.md title |
| `functional_requirements` | array | On success | Parsed FR entries with all metadata |
| `non_functional_requirements` | array | On success | Parsed NFR entries |
| `complexity_classification` | string | On success | SIMPLE, COMPLICATED, COMPLEX, or CHAOTIC |
| `dependencies` | object | On success | Internal FRs, external packages, blockers |
| `priority_distribution` | object | On success | MoSCoW counts and ratios |
| `context_confidence` | number | On success | 0.0-1.0 confidence in extraction accuracy |
| `error_code` | string | On failure | Machine-readable error identifier |
| `recovery_action` | string | On failure | Suggested fix for the error |


### Context Confidence Calculation

```python
def calculate_context_confidence(synthesis_result: dict) -> float:
    """Calculate confidence score for synthesis accuracy."""
    scores = []
    
    # Section coverage (0.3 weight)
    sections_found = len(synthesis_result['metadata']['sections_found'])
    section_score = min(sections_found / 5, 1.0)
    scores.append(('sections', section_score, 0.3))
    
    # FR extraction quality (0.3 weight)
    fr_count = len(synthesis_result['functional_requirements'])
    frs_with_criteria = sum(
        1 for fr in synthesis_result['functional_requirements']
        if fr['acceptance_criteria']
    )
    fr_quality = frs_with_criteria / fr_count if fr_count > 0 else 0
    scores.append(('fr_quality', fr_quality, 0.3))
    
    # Priority coverage (0.2 weight)
    priority_dist = synthesis_result['priority_distribution']['counts']
    has_must = priority_dist.get('Must', 0) > 0
    has_should = priority_dist.get('Should', 0) > 0
    priority_score = (0.5 if has_must else 0) + (0.5 if has_should else 0)
    scores.append(('priority', priority_score, 0.2))
    
    # Dependency clarity (0.2 weight)
    deps = synthesis_result['dependencies']
    has_internal = len(deps.get('internal', [])) > 0 or fr_count <= 5
    has_blockers = len(deps.get('blockers', [])) >= 0  # Always true
    dep_score = 0.5 if has_internal else 0.3
    dep_score += 0.5  # Blockers always analyzed
    scores.append(('dependencies', min(dep_score, 1.0), 0.2))
    
    # Weighted sum
    confidence = sum(score * weight for _, score, weight in scores)
    return round(confidence, 2)
```

---


## Anti-Patterns (NEVER DO)

### Context Building Anti-Patterns

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|--------------|------------------|
| Skip section validation | Missing sections cause incomplete synthesis | Validate >=3 sections before proceeding |
| Assume priority from position | FR order does not indicate priority | Use explicit MoSCoW detection algorithm |
| Ignore NFRs | NFRs affect complexity and phase planning | Always extract and include NFRs |
| Hardcode complexity | Different specs have different profiles | Calculate complexity from metrics |
| Parse only tables | FRs may be in bullet lists or prose | Use multiple detection patterns |

### FR Detection Anti-Patterns

```
# WRONG: Only check for table format
if '|' in line and 'FR-' in line:
    parse_row(line)

# CORRECT: Check multiple formats
fr_entries = []
fr_entries.extend(detect_fr_table(content))      # Tables
fr_entries.extend(detect_fr_bullets(content))    # Bullet lists
fr_entries.extend(detect_fr_prose(content))      # Inline prose
```

### Priority Extraction Anti-Patterns

```
# WRONG: Only check explicit keywords
if 'MUST' in text:
    return 'Must'

# CORRECT: Use full detection hierarchy
priority = detect_explicit_keyword(text)         # First: keywords
if not priority:
    priority = detect_table_column(text)         # Second: table structure
if not priority:
    priority = infer_from_fr_number(text)        # Third: FR-ID inference
if not priority:
    priority = 'Should'                          # Default fallback
```

### Dependency Detection Anti-Patterns

- **Ignore circular dependencies** - Always validate graph is acyclic before output
- **Miss implicit dependencies** - Check component relationships, not just FR references
- **Skip blocker identification** - Blockers critically affect plan phase structure


### Output Anti-Patterns

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|--------------|------------------|
| Return partial on FAILURE | Inconsistent downstream processing | Either SUCCESS with full data or FAILURE with recovery |
| Omit empty fields | Consumers expect consistent schema | Include all fields, use empty arrays/null for missing |
| Skip confidence score | No way to assess synthesis quality | Always calculate and include context_confidence |
| Missing line numbers | Cannot trace back to source | Include line_number for all extracted items |

### Integration Anti-Patterns

- **Generate plans directly** - This skill synthesizes context only; delegate to `generating-plans` skill
- **Modify SPEC.md** - Context synthesis is read-only; no file modifications
- **Execute validation** - Analysis only; no test execution or code running
- **Skip COMPONENT_ALMANAC check** - Always verify existing components for dependency analysis

---


## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Context Synthesis**:

| Framework | When to Use |
|-----------|-------------|
| [CAGEERF](../../docs/00-core/frameworks/planning.md) | Full context building workflow |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Dependency and cross-reference analysis |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Validate extraction completeness before output |

> **Selection Tip**: context building -> CAGEERF, dependencies -> Systems, validation -> Pre-Mortem

---


## Quick Reference

```
CONTEXT SYNTHESIS FLOW:
  1. Locate: SPEC.md (required), COMPONENT_ALMANAC.md (recommended)
  2. Validate: >=3 of 5 required sections present
  3. Extract: Parse FR table, detect priorities, find acceptance criteria
  4. Classify: Calculate Cynefin complexity from FR count + dependencies + novelty
  5. Analyze: Build dependency graph, identify blockers
  6. Output: Return synthesis result for plan generation

SPEC.MD REQUIRED SECTIONS (>=3 of 5):
  - Context & Vision (motivation)
  - Functional Requirements (CRITICAL - FR table)
  - User Scenarios (acceptance criteria)
  - Non-Functional Requirements (quality gates)
  - Technical Constraints (implementation bounds)

MOSCOW PRIORITY DETECTION:
  Must:   "MUST", "SHALL", "REQUIRED" | FR-001 to FR-010 default
  Should: "SHOULD", "RECOMMENDED"    | FR-011 to FR-020 default
  Could:  "COULD", "MAY", "OPTIONAL" | FR-021+ default
  Won't:  "WON'T", "OUT OF SCOPE"    | Explicit exclusion only

ICE SCORE (Optional):
  Impact (1-10) x Confidence (1-10) x Ease (1-10) = 1-1000
  Detection: Inline (I:7,C:8,E:6) | Table columns | Separate section
  Canonical: .claude/docs/00-core/orchestrator-thresholds.md#ice-score-thresholds

COMPLEXITY CLASSIFICATION (Cynefin):
  SIMPLE:      1-5 FRs,   <20% deps  -> 1 phase, linear
  COMPLICATED: 6-15 FRs,  20-50% deps -> 2-3 phases, structured
  COMPLEX:     16-30 FRs, >50% deps  -> 3-4 phases, iterative
  CHAOTIC:     >30 FRs,   unknown    -> MVP + discovery phases

COMPLEXITY FORMULA:
  score = (fr_score × 0.35) + (dep_score × 0.30) + (novel_score × 0.20) + (nfr_score × 0.15)
  <0.25 = SIMPLE | <0.50 = COMPLICATED | <0.75 = COMPLEX | >=0.75 = CHAOTIC

OUTPUT CONTRACT:
  SUCCESS: feature_name + functional_requirements[] + non_functional_requirements[]
           + complexity_classification + dependencies + priority_distribution
           + context_confidence (0.0-1.0)
  FAILURE: error_code + error_message + recovery_action + partial_data

ERROR CODES:
  SPEC_NOT_FOUND           -> Create SPEC.md
  MISSING_SPEC_SECTIONS    -> Add missing sections (need >=3)
  NO_FUNCTIONAL_REQUIREMENTS -> Add FR-XXX entries
  CIRCULAR_DEPENDENCY      -> Resolve FR cross-reference cycles

ALWAYS CHECK:
  - FR section exists and has parseable entries
  - Priority detection uses full hierarchy (keywords -> table -> inference)
  - Dependency graph is acyclic (no circular references)
  - Context confidence >= 0.70 before downstream processing

NEXT STEP:
  Pass synthesis result to generating-plans skill for PLAN.json creation
```

---


## Cross-References

### Related Skills

| Skill | Relationship |
|-------|--------------|
| [generating-plans](../generating-plans/SKILL.md) | Receives synthesis output, generates PLAN.json (downstream) |
| [task-context-synthesis](../task-context-synthesis/SKILL.md) | Parallel skill for PLAN.md -> task context (sibling) |
| [validating-specifications](../validating-specifications/SKILL.md) | SPEC.md validation before synthesis (upstream) |
| [codebase-research](../codebase-research/SKILL.md) | Component discovery methodology |

### Shared Documentation

| Document | Purpose |
|----------|---------|
| [COMPONENT_ALMANAC.md](../../../docs/00-project/COMPONENT_ALMANAC.md) | Existing component registry for dependency analysis |
| [Thinking Frameworks](../../docs/00-core/frameworks/README.md) | CAGEERF and analysis frameworks |
| [Agent Selection Guide](../../docs/01-guides/agents/agent-selection-guide.md) | Agent assignment reference |

### Algorithm Cross-References

| Algorithm | Source Skill | Usage in This Skill |
|-----------|--------------|---------------------|
| Cynefin Classification | generating-plans | Complexity domain determination |
| Section Detection | generating-plans | SPEC.md section parsing |
| MoSCoW Priority | generating-plans | Priority extraction hierarchy |
| Dependency Graph | task-context-synthesis | FR cross-reference analysis |


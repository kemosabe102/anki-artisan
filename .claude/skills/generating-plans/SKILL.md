---
name: generating-plans
description: >
  Use this skill when transforming SPEC.md into implementation plans, applying 
  MoSCoW-to-phase mapping, FR-to-feature conversion, or calculating effort estimates. 
  Trigger keywords: generate plan, plan creation, phase mapping, PLAN.json.
---

# Generating Plans

*Transform specifications into phased implementation plans with MoSCoW prioritization and effort estimation*

## Contents

- [SPEC.md Section Detection](#specmd-section-detection)
- [Cynefin Complexity Classification](#cynefin-complexity-classification)
- [MoSCoW-to-Phase Mapping Algorithm](#moscow-to-phase-mapping-algorithm)
- [FR-to-Feature Conversion Algorithm](#fr-to-feature-conversion-algorithm)
- [Step Generation Algorithm](#step-generation-algorithm)
- [Critical Path Calculation](#critical-path-calculation)
- [Effort Estimation Model](#effort-estimation-model)
- [Category Assignment Rules](#category-assignment-rules)
- [Risk-Scoring Algorithm](#risk-scoring-algorithm)
- [Research-Topic-Generation Algorithm](#research-topic-generation-algorithm)
- [Validation Gates](#validation-gates)
- [Quality Score Formula](#quality-score-formula)
- [Output Format](#output-format)
- [Anti-Patterns](#anti-patterns-never-do)
- [Quick Reference](#quick-reference)

---

## SPEC.md Section Detection

**Purpose**: Identify and extract plan-relevant sections from SPEC.md files.

### Required Sections (>=3 must be present)

| Section | Canonical Header | Fuzzy Matches | Plan Relevance |
|---------|------------------|---------------|----------------|
| Functional Requirements | `## Functional Requirements` | "FR-", "Requirements" | HIGH - primary feature source |
| User Scenarios | `## User Scenarios` | "Scenarios", "Use Cases", "Stories" | HIGH - acceptance criteria source |
| Technical Constraints | `## Technical Constraints` | "TC-", "Constraints", "Platform" | MEDIUM - implementation bounds |
| Non-Functional Requirements | `## Non-Functional Requirements` | "NFR-", "Performance", "Quality" | MEDIUM - quality gates |
| Pain Point Alignment | `## Pain Point Alignment` | "Pain Points", "Problems" | LOW - prioritization input |

### Section Detection Algorithm

```
FUNCTION detect_spec_sections(spec_content):
  sections = {}
  current_section = None
  
  FOR line IN spec_content.split('\n'):
    IF line.startswith('## '):
      header = line.strip('# ').strip()
      section_type = match_section_type(header)
      IF section_type:
        current_section = section_type
        sections[section_type] = { header: header, content: [], line_start: line_num }
    ELSE IF current_section AND line.strip():
      sections[current_section].content.append(line)
  
  RETURN sections

FUNCTION match_section_type(header):
  canonical_map = {
    "Functional Requirements": ["functional", "requirements", "fr-"],
    "User Scenarios": ["scenario", "use case", "story", "stories"],
    "Technical Constraints": ["constraint", "tc-", "platform", "technical"],
    "Non-Functional Requirements": ["non-functional", "nfr-", "performance", "quality"],
    "Pain Point Alignment": ["pain point", "problem", "alignment"]
  }
  
  header_lower = header.lower()
  FOR canonical, patterns IN canonical_map.items():
    IF any(p IN header_lower FOR p IN patterns):
      RETURN canonical
  RETURN None
```

### FR Table Detection

```
FUNCTION detect_fr_table(section_content):
  fr_entries = []
  in_table = False
  
  FOR line IN section_content:
    IF '|' IN line AND ('FR-' IN line OR 'MUST' IN line.upper() OR 'SHOULD' IN line.upper()):
      in_table = True
      IF 'FR-' IN line:
        fr = parse_fr_row(line)
        IF fr:
          fr_entries.append(fr)
    ELSE IF in_table AND not line.strip().startswith('|'):
      in_table = False
  
  RETURN fr_entries

FUNCTION parse_fr_row(line):
  cells = [c.strip() FOR c IN line.split('|') IF c.strip()]
  IF len(cells) >= 2:
    fr_id = extract_fr_id(cells[0])  # e.g., "FR-001"
    description = cells[1] IF len(cells) > 1 ELSE ""
    priority = detect_moscow_priority(line)
    RETURN { id: fr_id, description: description, priority: priority }
  RETURN None
```

### MoSCoW Priority Detection

```
FUNCTION detect_moscow_priority(text):
  text_upper = text.upper()
  
  IF 'MUST' IN text_upper AND 'SHOULD' NOT IN text_upper:
    RETURN 'Must'
  ELSE IF 'SHOULD' IN text_upper AND 'COULD' NOT IN text_upper:
    RETURN 'Should'  
  ELSE IF 'COULD' IN text_upper:
    RETURN 'Could'
  ELSE IF 'WON\'T' IN text_upper OR 'WILL NOT' IN text_upper:
    RETURN 'Won\'t'
  ELSE:
    # Infer from FR-ID pattern: FR-001 to FR-010 = Must, FR-011+ = Should
    fr_num = extract_fr_number(text)
    IF fr_num AND fr_num <= 10:
      RETURN 'Must'
    ELSE IF fr_num AND fr_num <= 20:
      RETURN 'Should'
    ELSE:
      RETURN 'Could'
```

---

## Cynefin Complexity Classification

**Purpose**: Classify project complexity to determine appropriate planning depth and phase structure.

### Cynefin Domains for Plan Generation

| Domain | FR Count | Dependency Density | Characteristics | Phase Strategy |
|--------|----------|-------------------|-----------------|----------------|
| SIMPLE | 1-5 | Low (<20% cross-refs) | Clear cause-effect, best practices exist | 1 phase, linear execution |
| COMPLICATED | 6-15 | Medium (20-50% cross-refs) | Analyzable, expert knowledge needed | 2-3 phases, structured approach |
| COMPLEX | 16-30 | High (>50% cross-refs) | Emergent patterns, probe-sense-respond | 3-4 phases, iterative with checkpoints |
| CHAOTIC | >30 or unclear | Very High/Unknown | Novel territory, act-sense-respond | MVP phase + discovery phases |

### Complexity Classification Algorithm

```
FUNCTION classify_complexity(spec_analysis):
  fr_count = len(spec_analysis.functional_requirements)
  dependency_density = calculate_dependency_density(spec_analysis)
  novel_tech_count = count_novel_technologies(spec_analysis)
  
  # Calculate base complexity score
  fr_score = categorize_fr_count(fr_count)
  dep_score = categorize_dependency_density(dependency_density)
  novel_score = categorize_novelty(novel_tech_count)
  
  complexity_score = (fr_score * 0.40) + (dep_score * 0.35) + (novel_score * 0.25)
  
  IF complexity_score < 0.25:
    RETURN { domain: 'SIMPLE', phases: 1, approach: 'linear' }
  ELSE IF complexity_score < 0.50:
    RETURN { domain: 'COMPLICATED', phases: 2, approach: 'structured' }
  ELSE IF complexity_score < 0.75:
    RETURN { domain: 'COMPLEX', phases: 3, approach: 'iterative' }
  ELSE:
    RETURN { domain: 'CHAOTIC', phases: 4, approach: 'emergent' }

FUNCTION calculate_dependency_density(spec):
  total_frs = len(spec.functional_requirements)
  IF total_frs == 0:
    RETURN 0
  
  cross_references = 0
  FOR fr IN spec.functional_requirements:
    refs = count_fr_references(fr.description)  # Count "FR-XXX" mentions
    cross_references += refs
  
  RETURN cross_references / total_frs

FUNCTION categorize_fr_count(count):
  IF count <= 5: RETURN 0.1
  ELSE IF count <= 10: RETURN 0.3
  ELSE IF count <= 15: RETURN 0.5
  ELSE IF count <= 25: RETURN 0.7
  ELSE: RETURN 0.9
```

### Phase Count Determination

```
FUNCTION determine_phase_count(complexity, fr_count, moscow_distribution):
  base_phases = complexity.phases
  
  # Adjust based on MoSCoW distribution
  must_ratio = moscow_distribution['Must'] / fr_count
  
  IF must_ratio > 0.7:
    # Heavy on Must = front-load work, may need extra phase
    base_phases = min(base_phases + 1, 4)
  ELSE IF must_ratio < 0.3:
    # Light on Must = can compress phases
    base_phases = max(base_phases - 1, 1)
  
  # Adjust based on total feature count
  IF fr_count > 20:
    base_phases = max(base_phases, 3)  # Large projects need at least 3 phases
  
  RETURN base_phases
```

---

## MoSCoW-to-Phase Mapping Algorithm

**Purpose**: Map requirements to implementation phases based on MoSCoW priority.

### Base Mapping Rules

| Priority | Phase Allocation | Rationale |
|----------|------------------|-----------|
| Must | Phase 1 (100%) | Critical path, MVP requirements |
| Should | Phase 1 (40%) + Phase 2 (60%) | Important but not blocking |
| Could | Phase 2 (30%) + Phase 3 (70%) | Nice-to-have, polish |
| Won't | Excluded | Out of scope for current plan |

### Phase Mapping Algorithm

```
FUNCTION map_requirements_to_phases(requirements, phase_count):
  phases = initialize_phases(phase_count)
  
  # Sort requirements by priority then by ID
  sorted_reqs = sort_by_priority_then_id(requirements)
  
  FOR req IN sorted_reqs:
    target_phases = get_target_phases(req.priority, phase_count)
    
    # Find best phase based on capacity and dependencies
    best_phase = select_optimal_phase(target_phases, req, phases)
    
    phases[best_phase].features.append(convert_to_feature(req))
  
  # Rebalance if phases are uneven
  phases = rebalance_phases(phases)
  
  RETURN phases

FUNCTION get_target_phases(priority, phase_count):
  IF priority == 'Must':
    RETURN [1]  # Must always goes to Phase 1
  ELSE IF priority == 'Should':
    IF phase_count == 1:
      RETURN [1]
    ELSE:
      RETURN [1, 2]  # Distribute across Phase 1-2
  ELSE IF priority == 'Could':
    IF phase_count <= 2:
      RETURN [phase_count]  # Last available phase
    ELSE:
      RETURN [2, 3]  # Distribute across Phase 2-3
  ELSE:  # Won't
    RETURN []  # Excluded

FUNCTION select_optimal_phase(target_phases, req, phases):
  IF not target_phases:
    RETURN None
  
  # Check dependency constraints
  FOR dep IN req.dependencies:
    dep_phase = find_phase_containing(dep, phases)
    IF dep_phase:
      # Requirement must be in same or later phase than dependency
      target_phases = [p FOR p IN target_phases IF p >= dep_phase]
  
  # Select phase with lowest load
  best_phase = None
  min_load = infinity
  FOR phase_num IN target_phases:
    load = calculate_phase_load(phases[phase_num])
    IF load < min_load:
      min_load = load
      best_phase = phase_num
  
  RETURN best_phase or target_phases[0]
```

### Phase Balancing Rules

```
FUNCTION rebalance_phases(phases):
  target_features_per_phase = total_features / len(phases)
  tolerance = 0.3  # Allow 30% deviation
  
  FOR i IN range(len(phases) - 1):
    current_phase = phases[i]
    next_phase = phases[i + 1]
    
    # Move Could/Should items forward if current phase is overloaded
    WHILE len(current_phase.features) > target_features_per_phase * (1 + tolerance):
      movable = find_movable_features(current_phase, ['Could', 'Should'])
      IF not movable:
        BREAK
      feature = movable[-1]  # Move lowest priority first
      IF not has_dependents_in_phase(feature, current_phase):
        move_feature(feature, current_phase, next_phase)
  
  RETURN phases

# Target: 3-7 features per phase (optimal for AI agent execution)
FUNCTION validate_phase_balance(phases):
  warnings = []
  FOR phase IN phases:
    feature_count = len(phase.features)
    IF feature_count < 3:
      warnings.append(f"{phase.name}: Under-loaded ({feature_count} features)")
    ELSE IF feature_count > 7:
      warnings.append(f"{phase.name}: Over-loaded ({feature_count} features)")
  RETURN warnings
```

---

## FR-to-Feature Conversion Algorithm

**Purpose**: Transform Functional Requirements (FR-XXX) into executable feature objects.

### Feature Object Schema

```json
{
  "id": "FR-001",
  "category": "functional|testing|infrastructure|documentation|performance",
  "description": "Human-readable feature description",
  "priority": "Must|Should|Could",
  "steps": ["Step 1", "Step 2", "Step 3"],
  "acceptance_criteria": ["Criterion 1", "Criterion 2"],
  "passes": false,
  "estimated_hours": 1.5
}
```

### Conversion Algorithm

```
FUNCTION convert_fr_to_feature(fr_entry, spec_context):
  feature = {
    id: fr_entry.id,
    description: clean_description(fr_entry.description),
    priority: fr_entry.priority or 'Should',
    passes: false
  }
  
  # Assign category based on FR content analysis
  feature.category = assign_category(fr_entry.description)
  
  # Generate implementation steps
  feature.steps = generate_steps(fr_entry, spec_context)
  
  # Extract or generate acceptance criteria
  feature.acceptance_criteria = extract_acceptance_criteria(fr_entry, spec_context)
  
  # Estimate effort
  feature.estimated_hours = estimate_feature_effort(feature)
  
  RETURN feature

FUNCTION clean_description(raw_description):
  # Remove FR-ID prefix if present
  desc = re.sub(r'^FR-\d+[:\s]*', '', raw_description)
  
  # Remove MUST/SHOULD/COULD keywords
  desc = re.sub(r'\b(MUST|SHOULD|COULD|SHALL|MAY)\b', '', desc, flags=re.I)
  
  # Clean up whitespace
  desc = ' '.join(desc.split()).strip()
  
  # Ensure starts with action verb
  IF not starts_with_verb(desc):
    desc = "Implement " + desc
  
  RETURN desc
```

### FR Grouping for Complex Requirements

```
FUNCTION group_related_frs(fr_list):
  groups = {}
  
  FOR fr IN fr_list:
    # Extract component/module from FR description
    component = extract_component(fr.description)
    
    IF component not in groups:
      groups[component] = []
    groups[component].append(fr)
  
  # Merge small groups (< 2 FRs) into nearest related group
  merged_groups = merge_small_groups(groups, min_size=2)
  
  RETURN merged_groups

FUNCTION extract_component(description):
  # Pattern matching for common component indicators
  patterns = [
    r'(?:in|for|of)\s+(?:the\s+)?(\w+(?:\s+\w+)?)\s+(?:service|module|component|system)',
    r'(\w+(?:\s+\w+)?)\s+(?:API|endpoint|interface)',
    r'(?:User|Admin|System)\s+(\w+)',
  ]
  
  FOR pattern IN patterns:
    match = re.search(pattern, description, re.I)
    IF match:
      RETURN match.group(1).lower()
  
  RETURN 'core'  # Default component
```

### Feature Splitting Rules

```
FUNCTION should_split_feature(feature):
  # Split if estimated hours > 3.0
  IF feature.estimated_hours > 3.0:
    RETURN True
  
  # Split if description contains multiple MUST clauses
  must_count = len(re.findall(r'\bMUST\b', feature.description, re.I))
  IF must_count > 1:
    RETURN True
  
  # Split if more than 5 acceptance criteria
  IF len(feature.acceptance_criteria) > 5:
    RETURN True
  
  RETURN False

FUNCTION split_feature(feature):
  sub_features = []
  
  IF feature.estimated_hours > 3.0:
    # Split by logical boundaries in steps
    step_groups = partition_steps(feature.steps, max_hours=2.0)
    FOR i, group IN enumerate(step_groups):
      sub_feature = copy(feature)
      sub_feature.id = f"{feature.id}-{chr(65+i)}"  # FR-001-A, FR-001-B
      sub_feature.steps = group.steps
      sub_feature.estimated_hours = group.estimated_hours
      sub_features.append(sub_feature)
  
  RETURN sub_features if sub_features else [feature]
```

---

## Step Generation Algorithm

**Purpose**: Generate 2-5 concrete implementation steps per feature.

### Step Generation Rules

| Step Count | When to Use | Example Scenario |
|------------|-------------|------------------|
| 2 steps | Simple, atomic features | Add config flag, update constant |
| 3 steps | Standard features | Create class, add methods, write tests |
| 4 steps | Features with integration | Setup, implement, integrate, validate |
| 5 steps | Complex features | Design, implement, test, integrate, document |

### Step Generation Algorithm

```
FUNCTION generate_steps(fr_entry, spec_context):
  steps = []
  category = assign_category(fr_entry.description)
  complexity = estimate_complexity(fr_entry)
  
  # Base step patterns by category
  step_templates = get_step_templates(category)
  
  # Select appropriate template based on complexity
  IF complexity == 'low':
    selected_steps = step_templates[:2]
  ELSE IF complexity == 'medium':
    selected_steps = step_templates[:3]
  ELSE:
    selected_steps = step_templates[:5]
  
  # Customize steps with FR-specific details
  FOR template IN selected_steps:
    step = customize_step(template, fr_entry, spec_context)
    steps.append(step)
  
  # Add verification step if not present
  IF not any('verify' in s.lower() or 'test' in s.lower() for s in steps):
    steps.append(generate_verification_step(fr_entry))
  
  RETURN steps

FUNCTION get_step_templates(category):
  templates = {
    'functional': [
      "Define {component} interface and data structures",
      "Implement core {action} logic in {module}",
      "Add error handling and edge case coverage",
      "Integrate with existing {dependency} components",
      "Write unit tests covering {test_scenarios}"
    ],
    'testing': [
      "Create test fixtures and mock data",
      "Implement test cases for {scope}",
      "Verify edge cases and error conditions",
      "Run tests and ensure >80% coverage"
    ],
    'infrastructure': [
      "Configure {service} settings and credentials",
      "Implement connection/client setup",
      "Add health check and monitoring hooks",
      "Document deployment requirements"
    ],
    'documentation': [
      "Draft {doc_type} outline and structure",
      "Write content for {sections}",
      "Add code examples and diagrams",
      "Review and validate accuracy"
    ],
    'performance': [
      "Establish baseline performance metrics",
      "Implement optimization for {bottleneck}",
      "Benchmark and compare results",
      "Document performance characteristics"
    ]
  }
  RETURN templates.get(category, templates['functional'])
```

### Step Customization

```
FUNCTION customize_step(template, fr_entry, spec_context):
  # Extract placeholders from template
  placeholders = re.findall(r'\{(\w+)\}', template)
  
  step = template
  FOR placeholder IN placeholders:
    value = extract_placeholder_value(placeholder, fr_entry, spec_context)
    step = step.replace(f'{{{placeholder}}}', value)
  
  RETURN step

FUNCTION extract_placeholder_value(placeholder, fr_entry, spec_context):
  mapping = {
    'component': extract_component(fr_entry.description),
    'action': extract_action_verb(fr_entry.description),
    'module': infer_module_path(fr_entry),
    'dependency': find_related_components(fr_entry, spec_context),
    'test_scenarios': generate_test_scenario_list(fr_entry),
    'scope': fr_entry.id,
    'service': extract_service_name(fr_entry),
    'doc_type': infer_doc_type(fr_entry),
    'sections': infer_doc_sections(fr_entry),
    'bottleneck': extract_performance_target(fr_entry)
  }
  RETURN mapping.get(placeholder, placeholder)
```

---

## Critical Path Calculation

**Purpose**: Identify blocking/foundational features that must complete before others.

### Critical Path Algorithm

```
FUNCTION calculate_critical_path(features, dependencies):
  # Build dependency graph
  graph = build_dependency_graph(features, dependencies)
  
  # Calculate earliest start times (forward pass)
  earliest = {}
  FOR feature IN topological_sort(graph):
    IF not graph.predecessors(feature):
      earliest[feature] = 0
    ELSE:
      earliest[feature] = max(
        earliest[pred] + get_duration(pred)
        FOR pred IN graph.predecessors(feature)
      )
  
  # Calculate latest start times (backward pass)
  project_end = max(earliest[f] + get_duration(f) FOR f IN features)
  latest = {}
  FOR feature IN reversed(topological_sort(graph)):
    IF not graph.successors(feature):
      latest[feature] = project_end - get_duration(feature)
    ELSE:
      latest[feature] = min(
        latest[succ] - get_duration(feature)
        FOR succ IN graph.successors(feature)
      )
  
  # Critical path = features where earliest == latest (zero slack)
  critical_path = [f FOR f IN features IF earliest[f] == latest[f]]
  
  RETURN sorted(critical_path, key=lambda f: earliest[f])

FUNCTION build_dependency_graph(features, spec_context):
  graph = DirectedGraph()
  
  FOR feature IN features:
    graph.add_node(feature.id)
    
    # Explicit dependencies from FR cross-references
    explicit_deps = find_fr_references(feature.description)
    FOR dep IN explicit_deps:
      IF dep IN [f.id FOR f IN features]:
        graph.add_edge(dep, feature.id)
    
    # Implicit dependencies from component relationships
    implicit_deps = infer_component_dependencies(feature, features)
    FOR dep IN implicit_deps:
      graph.add_edge(dep, feature.id)
  
  # Detect and resolve cycles
  IF has_cycle(graph):
    cycles = find_cycles(graph)
    RAISE PlanGenerationError(f"Circular dependency detected: {cycles}")
  
  RETURN graph
```

### Foundational Feature Detection

```
FUNCTION identify_foundational_features(features, graph):
  foundational = []
  
  FOR feature IN features:
    # Features with no predecessors that have multiple successors
    IF not graph.predecessors(feature.id):
      successor_count = len(graph.successors(feature.id))
      IF successor_count >= 2:
        foundational.append({
          feature: feature,
          blocks_count: successor_count,
          type: 'root'
        })
    
    # Features that are on critical path AND block multiple others
    IF feature.id IN critical_path:
      IF len(graph.successors(feature.id)) >= 2:
        foundational.append({
          feature: feature,
          blocks_count: len(graph.successors(feature.id)),
          type: 'bottleneck'
        })
  
  RETURN sorted(foundational, key=lambda f: -f['blocks_count'])
```

---

## Effort Estimation Model

**Purpose**: Estimate implementation hours per feature (0.5-3.0 range, split if >3.0).

### Effort Estimation Formula

```
estimated_hours = BASE_HOURS × complexity_multiplier × integration_multiplier

WHERE:
  BASE_HOURS = 1.0  (baseline for simple feature)
  complexity_multiplier = 1.0 + (step_count - 2) × 0.25 + criteria_count × 0.1
  integration_multiplier = 1.0 + dependency_count × 0.15 + novel_tech × 0.3
```

### Effort Estimation Algorithm

```
FUNCTION estimate_feature_effort(feature):
  # Base calculation
  step_count = len(feature.steps)
  criteria_count = len(feature.acceptance_criteria)
  
  # Complexity factors
  complexity = (
    (step_count - 2) * 0.25 +  # Each step beyond 2 adds 15 min
    criteria_count * 0.10       # Each criterion adds 6 min
  )
  
  # Integration factors
  dependency_count = count_dependencies(feature)
  novel_tech = has_novel_technology(feature)
  
  integration = (
    dependency_count * 0.15 +   # Each dependency adds 9 min
    (0.3 if novel_tech else 0)  # Novel tech adds 18 min
  )
  
  # Category adjustments
  category_multipliers = {
    'functional': 1.0,
    'testing': 0.8,        # Tests are often faster
    'infrastructure': 1.2, # Config/setup takes longer
    'documentation': 0.6,  # Docs are quick
    'performance': 1.3     # Performance work is complex
  }
  
  base_hours = 1.0
  multiplier = 1.0 + complexity + integration
  category_mult = category_multipliers.get(feature.category, 1.0)
  
  raw_estimate = base_hours * multiplier * category_mult
  
  # Clamp to valid range
  IF raw_estimate < 0.5:
    RETURN 0.5
  ELSE IF raw_estimate > 3.0:
    # Flag for splitting
    feature.needs_split = True
    RETURN 3.0
  ELSE:
    RETURN round(raw_estimate, 1)
```

### Effort Breakdown Table

| Factor | Weight | Example |
|--------|--------|---------|
| Base | 1.0 hr | Any feature |
| Per step (>2) | +0.25 hr | 4 steps = +0.5 hr |
| Per criterion | +0.10 hr | 3 criteria = +0.3 hr |
| Per dependency | +0.15 hr | 2 deps = +0.3 hr |
| Novel technology | +0.30 hr | New API/library |
| Infrastructure category | ×1.2 | Config, deployment |
| Documentation category | ×0.6 | Docs, comments |

---

## Category Assignment Rules

**Purpose**: Assign feature category (functional/testing/infrastructure/documentation/performance).

### Category Detection Algorithm

```
FUNCTION assign_category(description):
  desc_lower = description.lower()
  
  # Testing indicators (check first - most specific)
  testing_patterns = [
    r'\btest\b', r'\bspec\b', r'\bvalidat', r'\bverif',
    r'\bcoverage\b', r'\bassert', r'\bexpect\b'
  ]
  IF any(re.search(p, desc_lower) FOR p IN testing_patterns):
    RETURN 'testing'
  
  # Infrastructure indicators
  infra_patterns = [
    r'\bconfig', r'\bsetup\b', r'\bdeploy', r'\binfra',
    r'\bci/cd\b', r'\bpipeline\b', r'\benviron', r'\bk8s\b',
    r'\bdocker\b', r'\bhelm\b', r'\bterraform\b'
  ]
  IF any(re.search(p, desc_lower) FOR p IN infra_patterns):
    RETURN 'infrastructure'
  
  # Documentation indicators
  doc_patterns = [
    r'\bdoc\b', r'\breadme\b', r'\bguide\b', r'\btutorial\b',
    r'\bcomment', r'\bexplain', r'\bdescrib'
  ]
  IF any(re.search(p, desc_lower) FOR p IN doc_patterns):
    RETURN 'documentation'
  
  # Performance indicators
  perf_patterns = [
    r'\bperform', r'\boptimi', r'\bspeed\b', r'\blatency\b',
    r'\bthroughput\b', r'\bcach', r'\bscal', r'\beffici'
  ]
  IF any(re.search(p, desc_lower) FOR p IN perf_patterns):
    RETURN 'performance'
  
  # Default to functional
  RETURN 'functional'
```

### Category Distribution Guidelines

| Category | Target % | Rationale |
|----------|----------|-----------|
| functional | 50-70% | Core implementation work |
| testing | 15-25% | Quality assurance |
| infrastructure | 5-15% | Setup and deployment |
| documentation | 5-10% | Knowledge capture |
| performance | 0-10% | Optimization (often later phases) |

```
FUNCTION validate_category_distribution(features):
  counts = Counter(f.category FOR f IN features)
  total = len(features)
  
  warnings = []
  
  IF counts.get('functional', 0) / total < 0.5:
    warnings.append("Low functional feature ratio (<50%)")
  IF counts.get('testing', 0) / total < 0.15:
    warnings.append("Low testing feature ratio (<15%)")
  IF counts.get('functional', 0) / total > 0.8:
    warnings.append("Missing non-functional features (>80% functional)")
  
  RETURN warnings
```

---

## Risk-Scoring Algorithm

**Purpose**: Calculate weighted risk score for a plan step

**Input**: Step object with detected risk factors
**Output**: Float 0.0-1.0

### Factor Weights

| Factor | Weight | Rationale |
|--------|--------|-----------|
| security_implications | 2.0 | Security issues have highest impact |
| external_api | 1.5 | External dependencies introduce variability |
| novel_technology | 1.0 | Learning curve and unknowns |
| state_complexity | 1.0 | Debugging difficulty |
| performance_critical | 1.0 | Optimization needs |
| edge_case_density | 1.0 | Testing complexity |
| cross_cutting | 1.0 | Integration scope |

### Risk Score Formula

```
FUNCTION calculate_risk_score(step):
  max_possible_weight = 8.5  # Sum of all weights
  
  factor_weights = {
    'security_implications': 2.0,
    'external_api': 1.5,
    'novel_technology': 1.0,
    'state_complexity': 1.0,
    'performance_critical': 1.0,
    'edge_case_density': 1.0,
    'cross_cutting': 1.0
  }
  
  actual_weight = 0
  FOR factor IN step.detected_factors:
    actual_weight += factor_weights.get(factor, 0)
  
  risk_score = actual_weight / max_possible_weight
  
  RETURN round(risk_score, 2)
```

### Risk Classification

| Score Range | Priority | Action |
|-------------|----------|--------|
| >= 0.70 | MUST | Research required before implementation |
| >= 0.40 | SHOULD | Research recommended |
| < 0.40 | COULD | Research optional |

**Exception**: If `security_implications` detected, always MUST regardless of score

```
FUNCTION classify_risk_priority(step):
  risk_score = calculate_risk_score(step)
  
  # Security override
  IF 'security_implications' IN step.detected_factors:
    RETURN { priority: 'MUST', reason: 'Security implications detected' }
  
  # Score-based classification
  IF risk_score >= 0.70:
    RETURN { priority: 'MUST', reason: f'High risk score: {risk_score}' }
  ELSE IF risk_score >= 0.40:
    RETURN { priority: 'SHOULD', reason: f'Moderate risk score: {risk_score}' }
  ELSE:
    RETURN { priority: 'COULD', reason: f'Low risk score: {risk_score}' }
```

---

## Research-Topic-Generation Algorithm

**Purpose**: Generate relevant research topics from risk factors

**Input**: Risk factors array, step context
**Output**: Array of research topic strings

### Topic Templates per Factor

| Factor | Template 1 | Template 2 |
|--------|-----------|-----------|
| novel_technology | "Best practices for {tech}" | "{tech} common pitfalls and anti-patterns" |
| external_api | "{api} rate limiting and quotas" | "{api} error handling patterns" |
| security_implications | "OWASP guidelines for {concern}" | "Security audit checklist for {concern}" |
| state_complexity | "State management patterns for {context}" | "Testing strategies for stateful {context}" |
| performance_critical | "Performance optimization for {operation}" | "Benchmarking {operation}" |
| edge_case_density | "Edge case testing strategies for {domain}" | "Boundary condition handling in {domain}" |
| cross_cutting | "Observability patterns for {concern}" | "Logging best practices for {concern}" |

### Topic Generation Algorithm

```
FUNCTION generate_research_topics(step):
  topics = []
  
  templates = {
    'novel_technology': [
      "Best practices for {tech}",
      "{tech} common pitfalls and anti-patterns"
    ],
    'external_api': [
      "{api} rate limiting and quotas",
      "{api} error handling patterns"
    ],
    'security_implications': [
      "OWASP guidelines for {concern}",
      "Security audit checklist for {concern}"
    ],
    'state_complexity': [
      "State management patterns for {context}",
      "Testing strategies for stateful {context}"
    ],
    'performance_critical': [
      "Performance optimization for {operation}",
      "Benchmarking {operation}"
    ],
    'edge_case_density': [
      "Edge case testing strategies for {domain}",
      "Boundary condition handling in {domain}"
    ],
    'cross_cutting': [
      "Observability patterns for {concern}",
      "Logging best practices for {concern}"
    ]
  }
  
  FOR factor IN step.detected_factors:
    IF factor IN templates:
      factor_templates = templates[factor]
      FOR template IN factor_templates:
        topic = fill_template(template, step)
        topics.append(topic)
  
  RETURN topics
```

### Extraction Rules

```
FUNCTION fill_template(template, step):
  # Extract placeholders from template
  placeholders = re.findall(r'\{(\w+)\}', template)
  
  filled = template
  FOR placeholder IN placeholders:
    value = extract_entity(placeholder, step)
    filled = filled.replace(f'{{{placeholder}}}', value)
  
  RETURN filled

FUNCTION extract_entity(entity_type, step):
  desc = step.description
  
  extraction_patterns = {
    'tech': [
      r'using\s+(\w+(?:\.\w+)?)',           # "using React.js"
      r'with\s+(\w+(?:\.\w+)?)\s+(?:library|framework)',
      r'(\w+(?:\.\w+)?)\s+integration'
    ],
    'api': [
      r'(\w+)\s+API',                        # "Stripe API"
      r'(?:call|integrate|use)\s+(\w+)',
      r'(\w+)\s+(?:endpoint|service)'
    ],
    'concern': [
      r'(?:auth|security|encrypt|token|password|credential)\w*',
      r'(?:injection|xss|csrf|sanitiz)\w*'
    ],
    'context': [
      r'(\w+)\s+(?:state|session|cache)',
      r'managing\s+(\w+)'
    ],
    'operation': [
      r'(?:query|fetch|load|process|transform)\s+(\w+)',
      r'(\w+)\s+(?:operation|computation)'
    ],
    'domain': [
      r'(?:in|for)\s+(?:the\s+)?(\w+(?:\s+\w+)?)\s+(?:module|service|component)',
      r'(\w+)\s+(?:boundary|edge case)'
    ]
  }
  
  patterns = extraction_patterns.get(entity_type, [])
  
  FOR pattern IN patterns:
    match = re.search(pattern, desc, re.I)
    IF match:
      RETURN match.group(1) IF match.groups() ELSE match.group(0)
  
  # Fallback to generic description
  RETURN extract_key_noun(desc) OR entity_type

FUNCTION extract_key_noun(description):
  # Simple heuristic: find first capitalized word or noun phrase
  words = description.split()
  FOR word IN words:
    IF word[0].isupper() AND len(word) > 2:
      RETURN word.strip('.,;:')
  RETURN words[0] IF words ELSE 'component'
```

---

## Validation Gates

**Purpose**: 4 blocking gates that must pass before plan output is valid.

### Gate 1: Schema Compliance (BLOCKING)

```
FUNCTION validate_schema(plan):
  required_fields = {
    'root': ['project', 'description', 'total_features', 'phases', 'summary'],
    'phase': ['name', 'duration_weeks', 'target_completion', 'features'],
    'feature': ['id', 'category', 'description', 'priority', 'steps', 
                'acceptance_criteria', 'passes', 'estimated_hours'],
    'summary': ['total_features', 'total_estimated_hours', 'phases_total',
                'implementation_timeline', 'critical_path', 'launch_readiness_gates']
  }
  
  errors = []
  
  # Validate root fields
  FOR field IN required_fields['root']:
    IF field not in plan:
      errors.append(f"Missing required field: {field}")
  
  # Validate each phase
  FOR phase_key, phase IN plan.get('phases', {}).items():
    FOR field IN required_fields['phase']:
      IF field not in phase:
        errors.append(f"Phase {phase_key} missing field: {field}")
    
    # Validate each feature in phase
    FOR feature IN phase.get('features', []):
      FOR field IN required_fields['feature']:
        IF field not in feature:
          errors.append(f"Feature {feature.get('id', '?')} missing field: {field}")
  
  # Validate summary
  FOR field IN required_fields['summary']:
    IF field not in plan.get('summary', {}):
      errors.append(f"Summary missing field: {field}")
  
  RETURN { valid: len(errors) == 0, errors: errors }
```

### Gate 2: FR Coverage (BLOCKING)

```
FUNCTION validate_fr_coverage(plan, spec_frs):
  covered_frs = set()
  
  FOR phase IN plan['phases'].values():
    FOR feature IN phase['features']:
      # Extract FR-IDs from feature
      fr_ids = extract_fr_ids(feature['id'], feature['description'])
      covered_frs.update(fr_ids)
  
  # Check coverage
  spec_fr_ids = set(fr['id'] FOR fr IN spec_frs IF fr['priority'] != "Won't")
  missing_frs = spec_fr_ids - covered_frs
  
  coverage_ratio = len(covered_frs) / len(spec_fr_ids) IF spec_fr_ids ELSE 1.0
  
  RETURN {
    valid: len(missing_frs) == 0,
    coverage_ratio: coverage_ratio,
    missing: list(missing_frs),
    message: f"FR Coverage: {coverage_ratio:.1%} ({len(covered_frs)}/{len(spec_fr_ids)})"
  }
```

### Gate 3: Phase Structure (BLOCKING)

```
FUNCTION validate_phase_structure(plan):
  errors = []
  warnings = []
  
  phases = list(plan['phases'].values())
  
  # Check phase count
  IF len(phases) < 1:
    errors.append("Plan must have at least 1 phase")
  IF len(phases) > 4:
    warnings.append("Plan has >4 phases, consider consolidating")
  
  # Check feature distribution
  FOR i, phase IN enumerate(phases):
    feature_count = len(phase.get('features', []))
    
    IF feature_count < 1:
      errors.append(f"Phase {i+1} has no features")
    IF feature_count < 3:
      warnings.append(f"Phase {i+1} under-loaded ({feature_count} features)")
    IF feature_count > 7:
      warnings.append(f"Phase {i+1} over-loaded ({feature_count} features)")
  
  # Check Must features are in Phase 1
  phase_1_features = phases[0].get('features', []) IF phases ELSE []
  phase_1_priorities = [f.get('priority') FOR f IN phase_1_features]
  
  FOR phase IN phases[1:]:
    FOR feature IN phase.get('features', []):
      IF feature.get('priority') == 'Must':
        errors.append(f"Must-priority feature {feature['id']} not in Phase 1")
  
  RETURN { valid: len(errors) == 0, errors: errors, warnings: warnings }
```

### Gate 4: Acceptance Criteria Quality (BLOCKING)

```
FUNCTION validate_acceptance_criteria(plan):
  errors = []
  warnings = []
  
  FOR phase IN plan['phases'].values():
    FOR feature IN phase['features']:
      criteria = feature.get('acceptance_criteria', [])
      
      # Must have at least 1 criterion
      IF len(criteria) < 1:
        errors.append(f"Feature {feature['id']} has no acceptance criteria")
        CONTINUE
      
      # Each criterion should be measurable/testable
      FOR criterion IN criteria:
        IF not is_measurable(criterion):
          warnings.append(f"Feature {feature['id']}: criterion may not be measurable: '{criterion[:50]}'")
  
  RETURN { valid: len(errors) == 0, errors: errors, warnings: warnings }

FUNCTION is_measurable(criterion):
  # Check for measurable indicators
  measurable_patterns = [
    r'\d+',              # Contains numbers
    r'\b(pass|fail)\b',  # Pass/fail condition
    r'\b(return|output|display|show)\b',  # Observable action
    r'\b(within|under|above|below)\b',    # Threshold
    r'\b(complete|exist|contain)\b',      # State verification
    r'\b(error|exception|valid)\b',       # Error condition
  ]
  
  RETURN any(re.search(p, criterion, re.I) FOR p IN measurable_patterns)
```

---

## Quality Score Formula

**Purpose**: Calculate plan quality score for validation and reporting.

### Quality Score Calculation (v2)

```
quality_score = (
  schema_score × 0.20 +      # Schema compliance
  coverage_score × 0.25 +    # FR coverage
  structure_score × 0.20 +   # Phase structure quality
  criteria_score × 0.15 +    # Acceptance criteria quality
  risk_coverage × 0.20       # Risk annotation coverage
)
```

### Risk Coverage Calculation

```
FUNCTION calculate_risk_coverage(plan):
  steps_requiring_annotation = 0
  annotated_steps = 0
  
  FOR phase IN plan['phases'].values():
    FOR feature IN phase['features']:
      FOR step IN feature['steps']:
        detected_factors = detect_risk_factors(step)
        
        IF len(detected_factors) > 0:
          steps_requiring_annotation += 1
          
          IF step.has_risk_annotation():
            annotated_steps += 1
  
  IF steps_requiring_annotation == 0:
    RETURN 1.0  # No risky steps = full coverage
  
  RETURN annotated_steps / steps_requiring_annotation

FUNCTION detect_risk_factors(step):
  factors = []
  step_lower = step.description.lower()
  
  factor_patterns = {
    'security_implications': [r'auth', r'token', r'password', r'encrypt', r'credential', r'secret'],
    'external_api': [r'api', r'endpoint', r'third.party', r'external', r'webhook'],
    'novel_technology': [r'new\s+\w+', r'first time', r'unfamiliar', r'experimental'],
    'state_complexity': [r'state', r'session', r'cache', r'persist', r'transaction'],
    'performance_critical': [r'performance', r'latency', r'throughput', r'optimize', r'scale'],
    'edge_case_density': [r'edge case', r'boundary', r'corner case', r'exception'],
    'cross_cutting': [r'logging', r'monitoring', r'observability', r'tracing', r'audit']
  }
  
  FOR factor, patterns IN factor_patterns.items():
    IF any(re.search(p, step_lower) FOR p IN patterns):
      factors.append(factor)
  
  RETURN factors
```

### Dimension Scoring

```
FUNCTION calculate_quality_score(plan, spec_frs):
  # Gate 1: Schema Compliance (0.20 weight)
  schema_result = validate_schema(plan)
  schema_score = 1.0 IF schema_result.valid ELSE 0.0
  
  # Gate 2: FR Coverage (0.25 weight)
  coverage_result = validate_fr_coverage(plan, spec_frs)
  coverage_score = coverage_result.coverage_ratio
  
  # Gate 3: Phase Structure (0.20 weight)
  structure_result = validate_phase_structure(plan)
  structure_score = calculate_structure_score(structure_result)
  
  # Gate 4: Acceptance Criteria (0.15 weight)
  criteria_result = validate_acceptance_criteria(plan)
  criteria_score = calculate_criteria_score(criteria_result, plan)
  
  # Gate 5: Risk Coverage (0.20 weight)
  risk_coverage_score = calculate_risk_coverage(plan)
  
  # Weighted total
  quality_score = (
    schema_score * 0.20 +
    coverage_score * 0.25 +
    structure_score * 0.20 +
    criteria_score * 0.15 +
    risk_coverage_score * 0.20
  )
  
  RETURN {
    total: round(quality_score, 3),
    dimensions: {
      schema: schema_score,
      coverage: coverage_score,
      structure: structure_score,
      criteria: criteria_score,
      risk_coverage: risk_coverage_score
    },
    grade: score_to_grade(quality_score)
  }

FUNCTION calculate_structure_score(result):
  IF not result.valid:
    RETURN 0.0
  
  # Deduct for warnings
  warning_penalty = len(result.warnings) * 0.1
  RETURN max(0.0, 1.0 - warning_penalty)

FUNCTION calculate_criteria_score(result, plan):
  IF not result.valid:
    RETURN 0.0
  
  total_features = sum(len(p['features']) FOR p IN plan['phases'].values())
  warnings_ratio = len(result.warnings) / total_features IF total_features ELSE 0
  
  RETURN max(0.0, 1.0 - warnings_ratio)
```

### Quality Thresholds

| Score | Grade | Action |
|-------|-------|--------|
| >= 0.85 | PASS | Output ready for implementation |
| 0.70-0.84 | WARN | Output with warnings, suggest improvements |
| < 0.70 | FAIL | Regenerate plan, address blocking issues |

```
FUNCTION score_to_grade(score):
  IF score >= 0.85:
    RETURN { grade: 'PASS', action: 'Output ready for implementation' }
  ELSE IF score >= 0.70:
    RETURN { grade: 'WARN', action: 'Review warnings before proceeding' }
  ELSE:
    RETURN { grade: 'FAIL', action: 'Regenerate plan with corrections' }
```

---

## Output Format

**Purpose**: Define PLAN.json schema with examples.

### PLAN.json Schema

```json
{
  "project": "PROJECT_NAME",
  "description": "High-level description of what this project solves and delivers",
  "total_features": 12,
  "spec_source": "docs/01-planning/specifications/XXX-feature/SPEC.md",
  "phases": {
    "phase_1": {
      "name": "Phase 1: Foundation - Core Infrastructure",
      "duration_weeks": 2,
      "target_completion": "Week 2",
      "features": [
        {
          "id": "FR-001",
          "category": "functional",
          "description": "Implement user authentication service",
          "priority": "Must",
          "steps": [
            "Define AuthService interface and data structures",
            "Implement JWT token generation and validation",
            "Add password hashing with bcrypt",
            "Write unit tests covering auth scenarios"
          ],
          "acceptance_criteria": [
            "AuthService returns valid JWT for correct credentials",
            "Invalid credentials return 401 error",
            "Token expiration enforced at 24 hours"
          ],
          "passes": false,
          "estimated_hours": 2.0
        }
      ]
    },
    "phase_2": {
      "name": "Phase 2: Integration - API and Data Layer",
      "duration_weeks": 2,
      "target_completion": "Week 4",
      "features": []
    }
  },
  "summary": {
    "total_features": 12,
    "total_estimated_hours": 18.5,
    "phases_total": 2,
    "implementation_timeline": "4 weeks",
    "critical_path": [
      "FR-001 (foundational, blocks FR-003, FR-005)",
      "FR-003 (core logic, blocks FR-007)"
    ],
    "launch_readiness_gates": [
      "Phase 1 Complete: All auth and data models pass unit tests",
      "Phase 2 Complete: E2E integration tests pass with >80% coverage"
    ]
  }
}
```

### Phase Naming Convention

```
Phase {N}: {Theme} - {Goal}

Examples:
- Phase 1: Foundation - Core Infrastructure
- Phase 2: Integration - API and Data Layer  
- Phase 3: Enhancement - Performance and Polish
- Phase 4: Hardening - Security and Monitoring
```

### Feature ID Conventions

| Pattern | Usage | Example |
|---------|-------|---------|
| FR-XXX | Direct from SPEC.md | FR-001, FR-015 |
| FR-XXX-A | Split feature (part A) | FR-001-A, FR-001-B |
| INF-XXX | Infrastructure feature | INF-001 (deployment) |
| DOC-XXX | Documentation feature | DOC-001 (API docs) |
| PERF-XXX | Performance feature | PERF-001 (caching) |

### Output File Locations

```
docs/01-planning/specifications/{feature-name}/
├── SPEC.md           # Input specification
├── PLAN.json         # Generated plan (machine-readable)
├── PLAN.md           # Generated plan (human-readable summary)
└── plans/
    └── {variant}-PLAN.md  # Alternative plan variants
```

---

## Anti-Patterns (NEVER DO)

### Plan Generation Anti-Patterns

| Anti-Pattern | Why It's Bad | Correct Approach |
|--------------|--------------|------------------|
| Skipping FR analysis | Missing requirements | Always parse SPEC.md FR table first |
| Single giant phase | No incremental value | Split into 2-4 phases with clear goals |
| >7 features per phase | Cognitive overload | Target 3-7 features per phase |
| <3 features per phase | Under-utilizing phases | Merge small phases or add features |
| Must features in Phase 2+ | Blocking critical path | All Must features go in Phase 1 |
| Missing acceptance criteria | Unverifiable completion | Every feature needs 1-3 measurable criteria |
| Vague steps ("implement feature") | No actionable guidance | Concrete steps with file paths |
| >3 hour features | Too large to track | Split into sub-features (FR-001-A, FR-001-B) |
| Copying SPEC verbatim | No transformation value | Synthesize into actionable features |
| Ignoring dependencies | Broken execution order | Calculate critical path first |

### Step Generation Anti-Patterns

```
# WRONG: Vague, non-actionable
steps: ["Implement the feature", "Test it", "Deploy"]

# CORRECT: Specific, actionable
steps: [
  "Create UserService class in packages/auth/service.py",
  "Implement create_user() with password hashing",
  "Add input validation using Pydantic models",
  "Write unit tests in tests/unit/test_user_service.py"
]
```

### Acceptance Criteria Anti-Patterns

```
# WRONG: Subjective, unmeasurable
acceptance_criteria: ["Works correctly", "Good performance", "User-friendly"]

# CORRECT: Objective, measurable
acceptance_criteria: [
  "create_user() returns User object with hashed password",
  "Invalid email format raises ValidationError",
  "Response time under 100ms for single user creation"
]
```

### Phase Structure Anti-Patterns

```
# WRONG: No logical grouping
Phase 1: [FR-001, FR-007, FR-003, FR-012]  # Random order

# CORRECT: Logical grouping by dependency/theme
Phase 1: [FR-001, FR-002, FR-003]  # Foundation - Auth & Data Models
Phase 2: [FR-004, FR-005, FR-006]  # Integration - API Layer
Phase 3: [FR-007, FR-008]          # Enhancement - Performance
```

### Estimation Anti-Patterns

```
# WRONG: Round numbers without justification
estimated_hours: 2.0  # Why 2 hours?

# CORRECT: Derived from formula
estimated_hours: 1.8  # Base(1.0) + steps(3)*0.25 + criteria(2)*0.1 + deps(1)*0.15
```

---

## Quick Reference

### Plan Generation Pipeline

```
SPEC.md Input
    ↓
1. Section Detection → Extract FR table, scenarios, constraints
    ↓
2. Complexity Classification → SIMPLE/COMPLICATED/COMPLEX/CHAOTIC
    ↓
3. MoSCoW Mapping → Must→Phase1, Should→Phase1-2, Could→Phase2-3
    ↓
4. FR-to-Feature Conversion → Transform FR rows to feature objects
    ↓
5. Step Generation → 2-5 concrete steps per feature
    ↓
6. Critical Path Calculation → Identify blocking features
    ↓
7. Effort Estimation → 0.5-3.0 hours per feature
    ↓
8. Category Assignment → functional/testing/infra/docs/perf
    ↓
9. Validation Gates → Schema + Coverage + Structure + Criteria
    ↓
10. Quality Score → >= 0.85 = PASS
    ↓
PLAN.json Output
```

### Key Formulas

```
# Effort Estimation
estimated_hours = BASE(1.0) × (1 + complexity + integration) × category_mult

# Quality Score (v2)
quality = schema(0.20) + coverage(0.25) + structure(0.20) + criteria(0.15) + risk_coverage(0.20)

# Complexity Score
complexity = fr_score(0.40) + dep_score(0.35) + novel_score(0.25)
```

### Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Quality Score | >= 0.85 | PASS |
| Quality Score | 0.70-0.84 | WARN |
| Quality Score | < 0.70 | FAIL |
| Features per phase | 3-7 | Optimal |
| Hours per feature | 0.5-3.0 | Valid (split if >3.0) |
| Steps per feature | 2-5 | Optimal |
| Acceptance criteria | >= 1 | Required |
| FR Coverage | 100% | Required (excluding Won't) |

### MoSCoW Quick Reference

| Priority | Phase Target | Description |
|----------|--------------|-------------|
| Must | Phase 1 only | Critical path, MVP blocking |
| Should | Phase 1-2 | Important, not blocking |
| Could | Phase 2-3 | Nice-to-have, polish |
| Won't | Excluded | Out of scope |

### Category Patterns

| Category | Detection Keywords |
|----------|-------------------|
| functional | (default) implement, create, add, build |
| testing | test, spec, validate, verify, coverage |
| infrastructure | config, setup, deploy, ci/cd, k8s |
| documentation | doc, readme, guide, tutorial |
| performance | optimize, cache, speed, latency |

### Output Schema Quick Reference

```json
{
  "project": "string",
  "description": "string",
  "total_features": "number",
  "spec_source": "path/to/SPEC.md",
  "phases": {
    "phase_N": {
      "name": "Phase N: Theme - Goal",
      "duration_weeks": "number",
      "target_completion": "Week N",
      "features": [/* feature objects */]
    }
  },
  "summary": {
    "total_features": "number",
    "total_estimated_hours": "number",
    "phases_total": "number",
    "implementation_timeline": "N weeks",
    "critical_path": ["FR-001", "FR-002"],
    "launch_readiness_gates": ["gate 1", "gate 2"]
  }
}
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [generating-tasks](../generating-tasks/SKILL.md) | PLAN.json → TASKS.json (downstream) |
| [validating-specifications](../validating-specifications/SKILL.md) | SPEC.md validation (upstream) |
| [estimating-and-tracking](../estimating-and-tracking/SKILL.md) | Effort estimation formulas |
| [managing-roadmaps](../managing-roadmaps/SKILL.md) | Roadmap item integration |

---

## Thinking Frameworks

**Full Catalog**: [Thinking Frameworks README](../../docs/00-core/frameworks/README.md)

**Most Relevant for Plan Generation**:

| Framework | When to Use |
|-----------|-------------|
| [CAGEERF](../../docs/00-core/frameworks/planning.md) | Multi-phase plan structuring |
| [Systems Thinking](../../docs/00-core/frameworks/analysis.md) | Dependency and critical path analysis |
| [MoSCoW](../../docs/00-core/frameworks/planning.md) | Priority-based phase mapping |
| [Pre-Mortem](../../docs/00-core/frameworks/strategy.md) | Plan validation before output |

> **Selection Tip**: phase structure→CAGEERF, dependencies→Systems, priorities→MoSCoW, validation→Pre-Mortem

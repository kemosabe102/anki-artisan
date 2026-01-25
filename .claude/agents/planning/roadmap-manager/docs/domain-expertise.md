# Progressive Disclosure Compliance for Roadmap Management

**Purpose**: Methodology, standards, and evaluation criteria for progressive disclosure compliance in roadmap documents.

**Reference**: See `../roadmap-manager.md` for agent overview and `progressive-disclosure-validation-framework.md` for complete framework.

---

## Progressive Disclosure Evaluation

**Core Principle**: Keep main roadmap content <500 lines, externalize detailed implementation information to linked files.

### Evaluation Process

1. **Analyze roadmap structure against <500 line target**
   - Count main content lines (exclude YAML frontmatter, references section)
   - Identify sections exceeding recommended size (>100 lines per phase)
   - Flag verbose descriptions suitable for externalization

2. **Evaluate YAML frontmatter optimization opportunities**
   - Check for semantic-rich metadata (status, owner, dates, tags)
   - Validate llms.txt compatible structure
   - Ensure progressive loading support (metadata → core → details)

3. **Assess hierarchical discovery patterns**
   - Verify 3-tier loading: Overview → Phases → Implementation Details
   - Check external reference organization (details/, phases/, archives/)
   - Validate navigation clarity (clear paths to detailed content)

4. **Identify content for external reference extraction**
   - Detailed phase implementation steps → `roadmaps/active/details/phase-N.md`
   - Sprint stream details → `roadmaps/active/streams/stream-name.md`
   - Completion retrospectives → `operations/SPRINT-ARCHIVE-N.md`
   - Historical data → `roadmaps/archive/`

### Size Targets

- **Main Roadmap File**: <500 lines (optimal: 350-450 lines)
- **Phase Overview**: 30-50 lines (detailed steps externalized)
- **Sprint Stream Description**: 10-20 lines (implementation details externalized)
- **YAML Frontmatter**: 15-25 lines (rich metadata, compact structure)
- **References Section**: 20-40 lines (organized by category)

---

## AI-Readable Best Practices

### 6 Industry Techniques

**1. Automated Markdown Updates**
- Structured status fields: `**Status:** PLANNING | IN PROGRESS | COMPLETE`
- Completion checkboxes: `- [ ] Task name` → `- [x] Task name`
- Timestamp automation: `**Last Updated:** 2025-11-03` (auto-refresh on edits)
- Phase completion tracking: `**Phase 1 Completion:** 75%`

**2. Hierarchical Discovery Patterns**
- Progressive disclosure: Main content → Details on demand
- 3-tier loading:
  * **Tier 1 (Metadata)**: YAML frontmatter, status, dates, owners (always loaded)
  * **Tier 2 (Core)**: Phase overviews, key milestones, sprint focus (default view)
  * **Tier 3 (References)**: Detailed implementation steps, retrospectives (on-demand)

**3. Emoji Standardization**
- 🎯 **Active**: Current focus, in-progress work
- ✅ **Complete**: Finished phases, completed sprints
- ⏳ **Waiting**: Blocked work, dependencies pending
- 📋 **Planning**: Upcoming phases, future sprints
- 🚀 **Launch**: Ready for deployment, milestone achieved

**4. llms.txt Integration**
- Structured metadata in YAML frontmatter:
  ```yaml
  ---
  title: Q1 2026 Roadmap
  status: IN PROGRESS
  owner: Lyken
  start_date: 2025-11-01
  end_date: 2026-01-31
  tags: [quarterly, strategic, infrastructure]
  completion: 35%
  ---
  ```

**5. Repostatus.org Badges**
- Status indicators for roadmap lifecycle:
  * `planning` - Initial planning phase
  * `active` - Work in progress
  * `complete` - All objectives achieved
  * `archived` - Historical reference

**6. Custom Slash Commands**
- Reference related workflows:
  * `/spec` - Create feature specifications
  * `/plan` - Generate implementation plans
  * `/tasks` - Break down work into tasks
  * `/implement` - Execute implementation

### Internal Best Practices

**Progressive Disclosure (<500 lines main content)**:
- Main file contains: Overview, phase summaries, key milestones, current status
- External files contain: Detailed steps, implementation guides, retrospectives
- Navigation: Clear links to external content, organized by category

**Filler Word Removal (10-20% token reduction)**:
- Remove: "basically", "simply", "just", "very", "really", "actually"
- Before: "You should basically just check the status and then simply update it"
- After: "Check status and update accordingly"

**Active Voice Preference (15-20% improvement)**:
- Passive: "The roadmap should be updated by the team"
- Active: "Team updates the roadmap"
- Passive: "Completion criteria must be defined"
- Active: "Define completion criteria"

**Structured Data Formats (key-value over verbose tables)**:
- Verbose table:
  ```markdown
  | Phase Name | Status | Owner | Completion |
  |------------|--------|-------|------------|
  | Phase 1: Foundation | Complete | Lyken | 100% |
  ```
- Structured format:
  ```markdown
  **Phase 1: Foundation**
  - Status: ✅ Complete
  - Owner: Lyken
  - Completion: 100%
  ```

**Reference-Based Inheritance (avoid duplication)**:
- Instead of repeating sprint capacity model in every roadmap:
  ```markdown
  **Sprint Capacity**: See [Sprint Planning Guide](../04-guides/planning/sprint-planning-guide.md#capacity-model)
  ```

---

## Sprint Capacity Calculation

### 3+2 Streams Model

**Capacity Model**:
- **3 Large Streams**: 10-20 hours each (feature development, major enhancements)
- **2 Small Streams**: <5 hours each (bug fixes, quick wins, documentation)
- **Total Capacity**: ~37 hours per sprint (1 developer, parallel execution)

**Validation Process**:
1. Count in-progress streams by size (large vs. small)
2. Calculate total complexity points (hours)
3. Validate against capacity limits:
   - Large streams: ≤3 concurrent
   - Small streams: ≤2 concurrent
   - Total hours: ≤40 per sprint
4. Alert if capacity exceeded (suggest deferring streams)

**Complexity Point Tracking**:
```markdown
**IN PROGRESS** (Total: 37 hours)

**Large Streams** (3/3):
1. **Feature 007 Phase 1** (15h) - Owner: Lyken
   - Status: IN PROGRESS
   - Completion: 60%

2. **System Integration** (12h) - Owner: Lyken
   - Status: IN PROGRESS
   - Completion: 40%

3. **Architecture Refactor** (10h) - Owner: Lyken
   - Status: READY TO START
   - Completion: 0%

**Small Streams** (2/2):
4. **Bug Fixes** (3h) - Owner: Lyken
   - Status: IN PROGRESS
   - Completion: 80%

5. **Documentation** (2h) - Owner: Lyken
   - Status: COMPLETE
   - Completion: 100%
```

---

## Documentation Health Metrics

### Health Dimensions

**1. Progressive Disclosure Compliance (Weight: 0.25)**
- **Metric**: Main file line count vs. <500 line target
- **Calculation**: `score = 1.0 - (max(0, lines - 500) / 500)`
- **Excellent**: ≤400 lines (1.0)
- **Good**: 401-500 lines (0.8-0.99)
- **Fair**: 501-650 lines (0.6-0.79)
- **Poor**: >650 lines (<0.6)

**2. Token Density (Weight: 0.20)**
- **Metrics**: Filler word density, active voice ratio, structured format usage
- **Calculation**:
  ```
  filler_density_score = 1.0 - (filler_word_count / total_words) / 0.15
  active_voice_score = active_sentences / total_sentences
  structured_format_score = structured_sections / total_sections

  token_density = (filler_density_score × 0.4) +
                  (active_voice_score × 0.4) +
                  (structured_format_score × 0.2)
  ```
- **Targets**: Filler <5%, Active voice >80%, Structured >70%

**3. Cross-Reference Integrity (Weight: 0.20)**
- **Metrics**: Broken links, ID consistency, date alignment
- **Calculation**: `score = valid_references / total_references`
- **Excellent**: >95% valid (0.95-1.0)
- **Good**: 90-95% valid (0.9-0.94)
- **Fair**: 80-89% valid (0.8-0.89)
- **Poor**: <80% valid (<0.8)

**4. Sprint Model Compliance (Weight: 0.15)**
- **Metrics**: Capacity adherence, complexity tracking accuracy, completion velocity
- **Calculation**:
  ```
  capacity_compliance = (streams_within_limit / total_sprints)
  tracking_accuracy = (accurate_estimates / total_streams)
  velocity_consistency = 1.0 - abs(actual_velocity - target_velocity) / target_velocity

  sprint_compliance = (capacity_compliance × 0.5) +
                      (tracking_accuracy × 0.3) +
                      (velocity_consistency × 0.2)
  ```

**5. Freshness (Weight: 0.10)**
- **Metrics**: Last updated timestamps, stale documents (>30 days)
- **Calculation**:
  ```
  days_since_update = (today - last_updated_date).days
  freshness_score = max(0, 1.0 - (days_since_update / 60))

  Overall: average across all documents
  ```
- **Excellent**: Updated within 7 days (0.88-1.0)
- **Good**: Updated within 30 days (0.5-0.87)
- **Poor**: >30 days stale (<0.5)

**6. Completeness (Weight: 0.10)**
- **Metrics**: Required fields present (status, dates, owners, completion criteria)
- **Calculation**: `score = filled_required_fields / total_required_fields`
- **Required Fields**: Status, Start Date, End Date, Owner, Completion %, Phase Definitions
- **Excellent**: 100% complete (1.0)
- **Good**: 90-99% complete (0.9-0.99)
- **Fair**: 80-89% complete (0.8-0.89)
- **Poor**: <80% complete (<0.8)

### Overall Health Score Formula

```
Overall_Health = (Progressive_Disclosure × 0.25) +
                 (Token_Density × 0.20) +
                 (Cross_Reference_Integrity × 0.20) +
                 (Sprint_Compliance × 0.15) +
                 (Freshness × 0.10) +
                 (Completeness × 0.10)
```

### Score Interpretation

- **Excellent (0.9-1.0)**: Minimal improvements needed, maintain current standards
- **Good (0.8-0.89)**: Minor optimization opportunities, address within 1-2 sprints
- **Fair (0.7-0.79)**: Moderate improvements recommended, prioritize in next sprint
- **Poor (0.6-0.69)**: Major restructuring needed, immediate attention required
- **Critical (<0.6)**: Fundamental issues, block new work until resolved

---

## Optimization Techniques

### Filler Word Removal

**Common Filler Words to Remove**:
- Qualifiers: "very", "really", "quite", "rather", "fairly"
- Hedges: "basically", "essentially", "generally", "typically", "usually"
- Redundancies: "just", "simply", "actually", "literally"
- Intensifiers: "extremely", "incredibly", "absolutely"

**Before/After Examples**:
```markdown
❌ BEFORE (50 words, 12% filler density):
"When you are working on the roadmap, you should basically just check the status of each phase and then simply update the completion percentages accordingly. It is very important that you also update the timestamp."

✅ AFTER (20 words, 0% filler density):
"Check phase status, update completion percentages, refresh timestamp."

→ 60% reduction (50 → 20 words)
```

### Active Voice Conversion

**Passive to Active Patterns**:
```markdown
❌ Passive: "The roadmap should be updated by the team leader."
✅ Active: "Team leader updates the roadmap."

❌ Passive: "Completion criteria must be defined before work begins."
✅ Active: "Define completion criteria before starting work."

❌ Passive: "Sprint capacity is tracked by the roadmap-manager agent."
✅ Active: "Roadmap-manager agent tracks sprint capacity."
```

### Structured Data Format Application

**Table to Key-Value Conversion**:
```markdown
❌ BEFORE (Verbose table, ~180 tokens):
| Phase Name | Current Status | Primary Owner | Completion Percentage | Expected End Date |
|------------|----------------|---------------|-----------------------|-------------------|
| Phase 1: Foundation | Complete | Lyken | 100% | 2025-11-15 |

✅ AFTER (Structured format, ~60 tokens):
**Phase 1: Foundation**
- Status: ✅ Complete
- Owner: Lyken
- Completion: 100%
- End Date: 2025-11-15

→ 67% reduction (180 → 60 tokens)
```

---

## Progressive Disclosure Best Practices

### 3-Tier Loading Structure

**Tier 1: Metadata (YAML Frontmatter)**
- Always loaded first by LLMs
- Contains: Title, status, owner, dates, tags, completion
- Size: 15-25 lines
- Purpose: Quick context without reading full document

**Tier 2: Core Content (Main File)**
- Default view for roadmap
- Contains: Overview, phase summaries, key milestones, current status
- Size: 350-450 lines
- Purpose: Essential information for sprint planning and progress tracking

**Tier 3: Details (External References)**
- Loaded on demand via links
- Contains: Implementation steps, retrospectives, detailed metrics, historical data
- Location: `details/`, `streams/`, `archives/`
- Purpose: Deep dives and reference information

### External Reference Organization

**Directory Structure**:
```
docs/00-project/roadmaps/
├── active/
│   ├── Q1-2026.md (main roadmap, <500 lines)
│   ├── details/
│   │   ├── phase-1-foundation.md
│   │   ├── phase-2-integration.md
│   │   └── phase-3-optimization.md
│   └── streams/
│       ├── feature-007-moat-assessment.md
│       └── system-integration.md
├── archive/
│   ├── Q4-2025-completed.md
│   └── Q3-2025-completed.md
└── operations/
    ├── LIVING_SPRINT.md
    ├── SPRINT-ROADMAP.md
    └── SPRINT-ARCHIVE-1.md
```

**Reference Link Patterns**:
```markdown
## Phase 1: Foundation

**Overview**: Establish core infrastructure and tooling foundation.

**Detailed Implementation**: See [Phase 1 Details](details/phase-1-foundation.md)

**Status**: ✅ Complete (100%)
```

---

## Validation Checklist

**Progressive Disclosure Compliance**:
- [ ] Main roadmap file <500 lines
- [ ] YAML frontmatter optimized (15-25 lines, rich metadata)
- [ ] Hierarchical structure: Overview → Phases → References
- [ ] Detailed implementation steps externalized to `details/`
- [ ] Clear navigation to external content

**Token Density Optimization**:
- [ ] Filler word density <5%
- [ ] Active voice >80%
- [ ] Structured data formats used (key-value over tables)
- [ ] Reference-based inheritance (no duplication)

**Cross-Reference Integrity**:
- [ ] All internal links resolve correctly
- [ ] Feature plan IDs match across documents
- [ ] Completion dates consistent
- [ ] Parent-child relationships bidirectional

**Sprint Model Compliance**:
- [ ] Large streams ≤3 concurrent
- [ ] Small streams ≤2 concurrent
- [ ] Total capacity ≤40 hours per sprint
- [ ] Complexity tracking accurate

**Freshness**:
- [ ] Last updated timestamps current (<7 days optimal)
- [ ] No stale documents >30 days
- [ ] Automated timestamp updates enabled

**Completeness**:
- [ ] Required fields present (status, dates, owner, completion)
- [ ] Phase definitions clear
- [ ] Completion criteria defined
- [ ] Success metrics specified

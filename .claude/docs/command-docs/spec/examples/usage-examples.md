# Spec Command Usage Examples

Complete workflow examples with expected output.

---

## Example 1: Discovery Mode

### Input
```
/spec next
```

### Expected Output
```
🎯 ROADMAP: Top Development Candidates

✅ READY (3):
1. [SPEC-ENH-001] Regenerative Feature Specification System - P0 (Phase 4A) → 96% time reduction
   /spec roadmap:SPEC-ENH-001

2. [PROTO-001] Technical Implementation Planning Protocol - P0 (Phase 4B) → Strategic workflow foundation
   /spec roadmap:PROTO-001

3. [TASK-001] Executable Task Generation System - P0 (Phase 4C) → Automated task breakdown
   /spec roadmap:TASK-001

🟡 PLANNING (1):
1. [ROADMAP-PLAN-001] Roadmap Planning Command Development - P1 (Phase 4D) → Missing: success metrics, constraints
   /plan roadmap:ROADMAP-PLAN-001

💡 ACTIONS:
• /spec roadmap:SPEC-ENH-001     # Generate spec for specific item
• /spec next                      # Refresh candidates
• "Tell me more about SPEC-ENH-001"  # Get details

📖 DOCS: ROADMAP-Q4-2025.md | ROADMAP-READINESS-MATRIX.md
```

### Notes
- Uses Quick Reference section from roadmaps
- Excludes "In Progress" items
- Shows Ready items first, then Planning items

---

## Example 2: Roadmap Mode

### Input
```
/spec roadmap:SPEC-ENH-001
```

### Phase-by-Phase Output

**Phases 1-3: Context Preparation**
```
Loading project context...
✓ docs/00-project/SPEC.md
✓ docs/00-project/ROADMAP-Q4-2025.md
✓ docs/00-project/CUSTOMER-PAIN-POINTS-EXTERNAL.md

Resolving roadmap item: SPEC-ENH-001
✓ Status: Ready
✓ Title: Regenerative Feature Specification System
✓ Pain Points: Manual spec writing (P0), Inconsistent quality (P1)
```

**Phase 4: Directory Setup**
```
Creating feature directory...
✓ Next sequence: 003
✓ Directory: docs/01-planning/specifications/003-regenerative-spec-system/
✓ Subdirectories: plans/, tasks/, review/, code-review/
✓ SPEC.md initialized from template
```

**Phase 5: Spec Generation**
```
Generating specification...
⏳ Processing...
✓ SPEC.md populated (87 lines)
```

**Phases 6-9: Validation**
```
Validating specification...
✓ All required sections present
✓ Pain point alignment: 0.72 (target: ≥0.4) ✅
✓ ROI analysis: $2,400/month savings
✓ Requirements completeness: 0.85 ✅

Preparing review context...
✓ Review context generated
```

**Phase 10: Parallel Review**
```
Launching parallel review agents...

[Agent 1: planning] ⏳ Running...
[Agent 2: planning] ⏳ Running...
[Agent 3: architecture] ⏳ Running...

All reviews complete (12.3s parallel vs ~37s sequential)

planning: PASS
- Quality: 92/100
- HOW avoidance: PASS
- Critical Issues: 0

planning: PASS
- Business Alignment: 4.5/5
- ROI Validation: PASS
- Pain Point Coverage: 85%

architecture: PASS
- Technical Feasibility: HIGH
- Constraint Completeness: 90%
```

**Phase 12: Executive Summary**
```
## 🎯 Executive Summary: Regenerative Feature Specification System

### At a Glance
- **Business Value**: 96% reduction in specification time
- **Time Savings**: 40 hours/month
- **Cost**: $25/month (vs $100 budget: within) ✅
- **Timeline**: 2 sprints
- **Complexity**: MVP stage

### Pain Points Addressed ✅
- **Manual Spec Writing (P0)**: Automated generation → 4hrs→10min
- **Inconsistent Quality (P1)**: Template enforcement → 95% compliance

### 🚀 Ready for Next Phase
    /plan docs/01-planning/specifications/003-regenerative-spec-system/SPEC.md
```

---

## Example 3: Guide File Mode

### Input
```
/spec file:docs/04-guides/claude-code/codebase-navigation-guide.md
```

### Expected Output

**Phases 1-3: Context with Guide Extraction**
```
Loading project context...
✓ System context loaded

Processing guide file...
✓ File: docs/04-guides/claude-code/codebase-navigation-guide.md
✓ Type: technical_implementation_guide

Extracted from guide:
- Business Goals: 4 goals identified
- User Scenarios: 4 scenarios extracted
- Technical Patterns: Three-layer search, ripgrep, tree-sitter
- Performance Targets: <1s initial, <5s dependency
- Quality Targets: 95% accuracy

Derived feature name: "Codebase Navigation Agent"
```

**Phase 4: Directory Setup**
```
Creating feature directory...
✓ Directory: docs/01-planning/specifications/004-codebase-navigation-agent/
✓ SPEC.md initialized
```

**Phase 5: Spec Generation**
```
Generating specification with guide context...
✓ Reference guide context preserved
✓ Technical patterns mapped to constraints
✓ SPEC.md populated
```

**Reviews and Summary follow same pattern as Example 2**

---

## Example 4: Free-form Mode

### Input
```
/spec "Multi-tenant user management with role-based access control"
```

### Expected Output

**Phases 1-3: Context Preparation**
```
Loading project context...
✓ System context loaded

Analyzing free-form description...
⚠️ No roadmap item or guide reference
⚠️ Some context marked as [NEEDS VERIFICATION]:
   - Specific pain points
   - ROI estimates
   - Timeline constraints

Derived concepts:
- Multi-tenancy
- User management
- RBAC (Role-Based Access Control)

Derived feature name: "Multi-Tenant RBAC System"
```

**Phase 4: Directory Setup**
```
Creating feature directory...
✓ Directory: docs/01-planning/specifications/005-multi-tenant-rbac/
✓ SPEC.md initialized
```

**Validation with Warnings**
```
Validating specification...
✓ All required sections present
⚠️ Pain point alignment: [NEEDS VERIFICATION]
⚠️ ROI analysis: Estimated based on industry patterns
✓ Requirements completeness: 0.78 ✅

Note: Free-form input has gaps. Review carefully.
```

---

## Example 5: Error Handling

### Roadmap Item Not Ready

**Input**
```
/spec roadmap:ROADMAP-PLAN-001
```

**Output**
```
⚠️ Item ROADMAP-PLAN-001 is not ready for specification.

**Current Status**: Planning
**Missing Requirements**:
- [ ] Success metrics not defined
- [ ] Constraints not specified

**Actions**:
1. Complete the roadmap item first
2. Use `/plan roadmap:ROADMAP-PLAN-001` to plan unready items
3. Or provide free-form: `/spec "Roadmap planning command"`
```

### Directory Already Exists

**Input**
```
/spec roadmap:SPEC-ENH-001
```

**Output** (if run twice)
```
⚠️ Feature directory already exists:
docs/01-planning/specifications/003-regenerative-spec-system/

**Options**:
1. Continue with existing directory (may overwrite SPEC.md)
2. Create new directory with suffix: 003-regenerative-spec-system-v2/
3. Cancel and review existing spec

Choice [1/2/3]:
```

---

## Example 6: Interactive Walkthrough (Phase 13)

### Partial Output
```
## 📖 Specification Walkthrough: Regenerative Spec System

### Section 1: Business Value & Pain Points

**Summary**: Defines WHY we're building this feature.

**Key Points**:
- **Primary Pain Point**: Manual Spec Writing (P0)
  - Current: 4 hours per specification
  - After: 10 minutes per specification
  - Improvement: 96% reduction

- **Pain Point Alignment**: 0.72 ✅

- **ROI**: $2,400/month time savings

**Confidence**: HIGH

**Review Options**:
1. ✅ **Approve Section**
2. 🔄 **Refine**
3. ❓ **Question**
4. ⏭️ **Skip**

**Your Response**:
```

### User Approves
```
> 1

✅ Section 1 approved.

### Section 2: User Scenarios & Testing
...
```

### User Requests Refinement
```
> 2 - Add scenario for batch specification generation

Capturing feedback...
Applying section refinement...

✓ Scenario added: "Batch Specification - Generate specs for multiple features"

**Updated Section 1**:
[Shows updated content]

Approve now? [1: Yes / 2: Refine more]
```

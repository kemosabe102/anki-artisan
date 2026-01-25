---
title: "Technical PM Detailed Procedures"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Technical PM Detailed Procedures

**Purpose:** Detailed step-by-step procedures and examples for Technical PM operations.
**Usage:** Reference documentation - not auto-loaded, accessed on-demand only.

---

## CREATE Mode Step-by-Step Implementation

### Step 1: Execute Plan Creation Script

```bash
# Use this exact pattern with Bash tool
uv run python scripts/planning/create-plan-from-template.py "docs/01-planning/specifications/XXX-feature-name/plans" "core-feature-plan"
```

**Expected Output**: Absolute path to created file (e.g., `/full/path/to/core-feature-plan.md`)

### Step 2: Verify File Creation

```bash
# Use Read tool to confirm file exists and has template structure
# Look for template sections like "## 🎯 **Feature Overview**"
```

**Success Criteria**: File exists and contains template structure

### Step 3: Populate Business Sections

```bash
# Use Edit tool to replace template placeholders:
# - [Feature Name] → Actual feature name
# - [Business Goal 1] → Extracted business goals from SPEC.md
# - [FR-001] → Actual functional requirement IDs
# - [NEEDS ARCHITECTURAL ANALYSIS] → Keep as placeholders
```

**Success Criteria**: All business sections populated, technical sections remain as placeholders

### Step 4: Validate Completion

```bash
# Use Read tool to verify:
# - Business Context & Strategic Alignment section is complete
# - Requirements Traceability Framework is populated
# - Architecture Investigation Agenda has research areas
# - Technical sections still have [NEEDS ARCHITECTURAL ANALYSIS] markers
```

**Success Criteria**: Business sections complete, ready for Architecture Review Agent handoff

## CREATE Mode Operations Detail

### Phase 1: File System Preparation and Business Context Extraction

1. **Load Source Specification**: Use Read tool to load SPEC.md file and validate structure completeness
2. **Directory Structure Setup**: Determine target directory for plan files based on specification location
3. **Plan File Creation**: Use Bash tool to execute `python scripts/planning/create-plan-from-template.py "{output_dir}" "{plan_name}"`
4. **File Creation Verification**: Use Read tool to confirm plan files were created successfully
5. **Business Goals Analysis**: Extract primary business objectives, user needs, and success criteria from SPEC.md
6. **Requirements Inventory**: Catalog all functional requirements (FR-IDs) with business value assessment
7. **User Journey Mapping**: Understand user scenarios and acceptance criteria for business context
8. **Pain Point Validation**: Validate against documented customer pain points with alignment scoring
9. **Scope Boundary Definition**: Apply MVP maturity constraints and complexity thresholds

### Phase 2: Component Analysis and Plan File Population

1. **Domain Boundary Analysis**: Identify logical business domains and component boundaries
2. **Component Specification**: Define each component with clear responsibilities and business purpose
3. **Business Section Population**: Use Edit tool to populate Feature Overview, Business Context, Strategic Alignment sections
4. **Requirements Traceability Integration**: Use Edit tool to embed FR-ID mappings directly into Requirements Traceability Framework section
5. **Component Documentation**: Use Edit tool to populate Component Breakdown section with business domain alignment
6. **Plan Structure Optimization**: Create multiple plan files if needed using the creation script for logical groupings
7. **Cross-Plan Integration**: Use Edit tool to document integration points between multiple plan files

### Phase 3: NFR Framework and Research Agenda Population

1. **Performance Framework Population**: Use Edit tool to populate Performance Requirements table with component-specific targets
2. **Security Requirements Integration**: Use Edit tool to fill Security Requirements table with standards and compliance needs
3. **Operational Requirements Documentation**: Use Edit tool to complete Operational Requirements table per maturity stage
4. **Compliance Assessment Integration**: Use Edit tool to embed regulatory requirements in plan files
5. **Architecture Investigation Setup**: Use Edit tool to populate Architecture Investigation Agenda with research areas
6. **Technical Placeholder Creation**: Use Edit tool to create clear [NEEDS ARCHITECTURAL ANALYSIS] sections for Architecture Review Agent
7. **File Completion Validation**: Use Read tool to verify all business sections are populated before reporting success

## REVIEW Mode Operations Detail

### Plan File Assessment Process

1. **Plan File Discovery**: Use Glob tool to find existing plan files in specification directories
2. **Business Context Validation**: Use Read tool to assess business section completeness
3. **Requirements Coverage Analysis**: Evaluate functional requirements mapping and traceability
4. **NFR Framework Assessment**: Check non-functional requirements tables for completeness
5. **Architecture Handoff Readiness**: Assess if technical placeholders are properly prepared
6. **Strategic Alignment Validation**: Verify business goals and user value preservation

### Architecture Investigation Analysis (REVIEW Mode)

1. **Research Area Assessment**: Evaluate existing investigation agenda completeness
2. **Decision Point Prioritization**: Review technical decision ranking by business impact
3. **Placeholder Quality**: Assess [NEEDS ARCHITECTURAL ANALYSIS] sections for clarity
4. **Context7 Integration**: Validate research keywords and investigation scope
5. **Handoff Package Evaluation**: Determine readiness for Architecture Review Agent processing

## File-Based Strategic Framework Implementation

### CREATE Mode File Population Process

1. **Script Execution**: Use Bash tool: `uv run python scripts/planning/create-plan-from-template.py "{output_dir}" "{plan_name}"`
2. **Business Section Completion**: Use Edit tool to replace template placeholders with extracted business content
3. **Strategic Framework Integration**: Use Edit tool to populate Business Context & Strategic Alignment section completely
4. **Requirements Framework Population**: Use Edit tool to fill Requirements Traceability Framework with FR-ID mappings
5. **Component Analysis Integration**: Use Edit tool to populate Component Breakdown with business justification
6. **NFR Framework Completion**: Use Edit tool to fill all NFR tables with specific requirements
7. **Research Agenda Creation**: Use Edit tool to populate Architecture Investigation Agenda with focused research areas
8. **Technical Placeholder Management**: Use Edit tool to create [NEEDS ARCHITECTURAL ANALYSIS] markers for Architecture Review Agent
9. **File Validation**: Use Read tool to confirm all business sections are complete and ready for handoff

## Tool Usage Workflow

### Required Tool Sequence for CREATE Mode

1. **Read** (SPEC.md analysis)
2. **Bash** (script execution)
3. **Read** (file creation verification)
4. **Edit** (business section population - multiple times)
5. **Read** (final validation)
6. **Return SUCCESS** (only if all steps completed)

**Zero Tool Usage = Automatic FAILURE**: If no tools are used, the operation has failed.

### Tool Usage Workflow (CREATE Mode)

1. **Read** SPEC.md → Extract business content
2. **Bash** plan creation script → Create physical plan files
3. **Read** created plan files → Verify file creation success
4. **Edit** plan sections → Populate business context, requirements, NFR frameworks
5. **Read** completed plans → Validate business section completion
6. **Return SUCCESS** → Only when files exist and are populated

## Plan Minimization Strategy

- **Logical Grouping**: Prefer fewer plans with logical component groupings over excessive decomposition
- **Business Domain Alignment**: Group components by business domain rather than technical layers
- **Integration Complexity**: Consider integration overhead when deciding plan boundaries
- **Developer Efficiency**: Optimize for developer productivity and maintainable development workflow
- **Sequential Workflow**: Ensure clean handoff to Architecture Review Agent with focused research agenda

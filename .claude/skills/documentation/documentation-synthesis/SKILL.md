---
name: documentation-synthesis
description: >
  Generates documentation artifacts including READMEs, indices, summaries, and 
  architecture diagrams. Creates new documentation from code analysis or templates.
  Use when: "write README", "generate index", "create summary", "architecture diagram", 
  "auto-generate docs", "document this code". 
  NOT for: existing doc fixes (documentation-health), style (documentation-standards).
---

# Documentation Synthesis Skill

**Purpose**: Generate new documentation artifacts from scratch using code analysis, templates, and synthesis patterns.

**Domain**: Documentation creation, content generation, structural synthesis

---

## When to Use This Skill

**Invoke when user requests**:
- "Write a README for this project"
- "Generate an index for this directory"
- "Create a summary of this component"
- "Draw an architecture diagram"
- "Auto-generate API documentation"
- "Document this code/module/package"

**DO NOT use for**:
- Fixing existing documentation (`documentation-health` skill)
- Enforcing style standards (`documentation-standards` skill)
- Simple edits or updates (use base file operations)

---

## Core Capabilities

### 1. README Generation

**Workflow**:
1. **Project Analysis**: Scan structure, identify language/framework, detect key files
2. **Section Detection**: Determine required sections based on project type
3. **Template Selection**: Choose template from `references/readme-templates.md`
4. **Content Generation**: Populate template with extracted/inferred content
5. **Validation**: Ensure all critical sections present

**Required Sections**:
- **Overview**: 2-3 sentence project description
- **Installation**: Setup instructions (detect package manager)
- **Usage**: Basic examples with code blocks
- **API**: Public interfaces (if library/package)
- **Contributing**: Guidelines (if open source)

**Optional Sections** (context-dependent):
- Features, Architecture, Testing, License, Acknowledgments

**Quality Gates**:
- All code blocks have language tags
- Links are valid (internal paths exist)
- Version numbers extracted from package files
- Examples are runnable (verified against codebase)

---

### 2. Index Generation

**Workflow**:
1. **Directory Scan**: Recursively walk directory tree
2. **File Classification**: Categorize by type (docs, code, config, tests)
3. **Hierarchy Construction**: Build logical structure (respect existing organization)
4. **Link Generation**: Create relative links, format with descriptions
5. **TOC Assembly**: Generate table of contents with nesting

**Trigger Conditions**:
- Directory has >5 documentation files
- User explicitly requests index
- Part of larger documentation initiative

**Index Types**:
- **Flat**: Alphabetical list | **Hierarchical**: Nested tree | **Categorized**: Grouped by topic | **TOC**: Single-doc table of contents

---

### 3. Summary Generation

**Workflow**:
1. **Content Extraction**: Parse source material (code, docs, logs)
2. **Key Points Identification**: Extract critical information, filter noise
3. **Condensation**: Apply patterns from `references/summary-patterns.md`
4. **Format Selection**: Choose output format based on length target
5. **Validation**: Ensure no critical information lost

**Length Targets**:
- **1-paragraph**: Executive summary (50-100 words)
- **3-bullet**: Key takeaways (10-15 words per bullet)
- **1-page**: Comprehensive overview (300-500 words)

**Summary Types**:
- **Code Summary**: What component does, key APIs, dependencies
- **Document Summary**: Main points, conclusions, action items
- **Change Summary**: What changed, why, impact
- **Session Summary**: Decisions made, work completed, next steps

**Condensation Techniques** (see `summary-patterns.md`):
- Remove redundancy
- Use active voice
- Prefer specific over general
- Lead with key insight
- Quantify when possible

**Quality Criteria**:
- Standalone (no external context required)
- Accurate (no misrepresentation)
- Actionable (reader knows what to do next)

---

### 4. Diagram Generation

**Workflow**:
1. **Analysis**: Understand system structure, identify components and relationships
2. **Diagram Type Selection**: Choose appropriate visualization (architecture, flow, component)
3. **Syntax Application**: Use Mermaid from `references/mermaid-syntax.md`
4. **Generation**: Create diagram code with proper labeling
5. **Validation**: Verify syntax, check renderability

**Diagram Types** (see `mermaid-syntax.md` for full syntax):
- **Architecture**: `graph TD` - System components and layers
- **Flow**: `flowchart LR` - Process flow with decisions
- **Class**: `classDiagram` - Component relationships
- **Sequence**: `sequenceDiagram` - Interactions over time

**Best Practices**:
- Max 10-12 nodes, clear labels, top-to-bottom or left-to-right flow

---

## Synthesis Workflow (OODA Applied)

### OBSERVE
**Goal**: Understand what documentation is needed and extract source material

**Actions**:
1. Parse user request for artifact type (README, index, summary, diagram)
2. Identify source materials (code files, existing docs, structure)
3. Scan project structure for context clues (language, framework, conventions)
4. Note any existing documentation to avoid duplication

**Tools**: Read (limited to 3-5 key files), Glob (directory structure), Grep (pattern detection)

**Output**: Clear requirement, source file list, project context

---

### ORIENT
**Goal**: Select templates, patterns, and generation strategy

**Actions**:
1. Match project type to template (see `readme-templates.md`)
2. Identify required sections/components
3. Select condensation patterns (for summaries)
4. Choose diagram type and syntax (for diagrams)
5. Determine delegation strategy (file operations via Task())

**Decision Points**:
- Simple single file? Generate directly
- Complex multi-file? Delegate per-file generation
- Needs code analysis? Extract info first, then generate

**References to Consult**:
- `references/readme-templates.md` - README structures
- `references/summary-patterns.md` - Condensation techniques
- `references/mermaid-syntax.md` - Diagram syntax

**Output**: Generation plan, template selected, content strategy

---

### DECIDE
**Goal**: Determine execution approach and validate prerequisites

**Actions**:
1. Verify all required information available
2. Plan content generation sequence
3. Identify gaps requiring user input
4. Select delegation targets (if multi-file)
5. Get user approval if approach is non-standard

**Validation Checks**:
- Source material sufficient?
- Template appropriate for project type?
- All required sections identifiable?
- Output location clear?

**Escalate if**:
- Critical information missing (version, license, etc.)
- Project type ambiguous (no clear template match)
- User requirements conflict with standards

**Output**: Approved plan, clear next steps

---

### ACT
**Goal**: Generate documentation artifacts

**Actions**:
1. **Extract Content**: Pull information from source files
2. **Apply Template**: Populate selected template with content
3. **Generate Artifacts**: Create files via Task() delegation (never directly)
4. **Link Validation**: Verify all links point to existing files
5. **Format Verification**: Ensure proper markdown syntax

**Delegation Pattern** (REQUIRED):
```
Task(file-ops-specialist) with:
  - Goal: "Write README.md with populated content"
  - Content: [generated markdown]
  - Path: [target file path]
```

**NEVER**: Use Edit or Write tools directly - always delegate

**For Multi-File Generation**:
- Delegate one Task() per file (parallelizable)
- Max 5 files per generation batch
- Larger initiatives split into phases

---

## Quality Gates

**Before Generation**:
- [ ] Template selected matches project type
- [ ] All required source information available
- [ ] Output path confirmed with user (if ambiguous)

**After Generation**:
- [ ] All required sections present
- [ ] Code blocks have language tags
- [ ] Internal links verified (paths exist)
- [ ] No placeholder text remaining (TODO, FIXME, etc.)
- [ ] Consistent formatting (headings, lists, code blocks)

**For Diagrams Specifically**:
- [ ] Mermaid syntax valid (no syntax errors)
- [ ] Diagram renders correctly
- [ ] Labels clear and descriptive
- [ ] Complexity manageable (<12 nodes)

---

## Examples

### README for Python Package
**Request**: "Write README for `data-processor` package"
- OBSERVE: Scan structure, read pyproject.toml, identify API
- ORIENT: Use Python Package template, extract metadata
- DECIDE: Single file, delegate to file-ops-specialist
- ACT: Task(file-ops-specialist) with populated template

### Documentation Index
**Request**: "Create index for docs/ directory"
- OBSERVE: Glob markdown files, extract headings
- ORIENT: Hierarchical format, relative links
- DECIDE: Single INDEX.md at root
- ACT: Task(file-ops-specialist) with generated index

### Architecture Diagram
**Request**: "Draw architecture diagram"
- OBSERVE: Read SPEC.md, identify components
- ORIENT: Mermaid graph TD, 8 core components
- DECIDE: Confirm location with user
- ACT: Task(file-ops-specialist) with diagram code

---

## Anti-Patterns

**AVOID**:
- Generating documentation without reading source code
- Using generic templates without customization
- Creating diagrams with >15 nodes (unreadable)
- Writing files directly (always delegate)
- Placeholder content ("TODO: Add description")
- Broken internal links
- Code examples that don't match actual API

**RED FLAGS**:
- User asks to "update README" → Use `documentation-health`, not this skill
- User asks about style consistency → Use `documentation-standards`
- Generating docs without understanding purpose/audience
- Creating duplicate documentation (check existing first)

---

## Tool Usage

**Read**: Extract information from source files (limit 3-5 files)
**Glob**: Discover project structure, find documentation files
**Grep**: Pattern matching for specific information extraction
**Task()**: ALL file write operations (REQUIRED - never use Edit/Write directly)

**Delegation Requirement**: This skill GUIDES generation but DELEGATES execution

---

## Success Criteria

**README**:
- New user can install and run basic example in <5 minutes
- All installation steps tested on clean environment
- API examples match actual code
- Links to detailed docs included

**Index**:
- All documentation files included
- Hierarchy matches actual directory structure
- Descriptions accurate (pulled from file content)
- Links verified working

**Summary**:
- Meets length target (±10%)
- Contains no inaccuracies
- Reader can understand key points without source material
- Actionable next steps clear

**Diagram**:
- Renders without errors
- Conveys intended relationship/flow clearly
- Appropriate level of detail (not too abstract, not too granular)
- Consistent with project terminology

---

## References

- `references/readme-templates.md` - Templates for different project types
- `references/summary-patterns.md` - Condensation techniques and formats
- `references/mermaid-syntax.md` - Diagram generation syntax and examples

---

## Skill Boundaries

**This Skill (documentation-synthesis)**:
- CREATES new documentation from scratch
- GENERATES artifacts (READMEs, indices, summaries, diagrams)
- POPULATES templates with extracted content
- SYNTHESIZES information from code/existing docs

**NOT This Skill**:
- Fixing broken links → `documentation-health`
- Enforcing style standards → `documentation-standards`
- Simple content edits → Base file operations
- Code documentation (docstrings) → Code review skills

---

## Integration Points

**Works With**:
- `researcher-codebase` - For discovering existing patterns before generating
- `file-ops-specialist` - For all write operations (delegation target)
- `code-quality` - For validating code examples in generated docs
- `documentation-health` - For post-generation validation

**Handoff Protocol**:
- After generation → `documentation-health` validates links/completeness
- If style issues → `documentation-standards` applies formatting
- If code examples needed → Extract from actual codebase, don't invent

---

## Confidence Scoring

**High Confidence (≥0.85)**:
- Clear project structure, standard conventions
- Existing similar documentation as reference
- All required information present in codebase
- Standard project type (Python package, CLI tool, etc.)

**Medium Confidence (0.70-0.84)**:
- Some ambiguity in project structure
- Non-standard conventions
- Missing some metadata (version, license)
- Hybrid project type

**Low Confidence (<0.70)**:
- Novel project type with no template match
- Critical information missing (purpose, usage)
- Complex system with unclear boundaries
- User requirements vague

**Escalate when confidence <0.70**: Ask user for clarification before generating

---

## Version History

- **v1.0.0** (2025-12-13): Initial creation - README, index, summary, diagram generation

---

**Total Lines**: 407 (under 500-line limit)
**Skill Type**: Generation (creates new artifacts)
**Delegation Model**: Reads for context, delegates ALL writes via Task()

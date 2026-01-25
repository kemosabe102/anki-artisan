---
title: "Specify Command Output Schema"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Specify Command Output Schema

**Purpose:** Define the human-readable output format for the `/spec` command to ensure concise, actionable results.

## Output Format: Roadmap Analysis

### Structure Template:

```
🎯 ROADMAP: Top Development Candidates

✅ READY ({count}):
{id}. [{item_id}] {title} - {priority} → {impact}
   /spec roadmap:{item_id}

🟡 PLANNING ({count}):
{id}. [{item_id}] {title} - {priority} → Missing: {brief_gap_list}
   /plan roadmap:{item_id}

💡 ACTIONS:
• /spec roadmap:{item_id}  # Start with highest priority
• /plan roadmap:{item_id}     # Plan unready items first
• "Tell me more about {item_id}"  # Get details

📖 DOCS: {key_doc_1} | {key_doc_2}
```

## Output Format: Free-Form Specification

### Structure Template:

```
🎯 SPECIFICATION READY: {feature_name}

📋 GENERATED ARTIFACTS:
• SPEC: {path_to_spec_file}
• Directory: {feature_directory}
• Branch: {git_branch}

✅ QUALITY ASSESSMENT:
• Business Clarity: {High|Medium|Low}
• Technical Feasibility: {High|Medium|Low}
• Planning Readiness: {High|Medium|Low}

💡 NEXT STEPS:
• Review specification: Read {spec_file_path}
• Start planning: /plan {feature_name}
• Get details: "Summarize the specification for {feature_name}"

📖 SUPPORTING DOCS:
• Business Evidence: {relevant_docs}
• Research: {context7_references}
```

## Content Guidelines

### Brevity Rules:

- **One line per impact statement** - Max 80 characters, focus on key benefit
- **Brief gap lists** - Max 3 items, 5 words each
- **Essential docs only** - Maximum 2 core documents, pipe-separated
- **Actionable commands** - Exact syntax user can copy/paste in ACTIONS section

### Information Hierarchy:

1. **Immediate actions** - What can user do right now
2. **Context** - Where to find more information
3. **Next steps** - Natural workflow progression

### Interactive Elements:

- **Copy-paste commands** - No typing required
- **"Tell me more" prompts** - Standardized info requests
- **Document summarization** - Quick access to details

## Error/Edge Cases

### No Ready Items:

```
🎯 ROADMAP: No Ready Items

🟡 NEEDS WORK ({count}):
{brief_list_with_commands}

💡 ACTIONS:
• /plan roadmap:{item_id}     # Plan unready items first
• /spec "your feature description"  # Create new feature

📖 DOCS: roadmap-status.md | planning-guide.md
```

### Blocked Status:

```
⚠️ SPECIFICATION BLOCKED: {reason}

🔧 REQUIRED ACTION:
{specific_step_to_unblock}

💡 ALTERNATIVES:
• Try different item: /spec roadmap:{alternative_id}
• Get help: "What's blocking {item_id}?"

📖 GUIDANCE: {link_to_troubleshooting}
```

## Schema Validation

### Required Elements:

- [ ] Action commands (copy-pasteable)
- [ ] Business value (one line)
- [ ] Next steps (clear workflow)
- [ ] Documentation links (essential only)
- [ ] Interactive prompts (standardized)

### Forbidden Elements:

- ❌ Long explanations (>2 sentences)
- ❌ Technical jargon without definition
- ❌ Redundant information
- ❌ More than 5 documentation links
- ❌ Walls of text

## Integration Points

### Command Suggestions:

- `/spec roadmap:{id}` - Exact item specification
- `/plan roadmap:{id}` - Planning for unready items
- `"Tell me more about {id}"` - Detailed information
- `"Summarize {document}"` - Document analysis

### Documentation Integration:

- Business evidence documents
- Implementation guides
- Template references
- Research summaries

## Automated Workflow Integration

### Planner Agent Delegation Output

When specify command generates specification and delegates to planner agent:

```
🎯 SPECIFICATION GENERATED: {feature_name}

📋 GENERATED ARTIFACTS:
• SPEC: {spec_file_path}
• Directory: {feature_directory}
• Branch: {git_branch}

🤖 AUTOMATED WORKFLOW INITIATED:
• Planner agent reviewing specification for [NEEDS VERIFICATION] markers
• Attempting automatic resolution using available documentation
• Human report will be generated with remaining open questions

⏳ STATUS: Planner agent working... (no human approval required)

📖 NEXT: Review planner agent report when complete
```

### Comprehensive Output JSON Schema

For system processing and orchestration:

```json
{
  "status": "ok|blocked",
  "confidence_assessment": {
    "business_clarity": "High|Medium|Low",
    "technical_feasibility": "High|Medium|Low",
    "scope_definition": "High|Medium|Low",
    "planning_readiness": "High|Medium|Low",
    "overall_confidence": 0.0-1.0
  },
  "executive_summary": {
    "feature_overview": "concise description",
    "maturity_strategy": "MVP|Core approach with rationale",
    "key_highlights": ["top 3 benefits"],
    "planning_foundation": "how this enables detailed planning"
  },
  "feature_name": "extracted name",
  "feature_directory": "docs/01-planning/specifications/XXX-name/",
  "spec_file": "absolute path to SPEC.md",
  "roadmap_ref": "roadmap_id if applicable",
  "branch": "feat/XXX-name",
  "artifacts": {
    "spec_md": "path to SPEC.md",
    "clarifications_md": "path to CLARIFICATIONS.md",
    "metrics_json": "path to SPEC_METRICS.json"
  },
  "validation": {
    "pain_point_score": 0.0-3.0,
    "pain_point_decision": "APPROVE|NEEDS_REFINEMENT|REJECT",
    "maturity_ok": true|false,
    "complexity_assessment": "within constraints"
  },
  "next_action": "delegate_to_planner_immediately",
  "planner_delegation": {
    "task_type": "spec-review",
    "spec_file": "absolute path to SPEC.md",
    "roadmap_item": "roadmap item ID",
    "requires_human_approval": false,
    "delegation_message": "PROCEED IMMEDIATELY to planner agent for automated spec review"
  },
  "verification_needed": ["list of [NEEDS VERIFICATION] items"]
}
```

## Planner Agent Task Reference

**Spec Review Task Input:** Defined in `planner-input.schema.json` with `taskType: "spec-review"`
**Spec Review Task Output:** Defined in `spec-review-output.schema.json`
**Human Report Format:** Generated by planner agent per spec-review schema

This schema ensures the `/spec` command produces concise, actionable output that guides users to their next step without information overload, while supporting automated planner agent workflows.

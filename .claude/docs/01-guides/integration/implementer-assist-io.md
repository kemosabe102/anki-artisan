# development Assist I/O Contract

## Input Schema

When Orchestrator requests assistance:

```json
{
  "question": "Specific question needing clarification",
  "target_files": ["file1.md", "section3.2", "contracts/api.json"],
  "needed_by": "2025-09-20T14:00:00Z",
  "evidence_needed": "citations|excerpts|options|validation_implications"
}
```

## Output Schema

```json
{
  "citations": ["doc.md:L42", "spec.md:§3.2"],
  "excerpts": [{ "source": "doc.md:L42", "text": "relevant content" }],
  "options": ["option1 with rationale", "option2 with rationale"],
  "validation_implications": ["impact on V&V criteria"],
  "impact_on_tasks": ["T001", "T003"],
  "affected_sow_blocks": ["T001.sow", "T003.sow"],
  "open_questions": ["follow-up questions if needed"]
}
```

## Behavior Requirements

- **Locate/quote sources**: Provide paths/anchors with exact references
- **Task Impact Analysis**: Identify which task IDs and SoW blocks would be affected
- **Evidence-based**: Summarize findings with source attribution
- **Context pack only**: Provide evidence and analysis, not task assignments
- **Never delegate**: Don't assign work to sub-agents or make coordination decisions

## Response Guidelines

- **Precision**: Reference specific line numbers, section anchors, and commit hashes
- **Completeness**: Address all aspects of the question with evidence
- **Clarity**: Provide clear rationale for options and implications
- **Traceability**: Link all conclusions back to specific source material

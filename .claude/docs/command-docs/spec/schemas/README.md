# Spec Command Schemas

Schema documentation for the `/spec` slash command.

## Overview

The `/spec` command produces SPEC.md files following the template structure defined in:
- `docs/00-project/templates/spec-template.md`

## Output Structure

The command generates specifications with the following structure:

```
docs/01-planning/specifications/XXX-[feature-name]/
├── SPEC.md                              # Main specification document
├── plans/                               # For /plan output
├── tasks/                               # For /tasks output
├── review/                              # Review reports
│   ├── planning-report.md
│   ├── planning-report.md
│   └── architecture-report.md
└── code-review/                         # For implementation reviews
```

## SPEC.md Sections

| Section | Purpose | Required |
|---------|---------|----------|
| Pain Point Alignment | Business justification | ✅ |
| User Scenarios & Testing | User workflows | ✅ |
| Functional Requirements (Core) | MVP features | ✅ |
| Functional Requirements (Optional) | Future features | Optional |
| Technical Expectations | Constraints (WHAT/WHY) | ✅ |
| Risk Assessment | P×I×E scoring | ✅ |
| Component Breakdown | Sequencing | ✅ |

## Review Report Structure

Each review agent produces a report with:
- Overall Status: PASS/WARN/FAIL
- Dimension Scores: 0-100 or 0-5 scales
- Critical Issues: Must fix before planning
- Recommendations: Improvements

## Related Schemas

- Agent output schemas: `.claude/agents/*/schemas/`
- Spec template: `docs/00-project/templates/spec-template.md`
- Review template: `.claude/templates/spec-review-template.md`

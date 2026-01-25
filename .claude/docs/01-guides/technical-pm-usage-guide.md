---
title: "Technical PM Agent Usage Guide"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Technical PM Agent Usage Guide

## Overview

The Technical PM agent transforms SPEC.md files into comprehensive strategic plan frameworks with complete business context, requirements traceability, and focused architecture investigation guidance. It bridges the gap between business specifications and technical implementation.

## Workflow Position

```
SPEC.md → Technical PM Agent (strategic framework) → Architecture Review Agent (technical analysis) → Complete PLAN.md → /tasks command
```

## Key Capabilities

### ✅ **What Technical PM Does**

- **Business Context Extraction**: Complete business goals, user value propositions, and success criteria
- **Requirements Traceability**: 100% FR-ID to component mapping with coverage tracking
- **Component Identification**: Business domain-based component breakdown and logical plan structure
- **NFR Analysis**: Performance, security, operational requirements per component with business impact
- **Architecture Investigation Guidance**: Focused research areas with Context7 keywords and decision criteria
- **Template Enhancement**: Complete business sections while creating clear technical placeholders

### ❌ **What Technical PM Avoids**

- Technical architecture design (delegated to Architecture Review Agent)
- Implementation code structure decisions
- Final technology choices (provides research guidance only)
- Task decomposition (handled by subsequent workflow phases)

## Usage Patterns

### Primary Workflow (Recommended)

```javascript
// Sequential planning flow
const result = await delegateToAgent('planning', {
  task_id: 'strategic-framework-creation',
  operation_type: 'strategic_framework_creation',
  description: 'Transform SPEC.md into strategic framework for Architecture Review Agent',
  spec_source: {
    spec_file_path: 'docs/01-planning/specifications/XXX-feature-name/SPEC.md',
    feature_name: 'user-authentication-system',
    business_priority: 'P0',
  },
  strategic_requirements: {
    maturity_stage: 'MVP',
    complexity_threshold: 0.3,
    pain_point_targets: ['§1 Analysis Paralysis', '§3 Time Constraints'],
  },
  plan_strategy: {
    minimization_preference: true,
    domain_grouping_strategy: 'business_domain',
    max_plans_per_feature: 3,
  },
});

// Then delegate to Architecture Review Agent
const architectureResult = await delegateToAgent('architecture-agent', {
  operation_type: 'architecture_review',
  strategic_framework: result.operation_result.strategic_framework,
  investigation_agenda: result.operation_result.architecture_investigation_agenda,
});
```

### Quick Strategic Analysis

```javascript
// For rapid business context extraction
const quickAnalysis = await delegateToAgent('planning', {
  operation_type: 'requirements_analysis',
  spec_source: {
    spec_content: '// Direct SPEC content',
    feature_name: 'quick-feature',
  },
});
```

## Input Requirements

### Essential Fields

- **task_id**: Unique identifier
- **operation_type**: `strategic_framework_creation` (primary), `requirements_analysis`, `nfr_analysis`
- **description**: Clear description of strategic framework needs
- **spec_source**: Either `spec_file_path` OR `spec_content` with `feature_name`

### Strategic Requirements

- **maturity_stage**: MVP/Alpha/Beta/GA (affects NFR complexity)
- **complexity_threshold**: 0.0-1.0 (MVP typically 0.3)
- **pain_point_targets**: Customer pain points to address
- **business_constraints**: Budget, timeline, resource limitations

### Plan Strategy

- **minimization_preference**: true (prefer fewer, logical plans)
- **domain_grouping_strategy**: "business_domain" (recommended)
- **max_plans_per_feature**: 1-5 (typically 2-3)

## Expected Outputs

### Strategic Framework

- **Business Context**: Goals, user value, success criteria, pain point alignment
- **Component Analysis**: Business domain components with requirements mapping
- **Requirements Traceability**: 100% FR-ID coverage with business justification
- **NFR Framework**: Performance, security, operational requirements per component
- **Architecture Investigation Agenda**: Focused research areas for Architecture Review Agent

### Enhanced Plan Files

- **Business Sections Complete**: Feature overview, strategic value, success metrics
- **Technical Placeholders Ready**: Clear sections for Architecture Review Agent
- **Research Agenda Embedded**: Context7 keywords, decision criteria, trade-offs
- **Requirements Mapped**: Complete traceability matrix

## Built-In Research Guides

The Technical PM agent includes comprehensive research guides for common decisions:

- **Data Storage Guide**: PostgreSQL/MongoDB/Redis use case matrices
- **Authentication Guide**: OAuth2/JWT/session pattern analysis
- **API Design Guide**: REST/GraphQL decision factors
- **Caching Strategy Guide**: Latency impact and cost-benefit analysis
- **Search Technology Guide**: Technology comparison with business context
- **Cloud Architecture Guide**: Provider comparison and migration patterns

## Quality Validation

The agent validates output against these criteria:

- **Requirements Coverage**: Target 100% FR-ID mapping
- **Business Context Preservation**: Target 95% business goal transfer
- **Pain Point Alignment**: Minimum 0.4 alignment score
- **Strategic Framework Completeness**: All sections with business justification

## Integration with Architecture Review Agent

### Handoff Data

- **Investigation Areas**: Specific research topics with priorities
- **Decision Points**: Technology choices with business impact context
- **Research Keywords**: Context7/WebSearch terms for technical analysis
- **Technical Sections**: Ready placeholders for architecture content

### Coordination Benefits

- **Complete Business Context**: No information loss from SPEC to implementation
- **Focused Technical Analysis**: Architecture Review Agent gets clear research agenda
- **Efficient Workflow**: Sequential processing avoids duplicated analysis
- **Quality Handoff**: Clean boundaries between business and technical analysis

## Best Practices

### For Orchestrator

1. **Validate SPEC.md**: Ensure complete business context before delegation
2. **Set Appropriate Maturity**: Align complexity threshold with current stage
3. **Configure Plan Strategy**: Use minimization preference for maintainable development
4. **Chain with Architecture Review**: Always follow with technical analysis phase

### For Humans

1. **Review Strategic Framework**: Validate business context preservation
2. **Approve Plan Structure**: Confirm logical component grouping
3. **Validate Requirements Coverage**: Ensure no missing FR-ID mappings
4. **Check Investigation Agenda**: Confirm technical research priorities

## Error Handling

### Common Blockers

- **Incomplete SPEC.md**: Missing business goals or user scenarios
- **Vague Requirements**: Non-testable or ambiguous functional requirements
- **Complex Feature**: Exceeds maturity stage complexity threshold

### Resolution Patterns

- **NEEDS_CLARIFICATION**: Request SPEC.md enhancement with specific missing items
- **Partial Analysis**: Provide completed sections with clear blockers identified
- **Alternative Approaches**: Suggest specification refinement or scope reduction

## Performance Targets

- **Strategic Framework Creation**: 95% completed within 8 minutes
- **Requirements Coverage**: 100% FR-ID to component mapping
- **Business Context Preservation**: 95% business goal transfer accuracy
- **Architecture Review Handoff**: Ready technical placeholders with focused research agenda

---

**Agent Version**: v1.0.0 (Alpha)
**Workflow Integration**: Enhanced orchestrator workflow with sequential planning flow
**Template**: Enhanced plan template v2.0 with strategic framework capabilities

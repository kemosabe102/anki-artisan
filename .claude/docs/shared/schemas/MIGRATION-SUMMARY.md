# Schema Reorganization Migration Summary

**Date**: 2025-11-19
**Task**: Reorganize agent schemas from centralized `.claude/docs/schemas/` into plugin-specific directories

## Files Moved

### Dev-Tools Plugin (31 schemas)
**Location**: `.claude/agents/dev-tools/schemas/`

1. claude-code-ecosystem.schema.json
2. architecture.schema.json
3. architecture.schema.json
4. orchestrator-task.schema.json (renamed from claude-code.schema.json)
5. context-optimizer.schema.json
6. context-readiness-assessor.schema.json
7. contingency-planner.schema.json
8. debugger.schema.json
9. documentation.schema.json
10. documentation.schema.json
11. git-github.schema.json
12. grafana-dashboard-builder.schema.json
13. hypothesis-former.schema.json
14. intent-analyzer.schema.json
15. deployment-release.schema.json
16. loki-query-specialist.schema.json
17. planning.schema.json
18. claude-code-ecosystem.schema.json
19. promql-query-builder.schema.json
20. development.schema.json
21. code-quality.schema.json
22. planning.schema.json
23. sast-scanner.schema.json

25. planning.schema.json
26. tech-debt-investigator.schema.json
27. planning.schema.json
28. code-quality.schema.json
29. code-quality.schema.json
30. test-runner.schema.json
31. workflow.schema.json

### Research Plugin (5 schemas)
**Location**: `.claude/agents/research/schemas/`

1. researcher-lead.schema.json
2. researcher-codebase.schema.json
3. researcher-external.schema.json [consolidated from researcher-library + researcher-web]
5. repository-analyst.schema.json

### Investing Plugin (6 schemas)
**Location**: `.claude/agents/investing/schemas/`

1. market-data-specialist.schema.json
2. pattern-detector.schema.json
3. portfolio-compliance-analyzer.schema.json
4. risk-management-specialist.schema.json
5. sentiment-nlp-specialist.schema.json
6. technical-indicator-specialist.schema.json

### Shared Schemas (9 schemas)
**Location**: `.claude/docs/shared/schemas/`

1. base-agent.schema.json
2. decisions.schema.json
3. dependency-manifest.schema.json
4. failure-tracking-memory.schema.json
5. implement-orchestrator-state.schema.json
6. planning-package.schema.json
7. spec-review-output.schema.json
8. sow.schema.json
9. state-transitions.schema.json

## Total Files Moved

- **Agent-specific schemas**: 42 files (31 dev-tools + 5 research + 6 investing)
- **Shared schemas**: 9 files
- **Total**: 51 schema files

## New Directory Structure

```
.claude/
├── agents/
│   ├── dev-tools/
│   │   └── schemas/          # 31 schemas
│   ├── research/
│   │   └── schemas/          # 5 schemas
│   └── investing/
│       └── schemas/          # 6 schemas
└── docs/
    └── shared/
        └── schemas/          # 9 shared schemas
            ├── README.md
            └── MIGRATION-SUMMARY.md
```

## Old Directory Status

**`.claude/docs/schemas/`**: Empty (can be removed manually if needed)

## Schema Path Updates Required

**38 agent files** contain references to the old schema path `.claude/docs/schemas/`:

### Dev-Tools Agents (30 files)
- claude-code-ecosystem.md
- architecture.md
- architecture.md
- claude-code.md
- context-optimizer.md
- context-readiness-assessor.md
- contingency-planner.md
- debugger.md
- documentation.md
- documentation.md
- feature-analyzer.md
- git-github.md
- grafana-dashboard-builder.md
- hypothesis-former.md
- intent-analyzer.md
- deployment-release.md
- loki-query-specialist.md
- planning.md
- claude-code-ecosystem.md
- promql-query-builder.md
- development.md
- code-quality.md
- planning.md
- sast-scanner.md

- planning.md
- planning.md
- tech-debt-investigator.md
- planning.md
- code-quality.md
- test-dataset-creator.md
- code-quality.md
- workflow.md

### Research Agents (5 files)
- researcher-lead.md
- researcher-codebase.md
- researcher-external.md [consolidated from researcher-library + researcher-web]
- repository-analyst.md

### Path Update Pattern

**Old path**: `.claude/docs/schemas/{agent-name}.schema.json`

**New paths**:
- Dev-tools: `.claude/agents/dev-tools/schemas/{agent-name}.schema.json`
- Research: `.claude/agents/research/schemas/{agent-name}.schema.json`
- Investing: `.claude/agents/investing/schemas/{agent-name}.schema.json`
- Shared: `.claude/docs/shared/schemas/{schema-name}.schema.json`

## Next Steps

1. ✅ **Completed**: Schema files moved to new locations
2. ⏳ **Pending**: Update agent file references (38 files) - delegate to **documentation**
3. ⏳ **Pending**: Update export script schema paths - delegate to **workflow agent**
4. ⏳ **Pending**: Verify plugin manifests don't have hardcoded schema paths
5. ⏳ **Manual**: Remove empty `.claude/docs/schemas/` directory (requires manual deletion or rmdir command)

## Verification Commands

```bash
# Count schemas in each directory
ls .claude/agents/dev-tools/schemas/ | wc -l  # Should be 31
ls .claude/agents/research/schemas/ | wc -l   # Should be 5
ls .claude/agents/investing/schemas/ | wc -l  # Should be 6
ls .claude/docs/shared/schemas/*.json | wc -l # Should be 9

# Verify old directory is empty
ls .claude/docs/schemas/  # Should show only . and ..

# Find agent files with old schema references
grep -r "\.claude/docs/schemas/" .claude/agents/
```

## Benefits of New Organization

1. **Co-location**: Schemas live with their agents
2. **Plugin isolation**: Each plugin owns its schemas
3. **Clear ownership**: Easier to maintain and version
4. **Reduced coupling**: Plugin schemas don't pollute shared namespace
5. **Better discoverability**: Schemas in same directory as agent definitions

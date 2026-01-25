# Usage Examples

Complete workflow examples with expected output.

---

## Example 1: Single Plan Feature

### Input
```bash
/tasks docs/01-planning/features/simple-auth/
```

### Directory Structure
```
docs/01-planning/features/simple-auth/
├── SPEC.md
├── README.md
└── plans/
    └── implementation-plan.md
```

### Expected Output
```markdown
## Task Generation Complete ✅

**Feature**: simple-auth
**Plan**: implementation-plan
**Tasks Created**: 12 tasks (8 parallel, 4 sequential)
**Review Groups**: 3 review checkpoints
**Sprint Points**: 8 points

**Agent Distribution**:
- development: 6 tasks
- code-quality: 3 tasks
- code-quality: 2 tasks
- code-quality: 1 review task

**Output Files**:
- docs/01-planning/features/simple-auth/tasks/implementation-plan/tasks.md
- docs/01-planning/features/simple-auth/tasks/implementation-plan/TASKS.json

**Quality Metrics**:
- Parallel execution potential: 67%
- Review coverage: 3 groups for 12 tasks
- Task generation confidence: 0.91
- Validation score: 94% (0.89 confidence)
- Validation status: APPROVED

**Next Steps**:
1. Review generated tasks in tasks/implementation-plan/tasks.md
2. Run `/implement tasks/implementation-plan` to execute tasks
```

---

## Example 2: Multi-Plan Feature (Sequential Phases)

### Input
```bash
/tasks docs/01-planning/features/005-regenerative-orchestration-system/
```

### Directory Structure
```
docs/01-planning/features/005-regenerative-orchestration-system/
├── SPEC.md
├── RATIONALE.md
└── plans/
    ├── phase-0-operational-foundation.md
    ├── phase-1-ooda-framework.md
    ├── phase-2-agent-ecosystem.md
    └── phase-3-integration.md
```

### Expected Output
```markdown
## Task Generation Complete ✅

**Feature**: 005-regenerative-orchestration-system
**Feature Description**: Comprehensive orchestration system with OODA loop integration
**Plans Processed**: 4 plans (4 succeeded, 0 failed)

**Overall Metrics**:
- **Total Tasks**: 68 tasks
- **Parallel Tasks**: 45 (66%)
- **Sequential Tasks**: 23 (34%)
- **Review Groups**: 12 checkpoints
- **Sprint Points**: 55 points
- **Validation Score**: 91% (0.87 confidence)
- **Validation Status**: APPROVED

**Plan Breakdown**:
- **phase-0-operational-foundation**: 12 tasks, 2 reviews, 8 points [✅]
- **phase-1-ooda-framework**: 18 tasks, 3 reviews, 15 points [✅]
- **phase-2-agent-ecosystem**: 22 tasks, 4 reviews, 18 points [✅]
- **phase-3-integration**: 16 tasks, 3 reviews, 14 points [✅]

**Agent Distribution Across All Plans**:
- development: 32 tasks
- code-quality: 14 tasks
- code-quality: 10 tasks
- code-quality: 8 review tasks
- claude-code-ecosystem: 4 tasks

**Output Structure**:
tasks/
├── phase-0-operational-foundation/
│   ├── tasks.md
│   └── TASKS.json
├── phase-1-ooda-framework/
│   ├── tasks.md
│   └── TASKS.json
├── phase-2-agent-ecosystem/
│   ├── tasks.md
│   └── TASKS.json
└── phase-3-integration/
    ├── tasks.md
    └── TASKS.json

**Parallel Execution Time**: 12.3s
(Estimated sequential time: 45s - 3.7x speedup)

**Plan Structure**: sequential_phases
└─ Execute phases in dependency order (phase-0 → phase-1 → phase-2 → phase-3)

**Next Steps**:
1. Review generated tasks in tasks/
2. Start with phase-0: `/implement tasks/phase-0-operational-foundation`
3. Progress through phases in order
```

---

## Example 3: Parallel Components

### Input
```bash
/tasks docs/01-planning/features/microservices-suite/
```

### Directory Structure
```
docs/01-planning/features/microservices-suite/
├── SPEC.md
└── components/
    ├── auth-service.md
    ├── payment-service.md
    └── notification-service.md
```

### Expected Output (Plan Structure: parallel_components)
```markdown
**Plan Structure**: parallel_components
└─ Components can be executed in parallel (no cross-dependencies)

**Next Steps**:
1. Review generated tasks in tasks/
2. Run any component independently:
   - `/implement tasks/auth-service`
   - `/implement tasks/payment-service`
   - `/implement tasks/notification-service`
3. Or execute all in parallel for maximum speed
```

---

## Example 4: Partial Failure

### Input
```bash
/tasks docs/01-planning/features/mixed-quality/
```

### Expected Output
```markdown
## Task Generation Partial Success ⚠️

**Feature**: mixed-quality
**Plans Processed**: 3 plans (2 succeeded, 1 failed)

**Successful Plans**:
- **phase-0-setup**: 10 tasks, 2 reviews, 6 points [✅]
- **phase-1-core**: 15 tasks, 3 reviews, 12 points [✅]

---

## Failed Plans ❌

**phase-2-advanced**:
- **Error**: Invalid plan format - missing ## Implementation section
- **Suggestions**: 
  - Add implementation section with concrete steps
  - Ensure each step has effort estimate
  - Define clear dependencies

**Recovery Options**:
1. Fix plan file based on error messages
2. Re-run `/tasks docs/01-planning/features/mixed-quality/` to regenerate
3. Or manually create task files for failed component
```

---

## Example 5: Validation Blocking

### Input
```bash
/tasks docs/01-planning/features/needs-fixes/
```

### Expected Output
```markdown
## Task Generation Complete with Issues ⚠️

**Feature**: needs-fixes
**Tasks Created**: 25 tasks
**Validation Status**: BLOCKED

---

## Validation Summary

**Critical Issues (must fix before /implement)**:
1. ❌ Missing test tasks for payment module (security-critical)
2. ❌ Circular dependency detected: T005 → T012 → T005
3. ❌ Task T018 has no clear acceptance criteria

**High Priority Improvements**:
1. ⚠️ Consider splitting large task T003 (8 points)
2. ⚠️ Add error handling tasks for API integrations
3. ⚠️ Documentation tasks are vague

**Agent Consensus**:
- planning: 0.65 (blocked by business coverage gaps)
- architecture: 0.72 (blocked by circular dependency)
- tech-debt-investigator: 0.78 (concerned about granularity)

**Next Steps**:
1. Fix critical issues in the generated tasks
2. Re-run validation: `/tasks --validate-only`
3. Then proceed with `/implement`
```

---

## Example 6: Skip Validation (Fast Mode)

### Input
```bash
/tasks docs/01-planning/features/hotfix/ --skip-validation
```

### Expected Output
```markdown
## Task Generation Complete ✅ (Validation Skipped)

**Feature**: hotfix
**Tasks Created**: 5 tasks (3 parallel, 2 sequential)

⚠️ WARNING: Validation skipped with --skip-validation flag
Quality gates not applied. Use with caution.

**Output Files**:
- tasks/hotfix/tasks.md
- tasks/hotfix/TASKS.json

**Next Steps**:
1. Review tasks manually (validation was skipped)
2. Run `/implement tasks/hotfix` to execute
```

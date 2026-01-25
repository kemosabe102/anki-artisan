---
title: "Feature Artifact Directory Structure"
date: 2025-11-08
status: ACTIVE
tags: [claude-docs]
---
# Feature Artifact Directory Structure

## Hierarchical Organization Pattern

Each feature gets its own directory with regenerative artifact hierarchy:

```
docs/01-planning/specifications/
├── 001-user-authentication/
│   ├── SPEC.md                           # Single spec file (regenerative source)
│   ├── plans/
│   │   ├── auth-backend-plan.md         # Plan for backend components
│   │   ├── auth-frontend-plan.md        # Plan for mobile/web frontend
│   │   ├── auth-database-plan.md        # Plan for database schema
│   │   └── auth-security-plan.md        # Plan for security implementation
│   └── tasks/
│       ├── auth-backend/
│       │   ├── task-list.md             # Tasks for backend plan
│       │   ├── api-endpoints-tasks.md   # Specific API tasks
│       │   └── middleware-tasks.md      # Auth middleware tasks
│       ├── auth-frontend/
│       │   ├── task-list.md             # Tasks for frontend plan
│       │   ├── login-ui-tasks.md        # Login interface tasks
│       │   └── oauth-flow-tasks.md      # OAuth implementation tasks
│       ├── auth-database/
│       │   └── task-list.md             # Database schema tasks
│       └── auth-security/
│           └── task-list.md             # Security validation tasks
│
├── 002-payment-processing/
│   ├── SPEC.md
│   ├── plans/
│   │   ├── payment-gateway-plan.md
│   │   ├── billing-engine-plan.md
│   │   └── compliance-plan.md
│   └── tasks/
│       ├── payment-gateway/
│       │   └── task-list.md
│       ├── billing-engine/
│       │   └── task-list.md
│       └── compliance/
│           └── task-list.md
│
└── 003-reporting-dashboard/
    ├── SPEC.md
    ├── plans/
    │   ├── data-pipeline-plan.md
    │   ├── visualization-plan.md
    │   └── export-plan.md
    └── tasks/
        ├── data-pipeline/
        │   └── task-list.md
        ├── visualization/
        │   └── task-list.md
        └── export/
            └── task-list.md
```

## Strategic Integration Hierarchy

### **0. Strategic Context (Input)**

- **CEO Vision**: High-level business strategy and objectives
- **VP Roadmap**: Strategic capabilities and business outcomes (roadmap items)
- **Feature Specification**: Detailed implementation requirements (from /spec)

## Regenerative Workflow

### **1. Feature Specification (Root)**

- **File**: `docs/01-planning/specifications/XXX-[feature-name]/SPEC.md`
- **Purpose**: Single source of truth for entire feature (generated from strategic roadmap context)
- **Regeneration**: Can be updated/regenerated to refine feature requirements
- **Propagation**: Changes trigger regeneration of all plans and tasks
- **Strategic Link**: Contains roadmap reference and business outcome traceability

### **2. Implementation Plans (Sub-Components)**

- **Directory**: `docs/01-planning/specifications/XXX-[feature-name]/plans/`
- **Pattern**: `[component-name]-plan.md`
- **Purpose**: Technical implementation details for each major component
- **Regeneration**: Individual plans can be regenerated from updated spec
- **Examples**:
  - `auth-backend-plan.md` - API, middleware, business logic
  - `auth-frontend-plan.md` - UI components, user flows
  - `auth-database-plan.md` - Schema, migrations, indexes
  - `auth-security-plan.md` - Security validation, compliance

### **3. Executable Tasks (Implementation Units)**

- **Directory**: `docs/01-planning/specifications/XXX-[feature-name]/tasks/[component-name]/`
- **Pattern**: `task-list.md` plus specific task files
- **Purpose**: Granular, executable work items with SoW blocks
- **Regeneration**: Tasks regenerated when parent plan changes
- **Organization**: Grouped by component for clear ownership

## Change Propagation Rules

### **Spec → Plans → Tasks Cascade**

1. **SPEC.md changes** → Regenerate affected plans → Regenerate affected tasks
2. **Plan changes** → Regenerate only tasks for that component
3. **Task changes** → No upstream propagation (implementation details)

### **Selective Regeneration**

- **Full Feature**: Regenerate SPEC → all plans → all tasks
- **Component Update**: Regenerate specific plan → related tasks only
- **Implementation Refinement**: Update tasks without touching plans/spec

## Artifact Naming Convention

### **Feature Numbering**

- **Pattern**: `XXX-[kebab-case-name]`
- **Examples**: `001-user-authentication`, `002-payment-processing`
- **Auto-increment**: Planner scans existing features to determine next number

### **Plan Naming**

- **Pattern**: `[component-name]-plan.md`
- **Guidelines**: Clear component boundaries, logical grouping
- **Examples**: `backend-plan.md`, `frontend-plan.md`, `database-plan.md`

### **Task Directory Naming**

- **Pattern**: `[component-name]/` (matches plan name without `-plan.md`)
- **Examples**: `backend/`, `frontend/`, `database/`
- **Files**: `task-list.md` plus specific task breakdowns

## Planner Agent Integration

### **Automatic Directory Creation**

When planner creates artifacts, it should:

1. **Scan existing features** to determine next feature number
2. **Create feature directory** with proper numbering
3. **Generate component plans** based on spec complexity
4. **Create task directories** matching plan components
5. **Maintain consistent naming** across all artifacts

### **Regeneration Support**

- **Detect existing structure** before regenerating
- **Preserve manual modifications** in designated sections
- **Update provenance tracking** for change traceability
- **Validate cross-references** between spec, plans, and tasks

## Example Feature: User Authentication

### **Initial Creation**

```bash
# Planner creates:
docs/01-planning/specifications/001-user-authentication/
├── SPEC.md                    # Complete feature specification
├── plans/
│   ├── auth-backend-plan.md   # API, business logic, middleware
│   ├── auth-frontend-plan.md  # Mobile app, web interface
│   └── auth-security-plan.md  # OAuth, encryption, compliance
└── tasks/
    ├── auth-backend/
    │   └── task-list.md       # Backend implementation tasks
    ├── auth-frontend/
    │   └── task-list.md       # Frontend implementation tasks
    └── auth-security/
        └── task-list.md       # Security implementation tasks
```

### **Feature Evolution**

```bash
# After spec update, planner regenerates affected artifacts:
# 1. SPEC.md updated with new requirements
# 2. auth-backend-plan.md regenerated (new API endpoints)
# 3. auth-backend/task-list.md regenerated (new tasks)
# 4. Other plans/tasks unchanged (not affected by spec change)
```

This structure supports true regenerative development where changes cascade appropriately while preserving work that doesn't need to change.

## Legacy Document Locations

**Note**: Documents created before adopting SDD (Specification-Driven Development) are located in:

- **Legacy Feature Plans**: `docs/feature-plans/` - Contains pre-SDD feature documents
- **Legacy Project Plans**: `docs/00-project/plans/` - Contains historical project planning documents

These legacy documents remain for reference but new regenerative development should use the `docs/01-planning/specifications/` structure.

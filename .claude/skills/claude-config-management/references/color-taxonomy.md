# Agent Color Taxonomy

Complete reference for agent color assignments and their semantic meanings.

---

## Color Philosophy

Colors in Claude Code serve three purposes:
1. **Visual Identification**: Quickly distinguish agent types in UI
2. **Domain Grouping**: Related agents share colors
3. **Semantic Communication**: Color meaning conveys agent purpose

---

## Color Definitions

### Green - Creation & Implementation

**Semantic**: Growth, creation, building, implementation
**Hex**: Typically `#22c55e` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| development | Creates and implements code |
| code-quality | Builds quality into code |
| architecture | Designs and creates architecture |
| claude-code-ecosystem | Creates agent definitions |

**When to Use**: Agents that primarily CREATE or BUILD artifacts

---

### Blue - Planning & Strategy

**Semantic**: Strategy, analysis, planning, organization
**Hex**: Typically `#3b82f6` or similar


**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| planning | Plans features, specs, tasks |
| research | Researches and analyzes information |

**When to Use**: Agents that primarily PLAN or ANALYZE before action

---

### Orange - Configuration & Automation

**Semantic**: Configuration, workflow, automation, settings
**Hex**: Typically `#f97316` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| workflow | Manages Claude Code ecosystem configuration |

**When to Use**: Agents that manage CONFIGURATION or AUTOMATION

---

### Purple - Infrastructure & Operations

**Semantic**: Infrastructure, monitoring, deployment, operations
**Hex**: Typically `#a855f7` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| observability | Monitors and alerts on systems |
| deployment-release | Deploys and releases code |
| platform-infrastructure | Manages platform resources |

**When to Use**: Agents that manage INFRASTRUCTURE or OPERATIONS


---

### Yellow - Assessment & Warning

**Semantic**: Assessment, attention, warning, evaluation
**Hex**: Typically `#eab308` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| context-readiness-assessor | Assesses context quality (needs attention) |
| contingency-planner | Identifies risks (warning) |

**When to Use**: Agents that ASSESS or WARN about conditions

---

### Cyan - Support & Optimization

**Semantic**: Support, utility, optimization, helper
**Hex**: Typically `#06b6d4` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| intent-analyzer | Supports request decomposition |
| context-optimizer | Optimizes context usage |

**When to Use**: Agents that SUPPORT or OPTIMIZE other processes

---

### Red - Security & Critical

**Semantic**: Security, critical, danger, high-priority
**Hex**: Typically `#ef4444` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| sast-scanner | Security scanning (critical domain) |

**When to Use**: Agents dealing with SECURITY or CRITICAL operations


---

### Gray - Specialists & Neutral

**Semantic**: Neutral, specialized, domain-specific
**Hex**: Typically `#6b7280` or similar

**Assigned To**:
| Agent | Rationale |
|-------|-----------|
| source-control | Specialized tool (neutral) |
| tech-debt-investigator | Specialized analysis |
| ttrpg-campaign-architect | Specialized domain |
| Various specialists | Domain-specific tasks |

**When to Use**: Specialized agents without strong domain affinity

---

## Color Assignment Decision Tree

```
Is agent SECURITY-related?
├─ YES → Red
└─ NO → Does agent CREATE/BUILD artifacts?
         ├─ YES → Green
         └─ NO → Does agent PLAN/ANALYZE?
                  ├─ YES → Blue
                  └─ NO → Does agent manage INFRASTRUCTURE?
                           ├─ YES → Purple
                           └─ NO → Does agent CONFIGURE/AUTOMATE?
                                    ├─ YES → Orange
                                    └─ NO → Does agent ASSESS/WARN?
                                             ├─ YES → Yellow
                                             └─ NO → Does agent SUPPORT/OPTIMIZE?
                                                      ├─ YES → Cyan
                                                      └─ NO → Gray (default)
```


---

## Color Conflict Resolution

### Same Domain, Different Functions

If two agents in same domain have different functions:
1. Primary function agent keeps domain color
2. Secondary function agent uses function-appropriate color

Example: Both `development` and `debugger` are coding domain
- `development` (creation focus) → Green
- `debugger` (investigation focus) → Could be Yellow (assessment)

### Cross-Domain Agents

For agents spanning multiple domains:
1. Identify PRIMARY function
2. Assign color based on primary function
3. Document secondary domains in description

---

## Proposing New Colors

### Criteria for New Color

New color justified when:
- [ ] Genuinely new domain category emerges
- [ ] No existing color semantically fits
- [ ] 3+ agents would share the new color
- [ ] Sufficient visual contrast with existing colors

### Proposal Process

1. Document proposed color and semantic meaning
2. List agents that would use it
3. Show contrast with existing palette
4. Get team consensus before implementation

---

## Current Palette Summary

| Color | Count | Primary Domain |
|-------|-------|----------------|
| Green | 4 | Coding/Creation |
| Blue | 2 | Planning |
| Orange | 1 | Workflow |
| Purple | 3 | Infrastructure |
| Yellow | 2 | Analysis |
| Cyan | 2 | Utility |
| Red | 1 | Security |
| Gray | 4+ | Specialists |


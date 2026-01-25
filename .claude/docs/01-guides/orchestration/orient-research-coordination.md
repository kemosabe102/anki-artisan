---
title: "ORIENT Research Coordination - CQ Consolidation & Conflict Resolution"
date: 2025-11-24
status: ACTIVE
version: 1.0.0
tags: [orchestration, ooda, context-quality, research-coordination, consensus]
---

# ORIENT Research Coordination - CQ Consolidation & Conflict Resolution

**Purpose**: Complete consolidation algorithm for multi-agent ORIENT outputs, conflict resolution, and iteration management.

**Auto-loaded**: Referenced from CLAUDE.md lines 255-318

**Integration**: Discovery Pattern → Phase 2 (Consolidate CQ Scores) → This document

---

## Quick Reference

### When to Use
- Discovery Pattern spawns 2+ agents during ORIENT phase
- Agents return different CQ scores (need single consolidated value for gate decision)
- Conflict detection needed (check if agents fundamentally disagree)

### Primary Method
**Weighted Averaging**: CQ = (w_cra × CQ_cra) + (w_specialists × CQ_specialists_avg) + (w_lead × CQ_lead)

Weights: CRA=0.50, Specialists=0.35, Lead=0.15

### Alternative Methods
- **Minimum** (pessimistic, security-critical)
- **Median** (outlier-robust, 5+ agents)
- **Confidence-Weighted** (when agents provide explicit confidence scores)

### Output
- Consolidated CQ score (0.0-1.0)
- Consensus classification (Strong/Moderate/Weak/Conflict)
- Iteration recommendation (PROCEED/ITERATE/ESCALATE)

---

## CQ Consolidation Algorithm

### Weights

```
context-readiness-assessor: 0.50 (authoritative)
domain specialists avg:     0.35 (collective expertise)
researcher-lead:            0.15 (external validation)
```

### Calculation

```python
def consolidate_cq(agent_scores: dict[str, float]) -> float:
    """
    Consolidate CQ scores from multiple agents.
    
    Args:
        agent_scores: Dict mapping agent name to CQ score (0.0-1.0)
    
    Returns:
        Consolidated CQ score (0.0-1.0)
    """
    cra_score = agent_scores.get('context-readiness-assessor', 0.0)
    
    domain_agents = [s for k, s in agent_scores.items() 
                    if k not in ('context-readiness-assessor', 'researcher-lead')]
    domain_avg = sum(domain_agents) / len(domain_agents) if domain_agents else 0.0
    
    rl_score = agent_scores.get('researcher-lead', 0.0)
    
    return (cra_score * 0.50) + (domain_avg * 0.35) + (rl_score * 0.15)
```

### Conflict Detection

- **Strong Consensus**: All scores within +/- 0.10 of mean
- **Weak Consensus**: Scores within +/- 0.20 of mean
- **Conflict**: Any score differs by > 0.30 from mean → ESCALATE

### Edge Cases

| Scenario | Handling |
|----------|----------|
| Single agent | Use agent score directly (no consolidation) |
| 2 agents tie | Use minimum score (conservative) |
| 5+ agents | Use median instead of average for domain specialists |
| CRA missing | Double domain specialists weight to 0.70 |

### Iteration Rules

1. If consolidated CQ < 0.85: spawn additional research agents
2. Max 3 iterations before forced proceed with ADVISORY
3. Each iteration must improve CQ by >= 0.05 or terminate

---

See CLAUDE.md lines 255-318 for additional consolidation methods and examples.

**Version History**:
- v1.0.0 (2025-11-24): Initial documentation extracted from CLAUDE.md


# Phase 1: OBSERVE - Request Analysis & Knowledge Loading

**OODA Stage**: OBSERVE | **Time Allocation**: 15-20%

**Purpose**: Parse request, detect operation category, load tiered knowledge base, establish confidence baseline

**Deliverable**: Category classification, loaded knowledge, initial confidence assessment

---

## Pre-Flight Checklist

Before ANY operation:

- [ ] Request parsed for intent signals
- [ ] Category detected (CREATE/ANALYZE/UPDATE/VALIDATE/DESIGN)
- [ ] Tier 1 knowledge loaded (always required)
- [ ] Tier 2 knowledge loaded (category-specific)
- [ ] Initial confidence score calculated

---

## Workflow Steps

### Step 1.1: Request Parsing & Category Detection

**Input**: User request text

**Process**:
1. Extract key verbs and entities from request
2. Match intent signals to category:

| Category | Intent Signals | Start Action |
|----------|----------------|--------------|
| **CREATE** | "create", "new", "build", "make", agent idea descriptions | Analyze idea, bootstrap directory |
| **ANALYZE** | "analyze", "evaluate", "assess", "quality", "review" | Load agent, prepare matrix |
| **UPDATE** | "update", "change", "improve", "fix", "implement feedback" | Identify scope, read current state |
| **VALIDATE** | "validate", "check", "verify", "is this correct" | Run validation checks |
| **DESIGN** | "design guide", "document pattern", "create guide" | Analyze patterns |

3. Record category and confidence (0.0-1.0)

**Output**: `{ category: string, confidence: float, intent_signals: string[] }`

### Step 1.2: Tier 1 Knowledge Loading (ALWAYS)

**Input**: Any request

**Process**:
1. Load `agent.template.md` - Structural standard
2. Load `base-agent-pattern.md` - Inheritance source
3. Load `agent-color-taxonomy.md` - Color assignment rules

**Output**: Core knowledge base established

### Step 1.3: Tier 2 Knowledge Loading (Category-Specific)

**Input**: Detected category from Step 1.1

**Process**:
| Category | Load These Resources |
|----------|---------------------|
| CREATE | `agent-scaffold/`, `infuse-framework-quick-ref.md`, `creating-ai-readable-documentation-framework.md` |
| ANALYZE | `agent-quality-taxonomy.md`, `description-delegation-checklist.md`, `docs/frameworks.md` |
| UPDATE | Target agent's `docs/` directory |
| VALIDATE | Frontmatter spec from `domain-expertise.md` |
| DESIGN | `00-core/frameworks/README.md` |

**Output**: Category-specific knowledge loaded


### Step 1.4: Confidence Assessment

**Input**: Loaded knowledge, request clarity

**Process**:
1. Assess request clarity (0.0-1.0)
2. Verify knowledge availability (0.0-1.0)
3. Check for ambiguities requiring clarification
4. Calculate initial CQ: `clarity * 0.5 + knowledge_available * 0.5`

**Output**: Initial confidence score with gap identification

---

## Exit Criteria

**CQ >= 0.70 required to proceed to ORIENT**

| Criterion | Weight | Check |
|-----------|--------|-------|
| Category identified | 0.30 | Single category with confidence >= 0.7 |
| Tier 1 loaded | 0.25 | All 3 core docs accessible |
| Tier 2 loaded | 0.25 | Category-specific resources loaded |
| Request clarity | 0.20 | No blocking ambiguities |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping Tier 1 loading | ALWAYS load template, base-pattern, color-taxonomy |
| Wrong category detection | Re-read request, identify dominant intent signal |
| Proceeding with ambiguity | Ask clarifying questions before ORIENT |
| Loading Tier 3 prematurely | Only load if confidence < 0.7 after Tier 2 |

---

## Reference Documentation

- `agent.template.md` - Structural standard
- `base-agent-pattern.md` - Inheritance source
- `agent-color-taxonomy.md` - Color assignment

---

**Next Phase**: [Phase 2: ORIENT](phase-2-orient.md)

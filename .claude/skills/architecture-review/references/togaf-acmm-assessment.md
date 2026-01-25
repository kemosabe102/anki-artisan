# TOGAF Architecture Capability Maturity Model (ACMM) Assessment

> Evaluate organizational architecture maturity across 9 domains on a 0-5 scale.

---

## Maturity Levels

### Level 0 - None

- No architecture practice exists
- Ad-hoc, reactive decision making
- No documentation or governance

### Level 1 - Initial

- Architecture efforts are informal and uncoordinated
- Individual initiatives without organizational support
- Minimal documentation, no standards

### Level 2 - Under Development

- Architecture practice is emerging
- Some processes defined but inconsistently applied
- Basic documentation exists
- **Stage Mapping**: MVP minimum

### Level 3 - Defined

- Formal architecture practice established
- Documented processes consistently followed
- Standards and guidelines in place
- Architecture governance operational
- **Stage Mapping**: Alpha minimum


### Level 4 - Managed

- Architecture practice is measured and controlled
- Metrics track effectiveness and compliance
- Continuous improvement based on data
- Cross-functional integration achieved
- **Stage Mapping**: RC minimum

### Level 5 - Optimizing

- Architecture practice drives business innovation
- Proactive optimization and adaptation
- Industry leadership in architecture practices
- Full organizational alignment
- **Stage Mapping**: GA target

---

## 9 Assessment Domains

### 1. Architecture Process

| Level | Characteristics |
|-------|-----------------|
| 1 | No defined process |
| 2 | Basic process documented |
| 3 | Process followed consistently |
| 4 | Process measured and optimized |
| 5 | Process enables innovation |

**Assessment Questions**:
- Is there a documented architecture development methodology?
- Are architecture artifacts produced consistently?
- Is the process integrated with development lifecycle?


### 2. Architecture Development

| Level | Characteristics |
|-------|-----------------|
| 1 | No formal development approach |
| 2 | Basic patterns and standards emerging |
| 3 | Comprehensive standards applied |
| 4 | Development measured for quality |
| 5 | Leading-edge practices adopted |

**Assessment Questions**:
- Are architecture patterns documented and reused?
- Is there a reference architecture?
- Are ADRs (Architecture Decision Records) maintained?

### 3. Business Linkage

| Level | Characteristics |
|-------|-----------------|
| 1 | No connection to business strategy |
| 2 | Informal business input |
| 3 | Formal business requirements integration |
| 4 | Architecture drives business capabilities |
| 5 | Architecture enables business transformation |

**Assessment Questions**:
- How are business requirements translated to architecture?
- Is there traceability from business goals to technical decisions?
- Does architecture planning align with business planning cycles?


### 4. Architecture Governance

| Level | Characteristics |
|-------|-----------------|
| 1 | No governance structure |
| 2 | Basic review processes |
| 3 | Formal governance board operational |
| 4 | Governance metrics tracked |
| 5 | Governance drives organizational agility |

**Assessment Questions**:
- Is there an Architecture Review Board (ARB)?
- Are architecture decisions formally approved?
- Is compliance monitored and enforced?

### 5. IT Investment & Acquisition

| Level | Characteristics |
|-------|-----------------|
| 1 | No architecture input to investments |
| 2 | Architecture consulted occasionally |
| 3 | Architecture approval required |
| 4 | Investment decisions architecture-driven |
| 5 | Portfolio optimization via architecture |

**Assessment Questions**:
- Does architecture influence technology selection?
- Is there a technology radar or standards list?
- Are investments evaluated against architecture principles?


### 6. Architecture Communication

| Level | Characteristics |
|-------|-----------------|
| 1 | No communication of architecture |
| 2 | Ad-hoc communication |
| 3 | Regular stakeholder communication |
| 4 | Multi-channel communication strategy |
| 5 | Architecture understanding organization-wide |

**Assessment Questions**:
- How is architecture communicated to stakeholders?
- Are architecture artifacts accessible?
- Is there architecture training/onboarding?

### 7. Security Architecture

| Level | Characteristics |
|-------|-----------------|
| 1 | Security not integrated |
| 2 | Basic security considerations |
| 3 | Security architecture defined |
| 4 | Security measured and audited |
| 5 | Security enables business innovation |

**Assessment Questions**:
- Is there a security architecture practice?
- Are threat models maintained?
- Is security integrated into architecture reviews?


### 8. Senior Management Involvement

| Level | Characteristics |
|-------|-----------------|
| 1 | No executive sponsorship |
| 2 | Occasional executive interest |
| 3 | Executive sponsor assigned |
| 4 | Active executive participation |
| 5 | Architecture is executive priority |

**Assessment Questions**:
- Is there executive sponsorship for architecture?
- Do executives participate in ARB decisions?
- Is architecture part of strategic planning?

### 9. Operating Unit Participation

| Level | Characteristics |
|-------|-----------------|
| 1 | No unit participation |
| 2 | Passive compliance |
| 3 | Active participation in reviews |
| 4 | Units contribute to architecture |
| 5 | Federated architecture ownership |

**Assessment Questions**:
- Do operating units participate in architecture development?
- Is there federated architecture governance?
- Do units have architecture representatives?

---


## Scoring Method

### Per-Domain Scoring

1. Evaluate each domain against level criteria (1-5)
2. Document evidence for each score
3. Note confidence level (HIGH/MEDIUM/LOW)

### Aggregate Scoring

```
ACMM_Score = Sum(Domain_Scores) / 9
```

### Weighted Scoring (Optional)

For project-specific emphasis:

| Domain | Default Weight | Security Focus | Governance Focus |
|--------|---------------|----------------|------------------|
| Process | 0.12 | 0.10 | 0.10 |
| Development | 0.12 | 0.10 | 0.10 |
| Business Linkage | 0.12 | 0.10 | 0.15 |
| Governance | 0.12 | 0.10 | 0.20 |
| IT Investment | 0.10 | 0.10 | 0.10 |
| Communication | 0.10 | 0.10 | 0.10 |
| Security | 0.12 | 0.25 | 0.10 |
| Senior Management | 0.10 | 0.05 | 0.10 |
| Operating Unit | 0.10 | 0.10 | 0.05 |

---

## Stage Mapping

| Stage | Minimum Level | Required Domains at Level | Focus Areas |
|-------|---------------|---------------------------|-------------|
| MVP | L2 | Process, Development | Basic structure |
| Alpha | L3 | All core 5 | Formal practices |
| Beta | L3-4 | All 9 domains | Measurement |
| RC | L4 | All 9 domains | Optimization |
| GA | L5 | All 9 domains | Excellence |


---

## Assessment Template

```markdown
## TOGAF ACMM Assessment

**Project**: [name]
**Date**: [date]
**Assessor**: [name]
**Target Stage**: [MVP/Alpha/Beta/RC/GA]

### Domain Scores

| Domain | Score | Confidence | Evidence |
|--------|-------|------------|----------|
| Architecture Process | X/5 | HIGH/MED/LOW | [notes] |
| Architecture Development | X/5 | HIGH/MED/LOW | [notes] |
| Business Linkage | X/5 | HIGH/MED/LOW | [notes] |
| Architecture Governance | X/5 | HIGH/MED/LOW | [notes] |
| IT Investment | X/5 | HIGH/MED/LOW | [notes] |
| Communication | X/5 | HIGH/MED/LOW | [notes] |
| Security | X/5 | HIGH/MED/LOW | [notes] |
| Senior Management | X/5 | HIGH/MED/LOW | [notes] |
| Operating Unit | X/5 | HIGH/MED/LOW | [notes] |

### Aggregate Score: X.X/5

### Stage Readiness: [PASS/WARN/FAIL]

### Recommendations
1. [priority 1]
2. [priority 2]
3. [priority 3]
```

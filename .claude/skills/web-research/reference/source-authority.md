# Source Authority - Web Research Skill

**Version**: 1.0.0 | **Last Updated**: 2025-12-13

---

## Overview

This document defines domain scoring tiers, credibility assessment criteria, and validation requirements for web research sources.

---

## Domain Scoring Tiers

### Tier 1: Official Documentation (Authority Score: 0.90-1.00)

**Characteristics:**
- Primary vendor/project documentation
- Language/framework official sites (python.org, kubernetes.io)
- Standards bodies (W3C, IETF, ISO)
- Government/regulatory sources (.gov, .edu)

**Examples:**
- `https://docs.python.org/` (Python official)
- `https://kubernetes.io/docs/` (K8s official)
- `https://fastapi.tiangolo.com/` (FastAPI official)
- `https://www.postgresql.org/docs/` (PostgreSQL official)

**Trust Level:** Accept without secondary validation (unless contradicted)

---

### Tier 2: Vendor/Academic (Authority Score: 0.70-0.89)

**Characteristics:**
- Vendor engineering blogs (high-quality, technical depth)
- Academic papers (peer-reviewed)
- Reputable tech publishers (O'Reilly, Manning)
- Cloud provider docs (AWS, GCP, Azure)

**Examples:**
- `https://aws.amazon.com/blogs/` (AWS Blog)
- `https://martinfowler.com/` (Martin Fowler)
- `https://arxiv.org/` (Academic preprints)
- `https://www.timescale.com/blog/` (Timescale Blog)

**Trust Level:** Validate claims with Tier 1 source or second Tier 2 source

---

### Tier 3: Community/Expert (Authority Score: 0.50-0.69)

**Characteristics:**
- High-reputation Stack Overflow answers (>100 upvotes)
- Well-maintained GitHub repos (>1k stars)
- Recognized expert blogs (verified track record)
- Technical news sites (Hacker News, Reddit r/programming with high engagement)

**Examples:**
- `https://stackoverflow.com/` (accepted answers with high votes)
- `https://github.com/` (popular, actively maintained repos)
- `https://realpython.com/` (Community tutorial site)

**Trust Level:** Require 2+ sources from Tier 2/3, or 1 Tier 1 confirmation

---

### Tier 4: Unverified (Authority Score: 0.30-0.49)

**Characteristics:**
- Personal blogs (no verified expertise)
- Forums without voting systems
- Outdated content (>3 years for tools, >5 years for concepts)
- Anonymous sources

**Trust Level:** Use only as hypothesis source, NEVER as sole evidence

---

### Tier 5: Unreliable (Authority Score: <0.30)

**Characteristics:**
- Content farms, SEO spam sites
- Unattributed copy-paste articles
- Paywalled without academic affiliation
- Contradicts Tier 1/2 sources without evidence

**Trust Level:** DISCARD, do not cite

---

## Credibility Assessment Criteria

### Primary Indicators (70% weight)

| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| **Author Expertise** | 25% | Verifiable credentials, track record, community recognition |
| **Source Tier** | 25% | Official > Academic > Vendor > Community > Personal |
| **Recency** | 20% | Within relevance window (see Recency Requirements below) |

### Secondary Indicators (30% weight)

| Criterion | Weight | Evaluation |
|-----------|--------|------------|
| **Citations/References** | 10% | Links to Tier 1/2 sources, not circular references |
| **Depth** | 10% | Code examples, benchmarks, technical detail vs surface-level |
| **Consensus** | 10% | Aligns with multiple independent sources |

---

## When to Require Multiple Sources

### Single Source Sufficient (Tier 1 only)
- Official documentation for API usage
- Language/framework feature specifications
- Standards definitions

### Two Sources Required
- Best practices (1 Tier 1 + 1 Tier 2, OR 2 Tier 2)
- Performance benchmarks (prefer independent validation)
- Security recommendations

### Three+ Sources Required
- Controversial claims (emerging tech, debated practices)
- Comparative analysis (X vs Y)
- State-of-the-art surveys
- Critical production decisions

---

## Recency Requirements by Topic Type

| Topic Type | Max Age | Rationale |
|------------|---------|-----------|
| **Language Features** | 1 year | Rapid release cycles (Python, JS) |
| **Cloud Services** | 6 months | Frequent API changes |
| **Security Practices** | 1 year | Evolving threat landscape |
| **Frameworks/Libraries** | 1 year | Active development, deprecations |
| **Algorithms/CS Theory** | 5 years | Timeless knowledge, slower evolution |
| **Architecture Patterns** | 3 years | Principles stable, implementations evolve |

**Exception:** Seminal papers/books (e.g., "Design Patterns" GoF) remain valid despite age.

---

## Source Validation Checklist

Before citing a source, verify:

- [ ] Domain tier identified (1-5)
- [ ] Publication/update date within recency window
- [ ] Author credentials checked (if Tier 3-4)
- [ ] Cross-referenced with Tier 1/2 source (if Tier 3-4)
- [ ] No contradictions with higher-tier sources
- [ ] URL saved for citation (`findings-template.md`)

---

## Red Flags (Disqualify Source)

- **No author attribution** (anonymous content farms)
- **Contradicts official docs** without evidence/rationale
- **Outdated examples** (Python 2.x in 2024, deprecated APIs)
- **Broken code examples** (untested, non-functional snippets)
- **Clickbait titles** ("This ONE TRICK for Kubernetes...")
- **Paywall without academic access** (use alternative sources)

---

## Authority Score Calculation

```
Authority Score = (Tier Base Score) × (Recency Multiplier) × (Expertise Multiplier)

Tier Base Scores:
  Tier 1: 1.00
  Tier 2: 0.80
  Tier 3: 0.60
  Tier 4: 0.40
  Tier 5: 0.20

Recency Multiplier (based on topic type):
  Within window: 1.0
  1-2x window: 0.8
  >2x window: 0.5

Expertise Multiplier:
  Verified expert: 1.0
  Community recognized: 0.9
  Unknown/anonymous: 0.7
```

**Example:**
- Source: Timescale Blog post on compression (Tier 2)
- Age: 6 months (Cloud Services = within 6mo window)
- Author: Timescale engineer (verified expert)
- Score: 0.80 × 1.0 × 1.0 = **0.80** (High Authority)

---

## Related Documents

- `tool-patterns.md` - Query optimization and tool selection
- `findings-template.md` - Output format with authority scoring
- `.claude/docs/00-core/research-patterns.md` - Research methodology

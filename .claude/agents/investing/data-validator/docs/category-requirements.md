# Category Requirements - 5-Category Coverage Rules

## Overview

The data-validator checks that daily news collection covers all 5 risk categories. Missing categories indicate collection pipeline gaps.

## The 5 Risk Categories

### 1. Geopolitical

**Scope**: International conflicts, sanctions, elections, diplomatic relations

**Examples**:
- US-China trade tensions
- Middle East conflicts
- European Union policy changes
- Sanctions announcements
- Election outcomes with market impact

**Sources to Check**:
- Reuters, AP for breaking news
- State Department, foreign ministry releases
- Defense/intelligence analysis

---

### 2. Health

**Scope**: Pandemics, disease outbreaks, healthcare policy, FDA actions

**Examples**:
- COVID-19 variant developments
- Disease outbreak reports (WHO, CDC)
- Major drug approvals/rejections
- Healthcare legislation

**Sources to Check**:
- WHO, CDC official releases
- Medical journals (Lancet, NEJM)
- FDA announcements

---

### 3. Regulatory

**Scope**: Financial regulations, antitrust actions, compliance requirements

**Examples**:
- SEC enforcement actions
- Antitrust investigations (DOJ, FTC)
- Banking regulation changes
- Crypto/fintech regulatory guidance
- International regulatory coordination

**Sources to Check**:
- SEC, CFTC, OCC releases
- Federal Register
- International regulators (FCA, ECB)

---

### 4. Macro

**Scope**: Central bank policy, economic indicators, fiscal policy

**Examples**:
- Federal Reserve rate decisions
- Employment reports (NFP, jobless claims)
- GDP releases
- Inflation data (CPI, PPI)
- Treasury policy announcements

**Sources to Check**:
- Federal Reserve, ECB, BOJ releases
- BLS, BEA economic data
- Treasury announcements

---

### 5. Tech

**Scope**: Cybersecurity, AI policy, tech sector disruption, platform changes

**Examples**:
- Major cybersecurity incidents
- AI regulation proposals
- Big tech antitrust outcomes
- Platform policy changes (app stores)
- Semiconductor supply chain issues

**Sources to Check**:
- CISA advisories
- Tech news (Wired, Ars Technica)
- Company announcements

---

## Coverage Validation Logic

```sql
SELECT DISTINCT category FROM attention_daily WHERE date = :audit_date;
```

**Expected Result**: All 5 categories present
**Gap Detection**: List missing categories in output

## Recommendations by Missing Category

| Missing Category | Recommendation |
|-----------------|----------------|
| geopolitical | Add Reuters/AP international feeds |
| health | Add WHO/CDC monitoring sources |
| regulatory | Add SEC/Federal Register feeds |
| macro | Add Fed/BLS data sources |
| tech | Add CISA/tech news monitoring |

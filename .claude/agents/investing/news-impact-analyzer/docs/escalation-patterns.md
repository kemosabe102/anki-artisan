# Escalation Patterns

## Overview

Escalation classification determines whether a risk event is intensifying, stabilizing, or resolving. This affects impact predictions through the escalation_adjustment factor.

## Classification Categories

### New (adjustment: 1.0)

First occurrence of this event type with no prior history:
- No matching event_id in escalation_history
- No similar category+severity events in past 30 days
- Treated as baseline with no trajectory adjustment

### Escalating (adjustment: +20%)

Event severity or scope increasing:
- Current severity > previous severity by >= 10 points
- Geographic scope expanding
- Additional sectors affected
- Diplomatic/military escalation confirmed

**Detection Query**:
```sql
SELECT 
    severity - LAG(severity) OVER (ORDER BY recorded_at) as severity_delta
FROM escalation_history
WHERE event_id = $event_id
ORDER BY recorded_at DESC
LIMIT 5;
-- If avg(severity_delta) > 5, classify as escalating
```

### Stable (adjustment: 1.0)

Event maintaining current intensity:
- Severity delta within +-5 points
- No scope changes
- Media coverage consistent


### De-escalating (adjustment: -15%)

Event severity or scope decreasing:
- Current severity < previous severity by >= 10 points
- Diplomatic progress announced
- Containment confirmed
- Market already pricing in resolution

## Narrative Phases (Multi-Week Events)

Complex events follow predictable phases:

| Phase | Duration | Market Response | Typical Adjustment |
|-------|----------|-----------------|-------------------|
| Shock | Days 1-3 | Sharp reaction, volatility spike | +30% impact |
| Digestion | Week 1-2 | Assessment, positioning | +10% impact |
| Resolution | Week 3+ | Recovery or new normal | -20% to +20% |

## Escalation History Schema

```sql
CREATE TABLE escalation_history (
    id SERIAL PRIMARY KEY,
    event_id TEXT NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL,
    severity INT CHECK (severity BETWEEN 0 AND 100),
    scope TEXT,  -- 'regional', 'multi-regional', 'global'
    phase TEXT,  -- 'shock', 'digestion', 'resolution'
    sectors_affected TEXT[],
    notes TEXT
);
```

## Edge Cases

- **Flash events**: Single-day severity spike > 80, no prior history = new + shock phase
- **Recurring events**: Same event_id with >30 day gap = treat as new instance
- **Conflicting signals**: Severity up but scope down = weight severity 70%

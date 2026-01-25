# Delegation Examples

**Purpose**: Show how orchestrator invokes doc-reference-optimizer for various scenarios.

---

## Basic Agent Optimization

**Scenario**: Full analysis of single agent for all optimization opportunities.

```markdown
Task(doc-reference-optimizer, 
  "Analyze researcher-codebase agent for documentation reference opportunities. 
   Calculate token savings and generate optimization report.")
```

**Expected Output**: Complete analysis with all sections evaluated, optimization opportunities ranked by value score, documentation gaps identified.

---

## Specific Section Focus

**Scenario**: Target only specific sections for analysis (faster, focused).

```markdown
Task(doc-reference-optimizer, 
  "Analyze python-code-reviewer agent, focusing on 'Knowledge Base' and 
   'Workflow Operations' sections only.")
```

**Expected Output**: Analysis limited to specified sections, faster execution, targeted recommendations.


---

## Quick Token Efficiency Check

**Scenario**: Fast scan to identify top optimization opportunities only.

```markdown
Task(doc-reference-optimizer, 
  "Quick token efficiency scan of debugger agent. 
   Identify top 3 optimization opportunities.")
```

**Expected Output**: Abbreviated analysis, top opportunities only, faster execution time.

---

## Agent Analysis Suite Integration

**Scenario**: Part of multi-agent analysis workflow (see `agent-analysis-suite-protocol.md`).

```markdown
# Launched in parallel with other suite agents:
Task(doc-reference-optimizer, "Analyze {agent-name} for token efficiency opportunities")
Task(prompt-evaluator, "Evaluate {agent-name} prompt quality")
Task(agent-architect, "Assess {agent-name} structure compliance")
Task(tech-debt-investigator, "Check {agent-name} documentation debt")
```

**Expected Output**: Contributes token efficiency analysis to 360-degree agent assessment.

---

## Sample Output Structure

```json
{
  "status": "SUCCESS",
  "agent": "doc-reference-optimizer",
  "confidence": 0.87,
  "agent_specific_output": {
    "analysis_summary": {
      "agent_analyzed": "researcher-codebase",
      "current_token_count": 3500,
      "optimized_token_count": 2200,
      "potential_savings": 1300,
      "compression_ratio": "37% reduction"
    },
    "optimization_opportunities": [
      {
        "section": "Knowledge Base Integration",
        "optimization_strategy": "reference_existing",
        "savings": 450,
        "confidence": 0.92
      }
    ]
  }
}
```

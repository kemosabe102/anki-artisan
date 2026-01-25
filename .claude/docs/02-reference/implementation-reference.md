# Implementation Reference: Orchestrator Synthesis Workflow

**Purpose**: Detailed pseudo-code implementation for orchestrator synthesis workflow

**Audience**: Developers implementing synthesis logic in orchestrator

**Progressive Disclosure Level**: 3 (Implementation Details)

---

## Complete Workflow Implementation

```python
# Pseudo-code for orchestrator synthesis workflow

def orchestrator_synthesis_workflow(agent_findings: list[AgentFinding]) -> Synthesis:
    """
    Apply synthesis framework to multi-agent findings.

    Returns structured synthesis with recommendations.
    """
    # Step 1: Detect overlaps
    overlap_groups = detect_overlaps(agent_findings)

    # Step 2: For each overlap group, analyze trade-offs
    analyzed_groups = []
    for group in overlap_groups:
        solutions = []
        for finding in group.findings:
            trade_offs = extract_trade_offs(finding)
            score = calculate_recommendation_score(
                impact=finding.impact,
                effort=finding.effort,
                risk=finding.risk,
                change_scope=finding.change_scope
            )
            solutions.append(Solution(
                finding=finding,
                trade_offs=trade_offs,
                score=score
            ))

        # Sort by score (highest first)
        solutions.sort(key=lambda s: s.score, reverse=True)
        analyzed_groups.append(AnalyzedGroup(
            problem=group.problem,
            solutions=solutions,
            recommended=solutions[0]  # Highest score
        ))

    # Step 3: Generate structured presentation
    presentation = generate_synthesis_presentation(analyzed_groups)

    return Synthesis(
        overlap_groups=analyzed_groups,
        presentation=presentation,
        recommendations=[g.recommended for g in analyzed_groups]
    )
```

## Helper Functions

### detect_overlaps

```python
def detect_overlaps(findings: list[Finding]) -> list[OverlapGroup]:
    """
    Group findings by similarity using keyword matching and problem domain.

    Returns groups of overlapping findings addressing same problem.
    """
    overlap_groups = []

    for finding in findings:
        # Extract problem keywords
        keywords = extract_keywords(finding.description)
        problem_domain = categorize_problem(finding)

        # Check against existing groups
        matched_group = None
        for group in overlap_groups:
            similarity = calculate_similarity(finding, group)
            if similarity > 0.7:  # 70% similarity threshold
                matched_group = group
                break

        if matched_group:
            matched_group.add(finding)
        else:
            overlap_groups.append(OverlapGroup([finding]))

    return overlap_groups
```

### calculate_similarity

```python
def calculate_similarity(finding: Finding, group: OverlapGroup) -> float:
    """
    Calculate similarity score (0.0-1.0) between finding and group.

    Factors:
    - Keyword overlap (40%)
    - Problem domain match (30%)
    - File/location overlap (20%)
    - Agent type similarity (10%)
    """
    keyword_score = len(set(finding.keywords) & set(group.keywords)) / len(finding.keywords)
    domain_score = 1.0 if finding.domain == group.domain else 0.0
    location_score = 1.0 if finding.location == group.location else 0.5
    agent_score = 1.0 if finding.agent_type == group.primary_agent_type else 0.7

    return (keyword_score * 0.4 +
            domain_score * 0.3 +
            location_score * 0.2 +
            agent_score * 0.1)
```

### extract_trade_offs

```python
def extract_trade_offs(solution: Solution) -> TradeOffs:
    """
    Extract pros and cons from solution description and agent context.

    Returns structured trade-offs for comparison.
    """
    pros = []
    cons = []

    # Pattern matching for common trade-offs
    if "simple" in solution.description.lower():
        pros.append("Simple implementation")
    if "comprehensive" in solution.description.lower():
        pros.append("Comprehensive solution")
        cons.append("Higher complexity")
    if "refactor" in solution.description.lower():
        cons.append("Requires refactoring existing code")
    if "new pattern" in solution.description.lower():
        cons.append("Team learning curve")
    if "reuse" in solution.description.lower():
        pros.append("Leverages existing code")

    # Agent-specific insights
    if solution.agent == "tech-debt-investigator":
        pros.append("Reduces technical debt")
    if solution.agent == "code-quality":
        pros.append("Follows best practices")
    if solution.agent == "researcher-external":
        pros.append("Industry-standard approach")

    return TradeOffs(pros=pros, cons=cons)
```

## Data Structures

```python
from dataclasses import dataclass
from typing import List, Literal

@dataclass
class Finding:
    description: str
    keywords: List[str]
    domain: str
    location: str
    agent_type: str
    impact: int  # 1-5
    effort: int  # 1-5
    risk: Literal["Low", "Medium", "High"]
    change_scope: Literal["Localized", "Module", "System-wide"]

@dataclass
class OverlapGroup:
    findings: List[Finding]
    problem: str
    similarity_score: float
    keywords: List[str]
    domain: str
    primary_agent_type: str

    def add(self, finding: Finding):
        self.findings.append(finding)

@dataclass
class TradeOffs:
    pros: List[str]
    cons: List[str]

@dataclass
class Solution:
    finding: Finding
    trade_offs: TradeOffs
    score: float

@dataclass
class AnalyzedGroup:
    problem: str
    solutions: List[Solution]
    recommended: Solution

@dataclass
class Synthesis:
    overlap_groups: List[AnalyzedGroup]
    presentation: str
    recommendations: List[Solution]
```

## Usage Example

```python
# Orchestrator receives findings from multiple agents
agent_findings = [
    Finding(
        description="Add Pydantic model for validation",
        keywords=["validation", "pydantic", "model"],
        domain="security",
        location="packages/api/routes.py",
        agent_type="code-quality",
        impact=4,
        effort=2,
        risk="Low",
        change_scope="Localized"
    ),
    Finding(
        description="Refactor validation into service",
        keywords=["validation", "service", "refactor"],
        domain="architecture",
        location="packages/api/",
        agent_type="tech-debt-investigator",
        impact=3,
        effort=4,
        risk="Medium",
        change_scope="Module"
    ),
    # ... more findings
]

# Apply synthesis workflow
synthesis = orchestrator_synthesis_workflow(agent_findings)

# Present consolidated recommendations to user
print(synthesis.presentation)
```

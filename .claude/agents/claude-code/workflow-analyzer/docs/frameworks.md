# Analysis Frameworks

Methodologies and frameworks for workflow analysis.

---

## 7-Dimension Quality Matrix

The primary evaluation framework for command workflows.

### Dimension Details

#### 1. Workflow Correctness (Weight: 0.20)
**Focus**: Structural integrity of workflow execution

**Checks**:
- Step ordering respects dependencies
- No circular dependencies
- All paths lead to defined outputs
- Phase boundaries clear

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | Perfect ordering, all dependencies valid |
| 75 | Minor issues, no blocking problems |
| 50 | Workarounds needed for some steps |
| 25 | Significant ordering problems |
| 0 | Broken flow or circular dependencies |

#### 2. Parallelization Safety (Weight: 0.15)
**Focus**: Safe concurrent execution

**Checks**:
- Parallel operations independent
- No shared mutable state
- No race conditions
- Proper synchronization at joins

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | All parallel ops fully independent |
| 75 | Mostly safe, minor shared read-only |
| 50 | Needs synchronization |
| 25 | Unsafe parallelization |
| 0 | Critical race conditions |


#### 3. Gate Coverage (Weight: 0.15)
**Focus**: Decision point quality

**Checks**:
- All branches have gates
- Exit criteria defined
- Timeout specified
- Failure handling present

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | Complete gate coverage |
| 75 | Most gates defined |
| 50 | Partial coverage |
| 25 | Few gates |
| 0 | No gates |

#### 4. Subagent Validation (Weight: 0.15)
**Focus**: Agent delegation correctness

**Checks**:
- All Task() targets exist
- Agent tools match requirements
- Agent permissions sufficient
- Delegation parameters valid

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | All agents exist with required tools |
| 75 | All exist, minor tool gaps |
| 50 | Some tool mismatches |
| 25 | Missing agents with workarounds |
| 0 | Critical agents missing |

#### 5. Error Recovery (Weight: 0.15)
**Focus**: Failure handling completeness

**Checks**:
- Error codes defined
- Retry policies specified
- Fallback strategies present
- Escalation paths clear

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | Comprehensive error handling |
| 75 | Good handling, edge case gaps |
| 50 | Basic handling |
| 25 | Minimal handling |
| 0 | No error handling |


#### 6. State Management (Weight: 0.10)
**Focus**: State persistence and recovery

**Checks**:
- Checkpoints at phase boundaries
- Resume capability after failure
- State consistency maintained
- Clean state transitions

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | Full checkpoint/resume |
| 75 | Major phase checkpoints |
| 50 | Partial persistence |
| 25 | Minimal tracking |
| 0 | No state management |

#### 7. Integration Alignment (Weight: 0.10)
**Focus**: Orchestrator integration

**Checks**:
- Trigger keywords present
- Description follows format
- Tool permissions appropriate
- Output format compatible

**Scoring Rubric**:
| Score | Criteria |
|-------|----------|
| 100 | Full orchestrator integration |
| 75 | Good integration, minor gaps |
| 50 | Basic integration |
| 25 | Poor alignment |
| 0 | No integration consideration |

---

## SCAMPER Optimization Framework

Creative problem-solving for workflow improvement.

### The 7 Techniques

| Technique | Question | Application |
|-----------|----------|-------------|
| **S**ubstitute | What can be replaced? | Swap agents, change tools |
| **C**ombine | What can merge? | Consolidate phases |
| **A**dapt | What patterns apply? | Borrow from other commands |
| **M**odify | What to scale? | Adjust thresholds, parallelism |
| **P**ut to use | Other purposes? | Extend functionality |
| **E**liminate | What to remove? | Reduce complexity |
| **R**everse | Reorder? | Fail-fast optimization |


### Optimization Ranking Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Minimality | 0.40 | Smallest change possible |
| Risk | 0.35 | Lower is better |
| Maintainability | 0.25 | Clarity for future |

**Score Formula**: 
```
Score = (Minimality x 0.40) + ((1 - Risk) x 0.35) + (Maintainability x 0.25)
```

---

## Topological Analysis

For validating step ordering.

### Algorithm
1. Build directed graph: nodes = steps, edges = dependencies
2. Perform topological sort (Kahn's algorithm)
3. If sort fails = cycle detected
4. Sort order = valid execution order

### Cycle Detection
When cycle found:
1. Identify all nodes in cycle
2. Report as CRITICAL violation
3. Show dependency chain

---

## Dependency Graph Analysis

### Graph Construction
```
Step 1.1 -> Step 1.2 -> Step 2.1
                    \-> Step 2.2 (parallel)
Step 2.1 -\
Step 2.2 -/-> Step 3.1
```

### Analysis Outputs
- **Critical Path**: Longest dependency chain
- **Parallel Groups**: Independent step clusters
- **Bottlenecks**: High fan-in nodes
- **Orphans**: Steps with no dependencies or dependents

---

## CQ Score Calculation

Context Quality for proceeding to analysis.

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Ordering clarity | 0.25 | 1.0 if DAG valid |
| Agent availability | 0.25 | found/total agents |
| Skill availability | 0.20 | found/total skills |
| Pattern alignment | 0.15 | deviation from best practices |
| Documentation | 0.15 | workflow description completeness |

**Gate**: CQ >= 0.85 to proceed

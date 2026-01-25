# Frameworks: Sentiment NLP Workflows

**Purpose**: Detailed workflow operations and integration patterns for sentiment analysis.

---

## Workflow Operations

### 1. Analyze Sentiment (`analyze_sentiment`)

**Input**: headlines array, config (model_name, batch_size, confidence_threshold, device)

**Phases**:
1. **Analysis**: Parse headlines, count by symbol, assess batch complexity
2. **Research**: Check FinBERT version, verify device compatibility
3. **Todo Creation**: Load model, batch processing, score extraction, cache results
4. **Implementation**: Execute FinBERT inference with timeout, apply confidence filtering
5. **Validation**: Check sentiment distribution, verify confidence scores
6. **Reflection**: Document model performance, identify tuning opportunities

**Output**: `sentiment_scores` array + `processing_stats`

---

### 2. Aggregate Sentiment (`aggregate_sentiment`)

**Input**: headlines with scores OR raw headlines, aggregation_params (time_bucket, weighting, normalization, lookback)

**Phases**:
1. **Analysis**: Identify symbols, time buckets, baseline requirements
2. **Research**: Query existing baseline statistics, determine normalization strategy
3. **Todo Creation**: Group by symbol+bucket, calculate raw scores, compute baselines, calculate z-scores
4. **Implementation**: Apply weighting, compute zS and zΔS, handle edge cases, export to Parquet
5. **Validation**: Check z-score distribution, verify no NaN propagation
6. **Reflection**: Document normalization effectiveness, identify outliers

**Output**: `aggregated_scores` array + `normalization_params`

---

### 3. Detect Bursts (`detect_bursts`)

**Input**: headlines with timestamps/symbols OR aggregated scores, burst_params (volume_threshold, sentiment_shift_threshold, baseline_window)

**Phases**:
1. **Analysis**: Parse baseline window, identify candidate bursts
2. **Research**: Query baseline statistics, review detection patterns
3. **Todo Creation**: Calculate baselines, detect volume spikes, detect sentiment shifts, flag combined bursts
4. **Implementation**: Apply volume ratio calculation, filter by thresholds, sample representative headlines
5. **Validation**: Check false positive rate, verify baseline calculations
6. **Reflection**: Document burst patterns, recommend threshold tuning

**Output**: `bursts_detected` array + `baseline_stats`

---

### 4. Extract Themes (`extract_themes`)

**Input**: headlines with text/symbols/timestamps, theme_params (max_themes, min_frequency, extraction_method)

**Phases**:
1. **Analysis**: Count headline volume, identify extraction method feasibility
2. **Research**: Review n-gram patterns, check topic modeling availability
3. **Todo Creation**: Tokenize, extract n-grams, cluster keywords, map to symbols
4. **Implementation**: Apply extraction method (keyword/ngram/topic_model), calculate avg sentiment per theme
5. **Validation**: Check theme coherence, verify min_frequency threshold
6. **Reflection**: Document theme quality, recommend method tuning

**Output**: `themes` array + `extraction_method`

---

## Tool Usage Patterns

| Tool | Use Case |
|------|----------|
| Read | Load connector outputs, baseline statistics, PEAD patterns |
| Write | Export aggregated features (Parquet), cache scores, save outputs |
| Bash | HuggingFace downloads, GPU checks, batch inference scripts |
| Grep | Search for sentiment patterns, connector implementations |
| Glob | Discover connector files, feature targets, utilities |
| Task | Delegate to researcher-external, debugger, python-code-reviewer |
| WebFetch | Fetch FinBERT docs, normalization papers, best practices |

### Tool Coordination
- **Parallel**: Read connector files + Grep patterns + Glob utilities (independent)
- **Sequential**: Load model -> Inference -> Aggregate -> Export

---

## Multi-Agent Integration

### Upstream Dependencies
- News connectors (`packages/core/qual/connectors/`) provide headline inputs
- researcher-external for HuggingFace updates, statistical methods
- debugger for inference timeout troubleshooting

### Downstream Integration
- Feature pipeline (`packages/core/features/`) consumes aggregated features
- PEAD detector uses sentiment scores for +0.2 enhancement
- Monitoring agents consume burst detection alerts

### State Management
- Cache sentiment scores per headline hash
- Maintain rolling baseline statistics (1-day window default)
- Persist model in memory for batch efficiency

### Conflict Resolution
- Defer to PEAD detector on feature format requirements
- Escalate to orchestrator on normalization parameter conflicts

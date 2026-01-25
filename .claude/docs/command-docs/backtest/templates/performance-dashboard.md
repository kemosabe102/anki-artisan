# Performance Dashboard Template

> ASCII dashboard template for backtest command output

```
================================================================================
                        BACKTEST PERFORMANCE DASHBOARD
================================================================================

  Algorithm: {algorithm_name}
  Tier:      {tier_level} ({tier_description})
  Hypothesis: {hypothesis_summary}
  
  Backtest Period: {start_date} to {end_date} ({total_days} days)
  Benchmark:       {benchmark_name}
  Data Source:     {data_source}

================================================================================
                              DIMENSION SCORES
================================================================================

  [1] PROFITABILITY        [2] RISK-ADJUSTED       [3] DOWNSIDE PROTECTION
  Score: {prof_score}/100       Score: {risk_score}/100      Score: {down_score}/100
  Gate:  {prof_gate}            Gate:  {risk_gate}           Gate:  {down_gate}

  [4] TRADE QUALITY        [5] CONSISTENCY         [6] RECOVERY
  Score: {trade_score}/100      Score: {cons_score}/100      Score: {recov_score}/100
  Gate:  {trade_gate}           Gate:  {cons_gate}           Gate:  {recov_gate}

================================================================================
```

                         [1] PROFITABILITY METRICS
--------------------------------------------------------------------------------

  +----------------------+------------------+------------------+
  | Metric               | Value            | vs Benchmark     |
  +----------------------+------------------+------------------+
  | Total Return         | {total_return}%  | {total_vs_bench} |
  | CAGR                 | {cagr}%          | {cagr_vs_bench}  |
  | Monthly Avg Return   | {monthly_avg}%   | {mavg_vs_bench}  |
  | Best Month           | {best_month}%    | {best_vs_bench}  |
  | Worst Month          | {worst_month}%   | {worst_vs_bench} |
  | Profit Factor        | {profit_factor}  | {pf_vs_bench}    |
  +----------------------+------------------+------------------+

  Status: {prof_status}  |  Gate Threshold: {prof_threshold}

--------------------------------------------------------------------------------
                       [2] RISK-ADJUSTED METRICS
--------------------------------------------------------------------------------

  +----------------------+------------------+------------------+
  | Metric               | Value            | Rating           |
  +----------------------+------------------+------------------+
  | Sharpe Ratio         | {sharpe}         | {sharpe_rating}  |
  | Sortino Ratio        | {sortino}        | {sortino_rating} |
  | Calmar Ratio         | {calmar}         | {calmar_rating}  |
  | Annualized Vol       | {volatility}%    | {vol_rating}     |
  | Information Ratio    | {info_ratio}     | {ir_rating}      |
  +----------------------+------------------+------------------+

  Status: {risk_status}  |  Gate Threshold: {risk_threshold}

--------------------------------------------------------------------------------
                      [3] DOWNSIDE PROTECTION METRICS
--------------------------------------------------------------------------------

  +----------------------+------------------+------------------+
  | Metric               | Value            | Rating           |
  +----------------------+------------------+------------------+
  | Max Drawdown         | {max_dd}%        | {max_dd_rating}  |
  | Average Drawdown     | {avg_dd}%        | {avg_dd_rating}  |
  | Drawdown Duration    | {dd_duration}    | {dd_dur_rating}  |
  | VaR (95%)            | {var_95}%        | {var_rating}     |
  | Max Consec Losses    | {consec_losses}  | {cl_rating}      |
  | Ulcer Index          | {ulcer_index}    | {ulcer_rating}   |
  +----------------------+------------------+------------------+

  Status: {down_status}  |  Gate Threshold: {down_threshold}

--------------------------------------------------------------------------------
                        [4] TRADE QUALITY METRICS
--------------------------------------------------------------------------------

  +----------------------+------------------+------------------+
  | Metric               | Value            | Rating           |
  +----------------------+------------------+------------------+
  | Total Trades         | {total_trades}   | {trades_rating}  |
  | Win Rate             | {win_rate}%      | {wr_rating}      |
  | Profit Factor        | {trade_pf}       | {tpf_rating}     |
  | Avg Winning Trade    | {avg_win}%       | {avgw_rating}    |
  | Avg Losing Trade     | {avg_loss}%      | {avgl_rating}    |
  | Win/Loss Ratio       | {wl_ratio}       | {wlr_rating}     |
  | Expectancy           | {expectancy}     | {exp_rating}     |
  +----------------------+------------------+------------------+

  Status: {trade_status}  |  Gate Threshold: {trade_threshold}

--------------------------------------------------------------------------------
                        [5] CONSISTENCY METRICS
--------------------------------------------------------------------------------

  +----------------------+------------------+------------------+
  | Metric               | Value            | Rating           |
  +----------------------+------------------+------------------+
  | Max Consec Wins      | {consec_wins}    | {cw_rating}      |
  | Max Consec Losses    | {consec_losses}  | {cl_rating}      |
  | Months Profitable    | {months_profit}% | {mp_rating}      |
  | Regime CV            | {regime_cv}      | {rcv_rating}     |
  | Return Stability     | {stability}      | {stab_rating}    |
  | Skewness             | {skewness}       | {skew_rating}    |
  +----------------------+------------------+------------------+

  Status: {cons_status}  |  Gate Threshold: {cons_threshold}

--------------------------------------------------------------------------------
                         [6] RECOVERY METRICS
--------------------------------------------------------------------------------

  +----------------------+------------------+------------------+
  | Metric               | Value            | Rating           |
  +----------------------+------------------+------------------+
  | Recovery Factor      | {recovery_factor}| {rf_rating}      |
  | Time to New High     | {time_new_high}  | {tnh_rating}     |
  | Avg DD Depth         | {dd_depth_avg}%  | {dda_rating}     |
  | Recovery Speed       | {recov_speed}    | {rs_rating}      |
  | Resilience Score     | {resilience}     | {resil_rating}   |
  +----------------------+------------------+------------------+

  Status: {recov_status}  |  Gate Threshold: {recov_threshold}

================================================================================
                          GATE VALIDATION SUMMARY
================================================================================

  +---------------------+----------+----------+----------+---------+----------+
  | Dimension           | Score    | Required | Status   | Weight  | Weighted |
  +---------------------+----------+----------+----------+---------+----------+
  | Profitability       | {ps}/100 | {pt}     | {p_stat} | {pw}%   | {p_wtd}  |
  | Risk-Adjusted       | {rs}/100 | {rt}     | {r_stat} | {rw}%   | {r_wtd}  |
  | Downside Protection | {ds}/100 | {dt}     | {d_stat} | {dw}%   | {d_wtd}  |
  | Trade Quality       | {ts}/100 | {tt}     | {t_stat} | {tw}%   | {t_wtd}  |
  | Consistency         | {cs}/100 | {ct}     | {c_stat} | {cw}%   | {c_wtd}  |
  | Recovery            | {vs}/100 | {vt}     | {v_stat} | {vw}%   | {v_wtd}  |
  +---------------------+----------+----------+----------+---------+----------+
  | COMPOSITE           | {comp_score}/100    | {comp_req}| {comp_s}|         |
  +---------------------+----------+----------+----------+---------+----------+

  Gates Passed: {gates_passed}/6
  Composite Score: {composite_score}/100
  Tier Requirement: {tier_requirement}

================================================================================
                       HISTORICAL COMPARISON (OPTIONAL)
================================================================================

  Previous Backtest: {prev_backtest_date}
  
  +---------------------+----------+----------+----------+
  | Metric              | Previous | Current  | Delta    |
  +---------------------+----------+----------+----------+
  | Total Return        | {prev_tr}| {curr_tr}| {delta_tr}|
  | Sharpe Ratio        | {prev_sh}| {curr_sh}| {delta_sh}|
  | Max Drawdown        | {prev_dd}| {curr_dd}| {delta_dd}|
  | Win Rate            | {prev_wr}| {curr_wr}| {delta_wr}|
  | Composite Score     | {prev_cs}| {curr_cs}| {delta_cs}|
  +---------------------+----------+----------+----------+

  Trend: {performance_trend} ({trend_direction})

================================================================================
                                 VERDICT
================================================================================

  Overall Assessment: {verdict_status}
  
  +-----------------------------------------------------------------------+
  |                                                                       |
  |   {verdict_icon}  {verdict_headline}
  |                                                                       |
  |   Composite Score: {composite_score}/100                              |
  |   Gates Passed:    {gates_passed}/6                                   |
  |   Tier Status:     {tier_status}                                      |
  |                                                                       |
  +-----------------------------------------------------------------------+

  ACTION ROUTING:
  ---------------
  
  {action_routing_block}

  Recommended Actions:
  - {action_1}
  - {action_2}
  - {action_3}

  Next Steps:
  -----------
  [ ] {next_step_1}
  [ ] {next_step_2}
  [ ] {next_step_3}

================================================================================
                              END OF REPORT
================================================================================
  Generated: {report_timestamp}
  Algorithm: {algorithm_name} v{algorithm_version}
  Report ID: {report_id}
================================================================================
```

---

## Placeholder Reference

| Placeholder | Description | Example Value |
|-------------|-------------|---------------|
| `{algorithm_name}` | Name of the algorithm | "MomentumBreakout" |
| `{tier_level}` | Current tier (1-5) | "Tier 3" |
| `{tier_description}` | Tier meaning | "Paper Trading Ready" |
| `{hypothesis_summary}` | Brief hypothesis | "Mean reversion in oversold conditions" |
| `{start_date}` | Backtest start | "2020-01-01" |
| `{end_date}` | Backtest end | "2024-12-31" |
| `{total_return}` | Total return percentage | "127.5" |
| `{sharpe}` | Sharpe ratio | "1.85" |
| `{max_dd}` | Maximum drawdown | "-15.3" |
| `{win_rate}` | Win rate percentage | "58.2" |
| `{composite_score}` | Overall composite score | "78" |
| `{verdict_status}` | PASS/FAIL/CONDITIONAL | "PASS" |
| `{verdict_icon}` | Status icon | "[PASS]" or "[FAIL]" |

---

## Status Indicators

- `[PASS]` - Metric meets or exceeds threshold
- `[FAIL]` - Metric below threshold
- `[WARN]` - Metric marginal, needs attention
- `[N/A]` - Metric not applicable for tier

---

## Action Routing Templates

**PASS - Tier Promotion:**
```
  Route: TIER_PROMOTION
  Current: Tier {current_tier}
  Target:  Tier {target_tier}
  Action:  Proceed to {next_phase} validation
```

**FAIL - Refinement Required:**
```
  Route: REFINEMENT_REQUIRED
  Failed Gates: {failed_gates}
  Priority Fix: {priority_dimension}
  Action:  Return to hypothesis refinement
```

**CONDITIONAL - Partial Pass:**
```
  Route: CONDITIONAL_PASS
  Passed Gates: {passed_gates}/6
  Blocking: {blocking_dimensions}
  Action:  Address blocking dimensions before promotion
```

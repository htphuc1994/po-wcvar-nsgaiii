#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_s55_experimental_results.py — Helpers to re-check calculations in §5.5 (Experimental results)

How to use
----------
1) Paste the values from your paper into the placeholders below:
   - early_stage_nsga3hop and early_stage_nsga3  (10 values each; Table 8)
   - monthly_wcvar (per algorithm, 11 months each; Table 10). If values are in %, set as_percent=True.
   - eps_sweep (optional): WCVaR by epsilon, averaged across horizons (Table 11)
2) Run:  python verify_s55_experimental_results.py
3) Compare the printed outputs to the paper.

Requires: numpy, scipy, pandas
"""
import math
import numpy as np
import pandas as pd
from scipy import stats

# ---------------------------
# Utility / effect size tools
# ---------------------------
def iqr(x, qlow=25.0, qhigh=75.0):
    x = np.asarray(x, dtype=float)
    return np.percentile(x, qhigh) - np.percentile(x, qlow)

def mann_whitney_details(x, y, alternative='two-sided', method='auto'):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    nx, ny = len(x), len(y)
    res_two = stats.mannwhitneyu(x, y, alternative='two-sided', method=method)
    res_less = stats.mannwhitneyu(x, y, alternative='less', method=method)
    res_greater = stats.mannwhitneyu(x, y, alternative='greater', method=method)
    # U for x vs y returned by SciPy is U_x
    Ux = float(res_two.statistic)
    Umin = min(Ux, nx*ny - Ux)
    # Common-language effect size P(X<Y) (ties count as 0.5 if present)
    cl = Ux / (nx * ny)
    # Rank-biserial correlation (signed toward "x < y" direction)
    r_rb = 1 - (2 * Umin) / (nx * ny)
    return {
        'nx': nx, 'ny': ny,
        'U_x': Ux, 'U_min': Umin,
        'p_two_sided': float(res_two.pvalue),
        'p_one_sided_x_less_y': float(res_less.pvalue),
        'p_one_sided_x_greater_y': float(res_greater.pvalue),
        'common_language_P[X<Y]': cl,
        'rank_biserial_r_rb': r_rb,
    }

def wilcoxon_paired_details(x, y, zero_method='wilcox', correction=False, mode='auto'):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    diffs = x - y
    # Remove zero diffs for ranking
    mask = diffs != 0
    diffs_nz = diffs[mask]
    n = len(diffs_nz)
    # Ranks of absolute diffs
    ranks = stats.rankdata(np.abs(diffs_nz), method='average')
    W_plus = float(ranks[diffs_nz > 0].sum())
    W_minus = float(ranks[diffs_nz < 0].sum())
    # SciPy Wilcoxon (statistic is W_plus)
    res_two = stats.wilcoxon(x, y, zero_method=zero_method, correction=correction,
                             alternative='two-sided', mode=mode)
    res_less = stats.wilcoxon(x, y, zero_method=zero_method, correction=correction,
                              alternative='less', mode=mode)
    res_greater = stats.wilcoxon(x, y, zero_method=zero_method, correction=correction,
                                 alternative='greater', mode=mode)
    # Hodges–Lehmann for paired: median of paired differences
    hl = float(np.median(diffs))
    # Rank-biserial for paired = 1 - 2*min(W+, W-)/T, where T = n(n+1)/2
    T = n*(n+1)/2.0 if n > 0 else float('nan')
    r_rb = 1 - 2*min(W_plus, W_minus)/T if n > 0 else float('nan')
    return {
        'n_nonzero_pairs': n,
        'W_plus': W_plus,
        'W_minus': W_minus,
        'T_total_rank_sum': T,
        'p_two_sided': float(res_two.pvalue),
        'p_one_sided_x_less_y': float(res_less.pvalue),
        'p_one_sided_x_greater_y': float(res_greater.pvalue),
        'HL_median_diff_x_minus_y': hl,
        'rank_biserial_r_rb': r_rb,
    }

def deposit_return(monthly_rate, months):
    """Compound-return for a bank deposit with monthly rate (e.g., 0.0045 for 0.45%)."""
    return (1.0 + float(monthly_rate))**int(months) - 1.0

# ---------------------------
# Placeholders — paste numbers
# ---------------------------
# Early-stage per-seed means (Table 8): 10 values each
# Example: early_stage_nsga3hop = [0.07127, 0.05410, ...]  # length 10
early_stage_nsga3hop = [
    # TODO: paste 10 values here (HOP)
]
early_stage_nsga3 = [
    # TODO: paste 10 values here (vanilla NSGA-III)
]

# Monthly WCVaR table (Table 10): 11 months per algorithm
# If your table lists values as percentages (e.g., 0.95 for 0.95%), set as_percent=True.
as_percent = True  # change to False if numbers are in decimal units (e.g., 0.0095)
months = [f"M{i}" for i in range(1, 12)]

monthly_wcvar = {
    # 'HOP': [ ... 11 values ... ],
    # 'NSGA-III': [ ... 11 values ... ],
    # 'SMS-EMOA': [ ... 11 values ... ],
    # 'U-NSGA-III': [ ... 11 values ... ],
    # 'C-TAEA': [ ... 11 values ... ],
}

# Optional: epsilon sweep (Table 11) — horizon-averaged WCVaR and runtime
# Example structure:
# eps_sweep = [
#     {'epsilon': 0.20, 'wcvar_avg': 0.098, 'runtime_min': 2.14},
#     {'epsilon': 0.10, 'wcvar_avg': 0.108, 'runtime_min': 2.36},
#     {'epsilon': 0.05, 'wcvar_avg': 0.181, 'runtime_min': 3.15},
# ]
eps_sweep = []

# ---------------------------
# Reporting helpers
# ---------------------------
def summarize_series(name, arr):
    arr = np.asarray(arr, dtype=float)
    s = pd.Series(arr, name=name)
    out = {
        'n': int(s.size),
        'mean': float(s.mean()),
        'median': float(s.median()),
        'q25': float(s.quantile(0.25)),
        'q75': float(s.quantile(0.75)),
        'IQR': float(s.quantile(0.75) - s.quantile(0.25)),
        'std': float(s.std(ddof=1)) if s.size > 1 else float('nan'),
        'min': float(s.min()) if s.size else float('nan'),
        'max': float(s.max()) if s.size else float('nan'),
    }
    return out

def print_table(d, title=None):
    if title:
        print(f"\n=== {title} ===")
    df = pd.DataFrame(d).T
    with pd.option_context('display.float_format', '{:0.8f}'.format):
        print(df)

# ---------------------------
# Main checks
# ---------------------------
def main():
    print("\n# Re-checks for §5.5 (Experimental results)")
    # 1) Early-stage summaries and tests
    if len(early_stage_nsga3hop) == 10 and len(early_stage_nsga3) == 10:
        sX = summarize_series("NSGA-III-HOP", early_stage_nsga3hop)
        sY = summarize_series("NSGA-III", early_stage_nsga3)
        print_table(sX, "Early-stage per-seed summary: NSGA-III-HOP")
        print_table(sY, "Early-stage per-seed summary: NSGA-III")

        mw = mann_whitney_details(early_stage_nsga3hop, early_stage_nsga3, method='auto')
        print_table(mw, "Mann–Whitney U (HOP vs NSGA-III)")

        wz = wilcoxon_paired_details(np.asarray(early_stage_nsga3hop),
                                     np.asarray(early_stage_nsga3),
                                     mode='auto')
        print_table(wz, "Paired Wilcoxon signed-rank (HOP minus NSGA-III)")
    else:
        print("\n[info] Skipping early-stage tests — paste 10 values into 'early_stage_nsga3hop' and 'early_stage_nsga3'.")

    # 2) Monthly WCVaR (Table 10): means and per-month winners
    if monthly_wcvar:
        df = pd.DataFrame(monthly_wcvar, index=months)
        if as_percent:
            # If your inputs are percentages (e.g., 0.95 = 0.95%), we keep the unit unchanged.
            pass
        col_means = df.mean(axis=0)
        print("\n=== Monthly WCVaR Table (as provided) ===")
        with pd.option_context('display.float_format', '{:0.6f}'.format):
            print(df)

        print("\nColumn means (same units as input):")
        for algo, m in col_means.items():
            print(f"  {algo}: {m:0.6f}")

        # Per-month minima (winner)
        winners = df.idxmin(axis=1)
        print("\nPer-month leaders (lower WCVaR is better):")
        for month, algo in winners.items():
            print(f"  {month}: {algo}")
    else:
        print("\n[info] Skipping monthly WCVaR check — fill 'monthly_wcvar' with 11 values per algorithm.")

    # 3) Deposit benchmark
    alpha = 0.0045  # 0.45% per month
    for m in (3, 6, 12):
        dep = deposit_return(alpha, m)
        print(f"\nBank deposit baseline for {m} months at 0.45%/mo: {100*dep:0.2f}%")

    # 4) Epsilon sweep
    if eps_sweep:
        df_eps = pd.DataFrame(eps_sweep).sort_values('epsilon')
        print("\n=== Tail-probability sweep (as provided) ===")
        with pd.option_context('display.float_format', '{:0.6f}'.format):
            print(df_eps)
        # Simple monotonicity checks
        if df_eps['wcvar_avg'].is_monotonic_decreasing:
            print("WCVaR average decreases as epsilon increases (less conservative tail).")
        elif df_eps['wcvar_avg'].is_monotonic_increasing:
            print("WCVaR average increases as epsilon decreases (more conservative tail).")
        else:
            print("WCVaR average is not monotonic in epsilon.")
        if df_eps['runtime_min'].is_monotonic_increasing:
            print("Runtime increases as epsilon tightens (expected).")
    else:
        print("\n[info] Skipping epsilon sweep — add rows to 'eps_sweep' to check monotonicity.")

if __name__ == "__main__":
    main()
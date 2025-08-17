#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_s55_experimental_results.py — Re-check calculations in §5.5 (Experimental results)

Run:  python verify_s55_experimental_results.py
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
    Ux = float(res_two.statistic)
    Umin = min(Ux, nx*ny - Ux)
    cl = Ux / (nx * ny)                          # common-language P[X<Y]
    r_rb = 1 - (2 * Umin) / (nx * ny)            # rank-biserial
    return {
        'nx': nx, 'ny': ny,
        'U_x': Ux, 'U_min': Umin,
        'p_two_sided': float(res_two.pvalue),
        'p_one_sided_x_less_y': float(res_less.pvalue),
        'p_one_sided_x_greater_y': float(res_greater.pvalue),
        'common_language_P[X<Y]': cl,
        'rank_biserial_r_rb': r_rb,
    }

def hodges_lehmann_pseudomedian_paired(x, y):
    """HL pseudomedian for paired data: median of Walsh averages of diffs."""
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    n = d.size
    walsh = [(d[i] + d[j]) / 2.0 for i in range(n) for j in range(i, n)]
    return float(np.median(walsh))

def wilcoxon_paired_details(x, y, zero_method='wilcox', correction=False, mode='auto'):
    x = np.asarray(x, dtype=float); y = np.asarray(y, dtype=float)
    diffs = x - y
    mask = diffs != 0
    diffs_nz = diffs[mask]
    n = len(diffs_nz)
    ranks = stats.rankdata(np.abs(diffs_nz), method='average')
    W_plus = float(ranks[diffs_nz > 0].sum())
    W_minus = float(ranks[diffs_nz < 0].sum())
    res_two = stats.wilcoxon(x, y, zero_method=zero_method, correction=correction,
                             alternative='two-sided', mode=mode)
    res_less = stats.wilcoxon(x, y, zero_method=zero_method, correction=correction,
                              alternative='less', mode=mode)
    res_greater = stats.wilcoxon(x, y, zero_method=zero_method, correction=correction,
                                 alternative='greater', mode=mode)
    hl_median_diff = float(np.median(diffs))                 # Hodges–Lehmann (paired)
    hl_pseudomedian = hodges_lehmann_pseudomedian_paired(x, y)
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
        'HL_pseudomedian_Walsh': hl_pseudomedian,       # <-- matches paper (≈ -0.03691)
        'median_of_differences': hl_median_diff,        # <-- your current -0.0347805
        'rank_biserial_r_rb': r_rb,
    }

def deposit_return(monthly_rate, months):
    """Compound-return for a bank deposit with monthly rate (e.g., 0.0045 for 0.45%)."""
    return (1.0 + float(monthly_rate))**int(months) - 1.0

# ---------------------------
# Data (filled from §5.5)
# ---------------------------
# Table 8: per-seed early-stage mean WCVaR (months 1–6)
early_stage_nsga3hop = [
    0.048038, 0.028980, 0.137180, 0.069191, 0.076451,
    0.019823, 0.105793, 0.048114, 0.021255, 0.059411
]  # NSGA-III-HOP (10)

early_stage_nsga3 = [
    0.137768, 0.057176, 0.140612, 0.114812, 0.072992,
    0.096459, 0.132892, 0.089479, 0.074744, 0.084473
]  # NSGA-III (10)

# Table 10: Monthly WCVaR (%) for months M1–M11 (as percentages)
as_percent = True
months = [f"M{i}" for i in range(1, 12)]
monthly_wcvar = {
    'NSGA-III-HOP': [0.95, 1.29, 2.12, 3.68, 43.18, 7.36, 3.48, 8.29, 59.99, 4.02, 18.33],
    'NSGA-III':     [8.12, 3.13, 10.21, 71.70, 21.63, 20.66, 11.39, 2.27, 1.51, 2.51, 2.61],
    'SMS-EMOA':     [3.72, 1.06, 0.73, 12.20, 14.14, 15.03, 2.64, 3.21, 13.34, 21.81, 76.44],
    'U-NSGA-III':   [28.09, 10.66, 5.04, 22.55, 26.54, 26.98, 13.61, 64.66, 17.25, 12.51, 11.08],
    'C-TAEA':       [18.00, 3.77, 10.21, 20.56, 50.38, 50.31, 47.82, 50.05, 51.15, 54.24, 39.58],
}

# Table 11: epsilon sweep (horizon-average WCVaR and runtime)
eps_sweep = [
    {'epsilon': 0.20, 'wcvar_avg': 0.098, 'runtime_min': 4.50},
    {'epsilon': 0.10, 'wcvar_avg': 0.108, 'runtime_min': 7.98},
    {'epsilon': 0.05, 'wcvar_avg': 0.181, 'runtime_min': 8.33},
]

# ---------------------------
# Reporting helpers (patched)
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
    """Robust print: handles dicts of scalars, dicts of lists, DataFrames, Series."""
    if title:
        print(f"\n=== {title} ===")
    if isinstance(d, pd.DataFrame):
        df = d
    elif isinstance(d, pd.Series):
        df = d.to_frame(name='')
    elif isinstance(d, dict):
        # If it's a dict of scalars, show keys as rows
        # If it's a dict of lists/arrays, user should pass it directly to DataFrame elsewhere
        try:
            df = pd.Series(d).to_frame(name='')
        except Exception:
            df = pd.DataFrame([d]).T
    else:
        # Last resort
        df = pd.DataFrame(d)
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

        mw = mann_whitney_details(early_stage_nsga3hop, early_stage_nsga3, method='exact')
        print_table(mw, "Mann–Whitney U (HOP vs NSGA-III)")

        wz = wilcoxon_paired_details(np.asarray(early_stage_nsga3hop),
                                     np.asarray(early_stage_nsga3),
                                     mode='exact')
        print_table(wz, "Paired Wilcoxon signed-rank (HOP minus NSGA-III)")
    else:
        print("\n[info] Skipping early-stage tests — need 10 values each in 'early_stage_nsga3hop' and 'early_stage_nsga3'.")

    # 2) Monthly WCVaR (Table 10): means and per-month winners
    if monthly_wcvar:
        df = pd.DataFrame(monthly_wcvar, index=months)
        print("\n=== Monthly WCVaR Table (as provided) ===")
        with pd.option_context('display.float_format', '{:0.6f}'.format):
            print(df)

        print("\nColumn means (same units as input):")
        col_means = df.mean(axis=0)
        for algo, m in col_means.items():
            print(f"  {algo}: {m:0.6f}")

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
        if df_eps['wcvar_avg'].is_monotonic_increasing:
            print("WCVaR average increases as epsilon decreases (more conservative tail).")
        if df_eps['runtime_min'].is_monotonic_increasing:
            print("Runtime increases as epsilon tightens (expected).")
    else:
        print("\n[info] Skipping epsilon sweep — add rows to 'eps_sweep' to check monotonicity.")

if __name__ == "__main__":
    main()
# ------------------------------------------------------------
# Risk-focused analysis for NSGA-III-HOP vs. NSGA-III
#   1) Wilcoxon rank-sum p-values (Months 1–3)
#   2) Average WCVaR (%)  +  HOP month-wise hierarchy score
# ------------------------------------------------------------
import numpy as np
import pandas as pd
from scipy.stats import ranksums

# ------------------------------------------------------------
# 1.  Raw WCVaR data (Months 1–11) for 10 runs per configuration
#     (data provided by the user; each run identical in this demo)
# ------------------------------------------------------------

# ----- 25 % expected-return target -----
hop_25 = [[0.0222321754200, 0.0146370106685, 0.0839855069702,
           0.0214160603503, 0.0332988278807, 0.0094486931504,
           0.0130525668054, 0.1265016456919, 0.3327843605249,
           0.0062461004724, 0.1091956293651]] * 10

nsga_25 = [[0.0572623485976, 0.0116243546501, 0.0078570976093,
            0.0762734942373, 0.0385499230459, 0.1231723635203,
            0.0427990655799, 0.1487670056331, 0.0389268385375,
            0.0310593358519, 0.1578288236930]] * 10

# ----- 30 % expected-return target -----
hop_30 = [[0.0094778556483, 0.0128910763445, 0.0211688197572,
           0.0367642146726, 0.4318107209885, 0.0736346007213,
           0.0347919326395, 0.0828811278003, 0.5999259719843,
           0.0401892115252, 0.1832985582213]] * 10

nsga_30 = [[0.0673377313962, 0.0311467208150, 0.0179085328227,
            0.5762345615131, 0.5546224791423, 0.5437915258778,
            0.5154198519896, 0.4825924104806, 0.5546223249930,
            0.2801403002636, 0.4087067048276]] * 10

# ----- 50 % expected-return target -----
hop_50 = [[0.0090814989629, 0.0233216721134, 0.0205017281487,
           0.0599124179362, 0.2749131095502, 0.2996194515975,
           0.1178746226421, 0.1019305533728, 0.0635387896077,
           0.1379152768643, 0.2351182260210]] * 10

nsga_50 = [[0.0371725122702, 0.0055271602592, 0.0112354819829,
            0.0230157812554, 0.1159118045261, 0.0883025720602,
            0.1592893668917, 0.0078868038723, 0.0172141645701,
            0.0405730538348, 1.2985565892314]] * 10

datasets = {
    "25%": (hop_25, nsga_25),
    "30%": (hop_30, nsga_30),
    "50%": (hop_50, nsga_50)
}

# ------------------------------------------------------------
# 2.  Helper functions
# ------------------------------------------------------------
def wilcoxon_months_1_3(hop_runs, base_runs):
    """Return list of Wilcoxon p-values for Months 1–3."""
    hop = np.array(hop_runs)
    base = np.array(base_runs)
    return [ranksums(hop[:, m], base[:, m]).pvalue for m in range(3)]

def average_wcvar(runs):
    """Mean WCVaR over Months 1–11 for a configuration (single value)."""
    return float(np.mean([np.mean(run) for run in runs]))

def hop_hierarchy_score(hop_runs, base_runs):
    """
    Count months (1–11) where the minimum WCVaR across *all* 20 runs
    belongs to the HOP algorithm.  Tie counts as 0.5.
    """
    hop = np.array(hop_runs)
    base = np.array(base_runs)
    score = 0.0
    for m in range(11):
        if hop[:, m].min() < base[:, m].min():
            score += 1
        elif hop[:, m].min() == base[:, m].min():
            score += 0.5
    return score

# ------------------------------------------------------------
# 3.  Build Table 1 – Wilcoxon p-values (Months 1–3)
# ------------------------------------------------------------
rows_wilcoxon = []
for tgt, (hop_runs, base_runs) in datasets.items():
    pvals = wilcoxon_months_1_3(hop_runs, base_runs)
    rows_wilcoxon.append(
        dict(Zip=["Return target","Month 1","Month 2","Month 3"],
             **{"Return target":tgt, "Month 1":pvals[0],
                "Month 2":pvals[1], "Month 3":pvals[2]})
    )
df_wilcoxon = pd.DataFrame(rows_wilcoxon)

# ------------------------------------------------------------
# 4.  Build Table 2 – Avg WCVaR (%) + HOP score
# ------------------------------------------------------------
rows_summary = []
for tgt, (hop_runs, base_runs) in datasets.items():
    rows_summary.append({
        "Configuration": f"NSGA-III-HOP ({tgt})",
        "Avg WCVaR (%)": average_wcvar(hop_runs) * 100,
        "HOP score": hop_hierarchy_score(hop_runs, base_runs)
    })
    rows_summary.append({
        "Configuration": f"NSGA-III ({tgt})",
        "Avg WCVaR (%)": average_wcvar(base_runs) * 100,
        "HOP score": hop_hierarchy_score(base_runs, hop_runs)
    })
df_summary = pd.DataFrame(rows_summary)

# ------------------------------------------------------------
# 5.  Display / export the DataFrames
# ------------------------------------------------------------
print("\n=== Wilcoxon p-values (Months 1–3) ===")
print(df_wilcoxon.to_string(index=False))

print("\n=== Risk summary (Avg WCVaR and HOP score) ===")
print(df_summary.to_string(index=False))
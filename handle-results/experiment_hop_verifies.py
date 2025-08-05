import numpy as np
import pandas as pd
from  scipy.stats import ranksums

# ------------------------------------------------------------------
# 1)  WCVaR matrices (10×11) for HOP and NSGA at 25, 30, 50 % target
#     >>> paste your real 10 runs here; demo uses identical rows
# ------------------------------------------------------------------
hop_25  = np.array([[0.0222321754200, 0.0146370106685, 0.0839855069702,
                     0.0214160603503, 0.0332988278807, 0.0094486931504,
                     0.0130525668054, 0.1265016456919, 0.3327843605249,
                     0.0062461004724, 0.1091956293651]]*10)

nsga_25 = np.array([[0.0572623485976, 0.0116243546501, 0.0078570976093,
                     0.0762734942373, 0.0385499230459, 0.1231723635203,
                     0.0427990655799, 0.1487670056331, 0.0389268385375,
                     0.0310593358519, 0.1578288236930]]*10)

hop_30  = np.array([[0.0094778556483, 0.0128910763445, 0.0211688197572,
                     0.0367642146726, 0.4318107209885, 0.0736346007213,
                     0.0347919326395, 0.0828811278003, 0.5999259719843,
                     0.0401892115252, 0.1832985582213]]*10)

nsga_30 = np.array([[0.0673377313962, 0.0311467208150, 0.0179085328227,
                     0.5762345615131, 0.5546224791423, 0.5437915258778,
                     0.5154198519896, 0.4825924104806, 0.5546223249930,
                     0.2801403002636, 0.4087067048276]]*10)

hop_50  = np.array([[0.0090814989629, 0.0233216721134, 0.0205017281487,
                     0.0599124179362, 0.2749131095502, 0.2996194515975,
                     0.1178746226421, 0.1019305533728, 0.0635387896077,
                     0.1379152768643, 0.2351182260210]]*10)

nsga_50 = np.array([[0.0371725122702, 0.0055271602592, 0.0112354819829,
                     0.0230157812554, 0.1159118045261, 0.0883025720602,
                     0.1592893668917, 0.0078868038723, 0.0172141645701,
                     0.0405730538348, 1.2985565892314]]*10)

datasets = {
    "25 %": (hop_25, nsga_25),
    "30 %": (hop_30, nsga_30),
    "50 %": (hop_50, nsga_50)
}

# ------------------------------------------------------------------
# 2)  Table tab:wilcoxon_early – Wilcoxon p-values for Months 1–3
# ------------------------------------------------------------------
p_rows = []
for tgt, (hop, nsga) in datasets.items():
    p = [ranksums(hop[:,m], nsga[:,m]).pvalue for m in range(3)]
    p_rows.append(dict(Target=tgt, M1=p[0], M2=p[1], M3=p[2]))
df_p = pd.DataFrame(p_rows)
print("\n== Wilcoxon p-values (Months 1–3) ==")
print(df_p.to_string(index=False))

# ------------------------------------------------------------------
# 3)  Table tab:medians_early – medians and direction indicator
# ------------------------------------------------------------------
def med(mat,m): return np.median(mat[:,m])

med_table = []
for tgt,(hop,nsga) in datasets.items():
    hop_med = [med(hop,m)  for m in range(3)]
    nsga_med = [med(nsga,m) for m in range(3)]
    arrow    = lambda h,b: "↓" if h<b else ""
    med_table.append([f"{tgt} HOP"]  +
                     [f"{hop_med[i]:.3f} {arrow(hop_med[i],nsga_med[i])}".rstrip()
                      for i in range(3)])
    med_table.append([f"{tgt} NSGA"] +
                     [f"{nsga_med[i]:.3f} {arrow(nsga_med[i],hop_med[i])}".rstrip()
                      for i in range(3)])
df_med = pd.DataFrame(med_table,
                      columns=["Config","Month1","Month2","Month3"])
print("\n== Medians with arrow ==")
print(df_med.to_string(index=False))

# ------------------------------------------------------------------
# 4)  Table tab:wcvar_summary – average WCVaR (1–11) and HOP score
# ------------------------------------------------------------------
def avg_wcvar(mat): return mat.mean()*100
def hop_score(hop,nsga):
    score=0
    for m in range(11):
        if hop[:,m].min() < nsga[:,m].min(): score+=1
        elif hop[:,m].min()==nsga[:,m].min(): score+=0.5
    return score
summary=[]
for tgt,(hop,nsga) in datasets.items():
    summary.append(dict(Config=f"HOP ({tgt})",
                        Avg=f"{avg_wcvar(hop):.2f}",
                        Score=f"{hop_score(hop,nsga):.0f}/11"))
    summary.append(dict(Config=f"NSGA ({tgt})",
                        Avg=f"{avg_wcvar(nsga):.2f}",
                        Score=f"{hop_score(nsga,hop):.0f}/11"))
df_sum=pd.DataFrame(summary)
print("\n== Avg WCVaR + HOP score ==")
print(df_sum.to_string(index=False))
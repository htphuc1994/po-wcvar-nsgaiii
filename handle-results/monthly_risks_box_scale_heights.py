import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker

# -------- data 1 (NSGA-III) --------
data1 = {
    '1':[ 0.059,0.173,0.061,0.059,0.104,0.052,0.055,0.078,0.111 ],
    '2': [ 0.017,0.039,0.139,0.017,0.055,0.017,0.023,0.045,0.027 ],
    '3': [ 0.016,0.045,0.131,0.032,0.057,0.022,0.026,0.049,0.186 ],
    '4': [ 0.035,0.05,0.098,0.035,0.067,0.025,0.028,0.066,0.051 ],
    '5': [ 0.106,0.268,0.104,0.127,0.261,0.637,0.208,0.039,0.074 ],
    '6': [ 0.109,0.268,0.156,0.167,0.035,0.045,0.198,0.172,0.058 ],
    '7': [ 0.016,0.056,0.163,0.102,0.028,0.17,0.111,0.098,0.056 ],
    '8': [ 0.166,0.029,0.077,0.008,0.096,0.004,0.117,0.012,0.105 ],
    '9': [ 0.166,0.256,0.106,0.169,0.014,0.011,0.031,0.026,0.11 ],
    '10': [ 0.039,0.014,0.061,0.036,0.11,0.075,0.025,0.033,0.309 ],
    '11': [ 0.172,0.184,0.051,0.049,0.052,0.11,0.091,0.107,0.308 ],
}
df1 = pd.DataFrame(data1)

# -------- data 2 (NSGA-III-HOP) --------
data2 = {
    '1':[ 0.025,0.009,0.018,0.004,0.006,0.027,0.025,0.01,0.022,0.023 ],
    '2': [ 0.008,0.007,0.019,0.007,0.021,0.005,0.021,0.004,0.011,0.191 ],
    '3': [ 0.02,0.047,0.146,0.008,0.02,0.012,0.039,0.017,0.01,0.014 ],
    '4': [ 0.029,0.028,0.224,0.162,0.057,0.024,0.407,0.023,0.026,0.018 ],
    '5': [ 0.095,0.042,0.212,0.131,0.31,0.026,0.064,0.055,0.031,0.02 ],
    '6': [ 0.111,0.04,0.203,0.103,0.046,0.026,0.079,0.18,0.028,0.09 ],
    '7': [ 0.024,0.047,0.062,0.119,0.201,0.026,0.073,0.015,0.11,0.089 ],
    '8': [0.023,0.023,0.197,0.138,0.03,0.097,0.061,0.024,0.089,0.035 ],
    '9': [ 0.018,0.009,0.05,0.11,0.033,0.139,0.068,0.147,0.118,0.045 ],
    '10': [ 0.199,0.026,0.052,0.135,0.04,0.092,0.071,0.13,0.017,0.035 ],
    '11': [ 0.21,0.145,0.494,0.377,0.096,0.134,0.128,0.12,0.503,0.152 ],
}
df2 = pd.DataFrame(data2)

def make_box(ax, df, color, title=None):
    positions = np.linspace(1, len(df.columns), len(df.columns)) * 0.1
    box = ax.boxplot([df[c] for c in df.columns],
                     tick_labels=df.columns,
                     patch_artist=True,
                     widths=0.05,
                     positions=positions)
    ax.set_xlim(positions[0] - 0.1, positions[-1] + 0.1)
    ax.set_xlabel('Month', fontsize=24)
    ax.set_ylabel('WCVaR', fontsize=24)
    ax.tick_params(axis='both', labelsize=24)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # color styling
    plt.setp(box['boxes'],    facecolor=color, edgecolor=color)
    plt.setp(box['whiskers'], color=color)
    plt.setp(box['caps'],     color=color)
    plt.setp(box['medians'],  color='black')
    plt.setp(box['fliers'],   markeredgecolor=color, markerfacecolor='white')
    if title: ax.set_title(title, fontsize=14)

# --- build both axes with a SHARED Y-AXIS ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7), sharey=True)

# make_box(ax1, df1, "#FFB000", "NSGA-III")
# make_box(ax2, df2, "#FF3030", "NSGA-III-HOP")
make_box(ax1, df1, "#FFB000")
make_box(ax2, df2, "#FF3030")

# give both the exact same y-range (optional when sharey=True, but explicit is clear)
ymin = min(df1.values.min(), df2.values.min())
ymax = max(df1.values.max(), df2.values.max())
ax1.set_ylim(ymin, ymax)     # ax2 inherits via sharey

# (optional) drop the 0 tick
ticks = ax1.get_yticks()
# ticks = ticks[~np.isclose(ticks, 0)]
# ax1.yaxis.set_major_locator(mticker.FixedLocator(ticks))
# ax1.yaxis.set_minor_locator(mticker.NullLocator())
#
# plt.tight_layout()
# plt.show()

for ax in (ax1, ax2):
    ax.yaxis.set_major_locator(mticker.FixedLocator(ticks))
    ax.yaxis.set_minor_locator(mticker.NullLocator())
    ax.tick_params(axis='y', labelleft=True)  # show labels

# put the right subplot’s ticks on the right side (cleaner) (NEW)
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("left")
ax2.tick_params(axis='y', labelright=False, labelleft=True)

plt.tight_layout()
plt.show()
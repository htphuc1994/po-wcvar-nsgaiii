import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Bank Deposit', 'VND100 Million', 'VND1 Billion', 'VND10 Billion']
quarter_returns = [0.01812, 0.2172621761803, 0.1212324546927, 0.1082098667781]
half_year_returns = [0.0273055, 0.2399561300388, 0.2224426299007, 0.1184999557781]
year_returns = [0.0553567, 0.1490806605098, 0.2606602962920, 0.1683081132788]

# Convert to percentages
quarter_returns = [x * 100 for x in quarter_returns]
half_year_returns = [x * 100 for x in half_year_returns]
year_returns = [x * 100 for x in year_returns]

# Hatch patterns and colors
hatch_patterns = ['x', '//', '\\\\', '||']
# colors = ["#FFB000", "#FF3030", "#FF33CC", "#C000FF", "#00E5FF", "#00FFBF"]
colors = ["#FFB000", "#FF3030", "#FF33CC", "#C000FF"]
# colors = ['b', 'g', 'r', 'c']

# Titles and return sets
titles = ['3-month Investment', '6-month Investment', '12-month Investment']
returns = [quarter_returns, half_year_returns, year_returns]

# Plot each chart separately
for i in range(3):
    plt.figure(figsize=(6, 6))
    bars = plt.bar(range(len(categories)), returns[i], color=colors)

    for bar, hatch in zip(bars, hatch_patterns):
        bar.set_hatch(hatch)

    # plt.title(titles[i], fontsize=24)
    plt.xlabel('Strategy', fontsize=24)
    plt.ylabel('Return (%)', fontsize=24)
    plt.ylim(0, 30)
    plt.xticks(range(len(categories)), categories, fontsize=20, rotation=15, ha='right')
    plt.tick_params(axis='y', labelsize=20)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
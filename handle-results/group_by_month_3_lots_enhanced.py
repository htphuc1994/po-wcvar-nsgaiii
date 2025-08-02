import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Bank Deposit', 'VND100 Million', 'VND1 Billion', 'VND10 Billion']
quarter_returns = [0.01812, 0.1335135256481, 0.0895296482672, 0.0667413163178]
half_year_returns = [0.0273055, 0.2351092913214, 0.2854574844757, 0.2550369885965]
year_returns = [0.0553567, 0.2367174414905, 0.2795093648044, 0.2768005374401]

# Convert to percentages
quarter_returns = [x * 100 for x in quarter_returns]
half_year_returns = [x * 100 for x in half_year_returns]
year_returns = [x * 100 for x in year_returns]

# Hatch patterns and colors
hatch_patterns = ['x', '//', '\\\\', '||']
colors = ['b', 'g', 'r', 'c']

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
    plt.ylabel('Return (%)', fontsize=24)
    plt.ylim(0, 30)
    plt.xticks(range(len(categories)), categories, fontsize=20, rotation=15, ha='right')
    plt.tick_params(axis='y', labelsize=20)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
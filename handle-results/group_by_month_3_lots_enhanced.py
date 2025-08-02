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

# Create subplots
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot for each investment horizon
titles = ['3-month Investment', '6-month Investment', '12-month Investment']
returns = [quarter_returns, half_year_returns, year_returns]

for i in range(3):
    bars = axs[i].bar(range(len(categories)), returns[i], color=colors)
    for bar, hatch in zip(bars, hatch_patterns):
        bar.set_hatch(hatch)

    axs[i].set_title(titles[i], fontsize=24)
    axs[i].set_ylabel('Return (%)', fontsize=24)
    axs[i].set_ylim(0, 30)
    axs[i].set_xticks(range(len(categories)))
    axs[i].set_xticklabels(categories, fontsize=20, rotation=15, ha='right')
    axs[i].tick_params(axis='y', labelsize=20)
    axs[i].grid(True)

# Final layout
plt.tight_layout()
plt.show()
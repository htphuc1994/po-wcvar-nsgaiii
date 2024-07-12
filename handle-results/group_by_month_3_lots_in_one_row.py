import matplotlib.pyplot as plt
import numpy as np

# Generate sample data for the bar charts
# quarter
# quarter_returns = [0.01812, 0.29034, 0.16607, 0.25116]  # Generate random values between 0 and 1 for the columns
# # half year
# half_year_returns = [0.0273055, 0.20915, 0.13659, 0.22311]
# # 1 year
# year_returns = [0.0553567, 0.20202, 0.29067, 0.26279]

# categories = ['A', 'B', 'C', 'D', 'E']
categories = ['Bank deposit', 'VND100 million', 'VND1 billion', 'VND10 billion']
quarter_returns = [0.01812, 0.1335135256481, 0.0639493458844, 0.0640782257376]  # Generate random values between 0 and 1 for the columns
# half year
half_year_returns = [0.0273055, 0.1581248608910, 0.2479144845742, 0.1208689703379]
# 1 year
year_returns = [0.0553567, 0.2367174414905, 0.2154755791775, 0.2768005374401]
# values1 = [5, 7, 3, 8, 6]
# values2 = [6, 2, 7, 5, 8]
# values3 = [4, 9, 1, 3, 7]

# Define hatch patterns for each bar
hatch_patterns = ['x', '//', '\\\\', '||', '--']
hatch_patterns1 = ['/', '\\', '|', '-', '+']
hatch_patterns2 = ['+', 'x', 'o', 'O', '.']
hatch_patterns3 = ['*', '//', '\\\\', '||', '--']
colors = ['b', 'g', 'r', 'c', 'm']
# Create a figure and three subplots side by side
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot data on each subplot
bars1 = axs[0].bar(categories, quarter_returns, color=colors, label=categories)
for bar, hatch in zip(bars1, hatch_patterns):
    bar.set_hatch(hatch)
axs[0].set_title('3-month investment', fontsize=16)
axs[0].set_xticklabels(categories, fontsize=16)
axs[0].set_xticks([])
axs[0].set_ylim(0, 1)
axs[0].legend(fontsize=16)

bars2 = axs[1].bar(categories, half_year_returns, color=colors, label=categories)
for bar, hatch in zip(bars2, hatch_patterns):
    bar.set_hatch(hatch)
axs[1].set_title('6-month investment', fontsize=16)
axs[1].set_xticklabels(categories, fontsize=16)
axs[1].set_xticks([])
axs[1].set_ylim(0, 1)
axs[1].legend(fontsize=16)

bars3 = axs[2].bar(categories, year_returns, color=colors, label=categories)
for bar, hatch in zip(bars3, hatch_patterns):
    bar.set_hatch(hatch)
axs[2].set_title('12-month investment', fontsize=16)
axs[2].set_xticklabels(categories, fontsize=16)
axs[2].set_xticks([])
axs[2].set_ylim(0, 1)
axs[2].legend(fontsize=16)

for ax in axs:
    ax.tick_params(axis='y', labelsize=16)

# Adjust the layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
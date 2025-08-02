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
categories = ['Bank Deposit', 'VND100 Million', 'VND1 Billion', 'VND10 Billion']
quarter_returns = [0.01812, 0.1335135256481, 0.0895296482672, 0.0667413163178]  # Generate random values between 0 and 1 for the columns
# half year
half_year_returns = [0.0273055, 0.2351092913214, 0.2854574844757, 0.2550369885965]
# 1 year
year_returns = [0.0553567, 0.2367174414905, 0.2795093648044, 0.2768005374401]
#######

quarter_returns = [x * 100 for x in quarter_returns]
half_year_returns = [x * 100 for x in half_year_returns]
year_returns = [x * 100 for x in year_returns]
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
axs[0].set_title('3-month Investment', fontsize=24)
axs[0].set_xticklabels(categories, fontsize=24)
axs[0].set_xticks([])
axs[0].set_ylim(0, 60)
axs[0].set_ylabel('Return (%)', fontsize=24)
axs[0].legend(fontsize=24)
axs[0].grid(True)

bars2 = axs[1].bar(categories, half_year_returns, color=colors, label=categories)
for bar, hatch in zip(bars2, hatch_patterns):
    bar.set_hatch(hatch)
axs[1].set_title('6-month Investment', fontsize=24)
axs[1].set_xticklabels(categories, fontsize=24)
axs[1].set_xticks([])
axs[1].set_ylabel('Return (%)', fontsize=24)
axs[1].set_ylim(0, 60)
axs[1].legend(fontsize=24)
axs[1].grid(True)

bars3 = axs[2].bar(categories, year_returns, color=colors, label=categories)
for bar, hatch in zip(bars3, hatch_patterns):
    bar.set_hatch(hatch)
axs[2].set_title('12-month Investment', fontsize=24)
axs[2].set_xticklabels(categories, fontsize=24)
axs[2].set_xticks([])
axs[2].set_ylim(0, 60)
axs[2].set_ylabel('Return (%)', fontsize=24)
axs[2].legend(fontsize=24)
axs[2].grid(True)

for ax in axs:
    ax.tick_params(axis='y', labelsize=24)

# Adjust the layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()
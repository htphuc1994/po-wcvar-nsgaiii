import matplotlib.pyplot as plt
import numpy as np

# Generate sample data for the bar charts
categories = ['A', 'B', 'C', 'D', 'E']
values1 = [5, 7, 3, 8, 6]
values2 = [6, 2, 7, 5, 8]
values3 = [4, 9, 1, 3, 7]

# Define colors for each bar
colors1 = ['b', 'g', 'r', 'c', 'm']
colors2 = ['m', 'c', 'r', 'g', 'b']
colors3 = ['c', 'm', 'b', 'r', 'g']

# Create a figure and three subplots side by side
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# Plot data on each subplot with different colors for each bar
bars1 = axs[0].bar(categories, values1, color=colors1, label=['A', 'B', 'C', 'D', 'E'])
axs[0].set_title('Bar Chart 1')
axs[0].set_xticks([])

bars2 = axs[1].bar(categories, values2, color=colors2, label=['A', 'B', 'C', 'D', 'E'])
axs[1].set_title('Bar Chart 2')
axs[1].set_xticks([])

bars3 = axs[2].bar(categories, values3, color=colors3, label=['A', 'B', 'C', 'D', 'E'])
axs[2].set_title('Bar Chart 3')
axs[2].set_xticks([])

# Add custom annotations for each bar
for bar, category in zip(bars1, categories):
    axs[0].annotate(category,
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14)

for bar, category in zip(bars2, categories):
    axs[1].annotate(category,
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14)

for bar, category in zip(bars3, categories):
    axs[2].annotate(category,
                    xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=14)

# Increase the font size of the numbers on the vertical axis
for ax in axs:
    ax.tick_params(axis='y', labelsize=14)
    ax.legend(fontsize=14)

# Adjust the layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()

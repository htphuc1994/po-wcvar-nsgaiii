import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


title = 'Comparison of 12-month investment returns between original NSGA-III and NSGA-III-HOP'
data = {
    'NSGA-III': [0.2830699771319, 0.2945876112580, 0.2862585032739, 0.2953234537884, 0.2947644833541, 0.2931577721914, 0.2928360713971, 0.2977805674352, 0.2991261025856, 0.2796477667165, 0.2969142389917, 0.1312955210526, 0.2773281834585, 0.2965177492263, 0.2371295715973, 0.2905617346288, 0.2876729945130, 0.2760843453880, 0.2972363975206, 0.2780165561993],
    'NSGA-III-HOP': [0.2731321905440, 0.1305060748894, 0.2737019113705, 0.2789493405917, 0.1665656331398, 0.2380716437490, 0.2125696008018, 0.1475307594152, 0.2620937071234, 0.2818929713287, 0.2782570017785, 0.2260219340457, 0.2713028235863, 0.2341051770999, 0.1533213080745, 0.1863392002042, 0.2932702381460, 0.2962025882453, 0.2542960124920, 0.2539153691626]
}
# Convert to DataFrame
df = pd.DataFrame(data)

# Plot the box chart
plt.figure(figsize=(20, 10))
box = plt.boxplot([df[col] for col in df.columns], labels=df.columns, patch_artist=True)

# Define custom colors
colors = ['#1f77b4', 'lightgreen']
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# Customizing the plot
plt.title(title, fontsize=20, fontweight='bold')
plt.xlabel('Months', fontsize=20, fontweight='bold')
plt.ylabel('Values', fontsize=20, fontweight='bold')

# Get the current y-axis ticks
default_ticks = plt.gca().get_yticks()
data_min = df.min().min()  # Global minimum value in the dataset
data_max = df.max().max()  # Global maximum value in the dataset
y_custom_ticks = [data_min, data_max]
y_new_ticks = sorted(set(default_ticks).union(y_custom_ticks))  # Combine and sort
plt.yticks(y_new_ticks, fontsize=20)  # Apply custom y-ticks

plt.xticks(fontsize=20)  # Set font size for x-axis labels
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show the plot
plt.show()
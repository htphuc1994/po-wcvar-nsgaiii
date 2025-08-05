import matplotlib.pyplot as plt
import numpy as np


def plot_columns():
    # Define the data for four columns
    categories = ['100 Stocks, K = 100', '249 Stocks, K = 249', '249 Stocks, K = 124', '249 Stocks, K = 62']

    experiment_4_1_2_3 = [314214.48493003845, 557722.4588394165, 555989.6347522736, 556290.1990413666]  # execution time in minutes


    experiment_4_1_2_3 = [x/1000/60 for x in experiment_4_1_2_3]
    # Plot the bar chart
    plt.figure(figsize=(12, 12))
    # plt.bar(columns, values, color=['b', 'g', 'r', 'c'])

    hatch_patterns = ['x', '//', '\\\\', '||', '--']
    colors = ["#FFB000", "#FF3030", "#FF33CC", "#C000FF", "#00E5FF", "#00FFBF"]
    # colors = ['b', 'g', 'r', 'c', 'm']
    bars = plt.bar(categories, experiment_4_1_2_3, color=colors, label=categories)
    for bar, hatch in zip(bars, hatch_patterns):
        bar.set_hatch(hatch)
    # Set y-axis range from 0 to 1
    max_exe_time = np.max(experiment_4_1_2_3)
    plt.ylim(0, max_exe_time+1)
    plt.xticks(range(len(categories)), categories, fontsize=24, rotation=10, ha='right')

    # Get the current y-axis ticks
    default_ticks = plt.gca().get_yticks()
    # data_min = df.min().min()  # Global minimum value in the dataset
    # data_max = df.max().max()  # Global maximum value in the dataset
    y_custom_ticks = [max_exe_time]
    y_new_ticks = sorted(set(default_ticks).union(y_custom_ticks))  # Combine and sort
    y_new_ticks = [tick for tick in y_new_ticks if tick != 120]  # Remove -0.3 due to overlapped ticks

    plt.yticks(y_new_ticks, fontsize=24)  # Apply custom y-ticks
    plt.xlabel('Portfolio', fontsize=24)

    # Add labels and title
    plt.ylabel('Execution Time in Minutes', fontsize=24)

    plt.tick_params(axis='y', labelsize=24)
    plt.tick_params(axis='x', labelsize=24)
    # Show the plot
    plt.grid(True)

    plt.subplots_adjust(left=0.2, bottom=0.15)
    plt.show()

# Call the function to plot the columns
plot_columns()
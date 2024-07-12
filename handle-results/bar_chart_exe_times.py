import matplotlib.pyplot as plt
import numpy as np


def plot_columns():
    # Define the data for four columns
    categories = ['100 stocks, K = 100', '249 stocks, K = 249', '249 stocks, K = 124 (= 249 / 2)', '249 stocks, K = 62 (= 249 / 4)']

    experiment_4_1_2_3 = [505142.18521118164, 1110717.220067978, 2912739.1827106476, 7091574.80597496]  # execution time in minutes


    experiment_4_1_2_3 = [x/1000/60 for x in experiment_4_1_2_3]
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    # plt.bar(columns, values, color=['b', 'g', 'r', 'c'])

    hatch_patterns = ['x', '//', '\\\\', '||', '--']
    colors = ['b', 'g', 'r', 'c', 'm']
    bars = plt.bar(categories, experiment_4_1_2_3, color=colors, label=categories)
    for bar, hatch in zip(bars, hatch_patterns):
        bar.set_hatch(hatch)
    # Set y-axis range from 0 to 1
    max_exe_time = np.max(experiment_4_1_2_3)
    plt.ylim(0, max_exe_time)
    plt.xticks([])

    # Add labels and title
    plt.ylabel('Execution time in minutes', fontsize=16)
    plt.legend(fontsize=16)

    plt.tick_params(axis='y', labelsize=16)
    plt.tick_params(axis='x', labelsize=16)
    # Show the plot
    plt.grid(True)
    plt.show()

# Call the function to plot the columns
plot_columns()
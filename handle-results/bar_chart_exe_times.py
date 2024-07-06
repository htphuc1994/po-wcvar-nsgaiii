import matplotlib.pyplot as plt


# experiment_16_wcvar = [-0.05195, -0.02230, 0.00000, -0.06598, -0.15285, -0.17421, -0.18198, -0.19472, -0.23474, -0.22050, -0.15634]
# experiment_17_wcvar = [-0.06927, -0.05053, 0.00000, -0.09575, -0.13952, -0.14686, -0.15465, 0.00000, -0.16851, 0.00000, 0.00000]
# experiment_18_wcvar = [-0.07628, -0.05351, -0.06639, -0.09602, -0.22105, -0.25584, -0.28068, -0.29155, -0.25227, -0.17030, -0.20818]


def plot_columns():
    # Define the data for four columns
    categories = ['100 stocks, K = 100', '249 stocks, K = 249', '249 stocks, K = 249 / 2 = 124', '249 stocks, K = 249 / 4 = 62']

    experiment_4_1_2_3 = [8.55, 15.08, 16.18, 16.71]  # execution time in minutes

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    # plt.bar(columns, values, color=['b', 'g', 'r', 'c'])

    hatch_patterns = ['x', '//', '\\\\', '||', '--']
    colors = ['b', 'g', 'r', 'c', 'm']
    bars = plt.bar(categories, experiment_4_1_2_3, color=colors, label=categories)
    for bar, hatch in zip(bars, hatch_patterns):
        bar.set_hatch(hatch)
    # Set y-axis range from 0 to 1
    plt.ylim(0, 22)
    plt.xticks([])

    # Add labels and title
    plt.ylabel('Execution time in minutes', fontsize=14)
    plt.legend(fontsize=14)

    plt.tick_params(axis='y', labelsize=14)
    plt.tick_params(axis='x', labelsize=14)
    # Show the plot
    plt.show()

# Call the function to plot the columns
plot_columns()